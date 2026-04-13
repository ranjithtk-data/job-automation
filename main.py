import requests
from bs4 import BeautifulSoup
from email_sender import send_email

keywords = [
    "data analyst",
    "junior data analyst",
    "mis analyst",
    "mis executive",
    "reporting analyst",
    "business analyst",
    "analytics associate",
    "data associate"
]

location = "Bangalore"

job_links = []

def search_indeed():
    for keyword in keywords:
        url = f"https://in.indeed.com/jobs?q={keyword.replace(' ','+')}&l={location}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for job in soup.select("a.tapItem"):
            title = job.select_one("h2").text.strip()
            link = "https://in.indeed.com" + job.get("href")
            job_links.append(f"{title}\n{link}")

def search_naukri():
    for keyword in keywords:
        url = f"https://www.naukri.com/{keyword.replace(' ','-')}-jobs-in-{location}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for job in soup.select("a.title"):
            title = job.text.strip()
            link = job.get("href")
            job_links.append(f"{title}\n{link}")

def search_linkedin():
    for keyword in keywords:
        link = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ','%20')}&location=Bangalore"
        job_links.append(f"LinkedIn search: {keyword}\n{link}")

def main():
    print("Collecting jobs...")

    search_indeed()
    search_naukri()
    search_linkedin()

    unique_jobs = list(set(job_links))

    jobs_text = "\n\n".join(unique_jobs[:20])

    send_email(
        "Daily Data Analyst Jobs – Bangalore",
        jobs_text
    )

if __name__ == "__main__":
    main()
