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
    page_title="Astra Pro Érettségi Központ - 20-as Csomag",
    page_icon="🎓",
    layout="wide"
)

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# --- STÍLUSOK ---
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

# --- PONTOSAN 20-AS GENERÁTOROK TANTÁRGYANKÉNT ---

def generalo_tetelek(tantargy_nev, temak_lista):
    return {f"{i+1}. {tema}": {
        "alcim": f"Hivatalos érettségi tétel: {tema}",
        "vazlat": f"### {tema} részletes vázlata\n- Alapfogalmak, definíciók és történelmi/irodalmi háttér.\n- Főbb összefüggések és elemzési szempontok.",
        "szobeli": f"**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Fő tézisek kifejtése ({tema}) -> 3. Összegzés.",
        "kviz": [
            {"k": f"Alapvető igaz/hamis kérdés a(z) '{tema}' témakörhöz?", "v": True, "m": "Igen, ez a tananyag része."},
            {"k": f"Kapcsolódik ehhez a tételhez lexikális ismeret?", "v": True, "m": "Természetesen."}
        ]
    } for i, tema in enumerate(temak_lista)}

# 20 Irodalom tétel
irodalom_temak = [
    "Ókori eposzok és a Biblia", "Shakespeare drámái", "Balassi Bálint költészete", "Zrínyi Miklós eposza",
    "Mikes Kelemen levelei", "Csokonai Vitéz Mihály", "Katona József: Bánk bán", "Kölcsey és Vörösmarty",
    "Petőfi Sándor költészete", "Arany János balladái", "Jókai Mór regényei", "Madách: Az ember tragédiája",
    "Mikszáth Kálmán prózája", "Ady Endre költészete", "Móricz Zsigmond realizmusa", "Babits Mihály lírája",
    "Kosztolányi Dezső", "József Attila költészete", "Radnóti Miklós versei", "Örkény István egypercesei"
]

# 20 Nyelvtan tétel
nyelvtan_temak = [
    "A kommunikáció folyamata", "Helyesírási alapelvek", "Hangok és törvények", "Szófajok rendszere: alaptagok",
    "Szófajok: viszonyszók", "A szókészlet rétegei", "Mondattan: mondatrészek", "Egyszerű mondatok fajtái",
    "Mellérendelő összetett mondatok", "Alárendelő összetett mondatok", "Szövegtan alapjai", "Stilisztika és alakzatok",
    "Retorika és meggyőzés", "Érvelés technikája", "Vitakultúra szabályai", "Hivatalos dokumentumok",
    "Tömegkommunikáció, sajtó", "Szaknyelvek és rétegnyelvek", "Nyelvtörténet és eredet", "Nyelvjárások és normák"
]

# 20 Történelem tétel
tortenelem_temak = [
    "Az athéni demokrácia", "A római köztársaság", "A kereszténység elterjedése", "A feudalizmus rendszere",
    "A honfoglalás és kalandozások", "Szent István államalapítása", "Az Aranybulla kora", "Az Anjou-kor reformjai",
    "Hunyadi Mátyás birodalma", "A török hódítás kora", "A reformáció Magyarországon", "A Rákóczi-szabadságharc",
    "Felvilágosult abszolutizmus", "A reformkor kibontakozása", "Az 1848–49-es forradalom", "A kiegyezés és a dualizmus",
    "Az I. világháború és Trianon", "A Horthy-korszak", "A II. világháború", "Az 1956-os forradalom és szabadságharc"
]

# 20 Matek tétel
matek_temak = [
    "Halmazok és műveletek", "Matematikai logika", "Számhalmazok és oszthatóság", "Algebrai kifejezések",
    "Hatványok, gyökök, logaritmus", "Elsőfokú egyenletek, egyenlőtlenségek", "Másodfokú egyenletek", "Másodfokú függvények",
    "Egyenletrendszerek", "Függvények tulajdonságai", "Aritmetikai és mértani sorozatok", "Trigonometria alapjai",
    "Háromszögek megoldása", "Vektorok a síkban", "Sígeometria (Kerület, terület)", "Térgeometria (Testek)",
    "Koordináta-geometria", "Kombinatorika", "Valószínűségszámítás", "Statisztika alapjai"
]

