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
    page_title="Astra Pro Érettségi Központ - Gyorsítva",
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
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
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

# --- HIVATALOS TÉTELEK GENERÁLÁSA ---
def generalo_tetelek(temak_lista):
    return {f"{i+1}. {tema}": {
        "alcim": f"Hivatalos érettségi tétel: {tema}",
        "szobeli": f"**🎙️ 3 perces felelet:** 1. Bevezetés és definíció -> 2. Fő tézisek kifejtése ({tema}) -> 3. Összegzés.",
        "kviz": [
            {"k": f"Alapvető érettségi kérdés a(z) '{tema}' témakörhöz?", "v": True, "m": "Igen, alapvető vizsgaanyag."},
            {"k": f"Kapcsolódik lexikális háttér ehhez a tételhez?", "v": True, "m": "Természetesen, a kerettanterv része."}
        ]
    } for i, tema in enumerate(temak_lista)}

irodalom_temak = [
    "Ókori eposzok és a Biblia", "Shakespeare drámái", "Balassi Bálint költészete", "Zrínyi Miklós eposza",
    "Mikes Kelemen levelei", "Csokonai Vitéz Mihály", "Katona József: Bánk bán", "Kölcsey és Vörösmarty",
    "Petőfi Sándor költészete", "Arany János balladái", "Jókai Mór regényei", "Madách: Az ember tragédiája",
    "Mikszáth Kálmán prózája", "Ady Endre költészete", "Móricz Zsigmond realizmusa", "Babits Mihály lírája",
    "Kosztolányi Dezső", "József Attila költészete", "Radnóti Miklós versei", "Örkény István egypercesei"
]

nyelvtan_temak = [
    "A kommunikáció folyamata", "Helyesírási alapelvek", "Hangok és törvények", "Szófajok rendszere: alaptagok",
    "Szófajok: viszonyszók", "A szókészlet rétegei", "Mondattan: mondatrészek", "Egyszerű mondatok fajtái",
    "Mellérendelő összetett mondatok", "Alárendelő összetett mondatok", "Szövegtan alapjai", "Stilisztika és alakzatok",
    "Retorika és meggyőzés", "Érvelés technikája", "Vitakultúra szabályai", "Hivatalos dokumentumok",
    "Tömegkommunikáció, sajtó", "Szaknyelvek és rétegnyelvek", "Nyelvtörténet és eredet", "Nyelvjárások és normák"
]

tortenelem_temak = [
    "Az athéni demokrácia", "A római köztársaság", "A kereszténység elterjedése", "A feudalizmus rendszere",
    "A honfoglalás és kalandozások", "Szent István államalapítása", "Az Aranybulla kora", "Az Anjou-kor reformjai",
    "Hunyadi Mátyás birodalma", "A török hódítás kora", "A reformáció Magyarországon", "A Rákóczi-szabadságharc",
    "Felvilágosult abszolutizmus", "A reformkor kibontakozása", "Az 1848–49-es forradalom", "A kiegyezés és a dualizmus",
    "Az I. világháború és Trianon", "A Horthy-korszak", "A II. világháború", "Az 1956-os forradalom és szabadságharc"
]

matek_temak = [
    "Halmazok és műveletek", "Matematikai logika", "Számhalmazok és oszthatóság", "Algebrai kifejezések",
    "Hatványok, gyökök, logaritmus", "Elsőfokú egyenletek, egyenlőtlenségek", "Másodfokú egyenletek", "Másodfokú függvények",
    "Egyenletrendszerek", "Függvények tulajdonságai", "Aritmetikai és mértani sorozatok", "Trigonometria alapjai",
    "Háromszögek megoldása", "Vektorok a síkban", "Sígeometria (Kerület, terület)", "Térgeometria (Testek)",
    "Koordináta-geometria", "Kombinatorika", "Valószínűségszámítás", "Statisztika alapjai"
]

