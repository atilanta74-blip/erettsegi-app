import io
import os
import json
import random
import streamlit as st
import datetime
from fpdf import FPDF
from google import genai
from gtts import gTTS
import PyPDF2
import docx

st.set_page_config(
    page_title="Astra Érettségi Felkészítő Központ",
    page_icon="🎓",
    layout="wide"
)

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# --- PROFESSZIONÁLIS SÖTÉT DIZÁJN ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #0f172a !important; border-right: 1px solid #1e293b; }
    p, .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: #f3f4f6 !important; }
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px 24px !important;
        border: none; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    div[data-testid="stExpander"] { background-color: #111827 !important; border: 1px solid #374151 !important; border-radius: 12px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #111827 !important; color: #ffffff !important; border: 1px solid #374151 !important; border-radius: 10px !important; }
    
    [data-testid="stFileUploader"] { background-color: #111827 !important; padding: 20px; border-radius: 16px; border: 1px solid #374151; }
    [data-testid="stFileUploader"] section { background-color: #1f2937 !important; border: 2px dashed #6366f1 !important; }

    .stat-badge { background: linear-gradient(135deg, #6366f1, #a855f7); padding: 8px 18px; border-radius: 24px; font-weight: 700; display: inline-block; box-shadow: 0 2px 10px rgba(99,102,241,0.3); }
    .topic-card { background-color: #111827; border: 1px solid #374151; border-radius: 18px; padding: 28px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
    .oral-box { background-color: #1e1b4b; border-left: 5px solid #818cf8; padding: 20px; border-radius: 10px; margin-top: 18px; }
    .deep-text { background-color: #0f172a; border: 1px solid #374151; padding: 28px; border-radius: 14px; line-height: 1.9; }
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4); }
    .timeline-item { background-color: #111827; border-left: 5px solid #a855f7; padding: 18px 22px; margin-bottom: 16px; border-radius: 0 14px 14px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 14px 20px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #111827; color: #f3f4f6; border: 1px solid #374151; padding: 14px 20px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# --- KÜLSŐ ADATBÁZIS (TANANYAG.JSON) BETÖLTÉSE ---
@st.cache_data
def load_tananyag():
    if os.path.exists("tananyag.json"):
        with open("tananyag.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "Magyar Irodalom": {
            "tetelek": {
                "1. Ókori eposzok és a Biblia": {
                    "alcim": "Homérosz és az európai kultúra alapkövei",
                    "vazlat": "### I. Eposzi kellékek\n- Invokáció, propozíció, in medias res, csodás elemek.\n### II. Iliász és Odüsszeia\n- Trójai háború, emberi sorsok és istenek.",
                    "szobeli": "**🎙️ 3 perces felelet:** 1. Műfaj jellemzői -> 2. Hősök ábrázolása.",
                    "kviz": [{"k": "Az eposz nagy terjedelmű verses epikai mű.", "v": True, "m": "Igen, a klasszikus ókori műfajok egyike."}]
                }
            },
            "flashcards": [{"q": "Mit jelent az in medias res?", "a": "A dolgok sűrűjébe vágó évszázados eposzi kezdés."}],
            "timeline": [{"ev": "Kr. e. VIII. sz.", "cim": "Homéroszi eposzok", "leiras": "Az Iliász és az Odüsszeia megszületése."}],
            "detektiv": [{"idezet": "„Férfiat zengj nekem, múzsa, ki sokfelé bolyongott...”", "helyes": "Homérosz: Odüsszeia", "opciok": ["Homérosz: Odüsszeia", "Virgilius", "Dante"], "info": "Az Odüsszeia híres kezdősorai."}]
        }
    }

db = load_tananyag()

# Állapotkezelők
if 'xp' not in st.session_state: st.session_state.xp = 250
if 'streak' not in st.session_state: st.session_state.streak = 5
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Üdvözöllek! Én vagyok az AI érettségi mentorod. Válassz tantárgyat és kezdjük el a felkészülést!"}]

# --- OLDALSÁV MENÜ ---
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
elerheto_tantargyak = list(db.keys())
kivalasztott_tantargy = st.sidebar.selectbox("Válassz tantárgyat:", elerheto_tantargyak)

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#818cf8;'>Funkciók</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz modult:",
    [
        "📚 Tételek & Vázlatok", 
        "📂 Saját Fájlok & Képek Elemzése",
        "🎧 Hangoskönyv", 
        "🎴 Villámkártyák",
        "🎙️ Szóbeli Szimulátor", 
        "✍️ Esszé & Feladat Labor",
        "🎭 Tantárgyi Detektív", 
        "🧭 Történelmi Idővonal",
        "🏆 Nagy Próbavizsga", 
        "🤖 AI Érettségi Mentor"
    ]
)

tantargy_adat = db.get(kivalasztott_tantargy, {})
aktiv_tetelek = tantargy_adat.get("tetelek", {})
aktiv_flash = tantargy_adat.get("flashcards", [])
aktiv_time = tantargy_adat.get("timeline", [])
aktiv_det = tantargy_adat.get("detektiv", [])

# Fejléc
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("🎓 Astra Pro Érettségi Központ")
    st.caption(f"Aktív tantárgy: **{kivalasztott_tantargy}**")
with col_h2:
    st.markdown(f"<div style='text-align: right;'><span class='stat-badge'>🔥 {st.session_state.streak} nap széria</span><span class='stat-badge'>⚡ {st.session_state.xp} XP</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- MODULOK LOGIKÁJA ---
def ai_generalas(prompt, file_bytes=None, mime_type=None):
    api_k = get_api_key()
    if not api_k: return "⚠️ Hiányzik a GEMINI_API_KEY a Secretsből!"
    try:
        client = genai.Client(api_key=api_k)
        c = [prompt]
        if file_bytes and mime_type: c.append({"inline_data": {"mime_type": mime_type, "data": file_bytes}})
        res = client.models.generate_content(model='gemini-2.0-flash', contents=c)
        return res.text if res else "Nincs válasz."
    except Exception as e: return f"Hiba: {e}"

if menupont == "📚 Tételek & Vázlatok":
    if aktiv_tetelek:
        tetel_nev = st.selectbox("Válassz tételt a hivatalos listából:", list(aktiv_tetelek.keys()))
        t_adat = aktiv_tetelek[tetel_nev]
        st.markdown(f"<div class='topic-card'><h2>{tetel_nev}</h2><p style='color:#a5b4fc;'>{t_adat.get('alcim','')}</p></div>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📚 Részletes Tananyag", "🎙️ 3 Perces Felelet", "⚡ Interaktív Kvíz"])
        with tab1: st.markdown(f"<div class='deep-text'>{t_adat.get('vazlat','')}</div>", unsafe_allow_html=True)
        with tab2: st.markdown(f"<div class='oral-box'>{t_adat.get('szobeli','')}</div>", unsafe_allow_html=True)
        with tab3:
            for i, q in enumerate(t_adat.get("kviz", [])):
                st.write(f"**{i+1}. {q['k']}**")
                c1, c2 = st.columns(2)
                if c1.button("✅ Igaz", key=f"t_{i}"): st.success(f"Helyes! {q['m']}")
                if c2.button("❌ Hamis", key=f"f_{i}"): st.error(f"Nem helyes. {q['m']}")
    else:
        st.info("Ehhez a tantárgyhoz még nincsenek feltöltve tételek a tananyag.json fájlba.")

elif menupont == "📂 Saját Fájlok & Képek Elemzése":
    st.markdown("<div class='topic-card'><h3>📂 Dokumentum és Kép AI Elemzés</h3><p>Tölts fel PDF-et, Word dokumentumot vagy jegyzetfotót, és az AI azonnal feldolgozza.</p></div>", unsafe_allow_html=True)
    fajl = st.file_uploader("Fájl feltöltése", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    if fajl:
        if fajl.type.startswith("image/"):
            st.image(fajl, use_column_width=True)
            if st.button("🚀 Kérdések generálása a fotóból"):
                with st.spinner("Elemzés..."):
                    valasz = ai_generalas("Készíts 5 nehéz érettségi szintű kérdést ebből a vizuális anyagból:", fajl.read(), fajl.type)
                    st.markdown(f"<div class='deep-text'>{valasz}</div>", unsafe_allow_html=True)
        else:
            tartalom = ""
            if fajl.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(fajl)
                for p in reader.pages: tartalom += p.extract_text()
            elif fajl.name.endswith(".docx"):
                doc = docx.Document(fajl)
                for p in doc.paragraphs: tartalom += p.text + "\n"
            else:
                tartalom = fajl.read().decode("utf-8", errors="ignore")
            
            if st.button("🚀 Elemzés és Kvíz Generálás"):
                with st.spinner("AI feldolgozás..."):
                    valasz = ai_generalas(f"Készíts részletes vázlatot és tesztkérdéseket ebből a tananyagból: {tartalom[:6000]}")
                    st.markdown(f"<div class='deep-text'>{valasz}</div>", unsafe_allow_html=True)

elif menupont == "🎧 Hangoskönyv":
    if aktiv_tetelek:
        t_nev = st.selectbox("Válassz tételt a hallgatáshoz:", list(aktiv_tetelek.keys()))
        if st.button("▶️ Hangoskönyv Indítása"):
            szoveg = f"{t_nev}. {aktiv_tetelek[t_nev]['alcim']}. {aktiv_tetelek[t_nev]['vazlat']}"
            tts = gTTS(text=szoveg[:1000], lang='hu', slow=False)
            f = io.BytesIO(); tts.write_to_fp(f); f.seek(0); st.audio(f, format="audio/mp3")

elif menupont == "🎴 Villámkártyák":
    if aktiv_flash:
        idx = st.session_state.get('f_idx', 0) % len(aktiv_flash)
        k = aktiv_flash[idx]
        st.subheader(f"Villámkártya ({idx+1}/{len(aktiv_flash)})")
        if not st.session_state.card_flipped:
            st.markdown(f"<div class='flashcard'>❓ {k['q']}</div>", unsafe_allow_html=True)
            if st.button("🔄 Megfordítás"): st.session_state.card_flipped = True; st.rerun()
        else:
            st.markdown(f"<div class='flashcard' style='background:linear-gradient(135deg, #064e3b, #065f46);'>💡 {k['a']}</div>", unsafe_allow_html=True)
            if st.button("Következő kártya"):
                st.session_state.card_flipped = False
                st.session_state.f_idx = idx + 1
                st.rerun()
    else:
        st.info("Nincsenek villámkártyák ehhez a tantárgyhoz.")

elif menupont == "🎙️ Szóbeli Szimulátor":
    st.subheader("🎙️ Szóbeli Felelet Hangalapú Értékelése")
    st.write("Mondd fel a telefonod vagy mikrofonod segítségével a feleleted, az AI pedig jegyet és részletes értékelést ad rá.")
    audio = st.audio_input("Felelet rögzítése:")
    if audio and st.button("Felelet Értékelése"):
        with st.spinner("AI értékel tanárként..."):
            valasz = ai_generalas("Értékeld ezt a szóbeli érettségi feleletet, adj rá osztályzatot és fejlesztendő tippeket:", audio.read(), "audio/wav")
            st.markdown(f"<div class='deep-text'>{valasz}</div>", unsafe_allow_html=True)

elif menupont == "✍️ Esszé & Feladat Labor":
    st.subheader("✍️ Esszé és Feladatmegoldás Javító")
    szoveg = st.text_area("Másold be ide a saját esszédet vagy matek feladatmegoldásodat:")
    if st.button("Alapos AI Elemzés és Pontozás") and szoveg:
        with st.spinner("Értékelés..."):
            valasz = ai_generalas(f"Elemezd és javítsd ki ezt a diák által írt dolgozatot/esszét a hivatalos érettségi szempontok szerint: {szoveg}")
            st.markdown(f"<div class='deep-text'>{valasz}</div>", unsafe_allow_html=True)

elif menupont == "🎭 Tantárgyi Detektív":
    if aktiv_det:
        st.subheader("🎭 Ismerd fel a művet, forrást vagy képletet!")
        st.session_state.detektiv_index = st.session_state.detektiv_index % len(aktiv_det)
        idx = st.session_state.detektiv_index
        f = aktiv_det[idx]
        
        st.markdown(f"<div class='topic-card' style='text-align:center;'><h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3></div>", unsafe_allow_html=True)
        tipp = st.radio("Válaszd ki a helyes megfejtést:", f['opciok'], index=None, key=f"det_{idx}")
        
        if st.button("🔍 Ellenőrzés"):
            if tipp == f['helyes']:
                st.balloons()
                st.session_state.xp += 20
                st.success(f"Helyes válasz! 🎉 (+20 XP)\n\n📌 **Magyarázat:** {f['info']}")
            else:
                st.error(f"Nem találtad el. ❌ A helyes válasz: **{f['helyes']}**\n\n📌 **Magyarázat:** {f['info']}")
        if st.button("➡️ Következő feladvány"):
            st.session_state.detektiv_index += 1
            st.rerun()
    else:
        st.info("Nincsenek detektív feladványok ehhez a tantárgyhoz.")

elif menupont == "🧭 Történelmi Idővonal":
    if aktiv_time:
        st.subheader("🧭 Fontos Dátumok és Események")
        for item in aktiv_time:
            st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)
    else:
        st.info("Nincs idővonal adat ehhez a tantárgyhoz.")

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"🏆 Interaktív Próbavizsga – {kivalasztott_tantargy}")
    if aktiv_tetelek:
        osszes_kerdes = []
        for t_nev, t_adat in aktiv_tetelek.items():
            for q in t_adat.get("kviz", []): osszes_kerdes.append((t_nev, q))
        
        valaszok = {}
        with st.form("vizsga_form"):
            for i, (t_nev, q) in enumerate(osszes_kerdes):
                st.write(f"**{i+1}. [{t_nev}]**")
                st.write(q["k"])
                valaszok[i] = st.radio("Válasz:", ["Nem válaszoltam", "Igaz", "Hamis"], key=f"p_{i}", horizontal=True)
                st.markdown("---")
            bekuldve = st.form_submit_button("🏁 Próbavizsga Értékelése")
            
        if bekuldve:
            pont = sum(1 for i, (t_nev, q) in enumerate(osszes_kerdes) if valaszok[i] != "Nem válaszoltam" and ((valaszok[i] == "Igaz") == q["v"]))
            szaz = int((pont / len(osszes_kerdes)) * 100) if osszes_kerdes else 0
            st.metric("Elért eredmény", f"{pont} / {len(osszes_kerdes)} pont", f"{szaz}%")
            if szaz >= 85: st.success("🏆 Jeles (5) – Kiváló teljesítmény!")
            elif szaz >= 50: st.info("👍 Megfelelő vizsgaeredmény!")
            else: st.error("❌ Fejlesztendő!")
    else:
        st.warning("Nincsenek vizsgakérdések.")

elif menupont == "🤖 AI Érettségi Mentor":
    st.subheader("🤖 Személyes AI Érettségi Tanár")
    for msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    
    kerdes = st.text_input("Kérdezz bármit a tananyagtól:");
    if st.button("Küldés") and kerdes:
        st.session_state.chat_history.append({"role": "user", "text": kerdes})
        valasz = ai_generalas(f"Te egy segítőkész érettségi tanár vagy. Válaszolj a diák kérdésére: {kerdes}")
        st.session_state.chat_history.append({"role": "ai", "text": valasz})
        st.rerun()
