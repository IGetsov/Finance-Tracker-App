import os
import ssl
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_email(recepient_email: str, subject: str, body: str) -> bool:
    """Send an email using Gmail SMTP"""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recepient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attempt send notification via mail client or send an error
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(user=SENDER_EMAIL, password=SENDER_PASSWORD)
            server.sendmail(from_addr=SENDER_EMAIL, to_addrs=recepient_email, msg=msg.as_string())
        return True
    except Exception as e:
        print(f'Error sending email: {e}')
        return False