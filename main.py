from companies import companies
from scraper import scrape_company
from ai_filter import filter_jobs
from email_sender import send_email

all_jobs = []

for company in companies:

    print("Checking:", company["name"])

    jobs = scrape_company(company)

    all_jobs.extend(jobs)

filtered_jobs = filter_jobs(all_jobs)

final_jobs = filtered_jobs[:20]

print("Jobs found:", len(final_jobs))

if final_jobs:
    send_email(final_jobs)