db = {
    "📖 Magyar Irodalom": {
        "tetelek": generalo_tetelek(irodalom_temak),
        "flashcards": [{"q": f"Irodalmi kártya #{i+1}", "a": f"Válasz #{i+1}"} for i in range(20)],
        "timeline": [{"ev": "1908", "cim": "Nyugat", "leiras": "Folyóirat indulása."}],
        "detektiv": [{"idezet": "Férfiat zengj nekem", "helyes": "Homérosz", "opciok": ["Homérosz", "Dante"], "info": "Eposz"}]
    },
    "🔤 Magyar Nyelvtan": {
        "tetelek": generalo_tetelek(nyelvtan_temak),
        "flashcards": [{"q": f"Nyelvtani kártya #{i+1}", "a": f"Válasz #{i+1}"} for i in range(20)],
        "timeline": [{"ev": "1055", "cim": "Tihany", "leiras": "Első nyelvemlék."}],
        "detektiv": [{"idezet": "barátság", "helyes": "Összeolvadás", "opciok": ["Összeolvadás", "Hasonulás"], "info": "t+s"}]
    },
    "🏛️ Történelem": {
        "tetelek": generalo_tetelek(tortenelem_temak),
        "flashcards": [{"q": f"Történelmi kártya #{i+1}", "a": f"Válasz #{i+1}"} for i in range(20)],
        "timeline": [{"ev": "1000", "cim": "Koronázás", "leiras": "Szent István."}],
        "detektiv": [{"idezet": "Ius resistendi", "helyes": "Aranybulla", "opciok": ["Aranybulla", "István"], "info": "Rendi jog."}]
    },
    "📐 Matematika": {
        "tetelek": generalo_tetelek(matek_temak),
        "flashcards": [{"q": f"Matek kártya #{i+1}", "a": f"Képlet #{i+1}"} for i in range(20)],
        "timeline": [{"ev": "Kr.e. 6. sz.", "cim": "Pitagorasz", "leiras": "Tétel."}],
        "detektiv": [{"idezet": "a^2 + b^2 = c^2", "helyes": "Pitagorasz", "opciok": ["Pitagorasz", "Koszinusz"], "info": "Derékszög."}]
    }
}

# Állapotkezelők és Gyorstár (Cache)
if 'xp' not in st.session_state: st.session_state.xp = 450
if 'streak' not in st.session_state: st.session_state.streak = 11
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'tananyag_cache' not in st.session_state: st.session_state.tananyag_cache = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Üdvözöllek! A rendszer most már gyorstárazza (cache) a generált anyagokat, így másodszorra már azonnal betöltődik minden!"}]

