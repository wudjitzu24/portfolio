from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Portfolio API", version="1.0")

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
            "link": "https://github.com/wudjitzu24/NotePsyche"
        }
    ]
}

@app.get("/")
def get_info():
    return PORTFOLIO_DATA

@app.post("/contact")
def send_contact(form: ContactForm):
    if len(form.message) < 10:
        raise HTTPException(status_code=400, detail="Wiadomość za krótka. Minimum 10 znaków.")
    
    print(f"Nowa wiadomość od {form.name} ({form.email}): {form.message}")

    return {"message": "ok", "message": f"Dziękuję {form.name}! Odezwę się wkrótce."}