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
    
    div[data-testid="stExpander"] { background-color: #111827 !important; border: 1px solid #374151 !important; border-radius: 12px !important; }
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
    
    .deep-text { 
        background-color: #111827; 
        color: #ffffff !important; 
        border: 1px solid #374151; 
        padding: 40px; 
        border-radius: 14px; 
        line-height: 2.0; 
        font-size: 1.15rem;
    }
    .deep-text h3 { color: #818cf8 !important; margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #374151; padding-bottom: 8px; }
    .deep-text h4 { color: #a5b4fc !important; margin-top: 20px; }
    
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white; }
    .timeline-item { background-color: #111827; border-left: 5px solid #a855f7; padding: 18px 22px; margin-bottom: 16px; border-radius: 0 14px 14px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 14px 20px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #111827; color: #f3f4f6; border: 1px solid #374151; padding: 14px 20px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
<div class="menu-label">Menü</div>
""", unsafe_allow_html=True)

# --- KÖNYV SZINTŰ, RÉSZLETES TANANYAG GENERÁTOR ---
def generalo_tetelek(temak_lista, tipus):
    tetelek_dict = {}
    for i, tema in enumerate(temak_lista):
        if tipus == "matek":
            tartalom = f"""
### I. Bevezetés, Alapfogalmak és Elméleti Rendszer
* **A témakör pontos definíciója:** A(z) **{tema}** alapegységei, jelölései, halmazelméleti és logikai keretei. Részletesen tisztázni kell a használt fogalmakat, mivel a matematika szigorú logikai láncmegoldásokra épül.
* **Értelmezési tartomány és feltételek:** Milyen halmazon értelmezzük a kifejezéseket, milyen kikötések (pl. nevező nem lehet nulla, gyök alatt nem lehet negatív szám) vonódnak be automatikusan a vizsgálatba?
* **Történeti és módszertani kitekintés:** Hogyan alakult ki ez a matematikai eszköz, miért van rá szükség a gyakorlati problémák modellezésében?

### II. Főbb Tételek, Szabályok, Levezetések és Algoritmusok
* **Központi tételek:** A(z) {tema} legfontosabb összefüggéseinek szigorú matematikai levezetése és bizonyítási menete. 
* **Algoritmusok lépésről lépésre:** 
  1. Első lépés: A feltételek ellenőrzése és az adatok rögzítése.
  2. Második lépés: A megfelelő képlet, azonosság vagy függvénytranszformáció kiválasztása.
  3. Harmadik lépés: A számítás elvégzése, egyenletrendszerek rendezése vagy geometriai szerkesztés.
  4. Negyedik lépés: Ellenőrzés visszahelyettesítéssel vagy nagyságrendi becsléssel.
* **Gyakori hibaleforrások:** Előjel-tévesztések, zárójelezési hibák, a definíciós tartomány figyelmen kívül hagyása és a hamis gyökök kiszűrése.

### III. Részletesen Kidolgozott Mintafeladatok és Alkalmazások
* **1. Alapszintű feladat:** Közvetlen képletalkalmazás, rutinművelet a(z) {tema} köréből, részletes numerikus megoldással.
* **2. Emelt szintű / Összetett feladat:** Szöveges modell, paraméteres egyenlet vagy kombinált geometriai probléma, ahol a(z) {tema} más matematikai ágakkal (pl. trigonometria, koordináta-geometria) kapcsolódik össze.
* **Gyakorlati jelentőség:** Hogyan alkalmazzák ezt a mérnökök, a pénzügyi szakemberek vagy a természettudósok a mindennapi modellezésben?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Definíció és keretek:** A(z) {tema} alapfogalmainak tisztázása.\n2. **Főbb képletek és tételek:** A központi összefüggések felírása és magyarázata.\n3. **Alkalmazási példa:** Egy tipikus érettséges feladattípus rövid bemutatása."
        elif tipus == "tori":
            tartalom = f"""
### I. Gazdasági, Társadalmi és Politikai Előzmények
* **A korszak háttere:** Milyen folyamatok, struktúrák, válságok vagy gazdasági tényezők készítették elő a(z) **{tema}** kialakulását?
* **Okozati összefüggések:** A kortárs nagyhatalmi törekvések, érdekek, társadalmi feszültségek (pl. elszegényedés, polgárosodás, vallási ellentétek) rendszere.
* **Kiváltó okok (casus belli):** Az a konkrét esemény vagy pillanat, amely a folyamatot nyílt konfliktusba vagy rendszerszintű változásba torkollatta.

### II. Fő Események, Kulcsszereplők és Intézményi Keretek
* **Kronológiai ív és fordulópontok:** A(z) {tema} legfontosabb dátumai, csatái, békekötései, törvényei vagy reformintézkedései.
* **Meghatározó történelmi személyek:** Az uralkodók, hadvezérek, politikusok, reformátorok vagy népi hősök tettei, motivációi, stratégiai döntéseik és azok következményei.
* **Intézményi és katonai háttér:** Hogyan működtek a korabeli államapparátusok, parlamentek, egyházak, hadseregek vagy gazdasági intézmények?

### III. Következmények, Mérleg és Hatástörténet
* **Rövid távú következmények:** Területveszteségek vagy -nyereségek, hatalmi átrendeződések, vérveszteségek, politikai konszolidáció vagy forradalmi terror.
* **Hosszú távú hatások:** Hogyan formálta át a(z) {tema} az érintett ország (vagy Európa) társadalmi szerkezetét, határait, gazdaságát a következő évtizedekben vagy évszázadokban?
* **Történeti értékelés:** Hogyan ítéli meg a modern történettudomány ezt a korszakot, milyen historiográfiai viták övezik?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Előzmények:** Mi vezetett ide?\n2. **Fő események és személyek:** A(z) {tema} legfontosabb fordulópontjai.\n3. **Következmények:** Milyen hatást gyakorolt a történelem folyamatára?"
        elif tipus == "nyelvtan":
            tartalom = f"""
### I. Elméleti Rendszer és Fogalomkör
* **A nyelvi jelenség helye:** A(z) **{tema}** pontos elhelyezése a magyar nyelv hang-, szó-, mondat- vagy szövegtani rendszerében.
* **Alapfogalmak és terminológia:** A szakszerű nyelvészeti fogalmak pontos meghatározása.
* **A rendszerszintű működés elve:** Hogyan tagozódik be ez a jelenség a magyar nyelv egységébe?

### II. Szabályszerűségek, Paradigmák és Kivételek
* **A szabályok kifejtése:** A(z) {tema} strukturális törvényszerűségei, ragozási sorai, képzési módjai vagy mondattani kapcsolatai.
* **Kivételek és különleges esetek:** Melyek azok a nyelvi formák vagy kivételek, amelyeket a vizsgán különösen figyelembe kell venni?
* **Helyesírási és nyelvhelyességi normák:** Gyakorlati helyesírási szabályok, gyakran elkövetett hibák és az MTA által elvárt helyes formák.

### III. Gyakorlati Elemzés és Stilisztikai Érték
* **Elemzési mintaelemzés:** Hogyan kell felbontani, ábrázolni vagy elemezni egy erre vonatkozó nyelvi példát?
* **Stilisztikai funkció:** Milyen kifejezőerőt, hangulatot vagy pragmatikai célt szolgál a(z) {tema} alkalmazása a szövegben?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Fogalom és elmélet:** A(z) {tema} definíciója.\n2. **Szabályok és kivételek:** A legfontosabb nyelvtani/helyesírási törvények.\n3. **Gyakorlati példa:** Elemzési bemutató."
        else: # irodalom
            tartalom = f"""
### I. Történeti, Eszmei és Művészettörténeti Kontextus
* **Irodalomtörténeti korszak:** A(z) **{tema}** születésének korszaka (pl. ókor, reneszánsz, romantika, modernség) és annak szellemi, művészeti vonulatai.
* **Filozófiai és eszmei háttér:** Milyen világkép, emberkép, morális vagy egzisztenciális kérdések (pl. felvilágosodás, determinizmus, egzisztencializmus) hívták életre a művet/műveket?
* **Szerzői életmű beágyazottsága:** Hol helyezkedik el ez a mű az alkotó pályájában, milyen belső fejlődési ívet mutat?

### II. Részletes Műelemzés (Tematika, Szerkezet, Poétika)
* **Központi téma és motívumrendszer:** A(z) {tema} alapkonfliktusa, vezérmotívumai (pl. bűn és bűnhődés, halhatatlanság, magány, nemzeti sors).
* **Szerkezeti felépítés és kompozíció:** Hogyan épül fel a mű? (Expozíció, kibontakozás, tetőpont, fordulat, megoldás; vagy a lírai kompozíció belső íve).
* **Poétikai és stilisztikai eszközök:** Verselés, ritmus, rímelés, nyelvi alakzatok, szimbólumok, metaforarendszer, narratív technikák vagy drámai formanyelv részletes vizsgálata.
* **Karakterek és viszonyrendszerek:** A szereplők lelkiállapota, fejlődése, motivációi és drámai összecsapásai.

### III. Egyetemes Üzenet és Hatástörténet
* **Eszmei üzenet:** Mit üzen a mű az emberi létezésről, a morálról vagy a társadalomról a keletkezés sakor és ma?
* **Kulturális utóélet:** Hogyan hatott a(z) {tema} a későbbi magyar és európai irodalomra, színházra, zenére vagy a vizuális művészetekre?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:**\n1. **Kontextus:** Kor, eszmék és életmű.\n2. **Műelemzés:** A(z) {tema} főbb motívumai, szerkezete és poétikája.\n3. **Üzenet és utóélet:** Mi a mű jelentősége?"

        tetelek_dict[f"{i+1}. {tema}"] = {
            "alcim": f"Hivatalos érettségi tétel – Részletes, könyv szintű kidolgozás: {tema}",
            "tartalom": tartalom.strip(),
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
            return "⚠️ A szerver jelenleg túlterhelt (503-as hiba)."
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
    return f"{alap_szoveg}\n\n{alap_szoveg}"

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
                    szoveg = read_file(fajl)
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
                        q_payload = [img_data, "Készíts 5 db feleletválasztós vizsgakérdést a képen látható tartalom alapján. Add vissza KIZÁRÓLAG érvényes JSON formátumban: [{\"question\": \"...\", \"options\": [\"A) ...\", \"B) ...\", \"C) ...\", \"D) ...\"], \"answer\": \"A) ...\", \"explanation\": \"...\"}]"]
                    else:
                        doc_text = st.session_state.get('aktiv_fajl_szoveg', '')[:8000]
                        q_payload = [f"Készíts 5 db feleletválasztós vizsgakérdést a dokumentum alapján JSON-ban: {doc_text}"]

                    raw_res = ai_generalas_tartalom(q_payload)
                    try:
                        cleaned = raw_res.replace("```json", "").replace("```", "").strip()
                        st.session_state.ai_quiz_data = json.loads(cleaned)
                    except Exception as e:
                        st.error(f"Hiba történt a kvíz feldolgozásakor. ({e})")
                        st.session_state.ai_quiz_data = None

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
                        score = sum(1 for idx, q in enumerate(st.session_state.ai_quiz_data) if user_answers.get(idx) == q['answer'])
                        total = len(st.session_state.ai_quiz_data)
                        st.metric("Elért eredmény", f"{score} / {total} pont", f"{int((score/total)*100)}%")

elif menupont == "🎧 Hangoskönyv (Tétel-specifikus)":
    st.subheader("🎧 Tétel-specifikus Hangoskönyv")
    t_nev = st.selectbox("Válassz tételt a hallgatáshoz:", list(aktiv_tetelek.keys()))
    felolvashato_szoveg = get_tetel_specifikus_szkript(kivalasztott_tantargy, t_nev)[:4000]
    
    st.info(f"⚡ A(z) **{t_nev}** tétel hanganyaga elkészült:")
    tts = gTTS(text=felolvashato_szoveg, lang='hu', slow=False)
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
        st.markdown(ai_generalas_tartalom([f"Javítsd ki ezt az esszét: {sz}"]))

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
