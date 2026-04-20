from scraper import scrape_jobs
from ai_filter import filter_jobs
from email_sender import send_email

print("Scraping jobs...")

jobs = scrape_jobs()

filtered_jobs = filter_jobs(jobs)

final_jobs = filtered_jobs[:20]

print("Jobs found:", len(final_jobs))

if final_jobs:
    send_email(final_jobs)
