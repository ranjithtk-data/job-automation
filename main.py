from email_sender import send_email

jobs = []

def fetch_jobs():
    # Example job searches
    jobs.append("LinkedIn Data Analyst Jobs\nhttps://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=Bengaluru")
    jobs.append("Indeed Data Analyst Jobs\nhttps://in.indeed.com/jobs?q=data+analyst&l=Bangalore")
    jobs.append("Naukri Data Analyst Jobs\nhttps://www.naukri.com/data-analyst-jobs-in-bangalore")

def main():

    print("🔍 Collecting jobs...")
    fetch_jobs()

    print(f"📦 Total jobs found: {len(jobs)}")

    if len(jobs) == 0:
        email_body = """
No Data Analyst / MIS / Business Analyst jobs were detected today in Bengaluru.

Please check job portals manually:

LinkedIn
https://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=Bengaluru

Indeed
https://in.indeed.com/jobs?q=data+analyst&l=Bangalore

Naukri
https://www.naukri.com/data-analyst-jobs-in-bangalore
"""
    else:
        email_body = "\n\n".join(jobs)

    print("📧 Sending email...")

    send_email(
        "Daily Job Report – Bengaluru",
        email_body
    )

    print("✅ Email sent!")

if __name__ == "__main__":
    main()
