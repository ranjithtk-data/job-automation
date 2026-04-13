from email_sender import send_email
from datetime import datetime

print("=======================================================")
print("  Daily Job Automation – Bengaluru DA/BA Roles")
print(" ", datetime.now())
print("=======================================================")

jobs = []

# Job search links (these always work)
jobs.append("LinkedIn Data Analyst Jobs\nhttps://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=Bengaluru")
jobs.append("Indeed Data Analyst Jobs\nhttps://in.indeed.com/jobs?q=data+analyst&l=Bangalore")
jobs.append("Naukri Data Analyst Jobs\nhttps://www.naukri.com/data-analyst-jobs-in-bangalore")
jobs.append("LinkedIn Business Analyst Jobs\nhttps://www.linkedin.com/jobs/search/?keywords=business%20analyst&location=Bengaluru")
jobs.append("Naukri MIS Analyst Jobs\nhttps://www.naukri.com/mis-analyst-jobs-in-bangalore")

print(f"\n📦 Total job links prepared: {len(jobs)}")

print("\n📧 Preparing email...")

if len(jobs) == 0:
    email_body = """
⚠️ No Data Analyst / Business Analyst / MIS jobs were detected today in Bengaluru.

Please check these job portals manually:

LinkedIn
https://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=Bengaluru

Indeed
https://in.indeed.com/jobs?q=data+analyst&l=Bangalore

Naukri
https://www.naukri.com/data-analyst-jobs-in-bangalore
"""
else:
    email_body = "\n\n".join(jobs)

send_email(
    "Daily Job Report – Bengaluru",
    email_body
)

print("✅ Email sent successfully!")
print("\n🎉 Done!")
