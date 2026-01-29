import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "iamalvinnjoseph@gmail.com"
APP_PASSWORD = "eennxatlvbmddzax"

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg.set_content(f"Your OTP is {otp}. It is valid for 5 minutes.")
    msg["Subject"] = "OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