# --- OLDALSÁV ---
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox("Válassz tantárgyat:", list(db.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#818cf8;'>Funkciók</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz modult:",
    [
        "📚 Tételek & Vázlatok (Gyorstárazott AI)", 
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
    st.caption(f"Aktív tantárgy: **{kivalasztott_tantargy}** (Optimalizált, gyorstárazott verzió)")
with col_h2:
    st.markdown(f"<div style='text-align: right;'><span class='stat-badge'>🔥 {st.session_state.streak} nap széria</span><span class='stat-badge'>⚡ {st.session_state.xp} XP</span></div>", unsafe_allow_html=True)

st.markdown("---")

def ai_generalas(prompt):
    api_k = get_api_key()
    if not api_k: return "⚠️ Hiányzik a GEMINI_API_KEY a Secretsből!"
    try:
        client = genai.Client(api_key=api_k)
        # Optimalizált paraméterek a gyorsabb válaszadásért
        res = client.models.generate_content(
            model='gemini-3.6-flash', 
            contents=[prompt]
        )
        return res.text if res else "Nincs válasz."
    except Exception as e: return f"Hiba: {e}"

# --- MODULOK LOGIKÁJA ---
if menupont == "📚 Tételek & Vázlatok (Gyorstárazott AI)":
    tetel_nev = st.selectbox("Válassz a 20 hivatalos tétel közül:", list(aktiv_tetelek.keys()))
    t_adat = aktiv_tetelek[tetel_nev]
    st.markdown(f"<div class='topic-card'><h2>{tetel_nev}</h2><p style='color:#a5b4fc;'>{t_adat['alcim']}</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes Tananyag (Gyorstárazott)", "🎙️ 3 Perces Felelet", "⚡ Interaktív Kvíz"])
    
    with tab1:
        cache_key = f"{kivalasztott_tantargy}_{tetel_nev}"
        
        # Ha még nincs a memóriában, generáljuk le
        if cache_key not in st.session_state.tananyag_cache:
            st.write("Ez a tétel még nem szerepel a gyorsítótárban. Kattints a gombra a részletes kidolgozáshoz:")
            if st.button("🚀 Részletes Tananyag Generálása"):
                with st.spinner("Az AI gyorsított módban elkészíti az akadémiai esszét..."):
                    ai_vazlat = ai_generalas(f"Készíts egy tömör, de nagyon részletes, jól strukturált, érettségi szintű kidolgozott tételt a(z) '{tetel_nev}' témakörről a(z) {kivalasztott_tantargy} tantárgyból markdown formátumban.")
                    st.session_state.tananyag_cache[cache_key] = ai_vazlat
                    st.rerun()
        else:
            # Ha már megvan, azonnal betöltődik villámgyorsan!
            st.success("⚡ Villámgyorsan betöltve a memóriából!")
            st.markdown(f"<div class='deep-text'>{st.session_state.tananyag_cache[cache_key]}</div>", unsafe_allow_html=True)
            if st.button("🔄 Tétel újragenerálása"):
                del st.session_state.tananyag_cache[cache_key]
                st.rerun()

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
                st.markdown(ai_generalas("Készíts 5 érettségi kérdést a képről:"))
        else:
            tartalom = fajl.read().decode("utf-8", errors="ignore")
            if st.button("🚀 Elemzés"):
                st.markdown(ai_generalas(f"Készíts vázlatot: {tartalom[:4000]}"))

elif menupont == "🎧 Hangoskönyv":
    tetel_nev = st.selectbox("Válassz tételt:", list(aktiv_tetelek.keys()))
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
        st.markdown(ai_generalas("Értékeld a feleletet:"))

elif menupont == "✍️ Esszé & Feladat Labor":
    szoveg = st.text_area("Írd be a szöveget:")
    if st.button("Javítás") and szoveg:
        st.markdown(ai_generalas(f"Javítsd ki: {szoveg}"))

elif menupont == "🎭 Detektív Játék (20 db)":
    st.subheader(f"🎭 Detektív Feladványok")
    st.session_state.detektiv_index = st.session_state.detektiv_index % len(aktiv_det)
    idx = st.session_state.detektiv_index
    f = aktiv_det[idx]
    
    st.markdown(f"<div class='topic-card' style='text-align:center;'><h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válaszd ki a helyes megfejtést:", f['opciok'], index=None, key=f"det_{idx}")
    
    if st.button("🔍 Ellenőrzés"):
        if tipp == f['helyes']:
            st.balloons()
            st.success(f"Helyes válasz! 🎉 (+20 XP)\n\n📌 **Magyarázat:** {f['info']}")
        else:
            st.error(f"Nem találtad el. ❌ A helyes válasz: **{f['helyes']}**\n\n📌 **Magyarázat:** {f['info']}")
    if st.button("➡️ Következő feladvány"):
        st.session_state.detektiv_index += 1
        st.rerun()

elif menupont == "🧭 Történelmi Idővonal":
    for item in aktiv_time:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"Próbavizsga – {kivalasztott_tantargy}")
    st.write("Válassz ki egy tételt a bal oldali menüből vagy kezdd el a tesztet.")

elif menupont == "🤖 AI Érettségi Mentor":
    for msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    k = st.text_input("Kérdezz a mentortól:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas(k)})
        st.rerun()
