import smtplib
import os
from email.mime.text import MIMEText

def send_email(jobs):

    sender = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    html = """
    <html>
    <head>
    <style>

    body{
        font-family: Arial;
        background:#f4f6f8;
        padding:20px;
    }

    .container{
        max-width:600px;
        margin:auto;
        background:white;
        padding:20px;
        border-radius:8px;
        box-shadow:0 2px 10px rgba(0,0,0,0.1);
    }

    .job{
        border-bottom:1px solid #eee;
        padding:15px 0;
    }

    .company{
        font-size:18px;
        font-weight:bold;
        color:#333;
    }

    .title{
        color:#555;
        margin:5px 0;
    }

    .apply{
        display:inline-block;
        padding:8px 12px;
        background:#0073e6;
        color:white;
        text-decoration:none;
        border-radius:5px;
        font-size:14px;
    }

    </style>
    </head>
    <body>

    <div class="container">
    <h2>📊 Bengaluru Data / Business Analyst Jobs</h2>
    """

    for job in jobs:

        html += f"""
        <div class="job">
            <div class="company">{job['company']}</div>
            <div class="title">{job['title']}</div>
            <a class="apply" href="{job['link']}">Apply Now</a>
        </div>
        """

    html += """
    </div>
    </body>
    </html>
    """

    msg = MIMEText(html, "html")

    msg["Subject"] = "Daily Bengaluru Analyst Jobs"
    msg["From"] = sender
    msg["To"] = sender

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)

    server.sendmail(sender, sender, msg.as_string())

    server.quit()
