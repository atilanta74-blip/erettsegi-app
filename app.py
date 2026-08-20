import io
import os
import random
import streamlit as st
import datetime
from fpdf import FPDF
from google import genai
from gtts import gTTS
import PyPDF2
import docx

# Konfiguráció
st.set_page_config(page_title="Astra Érettségi Központ", layout="wide")

# Stílusok
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e5e7eb; }
    .topic-card { background-color: #111827; border: 1px solid #374151; border-radius: 16px; padding: 25px; margin: 15px 0; }
    .chat-user { background: #4f46e5; color: white; padding: 10px; border-radius: 10px; margin: 5px; text-align: right; }
    .chat-ai { background: #1f2937; color: #e5e7eb; padding: 10px; border-radius: 10px; margin: 5px; }
</style>
""", unsafe_allow_html=True)

# --- ADATBÁZIS: Irodalom ---
tetelek_irodalom = {
    "Ókor": {"alcim": "Homérosz", "vazlat": "Eposz...", "szobeli": "Felelet...", "kviz": [{"k": "Homérosz írta az Iliászt?", "v": True, "m": "Igen."}]},
    "Középkor": {"alcim": "Dante", "vazlat": "Isteni színjáték...", "szobeli": "Felelet...", "kviz": [{"k": "Dante firenzei?", "v": True, "m": "Igen."}]},
    "Felvilágosodás": {"alcim": "Csokonai", "vazlat": "Életmű...", "szobeli": "Felelet...", "kviz": [{"k": "Csokonai szerelme Lilla?", "v": True, "m": "Igen."}]}
}
# (Itt folytatódhatna további 50 tétellel...)

# --- SEGÉDFÜGGVÉNYEK ---
def get_api_key(): return os.environ.get("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY", ""))

def szoveg_kinyeres(fajl):
    tartalom = ""
    try:
        if fajl.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(fajl)
            for page in reader.pages: tartalom += page.extract_text()
        elif fajl.name.endswith(".docx"):
            doc = docx.Document(fajl)
            for p in doc.paragraphs: tartalom += p.text
        else:
            tartalom = fajl.read().decode("utf-8", errors="ignore")
    except Exception as e: return f"Hiba: {e}"
    return tartalom

def ai_generalas(prompt, file_bytes=None, mime=None):
    client = genai.Client(api_key=get_api_key())
    c = [prompt]
    if file_bytes: c.append({"inline_data": {"mime_type": mime, "data": file_bytes}})
    return client.models.generate_content(model='gemini-2.0-flash', contents=c).text

# --- APP STRUKTÚRA ---
st.sidebar.title("📚 Menü")
tantargy = st.sidebar.selectbox("Tantárgy:", ["Irodalom", "Nyelvtan", "Történelem", "Matek"])
menupont = st.sidebar.radio("Funkciók:", ["Tételek", "Fájl feltöltés", "Flashcards", "Detektív", "Mentor"])

st.title(f"🎓 Érettségi Felkészítő - {tantargy}")

if menupont == "Tételek":
    # Itt egy nagy lista generálható dinamikusan a szótárakból
    valasztott = st.selectbox("Válassz tételcímet:", list(tetelek_irodalom.keys()))
    st.markdown(f"<div class='topic-card'><h3>{valasztott}</h3>{tetelek_irodalom[valasztott]['vazlat']}</div>", unsafe_allow_html=True)

elif menupont == "Fájl feltöltés":
    f = st.file_uploader("Fájl:", type=["txt", "pdf", "docx", "png", "jpg"])
    if f:
        if st.button("Elemzés"):
            with st.spinner("AI feldolgozás..."):
                if f.type.startswith("image"):
                    st.markdown(ai_generalas("Elemezd a képet és készíts kérdéseket:", f.read(), f.type))
                else:
                    st.markdown(ai_generalas(f"Készíts kvízt ebből: {szoveg_kinyeres(f)[:8000]}"))

elif menupont == "Mentor":
    k = st.text_input("Kérdés:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        v = ai_generalas(k)
        st.session_state.chat_history.append({"role": "ai", "text": v})
    for m in st.session_state.chat_history: st.markdown(m['text'])

# (Ide illesztheted be a további funkciók részletes logikáját, 
# a határ a csillagos ég, ha bővíteni akarod a 'tetelek_...' szótárakat!)
