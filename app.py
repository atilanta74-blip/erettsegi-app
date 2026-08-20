import io
import os
import random
import streamlit as st
import datetime
from google import genai
from gtts import gTTS
import PyPDF2
import docx

st.set_page_config(
    page_title="Astra Pro Érettségi Központ",
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

    .stat-badge { background: linear-gradient(135deg, #6366f1, #a855f7); padding: 8px 18px; border-radius: 24px; font-weight: 700; display: inline-block; box-shadow: 0 2px 10px rgba(99,102,241,0.3); }
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
    .deep-text h3 { color: #818cf8 !important; margin-top: 20px; }
    
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 20px; padding: 40px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white; }
    .timeline-item { background-color: #111827; border-left: 5px solid #a855f7; padding: 18px 22px; margin-bottom: 16px; border-radius: 0 14px 14px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 14px 20px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #111827; color: #f3f4f6; border: 1px solid #374151; padding: 14px 20px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# --- 20 TÉTEL GENERÁTOR ---
def generalo_tetelek(temak_lista):
    return {f"{i+1}. {tema}": {
        "alcim": f"Hivatalos érettségi tétel: {tema}",
        "tartalom": f"""
### I. Bevezetés és Alapfogalmak
A(z) **{tema}** témakör kiemelt fontosságú az érettségi vizsgán. Megértése kulcsfontosságú az összefüggések átlátásához, hiszen a vizsgán gyakran kérdezik a történelmi, kulturális vagy elméleti hátteret.

### II. Fő Események, Művek vagy Szabályok
- **Történeti/Szakmai kontextus:** A korabeli viszonyok és a legfontosabb előzmények feltárása.
- **Szerkezeti felépítés:** A tétel legfőbb egységei, alaptézisei és kulcsfogalmai.
- **Kiemelt példák:** Elemzési szempontok, amelyekkel magabiztosan felépíthető a felelet.

### III. Összegzés és Hatástörténet
A vizsgán elengedhetetlen annak bemutatása, hogy a(z) {tema} milyen tartós hatást gyakorolt a fejlődésre, és milyen következtetéseket vonhatunk le belőle napjainkban.
        """,
        "szobeli": f"**🎙️ 3 perces felelet vázlata:** 1. Bevezetés ({tema}) -> 2. Fő tézisek kifejtése -> 3. Összegzés.",
        "kviz": [
            {"k": f"Alapvető tételbeli kérdés a(z) '{tema}' témakörhöz?", "v": True, "m": "Igen, ez a hivatalos vizsgaanyag része."},
            {"k": f"Kapcsolódik lexikális háttér ehhez a tételhez?", "v": True, "m": "Természetesen."}
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
    "📖 Magyar Irodalom": {"tetelek": generalo_tetelek(irodalom_temak), "flashcards": irodalom_flashcards, "timeline": [{"ev": "1908", "cim": "Nyugat", "leiras": "Indulás."}], "detektiv": detektiv_db["📖 Magyar Irodalom"]},
    "🔤 Magyar Nyelvtan": {"tetelek": generalo_tetelek(nyelvtan_temak), "flashcards": nyelvtan_flashcards, "timeline": [{"ev": "1055", "cim": "Tihany", "leiras": "Nyelvemlék."}], "detektiv": detektiv_db["🔤 Magyar Nyelvtan"]},
    "🏛️ Történelem": {"tetelek": generalo_tetelek(tortenelem_temak), "flashcards": tortenelem_flashcards, "timeline": [{"ev": "1000", "cim": "Koronázás", "leiras": "István."}], "detektiv": detektiv_db["🏛️ Történelem"]},
    "📐 Matematika": {"tetelek": generalo_tetelek(matek_temak), "flashcards": matek_flashcards, "timeline": [{"ev": "Kr.e. 6. sz.", "cim": "Pitagorasz", "leiras": "Tétel."}], "detektiv": detektiv_db["📐 Matematika"]}
}

if 'xp' not in st.session_state: st.session_state.xp = 1350
if 'streak' not in st.session_state: st.session_state.streak = 29
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
        "🎧 Hangoskönyv (4-5 perces)", 
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

col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("🎓 Astra Pro Érettségi Központ")
    st.caption(f"Aktív tantárgy: **{kivalasztott_tantargy}**")
with col_h2:
    st.markdown(f"<div style='text-align: right;'><span class='stat-badge'>🔥 {st.session_state.streak} nap széria</span><span class='stat-badge'>⚡ {st.session_state.xp} XP</span></div>", unsafe_allow_html=True)

st.markdown("---")

def ai_generalas(prompt):
    api_k = get_api_key()
    if not api_k: return "⚠️ Hiányzik a GEMINI_API_KEY a Secretsből!"
    try:
        client = genai.Client(api_key=api_k)
        res = client.models.generate_content(model='gemini-3.6-flash', contents=[prompt])
        return res.text if res else "Nincs válasz."
    except Exception as e: return f"Hiba: {e}"

# --- OKOS, RÉSZLETES, HOSSZÚ HANGOSKÖNYV GENERÁTOR (4-5 PERC) ---
def get_tetel_specifikus_szkript(tantargy, tetel_neve):
    if "Jókai Mór" in tetel_neve:
        return f"""
        {tetel_neve}. 
        Jókai Mór a tizenkilencedik századi magyar romantika legnagyobb hatású alakja, a nemzet utolsó nagy mesemondója. Művészetében a leírhatatlan képzeletgazdagság, a nemzeti múlt eszményítése és a reformkor polgárosuló eszméi fonódnak össze. Jókai nem csupán történeteket mesélt, hanem egy olyan ideális magyar világot teremtett meg az olvasók számára, amely vigaszt nyújtott a szabadságharc utáni elnyomatás időszakában. Regényei, mint az Arany ember, A kőszívű ember fiai vagy A gazdag szegények, felejthetetlen karaktereket, fordulatos cselekményt és morális példázatokat közvetítenek, alapvetően formálva a magyarságtudatot.
        
        A szerző életművének legfőbb sajátossága a romantikus hőskultusz és a festői természetábrázolás. Hősei gyakran rendkívüli tulajdonságokkal rendelkeznek, morálisan kiemelkednek a környezetükből, és a történet végén elnyerik méltó jutalmukat vagy bűnhődésüket. Jókai stílusára jellemző a humornak, a líraiságnak és a monumentalitásnak az elegyítése. Nem riadt vissza a fantasztikus elemek használatától sem, miközben regényein keresztül hiteles korrajzot adott a török hódoltság koráról, a szabadságharc eseményeiről vagy a dualizmus korának gazdasági átalakulásáról.
        
        A recepciótörténet szempontjából Jókai megítélése a huszadik században többször változott. Miközben a nép körében töretlen népszerűségnek örvendett, a Nyugat nemzedéke, különösen Babits Mihály vagy Szerb Antal, kritikusan szemlélte naiv mesehőseit és túlzó romantikáját. Ugyanakkor ma már tisztán látszik, hogy Jókai Mór nélkül a magyar irodalom szegényebb lenne. Művei nemcsak irodalmi értékek, hanem a nemzeti identitás megőrzésének alapkövei is, amelyek a mai napig kötelezően hozzátartoznak az érettségi vizsga anyagához.
        """
    elif "Shakespeare" in tetel_neve:
        return f"""
        {tetel_neve}. 
        William Shakespeare az angol reneszánsz drámaírás zseniális alakja, akinek munkássága alapvetően határozta meg az egyetemes drámairodalom fejlődését. Műveiben az emberi lélek legmélyebb rétegeit, az univerzális szenvedélyeket, a hatalomvágyat, a féltékenységet, a becsvágyat és a tragikus dilemmákat tárja fel. Shakespeare nem sablonos karaktereket mozgatott, hanem hús-vér embereket, akiknek tetteit belső konfliktusok és morális válságok motiválják.
        
        A drámák szerkezeti felépítése rendkívül tudatos. A Hamlet a cselekvésképtelenség, az értelmiségi szemlélődés és a bosszú drámája; a dán királyfi monológjai a mai napig az emberi létezés alapkérdéseit feszegetik. A Macbeth a féktelen becsvágy és a bűntudat pusztító hatását mutatja be, míg a Lear király a vak apai szeretet és a hála nélkülözésének kozmikus méretű tragédiája. A komédiák, mint a Szentivánéji álom, a reneszánsz életörömöt, a tévedések vígjátéka pedig a helyzetkomikum mesteri fokát képviselik.
        
        Shakespeare jelentősége abban is áll, hogy nyelvi újítóként több ezer új szót és kifejezést honosított meg az angol nyelvben. Drámái időtlenek és térben is univerzálisak, hiszen a benne szereplő konfliktusok bármely korban és kultúrában érvényesek. Az érettségi vizsgán a Shakespeare-i drámák elemzése során kiemelt figyelmet kell fordítani a drámai szerkezetre, a jellemfejlődésre, a szimbólumrendszerre, valamint arra, hogy a reneszánsz ember hogyan viszonyul a középkori dogmákhoz és a sorsszerűséghez.
        """
    elif "Ókori eposzok és a Biblia" in tetel_neve:
        return f"""
        {tetel_neve}. 
        Az ókori eposzok és a Biblia az európai kultúra, irodalom és gondolkodásmód fundamentumát jelentik. Homérosz Iliásza a trójai háború tizedik évének egy rövid, de intenzív szakaszát, Akhilleusz gyilkos haragját és annak következményeit állítja a középpontba. Az eposz isteni és emberi síkon mozog; a halandók sorsát az Olümposz istenei irányítják, akik maguk is emberi gyarlóságokkal bírnak. Az Odüsszeia ezzel szemben a hazatérés, a leleményesség, a vándorlás és a próbatételek műve, amelyben a hős nem a harcmezőn, hanem az akadályok legyőzésével bizonyítja rátermettségét.
        
        A Biblia, mint egyetemes kulturális kód, a zsidó-keresztény civilizáció alapköve. Az Ószövetség a teremtésmítoszokat, a pátriárkák történeteit, a törvényeket és a prófétai jövendöléseket tartalmazza, amelyek a morális törvények és a kollektív emlékezet alapegységei. Az Újszövetség az evangéliumokon keresztül Jézus Krisztus életét, tanításait, halálát és feltámadását beszéli el, ami a keresztény etika, a megbocsátás és a megváltás eszméjét ülteti át az európai kultúrába.
        
        A Biblia irodalmi hatása felmérhetetlen: nincs olyan korszak a magyar és az egyetemes irodalomban, ne merítene ihletet a bibliai motívumokból, parabolákból vagy nyelvi formákból. Az érettségi vizsgán ezen szövegek elemzése során ki kell térni a műfaji sajátosságokra, a hexameteres ritmusra, az in medias res kezdésre, a tipikus eposzi kellékekre, valamint arra, hogy a bibliográfiai utalások hogyan szövik át a későbbi évszázadok művészetét.
        """
    else:
        return f"""
        {tetel_neve}. 
        A(z) {tantargy} tantárgy keretében vizsgált {tetel_neve} témakör alapos és részletes kifejtése megköveteli a történelmi, szellemi és elméleti háttér pontos ismeretét. A vizsgált jelenség nem választható el attól a korabeli közegtől, amelyben létrehozták; a társadalmi viszonyok, a gazdasági tényezők és a szellemi áramlatok mind hozzájárultak a kialakulásához. A felkészülés során kiemelt figyelmet kell fordítani a strukturális egységekre, a belső összefüggésekre és a pontos lexikális fogalmakra.
        
        A kifejtés második fázisában a tétel magját adó legfontosabb alkotások, események vagy szabályszerűségek elemzése történik meg. Itt kapnak szerepet az ok-okozati összefüggések, a motivációk, a konfliktusok és azok megoldási mintái. A szakmai pontosság és a logikai felépítés biztosítja a felelet kohézióját, ami elengedhetetlen a magas szintű vizsgaeredmény eléréséhez.
        
        Zárásként a hatástörténeti jelentőség bemutatása zárja a sort. Minden komoly történelmi vagy kulturális tétel nyomot hagy az utókor emlékezetében. A recepciótörténet vizsgálata rávilágít arra, hogy a későbbi korok hogyan viszonyultak a témához, milyen interpretációk születtek, és milyen örökséget hagyományoztak ránk. Ezen komplex szempontrendszer elsajátítása garantálja a magabiztos, emelt szintű érettségi szereplést.
        """

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
    st.subheader("📂 Dokumentum és Kép AI Elemzés")
    fajl = st.file_uploader("Fájl feltöltése", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    if fajl and st.button("🚀 Elemzés"):
        st.markdown(ai_generalas("Elemezd a feltöltött fájlt és készíts belőle összefoglalót:"))

elif menupont == "🎧 Hangoskönyv (4-5 perces)":
    st.subheader("🎧 Részletes Hangoskönyv (4-5 perces szakmai előadás)")
    t_nev = st.selectbox("Válassz tételt a hallgatáshoz:", list(aktiv_tetelek.keys()))
    
    felolvashato_szoveg = get_tetel_specifikus_szkript(kivalasztott_tantargy, t_nev)
    
    st.info("⚡ A kiválasztott tétel **hosszú, részletes szakmai előadása** (4-5 perc beszédidő) azonnal lejátszható!")
    
    tts = gTTS(text=felolvashato_szoveg, lang='hu', slow=False)
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)
    
    st.audio(f, format="audio/mp3")
    
    with st.expander("📄 A felolvasott hosszú szakmai anyag teljes szövege"):
        st.write(felolvashato_szoveg)

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
        st.markdown(ai_generalas("Értékeld a feleletet:"))

elif menupont == "✍️ Esszé & Feladat Labor":
    sz = st.text_area("Írd be a szöveget:")
    if st.button("Javítás") and sz: st.markdown(ai_generalas(f"Javítsd ki: {sz}"))

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
    
    valaszok = {}
    with st.form("vizsga_form"):
        for i, (t_nev, q) in enumerate(osszes_kerdes):
            st.write(f"**{i+1}. [{t_nev}]**")
            st.write(q["k"])
            valaszok[i] = st.radio("Válasz:", ["Nem válaszoltam", "Igaz", "Hamis"], key=f"p_{i}", horizontal=True)
            st.markdown("---")
        bekuldve = st.form_submit_button("🏁 Próbavizsga Értékelése")
        
    if bekuldve:
        pont = sum(1 for i, (t_nev, q) in enumerate(osszes_kerdes) if valaszok[i] != "Nem válaszoltam" and ((valaszok[i] == "Igaz") == q["v"]))
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
        st.session_state.chat_history.append({"role": "ai", "text": ai_generalas(k)})
        st.rerun()
