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

    cards = soup.find_all("a", class_="tapItem")

    for card in cards[:20]:

        title = card.find("h2")
        company = card.find("span", class_="companyName")
        link = card.get("href")

        if title and company and link:

            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "location": "Bengaluru",
                "link": "https://in.indeed.com" + link
            })

    return jobs
