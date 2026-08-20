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
    .answer-box { background-color: #1f2937; border-left: 4px solid #10b981; padding: 18px; border-radius: 8px; margin-top: 10px; margin-bottom: 15px; color: #f3f4f6; line-height: 1.7; }
    
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white; }
    .timeline-item { background-color: #111827; border-left: 5px solid #a855f7; padding: 18px 22px; margin-bottom: 16px; border-radius: 0 14px 14px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 14px 20px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #111827; color: #f3f4f6; border: 1px solid #374151; padding: 14px 20px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
<div class="menu-label">Menü</div>
""", unsafe_allow_html=True)

# --- BŐVÍTETT, KIFEJTETT TARTALMÚ ADATBÁZIS ---
def generalo_tetelek(temak_lista, tipus):
    tetelek_dict = {}
    for i, tema in enumerate(temak_lista):
        if tipus == "matek":
            reszletek = {
                "Szakasz 1": ("I. Alapfogalmak, Definíciók és Elméleti Rendszer", [
                    ("Pontos fogalommeghatározás és jelölésrendszer", f"A(z) **{tema}** témakör matematikai megalapozása során rögzítenünk kell a halmazokat, relációkat és alapvető szimbólumokat. Minden kifejezésnek megvan a maga pontos matematikai jelentése, amely elengedhetetlen a helyes logikai következtetésekhez.", f"A matematika szigorú axiómákra épül. A(z) {tema} területén a jelölések pontos ismerete biztosítja a helyes értelmezési tartomány felírását."),
                    ("Értelmezési tartományok és kikötések", "Melyek a kötelező matematikai kikötések?", "A számítások megkezdése előtt mindig meg kell vizsgálni a nevezőket (nem lehetnek nullák), a gyök alatti mennyiségeket (nem lehetnek negatívak páros gyök esetén), valamint a logaritmus alapját és argumentumát."),
                    ("Gyakorlati modellalkotás", "Miért van erre szükség a gyakorlatban?", "A modellalkotás során a valós élet problémáit (pl. sebesség, út, idő számítása, pénzügyi kamatszámítás) öntjük matematikai formába.")
                ]),
                "Szakasz 2": ("II. Főbb Tételek, Szabályok és Számítási Menet", [
                    ("Központi tételek és levezetések", f"Hogyan épülnek fel a(z) {tema} tételei?", f"A területhez tartozó legfontosabb összefüggések és azonosságok logikai levezetése, amelyek ismerete elengedhetetlen a vizsgán."),
                    ("Lépésről lépésre követhető algoritmus", "Hogyan kell megoldani egy tipikus feladatot?", "1. lépés: Az adatok leírása és kikötések felírása.\n2. lépés: A megfelelő képlet kiválasztása.\n3. lépés: Az algebrai rendezés elvégzése.\n4. lépés: Ellenőrzés visszahelyettesítéssel."),
                    ("Gyakorlati hibaleforrások", "Mik a leggyakoribb vizsgabeli hibák?", "Előjelek elrontása a zárójelbontáskor, a négyzetre emelésből fakadó hamis gyökök beemelése, valamint a mértékegységek elhagyása.")
                ]),
                "Szakasz 3": ("III. Részletesen Kidolgozott Mintafeladatok", [
                    ("Alapszintű rutinfeladat részletes megoldása", f"Konkrét példa a(z) {tema} alkalmazására", f"A képlet közvetlen behelyettesítése és kiszámítása lépésről lépésre."),
                    ("Emelt szintű, összetett feladat", "Komplex vizsgapélda elemzése", "Olyan feladat, amely a(z) {tema} területét összekapcsolja egy másik területtel (pl. koordináta-geometriával)."),
                    ("Ellenőrzési technikák a vizsgán", "Hogyan győződhetünk meg a helyességről?", "Visszahelyettesítés az eredeti egyenletbe, nagyságrendi becslés és logikai ellenőrzés.")
                ])
            }
        elif tipus == "tori":
            reszletek = {
                "Szakasz 1": ("I. Történelmi Előzmények, Okok és Háttér", [
                    ("Gazdasági és társadalmi előzmények", f"Mi jellemezte a(z) **{tema}** előtti időszakot?", f"A társadalom elégedetlensége, a vagyoni különbségek növekedése, a gazdasági struktúrák elavulása vagy a reformokat kikényszerítő belső feszültségek."),
                    ("Okozati összefüggések és érdekek", "Kik voltak a kulcsszereplők és mik voltak a céljaik?", "A kortárs nagyhatalmi törekvések, gazdasági érdekek, területi követelések, vallási ellentétek és a hatalmi egyensúly megborulása."),
                    ("A kiváltó ok (casus belli)", "Mi lobbantotta be a konfliktust?", "Az a konkrét, sokszor drasztikus esemény (pl. merénylet, törvény elfogadása vagy katonai provokáció), amely az addig lappangó ellentéteket nyílt összecsapássá váltotta.")
                ]),
                "Szakasz 2": ("II. Fő Események, Személyek és Intézmények", [
                    ("Kronológiai ív és legfontosabb fordulópontok", f"Melyek a(z) {tema} legfontosabb eseményei?", f"A folyamat fontosabb dátumai, csatái, békekötései, törvényhozási határozatai és reformintézkedései kronologikus sorrendben."),
                    ("Meghatározó történelmi személyek és tetteik", "Kik irányították az eseményeket?", "A korszak kiemelt uralkodói, hadvezérei, politikusai (pl. Periklész, Julius Caesar, Szent István, Hunyadi Mátyás, Kossuth Lajos). Az ő személyes döntéseik, politikájuk és azok történelmi következményei."),
                    ("Intézményi, gazdasági és katonai háttér", "Hogyan működtek a korabeli szervek?", "A korabeli államszervezet, parlamentek, egyházak működése, valamint a harcmodor, a fegyvernemek fejlődése és a hátország logisztikai feladatai.")
                ]),
                "Szakasz 3": ("III. Következmények, Mérleg és Hatástörténet", [
                    ("Rövid távú következmények", f"Mi történt közvetlenül a(z) {tema} után?", f"Területi veszteségek vagy nyereségek, hatalmi átrendeződések, vérveszteségek, politikai konszolidáció vagy radikális fordulatok."),
                    ("Hosszú távú hatások a társadalomra", "Hogyan formálta át a jövőt?", "Az érintett ország társadalmi szerkezetének, jogrendszerének, határainak és gazdaságának tartós megváltozása a következő évszázadokban."),
                    ("Történeti értékelés és viták", "Hogyan ítéli meg a korunk?", "A modern történettudomány szempontjai, a különböző történeti iskolák értékelései és a korszak által hordozott egyetemes tanulságok.")
                ])
            }
        elif tipus == "nyelvtan":
            reszletek = {
                "Szakasz 1": ("I. Elméleti Rendszer és Alapfogalmak", [
                    ("A nyelvi jelenség elhelyezése", f"Hol helyezkedik el a(z) **{tema}** a nyelvben?", f"A magyar nyelv hang-, szó-, mondat- vagy szövegtani rendszerén belül elfoglalt pontos helye, a szakszerű terminológia tisztázása."),
                    ("Alaptételek és kategóriák", "Milyen alapegységekből áll?", "A főbb nyelvtani kategóriák, paradigmák, morfémák vagy szintaktikai egységek bemutatása."),
                    ("A rendszer működési elve", "Hogyan illeszkedik be a nyelvbe?", "Hogyan szolgálja a szabály a gondolatok pontos kifejezését és a logikus szerkesztést.")
                ]),
                "Szakasz 2": ("II. Szabályok, Paradigmák és Kivételek", [
                    ("A részletes szabályrendszer", f"Milyen szabályok vonatkoznak erre?", f"A(z) {tema} képzési szabályai, toldalékolási menete, hangtani törvényszerűségei vagy mondattani kapcsolódásai."),
                    ("Kivételek és különleges esetek", "Melyek a rendhagyó esetek?", "Azok a kivételek, alakzatok vagy ragozási formák, amelyeket a vizsgán különösen szigorúan kérdeznek."),
                    ("Helyesírási és nyelvhelyességi normák", "Mik az elvárt normák?", "Az MTA által megfogalmazott helyesírási alapelvek, gyakori hibák és a hivatalos nyelvhasználat előírásai.")
                ]),
                "Szakasz 3": ("III. Gyakorlati Elemzés és Stilisztika", [
                    ("Szakszerű elemzési minták", "Hogyan kell elemezni egy példát?", "Lépésről lépésre követhető elemzési útmutató mondat-, szó- vagy szövegelemzéshez."),
                    ("Stilisztikai és pragmatikai funkció", "Mi a célja a szövegben?", "A kifejezőerő, a hangulatkeltés és a szövegszervező erő biztosítása a kommunikációban.")
                ])
            }
        else: # irodalom
            reszletek = {
                "Szakasz 1": ("I. Kontextus, Történeti és Eszmei Háttér", [
                    ("Irodalomtörténeti korszak", f"Milyen korban született a(z) **{tema}**?", f"A keletkezés irodalomtörténeti korszaka (pl. reneszánsz, romantika, modernség) és annak meghatározó eszmei, művészeti áramlatai."),
                    ("Filozófiai és morális háttér", "Milyen világkép hatott a műre?", "Az emberkép, a morális dilemmák, a korszakra jellemző világmagyarázatok és a szerzői életműbe való beágyazottság.")
                ]),
                "Szakasz 2": ("II. Részletes Műelemzés (Tematika, Szerkezet, Poétika)", [
                    ("Központi téma és motívumrendszer", f"Mik a(z) {tema} legfőbb motívumai?", f"Az alapkonfliktus, a vezérmotívumok (pl. szerelem, halál, magány, nemzeti sors, bűn és bűnhődés) részletes kifejtése."),
                    ("Szerkezeti felépítés és kompozíció", "Hogyan épül fel a mű?", "Az expozíció, a kibontakozás, a tetőpont, a fordulat és a megoldás drámai vagy epikus ívének elemzése."),
                    ("Poétikai, stilisztikai eszközök", "Milyen eszközökkel dolgozik a szerző?", "Verselés, ritmus, rímelés, nyelvi alakzatok, metaforarendszer, szimbólumok és narratív technikák vizsgálata.")
                ]),
                "Szakasz 3": ("III. Egyetemes Üzenet és Hatástörténet", [
                    ("Egyetemes eszmei üzenet", "Mit üzen a mű az embernek?", "Az emberi létezésre vonatkozó örök érvényű tanulságok, amelyek a mai olvasó számára is aktuálisak maradnak."),
                    ("Kulturális utóélet és recepció", "Hogyan él tovább a mű?", "Hatása a későbbi irodalmi generációkra, a színházművészetre, a filmművészetre és a képzőművészetre.")
                ])
            }

        tetelek_dict[f"{i+1}. {tema}"] = {
            "alcim": f"Hivatalos érettségi tétel – Részletesen kifejtett tananyag: {tema}",
            "reszletek": reszletek,
            "szobeli": f"**🎙️ 3 perces felelet vázlata a(z) {tema} tételhez:**\n1. **Bevezetés:** Történeti/elméleti kontextus tisztázása.\n2. **Fő rész:** A legfontosabb művek, események vagy képletek részletes elemzése.\n3. **Összegzés:** Hatástörténet és egyetemes tanulságok.",
            "kviz": [
                {"k": f"Alapvető vizsgakérdés a(z) '{tema}' tétel lexikális anyagából?", "v": True, "m": "Igen, a vizsgakövetelmények szigorú alapját képezi."},
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
if 'chat_history' not in st.session_state: st.session_state.chat_history = [{"role": "ai", "text": "Üdvözöllek!"}]

st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 VizsgaMester</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #9ca3af; font-size: 0.85rem; margin-top: -10px; margin-bottom: 20px;'>powered by Nagy Attila</p>", unsafe_allow_html=True)

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

# Külön sorba tettük a neved, hogy garantáltan látszódjon a címsor alatt
st.title("🎓 VizsgaMester")
st.markdown("<p style='font-size: 1.2rem; color: #818cf8; font-weight: 600; margin-top: -15px; margin-bottom: 15px;'>powered by Nagy Attila</p>", unsafe_allow_html=True)
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
        st.info("💡 Kattints az egyes alfejezetekre (I., II., III.) a részletesen kifejtett válaszok és magyarázatok eléréséhez!")
        for szakasz_kod, (cim_nev, alfejezetek) in t_adat["reszletek"].items():
            with st.expander(cim_nev):
                for kerdes, leiras, valasz in alfejezetek:
                    st.markdown(f"#### 🔹 {kerdes}")
                    st.markdown(f"*{leiras}*")
                    st.markdown(f"<div class='answer-box'><strong>📖 Részletes válasz / Magyarázat:</strong><br>{valasz}</div>", unsafe_allow_html=True)
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
        for kerdes, leiras, valasz in alfejezetek:
            hang_szoveg += f"{kerdes}. {valasz} "
    
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
