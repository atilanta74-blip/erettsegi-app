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

# --- 20 HIVATALOS TÉTEL LISTÁK ---
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
    "📖 Magyar Irodalom": {"temak": irodalom_temak, "flashcards": irodalom_flashcards, "timeline": [{"ev": "1908", "cim": "Nyugat", "leiras": "Indulás."}], "detektiv": detektiv_db["📖 Magyar Irodalom"]},
    "🔤 Magyar Nyelvtan": {"temak": nyelvtan_temak, "flashcards": nyelvtan_flashcards, "timeline": [{"ev": "1055", "cim": "Tihany", "leiras": "Nyelvemlék."}], "detektiv": detektiv_db["🔤 Magyar Nyelvtan"]},
    "🏛️ Történelem": {"temak": tortenelem_temak, "flashcards": tortenelem_flashcards, "timeline": [{"ev": "1000", "cim": "Koronázás", "leiras": "István."}], "detektiv": detektiv_db["🏛️ Történelem"]},
    "📐 Matematika": {"temak": matek_temak, "flashcards": matek_flashcards, "timeline": [{"ev": "Kr.e. 6. sz.", "cim": "Pitagorasz", "leiras": "Tétel."}], "detektiv": detektiv_db["📐 Matematika"]}
}

if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'detektiv_index' not in st.session_state: st.session_state.detektiv_index = 0
if 'tananyag_cache' not in st.session_state: st.session_state.tananyag_cache = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = [{"role": "ai", "text": "Üdvözöllek! Miben segíthetek a felkészülésben?"}]

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
aktiv_temak = tantargy_adat["temak"]
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

# --- MODULOK ---
if menupont == "📚 Tételek & Vázlatok (20 db)":
    tetel_nev = st.selectbox("Válassz a 20 hivatalos tétel közül:", aktiv_temak)
    
    # Egyedi cache kulcs a tételhez
    cache_key = f"{kivalasztott_tantargy}_{tetel_nev}"
    
    if cache_key not in st.session_state.tananyag_cache:
        with st.spinner("🤖 Az AI jelenleg dolgozza ki részletesen ezt a tételt..."):
            prompt = f"""
            Írj egy rendkívül részletes, mélyreható, professzionális, érettségire felkészítő tananyagot a következő tételvázlat alapján:
            Tantárgy: {kivalasztott_tantargy}
            Tétel neve: {tetel_nev}
            
            A tananyag tartalmazza:
            1. Részletes bevezetés, alapfogalmak és történelmi/szakmai háttér.
            2. Fő rész: lépésről lépésre kifejtett események, művek, definíciók, képletek vagy szabályok részletes elemzése alfejezetekre bontva.
            3. Példák, gyakorlati alkalmazások vagy szemléltető részletek.
            4. Összegzés és jelentőség a mai kor emberének / a vizsgázónak.
            Használj tiszta, jól olvasható Markdown formázást (címek, felsorolások, kiemelések)!
            """
            st.session_state.tananyag_cache[cache_key] = ai_generalas_tartalom([prompt])

    tananyag_szoveg = st.session_state.tananyag_cache[cache_key]
    
    st.markdown(f"<div class='topic-card'><h2>{tetel_nev}</h2><p style='color:#a5b4fc;'>Hivatalos érettségi tétel részletes kidolgozása</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes Tananyag", "🎙️ 3 Perces Felelet Vázlat", "⚡ Interaktív Kvíz"])
    with tab1:
        st.markdown(f"<div class='deep-text'>{tananyag_szoveg}</div>", unsafe_allow_html=True)
    with tab2:
        vázlat_prompt = f"Készíts egy tömör, logikus, 3 perces szóbeli felelet vázlatot a(z) '{tetel_nev}' ({kivalasztott_tantargy}) témához, pontokba szedve."
        if f"valat_{cache_key}" not in st.session_state:
            st.session_state[f"valat_{cache_key}"] = ai_generalas_tartalom([vázlat_prompt])
        st.markdown(f"<div class='oral-box'>{st.session_state[f'valat_{cache_key}']}</div>", unsafe_allow_html=True)
    with tab3:
        kviz_prompt = f"Készíts 2 db feleletválasztós kvízkérdést a(z) '{tetel_nev}' tételkörhöz. Add vissza KIZÁRÓLAG érvényes JSON formátumban: [{{'k': 'Kérdés?', 'v': true, 'm': 'Magyarázat.'}}]"
        if f"kviz_{cache_key}" not in st.session_state:
            res_json = ai_generalas_tartalom([kviz_prompt])
            try:
                cleaned = res_json.replace("```json", "").replace("```", "").strip()
                st.session_state[f"kviz_{cache_key}"] = json.loads(cleaned)
            except:
                st.session_state[f"kviz_{cache_key}"] = [{"k": f"Alapvető kérdés a(z) {tetel_nev} témához?", "v": True, "m": "Igen."}]
        
        for i, q in enumerate(st.session_state[f"kviz_{cache_key}"]):
            st.write(f"**{i+1}. {q['k']}**")
            c1, c2 = st.columns(2)
            if c1.button("✅ Igaz", key=f"t_{cache_key}_{i}"): st.success(f"Helyes! {q['m']}")
            if c2.button("❌ Hamis", key=f"f_{cache_key}_{i}"): st.error(f"Nem helyes. {q['m']}")

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
    t_nev = st.selectbox("Válassz tételt a hallgatáshoz:", aktiv_temak)
    cache_key = f"{kivalasztott_tantargy}_{t_nev}"
    
    if cache_key not in st.session_state.tananyag_cache:
        st.session_state.tananyag_cache[cache_key] = ai_generalas_tartalom([f"Írj részletes tananyagot a(z) {t_nev} ({kivalasztott_tantargy}) témáról."])
    
    felolvashato_szoveg = st.session_state.tananyag_cache[cache_key][:4000] # gTTS limit miatt
    st.info(f"⚡ A(z) **{t_nev}** tétel hanganyaga elkészült és lejátszható:")
    
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
        st.markdown(ai_generalas_tartalom(["Értékeld a hangüzenetben hallható érettségi feleletet."]))

