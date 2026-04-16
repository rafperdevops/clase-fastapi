import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_otp_email(email: str, otp_code: str):
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        raise Exception("BREVO_API_KEY no configurada en .env")

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "sender": {"name": "App", "email": "noreply@app.com"},
        "to": [{"email": email}],
        "subject": "Tu código de verificación",
        "htmlContent": f"<h1>Tu código OTP: <b>{otp_code}</b></h1><p>Expira en 5 minutos.</p>"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 201