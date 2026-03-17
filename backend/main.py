from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = FastAPI(title="Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

PORTFOLIO_DATA = {
    "name": "Przemysław Włodarczyk",
    "title": "Inżynier elektroniki i telekomunikacji",
    "bio": "Jestem świeżo po studiach inżynierskich. Rozwijam się w kierunku Python Developer.",
    "email": "Przemyslaw_wlodarczyk@outlook.com",
    "github": "https://github.com/wudjitzu24",
    "linkedin": "https://www.linkedin.com/in/przemwlodarczyk/",
    "projects": [
        {
            "name": "NotePsyche",
            "description": "Wirtualny psycholog. Możesz mówić do mikrofonu — mowa zamienia się w tekst i trafia do modelu LLM.",
            "tech": ["Python", "LLM", "Speech-to-Text"],
            "link": "https://github.com/wudjitzu24"
        }
    ]
}

@app.get("/")
def root():
    return {"status": "API działa"}

@app.get("/info")
def get_info():
    return PORTFOLIO_DATA

@app.post("/contact")
def send_contact(form: ContactForm):
    if len(form.message) < 10:
        raise HTTPException(status_code=400, detail="Wiadomość za krótka (min. 10 znaków)")

    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        raise HTTPException(status_code=500, detail="Brak konfiguracji SMTP")

    try:
        msg = MIMEMultipart()
        msg["From"] = gmail_user
        msg["To"] = "Przemyslaw_wlodarczyk@outlook.com"
        msg["Subject"] = f"Portfolio — wiadomość od {form.name}"

        body = f"""
Nowa wiadomość z portfolio

Imię: {form.name}
E-mail: {form.email}

Wiadomość:
{form.message}
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, "Przemyslaw_wlodarczyk@outlook.com", msg.as_string())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd wysyłki: {str(e)}")

    return {"status": "ok", "message": f"Dziękuję {form.name}! Odezwę się wkrótce."}