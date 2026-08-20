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
# TELJES ADATBÁZISOK (Irodalom, Nyelvtan, Történelem, Matek)
# -------------------------------------------------------------
tetelek_irodalom = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, nagykőrösi és margitszigeti korszak",
        "vazlat": "### I. Műfajelmélet: Líra, epika és dráma szintézise.\n### II. Nagykőrösi korszak: Történelmi ellenállás és lélektan.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. Nagykőrösi balladák (Ágnes asszony, Szondi két apródja, A walesi bárdok).",
        "kviz": [{"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A három műnem találkozása."}]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus szintézise, polgári meghasonlás",
        "vazlat": "### I. Műfaj: Romantikus mesei fordulatok és realista társadalomrajz.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1872 kontextusa -> 2. Timár Mihály kettős élete és a Senki szigete.",
        "kviz": [{"k": "A Senki szigete pénzmentes természeti utópia a regényben.", "v": True, "m": "A társadalmi konvenciókon kívül áll."}]
    },
    "3. Petőfi Sándor költészete": {
        "alcim": "A népies helyzetdalok, tájleíró versek és a látomásköltészet",
        "vazlat": "### I. Népies lakodalom és tájköltészet.\n### II. Az Apostol és a látomásversek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Petőfi költészetének fordulatai -> 2. A szabadság és szerelem harmóniája.",
        "kviz": [{"k": "A Tisza című vers tájleírás és életkép egyszerre.", "v": True, "m": "A folyó és az Alföld egysége."}]
    },
    "4. Madách Imre: Az ember tragédiája": {
        "alcim": "Filozófiai dráma, emberiségdráma, történelmi színhelyek",
        "vazlat": "### I. Keretszín: Lucifer és az Úr vitája.\n### II. Történelmi színek: Egyiptom, Athén, Róma, London, stb.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Ádám és Éva szerepe -> 2. 'Küzdj és bízva bízzál!' üzenet.",
        "kviz": [{"k": "A falanszter színben a művészet és az egyéniség teljes eltörlése jelenik meg.", "v": True, "m": "A tudomány uralma."}]
    }
}

tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, funkciók",
        "vazlat": "### I. A Jakobson-féle modell: Adó, Vevő, Üzenet, Kód, Csatorna, Referens.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A kommunikáció definíciója -> 2. Nyelvi funkciók bemutatása példákkal.",
        "kviz": [{"k": "A fatikus funkció célja a kapcsolat felvétele és fenntartása.", "v": True, "m": "Ilyenek a köszönések vagy a telefonos 'halló'."}]
    },
    "2. A magyar helyesírás alapelvei": {
        "alcim": "Kiejtés, szóelemzés, hagyomány, egyszerűsítés elve",
        "vazlat": "### I. A négy fő helyesírási alapelv részletes kifejtése példákkal.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Alapelvek ismertetése -> 2. Kivételek a kiejtés elve alól.",
        "kviz": [{"k": "A 'zsiráf' szó j-vel írása a hagyomány elvére példa.", "v": True, "m": "Történeti írásmód."}]
    },
    "3. Szófajok rendszere a magyar nyelvben": {
        "alcim": "Alaptagok, viszonyszók, igék, főnevek, melléknevek",
        "vazlat": "### I. Alaptagok (ige, főnév, melléknév, számnév, névmás, határozószó).\n### II. Viszonyszók (névelő, névutó, kötőszó, segédige, igekötő, mondatszó).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szófaji csoportosítás szempontjai -> 2. Alaptagok és viszonyszók különbsége.",
        "kviz": [{"k": "A segédige viszonyszó, mert önmagában nem megnevező elem.", "v": True, "m": "Nyelvtani viszonyt fejez ki."}]
    }
}

