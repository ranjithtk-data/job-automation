# ─────────────────────────────────────────────────────────────
#  main.py  ·  Fetch → Deduplicate → Score → Email
# ─────────────────────────────────────────────────────────────

import re
import time
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

from companies import (
    TARGET_COMPANIES, JOB_ROLES, SEARCH_QUERIES,
    LOCATION, LOCATION_ALT, MAX_JOBS, DAYS_OLD,
)
from email_sender import send_email

# Pre-process for fast matching
_COMPANIES_LOWER = [c.lower() for c in TARGET_COMPANIES]
_ROLES_LOWER     = [r.lower() for r in JOB_ROLES]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# ── Scoring ───────────────────────────────────────────────────

def score_job(title: str, company: str) -> tuple[int, bool]:
    """Return (score, is_priority_company)."""
    title_l   = title.lower()
    company_l = company.lower()

    score    = 0
    priority = False

    # Role match
    for role in _ROLES_LOWER:
        if role in title_l:
            score += 3
            break

    # Priority company
    for comp in _COMPANIES_LOWER:
        if comp in company_l:
            score += 5
            priority = True
            break

    # Location keywords already filtered, give small base
    score += 1

    return score, priority


# ── Source 1 : Indeed India RSS ───────────────────────────────

def fetch_indeed(query: str) -> list[dict]:
    jobs = []
    url  = (
        f"https://www.indeed.co.in/rss"
        f"?q={query.replace(' ', '+')}"
        f"&l={LOCATION}"
        f"&sort=date"
        f"&fromage={DAYS_OLD}"
    )
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title   = entry.get("title", "").strip()
            link    = entry.get("link", "")
            summary = entry.get("summary", "")

            # Extract company from title pattern "Job Title - Company"
            company = ""
            if " - " in title:
                parts   = title.rsplit(" - ", 1)
                title   = parts[0].strip()
                company = parts[1].strip()

            if not company:
                company = "Company on Indeed"

            if not _is_relevant(title):
                continue

            score, priority = score_job(title, company)
            jobs.append({
                "title":    title,
                "company":  company,
                "location": LOCATION,
                "link":     link,
                "source":   "Indeed",
                "score":    score,
                "priority": priority,
                "key":      _dedup_key(title, company),
            })
    except Exception as exc:
        print(f"⚠️  Indeed error ({query}): {exc}")
    return jobs


# ── Source 2 : Naukri.com ─────────────────────────────────────

def fetch_naukri(query: str) -> list[dict]:
    jobs = []
    slug = query.replace(" ", "-").lower()
    url  = f"https://www.naukri.com/{slug}-jobs-in-bengaluru"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        if resp.status_code != 200:
            print(f"⚠️  Naukri returned {resp.status_code} for '{query}'")
            return jobs

        soup = BeautifulSoup(resp.text, "lxml")

        # Naukri wraps each listing in <article class="jobTuple …">
        cards = soup.select("article.jobTuple") or soup.select("div.jobTuple")
        if not cards:
            # Fallback: try JSON-LD structured data
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    import json
                    data = json.loads(script.string or "")
                    if isinstance(data, list):
                        items = data
                    elif data.get("@type") == "ItemList":
                        items = data.get("itemListElement", [])
                    else:
                        continue
                    for item in items[:5]:
                        j = item.get("item", item)
                        t = j.get("title", "") or j.get("name", "")
                        c = j.get("hiringOrganization", {}).get("name", "Naukri Company")
                        l = j.get("url", url)
                        if t and _is_relevant(t):
                            sc, pr = score_job(t, c)
                            jobs.append({
                                "title":    t,
                                "company":  c,
                                "location": LOCATION,
                                "link":     l,
                                "source":   "Naukri",
                                "score":    sc,
                                "priority": pr,
                                "key":      _dedup_key(t, c),
                            })
                except Exception:
                    pass
            return jobs

        for card in cards[:8]:
            try:
                title_el   = card.select_one("a.title")
                company_el = card.select_one("a.subTitle") or card.select_one(".companyInfo a")
                if not title_el:
                    continue

                title   = title_el.get_text(strip=True)
                company = company_el.get_text(strip=True) if company_el else "Naukri Company"
                link    = title_el.get("href", url)

                if not _is_relevant(title):
                    continue

                score, priority = score_job(title, company)
                jobs.append({
                    "title":    title,
                    "company":  company,
                    "location": LOCATION,
                    "link":     link,
                    "source":   "Naukri",
                    "score":    score,
                    "priority": priority,
                    "key":      _dedup_key(title, company),
                })
            except Exception:
                pass

    except Exception as exc:
        print(f"⚠️  Naukri error ({query}): {exc}")

    return jobs


