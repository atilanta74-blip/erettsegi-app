import io
import os
import random
import streamlit as st
import datetime
from fpdf import FPDF
from google import genai
from gtts import gTTS

# Beállítás: Hány naponta frissüljenek a kérdések? (1 = naponta)
FRISSITESI_GYAKORISAG_NAPOKBAN = 1

def get_daily_index(lista_hossza):
    nap_sorszam = datetime.date.today().toordinal() // FRISSITESI_GYAKORISAG_NAPOKBAN
    return nap_sorszam % lista_hossza

st.set_page_config(
    page_title="Érettségi Felkészítő Központ - Edited by Nagy Attila",
    page_icon="🎓",
    layout="wide"
)

# Háttérben tárolt Secrets kulcs automatikus betöltése
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Astra AI stílusú prémium sötét téma és javított kontrasztok
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: 1px solid #818cf8 !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background: linear-gradient(135deg, #6366f1, #9333ea) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stExpander"] { background-color: #1f2937 !important; border: 1px solid #4b5563 !important; border-radius: 10px !important; }
    div[data-testid="stExpander"] details summary { background-color: #1e1b4b !important; color: #ffffff !important; font-weight: 700 !important; padding: 12px !important; }
    div[data-testid="stExpander"] details div[data-testid="stExpanderDetails"] { background-color: #111827 !important; color: #f3f4f6 !important; padding: 16px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #4b5563 !important; }
    .stat-badge { background: linear-gradient(135deg, #6366f1, #a855f7); padding: 8px 16px; border-radius: 20px; font-weight: 700; display: inline-block; margin-right: 8px; }
    .subject-pill { background: #1e1b4b; border: 1px solid #6366f1; padding: 6px 14px; border-radius: 12px; font-weight: 600; display: inline-block; margin-bottom: 12px; }
    .topic-card { background-color: #1f2937; border: 1px solid #374151; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .oral-box { background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 18px; border-radius: 8px; margin-top: 15px; }
    .deep-text { background-color: #111827; border: 1px solid #374151; padding: 24px; border-radius: 12px; }
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 16px; padding: 35px; text-align: center; min-height: 180px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
    .audio-card { background-color: #182234; border: 1px solid #3b82f6; border-radius: 12px; padding: 20px; }
    .timeline-item { background-color: #1f2937; border-left: 4px solid #a855f7; padding: 16px 20px; margin-bottom: 15px; border-radius: 0 12px 12px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 12px 18px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #1f2937; color: #f3f4f6; border: 1px solid #374151; padding: 12px 18px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# Adatbázisok definiálása (kivonatolva a kód átláthatósága miatt)
# [Itt a korábbiakban definiált 'tetelek_irodalom', 'tetelek_nyelvtan', 'tetelek_tortenelem', 'tetelek_matek' 
# és a többi változó (flashcards, timeline, detektiv) ugyanúgy maradjon a kódban, mint a legutóbbi sikeres verzióban.]

# --- Mivel a kód hossza korlátozott, itt csak a lényegi logika-frissítést mutatom be, 
# --- A többi adatbázis részt (tetelek_irodalom, flashcards_irodalom stb.) másold be ugyanúgy, ahogy az előző válaszomban volt!

# ... (Kérlek másold ide a tetel-adatbázisokat a legutóbbi kódból) ...

# -------------------------------------------------------------
# 2. MENÜPONT: VILLÁMKÁRTYÁK (FLASHCARDS) - NAPI FRISSÍTÉSSEL
# -------------------------------------------------------------
elif menupont == "🎴 Villámkártyák (Flashcards)":
    st.title(f"🎴 {tantargy_cimke} Villámkártyák")
    
    # NAPI FRISSÍTÉS LOGIKA:
    # Nem a 'card_idx'-et használjuk, hanem a dátum alapú indexet!
    daily_idx = get_daily_index(len(aktiv_flashcards))
    aktualis_kartya = aktiv_flashcards[daily_idx]
    
    st.write(f"Mai kártya ({datetime.date.today()}):")
    
    if not st.session_state.card_flipped:
        st.markdown(f"<div class='flashcard'>❓ {aktualis_kartya['q']}</div>", unsafe_allow_html=True)
        if st.button("🔄 Kártya megfordítása", use_container_width=True):
            st.session_state.card_flipped = True
            st.rerun()
    else:
        st.markdown(f"<div class='flashcard' style='background:linear-gradient(135deg, #064e3b, #065f46); border-color:#34d399;'>💡 {aktualis_kartya['a']}</div>", unsafe_allow_html=True)
        if st.button("Következő napra / Ismétlés"):
            st.session_state.card_flipped = False
            st.rerun()

# -------------------------------------------------------------
# 6. MENÜPONT: TANTÁRGYI DETEKTÍV JÁTÉK - NAPI FRISSÍTÉSSEL
# -------------------------------------------------------------
elif menupont == "🎭 Tantárgyi Detektív Játék":
    st.title(f"🎭 {tantargy_cimke} Detektív Játék")
    
    # NAPI FRISSÍTÉS LOGIKA:
    daily_idx = get_daily_index(len(aktiv_detektiv))
    feladvany = aktiv_detektiv[daily_idx]
    
    st.markdown(f"<div class='topic-card'><h3>{feladvany['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válaszd ki a helyes megfejtést:", feladvany['opciok'])
    
    if st.button("🔍 Ellenőrzés"):
        if tipp == feladvany['helyes']:
            st.success("Helyes! 🎉")
        else:
            st.error(f"Sajnos nem. Helyes: {feladvany['helyes']}")

# ... [A többi kód változatlanul marad] ...
