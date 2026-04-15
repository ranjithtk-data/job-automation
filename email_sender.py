import smtplib
from email.mime.text import MIMEText
import os


def send_email(subject, body):

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_ADDRESS")

    print("Sender:", sender)
    print("Receiver:", receiver)

    if not sender or not password:
        print("❌ Email credentials not found.")
        return

    if not body:
        body = "No jobs were detected today."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender, password)

        server.sendmail(sender, receiver, msg.as_string())

        server.quit()

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Email sending failed:", e)
