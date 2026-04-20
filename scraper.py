import requests
from bs4 import BeautifulSoup

def scrape_jobs():

    url = "https://in.indeed.com/jobs?q=data+analyst&l=Bengaluru"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    cards = soup.select("div.job_seen_beacon")

    for card in cards[:20]:

        title = card.select_one("h2.jobTitle")
        company = card.select_one("span.companyName")
        link = card.select_one("a")

        if title and company and link:

            job_link = "https://in.indeed.com" + link.get("href")

            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "location": "Bengaluru",
                "link": job_link
            })

    return jobs
