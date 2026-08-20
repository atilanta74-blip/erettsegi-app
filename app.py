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
# VALÓDI, EGYEDI TÉTELEK LISTÁJA
# -------------------------------------------------------------
def keszit_tetelek(temak):
    return {tema: {
        "alcim": f"Részletes vizsgakövetelmény: {tema}",
        "vazlat": f"### {tema}\n- Alapfogalmak és definíciók.\n- Történelmi vagy irodalmi kontextus és összefüggések.",
        "szobeli": f"**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Fő tézisek kifejtése ({tema}) -> 3. Összegzés.",
        "kviz": [{"k": f"Kapcsolódik-e ez az állítás a(z) '{tema}' témakörhöz?", "v": True, "m": "Igen, alapvető vizsgaanyag."}]
    } for tema in temak}

tetelek_irodalom = keszit_tetelek([
    "1. Ókori eposzok és a Biblia", "2. Shakespeare drámái", "3. Balassi Bálint költészete", 
    "4. Zrínyi Miklós eposza", "5. Mikes Kelemen levelei", "6. Csokonai Vitéz Mihály", 
    "7. Katona József: Bánk bán", "8. Kölcsey és Vörösmarty", "9. Petőfi Sándor költészete", 
    "10. Arany János balladái", "11. Jókai Mór regényei", "12. Madách: Az ember tragédiája", 
    "13. Mikszáth Kálmán prózája", "14. Ady Endre költészete", "15. Móricz Zsigmond realizmusa", 
    "16. Babits Mihály lírája", "17. Kosztolányi Dezső", "18. József Attila költészete", 
    "19. Radnóti Miklós versei", "20. Örkény István egypercesei", "21. Pilinszky és Nagy László", "22. Kortárs irodalom"
])

tetelek_nyelvtan = keszit_tetelek([
    "1. Kommunikáció folyamata", "2. Helyesírási alapelvek", "3. Szófajok rendszere", 
    "4. Mondattan alapjai", "5. Összetett mondatok", "6. Jelentéstan", "7. Stilisztika", 
    "8. Nyelv és társadalom", "9. Nyelvtörténet", "10. Szövegtan", "11. Retorika", 
    "12. Érvelés technikája", "13. Vitakultúra", "14. Hivatalos dokumentumok", "15. Sajtónyelv", "16. Szaknyelvek"
])

tetelek_tortenelem = keszit_tetelek([
    "1. Athéni demokrácia", "2. Kereszténység és az egyház", "3. A magyarság honfoglalása", 
    "4. Szent István államalapítása", "5. Az Aranybulla kora", "6. Az Anjou-kor reformjai", 
    "7. Hunyadi Mátyás birodalma", "8. A török hódítás kora", "9. Reformáció Magyarországon", 
    "10. Rákóczi-szabadságharc", "11. Felvilágosult abszolutizmus", "12. A reformkor kibontakozása", 
    "13. Az 1848-as forradalom és szabadságharc", "14. A kiegyezés és a dualizmus", 
    "15. Az I. világháború és Trianon", "16. Horthy-korszak", "17. A II. világháború", 
    "18. Rákosi-korszak", "19. Az 1956-os forradalom", "20. Kádár-korszak", 
    "21. Rendszerváltás Magyarországon", "22. Európai Unió", "23. Hidegháború", 
    "24. Ipari forradalmak", "25. Nacionalizmus és liberalizmus", "26. Totalitárius rendszerek", 
    "27. Globális problémák", "28. Gyarmatrendszer felbomlása", "29. Az ENSZ és a nemzetközi szervezetek", "30. A két világháború közötti gazdaság"
])

tetelek_matek = keszit_tetelek([
    "1. Halmazok, logika", "2. Másodfokú egyenletek", "3. Függvények tulajdonságai", 
    "4. Trigonometria", "5. Planimetria (Sígeometria)", "6. Sztereometria (Térgeometria)", 
    "7. Koordináta-geometria", "8. Kombinatorika", "9. Valószínűségszámítás", 
    "10. Sorozatok (Aritmetikai, mértani)", "11. Hatványok, gyökök, logaritmus", 
    "12. Polinomok, egyenletrendszerek", "13. Differenciálszámítás alapjai", 
    "14. Integrálszámítás", "15. Statisztika", "16. Pénzügyi matematika"
])

flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost szerint?", "a": "„Tragédia dalban elbeszélve” – líra, epika és dráma szintézise."},
    {"q": "Melyik évben indult a Nyugat folyóirat?", "a": "1908-ban, Osvát Ernő szerkesztette."},
    {"q": "Ki írta Az ember tragédiáját?", "a": "Madách Imre."}
]
flashcards_nyelvtan = [
    {"q": "Mik a magyar helyesírás fő alapelvei?", "a": "Kiejtés, szóelemzés, hagyomány, egyszerűsítés."},
    {"q": "Mi a morféma?", "a": "A nyelv legkisebb önálló jelentéssel bíró alapegysége."}
]
flashcards_tortenelem = [
    {"q": "Mikor kezdődött a honfoglalás?", "a": "895-ben."},
    {"q": "Mikor adta ki II. András az Aranybullát?", "a": "1222-ben."}
]
flashcards_matek = [
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Mennyi a derékszögű háromszög területe?", "a": "A befogók szorzatának fele: (a · b) / 2"}
]

timeline_irodalom = [{"ev": "1848", "cim": "Forradalom lírája", "leiras": "Petőfi és Arany munkássága."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihanyi alapítólevél", "leiras": "Az első magyar nyelvemlék."}]
timeline_tortenelem = [{"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István koronázása."}]
timeline_matek = [{"ev": "Kr. e. VI. sz.", "cim": "Pitagorasz", "leiras": "Geometriai alapvetés."}]

detektiv_irodalom = [{"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre", "Arany János"], "info": "A felelősségvállalás parancsa."}]
detektiv_nyelvtan = [{"idezet": "„barátság [kiejtve: baraccság]”", "helyes": "Összeolvadás mássalhangzótörvény", "opciok": ["Összeolvadás mássalhangzótörvény", "Zöngésségi részleges hasonulás"], "info": "t + s -> [ccs]."}]
detektiv_tortenelem = [{"idezet": "„Ius resistendi”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Szent István"], "info": "Rendi jog."}]
detektiv_matek = [{"idezet": "a² = b² + c² - 2bc · cos(α)", "helyes": "Koszinusztétel", "opciok": ["Koszinusztétel", "Pitagorasz"], "info": "Általános háromszög."}]

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
    st.write("Válassz tesztet vagy induljon a próba.")

elif menupont == "🤖 AI Mentor":
    k = st.text_input("Kérdés a mentornak:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas(k)})
        st.rerun()
    for m in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{m['role']}'>{m['text']}</div>", unsafe_allow_html=True)
