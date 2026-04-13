# ─────────────────────────────────────────────────────────────
#  email_sender.py  ·  Build & send the daily HTML job digest
# ─────────────────────────────────────────────────────────────

import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from companies import SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_SUBJECT


# ── HTML builder ──────────────────────────────────────────────

def build_html(jobs: list[dict]) -> str:
    today = datetime.now().strftime("%A, %d %B %Y")

    # One card per job
    cards_html = ""
    for i, job in enumerate(jobs, start=1):
        badge_color = "#1a73e8" if job.get("priority") else "#5f6368"
        source_tag  = job.get("source", "Portal")
        priority_label = (
            '<span style="background:#e8f0fe;color:#1a73e8;'
            'font-size:11px;font-weight:700;padding:2px 8px;'
            'border-radius:20px;margin-left:8px;">⭐ Priority</span>'
            if job.get("priority") else ""
        )

        cards_html += f"""
        <tr>
          <td style="padding:0 0 16px 0;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#ffffff;border:1px solid #e0e0e0;
                          border-radius:10px;overflow:hidden;">
              <tr>
                <td style="background:{badge_color};width:6px;padding:0;"></td>
                <td style="padding:18px 20px;">

                  <!-- Job number + title -->
                  <p style="margin:0 0 4px 0;font-size:13px;color:#9aa0a6;">
                    #{i} &nbsp;·&nbsp; {source_tag}
                  </p>
                  <p style="margin:0 0 6px 0;font-size:17px;font-weight:700;
                             color:#202124;line-height:1.3;">
                    {job['title']}{priority_label}
                  </p>

                  <!-- Company & location -->
                  <p style="margin:0 0 14px 0;font-size:14px;color:#5f6368;">
                    🏢 <strong>{job['company']}</strong>
                    &nbsp;&nbsp;
                    📍 {job['location']}
                  </p>

                  <!-- Apply button -->
                  <a href="{job['link']}"
                     style="display:inline-block;background:#1a73e8;color:#ffffff;
                            font-size:13px;font-weight:600;padding:9px 22px;
                            border-radius:6px;text-decoration:none;
                            letter-spacing:0.3px;">
                    Apply Now →
                  </a>

                </td>
              </tr>
            </table>
          </td>
        </tr>
        """

    priority_count = sum(1 for j in jobs if j.get("priority"))

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f1f3f4;font-family:'Segoe UI',Arial,sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f3f4;padding:30px 0;">
    <tr><td align="center">

      <!-- Card container -->
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;width:100%;">

        <!-- ── Header ── -->
        <tr>
          <td style="background:linear-gradient(135deg,#1a73e8 0%,#0d47a1 100%);
                     border-radius:12px 12px 0 0;padding:32px 32px 28px;">
            <p style="margin:0 0 4px 0;font-size:13px;color:#a8c7fa;letter-spacing:1.5px;
                      text-transform:uppercase;font-weight:600;">Daily Job Digest</p>
            <h1 style="margin:0 0 8px 0;font-size:24px;font-weight:800;color:#ffffff;
                       line-height:1.2;">
              Data &amp; Business Analyst<br>Jobs · Bengaluru
            </h1>
            <p style="margin:0;font-size:13px;color:#c2d8fd;">{today}</p>
          </td>
        </tr>

        <!-- ── Stats bar ── -->
        <tr>
          <td style="background:#e8f0fe;padding:12px 32px;border-bottom:1px solid #d2e3fc;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="font-size:13px;color:#1a73e8;font-weight:600;">
                  📋 {len(jobs)} jobs found
                </td>
                <td align="right" style="font-size:13px;color:#1a73e8;font-weight:600;">
                  ⭐ {priority_count} priority companies
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ── Job cards ── -->
        <tr>
          <td style="background:#f1f3f4;padding:20px 24px 8px;">
            <table width="100%" cellpadding="0" cellspacing="0">
              {cards_html}
            </table>
          </td>
        </tr>

        <!-- ── Footer ── -->
        <tr>
          <td style="background:#ffffff;border:1px solid #e0e0e0;border-radius:0 0 12px 12px;
                     padding:20px 32px;text-align:center;">
            <p style="margin:0 0 6px 0;font-size:12px;color:#9aa0a6;">
              Sources: Indeed · Naukri · TimesJobs &nbsp;|&nbsp; Auto-sent by GitHub Actions
            </p>
            <p style="margin:0;font-size:11px;color:#bdc1c6;">
              Filtered for Bengaluru · Roles: Data Analyst, Business Analyst, MIS Analyst, Reporting Analyst
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>

</body>
</html>
"""
    return html


# ── Sender ────────────────────────────────────────────────────

def send_email(jobs: list[dict]) -> None:
    """Build and send the HTML digest email via Gmail SMTP."""

    gmail_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    if not gmail_password:
        raise ValueError("GMAIL_APP_PASSWORD environment variable is not set.")

    if not jobs:
        print("⚠️  No jobs found today – skipping email.")
        return

    html_body = build_html(jobs)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL

    # Plain-text fallback
    plain = "\n".join(
        f"{i}. {j['title']} | {j['company']} | {j['location']} | {j['link']}"
        for i, j in enumerate(jobs, 1)
    )
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    print(f"📤 Sending email to {RECEIVER_EMAIL}...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, gmail_password)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    print(f"✅ Email sent successfully with {len(jobs)} jobs!")
