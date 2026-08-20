import io
import os
import random
import json
import streamlit as st
from google import genai
from gtts import gTTS
import PyPDF2
import docx
from PIL import Image

# --- KONFIGURÁCIÓ ---
st.set_page_config(page_title="VizsgaMester - Érettségi Központ", page_icon="🎓", layout="wide")

def get_api_key():
    return os.environ.get("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY", ""))

# --- STÍLUSOK ÉS MENÜ FELIRAT ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #f3f4f6; }
    .menu-label { position: fixed; top: 14px; left: 45px; font-size: 14px; font-weight: 600; color: #818cf8; z-index: 999999; pointer-events: none; }
    .topic-card { background-color: #111827; border: 1px solid #374151; border-radius: 18px; padding: 28px; margin-bottom: 24px; }
    .deep-text { background-color: #111827; color: #ffffff !important; border: 1px solid #374151; padding: 32px; border-radius: 14px; line-height: 1.8; }
    .stat-badge { background: linear-gradient(135deg, #6366f1, #a855f7); padding: 8px 18px; border-radius: 24px; font-weight: 700; }
    .chat-ai { background-color: #111827; border: 1px solid #374151; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
<div class="menu-label">Menü</div>
""", unsafe_allow_html=True)

# --- ADATBÁZIS ÉS SEGÉDFÜGGVÉNYEK ---
def ai_generalas(payload):
    api_k = get_api_key()
    if not api_k: return "⚠️ API kulcs hiányzik."
    try:
        client = genai.Client(api_key=api_k)
        res = client.models.generate_content(model='gemini-3.6-flash', contents=payload)
        return res.text
    except Exception as e: return f"Hiba: {e}"

def read_file(f):
    if f.type == "application/pdf":
        return "\n".join([p.extract_text() for p in PyPDF2.PdfReader(f).pages])
    if "wordprocessingml" in f.type:
        return "\n".join([p.text for p in docx.Document(f).paragraphs])
    return f.getvalue().decode("utf-8")

# --- MENÜ ÉS FŐSTRUKTÚRA ---
st.sidebar.title("📚 VizsgaMester")
tantargy = st.sidebar.selectbox("Válassz tantárgyat:", ["Magyar Irodalom", "Történelem", "Matek"])
modul = st.sidebar.radio("Modul választása:", ["Tételek", "Fájl Elemzés", "Kvíz Labor", "AI Mentor", "Hangoskönyv"])

st.title(f"🎓 {tantargy} Központ")

if modul == "Tételek":
    st.subheader("Hivatalos Tételsor")
    tétel = st.selectbox("Válassz tételcímet:", ["1. Tétel", "2. Tétel", "3. Tétel"])
    if st.button("Tétel kifejtése"):
        tartalom = ai_generalas([f"Írj részletes érettségi tételt {tantargy} - {tétel} témában."])
        st.markdown(f"<div class='deep-text'>{tartalom}</div>", unsafe_allow_html=True)

elif modul == "Fájl Elemzés":
    fajl = st.file_uploader("Tölts fel fájlt vagy képet:", type=["jpg", "png", "docx", "pdf", "txt"])
    if fajl and st.button("AI Elemzés"):
        payload = [Image.open(fajl), "Elemezd a képet:"] if fajl.type.startswith("image") else [f"Elemezd: {read_file(fajl)}"]
        res = ai_generalas(payload)
        st.session_state.utolso_elemzes = res
        st.markdown(f"<div class='deep-text'>{res}</div>", unsafe_allow_html=True)

elif modul == "Kvíz Labor":
    if "utolso_elemzes" in st.session_state:
        if st.button("Kvíz generálása az előzőből"):
            prompt = "Készíts 5 feleletválasztós kérdést ebből JSON formátumban: [{'q': '...', 'opt': ['A', 'B', 'C', 'D'], 'a': '...', 'exp': '...'}]"
            res = ai_generalas([prompt + st.session_state.utolso_elemzes])
            try:
                data = json.loads(res.replace("```json", "").replace("```", "").strip())
                for i, q in enumerate(data):
                    st.write(f"**{i+1}. {q['q']}**")
                    if st.radio("Válasz:", q['opt'], key=f"q{i}", index=None) == q['a']:
                        st.success("Helyes!")
                    else: st.warning(f"Helytelen! Helyes: {q['a']}. {q['exp']}")
            except: st.error("Hiba a kvíz betöltésében.")
    else: st.write("Előbb elemezz egy fájlt a 'Fájl Elemzés' modulban.")

elif modul == "AI Mentor":
    if "chat" not in st.session_state: st.session_state.chat = []
    for msg in st.session_state.chat:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    kerdes = st.text_input("Kérdezz a mentortól:")
    if st.button("Küldés") and kerdes:
        valasz = ai_generalas([kerdes])
        st.session_state.chat.extend([{"role": "user", "text": kerdes}, {"role": "ai", "text": valasz}])
        st.rerun()

elif modul == "Hangoskönyv":
    szoveg = st.text_area("Írd be a szöveget, amit meghallgatnál:")
    if st.button("Generálás"):
        tts = gTTS(text=szoveg, lang='hu')
        f = io.BytesIO()
        tts.write_to_fp(f)
        st.audio(f.getvalue(), format="audio/mp3")