tetelek_tortenelem = {
    "1. Az athéni demokrácia működése a Kr. e. V. században": {
        "alcim": "Szolón, Kleiszthenész reformjai, Periklész kora",
        "vazlat": "### I. Intézményrendszer: Népgyűlés, Boule, Héliaia, sztratégoszok.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kialakulás -> 2. Cserépszavazás és a démosz jogai.",
        "kviz": [{"k": "Az athéni népgyűlés tagja lehetett minden szabad férfi polgár.", "v": True, "m": "Közvetlen demokrácia volt."}]
    },
    "2. A magyarság honfoglalása és kalandozásai": {
        "alcim": "Etelköz, Vereckei-hágó, kalandozó hadjáratok irányai",
        "vazlat": "### I. A magyarság vándorlása és őshazái.\n### II. A Kárpát-medence elfoglalása és a kalandozások kora.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Honfoglalás okai -> 2. Kalandozások európai hatásai.",
        "kviz": [{"k": "A kalandozások az augsburgi csatában (955) szenvedett vereséggel zárultak nyugat felé.", "v": True, "m": I. Ottó megállította a magyarokat."}]
    },
    "3. Szent István államalapítása és egyházszervezése": {
        "alcim": "Géza politikája, koronázás, vármegyerendszer, tized",
        "vazlat": "### I. Géza fejedelem előkészítő munkája.\n### II. István király egyházmegyéi és törvényei.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kereszténység felvétele -> 2. Vármegyék és püspökségek.",
        "kviz": [{"k": "Szent István tíz falu után egy templom építését rendelte el.", "v": True, "m": "Ez volt a tizedik falu templomépítési kötelezettsége."}]
    }
}

tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció, kombináció",
        "vazlat": "### I. Halmazműveletek és kombinatorikai képletek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Halmazok, metszet, unió -> 2. Ismétlés nélküli és ismétléses permutáció.",
        "kviz": [{"k": "Az 5-ös lottó kihúzásainak száma kombinációval számítható.", "v": True, "m": "A sorrend nem számít."}]
    },
    "2. Másodfokú egyenletek, egyenlőtlenségek és függvények": {
        "alcim": "Megoldóképlet, Viète-formulák, másodfokú függvény tulajdonságai",
        "vazlat": "### I. Diszkrimináns szerepe.\n### II. Parabola csúcspontja, zérushelyei.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Megoldóképlet levezetése -> 2. Függvény transzformációi.",
        "kviz": [{"k": "Ha a diszkrimináns negatív, akkor a másodfokú egyenletnek nincs valós gyöke.", "v": True, "m": "A gyökjel alatt negatív szám áll."}]
    },
    "3. Trigonometria és geometria": {
        "alcim": "Szinusztétel, koszinusztétel, derékszögű háromszög összefüggései",
        "vazlat": "### I. Szögfüggvények értelmezése.\n### II. Háromszögek megoldása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Pitagorasz tétel alkalmazásai -> 2. Koszinusztétel bizonyítása.",
        "kviz": [{"k": "A szinusztétel minden háromszögre érvényes.", "v": True, "m": "A oldal és szemközti szög szinuszának aránya állandó."}]
    }
}

flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra, epika és dráma sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat?", "a": "1908-ban indult, Osvát Ernő szerkesztette."},
    {"q": "Ki írta Az ember tragédiáját?", "a": "Madách Imre (1861-ben jelent meg)."}
]
flashcards_nyelvtan = [
    {"q": "Mi a 4 helyesírási alapelv?", "a": "Kiejtés, szóelemzés, hagyomány, egyszerűsítés."},
    {"q": "Mi a toldalékok sorrendje?", "a": "Tő + Képző + Jel + Rag."}
]
flashcards_tortenelem = [
    {"q": "Mikor adta ki Nagy Lajos az Ősiség törvényét?", "a": "1351-ben."},
    {"q": "Mikor esett el Buda?", "a": "1541. augusztus 29."}
]
flashcards_matek = [
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Melyik tétel általánosítja Pitagoraszt?", "a": "Koszinusztétel."}
]

