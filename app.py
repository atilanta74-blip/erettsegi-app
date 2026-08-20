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

st.set_page_config(
    page_title="Érettségi Felkészítő Központ - Edited by Nagy Attila",
    page_icon="🎓",
    layout="wide"
)

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Stílusok
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    p, .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: #f3f4f6 !important; }
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important; font-weight: 700 !important; border-radius: 10px !important; padding: 10px 24px !important;
    }
    div[data-testid="stExpander"] { background-color: #1f2937 !important; border: 1px solid #4b5563 !important; border-radius: 10px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #4b5563 !important; border-radius: 8px !important; }
    
    [data-testid="stFileUploader"] { background-color: #111827 !important; padding: 15px; border-radius: 12px; border: 1px solid #374151; }
    [data-testid="stFileUploader"] section { background-color: #1f2937 !important; border: 2px dashed #6366f1 !important; }
    
    .stat-badge { background: linear-gradient(135deg, #6366f1, #a855f7); padding: 8px 16px; border-radius: 20px; font-weight: 700; display: inline-block; margin-right: 8px; }
    .topic-card { background-color: #1f2937; border: 1px solid #374151; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .oral-box { background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 18px; border-radius: 8px; margin-top: 15px; }
    .deep-text { background-color: #111827; border: 1px solid #374151; padding: 24px; border-radius: 12px; line-height: 1.8; }
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 16px; padding: 35px; text-align: center; min-height: 180px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
    .timeline-item { background-color: #1f2937; border-left: 4px solid #a855f7; padding: 16px 20px; margin-bottom: 15px; border-radius: 0 12px 12px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 12px 18px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #1f2937; color: #f3f4f6; border: 1px solid #374151; padding: 12px 18px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# ADATBÁZIS GENERÁTOR (Minden tétel automatikusan betöltődik)
# -------------------------------------------------------------
def gener_tetelek(tantargy, db):
    return {f"{i}. {tantargy} Tétel": {
        "alcim": f"Hivatalos érettségi követelmény a(z) {i}. témakörhöz",
        "vazlat": f"### I. Részletes vázlat\n- A {tantargy} vizsgaanyag alapvető fogalmai és összefüggései a(z) {i}. tételnél.",
        "szobeli": f"**🎙️ 3 perces felelet:** 1. Bevezetés és definíció -> 2. Részletes kifejtés a(z) {i}. tételben.",
        "kviz": [{"k": f"Ehhez a tétethez kapcsolódó alapvető állítás?", "v": True, "m": "Helyes válasz és magyarázat."}]
    } for i in range(1, db + 1)}

tetelek_irodalom = gener_tetelek("Irodalom", 22)
tetelek_nyelvtan = gener_tetelek("Nyelvtan", 16)
tetelek_tortenelem = gener_tetelek("Történelem", 30)
tetelek_matek = gener_tetelek("Matek", 16)

flashcards_irodalom = [{"q": f"Irodalmi kérdés {i}", "a": f"Irodalmi válasz {i}"} for i in range(1, 10)]
flashcards_nyelvtan = [{"q": f"Nyelvtani kérdés {i}", "a": f"Nyelvtani válasz {i}"} for i in range(1, 10)]
flashcards_tortenelem = [{"q": f"Történelmi esemény {i}", "a": f"Történelmi válasz {i}"} for i in range(1, 10)]
flashcards_matek = [{"q": f"Matematikai feladat {i}", "a": f"Matematikai válasz {i}"} for i in range(1, 10)]

timeline_irodalom = [{"ev": "1848", "cim": "Forradalom", "leiras": "Irodalmi és történelmi események."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihany", "leiras": "Első nyelvemlék."}]
timeline_tortenelem = [{"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István koronázása."}]
timeline_matek = [{"ev": "Kr. e. VI. sz.", "cim": "Pitagorasz", "leiras": "Geometriai tétel."}]

detektiv_irodalom = [{"idezet": "„Példa idézet irodalom”", "helyes": "Szerző", "opciok": ["Szerző", "Másik"], "info": "Magyarázat"}]
detektiv_nyelvtan = [{"idezet": "„Példa nyelvtani jelenség”", "helyes": "Szabály", "opciok": ["Szabály", "Másik"], "info": "Magyarázat"}]
detektiv_tortenelem = [{"idezet": "„Példa történelmi forrás”", "helyes": "Esemény", "opciok": ["Esemény", "Másik"], "info": "Magyarázat"}]
detektiv_matek = [{"idezet": "„Példa képlet”", "helyes": "Tétel", "opciok": ["Tétel", "Másik"], "info": "Magyarázat"}]

# -------------------------------------------------------------
# SEGÉDFÜGGVÉNYEK
# -------------------------------------------------------------
def szoveg_kinyeres(fajl):
    tartalom = ""
    ext = fajl.name.split(".")[-1].lower()
    if ext == "txt": tartalom = fajl.read().decode("utf-8", errors="ignore")
    elif ext == "pdf":
        reader = PyPDF2.PdfReader(fajl)
        for page in reader.pages: tartalom += page.extract_text() + "\n"
    elif ext == "docx":
        doc = docx.Document(fajl)
        for para in doc.paragraphs: tartalom += para.text + "\n"
    return tartalom

def ai_generalas(prompt_text, file_bytes=None, mime_type=None):
    api_k = get_api_key()
    if not api_k: return "⚠️ Nincs beállítva a GEMINI_API_KEY kulcs!"
    try:
        client = genai.Client(api_key=api_k)
        contents_input = [prompt_text]
        if file_bytes and mime_type:
            contents_input.append({"inline_data": {"mime_type": mime_type, "data": file_bytes}})
        res = client.models.generate_content(model='gemini-2.0-flash', contents=contents_input)
        return res.text if res and res.text else "Nincs válasz."
    except Exception as e: return f"Hiba: {e}"

if 'xp' not in st.session_state: st.session_state.xp = 180
if 'streak' not in st.session_state: st.session_state.streak = 4
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Szia! Én vagyok a felkészítő mentorod. Kérdezz bátran!"}]

# -------------------------------------------------------------
# OLDALSÁV & TANTÁRGY VÁLASZTÓ
# -------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox("Válassz tantárgyat:", ["📖 Magyar Irodalom", "🔤 Magyar Nyelvtan", "🏛️ Történelem", "📐 Matematika"])

st.sidebar.markdown("---")
menupont = st.sidebar.radio("Válassz menüpontot:", [
    "📚 Tételek & Vázlatok", "📂 Saját Tételek Feltöltése", "🎧 Hangoskönyv (Monológ)", 
    "🎴 Villámkártyák (Flashcards)", "🎙️ Szóbeli Szimulátor", "✍️ Esszé Labor", 
    "🎭 Detektív Játék", "🧭 Idővonal", "🏆 Próbavizsga", "🤖 AI Mentor"
])

if "Irodalom" in kivalasztott_tantargy:
    aktiv_db, aktiv_flash, aktiv_time, aktiv_det, tantargy_cimke = tetelek_irodalom, flashcards_irodalom, timeline_irodalom, detektiv_irodalom, "Magyar Irodalom"
elif "Nyelvtan" in kivalasztott_tantargy:
    aktiv_db, aktiv_flash, aktiv_time, aktiv_det, tantargy_cimke = tetelek_nyelvtan, flashcards_nyelvtan, timeline_nyelvtan, detektiv_nyelvtan, "Magyar Nyelvtan"
elif "Történelem" in kivalasztott_tantargy:
    aktiv_db, aktiv_flash, aktiv_time, aktiv_det, tantargy_cimke = tetelek_tortenelem, flashcards_tortenelem, timeline_tortenelem, detektiv_tortenelem, "Történelem"
else:
    aktiv_db, aktiv_flash, aktiv_time, aktiv_det, tantargy_cimke = tetelek_matek, flashcards_matek, timeline_matek, detektiv_matek, "Matematika"

col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("✨ Edited by Nagy Attila")
    st.caption(f"Astra AI Érettségi Központ – Aktív: {tantargy_cimke}")
with col_h2:
    st.markdown(f"<div style='text-align: right;'><span class='stat-badge'>🔥 {st.session_state.streak} nap</span><span class='stat-badge'>⚡ {st.session_state.xp} XP</span></div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------------
# MENÜPONTOK
# -------------------------------------------------------------
if menupont == "📚 Tételek & Vázlatok":
    tetel = st.selectbox("Válassz tételt:", list(aktiv_db.keys()))
    adat = aktiv_db[tetel]
    st.markdown(f"<div class='topic-card'><h2>{tetel}</h2><p>{adat['alcim']}</p></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📚 Tananyag", "🎙️ Feleletvázlat", "⚡ Kvíz"])
    with tab1: st.markdown(f"<div class='deep-text'>{adat['vazlat']}</div>", unsafe_allow_html=True)
    with tab2: st.markdown(f"<div class='oral-box'>{adat['szobeli']}</div>", unsafe_allow_html=True)
    with tab3:
        for i, q in enumerate(adat["kviz"]):
            st.write(f"**{i+1}. {q['k']}**")
            c1, c2 = st.columns(2)
            if c1.button("✅ Igaz", key=f"t_{i}"): st.success(f"Helyes! {q['m']}")
            if c2.button("❌ Hamis", key=f"f_{i}"): st.error(f"Nem jó. {q['m']}")

elif menupont == "📂 Saját Tételek Feltöltése":
    st.markdown("<div class='topic-card'>", unsafe_allow_html=True)
    st.subheader("📂 Saját Fájlok Feltöltése (TXT, PDF, DOCX, Kép)")
    fajl = st.file_uploader("Válassz fájlt:", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    if fajl:
        if fajl.type.startswith("image/"):
            st.image(fajl, use_column_width=True)
            if st.button("🚀 Kérdések a képről"):
                st.markdown(ai_generalas("Készíts 5 kérdést a képről:", fajl.read(), fajl.type))
        else:
            tartalom = szoveg_kinyeres(fajl)
            if st.button("🚀 Kérdések a fájlból"):
                st.markdown(ai_generalas(f"Készíts 5 kérdést: {tartalom[:5000]}"))
    st.markdown("</div>", unsafe_allow_html=True)

elif menupont == "🎧 Hangoskönyv (Monológ)":
    tetel = st.selectbox("Válassz tételt:", list(aktiv_db.keys()))
    if st.button("▶️ Hangos indítás"):
        tts = gTTS(text=f"{tetel}. {aktiv_db[tetel]['alcim']}", lang='hu', slow=False)
        f = io.BytesIO(); tts.write_to_fp(f); f.seek(0); st.audio(f, format="audio/mp3")

elif menupont == "🎴 Villámkártyák (Flashcards)":
    idx = st.session_state.get('flash_idx', 0) % len(aktiv_flash)
    k = aktiv_flash[idx]
    st.markdown(f"<div class='flashcard'>❓ {k['q']}</div>", unsafe_allow_html=True)
    if st.button("Következő kártya"):
        st.session_state.flash_idx = idx + 1
        st.rerun()

elif menupont == "🎙️ Szóbeli Szimulátor":
    st.subheader("Szóbeli vizsga szimuláció")
    audio = st.audio_input("Mondd el a feleleted:")
    if audio and st.button("Értékelés"):
        st.write(ai_generalas("Értékeld a feleletet:", audio.read(), "audio/wav"))

elif menupont == "✍️ Esszé Labor":
     mun = st.text_area("Írd be az esszét:")
     if st.button("Javítás") and mun:
         st.markdown(ai_generalas(f"Javítsd ki: {mun}"))

elif menupont == "🎭 Detektív Játék":
    f = aktiv_det[st.session_state.detektiv_index % len(aktiv_det)]
    st.markdown(f"<div class='topic-card'><h3>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    v = st.radio("Válaszd ki a helyeset:", f['opciok'], index=None)
    if st.button("Ellenőrzés") and v == f['helyes']: st.success(f"Helyes! {f['info']}")

elif menupont == "🧭 Idővonal":
    for item in aktiv_time:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Próbavizsga":
    st.subheader(f"Próbavizsga ({tantargy_cimke})")
    st.write("Kattints a vizsga indításához a bal oldali menüben vagy válassz tesztet.")

elif menupont == "🤖 AI Mentor":
    k = st.text_input("Kérdés a mentornak:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas(k)})
        st.rerun()
    for m in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{m['role']}'>{m['text']}</div>", unsafe_allow_html=True)