elif menupont == "✍️ Esszé & Feladat Labor":
    sz = st.text_area("Írd be a megírt esszét vagy feladatot:")
    if st.button("Javítás és Értékelés") and sz:
        st.markdown(ai_generalas_tartalom([f"Javítsd ki és értékeld tanárként ezt az érettségi esszét/feladatot: {sz}"]))

elif menupont == "🎭 Detektív Játék (20 db)":
    st.subheader("🎭 Detektív Feladványok")
    idx = st.session_state.detektiv_index % len(aktiv_det)
    f = aktiv_det[idx]
    st.markdown(f"<div class='topic-card' style='text-align:center;'><h3 style='color:#f472b6;'>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válaszd ki a megfejtést:", f['opciok'], index=None, key=f"det_{idx}")
    if st.button("🔍 Ellenőrzés"):
        if tipp == f['helyes']: st.balloons(); st.success("Helyes válasz! 🎉")
        else: st.error(f"Nem találta el. Helyes: {f['helyes']}")
    if st.button("➡️ Következő feladvány"):
        st.session_state.detektiv_index += 1
        st.rerun()

elif menupont == "🧭 Történelmi Idővonal":
    for item in aktiv_time:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"🏆 Interaktív Próbavizsga – {kivalasztott_tantargy}")
    st.info("Kattints a próbavizsga indításához, és az AI generál egy teljes feladatsort.")
    if st.button("🚀 Próbavizsga Generálása"):
        st.markdown(ai_generalas_tartalom([f"Készíts egy 3 kérdéses interaktív próbavizsgát {kivalasztott_tantargy} tantárgyból."]))

elif menupont == "🤖 AI Érettségi Mentor":
    for msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat-{msg['role']}'>{msg['text']}</div>", unsafe_allow_html=True)
    k = st.text_input("Kérdezz a mentortól:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas_tartalom([k])})
        st.rerun()