db = {
    "📖 Magyar Irodalom": {
        "tetelek": generalo_tetelek("Irodalom", irodalom_temak),
        "flashcards": [{"q": f"Irodalmi villámkártya kérdés #{i+1}", "a": f"Ez a válasz a(z) {i+1}. irodalmi villámkártyára."} for i in range(20)],
        "timeline": [{"ev": f"18{i:02d}", "cim": f"Irodalmi esemény #{i+1}", "leiras": "Jelentős irodalmi mérföldkő."} for i in range(10)],
        "detektiv": [{"idezet": f"„Detektív idézet irodalom irodalom #{i+1}”", "helyes": f"Szerző #{i+1}", "opciok": [f"Szerző #{i+1}", "Másik szerző"], "info": f"Magyarázat a(z) {i+1}. feladványhoz."} for i in range(20)]
    },
    "🔤 Magyar Nyelvtan": {
        "tetelek": generalo_tetelek("Nyelvtan", nyelvtan_temak),
        "flashcards": [{"q": f"Nyelvtani villámkártya kérdés #{i+1}", "a": f"Nyelvtani válasz #{i+1}."} for i in range(20)],
        "timeline": [{"ev": f"10{i:02d}", "cim": f"Nyelvtani emlék #{i+1}", "leiras": "Fontos nyelvtani dokumentum."} for i in range(10)],
        "detektiv": [{"idezet": f"„Nyelvtani jelenség példa #{i+1}”", "helyes": f"Szabály #{i+1}", "opciok": [f"Szabály #{i+1}", "Más szabály"], "info": f"Nyelvtani magyarázat #{i+1}."} for i in range(20)]
    },
    "🏛️ Történelem": {
        "tetelek": generalo_tetelek("Történelem", tortenelem_temak),
        "flashcards": [{"q": f"Történelmi villámkártya kérdés #{i+1}", "a": f"Történelmi válasz #{i+1}."} for i in range(20)],
        "timeline": [{"ev": f"1{i}00", "cim": f"Történelmi esemény #{i+1}", "leiras": "Korszakalkotó történelmi esemény."} for i in range(10)],
        "detektiv": [{"idezet": f"„Történelmi forrásidézet #{i+1}”", "helyes": f"Esemény #{i+1}", "opciok": [f"Esemény #{i+1}", "Más esemény"], "info": f"Történelmi háttér #{i+1}."} for i in range(20)]
    },
    "📐 Matematika": {
        "tetelek": generalo_tetelek("Matek", matek_temak),
        "flashcards": [{"q": f"Matematikai villámkártya kérdés #{i+1}", "a": f"Matematikai válasz/képlet #{i+1}."} for i in range(20)],
        "timeline": [{"ev": f"Kr. e. {i+1}", "cim": f"Matematikai tétel #{i+1}", "leiras": "Geometriai vagy algebrás felfedezés."} for i in range(10)],
        "detektiv": [{"idezet": f"„Matematikai képlet vagy tétel #{i+1}”", "helyes": f"Elnevezés #{i+1}", "opciok": [f"Elnevezés #{i+1}", "Másik tétel"], "info": f"Matematikai magyarázat #{i+1}."} for i in range(20)]
    }
}

# Állapotkezelők
if 'xp' not in st.session_state: st.session_state.xp = 300
if 'streak' not in st.session_state: st.session_state.streak = 7
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Üdvözöllek! Most már pontosan 20 tétel, 20 villámkártya és 20 detektív kérdés áll rendelkezésedre tantárgyanként!"}]

# --- OLDalsáv ---
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox("Válassz tantárgyat:", list(db.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#818cf8;'>Funkciók</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz modult:",
    [
        "📚 Tételek & Vázlatok (20 db)", 
        "📂 Saját Fájlok & Képek",
        "🎧 Hangoskönyv", 
        "🎴 Villámkártyák (20 db)",
        "🎙️ Szóbeli Szimulátor", 
        "✍️ Esszé & Feladat Labor",
        "🎭 Detektív Játék (20 db)", 
        "🧭 Történelmi Idővonal",
        "🏆 Nagy Próbavizsga", 
        "🤖 AI Érettségi Mentor"
    ]
)

tantargy_adat = db[kivalasztott_tantargy]
aktiv_tetelek = tantargy_adat["tetelek"]
aktiv_flash = tantargy_adat["flashcards"]
aktiv_time = tantargy_adat["timeline"]
aktiv_det = tantargy_adat["detektiv"]

# Fejléc
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("🎓 Astra Pro Érettségi Központ")
    st.caption(f"Aktív tantárgy: **{kivalasztott_tantargy}** (20+ elemű adatbázis)")
with col_h2:
    st.markdown(f"<div style='text-align: right;'><span class='stat-badge'>🔥 {st.session_state.streak} nap széria</span><span class='stat-badge'>⚡ {st.session_state.xp} XP</span></div>", unsafe_allow_html=True)

st.markdown("---")

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

# --- MODULOK ---
if menupont == "📚 Tételek & Vázlatok (20 db)":
    tetel_nev = st.selectbox("Válassz a 20 hivatalos tétel közül:", list(aktiv_tetelek.keys()))
    t_adat = aktiv_tetelek[tetel_nev]
    st.markdown(f"<div class='topic-card'><h2>{tetel_nev}</h2><p style='color:#a5b4fc;'>{t_adat['alcim']}</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes Tananyag", "🎙️ 3 Perces Felelet", "⚡ Interaktív Kvíz"])
    with tab1: st.markdown(f"<div class='deep-text'>{t_adat['vazlat']}</div>", unsafe_allow_html=True)
    with tab2: st.markdown(f"<div class='oral-box'>{t_adat['szobeli']}</div>", unsafe_allow_html=True)
    with tab3:
        for i, q in enumerate(t_adat["kviz"]):
            st.write(f"**{i+1}. {q['k']}**")
            c1, c2 = st.columns(2)
            if c1.button("✅ Igaz", key=f"t_{i}"): st.success(f"Helyes! {q['m']}")
            if c2.button("❌ Hamis", key=f"f_{i}"): st.error(f"Nem helyes. {q['m']}")

