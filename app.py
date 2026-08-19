import io
import os
import random
import streamlit as st
from fpdf import FPDF
from google import genai
from gtts import gTTS

st.set_page_config(
    page_title="Érettségi Felkészítő Központ - Edited by Nagy Attila",
    page_icon="🎓",
    layout="wide"
)

# Háttérben tárolt Secrets kulcs automatikus betöltése
def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Astra AI stílusú prémium UI és vizuális elemek
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    
    /* Gombok univerzális stílusa: élénk, kontrasztos, jól látható */
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: 1px solid #818cf8 !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background: linear-gradient(135deg, #6366f1, #9333ea) !important;
        color: #ffffff !important;
        border-color: #a78bfa !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.4) !important;
    }
    
    /* Szövegbeviteli mezők és lenyílók igazítása */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border-color: #4b5563 !important;
    }
    
    .stat-badge {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        margin-right: 8px;
    }
    .subject-pill {
        background: #1e1b4b;
        border: 1px solid #6366f1;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
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
    .timeline-item {
        background-color: #1f2937;
        border-left: 4px solid #a855f7;
        padding: 16px 20px;
        margin-bottom: 15px;
        border-radius: 0 12px 12px 0;
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
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. MAGYAR IRODALOM TÉTELTÁR (11 Tétel)
# -------------------------------------------------------------
tetelek_irodalom = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, nagykőrösi és margitszigeti korszak",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja", "A walesi bárdok"],
        "audio_szoveg": "Arany János a magyar irodalom legnagyobb balladaírója. A műfajt Greguss Ágost nyomán tragédia dalban elbeszélveként határozzuk meg, mert egyesíti a líra, epika és dráma sajátosságait...",
        "vazlat": """
### I. A műfaj elméleti meghatározása
- **Három műnem szintézise:** Lírai forma, epikus cselekmény, drámai konfliktusok és dialógusok.
- **Formai sajátosságok:** Balladai homály, ellipszis (kihagyás), sűrítés, refrén.

### II. Nagykőrösi korszak (1850-es évek)
- **Történelmi-allegorikus balladák:** *A walesi bárdok* (szellemi meg nem alkuvás), *Szondi két apródja* (kétszólamú hűségének).
- **Lélektani balladák:** *Ágnes asszony* (a bűntudat és megbomló elme drámája, lepedőmosás).

### III. Őszikék korszak (1877, Margitsziget)
- *Híd-avatás:* Nagyvárosi modern haláltánc (*danse macabre*), társadalmi felelősség.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés (Greguss definíció) -> 2. Nagykőrös (Walesi bárdok, Ágnes asszony) -> 3. Őszikék (Híd-avatás) -> 4. Összegzés.",
        "kviz": [
            {"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A három műnem találkozására utal."},
            {"k": "Az Ágnes asszony lepedőmosása a bűn letörölhetetlenségének szimbóluma.", "v": True, "m": "A kényszeres mosás a lelkiismeret-furdalást jelzi."}
        ]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus szintézise, polgári meghasonlás és a Senki szigete",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi", "Ali Csorbadzsi", "Krisztyán Tódor"],
        "audio_szoveg": "Jókai Mór 1872-es Az arany ember című regénye az író legszemélyesebb alkotása, melyben a romantika és realizmus elemei ötvöződnek...",
        "vazlat": """
### I. Műfaj és stílusszintézis
- 1872: Romantikus mesei fordulatok és pontos realista gazdasági leírások.
### II. Timár Mihály meghasonlása
- Anyagi siker vs. belső boldogtalanság (török kincs, érdekházasság).
### III. Kettős világmodell
- Komárom/Bécs (Timea hideg hálája) <-> Senki szigete (Noémi tiszta természeti szerelme).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés (1872, stíluskettősség) -> 2. Timár jelleme -> 3. Két tér és két nőalak -> 4. Zárás (Balatoni sorsfordulat).",
        "kviz": [
            {"k": "Timea szerelemből ment hozzá Timár Mihályhoz.", "v": False, "m": "Pusztán hálából házasodtak össze."},
            {"k": "A Senki szigete pénzmentes, természeti utópia.", "v": True, "m": "A civilizáció törvényein kívül áll."}
        ]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény műfaja, eszmék küzdelme és az Úr zárszava",
        "kulcsszavak": ["Drámai költemény", "15 szín", "Ádám, Éva, Lucifer", "Párizs", "London"],
        "audio_szoveg": "Madách Imre Az ember tragédiája című drámai költeménye 1859-60-ban született, vizsgálva az emberi lét és a történelem végső értelmét...",
        "vazlat": """
### I. Műfaj és filozófia
- Drámai költemény (világdráma) hegel-i dialektikával.
### II. Szereplők
- Ádám (hit és tettvágy), Lucifer (ráció és tagadás), Éva (természetesség és élet).
### III. Történelmi ív (15 szín)
- Párizs (Danton – *egyetlen szín, amiből Ádám hittel ébred*), London (haláltánc).
- 15. szín: *„Mondottam, ember: küzdj és bízva bízzál!”*
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Drámai költemény fogalma -> 2. Szereplők hármassága -> 3. Történelmi színek csomópontjai -> 4. 15. szín katarzisa.",
        "kviz": [
            {"k": "Az ember tragédiája 15 színből áll.", "v": True, "m": "4 keretszín és 11 történelmi szín."},
            {"k": "Ádám a párizsi színből kiábrándultan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből hittel ébred."}
        ]
    },
    "4. Mikszáth Kálmán prózája": {
        "alcim": "Anekdotizmus, A tót atyafiak, A jó palócok és a Beszterce ostroma",
        "kulcsszavak": ["Anekdota", "A tót atyafiak", "A jó palócok", "Beszterce ostroma", "Pongrácz István"],
        "audio_szoveg": "Mikszáth Kálmán a 19. és 20. század fordulójának legnagyobb magyar mesélője, akinek művészete az anekdotára épül...",
        "vazlat": """
### I. Stílusjegyek: Anekdotizmus, szelíd irónia, élőbeszédszerű mesélés.
### II. Novelláskötetek: A tót atyafiak (4 hosszú elbeszélés) vs. A jó palócok (15 rövid novella).
### III. Beszterce ostroma: Pongrácz István Don Quijote-i alakja és a dzsentri világ kritikája.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Két kötet ellentéte -> 3. Beszterce ostroma -> 4. Összegzés.",
        "kviz": [{"k": "Pongrácz István középkori lovagként viselkedik Nedec várában.", "v": True, "m": "Anakronisztikus nemesi figura."}]
    },
    "5. Vajda János költészete": {
        "alcim": "A lírai magány mítosza, a Gina-szerelem és a szimbolizmus előfutára",
        "kulcsszavak": ["Gina-versek", "Montblanc", "A vaáli erdőben", "A virrasztók"],
        "audio_szoveg": "Vajda János a kiegyezés korának legmagányosabb költője, aki a Gina-szerelem és a panteista tájlíra mestere volt...",
        "vazlat": """
### I. Magány és társadalmi kiábrándulás (*A virrasztók*).
### II. Gina-líra: *Húsz év múlva* (Montblanc-metafora: külső jég és belső láva).
### III. Csend-líra: *A vaáli erdőben* (panteista megnyugvás és megbékélés a halállal).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Gina-szerelem (Montblanc) -> 3. Panteizmus (Vaáli erdő) -> 4. Hatása Adyra.",
        "kviz": [{"k": "A Montblanc-metafora a Húsz év múlva című vers központi képe.", "v": True, "m": "A fagyos csúcs és a vulkáni tűz ellentéte."}]
    },
    "6. XIX. századi dráma: Ibsen és Csehov": {
        "alcim": "Az analitikus dráma (Nóra) és a csehovi hangulatdráma (Sirály, Cseresznyéskert)",
        "kulcsszavak": ["Henrik Ibsen", "Analitikus dráma", "Nóra", "Anton Csehov", "Sirály", "Cseresznyéskert"],
        "audio_szoveg": "A 19. század végén Henrik Ibsen analitikus drámája és Anton Csehov hangulatdrámája forradalmasította a színházat...",
        "vazlat": """
### I. Henrik Ibsen: Analitikus technika (a múltbeli titkok lelepleződése); *Nóra* női önállósodása.
### II. Anton Csehov: Hangulatdráma; cselekvésképtelenség, párhuzamos monológok (*Sirály*, *Cseresznyéskert*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Polgári dráma válsága -> 2. Ibsen analitikája -> 3. Csehov atmoszférája -> 4. Modern színházi hatás.",
        "kviz": [{"k": "Ibsen darabjaiban a múltbeli titkok kiderülése robbantja ki a válságot.", "v": True, "m": "Ez az analitikus szerkesztés alapja."}]
    },
    "7. A Nyugat folyóirat": {
        "alcim": "A modern magyar irodalom indulása 1908-ban, szerkesztők és a 3 nemzedék",
        "kulcsszavak": ["1908", "Osvát Ernő", "Ignotus", "Mikes-emlékérem", "Három nemzedék"],
        "audio_szoveg": "1908. január 1-jén indult a Nyugat folyóirat, amely a magyar kultúra legfontosabb irodalmi műhelyévé vált...",
        "vazlat": """
### I. Indulás: 1908–1941; Mikes-emlékérem, művészi autonómia (*l'art pour l'art*).
### II. Szerkesztők: Ignotus (főszerkesztő), Osvát Ernő (irodalmi válogató zseni), Hatvany Lajos.
### III. Nemzedékek: 1. nemzedék (Ady, Babits, Kosztolányi, Móricz), 2. nemzedék (Szabó Lőrinc), 3. nemzedék (Radnóti).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1908 jelentősége -> 2. Osvát Ernő szerepe -> 3. Három nemzedék -> 4. Örökség.",
        "kviz": [{"k": "A Nyugat folyóirat 1908 és 1941 között működött.", "v": True, "m": "Babits haláláig állt fenn."}]
    },
    "8. Ady Endre költészete": {
        "alcim": "Szimbolizmus, magyarságtudat, lírai párharc és háborús apokalipszis",
        "kulcsszavak": ["Új versek 1906", "A magyar Ugaron", "Léda vs. Csinszka", "Harc a Nagyúrral"],
        "audio_szoveg": "Ady Endre 1906-os Új versek című kötetével megteremtette a modern magyar szimbolista költészetet...",
        "vazlat": """
### I. 1906: Új versek kötetkompozíciója, ars poetica (*Góg és Magóg fia vagyok én...*).
### II. Témák: Magyarság-versek (*A magyar Ugaron*), Pénz-versek (*Harc a Nagyúrral*), Szerelem (Léda párharc vs. Csinszka menedék).
### III. Háborús versek: *Ember az embertelenségben*.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1906 forradalma -> 2. Ugar és Nagyúr toposz -> 3. Léda és Csinszka -> 4. Háborús humánum.",
        "kviz": [{"k": "Ady korszakalkotó kötete az Új versek 1906-ban jelent meg.", "v": True, "m": "Ez nyitotta a modern magyar költészetet."}]
    },
    "9. Babits Mihály: Jónás könyve": {
        "alcim": "A prófétai szerep, a morális felelősségvállalás és a Jónás imája",
        "kulcsszavak": ["Jónás könyve", "Jónás imája", "Ninive", "Cinkos, aki néma", "1938"],
        "audio_szoveg": "Babits Mihály 1938-ban írta meg a Jónás könyvét a gégerákja és a fasizmus fenyegetése idején...",
        "vazlat": """
### I. 1938: Babits betegsége és a fasizmus előretörése; bibliai parafrázis groteszk elemekkel.
### II. Jónás útja: Menekülés -> Cethal (megtisztulás) -> Ninive intése -> Kegyelem diadala.
### III. Alaptétel: *„Mert vétkesek közt cinkos, aki néma.”* és a záró *Jónás imája*.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1938 kontextusa -> 2. Jónás esendősége és beavatása -> 3. Morális parancs -> 4. Jónás imája.",
        "kviz": [{"k": "A Jónás könyve központi szállóigéje: 'Mert vétkesek közt cinkos, aki néma'.", "v": True, "m": "Az értelmiségi felelősség imperatívusza."}]
    },
    "10. Móricz Zsigmond prózája": {
        "alcim": "A paraszti és dzsentri világ naturalista és kritikai ábrázolása (Tragédia, Barbárok, Úri muri)",
        "kulcsszavak": ["Naturalizmus", "Tragédia", "Barbárok", "Úri muri", "Szakhmáry Zoltán"],
        "audio_szoveg": "Móricz Zsigmond szakított a hamis népi idillel, és a valóságot a maga kíméletlen ösztönvilágában mutatta be...",
        "vazlat": """
### I. Stílusreform: Naturalizmus, biológiai és társadalmi determináció.
### II. Novellák: *Tragédia* (Kis János evésbe torkolló lázadása), *Barbárok* (pusztai kapzsiság és gyilkosság).
### III. Dzsentri válság: *Úri muri* (Szakhmáry Zoltán önpusztítása).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szakítás a népiességgel -> 2. Kis János és a Barbárok -> 3. Úri muri csődje -> 4. Összegzés.",
        "kviz": [{"k": "A Tragédia című novellában Kis János a lakodalmi evésbe pusztul bele.", "v": True, "m": "A zsíros hús jelenti vesztét."}]
    },
    "11. Kosztolányi Dezső: Édes Anna": {
        "alcim": "A lélektani regény, a megalázottság tudattalan robbanása és a humanizmus",
        "kulcsszavak": ["Édes Anna", "Vizy család", "Moviszter doktor", "1919", "Freudizmus"],
        "audio_szoveg": "Kosztolányi Dezső 1926-os Édes Anna című regénye az elfojtott sérelmek tudattalan kitörésének lélektani remekműve...",
        "vazlat": """
### I. Történelmi keret: 1919 nyara; Sigmund Freud pszichoanalízisének hatása.
### II. Anna dehumanizálása: Mintagépként kezelik, Jancsi úrfi elcsábítja és eldobja -> Kettős gyilkosság.
### III. Moviszter doktor: A tiszta részvét és emberi méltóság hangja.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1919 és a freudizmus -> 2. Anna tárgyiasítása -> 3. A gyilkosság lélektana -> 4. Moviszter üzenete.",
        "kviz": [{"k": "Moviszter doktor az egyetlen, aki emberi részvéttel tekint Annára.", "v": True, "m": "Ő képviseli a szerző humanista értékrendjét."}]
    }
}

# -------------------------------------------------------------
# 2. MAGYAR NYELVTAN TÉTELTÁR (8 Teljes Tétel)
# -------------------------------------------------------------
tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, kommunikációs funkciók",
        "kulcsszavak": ["Adó és Vevő", "Kód és Csatorna", "Jakobson modellje", "Metakommunikáció", "Zaj"],
        "audio_szoveg": "A kommunikáció információk, gondolatok és érzelmek átadása valamilyen jelrendszer segítségével. Jakobson klasszikus modellje szerint a folyamat alapvető tényezői az adó, a vevő, az üzenet, a kód, a csatorna és a valóságos kontextus...",
        "vazlat": """
### I. A kommunikációs folyamat tényezői (Jakobson-modell)
- **Adó (beszélő/feladó):** Aki az üzenetet kódolja és elindítja.
- **Vevő (címzett):** Aki az üzenetet felfogja és dekódolja.
- **Üzenet:** Maga a továbbított információ.
- **Kód:** A közös jelrendszer (pl. a magyar nyelv).
- **Csatorna:** A fizikai közeg, amin az információ áramlik (hanghullám, papír, digitális hálózat).
- **Kontextus (beszédhelyzet):** A valóságnak az a része, amire az üzenet utal.
- **Zaj:** Minden olyan tényező, ami akadályozza a megértést (pl. háttérzaj, félreértés).

### II. A nyelv funkciói
- *Tájékoztató (referenciális):* Ismeretátadás.
- *Érzelemkifejező (emotív):* A beszélő érzéseinek tükrözése.
- *Felhívó (konatív):* A vevő cselekvésre késztetése.
- *Kapcsolattartó (fatikus):* Kapcsolat felvétele és fenntartása (*„Halló!”, „Szép napot!”*).
- *Értelmező (metanyelvi):* Magáról a nyelvről való beszéd (*„Hogy érted ezt?”*).
- *Gyönyörködtető (poétikai):* Az esztétikai hatás megteremtése.

### III. Nem nyelvi (nonverbális) jelek
- Testbeszéd (gesztusok, mimika, testtartás), térközszabályozás (*proxemika*), vokális jelek (hangerő, intonáció, beszédtempó).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kommunikáció definíciója -> 2. A modell 6 alaptényezője (Jakobson) -> 3. Nyelvi funkciók bemutatása -> 4. Nonverbális jelek szerepe a mindennapi érintkezésben.",
        "kviz": [
            {"k": "A fatikus funkció célja a kapcsolatfelvétel és kapcsolattartás.", "v": True, "m": "Például a köszönések és bejelentkezések tartoznak ide."},
            {"k": "A nem nyelvi jelekhez tartozik a mimika és a térközszabályozás is.", "v": True, "m": "A nonverbális kommunikáció alapvető részei."}
        ]
    },
    "2. A szövegtan alapjai és a szövegtípusok": {
        "alcim": "A szöveg fogalma, kohéziós erői, szerkezeti egységei és típusai",
        "kulcsszavak": ["Globális kohézió", "Lokális kohézió", "Anafora és Katafora", "Elbeszélő, leíró, érvelő"],
        "audio_szoveg": "A szöveg a nyelv legmagasabb szintű, lezárt, kerek egysége, amely egy adott kommunikációs helyzetben keletkezik...",
        "vazlat": """
### I. A szöveg fogalma és kohéziója
- **Szöveg:** A nyelv és a beszéd legnagyobb, önálló, lezárt és egész egysége.
- **Grammatikai kohézió (Lokális):**
  - Kötőszók, névmási utalások (*anafora* = visszautalás, *katafora* = előreutalás), egyeztetések.
- **Jelentéstani kohézió (Globális):**
  - Témamegtartás, kulcsszavak hálózata, szinonimák, hiperonímiák (fölérendelt fogalmak).

### II. A szöveg szerkezete
- Cím $\rightarrow$ Bevezetés $\rightarrow$ Tárgyalás (bekezdések logikai íve) $\rightarrow$ Befejezés / Konklúzió.

### III. Szövegtípusok felosztása
- *Funkció szerint:* Elbeszélő, leíró, érvelő, magyarázó.
- *Kommunikációs színtér szerint:* Hétköznapi, publicisztikai, hivatalos, tudományos, szépirodalmi.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szöveg fogalma -> 2. Lokális és globális kohéziós erők -> 3. Szerkezeti hármasság -> 4. Főbb szövegtípusok.",
        "kviz": [
            {"k": "Az anafora a szövegben előre mutató névmási utalást jelent.", "v": False, "m": "Az anafora visszautalás, az előreutalás a katafora."},
            {"k": "A szöveg a nyelv legmagasabb szintű, önálló egysége.", "v": True, "m": "A mondatok feletti strukturált szint."}
        ]
    },
    "3. A magyar helyesírás alapelvei": {
        "alcim": "A 4 alapelv rendszere és alkalmazásuk a gyakorlatban",
        "kulcsszavak": ["Kiejtés elve", "Szóelemzés elve", "Hagyomány elve", "Egyszerűsítés elve", "Mássalhangzótörvények"],
        "audio_szoveg": "A magyar helyesírás rendszere négy alapelvre épül: a kiejtés, a szóelemzés, a hagyomány és az egyszerűsítés elvére...",
        "vazlat": """
### I. A 4 helyesírási alapelv

1. **A kiejtés (fonetikus) elve:**
   - Úgy írjuk a szót, ahogy ejtjük (pl. *asztal, ember, szép*).
2. **A szóelemzés (etimologikus) elve:**
   - Összetett és toldalékos szavaknál a szótövet és a toldalékot eredeti alakjukban rögzítjük, figyelmen kívül hagyva a kiejtésbeli mássalhangzótörvényeket (pl. *látja* [láttya], *barátság* [baraccság], *színpad* [szímpad]).
3. **A hagyomány elve:**
   - Történelmi családnevek és régies írásmódok megőrzése (pl. *Kossuth, Széchenyi, Weöres, ly betűs szavak: folyó, király*).
4. **Az egyszerűsítés elve:**
   - Hosszú kétjegyű mássalhangzók kettőzésekor csak az első jegyet kettőzzük (pl. *asszony, mennyi, loccsan*).
   - Három azonos mássalhangzó találkozásakor összevonjuk (pl. *tollal*, de összetételnél kötőjelezzük: *sakk-kör*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés (A helyesírás szerepe) -> 2. Kiejtés és szóelemzés elve -> 3. Hagyomány és egyszerűsítés elve -> 4. Kivételek és példák.",
        "kviz": [
            {"k": "A 'látja' szó leírása a szóelemzés elvét követi a kiejtett [láttya] hangzás ellenére.", "v": True, "m": "A szótő (lát) és toldalék (ja) tiszta marad."},
            {"k": "A családnevek írásakor a kiejtés elve mindig felülírja a hagyomány elvét.", "v": False, "m": "A történelmi családneveknél a hagyomány elve érvényesül (pl. Kossuth)."}
        ]
    },
    "4. Szófajok és mondatrészek rendszere": {
        "alcim": "Alapszófajok, viszonyszók, mondatrészi szerepek és mondattani elemzés",
        "kulcsszavak": ["Ige, Névszó, Igenév", "Névelő, Névutó, Kötőszó", "Alany, Állítmány, Tárgy, Határozó, Jelző"],
        "audio_szoveg": "A szófajok a szavak alaktani, mondattani és jelentéstani tulajdonságai alapján kialakított kategóriák...",
        "vazlat": """
### I. A szófaji rendszer felosztása
- **Alapszófajok:** Önálló jelentéssel bírnak, mondatrészek lehetnek.
  - *Ige* (cselekvés, történés, létezés).
  - *Névszók* (főnév, melléknév, számnév, névmás).
  - *Igenevek* (főnévi, melléknévi, határozói igenév).
  - *Határozószók* (itt, most, holnap).
- **Viszonyszók:** Nincs önálló mondatrészi szerepük, viszonyt fejeznek ki (névelő, névutó, kötőszó, igekötő, segédige).
- **Mondatszók:** Érzelmet, indulatot fejeznek ki (indulatszók, módosítószók: *igen, nem, talán, jaj*).

### II. Mondatrészek rendszere
- **Predikatív viszony:** Állítmány és Alany kapcsolata (a mondat magja).
- **Bővítmények:**
  - *Tárgy* (Kit? Mit?).
  - *Határozók* (Hely-, idő-, mód-, ok-, cél-, eszközhatározó stb.).
  - *Jelzők* (Minőség-, mennyiség-, birtokos, értelmező jelző).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szófajok hármas felosztása -> 2. Alapszófajok és viszonyszók -> 3. Mondatrészek rendszere -> 4. Szintaktikai elemzés.",
        "kviz": [
            {"k": "A névelők és kötőszók az alapszófajok csoportjába tartoznak.", "v": False, "m": "A viszonyszókhoz tartoznak, nincs önálló mondatrészi szerepük."}]
    },
    "5. Retorika és érvelési technikák": {
        "alcim": "A szónoki beszéd szerkezete, érvtípusok és vitatechnikák",
        "kulcsszavak": ["Érv szerkezete (Tétel, Bizonyíték, Összekötés)", "Szónoki beszéd részei", "Dedukció és Indukció"],
        "audio_szoveg": "A retorika az ékesszólás és meggyőzés tudománya. Az érvelés legkisebb egysége a hármas felépítésű érv...",
        "vazlat": """
### I. Az érv felépítése (Toulmin-modell)
1. **Tétel:** Az állítás, amit el akarunk fogadtatni.
2. **Bizonyíték (Adat):** A tényt alátámasztó példa, statisztika, hivatkozás.
3. **Összekötő elem:** A tétel és bizonyíték közötti logikai kapocs.

### II. Főbb érvtípusok
- *Meghatározásból levezetett érv* (definíció).
- *Ok-okozati érv* (a következmények bemutatása).
- *Tekintélyre hivatkozó érv* (szakértő, tudós idézése).
- *Analógián (hasonlóságon) alapuló érv*.

### III. A klasszikus szónoki beszéd szerkezete
1. Bevezetés (*Exordium*) -> 2. Elbeszélés (*Narratio*) -> 3. Részletezés (*Divisio*) -> 4. Bizonyítás (*Confirmatio*) -> 5. Cáfolás (*Refutatio*) -> 6. Befejezés (*Peroratio*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Retorika célja -> 2. Érv 3 szerkezeti eleme -> 3. Érvtípusok -> 4. A szónoki beszéd 6 lépése.",
        "kviz": [{"k": "A szónoki beszéd klasszikus felépítésében a cáfolás (refutatio) megelőzi a befejezést.", "v": True, "m": "A bizonyítás után a cáfolat következik."}]
    },
    "6. Stilisztika: Alakzatok és trópusok": {
        "alcim": "Költői képek (metafora, metonímia, szinesztézia) és szövegalakzatok",
        "kulcsszavak": ["Metafora, Metonímia, Szinekdoché", "Szinesztézia, Hasonlat", "Anafora, Párhuzam, Ellentét"],
        "audio_szoveg": "A stilisztika a nyelvi kifejezőeszközöket vizsgálja. Két fő csoportra osztjuk őket: a szóképekre és a szövegalakzatokra...",
        "vazlat": """
### I. Képi kifejezőeszközök (Trópusok / Szóképek)
- **Metafora:** Két fogalom azonosítása külső vagy belső hasonlóság alapján (pl. *„rabok legyünk vagy szabadok”*).
- **Metonímia:** Névátvitel térbeli, időbeli vagy anyagbeli érintkezés alapján (pl. *„alszik a ház”*, *„aranyat ér a szava”*).
- **Szinekdoché:** Rész-egész felcserélése (pl. *„lélek sem járt ott”*).
- **Szinesztézia:** Különböző érzékelési területek összekapcsolása (pl. *„sötét csend”*, *„lila dal”*).
- **Megszemélyesítés:** Élettelen dolgok felruházása emberi tulajdonságokkal.

### II. Alakzatok (Szövegformáló eszközök)
- *Ismétlések:* Anafora (sor eleji ismétlés), refrén.
- *Gondolati alakzatok:* Párhuzam (*paralelizmus*), ellentét (*antitézis*), túlzás (*hiperbola*), fokozás (*klimax*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trópusok fogalma -> 2. Metafora és metonímia különbsége -> 3. Szinesztézia és megszemélyesítés -> 4. Szövegalakzatok.",
        "kviz": [{"k": "A 'sötét csend' kifejezés a szinesztézia példája.", "v": True, "m": "A látás és hallás érzetét kapcsolja össze."}]
    },
    "7. A szókészlet rétegződése és változása": {
        "alcim": "Társadalmi és területi nyelvváltozatok, szleng, argó, neologizmusok és archaizmusok",
        "kulcsszavak": ["Köznyelv és Irodalmi nyelv", "Nyelvjárások (Dialektusok)", "Szleng és Szaknyelv", "Archaizmus és Neologizmus"],
        "audio_szoveg": "A magyar szókészlet folyamatosan változó, rétegzett rendszer, amely területi és társadalmi tagolódást mutat...",
        "vazlat": """
### I. Vízszintes (Területi) rétegződés: Nyelvjárások
- Regionális tájnyelvek (palóc, alföldi, dunántúli, északkeleti, székely stb.) tájszavakkal és egyedi hangkészlettel.

### II. Függőleges (Társadalmi) rétegződés: Szociolektusok
- **Szaknyelvek:** Pontos szakkifejezések (*terminológia*).
- **Rétegnyelvek:** Diáknyelv, hobbinyelvek.
- **Szleng és Argó:** Gyorsan változó, közvetlen, csoportkohéziót erősítő kifejezéskészlet.

### III. A szókészlet időbeli változása
- *Archaizmusok:* Elavult, kikopott szavak (pl. *delej, atyafi*).
- *Neologizmusok:* Újonnan született szavak (pl. *okostelefon, lájkol*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Területi nyelvjárások -> 2. Társadalmi rétegnyelvek (szleng, szaknyelv) -> 3. Szókincs időbeli mozgása (új és régi szavak).",
        "kviz": [{"k": "Az archaizmusok az újonnan született szavakat jelentik a nyelvben.", "v": False, "m": "Az archaizmusok a régies, elavult szavak."}]
    },
    "8. A magyar nyelv története és a nyelvújítás": {
        "alcim": "A finnugor rokonság, a nyelvújítás korszaka és Kazinczy Ferenc szerepe",
        "kulcsszavak": ["Uráli / Finnugor nyelvcsalád", "Halotti Beszéd (1195)", "Nyelvújítás (1790-1820)", "Kazinczy Ferenc", "Neológusok és Ortológusok"],
        "audio_szoveg": "A magyar nyelv az uráli nyelvcsalád finnugor ágába tartozik. Írásbeliségünk legrégebbi emléke a Halotti Beszéd és Könyörgés...",
        "vazlat": """
### I. Eredet és korai nyelvemlékek
- **Rokonság:** Uráli nyelvcsalád, finnugor ág (alapszókincs és ragozó/*agglutináló* jelleg azonossága).
- **Legfontosabb nyelvemlékek:**
  - *Tihanyi apátság alapítólevele (1055):* Szórványemlék.
  - *Halotti Beszéd és Könyörgés (1195 körül):* Első összefüggő szövegemlék.
  - *Ómagyar Mária-siralom (1300 körül):* Első magyar nyelvű vers.

### II. A Nyelvújítás korszaka (kb. 1790–1820)
- **Cél:** A magyar nyelv alkalmassá tétele a tudományok, művészetek és államigazgatás művelésére.
- **Vezéralakja:** Kazinczy Ferenc (Széphalom).
- **Viták:** Neológusok (újítók) vs. Ortológusok (hagyományőrzők) $\rightarrow$ *Tövisek és virágok*, *Mondolat*.
- **Szóalkotási módok:** Szóösszetétel, szóképzés, szóelvonás (*kapál $\rightarrow$ kapa*), szócsonkítás, szóösszerántás (*cső + orr $\rightarrow$ csőr*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Finnugor rokonság -> 2. Legkorábbi nyelvemlékek -> 3. Nyelvújítás célja és Kazinczy szerepe -> 4. Szóalkotási módok.",
        "kviz": [
            {"k": "A Halotti Beszéd és Könyörgés a legrégebbi fennmaradt összefüggő magyar szövegemlék.", "v": True, "m": "1195 körül keletkezett a Pray-kódexben."},
            {"k": "A nyelvújítási harcban Kazinczy Ferenc az ortológus hagyományőrzők vezére volt.", "v": False, "m": "Kazinczy a neológus újítók vezéralakja volt."}
        ]
    }
}

# -------------------------------------------------------------
# 3. IDÉZET-DETEKTÍV JÁTÉK ADATBÁZISA
# -------------------------------------------------------------
idezet_adatbazis = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma. / Fölkeltem én hát; megbánva a rest / lapulást...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Ember az embertelenségben", "Arany János: Szondi két apródja", "Radnóti Miklós: Nem tudhatom"], "info": "A morális felelősségvállalás központi parancsa 1938-ból."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb, / Mit kény és kedv szerint lök / A sors előbb-tovább.”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János: Toldi", "Ady Endre: Góg és Magóg fia vagyok én"], "info": "Petőfi forradalmi költészetének kiemelkedő felhívó verse."},
    {"idezet": "„Csillagok, csillagok, mondjátok el nekem: / Merre van, hol lakik az én bús szerelmem?”", "helyes": "Vajda János: Gina-versek", "opciok": ["Vajda János: Gina-versek", "Juhász Gyula: Milyen volt...", "Tóth Árpád: Körúti hajnal", "Kosztolányi Dezső: Boldog, szomorú dal"], "info": "Vajda kései szerelmi lírájának magányos hangulatképe."},
    {"idezet": "„Góg és Magóg fia vagyok én, / Hiába döngetek kaput, falat / S mégis megkérdem tőletek: / Szabad-e sírni a Kárpátok alatt?”", "helyes": "Ady Endre: Góg és Magóg fia vagyok én...", "opciok": ["Ady Endre: Góg és Magóg fia vagyok én...", "Babits Mihály: In Horatium", "Kosztolányi Dezső: A szegény kisgyermek panaszai", "József Attila: A Dunánál"], "info": "Ady 1906-os Új versek kötetének programadó nyitóverse."},
    {"idezet": "„Mondottam, ember: küzdj és bízva bízzál!”", "helyes": "Madách Imre: Az ember tragédiája", "opciok": ["Madách Imre: Az ember tragédiája", "Arany János: A walesi bárdok", "Vörösmarty Mihály: Csongor és Tünde", "Katona József: Bánk bán"], "info": "A 15. szín zárómondata, az Úr szózata Ádámhoz."}
]

# -------------------------------------------------------------
# 4. IDŐVONAL ADATBÁZIS
# -------------------------------------------------------------
idovonal_adat = [
    {"ev": "1848–1849", "cim": "Forradalom és Szabadságharc", "leiras": "Petőfi és a márciusi ifjak forradalmi költészete; Arany János korai korszaka és a nemzeti összefogás."},
    {"ev": "1850-es évek", "cim": "Bach-korszak & Elnyomás", "leiras": "Passzív ellenállás. Arany János nagykőrösi balladái (A walesi bárdok, Szondi két apródja); Madách megírja Az ember tragédiáját (1859-60)."},
    {"ev": "1867", "cim": "A Kiegyezés kora", "leiras": "Polgárosodás és gazdasági fejlődés. Jókai Mór érett regényei (Az arany ember, 1872), Mikszáth palóc novellái, Vajda János lírai magánya."},
    {"ev": "1877", "cim": "Arany János Őszikék korszaka", "leiras": "A Margitszigeten írt Kapcsos könyv; a modern nagyvárosi elidegenedés és a Híd-avatás haláltánca."},
    {"ev": "1908", "cim": "A Nyugat folyóirat indulása", "leiras": "A modern magyar irodalom forradalma. Ady Endre (Új versek), Babits Mihály, Kosztolányi Dezső, Móricz Zsigmond fellépése."},
    {"ev": "1914–1919", "cim": "I. Világháború és Tanácsköztársaság", "leiras": "Keserű háborús költészet (Ady: Ember az embertelenségben). Kosztolányi Édes Anna című regényének történelmi kezdőpontja (1919 nyara)."},
    {"ev": "1938–1944", "cim": "Fasizmus árnyéka és II. Világháború", "leiras": "Babits megírja a Jónás könyvét (1938), Radnóti Miklós kései eclogái és bori notesze a humanizmus védelmében."}
]

# Flashcard lista mindkét tantárgyból
flashcards_adat = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra (dalforma), epika (cselekmény) és dráma (konfliktus) sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a legfontosabb irodalmi szerkesztője?", "a": "1908. január 1-jén indult, és Osvát Ernő volt a lap legendás irodalmi szerkesztője."},
    {"q": "Mi a magyar helyesírás 4 alapelve?", "a": "1. Kiejtés elve, 2. Szóelemzés elve, 3. Hagyomány elve, 4. Egyszerűsítés elve."},
    {"q": "Mi a különbség az anafora és a katafora között a szövegtanban?", "a": "Az anafora visszautal egy korábbi szövegelemre, míg a katafora előreutal egy későbbi elemre."},
    {"q": "Mi a szónoki beszéd 6 klasszikus szerkezeti része?", "a": "Bevezetés (Exordium) -> Elbeszélés (Narratio) -> Részletezés -> Bizonyítás -> Cáfolás -> Befejezés (Peroratio)."},
    {"q": "Mit szimbolizál az Ágnes asszonyban a véres lepedő kényszeres mosása?", "a": "A bűn letörölhetetlenségét és a lelkiismeret-furdalás által kiváltott elmezavart."},
    {"q": "Melyik a legkorábbi fennmaradt összefüggő magyar szövegemlék?", "a": "A Halotti Beszéd és Könyörgés (1195 körül, a Pray-kódexben)."}
]

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
        {"role": "ai", "text": "Szia! Én vagyok az érettségi mentorod. Kérdezz bátran irodalomról vagy nyelvtanról!"}
    ]

# PDF Generálás
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

def letoltheto_pdf_generalas(tetelek_adat, tantargy_nev):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_x(15)
    pdf.cell(180, 8, f'{tantargy_nev} Erettsegi Tetelvazlatok', align='C', new_x="LMARGIN", new_y="NEXT")
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
    st.caption("Astra AI Érettségi Felkészítő Platform")
with col_h2:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 10px;'>
        <span class='stat-badge'>🔥 {st.session_state.streak} napos széria</span>
        <span class='stat-badge'>⚡ {st.session_state.xp} XP</span>
        <span class='stat-badge'>🏆 Szint {st.session_state.level}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================
# FŐ TANTÁRGY VÁLASZTÓ (Irodalom vs. Nyelvtan vs. Későbbi tantárgyak)
# =============================================================
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox(
    "Válassz tantárgyat:",
    ["📖 Magyar Irodalom (11 tétel)", "🔤 Magyar Nyelvtan (8 tétel)", "🏛️ Történelem (Hamarosan)", "📐 Matematika (Hamarosan)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#818cf8;'>Funkciók</h2>", unsafe_allow_html=True)
menupont = st.sidebar.radio(
    "Válassz menüpontot:",
    [
        "📚 Tételek & Vázlatok",
        "🎧 Hangoskönyv (Monológ)",
        "🎴 Villámkártyák (Flashcards)",
        "🎙️ Szóbeli Szimulátor",
        "✍️ Esszé & Írásbeli Javító",
        "🎭 Idézet-Detektív Játék",
        "🧭 Történelmi & Irodalmi Idővonal",
        "🏆 Nagy Próbavizsga",
        "🤖 AI Érettségi Mentor"
    ]
)

# Adatbázis hozzárendelése a kiválasztott tantárgyhoz
if "Irodalom" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_irodalom
    tantargy_cimke = "Magyar Irodalom"
elif "Nyelvtan" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_nyelvtan
    tantargy_cimke = "Magyar Nyelvtan"
else:
    st.info("Ez a tantárgyi modul hamarosan elérhető lesz! Addig válaszd a Magyar Irodalom vagy Magyar Nyelvtan tantárgyat.")
    aktiv_adatbazis = tetelek_irodalom
    tantargy_cimke = "Magyar Irodalom"

# PDF Letöltés
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Letölthető tananyag")
if st.sidebar.button(f"📄 {tantargy_cimke} PDF Puska"):
    pdf_bytes = letoltheto_pdf_generalas(aktiv_adatbazis, tantargy_cimke)
    st.sidebar.download_button(
        label="⬇️ Letöltés indítása",
        data=pdf_bytes,
        file_name=f"{tantargy_cimke}_Erettsegi_Puska.pdf",
        mime="application/pdf"
    )

# -------------------------------------------------------------
# 1. MENÜPONT: TÉTELEK ÉS VÁZLATOK
# -------------------------------------------------------------
if menupont == "📚 Tételek & Vázlatok":
    st.markdown(f"<div class='subject-pill'>🎯 Aktuális tantárgy: {tantargy_cimke}</div>", unsafe_allow_html=True)
    kivalasztott_tetel = st.selectbox("Válassz tételt a kidolgozáshoz:", list(aktiv_adatbazis.keys()))
    adat = aktiv_adatbazis[kivalasztott_tetel]
    
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

# -------------------------------------------------------------
# 2. MENÜPONT: HANGOSKÖNYV (1.5-2 perces monológok)
# -------------------------------------------------------------
elif menupont == "🎧 Hangoskönyv (Monológ)":
    st.title(f"🎧 Hangoskönyv Felkészítő – {tantargy_cimke}")
    st.caption("Hallgasd meg a tételek teljes, 1.5–2 perces összefüggő szóbeli elemzését!")
    
    kivalasztott_hangos = st.selectbox("Válassz meghallgatandó tételt:", list(aktiv_adatbazis.keys()), key="audio_select")
    adat_hangos = aktiv_adatbazis[kivalasztott_hangos]
    
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

# -------------------------------------------------------------
# 3. MENÜPONT: VILLÁMKÁRTYÁK (FLASHCARDS)
# -------------------------------------------------------------
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

# -------------------------------------------------------------
# 4. MENÜPONT: SZÓBELI SZIMULÁTOR
# -------------------------------------------------------------
elif menupont == "🎙️ Szóbeli Szimulátor":
    st.title("🎙️ Szóbeli Érettségi Szimulátor (Mock Exam)")
    st.caption("Gyakorold a szóbeli feleletet! Az AI vizsgaelnökként automatikusan meghallgat, belekérdez és leosztályoz.")
    
    valasztott_szim_tetel = st.selectbox(f"Válassz {tantargy_cimke} tételt a próbavizsgához:", list(aktiv_adatbazis.keys()))
    
    if st.button("🏁 Új szóbeli felelet indítása"):
        st.session_state.oral_history = [
            {"role": "ai", "text": f"Jó napot kívánok! Húzza ki a tételét... Az Ön tétele: **{valasztott_szim_tetel}**. Kérem, kezdje meg a feleletét a bevezetéssel és a legfontosabb fogalmi sajátosságokkal!"}
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
            {tantargy_cimke} szóbeli érettségi elnök vagy. A diák a(z) '{valasztott_szim_tetel}' tételből felel.
            A diák eddigi válasza: '{felelet_reszlet}'.
            Feladatod:
            1. Röviden értékeld az elmondottakat (pontosság, szakszavak).
            2. Tegyél fel egy célzott, érettségi szintű kérdést a tétel egy másik fontos részletére vonatkozóan, vagy ha a felelet végére ért, adj egy konkrét érdemjegyet (1-5) és szöveges záróértékelést.
            Legyél támogató, de szakmailag precíz tanár!
            """
            ai_valasz = ai_generalas(prompt)
            st.session_state.oral_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 30
            st.rerun()

# -------------------------------------------------------------
# 5. MENÜPONT: ESSZÉ & ÍRÁSBELI JAVÍTÓ
# -------------------------------------------------------------
elif menupont == "✍️ Esszé & Írásbeli Javító":
    st.title("✍️ Esszé & Műelemzés Értékelő Labor")
    st.caption("Másold be az írásbeli fogalmazásodat vagy érvelésedet, és az AI azonnal pontozza az érettségi szempontrendszer szerint!")
    
    diak_essze = st.text_area("Másold be a fogalmazásodat (műelemzés, összehasonlító elemzés vagy érvelés):", height=220)
    
    if st.button("📊 Esszé automatikus ellenőrzése és pontozása"):
        if diak_essze:
            with st.spinner("Az esszé elemzése érettségi szempontok alapján..."):
                prompt = f"""
                Magyar nyelv és irodalom érettségi javító tanár vagy. Értékeld az alábbi diákfogalmazást:
                ---
                {diak_essze}
                ---
                Kérlek, az alábbi szempontok szerint strukturáld az értékelést:
                1. **Tartalmi minőség & Szakmai pontosság (max 40 pont):** Tények, fogalmak helyes használata.
                2. **Szerkezet & Logikai felépítés (max 20 pont):** Bevezetés, tárgyalás, befejezés, bekezdések.
                3. **Nyelvhelyesség & Stílus (max 20 pont):** Szókincs, helyesírás.
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

# -------------------------------------------------------------
# 6. MENÜPONT: IDÉZET-DETEKTÍV JÁTÉK
# -------------------------------------------------------------
elif menupont == "🎭 Idézet-Detektív Játék":
    st.title("🎭 Idézet-Detektív Játék")
    st.caption("Felismered a legfontosabb kötelező irodalmi idézeteket és szerzőiket?")
    
    if 'game_idx' not in st.session_state:
        st.session_state.game_idx = 0
        
    feladvany = idezet_adatbazis[st.session_state.game_idx]
    
    st.markdown(f"""
    <div class='topic-card' style='border-color:#ec4899; text-align:center;'>
        <h3 style='color:#f472b6; font-style:italic;'>{feladvany['idezet']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    valasztott_tipp = st.radio("Válaszd ki a helyes művet és szerzőt:", feladvany['opciok'], key=f"detektiv_{st.session_state.game_idx}")
    
    if st.button("🔍 Tipp ellenőrzése"):
        if valasztott_tipp == feladvany['helyes']:
            st.balloons()
            st.session_state.xp += 30
            st.success(f"TÖKÉLETES! 🎉 Helyes válasz! (+30 XP)\n\n📌 Háttér: {feladvany['info']}")
        else:
            st.error(f"Sajnos nem! ❌ A helyes válasz: **{feladvany['helyes']}**\n\n📌 Háttér: {feladvany['info']}")
            
    if st.button("➡️ Következő idézet"):
        st.session_state.game_idx = (st.session_state.game_idx + 1) % len(idezet_adatbazis)
        st.rerun()

# -------------------------------------------------------------
# 7. MENÜPONT: TÖRTÉNELMI & IRODALMI IDŐVONAL
# -------------------------------------------------------------
elif menupont == "🧭 Történelmi & Irodalmi Idővonal":
    st.title("🧭 Történelmi & Irodalmi Idővonal (Timeline)")
    st.caption("Lásd át egyben, melyik szerző és mű melyik történelmi korszakhoz kapcsolódik!")
    
    for item in idovonal_adat:
        st.markdown(f"""
        <div class='timeline-item'>
            <span style='background:#7c3aed; color:white; padding:4px 10px; border-radius:8px; font-weight:700;'>{item['ev']}</span>
            <h3 style='color:#c084fc; margin:8px 0 4px 0;'>{item['cim']}</h3>
            <p style='color:#e2e8f0; margin:0;'>{item['leiras']}</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 8. MENÜPONT: NAGY PRÓBAVIZSGA
# -------------------------------------------------------------
elif menupont == "🏆 Nagy Próbavizsga":
    st.title(f"🏆 Teljes Érettségi Próbavizsga – {tantargy_cimke}")
    st.write("Válaszold meg az összes kérdést a felkészültségi szinted ellenőrzéséhez!")
    
    osszes_kerdes = []
    for t_nev, t_adat in aktiv_adatbazis.items():
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
                    
        szazalek = int((pont / len(osszes_kerdes)) * 100) if len(osszes_kerdes) > 0 else 0
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

# -------------------------------------------------------------
# 9. MENÜPONT: AI ÉRETTSÉGI MENTOR CHAT
# -------------------------------------------------------------
elif menupont == "🤖 AI Érettségi Mentor":
    st.title("🤖 AI Érettségi Mentor")
    st.caption("Kérdezz bármilyen irodalmi vagy nyelvtani tételről, fogalomról, versről vagy szerzőről!")

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
            prompt = f"Magyar nyelv és irodalom szakos érettségi felkészítő tanár vagy. Válaszolj tömören, lényegretörően egy 18 éves diák kérdésére: {felh_kerdes}"
            ai_valasz = ai_generalas(prompt)
            st.session_state.chat_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 10
            st.rerun()
