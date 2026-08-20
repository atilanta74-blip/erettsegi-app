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
    p, .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: #e5e7eb !important; font-size: 1.1rem; line-height: 1.8; }
    
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important; font-weight: 700 !important; border-radius: 12px !important; padding: 12px 24px !important;
        border: none; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    
    div[data-testid="stExpander"] { background-color: #111827 !important; border: 1px solid #374151 !important; border-radius: 14px !important; margin-bottom: 12px; }
    div[data-testid="stExpander"] summary p { color: #818cf8 !important; font-weight: 700 !important; font-size: 1.15rem !important; }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #111827 !important; color: #ffffff !important; border: 1px solid #374151 !important; border-radius: 10px !important; }
    
    [data-testid="stFileUploader"] { background-color: #111827 !important; padding: 20px; border-radius: 16px; border: 1px solid #374151; }
    [data-testid="stFileUploader"] section { background-color: #1f2937 !important; border: 2px dashed #6366f1 !important; }
    [data-testid="stFileUploader"] section div, 
    [data-testid="stFileUploader"] section span, 
    [data-testid="stFileUploader"] section small, 
    [data-testid="stFileUploader"] section p { color: #ffffff !important; }
    [data-testid="stFileUploader"] label { color: #ffffff !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stFileUploader"] button { background-color: #4f46e5 !important; color: #ffffff !important; border: none !important; }
    [data-testid="stFileUploader"] button p { color: #ffffff !important; }

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
    
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white; }
    .timeline-item { background-color: #111827; border-left: 5px solid #a855f7; padding: 18px 22px; margin-bottom: 16px; border-radius: 0 14px 14px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 14px 20px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #111827; color: #f3f4f6; border: 1px solid #374151; padding: 14px 20px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
<div class="menu-label">Menü</div>
""", unsafe_allow_html=True)

# --- RÉSZLETES, KIBONTHATÓ TANANYAG ADATBÁZIS GENERÁTOR ---
def generalo_tetelek(temak_lista, tipus):
    tetelek_dict = {}
    for i, tema in enumerate(temak_lista):
        if tipus == "matek":
            reszletek = {
                "Szakasz 1": ("I. Alapfogalmak, Definíciók és Elméleti Rendszer", [
                    ("A témakör pontos definíciója és jelölésrendszere", f"A(z) **{tema}** alapegységei, halmazelméleti és logikai keretei. A matematikában minden állítás pontos definíciókra épül, így elengedhetetlen a használt szimbólumok és alaphalmazok pontos ismerete."),
                    ("Értelmezési tartományok és kikötések", "Milyen megszorítások vonatkoznak a kifejezésekre? (Pl. nevező nem lehet nulla, logaritmus alapja pozitív és 1-től különböző kell legyen, gyök alatt nem állhat negatív szám). Ezen feltételek ellenőrzése minden számítás első lépése."),
                    ("Módszertani célkitűzés", "Miért alkalmazzuk ezt a matematikai eszközt? Hogyan segít ez valós idejű problémák, egyenletrendszerek vagy térbeli alakzatok leírásában?")
                ]),
                "Szakasz 2": ("II. Főbb Tételek, Szabályok és Levezetések", [
                    ("Központi tételek és logikai összefüggések", f"A(z) {tema} területéhez tartozó legfontosabb tételek. Itt tekintjük át a képletek érvényességi feltételeit és egymásból való levezetésüket."),
                    ("Algoritmusok lépésről lépésre", "1. Adatok rögzítése és feltételek vizsgálata.\n2. A megfelelő képlet vagy azonosság kiválasztása.\n3. Az algebrai vagy numerikus műveletek elvégzése.\n4. Ellenőrzés visszahelyettesítéssel."),
                    ("Gyakori hibaleforrások és buktatók", "Előjelek tévesztése zárójelbontáskor, hamis gyökök beemelése a négyzetre emelés miatt, valamint a mértékegységek elhanyagolása.")
                ]),
                "Szakasz 3": ("III. Részletesen Kidolgozott Példák és Alkalmazások", [
                    ("Alapszintű rutinfeladat részletes megoldása", f"Gyakorlati példa a(z) {tema} közvetlen alkalmazására, lépésről lépésre követhető numerikus menettel."),
                    ("Emelt szintű, összetett feladattípus", "Komplex, több témakört (pl. függvényvizsgálat és trigonometria) összekapcsoló érettségi feladat elemzése."),
                    ("Gyakorlati modellalkotás", "Hogyan hasznosul ez a tudás a fizikai mozgások leírásában, a pénzügyi kalkulációkban vagy a statisztikai elemzésekben?")
                ])
            }
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Definíciók:** A(z) {tema} alapfogalmai.\n2. **Főbb képletek:** A központi összefüggések felírása.\n3. **Alkalmazás:** Egy tipikus feladat bemutatása."
        elif tipus == "tori":
            reszletek = {
                "Szakasz 1": ("I. Történelmi Előzmények és Okok", [
                    ("Gazdasági és társadalmi háttér", f"Milyen folyamatok, struktúrák vagy válságok hívták életre a(z) **{tema}** eseményeit? A korabeli népesség helyzete, vagyoni viszonyok és rétegződés."),
                    ("Okozati összefüggések és érdekek", "A kortárs nagyhatalmi törekvések, geopolitikai érdekek, vallási ellentétek vagy gazdasági függőségi viszonyok rendszere."),
                    ("A kiváltó ok (casus belli)", "Az a konkrét, sokszor váratlan esemény vagy provokáció, amely a lappangó feszültséget nyílt konfliktusba vagy rendszerváltásba torkollatta.")
                ]),
                "Szakasz 2": ("II. Fő Események, Személyek és Intézmények", [
                    ("Kronológiai ív és legfontosabb fordulópontok", f"A(z) {tema} kulcsfontosságú dátumai, csatái, békekötései, törvényhozási határozatai vagy reformhullámai."),
                    ("Meghatározó történelmi személyek", "Az uralkodók, hadvezérek, politikusok, forradalmárok tettei, egyéni motivációi, politikai stratégiáik és azok történelmi súlya."),
                    ("Intézményi és katonai háttér", "Hogyan működtek a korabeli állami szervek, parlamentek, egyházak, vagy milyen fegyvernemek, harcmodorok határozták meg az eseményeket?")
                ]),
                "Szakasz 3": ("III. Következmények, Mérleg és Hatástörténet", [
                    ("Rövid távú következmények", f"Területi változások, hatalmi átrendeződések, vérveszteségek, politikai konszolidáció vagy éppen radikális fordulatok a(z) {tema} után."),
                    ("Hosszú távú hatások a társadalomra", "Hogyan formálta át ez a korszak az ország határait, gazdaságát, törvényeit és a mindennapi ember életét a következő évszázadokban?"),
                    ("Történeti értékelés és viták", "Hogyan ítéli meg a modern történettudomány ezt a korszakot, milyen különböző szempontokból elemezik a történészek?")
                ])
            }
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Előzmények:** Mi vezetett ide?\n2. **Fő események és személyek:** A(z) {tema} fordulópontjai.\n3. **Következmények:** Milyen hatást gyakorolt a történelemre?"
        elif tipus == "nyelvtan":
            reszletek = {
                "Szakasz 1": ("I. Elméleti Rendszer és Alapfogalmak", [
                    ("A nyelvi jelenség elhelyezése", f"A(z) **{tema}** pontos helye a magyar nyelv hang-, szó-, mondat- vagy szövegtani rendszerében. A szakszerű terminológia tisztázása."),
                    ("Alaptételek és szerkezeti egységek", "Milyen alapegységekből épül fel ez a nyelvi jelenség, mik a főbb kategóriái és paradigmái?"),
                    ("A rendszer működési elve", "Hogyan illeszkedik be ez a szabály a magyar nyelv logikai és kifejezési struktúrájába?")
                ]),
                "Szakasz 2": ("II. Szabályok, Paradigmák és Kivételek", [
                    ("A részletes szabályrendszer", f"A(z) {tema} törvényszerűségei, képzési szabályai, toldalékolási menete vagy mondattani kapcsolódásai."),
                    ("Kivételek és különleges esetek", "Melyek azok a rendhagyó alakok vagy kivételek, amelyeket a vizsgán szigorúan számon kérnek?"),
                    ("Helyesírási és nyelvhelyességi normák", "Az MTA által elvárt helyesírási szabályok, gyakori hibák elkerülése és a normatív nyelvhasználat.")
                ]),
                "Szakasz 3": ("III. Gyakorlati Elemzés és Stilisztikai Érték", [
                    ("Szakszerű elemzési minták", f"Hogyan kell felbontani, ábrázolni vagy elemezni a(z) {tema} körébe tartozó nyelvi példákat?"),
                    ("Stilisztikai és pragmatikai funkció", "Milyen kifejezőerőt, hangulatot vagy szövegszervező erőt biztosít ezen nyelvi elem alkalmazása?"),
                    ("Gyakorlati kommunikációs példák", "Mondatpéldák, szövegrészletek elemzése és magyarázata.")
                ])
            }
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Fogalom:** A(z) {tema} elmélete.\n2. **Szabályok:** A legfontosabb törvények.\n3. **Példa:** Elemzési bemutató."
        else: # irodalom
            reszletek = {
                "Szakasz 1": ("I. Történeti, Eszmei és Művészettörténeti Kontextus", [
                    ("Irodalomtörténeti korszak és eszmék", f"A(z) **{tema}** születésének korszaka (pl. reneszánsz, romantika, modernség) és annak meghatározó szellemi áramlatai."),
                    ("Filozófiai és morális háttér", "Milyen világkép, emberkép vagy egzisztenciális kérdések hívták életre a művet/műveket?"),
                    ("Szerzői életműbe ágyazottság", "Hol helyezkedik el ez az alkotás a szerző életpályájában, milyen művészi fejlődést mutat?")
                ]),
                "Szakasz 2": ("II. Részletes Műelemzés (Tematika, Szerkezet, Poétika)", [
                    ("Központi téma és motívumrendszer", f"A(z) {tema} alapkonfliktusa, vezérmotívumai (pl. bűn és bűnhődés, halhatatlanság, magány, nemzeti sors)."),
                    ("Szerkezeti felépítés és kompozíció", "Hogyan épül fel a mű? Expozíció, kibontakozás, tetőpont, fordulat, megoldás részletes elemzése."),
                    ("Poétikai és stilisztikai eszközök", "Verselés, ritmus, rímelés, nyelvi alakzatok, szimbólumok, metaforarendszer vagy drámai formanyelv vizsgálata.")
                ]),
                "Szakasz 3": ("III. Egyetemes Üzenet és Hatástörténet", [
                    ("Eszmei üzenet és morális tanulság", f"Mit üzen a(z) {tema} az emberi létezésről, a morálról vagy a társadalomról a keletkezésekor és napjainkban?"),
                    ("Kulturális utóélet és recepció", "Hogyan hatott ez a mű a későbbi irodalmi generációkra, színházra, zenére vagy a vizuális művészetekre?"),
                    ("Gyakorlati vizsgaszempontok", "Milyen kulcsmondatokat, idézeteket vagy szempontokat érdemes feltétlenül megemlíteni a felelet során?")
                ])
            }
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Kontextus:** Kor és eszmék.\n2. **Műelemzés:** A(z) {tema} főbb motívumai és poétikája.\n3. **Üzenet:** Mi a jelentősége?"

        tetelek_dict[f"{i+1}. {tema}"] = {
            "alcim": f"Hivatalos érettségi tétel – Részletes, kibontható tananyag: {tema}",
            "reszletek": reszletek,
            "szobeli": szobeli,
            "kviz": [
                {"k": f"Alapvető vizsgakérdés a(z) '{tema}' tétel lexikális anyagából?", "v": True, "m": "Igen, a vizsgakövetelmények szigorú alapját képezi."},
                {"k": f"Kapcsolódik ehhez a témához kiemelt elemzési vagy számítási szempont?", "v": True, "m": "Természetesen."}
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

# --- MODULOK ---
if menupont == "📚 Tételek & Vázlatok (20 db)":
    tetel_nev = st.selectbox("Válassz a 20 hivatalos tétel közül:", list(aktiv_tetelek.keys()))
    t_adat = aktiv_tetelek[tetel_nev]
    st.markdown(f"<div class='topic-card'><h2>{tetel_nev}</h2><p style='color:#a5b4fc;'>{t_adat['alcim']}</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes Tananyag", "🎙️ 3 Perces Felelet", "⚡ Interaktív Kvíz"])
    with tab1:
        st.info("💡 Kattints az egyes alfejezetekre a részletes kifejtés és magyarázat kibontásához!")
        for szakasz_kod, (cim_nev, alfejezetek) in t_adat["reszletek"].items():
            with st.expander(cim_nev):
                for alcim, leiras in alfejezetek:
                    st.markdown(f"#### 🔹 {alcim}")
                    st.markdown(leiras)
                    st.markdown("---")
    with tab2: 
        st.markdown(f"<div class='oral-box'>{t_adat['szobeli']}</div>", unsafe_allow_html=True)
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
            st.image(Image.open(fajl), caption="Feltöltött kép előnézete")
            fajl.seek(0)
        if st.button("🚀 Elemzés és Összefoglalás"):
            with st.spinner("Elemzés folyamatban..."):
                payload = [Image.open(fajl), "Elemezd részletesen:"] if fajl.type.startswith("image/") else [f"Elemezd részletesen: {read_file(fajl)[:10000]}"]
                st.session_state.aktiv_elemzes_eredmeny = ai_generalas_tartalom(payload)
        if "aktiv_elemzes_eredmeny" in st.session_state:
            st.markdown(f"<div class='topic-card'>{st.session_state.aktiv_elemzes_eredmeny}</div>", unsafe_allow_html=True)

elif menupont == "🎧 Hangoskönyv (Tétel-specifikus)":
    st.subheader("🎧 Tétel-specifikus Hangoskönyv")
    t_nev = st.selectbox("Válassz tételt a hallgatáshoz:", list(aktiv_tetelek.keys()))
    t_adat = aktiv_tetelek[t_nev]
    hang_szoveg = ""
    for _, (_, alfejezetek) in t_adat["reszletek"].items():
        for alcim, leiras in alfejezetek:
            hang_szoveg += f"{alcim}. {leiras} "
    
    st.info(f"⚡ A(z) **{t_nev}** tétel hanganyaga elkészült:")
    tts = gTTS(text=hang_szoveg[:4000], lang='hu', slow=False)
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)
    st.audio(f, format="audio/mp3")

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
        st.markdown(ai_generalas_tartalom(["Értékeld a szóbeli feleletet."]))

elif menupont == "✍️ Esszé & Feladat Labor":
    sz = st.text_area("Írd be a szöveget:")
    if st.button("Javítás") and sz:
        st.markdown(ai_generalas_tartalom([f"Javítsd ki: {sz}"]))

elif menupont == "🎭 Detektív Játék (20 db)":
    st.subheader("🎭 Detektív Feladványok")
    idx = st.session_state.detektiv_index % len(aktiv_det)
    f = aktiv_det[idx]
    st.markdown(f"<div class='topic-card' style='text-align:center;'><h3 style='color:#f472b6;'>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válaszd ki a megfejtést:", f['opciok'], index=None, key=f"det_{idx}")
    if st.button("🔍 Ellenőrzés"):
        if tipp == f['helyes']: st.balloons(); st.success("Helyes!")
        else: st.error(f"Helytelen! Helyes: {f['helyes']}")
    if st.button("➡️ Következő"):
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

elif menupont == "🤖 AI Érettségi Mentor":
    for msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    k = st.text_input("Kérdezz a mentortól:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas_tartalom([k])})
        st.rerun()
