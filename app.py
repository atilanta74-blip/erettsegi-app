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

# --- HIVATALOS, RÉSZLETESEN KIDOLGOZOTT TÉTEL GENERÁTOR ---
def generalo_tetelek(temak_lista, tipus):
    tetelek_dict = {}
    for i, tema in enumerate(temak_lista):
        if tipus == "matek":
            tartalom = f"""
### I. Alapfogalmak, Definíciók és Elméleti Hátterek
* **A témakör axiómái és jelölésrendszere:** A(z) **{tema}** szakszerű matematikai megalapozása, halmazelméleti vagy logikai keretei.
* **Feltételek és értelmezési tartományok:** Milyen megszorítások, feltételek mellett érvényesek a témakör összefüggései?

### II. Főbb Tételek, Szabályok és Képletek
* **Központi tételek és levezetések:** A(z) {tema} legfontosabb képleteinek logikai levezetése, geometriai vagy algebrabeli háttere.
* **Számítási módszerek és algoritmusok:** Lépésről lépésre követhető stratégiák egyenletek, függvényvizsgálatok, sorozatok vagy tértani testek kiszámítására.
* **Gyakori buktatók:** Tipikus hibaleforrások (pl. előjelek, hamis gyökök, mértékegységek) és elkerülésük.

### III. Tipikus Érettségi Feladatok és Alkalmazások
* **I. rész (rövid feladatok):** Alapdefiníciók, gyors számítások és tesztjellegű kérdések a(z) {tema} témaköréből.
* **II. rész (komplex feladatok):** Összetett szöveges vagy bizonyítási feladatok, modellalkotás és gyakorlati alkalmazás a mindennapokban.
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Alapfogalmak és definíciók ({tema}) -> 2. Főbb képletek és tételek bemutatása -> 3. Tipikus feladattípus szemléltetése."
        elif tipus == "tori":
            tartalom = f"""
### I. Történelmi Előzmények és Okok
* **Gazdasági, társadalmi és politikai háttér:** Milyen folyamatok, struktúrák vagy válságok hívták életre a(z) **{tema}** eseményeit?
* **Okozati összefüggések:** A kortárs nagyhatalmi törekvések, érdekek és a kiváltó okok komplex rendszere.

### II. Fő Események, Kulcsszereplők és Intézmények
* **Kronológiai ív és fordulópontok:** A(z) {tema} legfontosabb dátumai, csatái, szerződései vagy politikai fordulatai.
* **Meghatározó történelmi személyek:** Az uralkodók, hadvezérek, politikusok vagy gondolkodók tettei, motivációi és döntéseinek súlya.
* **Intézményi keretek:** Hogyan működtek a korabeli államapparátusok, gazdasági formációk vagy társadalmi csoportok?

### III. Következmények és Hatástörténet
* **Rövid és hosszú távú hatások:** Milyen geopolitikai, társadalmi vagy kulturális változásokat eredményezett a(z) {tema}?
* **Történeti értékelés:** Hogyan ítéli meg a jelenkori történettudomány ezt a korszakot, és milyen tanulságokat hordoz?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Előzmények és okok -> 2. Fő események és szereplők ({tema}) -> 3. Következmények és értékelés."
        elif tipus == "nyelvtan":
            tartalom = f"""
### I. Rendszerszintű Elméleti Alapok
* **Fogalomkör és definíciók:** A(z) **{tema}** helye és szerepe a magyar nyelv hang-, szó-, mondat- vagy szövegtani rendszerében.
* **Nyelvi kategóriák:** Az alapegységek, paradigmák és strukturális összefüggések bemutatása.

### II. Szabályok, Kivételek és Elemzési Szempontok
* **Nyelvtani és helyesírási szabályok:** A(z) {tema} törvényszerűségei, kivételei és az analógiák működése.
* **Gyakorlati elemzés:** Hogyan kell szakszerűen elemezni, felbontani vagy helyesbíteni a nyelvi jelenséget?

### III. Kommunikációs és Stilisztikai Érték
* **Stilisztikai funkció:** Milyen jelentésárnyalást vagy kifejezőerőt biztosít a(z) {tema} a beszédben és az írásban?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Elméleti alapok ({tema}) -> 2. Szabályok és elemzés -> 3. Kommunikációs szerep."
        else: # irodalom
            tartalom = f"""
### I. Történeti és Művészettörténeti Kontextus
* **Irodalomtörténeti kor:** A(z) **{tema}** keletkezésének korszaka (pl. antiskika, reneszánsz, romantika, modernség) és eszmei áramlatai.
* **Filozófiai háttér:** Milyen emberkép, világkép vagy morális kérdések határozták meg a mű(vek) születését?

### II. Részletes Műelemzés és Szerkezet
* **Központi téma és motívumok:** A(z) {tema} alapkonfliktusa, szimbólumai és vezérmotívumai.
* **Kompozíció és poétika:** Műfaji sajátosságok, szerkezeti egységek, narratív technikák vagy verselési formák részletes vizsgálata.
* **Karakterek és viszonyrendszerek:** A szereplők jelleme, fejlődéstörténete és drámai/epikus konfliktusai.

### III. Eszmei Üzenet és Hatástörténet
* **Egyetemes üzenet:** Mit üzen a mű a mai kor olvasójának?
* **Kulturális utóélet:** Hogyan él tovább a(z) {tema} a színházban, képzőművészetben vagy a kortárs kultúrában?
            """
            szobeli = f"**🎙️ 3 perces felelet vázlata:** 1. Történeti kontextus -> 2. Műelemzés és motívumok ({tema}) -> 3. Üzenet és utóélet."

        tetelek_dict[f"{i+1}. {tema}"] = {
            "alcim": f"Hivatalos érettségi tétel részletes kidolgozása: {tema}",
            "tartalom": tartalom.strip(),
            "szobeli": szobeli,
            "kviz": [
                {"k": f"Alapvető lexikális kérdés a(z) '{tema}' tételhez?", "v": True, "m": "Igen, szigorúan követelmény a vizsgán."},
                {"k": f"Kapcsolódik ehhez a témához kiemelt elemzési szempont?", "v": True, "m": "Természetesen."}
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
