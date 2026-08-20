import io
import os
import random
import json
import streamlit as st
import datetime
from google import genai
from gtts import gTTS
import PyPDF2
import docx
from PIL import Image

st.set_page_config(
    page_title="VizsgaMester - Érettségi Központ",
    page_icon="🎓",
    layout="wide"
)

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# --- STÍLUSOK ÉS MENÜ FELIRAT ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    p, .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: #e5e7eb !important; font-size: 1.05rem; }
    
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px 24px !important;
        border: none; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    
    div[data-testid="stExpander"] { background-color: #111827 !important; border: 1px solid #374151 !important; border-radius: 12px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #111827 !important; color: #ffffff !important; border: 1px solid #374151 !important; border-radius: 10px !important; }
    
    [data-testid="stFileUploader"] { background-color: #111827 !important; padding: 20px; border-radius: 16px; border: 1px solid #374151; }
    [data-testid="stFileUploader"] section { background-color: #1f2937 !important; border: 2px dashed #6366f1 !important; }
    [data-testid="stFileUploader"] section div, 
    [data-testid="stFileUploader"] section span, 
    [data-testid="stFileUploader"] section small, 
    [data-testid="stFileUploader"] section p { color: #ffffff !important; }
    [data-testid="stFileUploader"] label { color: #ffffff !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stFileUploader"] button {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        border: none !important;
    }
    [data-testid="stFileUploader"] button p {
        color: #ffffff !important;
    }

    /* Fix Menü felirat a bal felső nyíl mellé */
    .menu-label {
        position: fixed;
        top: 14px;
        left: 45px;
        font-size: 14px;
        font-weight: 600;
        color: #818cf8;
        z-index: 999999;
        pointer-events: none;
    }

    .topic-card { background-color: #111827; border: 1px solid #374151; border-radius: 18px; padding: 28px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
    .oral-box { background-color: #1e1b4b; border-left: 5px solid #818cf8; padding: 20px; border-radius: 10px; margin-top: 18px; color: #ffffff !important; }
    
    .deep-text { 
        background-color: #111827; 
        color: #ffffff !important; 
        border: 1px solid #374151; 
        padding: 32px; 
        border-radius: 14px; 
        line-height: 1.9; 
        font-size: 1.1rem;
    }
    .deep-text h3 { color: #818cf8 !important; margin-top: 25px; margin-bottom: 12px; }
    
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white; }
    .timeline-item { background-color: #111827; border-left: 5px solid #a855f7; padding: 18px 22px; margin-bottom: 16px; border-radius: 0 14px 14px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 14px 20px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #111827; color: #f3f4f6; border: 1px solid #374151; padding: 14px 20px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
<div class="menu-label">Menü</div>
""", unsafe_allow_html=True)

# --- MAGAS MINŐSÉGŰ TTÉLEG GENERÁTOR ---
def generalo_tetelek(temak_lista, tantargy_tipus):
    tetelek_dict = {}
    for i, tema in enumerate(temak_lista):
        if tantargy_tipus == "matek":
            tartalom = f"""
### I. Elméleti Alapok és Fogalmak
* **Definíció:** A(z) **{tema}** témakörhöz kapcsolódó alapvető matematikai fogalmak, halmazok és axiómák.
* **Jelölésrendszer:** A szabványos matematikai jelölések, képletekben szereplő változók és paraméterek pontos értelmezése.
* **Alaphalmazok:** Értelmezési tartományok és értékkészletek meghatározása.

### II. Főbb Tételek, Szabályok és Képletek
* **Központi összefüggések:** A(z) {tema} legfontosabb tételei, levezetései és logikai összefüggései.
* **Számítási algoritmusok:** Lépésről lépésre követhető módszerek egyenletek, egyenlőtlenségek, függvények vagy geometriai problémák megoldására.
* **Tipikus hibaleforrások:** Gyakori számítási hibák, előjelek helyes kezelése és ellenőrzési módszerek.

### III. Alkalmazások és Feladattípusok
* **Érettségi feladattípusok:** Hogyan jelenik meg a(z) {tema} az írásbeli és szóbeli vizsgákon (I. és II. rész)?
* **Gyakorlati példák:** Szöveges vagy gyakorlati problémák modellezése és megoldása a témakör segítségével.
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Főbb definíciók ({tema}) -> 2. Alaptételek és képletek bemutatása -> 3. Konkrét feladattípus szemléltetése."
        elif tantargy_tipus == "tori":
            tartalom = f"""
### I. Történelmi Kontextus és Előzmények
* **Gazdasági és társadalmi hátrányok/előnyök:** Milyen folyamatok vezettek a(z) **{tema}** kibontakozásához?
* **Okozati összefüggések:** A kortárs nagyhatalmi viszonyok, érdekek és kiváltó okok rendszere.

### II. Fő Események és Hátterük
* **Kronológia:** A legfontosabb dátumok, csaták, egyezmények vagy reformok láncolata.
* **Kulcsszereplők:** A korszak meghatározó politikusai, uralkodói, vezéralakjai és tetteik motivációi.
* **Intézményi keretek:** Hogyan működtek a korabeli állami, vallási vagy gazdasági szervezetek?

### III. Következmények és Hatástörténet
* **Rövid és hosszú távú hatások:** Milyen változásokat hozott a(z) {tema} a mindennapi életben, a határokban vagy a politikai rendszerben?
* **Történeti értékelés:** Hogyan ítéli meg a modern történettudomány ezt a korszakot vagy eseménysorozatot?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Előzmények és okok -> 2. Fő események és szereplők ({tema}) -> 3. Történelmi következmények."
        elif tantargy_tipus == "nyelvtan":
            tartalom = f"""
### I. Rendszerszintű Alapok
* **Fogalommeghatározás:** A(z) **{tema}** helye a magyar nyelv hang-, szó-, mondat- vagy szövegtani rendszerében.
* **Alaptételek:** A nyelvi jelenség törvényszerűségei és nyelvtani kategóriái.

### II. Szabályok, Kivételek és Elemzés
* **Szerkezeti felépítés:** Hogyan épül fel, milyen elemekből áll a(z) {tema} vizsgálatakor figyelembe veendő egység?
* **Helyesírási és nyelvhelyességi normák:** Gyakorlati szabályok, gyakran elkövetett hibák és azok elkerülése.

### III. Kommunikációs Szerep
* **Stilisztikai érték:** Milyen kifejezőereje van a(z) {tema} alkalmazásának a beszédben vagy az írásban?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Elméleti alapok ({tema}) -> 2. Szabályok és kivételek -> 3. Gyakorlati példa."
        else: # irodalom
            tartalom = f"""
### I. Történeti és Művészettörténeti Háttér
* **Korszakmeghatározás:** A(z) **{tema}** születésének irodalomtörténeti korszaka (pl. reneszánsz, romantika, modernség).
* **Kultúrtörténeti kontextus:** Milyen eszmék, filozófiai irányzatok (pl. felvilágosodás, egzisztencializmus) hatottak a mű(vek) keletkezésére?

### II. Részletes Műelemzés
* **Tematika és motívumok:** A műben megjelenő központi kérdések (pl. szerelem, halál, hazafiság, magány).
* **Szerkezet és kompozíció:** Milyen műfaji sajátosságokkal, felépítéssel, narratívával vagy verseléssel operál a(z) {tema}?
* **Stílusjegyek és alakzatok:** Retorikai eszközök, képek, szimbólumok és nyelvi rétegek elemzése.

### III. Üzenet és Hatástörténet
* **Alaptézis:** Milyen egyetemes emberi igazságot fogalmaz meg a(z) {tema}?
* **Utóélet:** Hogyan hatott a későbbi irodalmi generációkra, színházra vagy filmművészetre?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Történeti kontextus -> 2. Főbb művek és elemzés ({tema}) -> 3. Üzenet és hatástörténet."

        tetelek_dict[f"{i+1}. {tema}"] = {
            "alcim": f"Hivatalos érettségi tétel: {tema}",
            "tartalom": tartalom.strip(),
            "szobeli": szobeli,
            "kviz": [
                {"k": f"Alapvető vizsgakérdés a(z) '{tema}' témakör lexikális anyagából?", "v": True, "m": "Igen, a hivatalos érettségi követelményrendszer része."},
                {"k": f"Kapcsolódik ehhez a témához specifikus elemzési szempont?", "v": True, "m": "Természetesen."}
            ]
        }
    return tetelek_dict

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

irodalom_flashcards = [{"q": f"Irodalmi kártya #{i+1}", "a": f"Válasz #{i+1}"} for i in range(20)]
nyelvtan_flashcards = [{"q": f"Nyelvtani kártya #{i+1}", "a": f"Válasz #{i+1}"} for i in range(20)]
tortenelem_flashcards = [{"q": f"Történelmi kártya #{i+1}", "a": f"Válasz #{i+1}"} for i in range(20)]
matek_flashcards = [{"q": f"Matek kártya #{i+1}", "a": f"Képlet #{i+1}"} for i in range(20)]

detektiv_db = {
    "📖 Magyar Irodalom": [{"idezet": f"Idézet #{i+1}", "helyes": "Szerző", "opciok": ["Szerző", "Másik"], "info": "Elemzés."} for i in range(20)],
    "🔤 Magyar Nyelvtan": [{"idezet": f"Feladvány #{i+1}", "helyes": "Válasz", "opciok": ["Válasz", "Rossz"], "info": "Magyarázat."} for i in range(20)],
    "🏛️ Történelem": [{"idezet": f"Forrás #{i+1}", "helyes": "Esemény", "opciok": ["Esemény", "Más"], "info": "Háttér."} for i in range(20)],
    "📐 Matematika": [{"idezet": f"Képlet #{i+1}", "helyes": "Tétel", "opciok": ["Tétel", "Más"], "info": "Magyarázat."} for i in range(20)]
}

db = {
    "📖 Magyar Irodalom": {"tetelek": generalo_tetelek(irodalom_temak, "irodalom"), "flashcards": irodalom_flashcards, "timeline": [{"ev": "1908", "cim": "Nyugat", "leiras": "Indulás."}], "detektiv": detektiv_db["📖 Magyar Irodalom"]},
    "🔤 Magyar Nyelvtan": {"tetelek": generalo_tetelek(nyelvtan_temak, "nyelvtan"), "flashcards": nyelvtan_flashcards, "timeline": [{"ev": "1055", "cim": "Tihany", "leiras": "Nyelvemlék."}], "detektiv": detektiv_db["🔤 Magyar Nyelvtan"]},
    "🏛️ Történelem": {"tetelek": generalo_tetelek(tortenelem_temak, "tori"), "flashcards": tortenelem_flashcards, "timeline": [{"ev": "1000", "cim": "Koronázás", "leiras": "István."}], "detektiv": detektiv_db["🏛️ Történelem"]},
    "📐 Matematika": {"tetelek": generalo_tetelek(matek_temak, "matek"), "flashcards": matek_flashcards, "timeline": [{"ev": "Kr.e. 6. sz.", "cim": "Pitagorasz", "leiras": "Tétel."}], "detektiv": detektiv_db["📐 Matematika"]}
}

if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'tananyag_cache' not in st.session_state: st.session_state.tananyag_cache = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = [{"role": "ai", "text": "Üdvözöllek!"}]

st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox("Válassz tantárgyat:", list(db.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#818cf8;'>Funkciók</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz modult:",
    [
        "📚 Tételek & Vázlatok (20 db)", 
        "📂 Saját Fájlok & Képek",
        "🎧 Hangoskönyv (Tétel-specifikus)", 
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

st.title("🎓 VizsgaMester")
st.caption(f"Aktív tantárgy: **{kivalasztott_tantargy}**")

st.markdown("---")

def ai_generalas_tartalom(contents_list):
    api_k = get_api_key()
    if not api_k: return "⚠️ Hiányzik a GEMINI_API_KEY a Secretsből!"
    try:
        client = genai.Client(api_key=api_k)
        res = client.models.generate_content(model='gemini-3.6-flash', contents=contents_list)
        return res.text if res else "Nincs válasz."
    except Exception as e:
        if "503" in str(e):
            return "⚠️ A szerver jelenleg túlterhelt (503-as hiba). Kérlek, kattints újra néhány másodperc múlva!"
        return f"Hiba: {e}"

def read_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        else:
            text = uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        text = f"Hiba a fájl olvasásakor: {e}"
    return text

def get_tetel_specifikus_szkript(tantargy, tetel_neve):
    alap_szoveg = aktiv_tetelek[tetel_neve]["tartalom"].replace("###", "").replace("- **", "").replace("**", "")
    teljes_anyag = f"{alap_szoveg}\n\n{alap_szoveg}"
    return teljes_anyag

# --- MODULOK ---
if menupont == "📚 Tételek & Vázlatok (20 db)":
    tetel_nev = st.selectbox("Válassz a 20 hivatalos tétel közül:", list(aktiv_tetelek.keys()))
    t_adat = aktiv_tetelek[tetel_nev]
    st.markdown(f"<div class='topic-card'><h2>{tetel_nev}</h2><p style='color:#a5b4fc;'>{t_adat['alcim']}</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes Tananyag", "🎙️ 3 Perces Felelet", "⚡ Interaktív Kvíz"])
    with tab1:
        st.markdown(f"<div class='deep-text'>{t_adat['tartalom']}</div>", unsafe_allow_html=True)
    with tab2: st.markdown(f"<div class='oral-box'>{t_adat['szobeli']}</div>", unsafe_allow_html=True)
    with tab3:
        for i, q in enumerate(t_adat["kviz"]):
            st.write(f"**{i+1}. {q['k']}**")
            c1, c2 = st.columns(2)
            if c1.button("✅ Igaz", key=f"t_{i}"): st.success(f"Helyes! {q['m']}")
            if c2.button("❌ Hamis", key=f"f_{i}"): st.error(f"Nem helyes. {q['m']}")

elif menupont == "📂 Saját Fájlok & Képek":
    st.subheader("📂 Dokumentum és Kép AI Elemzés & Interaktív Kvíz")
    fajl = st.file_uploader("Fájl feltöltése (.docx, .pdf, .txt, .jpg, .png)", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    
    if fajl:
        if fajl.type.startswith("image/"):
            img_obj = Image.open(fajl)
            st.image(img_obj, caption="Feltöltött kép előnézete")
            fajl.seek(0)

        if st.button("🚀 Elemzés és Összefoglalás"):
            with st.spinner("Fájl / Kép olvasása és elemzése folyamatban..."):
                content_payload = []
                if fajl.type.startswith("image/"):
                    img_data = Image.open(fajl)
                    content_payload = [img_data, "Elemezd az alábbi képen látható tananyagot, tételt vagy feladatot, és készíts belőle részletes, érettségire felkészítő összefoglalót:"]
                else:
                    szoveg = ""
                    try:
                        if fajl.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            doc = docx.Document(fajl)
                            szoveg = "\n".join([para.text for para in doc.paragraphs])
                        elif fajl.type == "application/pdf":
                            reader = PyPDF2.PdfReader(fajl)
                            for page in reader.pages:
                                szoveg += page.extract_text() + "\n"
                        else:
                            szoveg = fajl.getvalue().decode("utf-8")
                    except Exception as e:
                        szoveg = f"Hiba a fájl olvasásakor: {e}"
                    
                    st.session_state.aktiv_fajl_szoveg = szoveg
                    content_payload = [f"Elemezd az alábbi feltöltött tananyagot és készíts belőle részletes, érettségire felkészítő összefoglalót: {szoveg[:10000]}"]

                eredmeny = ai_generalas_tartalom(content_payload)
                st.session_state.aktiv_elemzes_eredmeny = eredmeny
                st.session_state.ai_quiz_data = None

        if "aktiv_elemzes_eredmeny" in st.session_state and st.session_state.aktiv_elemzes_eredmeny:
            st.write("### 📌 Elemzés eredménye:")
            st.markdown(f"<div class='deep-text'>{st.session_state.aktiv_elemzes_eredmeny}</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🎯 Interaktív Kérdéssorozat Generálása"):
                with st.spinner("Kérdéssorozat generálása az AI segítségével..."):
                    if fajl.type.startswith("image/"):
                        fajl.seek(0)
                        img_data = Image.open(fajl)
                        q_payload = [img_data, "Készíts 5 db feleletválasztós vizsgakérdést a képen látható tartalom alapján. Add vissza KIZÁRÓLAG érvényes JSON formátumban, semmilyen egyéb szöveget vagy markdown kódblokkot ne adj vissza, csak a tiszta JSON tömböt az alábbi szerkezet szerint:\n[\n  {\n    \"question\": \"A kérdés szövege?\",\n    \"options\": [\"A) opció 1\", \"B) opció 2\", \"C) opció 3\", \"D) opció 4\"],\n    \"answer\": \"A) opció 1\",\n    \"explanation\": \"A helyes válasz magyarázata...\"\n  }\n]"]
                    else:
                        doc_text = st.session_state.get('aktiv_fajl_szoveg', '')[:8000]
                        q_payload = [
                            "Készíts 5 db feleletválasztós vizsgakérdést a következő dokumentum alapján. "
                            "Add vissza KIZÁRÓLAG érvényes JSON formátumban, semmilyen egyéb szöveget vagy "
                            "markdown kódblokkot ne adj vissza, csak a tiszta JSON tömböt az alábbi szerkezet szerint:\n"
                            "[\n  {\n    \"question\": \"A kérdés szövege?\",\n"
                            "    \"options\": [\"A) opció 1\", \"B) opció 2\", \"C) opció 3\", \"D) opció 4\"],\n"
                            "    \"answer\": \"A) opció 1\",\n"
                            "    \"explanation\": \"A helyes válasz magyarázata...\"\n  }\n]\n"
                            f"Dokumentum: {doc_text}"
                        ]

                    raw_res = ai_generalas_tartalom(q_payload)
                    try:
                        cleaned = raw_res.replace("```json", "").replace("```", "").strip()
                        st.session_state.ai_quiz_data = json.loads(cleaned)
                    except Exception as e:
                        st.error(f"Hiba történt a kvíz feldolgozásakor. Kattints újra a gombra. ({e})")
                        st.session_state.ai_quiz_data = None

            # Interaktív teszt kitöltő felület
            if "ai_quiz_data" in st.session_state and st.session_state.ai_quiz_data:
                st.markdown("### 🎯 Interaktív Teszt")
                with st.form("ai_document_quiz_form"):
                    user_answers = {}
                    for idx, q_item in enumerate(st.session_state.ai_quiz_data):
                        st.markdown(f"**{idx+1}. {q_item['question']}**")
                        user_answers[idx] = st.radio("Válassz:", q_item['options'], key=f"doc_q_{idx}", index=None)
                        st.markdown("---")
                    
                    submitted = st.form_submit_button("🏁 Válaszok Értékelése")
                    
                    if submitted:
                        score = 0
                        total = len(st.session_state.ai_quiz_data)
                        for idx, q_item in enumerate(st.session_state.ai_quiz_data):
                            chosen = user_answers.get(idx)
                            correct = q_item['answer']
                            if chosen == correct:
                                score += 1
                                st.success(f"**{idx+1}. kérdés:** Helyes! 🎉\n\n📌 {q_item['explanation']}")
                            elif chosen is None:
                                st.warning(f"**{idx+1}. kérdés:** Nem választottál semmit. ⚠️ A helyes válasz: **{correct}**\n\n📌 {q_item['explanation']}")
                            else:
                                st.error(f"**{idx+1}. kérdés:** Nem találtad el. ❌ A helyes válasz: **{correct}**\n\n📌 {q_item['explanation']}")
                        
                        st.metric("Elért eredmény", f"{score} / {total} pont", f"{int((score/total)*100)}%")

elif menupont == "🎧 Hangoskönyv (Tétel-specifikus)":
    st.subheader("🎧 Tétel-specifikus Hangoskönyv")
    t_nev = st.selectbox("Válassz tételt a hallgatáshoz:", list(aktiv_tetelek.keys()))
    
    felolvashato_szoveg = get_tetel_specifikus_szkript(kivalasztott_tantargy, t_nev)
    
    st.info(f"⚡ A(z) **{t_nev}** tétel saját szakmaianyaga azonnal lejátszható:")
    
    tts = gTTS(text=felolvashato_szoveg, lang='hu', slow=False)
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)
    
    st.audio(f, format="audio/mp3")
    
    st.markdown("---")
    st.markdown("### 📄 A felolvasott szakmai anyag teljes szövege:")
    st.markdown(f"<div class='deep-text'>{felolvashato_szoveg.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

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
    audio = st.audio_input("Felelet rögzítése:")
    if audio and st.button("Értékelés"):
        st.markdown(ai_generalas_tartalom(["Értékeld a feleletet:"]))

elif menupont == "✍️ Esszé & Feladat Labor":
    sz = st.text_area("Írd be a szöveget:")
    if st.button("Javítás") and sz: st.markdown(ai_generalas_tartalom([f"Javítsd ki: {sz}"]))

elif menupont == "🎭 Detektív Játék (20 db)":
    st.subheader(f"🎭 Detektív Feladványok ({len(aktiv_det)} db)")
    st.session_state.detektiv_index = st.session_state.detektiv_index % len(aktiv_det)
    idx = st.session_state.detektiv_index
    f = aktiv_det[idx]
    st.markdown(f"<div class='topic-card' style='text-align:center;'><h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válaszd ki a helyes megfejtést:", f['opciok'], index=None, key=f"det_{idx}")
    if st.button("🔍 Ellenőrzés"):
        if tipp == f['helyes']:
            st.balloons(); st.success(f"Helyes válasz! 🎉\n\n📌 {f['info']}")
        else:
            st.error(f"Nem találtad el. ❌ A helyes válasz: **{f['helyes']}**\n\n📌 {f['info']}")
    if st.button("➡️ Következő feladvány"):
        st.session_state.detektiv_index += 1
        st.rerun()

elif menupont == "🧭 Történelmi Idővonal":
    for item in aktiv_time:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"🏆 Interaktív Próbavizsga – {kivalasztott_tantargy}")
    osszes_kerdes = []
    for t_nev, t_adat in aktiv_tetelek.items():
        for q in t_adat.get("kviz", []): osszes_kerdes.append((t_nev, q))
    
    data_valaszok = {}
    with st.form("vizsga_form"):
        for i, (t_nev, q) in enumerate(osszes_kerdes):
            st.write(f"**{i+1}. [{t_nev}]**")
            st.write(q["k"])
            data_valaszok[i] = st.radio("Válasz:", ["Nem válaszoltam", "Igaz", "Hamis"], key=f"p_{i}", horizontal=True)
            st.markdown("---")
        bekuldve = st.form_submit_button("🏁 Próbavizsga Értékelése")
        
    if bekuldve:
        pont = sum(1 for i, (t_nev, q) in enumerate(osszes_kerdes) if data_valaszok[i] != "Nem válaszoltam" and ((data_valaszok[i] == "Igaz") == q["v"]))
        szaz = int((pont / len(osszes_kerdes)) * 100) if osszes_kerdes else 0
        st.metric("Elért eredmény", f"{pont} / {len(osszes_kerdes)} pont", f"{szaz}%")
        if szaz >= 85: st.success("🏆 Jeles (5) – Kiváló teljesítmény!")
        elif szaz >= 50: st.info("👍 Megfelelő vizsgaeredmény!")
        else: st.error("❌ Fejlesztendő!")

elif menupont == "🤖 AI Érettségi Mentor":
    for msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    k = st.text_input("Kérdezz a mentortól:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas_tartalom([k])})
        st.rerun()