# ── Source 3 : TimesJobs RSS ──────────────────────────────────

def fetch_timesjobs(query: str) -> list[dict]:
    jobs = []
    url  = (
        "https://www.timesjobs.com/jobfeed/rss-jobs.htm"
        f"?sk={query.replace(' ', '%20')}"
        f"&lid=3552"          # Bengaluru location ID
        "&postWeek=1"
    )
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title   = entry.get("title", "").strip()
            link    = entry.get("link", "")
            summary = entry.get("summary", "")

            company = ""
            soup_s  = BeautifulSoup(summary, "lxml")
            for tag in soup_s.find_all("b"):
                text = tag.get_text(strip=True)
                if text and len(text) < 60:
                    company = text
                    break
            company = company or "TimesJobs Company"

            if not _is_relevant(title):
                continue

            score, priority = score_job(title, company)
            jobs.append({
                "title":    title,
                "company":  company,
                "location": LOCATION,
                "link":     link,
                "source":   "TimesJobs",
                "score":    score,
                "priority": priority,
                "key":      _dedup_key(title, company),
            })
    except Exception as exc:
        print(f"⚠️  TimesJobs error ({query}): {exc}")
    return jobs


# ── Helpers ───────────────────────────────────────────────────

def _is_relevant(title: str) -> bool:
    """Return True if title matches at least one target role."""
    title_l = title.lower()
    return any(role in title_l for role in _ROLES_LOWER)


def _dedup_key(title: str, company: str) -> str:
    """Normalise strings for deduplication."""
    combined = f"{title.lower().strip()} | {company.lower().strip()}"
    return re.sub(r"\s+", " ", combined)


def deduplicate(jobs: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for job in jobs:
        k = job["key"]
        if k not in seen:
            seen.add(k)
            unique.append(job)
    return unique


# ── Orchestrator ──────────────────────────────────────────────

def collect_all_jobs() -> list[dict]:
    all_jobs = []

    for query in SEARCH_QUERIES:
        print(f"\n🔍 Fetching Indeed  → '{query}'")
        all_jobs.extend(fetch_indeed(query))
        time.sleep(1.5)

        print(f"🔍 Fetching Naukri  → '{query}'")
        all_jobs.extend(fetch_naukri(query))
        time.sleep(1.5)

        print(f"🔍 Fetching TimesJobs → '{query}'")
        all_jobs.extend(fetch_timesjobs(query))
        time.sleep(1.0)

    print(f"\n📦 Raw collected: {len(all_jobs)} jobs")

    # Deduplicate
    jobs = deduplicate(all_jobs)
    print(f"✂️  After deduplication: {len(jobs)} jobs")

    # Sort by score descending
    jobs.sort(key=lambda j: j["score"], reverse=True)

    # Take top N
    top_jobs = jobs[:MAX_JOBS]
    print(f"🏆 Top {len(top_jobs)} jobs selected for email")

    return top_jobs


# ── Entry point ───────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Daily Job Automation – Bengaluru DA/BA Roles")
    print(f"  {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print("=" * 55)

    jobs = collect_all_jobs()

    if jobs:
        for i, j in enumerate(jobs, 1):
            flag = "⭐" if j["priority"] else "  "
            print(f"  {flag} {i:02}. [{j['source']:10}] {j['title'][:40]:40} | {j['company'][:25]}")
    else:
        print("⚠️  No matching jobs found today.")

    print("\n📧 Preparing email...")
    send_email(jobs)
    print("\n🎉 Done!")
