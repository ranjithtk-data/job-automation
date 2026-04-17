import smtplib
import os
from email.mime.text import MIMEText

def send_email(jobs):

    sender = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    html = "<h2>Bengaluru Data / Business Analyst Jobs</h2>"

    for job in jobs:

        html += f"""
        <p>
        <b>{job['company']}</b><br>
        {job['title']}<br>
        <a href="{job['link']}">Apply Here</a>
        </p>
        """

    msg = MIMEText(html, "html")

    msg["Subject"] = f"{len(jobs)} New Analyst Jobs – Bengaluru"
    msg["From"] = sender
    msg["To"] = sender

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)

    server.sendmail(sender, sender, msg.as_string())

    server.quit()
