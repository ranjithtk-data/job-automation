from companies import companies
from ai_filter import filter_jobs
from email_sender import send_email

jobs = []

for company in companies:

    job = {
        "company": company["name"],
        "title": "Data Analyst",
        "location": "Bengaluru",
        "link": company["url"]
    }

    jobs.append(job)

filtered_jobs = filter_jobs(jobs)

final_jobs = filtered_jobs[:20]

send_email(final_jobs)
