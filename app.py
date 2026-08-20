import io
import os
import json
import streamlit as st
from google import genai
from gtts import gTTS
import PyPDF2
import docx
from PIL import Image

# --- BEÁLLÍTÁSOK ---
st.set_page_config(page_title="VizsgaMester", layout="wide")

def get_api_key():
    return os.environ.get("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY", ""))

# --- STÍLUSOK (Bal felső 'Menü' felirattal) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #f3f4f6; }
    .menu-label { position: fixed; top: 14px; left: 45px; font-size: 14px; font-weight: 600; color: #818cf8; z-index: 999999; pointer-events: none; }
    .topic-card { background-color: #111827; border: 1px solid #374151; border-radius: 18px; padding: 28px; }
    .deep-text { background-color: #111827; color: white !important; padding: 32px; border-radius: 14px; line-height: 1.8; }
    .flashcard { background: #1e1b4b; border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; }
</style>
<div class="menu-label">Menü</div>
""", unsafe_allow_html=True)

# --- AI ÉS FÁJLKEZELÉS ---
def ai_call(payload):
    try:
        client = genai.Client(api_key=get_api_key())
        return client.models.generate_content(model='gemini-3.6-flash', contents=payload).text
    except Exception as e: return f"Hiba: {e}"

def read_doc(f):
    if f.type == "application/pdf": return "\n".join([p.extract_text() for p in PyPDF2.PdfReader(f).pages])
    if "wordprocessingml" in f.type: return "\n".join([p.text for p in docx.Document(f).paragraphs])
    return f.getvalue().decode("utf-8", errors="ignore")

# --- ADATBÁZIS ---
db = {
    "Magyar Irodalom": {"temak": ["Eposzok", "Petőfi", "Ady"], "flash": ["Petőfi: Szeptember végén", "Ady: Új vizeken"]},
    "Történelem": {"temak": ["Athén", "Róma", "Honfoglalás"], "flash": ["1000: Államalapítás", "1222: Aranybulla"]},
    "Matek": {"temak": ["Algebra", "Geometria", "Valószínűség"], "flash": ["Pitagorasz-tétel", "Másodfokú megoldóképlet"]}
}

# --- UI ---
st.sidebar.title("📚 VizsgaMester")
tantargy = st.sidebar.selectbox("Tantárgy:", list(db.keys()))
modul = st.sidebar.radio("Modul:", ["Tételek", "Fájl Elemzés", "Kvíz Labor", "Villámkártyák", "AI Mentor"])

st.title(f"🎓 {tantargy} Központ")

if modul == "Tételek":
    tétel = st.selectbox("Válassz:", db[tantargy]["temak"])
    if st.button("Kifejtés"):
        st.markdown(f"<div class='deep-text'>{ai_call([f'Írj érettségi tételt: {tétel} ({tantargy})'])}</div>", unsafe_allow_html=True)

elif modul == "Fájl Elemzés":
    fajl = st.file_uploader("Feltöltés:", type=["jpg", "png", "pdf", "docx", "txt"])
    if fajl and st.button("Elemzés"):
        payload = [Image.open(fajl), "Elemezd a képet:"] if fajl.type.startswith("image") else [f"Elemezd: {read_doc(fajl)}"]
        st.session_state.res = ai_call(payload)
        st.markdown(f"<div class='deep-text'>{st.session_state.res}</div>", unsafe_allow_html=True)

elif modul == "Kvíz Labor":
    if "res" in st.session_state and st.button("Kvíz generálása"):
        res = ai_call([f"Készíts 5 kvízkérdést JSON-ban: {st.session_state.res}"])
        try:
            data = json.loads(res.replace("```json", "").replace("```", "").strip())
            for i, q in enumerate(data):
                st.write(f"**{i+1}. {q['question']}**")
                if st.radio("Válasz:", q['options'], key=f"q{i}", index=None) == q['answer']: st.success("Helyes!")
                else: st.warning(f"Helytelen! Helyes: {q['answer']}")
        except: st.error("Generálási hiba.")

elif modul == "Villámkártyák":
    k = random.choice(db[tantargy]["flash"])
    st.markdown(f"<div class='flashcard'>❓ {k}</div>", unsafe_allow_html=True)
    if st.button("Következő"): st.rerun()

elif modul == "AI Mentor":
    if "chat" not in st.session_state: st.session_state.chat = []
    k = st.text_input("Kérdezz:")
    if st.button("Küldés") and k:
        st.session_state.chat.append({"role": "user", "text": k})
        st.session_state.chat.append({"role": "ai", "text": ai_call([k])})
    for m in st.session_state.chat:
        st.markdown(f"<div class='chat-{m['role']}'>{m['text']}</div>", unsafe_allow_html=True)
