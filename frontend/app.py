import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.write(f"API_URL: {API_URL}")

try:
    r = requests.get(f"{API_URL}/info", timeout=60)
    st.write(f"Status: {r.status_code}")
    st.write(r.json())
except Exception as e:
    st.write(f"Błąd: {e}")

st.set_page_config(
    page_title="Przemysław Włodarczyk | Portfolio",
    page_icon="⚡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0d0d0f; color: #e8e6df; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px; padding: 3rem 2.5rem; margin-bottom: 2rem;
    border: 1px solid #2a2a4a;
}
.hero h1 { font-size: 2.6rem; font-weight: 700; color: #fff; margin: 0 0 .4rem; }
.hero h2 { font-size: 1.15rem; font-weight: 400; color: #7ecfff; margin: 0 0 1.2rem; }
.hero p  { color: #b0aec8; line-height: 1.7; }

.badge {
    display: inline-block;
    background: rgba(126,207,255,0.12); color: #7ecfff;
    border: 1px solid rgba(126,207,255,0.25);
    border-radius: 20px; padding: .25rem .85rem;
    font-size: .82rem; font-weight: 600; margin-right: .4rem;
}

.section-card {
    background: #141418; border: 1px solid #2a2a3a;
    border-radius: 12px; padding: 1.6rem 1.8rem; margin-bottom: 1.2rem;
}
.section-title {
    font-size: .85rem; font-weight: 700; color: #7ecfff;
    letter-spacing: .08em; text-transform: uppercase; margin-bottom: 1rem;
}

.project-card {
    background: #1a1a24; border: 1px solid #2e2e44;
    border-left: 3px solid #7ecfff;
    border-radius: 10px; padding: 1.2rem 1.4rem; margin-bottom: .8rem;
}
.project-name { font-size: 1.05rem; font-weight: 700; color: #fff; }
.project-desc { color: #9a98b2; font-size: .93rem; margin: .4rem 0 .7rem; line-height: 1.6; }
.tech-tag {
    display: inline-block; background: rgba(255,255,255,0.06);
    color: #c8c6de; border-radius: 6px;
    padding: .15rem .55rem; font-size: .78rem; margin-right: .3rem;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)
def fetch_portfolio():
    try:
        r = requests.get(f"{API_URL}/info", timeout=30)
        return r.json()
    except:
        return None
    

data = fetch_portfolio()

if data is None:
    st.error("Nie można połączyć się z API. Czy backend działa na porcie 8000?")
    st.stop()

# Wyciągnięcie danych do zmiennych — unikamy apostrofów w f-stringach
name     = data["name"]
title    = data["title"]
bio      = data["bio"]
email    = data["email"]
github   = data["github"]
linkedin = data["linkedin"]
projects = data["projects"]

# --- HERO ---
st.markdown(f"""
<div class="hero">
  <h1>👋 Cześć, jestem {name}</h1>
  <h2>{title}</h2>
  <p>{bio}</p>
  <div style="margin-top:1.4rem">
    <span class="badge">Python</span>
    <span class="badge">FastAPI</span>
    <span class="badge">Elektronika</span>
    <span class="badge">Telekomunikacja</span>
    <span class="badge">LLM / AI</span>
  </div>
</div>
""", unsafe_allow_html=True)

# --- KOLUMNY ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">O mnie</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#b0aec8;line-height:1.7">{bio}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Kontakt</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <p><a href="mailto:{email}" style="color:#7ecfff">✉️ {email}</a></p>
    <p style="margin-top:.6rem"><a href="{github}" target="_blank" style="color:#7ecfff">🐙 GitHub</a></p>
    <p style="margin-top:.6rem"><a href="{linkedin}" target="_blank" style="color:#7ecfff">💼 LinkedIn</a></p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Projekty</div>', unsafe_allow_html=True)
    for proj in projects:
        proj_name = proj["name"]
        proj_desc = proj["description"]
        proj_link = proj["link"]
        tags = " ".join(f'<span class="tech-tag">{t}</span>' for t in proj["tech"])
        st.markdown(f"""
        <div class="project-card">
          <div class="project-name">{proj_name}</div>
          <div class="project-desc">{proj_desc}</div>
          <div>{tags}</div>
          <div style="margin-top:.7rem">
            <a href="{proj_link}" target="_blank" style="font-size:.85rem;color:#7ecfff">→ Zobacz na GitHub</a>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- FORMULARZ ---
st.markdown("---")
st.markdown('<div class="section-title">Napisz do mnie</div>', unsafe_allow_html=True)

with st.form("contact_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        form_name = st.text_input("Imię", placeholder="Jan Kowalski")
    with c2:
        form_email = st.text_input("E-mail", placeholder="jan@example.com")
    message = st.text_area("Wiadomość", height=130)
    submitted = st.form_submit_button("Wyślij wiadomość", use_container_width=True)

if submitted:
    if not form_name or not form_email or not message:
        st.warning("Uzupełnij wszystkie pola.")
    else:
        try:
            resp = requests.post(f"{API_URL}/contact", json={
                "name": form_name, "email": form_email, "message": message
            }, timeout=10)
            if resp.status_code == 200:
                st.success(resp.json()["message"])
            else:
                st.error(resp.json().get("detail", "Błąd serwera"))
        except Exception as e:
            st.error(f"Błąd połączenia z API: {e}")