timeline_irodalom = [
    {"ev": "1848–1849", "cim": "Forradalom lírája", "leiras": "Petőfi Sándor és Arany János munkássága."},
    {"ev": "1908", "cim": "A Nyugat indulása", "leiras": "A modern magyar irodalom mérföldköve."}
]
timeline_nyelvtan = [
    {"ev": "1055", "cim": "Tihanyi apátság alapítólevele", "leiras": "Az első magyar nyelvemlék."},
    {"ev": "1533", "cim": "Komjáti Benedek", "leiras": "Az első magyar nyomtatott könyv."}
]
timeline_tortenelem = [
    {"ev": "1000 / 1001", "cim": "Magyar államalapítás", "leiras": "Szent István király koronázása."},
    {"ev": "1222", "cim": "Aranybulla", "leiras": "II. András kiadja Székesfehérváron."}
]
timeline_matek = [
    {"ev": "Kr. e. VI. század", "cim": "Pitagorasz tétele", "leiras": "Geometriai alapvetés."},
    {"ev": "1637", "cim": "Descartes analitikus geometria", "leiras": "Koordináta-rendszer bevezetése."}
]

detektiv_irodalom = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre", "Arany János", "Radnóti Miklós"], "info": "A felelősségvállalás parancsa a költő művében."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb...”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály", "Arany János", "Ady Endre"], "info": "Petőfi forradalmi felhívó verse."}
]
detektiv_nyelvtan = [
    {"idezet": "„barátság [kiejtve: baraccság]”", "helyes": "Összeolvadás mássalhangzótörvény", "opciok": ["Összeolvadás mássalhangzótörvény", "Zöngésségi részleges hasonulás", "Írásban jelölt teljes hasonulás", "Mássalhangzó-kiesés"], "info": "A t + s hangok találkozásakor [ccs] jön létre."},
    {"idezet": "„lila dalra kelt az éjcsend”", "helyes": "Szinesztézia (Költői kép)", "opciok": ["Szinesztézia (Költői kép)", "Megszemélyesítés", "Metonímia", "Szinekdoché"], "info": "Különböző érzékelési területek összemosása."}
]
detektiv_tortenelem = [
    {"idezet": "„Ius resistendi (A nemesek joga az ellenállásra)”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Nagy Lajos 1351", "Szent István", "Kollonics"], "info": "A királyi hatalom korlátozása a rendi jogok által."},
    {"idezet": "„Eb ura fakó, József császár nem királyunk!”", "helyes": "1707-es Ónodi országgyűlés (Trónfosztás)", "opciok": ["1707-es Ónodi országgyűlés (Trónfosztás)", "1849", "1526", "1608"], "info": "A Habsburg-ház trónfosztása Rákóczi szabadságharca alatt."}
]
detektiv_matek = [
    {"idezet": "a² = b² + c² - 2bc · cos(α)", "helyes": "Koszinusztétel (Általános háromszögekre)", "opciok": ["Koszinusztétel (Általános háromszögekre)", "Szinusztétel", "Pitagorasz", "Héron-képlet"], "info": "A Pitagorasz-tétel általánosítása tetszőleges háromszögre."},
    {"idezet": "(x^n)' = n · x^(n-1)", "helyes": "Hatványfüggvény deriválási szabálya", "opciok": ["Hatványfüggvény deriválási szabálya", "Exponenciális függvény", "Integrálás", "Másodfokú formula"], "info": "A differenciálszámítás alapvető szabálya."}
]

# -------------------------------------------------------------
# ÁLLAPOTKEZELÉS ÉS SEGÉDFÜGGVÉNYEK
# -------------------------------------------------------------
if 'xp' not in st.session_state: st.session_state.xp = 180
if 'level' not in st.session_state: st.session_state.level = 2
if 'streak' not in st.session_state: st.session_state.streak = 4
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Szia! Én vagyok a felkészítő mentorod. Kérdezz bátran!"}]

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

# -------------------------------------------------------------
# OLDALSÁV & TANTÁRGY VÁLASZTÓ
# -------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox(
    "Válassz tantárgyat:",
    ["📖 Magyar Irodalom (22 tétel)", "🔤 Magyar Nyelvtan (16 tétel)", "🏛️ Történelem (30 tétel)", "📐 Matematika (16 témakör)"]
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

# Adatbázisok kiosztása
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
