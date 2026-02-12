import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("EMAIL credentials not found in .env file")

# --------------------------------------------------
# Setup Jinja Template Environment
# --------------------------------------------------
env = Environment(loader=FileSystemLoader("templates"))


# --------------------------------------------------
# Core Email Sender (Professional Version)
# --------------------------------------------------
def send_email(to_email, subject, html_body, plain_text):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"SmartPower Team <{EMAIL_ADDRESS}>"
    msg["To"] = to_email

    # Attach plain text first (important for spam filters)
    msg.attach(MIMEText(plain_text, "plain"))

    # Then attach HTML
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"✅ Email sent to {to_email}")


# --------------------------------------------------
# Email Verification
# --------------------------------------------------
def send_verification_email(email, name, token):

    action_url = f"http://127.0.0.1:5000/verify-email?token={token}"

    # Render HTML from template
    template = env.get_template("verify_email.html")
    html_body = template.render(
        name=name,
        action_url=action_url
    )

    # Plain text fallback
    plain_text = f"""
Hi {name},

To complete your SmartPower registration, please verify your email:

{action_url}

This link will expire in 24 hours.

If you did not create this account, please ignore this email.
"""

    send_email(
        to_email=email,
        subject="Verify your SmartPower account",
        html_body=html_body,
        plain_text=plain_text
    )
