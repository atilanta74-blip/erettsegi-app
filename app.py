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

# Importáljuk az adatbázisokat a data.py-ból
from data import (
    tetelek_irodalom, tetelek_nyelvtan, tetelek_tortenelem, tetelek_matek,
    flashcards_irodalom, flashcards_nyelvtan, flashcards_tortenelem, flashcards_matek,
    timeline_irodalom, timeline_nyelvtan, timeline_tortenelem, timeline_matek,
    detektiv_irodalom, detektiv_nyelvtan, detektiv_tortenelem, detektiv_matek
)

st.set_page_config(
    page_title="Érettségi Felkészítő Központ - Edited by Nagy Attila",
    page_icon="🎓",
    layout="wide"
)

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Stílusok (sötét téma, gombok, feltöltők)
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
    div[data-testid="stExpander"] details summary { background-color: #1e1b4b !important; color: #ffffff !important; font-weight: 700 !important; padding: 12px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #4b5563 !important; border-radius: 8px !important; }
    
    /* Fájlfeltöltő sötét téma */
    [data-testid="stFileUploader"] { background-color: #111827 !important; padding: 15px; border-radius: 12px; border: 1px solid #374151; }
    [data-testid="stFileUploader"] section { background-color: #1f2937 !important; border: 2px dashed #6366f1 !important; }
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] div { color: #f3f4f6 !important; }
    [data-testid="stFileUploader"] button { background-color: #374151 !important; color: #ffffff !important; border: 1px solid #4b5563 !important; }
    [data-testid="stFileUploader"] button:hover { background-color: #4f46e5 !important; color: #ffffff !important; }

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
# SEGÉDFÜGGVÉNYEK
# -------------------------------------------------------------
def tiszta_pdf_szoveg(szoveg):
    cserel = {'ő': 'o', 'Ő': 'O', 'ű': 'u', 'Ű': 'U', 'á': 'a', 'Á': 'A', 'é': 'e', 'É': 'E', 'í': 'i', 'Í': 'I', 'ó': 'o', 'Ó': 'O', 'ö': 'o', 'Ö': 'O', 'ú': 'u', 'Ú': 'U', 'ü': 'u', 'Ü': 'U'}
    for k, v in cserel.items(): szoveg = szoveg.replace(k, v)
    return szoveg.encode('latin-1', 'replace').decode('latin-1')

def letoltheto_pdf_generalas(tetelek_adat, tantargy_nev):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 15)
    pdf.cell(180, 8, f'{tantargy_nev} Erettsegi Tetelvazlatok', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    for cim, adat in tetelek_adat.items():
        pdf.set_font('Helvetica', 'B', 10.5)
        pdf.multi_cell(180, 5.5, tiszta_pdf_szoveg(f"{cim} - {adat['alcim']}"), align='L')
        pdf.ln(3)
    return bytes(pdf.output())

def szoveg_kinyeres(fajl):
    tartalom = ""
    ext = fajl.name.split(".")[-1].lower()
    if ext == "txt":
        tartalom = fajl.read().decode("utf-8", errors="ignore")
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

# Állapotkezelés
if 'xp' not in st.session_state: st.session_state.xp = 180
if 'level' not in st.session_state: st.session_state.level = 2
if 'streak' not in st.session_state: st.session_state.streak = 4
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Szia! Én vagyok a felkészítő mentorod. Kérdezz bátran!"}]

# -------------------------------------------------------------
# OLDALSÁV & TANTÁRGY VÁLASZTÓ
# -------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox(
    "Válassz tantárgyat:",
    ["📖 Magyar Irodalom", "🔤 Magyar Nyelvtan", "🏛️ Történelem", "📐 Matematika"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#818cf8;'>Funkciók</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz menüpontot:",
    [
        "📚 Tételek & Vázlatok", 
        "📂 Saját Tételek Feltöltése",
        "🎧 Hangoskönyv (Monológ)", 
        "🎴 Villámkártyák (Flashcards)",
        "🎙️ Szóbeli Szimulátor (Beszéd / Írás)", 
        "✍️ Esszé & Feladatmegoldó Labor",
        "🎭 Tantárgyi Detektív Játék", 
        "🧭 Tantárgyi Idővonal & Térkép",
        "🏆 Nagy Próbavizsga", 
        "🤖 AI Érettségi Mentor"
    ]
)

# Adatbázisok kiosztása a kiválasztott tantárgy alapján
if "Irodalom" in kivalasztott_tantargy:
    aktiv_adatbazis, aktiv_flashcards, aktiv_timeline, aktiv_detektiv, tantargy_cimke = tetelek_irodalom, flashcards_irodalom, timeline_irodalom, detektiv_irodalom, "Magyar Irodalom"
elif "Nyelvtan" in kivalasztott_tantargy:
    aktiv_adatbazis, aktiv_flashcards, aktiv_timeline, aktiv_detektiv, tantargy_cimke = tetelek_nyelvtan, flashcards_nyelvtan, timeline_nyelvtan, detektiv_nyelvtan, "Magyar Nyelvtan"
elif "Történelem" in kivalasztott_tantargy:
    aktiv_adatbazis, aktiv_flashcards, aktiv_timeline, aktiv_detektiv, tantargy_cimke = tetelek_tortenelem, flashcards_tortenelem, timeline_tortenelem, detektiv_tortenelem, "Történelem"
else:
    aktiv_adatbazis, aktiv_flashcards, aktiv_timeline, aktiv_detektiv, tantargy_cimke = tetelek_matek, flashcards_matek, timeline_matek, detektiv_matek, "Matematika"

st.sidebar.markdown("---")
if st.sidebar.button(f"📄 {tantargy_cimke} PDF Letöltése"):
    pdf_bytes = letoltheto_pdf_generalas(aktiv_adatbazis, tantargy_cimke)
    st.sidebar.download_button("⬇️ Letöltés", data=pdf_bytes, file_name=f"{tantargy_cimke}_Puska.pdf", mime="application/pdf")

# Főoldali fejlécek
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("✨ Edited by Nagy Attila")
    st.caption(f"Astra AI Érettségi Felkészítő Központ – Aktív: {tantargy_cimke}")
with col_h2:
    st.markdown(f"<div style='text-align: right;'><span class='stat-badge'>🔥 {st.session_state.streak} napos széria</span><span class='stat-badge'>⚡ {st.session_state.xp} XP</span></div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------------
# MENÜPONTOK LOGIKÁJA
# -------------------------------------------------------------
if menupont == "📚 Tételek & Vázlatok":
    tetel = st.selectbox("Válassz tételt:", list(aktiv_adatbazis.keys()))
    adat = aktiv_adatbazis[tetel]
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
    st.subheader("📂 Saját Tételek és Fotók Feltöltése (TXT, PDF, DOCX, Kép)")
    st.write("Tölts fel egy saját tételt vagy jegyzetet, és az AI azonnal generál belőle gyakorló kérdéseket!")
    
    feltoltott_fajl = st.file_uploader("Válassz fájlt:", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    
    if feltoltott_fajl is not None:
        try:
            if feltoltott_fajl.type.startswith("image/"):
                st.image(feltoltott_fajl, caption="Feltöltött tétel fotó", use_column_width=True)
                file_bytes = feltoltott_fajl.read()
                if st.button("🚀 Kérdések generálása a fotóból"):
                    with st.spinner("Az AI elemzi a képet..."):
                        valasz = ai_generalas("Olvasd el a képen látható tananyagot, majd készíts belőle 5 darab igaz/hamis gyakorló kérdést válaszmagyarázattal.", file_bytes=file_bytes, mime_type=feltoltott_fajl.type)
                        st.markdown(f"<div class='deep-text' style='margin-top: 15px;'>{valasz}</div>", unsafe_allow_html=True)
            else:
                tartalom = szoveg_kinyeres(feltoltott_fajl)
                st.success(f"Sikeres feldolgozás: **{feltoltott_fajl.name}**")
                if st.button("🚀 Kérdések generálása a fájlból"):
                    with st.spinner("Az AI elemzi a tételt..."):
                        valasz = ai_generalas(f"Készíts 5 darab igaz/hamis kérdést és válaszmagyarázatot az alábbi tananyagból: {tartalom[:5000]}")
                        st.markdown(f"<div class='deep-text' style='margin-top: 15px;'>{valasz}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Hiba történt a fájl feldolgozása közben: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

elif menupont == "🎧 Hangoskönyv (Monológ)":
    tetel = st.selectbox("Válassz tételt hangoskönyvhöz:", list(aktiv_adatbazis.keys()))
    if st.button("▶️ Hangos indítás"):
        tts = gTTS(text=f"{tetel}. {aktiv_adatbazis[tetel]['alcim']}", lang='hu', slow=False)
        f = io.BytesIO(); tts.write_to_fp(f); f.seek(0); st.audio(f, format="audio/mp3")

elif menupont == "🎴 Villámkártyák (Flashcards)":
    if len(aktiv_flashcards) > 0:
        idx = st.session_state.get('flashcard_index', 0) % len(aktiv_flashcards)
        k = aktiv_flashcards[idx]
        st.subheader(f"Villámkártya ({tantargy_cimke}) - {idx+1}/{len(aktiv_flashcards)}")
        if not st.session_state.card_flipped:
            st.markdown(f"<div class='flashcard'>❓ {k['q']}</div>", unsafe_allow_html=True)
            if st.button("🔄 Megfordítás"): st.session_state.card_flipped = True; st.rerun()
        else:
            st.markdown(f"<div class='flashcard' style='background:linear-gradient(135deg, #064e3b, #065f46);'>💡 {k['a']}</div>", unsafe_allow_html=True)
            if st.button("Következő kártya"):
                st.session_state.card_flipped = False
                st.session_state.flashcard_index = idx + 1
                st.rerun()
    else:
        st.info("Nincsenek kártyák ehhez a tantárgyhoz.")

elif menupont == "🎙️ Szóbeli Szimulátor (Beszéd / Írás)":
    st.subheader("Szóbeli vizsga szimuláció")
    tetel = st.selectbox("Vizsgatétel:", list(aktiv_adatbazis.keys()))
    audio = st.audio_input("Mondd el a feleleted:")
    if audio and st.button("Vizsga értékelése"):
        st.write(ai_generalas(f"Értékeld ezt a szóbeli választ a(z) {tetel} tételben:", file_bytes=audio.read(), mime_type="audio/wav"))

elif menupont == "✍️ Esszé & Feladatmegoldó Labor":
    munka = st.text_area("Másold be az esszét vagy matek feladatot:")
    if st.button("Elemzés és javítás") and munka:
        st.markdown(f"<div class='deep-text'>{ai_generalas(f'Elemezd és javítsd ki: {munka}')}</div>", unsafe_allow_html=True)

elif menupont == "🎭 Tantárgyi Detektív Játék":
    st.title(f"🎭 {tantargy_cimke} Detektív Játék")
    st.caption(f"Felismered a legfontosabb {tantargy_cimke} idézeteket, forrásokat és képleteket?")
    
    st.session_state.detektiv_index = st.session_state.detektiv_index % len(aktiv_detektiv)
    idx = st.session_state.detektiv_index
    f = aktiv_detektiv[idx]
    
    st.progress((idx + 1) / len(aktiv_detektiv))
    st.write(f"Feladvány: **{idx + 1} / {len(aktiv_detektiv)}**")
    
    random.seed(idx + 99)
    kevert_opciok = f['opciok'].copy()
    random.shuffle(kevert_opciok)
    
    st.markdown(f"""
    <div class='topic-card' style='border-color:#ec4899; text-align:center;'>
        <h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    valasztott_tipp = st.radio("Válaszd ki a helyes megfejtést:", kevert_opciok, index=None, key=f"detektiv_radio_{idx}")
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        if st.button("🔍 Tipp ellenőrzése", use_container_width=True):
            if valasztott_tipp is None:
                st.warning("Kérlek, válassz egy választ először!")
            elif valasztott_tipp == f['helyes']:
                st.balloons()
                st.session_state.xp += 30
                st.success(f"TÖKÉLETES! 🎉 Helyes válasz! (+30 XP)\n\n📌 Magyarázat: {f['info']}")
            else:
                st.error(f"Sajnos nem! ❌ A helyes válasz: **{f['helyes']}**\n\n📌 Magyarázat: {f['info']}")
                
    with col_d2:
        if st.button("➡️ Következő feladvány", use_container_width=True):
            st.session_state.detektiv_index += 1
            st.rerun()

elif menupont == "🧭 Tantárgyi Idővonal & Térkép":
    st.subheader(f"{tantargy_cimke} Idővonal")
    for item in aktiv_timeline:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"Próbavizsga ({tantargy_cimke})")
    osszes_kerdes = []
    for t_nev, t_adat in aktiv_adatbazis.items():
        for q in t_adat["kviz"]: osszes_kerdes.append((t_nev, q))
    
    valaszok = {}
    with st.form("nagy_vizsga_form"):
        for idx, (t_nev, q) in enumerate(osszes_kerdes):
            st.markdown(f"**{idx+1}. [{t_nev}]**")
            st.write(q["k"])
            valaszok[idx] = st.radio("Választásod:", ["Nem válaszoltam", "Igaz", "Hamis"], key=f"pv_{idx}", horizontal=True)
            st.markdown("---")
        bekuldve = st.form_submit_button("🏁 Eredmények kiértékelése")
        
    if bekuldve:
        pont = sum(1 for idx, (t_nev, q) in enumerate(osszes_kerdes) if valaszok[idx] != "Nem válaszoltam" and ((valaszok[idx] == "Igaz") == q["v"]))
        szazalek = int((pont / len(osszes_kerdes)) * 100) if len(osszes_kerdes) > 0 else 0
        st.metric("Elért vizsgaeredmény", f"{pont} / {len(osszes_kerdes)} pont", f"{szazalek}%")
        if szazalek >= 85: st.success("🏆 Jeles (5) – Kiváló felkészültség!")
        elif szazalek >= 50: st.info("👍 Megfelelő eredmény!")
        else: st.error("❌ Fejlesztendő!")

elif menupont == "🤖 AI Érettségi Mentor":
    st.subheader("AI Érettségi Mentor")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user": st.markdown(f"<div class='chat-user'>🧑‍🎓 {msg['text']}</div>", unsafe_allow_html=True)
        else: st.markdown(f"<div class='chat-ai'>🤖 {msg['text']}</div>", unsafe_allow_html=True)
    
    audio_k = st.audio_input("Kérdezz hangban:")
    if audio_k and st.button("Hangüzenet küldése"):
        v = ai_generalas("Vlaszolj a diák hangüzenetére érettségi tanárként", file_bytes=audio_k.read(), mime_type="audio/wav")
        st.session_state.chat_history.append({"role": "user", "text": "🎙️ *(Hangüzenet)*"})
        st.session_state.chat_history.append({"role": "ai", "text": v})
        st.rerun()

    k = st.text_input("Írj a mentornak:")
    if st.button("Írásbeli küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        v = ai_generalas(f"Vlaszolj érettségi tanárként: {k}")
        st.session_state.chat_history.append({"role": "ai", "text": v})
        st.rerun()
