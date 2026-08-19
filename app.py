import io
import os
import streamlit as st
from fpdf import FPDF
from google import genai
from gtts import gTTS

st.set_page_config(
    page_title="Irodalom Érettségi Platform - Edited by Nagy Attila",
    page_icon="✨",
    layout="wide"
)

# Háttérben tárolt kulcs automatikus betöltése
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Astra AI prémium sötét téma és vizuális elemek
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    .stat-badge {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        margin-right: 8px;
    }
    .topic-card {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .oral-box {
        background-color: #1e1b4b;
        border-left: 4px solid #818cf8;
        padding: 18px;
        border-radius: 8px;
        margin-top: 15px;
        line-height: 1.6;
    }
    .deep-text {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 24px;
        border-radius: 12px;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    .flashcard {
        background: linear-gradient(135deg, #1e1b4b, #31104b);
        border: 2px solid #818cf8;
        border-radius: 16px;
        padding: 35px;
        text-align: center;
        margin: 20px 0;
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .audio-card {
        background-color: #182234;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .chat-user {
        background-color: #4f46e5;
        color: white;
        padding: 12px 18px;
        border-radius: 16px 16px 4px 16px;
        margin-bottom: 12px;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-ai {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        padding: 12px 18px;
        border-radius: 16px 16px 16px 4px;
        margin-bottom: 12px;
        max-width: 80%;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 11 Mély, tankönyvi szintű érettségi tétel
tetelek = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, a nagykőrösi és margitszigeti balladaköltészet mélyelemzése",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja", "A walesi bárdok", "Híd-avatás"],
        "audio_szoveg": """
Arany János a magyar irodalom történetének legnagyobb balladaírója. A ballada műfaját Greguss Ágost esztéta nyomán tragédia dalban elbeszélveként szoktuk meghatározni, ami arra utal, hogy a líra, az epika és a dráma műnemi jegyei egyszerre jelennek meg benne. A művek sűrített feszültségét az úgynevezett balladai homály, a kihagyásos szerkesztésmód és a gyors idősíkváltás teremti meg. 
Arany balladaművészete két meghatározó alkotói korszakra bontható. Az első az 1850-es évek nagykőrösi időszaka. A szabadságharc leverését követő Bach-korszak elnyomásában a költő történelmi allegóriákkal ébresztette a nemzet lelkiismeretét. A walesi bárdok és a Szondi két apródja a zsarnoksággal szembeni megalkuvást nem ismerő hűség örök emlékművei. Ugyanebben az időszakban születtek meg a lélektani balladák is: az Ágnes asszonyban a bűn letörölhetetlensége miatti tébolyt, a Tetemre hívásban pedig az istenítélet drámai mechanizmusát mutatja be. 
A második nagy korszak az 1877-es margitszigeti Őszikék ideje. A Kapcsos könyvbe írt kései művekben, például a Híd-avatásban, már a felgyorsult, modern nagyváros elidegenedése, a társadalmi felelőtlenség és az öngyilkosok tragikus haláltánca áll a középpontban.
        """,
        "vazlat": """
### I. A műfaj elméleti és esztétikai meghatározása
- **A három műnem találkozása:** Líra (dalforma, dallam, rímek), Epika (cselekmény, elbeszélő), Dráma (tragikus konfliktus, dialógusok).
- **Formanyelvi sajátosságok:**
  - *Balladai homály:* Az elbeszélő szándékosan homályban hagy részleteket; az olvasó képzeletére bízza az összefüggéseket.
  - *Ellipszis (kihagyás):* Az átvezetések elhagyása, ami gyorsítja a cselekmény ritmusát.
  - *Refrén:* Érzelmi nyomatékosítás és feszültségteremtés (*„Könyörülj, Jézus, a sok szegény bűnösön!”*).

---

### II. A nagykőrösi korszak (1850-es évek)
- **Történelmi-allegorikus balladák:**
  - *A walesi bárdok (1857):* Ferenc József látogatása ellen írt morális kiáltvány; az 500 bárd halála a szellemi függetlenség és a nemzeti hűség örök szimbóluma.
  - *Szondi két apródja (1856):* Kétszólamú szerkesztés; a hős Szondi dicsérete felesel Ali pasa szolgájának csábító ígéreteivel.
- **Lélektani balladák:**
  - *Ágnes asszony (1853):* A bűntudat és az elmezavar folyamata; a patakban mosott véres lepedő a letörölhetetlen bűn szimbóluma.

---

### III. Az Őszikék korszaka (1877, Margitsziget)
- **Híd-avatás:** Modern haláltánc (*danse macabre*); a nagyvárosi elidegenedés és céltalanság elől a halálba menekülő társadalmi rétegek bemutatása.
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (40 mp):** Greguss Ágost műfaji meghatározása, a 3 műnem szintézise, formai jegyek (homály, ellipszis, sűrítés).
2. **Nagykőrös (70 mp):** Történelmi ellenállás (*A walesi bárdok*, *Szondi két apródja*) és lélektani bűntudat (*Ágnes asszony* lepedőmosása).
3. **Őszikék (40 mp):** 1877, Margitsziget, Kapcsos könyv. A *Híd-avatás* nagyvárosi haláltánca.
4. **Befejezés (30 mp):** A klasszikus magyar ballada csúcspontjának összegzése.
        """,
        "kviz": [
            {"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A líra, epika és dráma ötvözésére utal."},
            {"k": "A walesi bárdok nyíltan, burkolás nélkül támadta Ferenc Józsefet.", "v": False, "m": "Allegorikus formában, a walesi monda köntösében fogalmazta meg az ellenállást."},
            {"k": "Az Ágnes asszony lepedőmosása a bűn letörölhetetlenségének lélektani szimbóluma.", "v": True, "m": "A kényszeres mosás a megbomló elme belső drámája."}
        ]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "A romantika és realizmus szintézise, a polgári meghasonlás és a Senki szigete utópiája",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi", "Ali Csorbadzsi", "Krisztyán Tódor", "Balaton"],
        "audio_szoveg": """
Jókai Mór 1872-ben megjelent regénye, Az arany ember az író legérettebb és legszemélyesebb alkotása. Bár az elbeszélésmód hordozza a romantika gazdag mesemondását és nagy léptékű fordulatait, a társadalmi környezetrajz és a főhős lélektani vívódása már a realizmus mélységeit idézi. 
A cselekmény fókuszában Timár Mihály áll, a zseniális polgári vállalkozó, akinek minden anyagi vállalkozását siker koronázza, magánéletében és lelkiismeretében mégis mélyen boldogtalan. A mű központi konfliktusa egy kettős világmodellre épül fel. Az egyik oldalon a rideg polgári társadalom áll, a komáromi és bécsi kapitalista világ a hálából feleségül vett Timeával, akinek szoborszerű hidegsége fojtogató. A másik pólust a Senki szigete jelenti: a pénz és államhatalom nélküli természeti paradicsom Noémi őszinte, természetes szerelmével. 
Timár belső hasadtsága addig nem oldódhat fel, amíg a civilizációhoz köti a neve és vagyona. A véletlen szerencse és Krisztyán Tódor halála teremti meg a lehetőséget a teljes újjászületésre.
        """,
        "vazlat": """
### I. Műfaj és stílusszintézis
- 1872-es megjelenés; a romantikus mesei fordulatok és a pontos realista társadalomrajz találkozása.

### II. Timár Mihály belső hasadtsága
- Külső siker és gazdagság vs. belső bűntudat (a török kincs megtartása és a Timeával kötött boldogtalan érdekházasság).

### III. Kettős világmodell
- **Komárom/Bécs:** Pénz, spekuláció, hideg pompa, látszatboldogság (*Timea* szoborszerű hálája).
- **Senki szigete:** Pénzmentes, romlatlan természeti utópia, őszinte szerelem (*Noémi*).
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** 1872, Jókai legérettebb alkotása, romantika és realizmus ötvöződése.
2. **Timár alakja (1 perc):** Anyagi felemelkedés vs. morális válság.
3. **Két világ és két nő (1 perc):** Timea ridegsége vs. Noémi és a Senki szigete természeti idillje.
4. **Befejezés (30 mp):** A társadalomból való kilépés tanulsága.
        """,
        "kviz": [
            {"k": "Timea szerelemből házasodott össze Timárral.", "v": False, "m": "Timea pusztán hálából kötött vele házasságot."},
            {"k": "A Senki szigete pénzmentes, önellátó természeti menedék.", "v": True, "m": "A civilizáció törvényein kívül álló romantikus édenkert."}
        ]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény műfaja, eszmék harca és az emberi küzdelem dialektikája a történelemben",
        "kulcsszavak": ["Drámai költemény", "15 szín", "Ádám, Éva, Lucifer", "Párizs", "London", "Küzdj és bízva bízzál"],
        "audio_szoveg": """
Madách Imre remekműve, Az ember tragédiája 1859 és 1860 között, a Bach-korszak legmélyebb nemzeti és személyes válságában született. A műfaja drámai költemény, azaz világdráma, amely a goethei Faust és a bibliai hagyományok nyomán az emberi lét alapvető filozófiai kérdéseit feszegeti: van-e célja a történelemnek, szabad-e az ember akarata, és érdemes-e küzdeni az eszmékért. 
A mű tizenöt színből épül fel. A transzcendens keretszínekben Lucifer és a Teremtő vitája nyitja meg a cselekményt. A közbülső tizenegy történelmi színben Lucifer álmot bocsát Ádámra, végigvezetve őt az emberiség történetének korszakain az ókori Egyiptomtól a Föld kihűlését mutató eszkimó színig. Ádám minden történelmi színben egy-egy magasztos eszméért lelkesedik, ám Lucifer hideg rációja leleplezi az eszmék elkorcsosulását. 
A dráma egyetlen olyan színe, amelyből Ádám hittel és elszántsággal ébred fel, a francia forradalmat bemutató párizsi szín. A mű végén Éva anyasága és a Teremtő zárszava helyreállítja a reményt: a küzdelem maga az emberi létezés értelme.
        """,
        "vazlat": """
### I. Műfaj és filozófia
- Drámai költemény (világdráma) – filozófiai kérdések dialógusos formában, hegel-i dialektikával.

### II. A három archetípus
- **Ádám:** A hit és az eszmékért küzdő emberi szellem.
- **Lucifer:** A hideg ráció, a tagadás és kétely szelleme.
- **Éva:** Az érzelmek, a természetesség és az élet folytonossága.

### III. A 15 szín íve
- Párizs (Danton forradalma: *egyetlen szín, amiből Ádám hittel ébred*).
- London (szabad piac, haláltánc a sírnál).
- 15. szín zárszava: *„Mondottam, ember: küzdj és bízva bízzál!”*
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Drámai költemény fogalma, 1859–60-as válság.
2. **Karakterek hármassága (1 perc):** Ádám, Lucifer és Éva szerepe.
3. **Történelmi színek (1 perc):** Párizs hite és London haláltánca.
4. **Befejezés (30 mp):** A 15. szín: Éva anyasága és az Úr parancsa.
        """,
        "kviz": [
            {"k": "Az ember tragédiája 15 színből áll.", "v": True, "m": "4 keretszín és 11 történelmi szín alkotja."},
            {"k": "Ádám a párizsi színből kiábrándultan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel tér magához."}
        ]
    }
}

# Flashcard adatbázis
flashcards_adat = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra (dalforma, rím), epika (cselekmény) és dráma (konfliktus, dialógus) műnemi sajátosságait."},
    {"q": "Mi a balladai homály és az ellipszis lényege?", "a": "Az elbeszélő szándékosan kihagy részleteket és összefüggéseket, ezáltal feszültséget teremt és a befogadó képzeletére bízza a történet kiegészítését."},
    {"q": "Melyik történelmi esemény ihlette Arany 'A walesi bárdok' című balladáját?", "a": "Ferenc József 1857-es magyarországi látogatása. Arany a költői meg nem alkuvás és a zsarnokellenes hűség példájaként írta meg."},
    {"q": "Mit szimbolizál az Ágnes asszonyban a véres lepedő kényszeres mosása?", "a": "A bűn letörölhetetlenségét és a lelkiismeret-furdalás által kiváltott elmezavart."},
    {"q": "Mi a kettős világmodell 'Az arany ember' című regényben?", "a": "Komárom/Bécs (a pénz, a spekuláció és a rideg polgári társadalom világa Timeával) vs. Senki szigete (a pénzmentes, romlatlan természeti utópia Noémivel)."},
    {"q": "Miért különleges a párizsi szín 'Az ember tragédiájában'?", "a": "Ez az egyetlen olyan történelmi szín, amelyből Ádám nem csalódottan és kiábrándultan, hanem hittel és cselekvési vággyal ébred fel."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a legfontosabb irodalmi szerkesztője?", "a": "1908. január 1-jén indult, és Osvát Ernő volt a lap legendás ízlésű irodalmi szerkesztője."},
    {"q": "Mit jelképez a disznófejű Nagyúr Ady Endre költészetében?", "a": "A pénz, az anyagi kiszolgáltatottság és az emberi méltóságot elnyomó tőke kegyetlen bálványát."},
    {"q": "Mi a központi szállóige és tanulság Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.” – Az értelmiségi ember és a művész morális felelősségvállalása a gonosszal szemben."}
]

stilusiranyzatok = {
    "Realizmus (19. sz. közepe)": """
### Realizmus (19. század dereka)
- **Központi esztétikai cél:** A valóság sallangmentes, tárgyilagos, hiteles és tipikus ábrázolása.
- **Módszertan:** Tipikus jellemek tipikus körülmények között; társadalmi determináció.
- **Képviselők:** Honoré de Balzac, Lev Tolsztoj, Mikszáth Kálmán, Jókai Mór.
    """,
    "Naturalizmus (19. sz. vége)": """
### Naturalizmus (19. század vége)
- **Központi esztétikai cél:** A valóság fotószerű, kíméletlen rögzítése, tabutémák beemelése.
- **Módszertan:** Biológiai determinizmus – az ember az ösztönök és gének rabja.
- **Képviselők:** Émile Zola, Móricz Zsigmond (*Tragédia*, *Barbárok*).
    """,
    "Impresszionizmus (19. sz. vége – 20. sz. eleje)": """
### Impresszionizmus (19–20. század fordulója)
- **Központi esztétikai cél:** A pillanatnyi benyomások, hangulatok és fények megragadása.
- **Stílusjegyek:** Névszói stílus, zeneiség, szinesztéziák.
- **Képviselők:** Kosztolányi Dezső, Tóth Árpád, Juhász Gyula.
    """,
    "Szimbolizmus (19. sz. vége – 20. sz. eleje)": """
### Szimbolizmus (19–20. század fordulója)
- **Központi esztétikai cél:** A látható világ mögötti transzcendens igazságok kifejezése szimbólumokkal.
- **Stílusjegyek:** Rejtélyesség, mítoszteremtés, mély zeneiség.
- **Képviselők:** Charles Baudelaire, Ady Endre, Vajda János.
    """
}

# Állapotkezelés
if 'xp' not in st.session_state:
    st.session_state.xp = 180
if 'level' not in st.session_state:
    st.session_state.level = 2
if 'streak' not in st.session_state:
    st.session_state.streak = 4
if 'card_idx' not in st.session_state:
    st.session_state.card_idx = 0
if 'card_flipped' not in st.session_state:
    st.session_state.card_flipped = False
if 'oral_history' not in st.session_state:
    st.session_state.oral_history = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "text": "Szia! Én vagyok az érettségi mentorod. Kérdezz bátran bármelyik tételről, versről vagy szerzőről!"}
    ]

# PDF Segédfüggvény
def tiszta_pdf_szoveg(szoveg):
    cserel = {
        'ő': 'o', 'Ő': 'O', 'ű': 'u', 'Ű': 'U', 'á': 'a', 'Á': 'A',
        'é': 'e', 'É': 'E', 'í': 'i', 'Í': 'I', 'ó': 'o', 'Ó': 'O',
        'ö': 'o', 'Ö': 'O', 'ú': 'u', 'Ú': 'U', 'ü': 'u', 'Ü': 'U',
        '„': '"', '”': '"', '’': "'", '–': '-'
    }
    for k, v in cserel.items():
        szoveg = szoveg.replace(k, v)
    return szoveg.encode('latin-1', 'replace').decode('latin-1')

def letoltheto_pdf_generalas(tetelek_adat):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_x(15)
    pdf.cell(180, 8, 'Magyar Irodalom Erettsegi Tetelvazlatok', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    for cim, adat in tetelek_adat.items():
        pdf.set_font('Helvetica', 'B', 10.5)
        pdf.set_x(15)
        fejlec = tiszta_pdf_szoveg(f"{cim} - {adat['alcim']}")
        pdf.multi_cell(180, 5.5, fejlec, align='L')
        pdf.ln(1)
        
        pdf.set_font('Helvetica', '', 8.5)
        tiszta_vazlat = adat['vazlat'].replace('###', '').replace('**', '').replace('*', '')
        for sor in tiszta_vazlat.strip().split('\n'):
            sor_tiszta = tiszta_pdf_szoveg(sor.strip())
            if sor_tiszta:
                pdf.set_x(15)
                pdf.multi_cell(180, 4.2, sor_tiszta, align='L')
        pdf.ln(3)
        
    return bytes(pdf.output())

# AI hívás segédfüggvény
def ai_generalas(prompt_text):
    api_k = get_api_key()
    if not api_k:
        return "⚠️ Nincs beállítva a Secrets-ben a GEMINI_API_KEY kulcs!"
    try:
        client = genai.Client(api_key=api_k)
        modellek = ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
        for m in modellek:
            try:
                res = client.models.generate_content(model=m, contents=prompt_text)
                if res and res.text:
                    return res.text
            except Exception:
                continue
        return "Nem sikerült választ kapni a Gemini modelltől."
    except Exception as e:
        return f"Hiba az API hívás során: {e}"

# Felső fejlécek & Gamifikáció
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("✨ Edited by Nagy Attila")
    st.caption("Astra AI Irodalom Érettségi Platform & Tréningközpont")
with col_h2:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 10px;'>
        <span class='stat-badge'>🔥 {st.session_state.streak} napos széria</span>
        <span class='stat-badge'>⚡ {st.session_state.xp} XP</span>
        <span class='stat-badge'>🏆 Szint {st.session_state.level}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Oldalsáv navigáció
st.sidebar.markdown("<h2 style='color:#818cf8;'>Navigáció</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz funkciót:",
    [
        "📖 Tételek & Vázlatok",
        "🎴 Villámkártyák (Flashcards)",
        "🎙️ Szóbeli Érettségi Szimulátor",
        "✍️ Esszé & Elemzés Értékelő",
        "🎧 Hangoskönyv (Monológ)",
        "🎨 Stílusirányzatok",
        "🏆 Nagy Próbavizsga",
        "🤖 AI Érettségi Mentor"
    ]
)

# PDF Letöltés
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Letölthető anyag")
if st.sidebar.button("📄 PDF Puska elkészítése"):
    pdf_bytes = letoltheto_pdf_generalas(tetelek)
    st.sidebar.download_button(
        label="⬇️ Letöltés indítása",
        data=pdf_bytes,
        file_name="Irodalom_Erettsegi_Puska.pdf",
        mime="application/pdf"
    )

# 1. Menüpont: Tételek & Vázlatok
if menupont == "📖 Tételek & Vázlatok":
    kivalasztott_tetel = st.selectbox("Válassz tételt:", list(tetelek.keys()))
    adat = tetelek[kivalasztott_tetel]
    
    st.markdown(f"""
    <div class='topic-card'>
        <h2 style='color:#818cf8; margin:0;'>{kivalasztott_tetel}</h2>
        <p style='color:#94a3b8; margin:4px 0 12px 0;'>🎯 {adat['alcim']}</p>
        <div>
            {' '.join([f"<span style='background:#374151; padding:4px 10px; border-radius:12px; font-size:0.85rem; margin-right:6px;'>#{k}</span>" for k in adat['kulcsszavak']])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes tankönyvi elemzés", "🎙️ 3 perces szóbeli feleletvázlat", "⚡ Gyors teszt"])
    
    with tab1:
        st.markdown("<div class='deep-text'>", unsafe_allow_html=True)
        st.markdown(adat["vazlat"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='oral-box'>", unsafe_allow_html=True)
        st.markdown(adat["szobeli"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab3:
        st.subheader("Ellenőrizd a tudásod ebből a tételből!")
        for i, q in enumerate(adat["kviz"]):
            st.write(f"**{i+1}. {q['k']}**")
            c1, c2 = st.columns([1, 1])
            valasz = None
            if c1.button("✅ Igaz", key=f"t_{kivalasztott_tetel}_{i}"):
                valasz = True
            if c2.button("❌ Hamis", key=f"f_{kivalasztott_tetel}_{i}"):
                valasz = False
                
            if valasz is not None:
                if valasz == q["v"]:
                    st.session_state.xp += 15
                    st.success(f"Helyes válasz! (+15 XP) 🎉 {q['m']}")
                else:
                    st.error(f"Helytelen! ❌ Magyarázat: {q['m']}")
            st.markdown("---")

# 2. Menüpont: Villámkártyák (Flashcards)
elif menupont == "🎴 Villámkártyák (Flashcards)":
    st.title("🎴 Érettségi Villámkártyák (Astra Flashcards)")
    st.caption("Pörgesd át a legfontosabb fogalmakat, évszámokat és összefüggéseket!")
    
    aktualis_kartya = flashcards_adat[st.session_state.card_idx]
    
    st.progress((st.session_state.card_idx + 1) / len(flashcards_adat))
    st.write(f"Kártya: {st.session_state.card_idx + 1} / {len(flashcards_adat)}")
    
    if not st.session_state.card_flipped:
        st.markdown(f"<div class='flashcard'>❓ {aktualis_kartya['q']}</div>", unsafe_allow_html=True)
        if st.button("🔄 Kártya megfordítása (Válasz megtekintése)", use_container_width=True):
            st.session_state.card_flipped = True
            st.rerun()
    else:
        st.markdown(f"<div class='flashcard' style='background:linear-gradient(135deg, #064e3b, #065f46); border-color:#34d399;'>💡 {aktualis_kartya['a']}</div>", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("✅ Tudtam (+10 XP)", use_container_width=True):
            st.session_state.xp += 10
            st.session_state.card_flipped = False
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(flashcards_adat)
            st.rerun()
        if col_b2.button("❌ Ismételni kell", use_container_width=True):
            st.session_state.card_flipped = False
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(flashcards_adat)
            st.rerun()

# 3. Menüpont: Szóbeli Érettségi Szimulátor
elif menupont == "🎙️ Szóbeli Érettségi Szimulátor":
    st.title("🎙️ Szóbeli Érettségi Szimulátor (Mock Exam)")
    st.caption("Gyakorold a szóbeli feleletet! Az AI vizsgaelnökként automatikusan meghallgat, belekérdez és leosztályoz.")
    
    valasztott_szim_tetel = st.selectbox("Válassz tételt a próbavizsgához:", list(tetelek.keys()))
    
    if st.button("🏁 Új szóbeli felelet indítása"):
        st.session_state.oral_history = [
            {"role": "ai", "text": f"Jó napot kívánok! Húzza ki a tételét... Az Ön tétele: **{valasztott_szim_tetel}**. Kérem, kezdje meg a feleletét a bevezetéssel és a legfontosabb műfaji, formai sajátosságokkal!"}
        ]
        st.rerun()
        
    for msg in st.session_state.oral_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑‍🎓 <strong>Ön feleli:</strong><br>{msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>👨‍🏫 <strong>Vizsgaelnök (AI):</strong><br>{msg['text']}</div>", unsafe_allow_html=True)
            
    with st.form("oral_form", clear_on_submit=True):
        felelet_reszlet = st.text_area("Mondd el / írd be a feleleted következő részét:")
        kuld_felelet = st.form_submit_button("Felelet beküldése")
        
        if kuld_felelet and felelet_reszlet:
            st.session_state.oral_history.append({"role": "user", "text": felelet_reszlet})
            prompt = f"""
            Magyar irodalom szóbeli érettségi elnök vagy. A diák a(z) '{valasztott_szim_tetel}' tételből felel.
            A diák eddigi válasza: '{felelet_reszlet}'.
            Feladatod:
            1. Röviden értékeld az elmondottakat (pontosság, fogalmak).
            2. Tegyél fel egy célzott, érettségi szintű kérdést a tétel egy másik fontos részletére vonatkozóan, vagy ha a felelet végére ért, adj egy konkrét érdemjegyet (1-5) és szöveges záróértékelést.
            Legyél támogató, de szakmailag pontos tanár!
            """
            ai_valasz = ai_generalas(prompt)
            st.session_state.oral_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 30
            st.rerun()

# 4. Menüpont: Esszé & Elemzés Értékelő
elif menupont == "✍️ Esszé & Elemzés Értékelő":
    st.title("✍️ Esszé & Műelemzés Értékelő Labor")
    st.caption("Másold be az írásbeli fogalmazásodat vagy verselemzés-tervezetedet, és az AI azonnal pontozza az érettségi szempontrendszer szerint!")
    
    diak_essze = st.text_area("Másold be a fogalmazásodat (műelemzés, összehasonlító elemzés vagy esszé):", height=220)
    
    if st.button("📊 Esszé automatikus ellenőrzése és pontozása"):
        if diak_essze:
            with st.spinner("Az esszé elemzése érettségi szempontok alapján..."):
                prompt = f"""
                Magyar nyelv és irodalom érettségi javító tanár vagy. Értékeld az alábbi diákfogalmazást:
                ---
                {diak_essze}
                ---
                Kérlek, az alábbi szempontok szerint strukturáld az értékelést:
                1. **Tartalmi minőség & Szakmai pontosság (max 40 pont):** Irodalomtörténeti tények, fogalmak helyes használata.
                2. **Szerkezet & Logikai felépítés (max 20 pont):** Bevezetés, tárgyalás, befejezés, logikus átvezetések.
                3. **Nyelvhelyesség & Stílus (max 20 pont):** Választékos szókincs, helyesírás.
                4. **Összesített érettségi pontszám & Érdemjegy (1-5)**
                5. **Konkrét javítási javaslatok:** 2-3 pontban, mit kell hozzátenni a maximális pontszámhoz.
                """
                valasz = ai_generalas(prompt)
                st.markdown("<div class='deep-text'>", unsafe_allow_html=True)
                st.markdown(valasz)
                st.markdown("</div>", unsafe_allow_html=True)
                st.session_state.xp += 50
        else:
            st.info("Kérlek előbb másold be a fogalmazás szövegét a fenti mezőbe!")

# 5. Menüpont: Hangoskönyv
elif menupont == "🎧 Hangoskönyv (Monológ)":
    st.title("🎧 Hangoskönyv Érettségi Felkészítő")
    st.caption("Hallgasd meg a tételek teljes, 1.5–2 perces összefüggő szóbeli elemzését!")
    
    kivalasztott_hangos = st.selectbox("Válassz meghallgatandó tételt:", list(tetelek.keys()), key="audio_select")
    adat_hangos = tetelek[kivalasztott_hangos]
    
    st.markdown(f"""
    <div class='audio-card'>
        <h3 style='color:#60a5fa; margin-top:0;'>🎙️ {kivalasztott_hangos}</h3>
        <p style='color:#cbd5e1;'><strong>Fókusz:</strong> {adat_hangos['alcim']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
        if st.button(f"▶️ Hangos monológ elindítása ({kivalasztott_hangos})"):
            with st.spinner("Hangfájl generálása tiszta magyar kiejtéssel..."):
                tts = gTTS(text=adat_hangos["audio_szoveg"].strip(), lang='hu', slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
                st.session_state.xp += 25
                st.success("Jó tanulást és hallgatást! (+25 XP) 🎧")
                
    with st.expander("📖 A monológ teljes szövege (olvasáshoz és követéshez)", expanded=True):
        st.write(adat_hangos["audio_szoveg"].strip())

# 6. Menüpont: Stílusirányzatok
elif menupont == "🎨 Stílusirányzatok":
    st.title("Kulcs Stílusirányzatok Mélyelemzése")
    for nev, leiras in stilusiranyzatok.items():
        with st.expander(f"📌 {nev}", expanded=True):
            st.markdown(leiras)

# 7. Menüpont: Nagy Próbavizsga
elif menupont == "🏆 Nagy Próbavizsga":
    st.title("Teljes Érettségi Próbavizsga")
    st.write("Válaszold meg az összes tételkérdést a tudásszinted ellenőrzéséhez!")
    
    osszes_kerdes = []
    for t_nev, t_adat in tetelek.items():
        for q in t_adat["kviz"]:
            osszes_kerdes.append((t_nev, q))
            
    valaszok = {}
    with st.form("nagy_vizsga_form"):
        for idx, (t_nev, q) in enumerate(osszes_kerdes):
            st.markdown(f"**{idx+1}. [{t_nev}]**")
            st.write(q["k"])
            valaszok[idx] = st.radio(
                "Választásod:",
                ["Nem válaszoltam", "Igaz", "Hamis"],
                key=f"probavizsga_{idx}",
                horizontal=True
            )
            st.markdown("---")
            
        bekuldve = st.form_submit_button("🏁 Eredmények kiértékelése")
        
    if bekuldve:
        pont = 0
        for idx, (t_nev, q) in enumerate(osszes_kerdes):
            v = valaszok[idx]
            if v != "Nem válaszoltam":
                if (v == "Igaz") == q["v"]:
                    pont += 1
                    
        szazalek = int((pont / len(osszes_kerdes)) * 100)
        st.metric("Elért vizsgaeredmény", f"{pont} / {len(osszes_kerdes)} pont", f"{szazalek}%")
        
        if szazalek >= 85:
            st.balloons()
            st.session_state.xp += 100
            st.success("🏆 Értékelés: Jeles (5) – Kiváló felkészültség! (+100 XP)")
        elif szazalek >= 70:
            st.info("👍 Értékelés: Jó (4) – Szép munka!")
        elif szazalek >= 50:
            st.warning("👌 Értékelés: Közepes (3) – A lényeg megvan.")
        elif szazalek >= 40:
            st.warning("⚠️ Értékelés: Elégséges (2) – Érdemes még átnézni a vázlatokat!")
        else:
            st.error("❌ Értékelés: Elégtelen (1) – Ismételd át a tételeket!")

# 8. Menüpont: AI Érettségi Mentor Chat
elif menupont == "🤖 AI Érettségi Mentor":
    st.title("🤖 AI Érettségi Mentor")
    st.caption("Kérdezz bármilyen irodalmi műről, versről vagy szerzőről!")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑‍🎓 {msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 {msg['text']}</div>", unsafe_allow_html=True)

    with st.form("mentor_chat_form", clear_on_submit=True):
        felh_kerdes = st.text_input("Írd be a kérdésed:")
        kuld = st.form_submit_button("Küldés")
        
        if kuld and felh_kerdes:
            st.session_state.chat_history.append({"role": "user", "text": felh_kerdes})
            prompt = f"Magyar irodalom szakos érettségi felkészítő tanár vagy. Válaszolj tömören, lényegretörően egy 18 éves diák kérdésére: {felh_kerdes}"
            ai_valasz = ai_generalas(prompt)
            st.session_state.chat_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 10
            st.rerun()
