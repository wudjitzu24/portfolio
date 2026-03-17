from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import resend
import os

app = FastAPI(title="Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Klucz Resend — bierzemy ze zmiennej środowiskowej
resend.api_key = os.getenv("RESEND_API_KEY", "")

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

    if not resend.api_key:
        raise HTTPException(status_code=500, detail="Brak klucza RESEND_API_KEY")

    try:
        resend.Emails.send({
            "from": "Portfolio <onboarding@resend.dev>",  # działa bez własnej domeny
            "to": "Przemyslaw_wlodarczyk@outlook.com",
            "subject": f"Portfolio — wiadomość od {form.name}",
            "html": f"""
                <h2>Nowa wiadomość z portfolio</h2>
                <p><strong>Imię:</strong> {form.name}</p>
                <p><strong>E-mail:</strong> {form.email}</p>
                <p><strong>Wiadomość:</strong></p>
                <p>{form.message}</p>
            """
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd wysyłki: {str(e)}")

    return {"status": "ok", "message": f"Dziękuję {form.name}! Odezwę się wkrótce."}