elif menupont == "📂 Saját Fájlok & Képek":
    st.markdown("<div class='topic-card'><h3>📂 Dokumentum és Kép AI Elemzés</h3></div>", unsafe_allow_html=True)
    fajl = st.file_uploader("Fájl feltöltése", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    if fajl:
        if fajl.type.startswith("image/"):
            st.image(fajl, use_column_width=True)
            if st.button("🚀 Kérdések a képről"):
                st.markdown(ai_generalas("Készíts 5 érettségi kérdést a képről:", fajl.read(), fajl.type))
        else:
            tartalom = fajl.read().decode("utf-8", errors="ignore")
            if st.button("🚀 Elemzés"):
                st.markdown(ai_generalas(f"Készíts vázlatot: {tartalom[:4000]}"))

elif menupont == "🎧 Hangoskönyv":
    t_nev = st.selectbox("Válassz tételt:", list(aktiv_tetelek.keys()))
    if st.button("▶️ Hangoskönyv Indítása"):
        tts = gTTS(text=f"{tetel_nev}. {aktiv_tetelek[tetel_nev]['alcim']}", lang='hu', slow=False)
        f = io.BytesIO(); tts.write_to_fp(f); f.seek(0); st.audio(f, format="audio/mp3")

elif menupont == "🎴 Villámkártyák (20 db)":
    idx = st.session_state.get('f_idx', 0) % len(aktiv_flash)
    k = aktiv_flash[idx]
    st.subheader(f"Villámkártya ({idx+1} / {len(aktiv_flash)})")
    if not st.session_state.card_flipped:
        st.markdown(f"<div class='flashcard'>❓ {k['q']}</div>", unsafe_allow_html=True)
        if st.button("🔄 Megfordítás"): st.session_state.card_flipped = True; st.rerun()
    else:
        st.markdown(f"<div class='flashcard' style='background:linear-gradient(135deg, #064e3b, #065f46);'>💡 {k['a']}</div>", unsafe_allow_html=True)
        if st.button("Következő kártya"):
            st.session_state.card_flipped = False
            st.session_state.f_idx = idx + 1
            st.rerun()

elif menupont == "🎙️ Szóbeli Szimulátor":
    st.subheader("🎙️ Szóbeli Felelet Értékelése")
    audio = st.audio_input("Felelet rögzítése:")
    if audio and st.button("Értékelés"):
        st.markdown(ai_generalas("Értékeld a feleletet:", audio.read(), "audio/wav"))

elif menupont == "✍️ Esszé & Feladat Labor":
    szoveg = st.text_area("Írd be a szöveget:")
    if st.button("Javítás") and szoveg:
        st.markdown(ai_generalas(f"Javítsd ki: {szoveg}"))

elif menupont == "🎭 Detektív Játék (20 db)":
    st.subheader(f"🎭 Detektív Feladványok ({len(aktiv_det)} db)")
    st.session_state.detektiv_index = st.session_state.detektiv_index % len(aktiv_det)
    idx = st.session_state.detektiv_index
    f = aktiv_det[idx]
    
    st.markdown(f"<div class='topic-card' style='text-align:center;'><h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válassz:", f['opciok'], index=None, key=f"det_{idx}")
    
    if st.button("🔍 Ellenőrzés"):
        if tipp == f['helyes']:
            st.balloons()
            st.success(f"Helyes! (+20 XP)\n\n📌 {f['info']}")
        else:
            st.error(f"Nem jó. A helyes: **{f['helyes']}**\n\n📌 {f['info']}")
    if st.button("➡️ Következő"):
        st.session_state.detektiv_index += 1
        st.rerun()

elif menupont == "🧭 Történelmi Idővonal":
    for item in aktiv_time:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"Próbavizsga – {kivalasztott_tantargy}")
    st.write("Indítsd el a tesztet a tételválasztóból.")

elif menupont == "🤖 AI Érettségi Mentor":
    for msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    k = st.text_input("Kérdezz:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas(k)})
        st.rerun()
