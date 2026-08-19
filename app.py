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

# Astra AI stílusú prémium sötét téma és gombkontraszt
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
# 2. MAGYAR NYELVTAN TÉTELTÁR (8 Tétel)
# -------------------------------------------------------------
tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, kommunikációs funkciók",
        "kulcsszavak": ["Adó és Vevő", "Kód és Csatorna", "Jakobson modellje", "Metakommunikáció"],
        "audio_szoveg": "A kommunikáció információk, gondolatok és érzelmek átadása valamilyen jelrendszer segítségével. Jakobson modellje szerint a folyamat alaptényezői az adó, a vevő, az üzenet, a kód és a csatorna...",
        "vazlat": """
### I. A kommunikáció 6 alaptényezője (Jakobson)
- Adó, Vevő, Üzenet, Kód (közös nyelv), Csatorna (közeg), Kontextus (beszédhelyzet), Zaj.
### II. Nyelvi funkciók
- Tájékoztató, Érzelemkifejező, Felhívó, Kapcsolattartó (fatikus), Értelmező (metanyelvi), Esztétikai (poétikai).
### III. Nem nyelvi jelek: Testbeszéd, mimika, gesztusok, térközszabályozás (proxemika).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. 6 tényező -> 3. Funkciók -> 4. Nem nyelvi kódok.",
        "kviz": [{"k": "A fatikus funkció célja a kapcsolat felvétele és fenntartása.", "v": True, "m": "Ilyenek a köszönések és bejelentkezések."}]
    },
    "2. A szövegtan alapjai és a szövegtípusok": {
        "alcim": "A szöveg kohéziós erői, szerkezeti egységei és típusai",
        "kulcsszavak": ["Globális kohézió", "Lokális kohézió", "Anafora és Katafora", "Elbeszélő, leíró, érvelő"],
        "audio_szoveg": "A szöveg a nyelv legmagasabb szintű, lezárt, kerek egysége...",
        "vazlat": """
### I. Szövegkohézió: Lokális (kötőszók, anafora=visszautalás, katafora=előreutalás) vs. Globális (témamegtartás, kulcsszavak).
### II. Szerkezet: Cím -> Bevezetés -> Tárgyalás -> Befejezés.
### III. Típusok: Elbeszélő, leíró, érvelő, magyarázó; hétköznapi, hivatalos, tudományos, publicisztikai.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szöveg fogalma -> 2. Kohéziós erők -> 3. Hármas szerkezet -> 4. Szövegtípusok.",
        "kviz": [{"k": "Az anafora a szövegben visszamutató utalást jelent.", "v": True, "m": "A katafora az előreutalás."}]
    },
    "3. A magyar helyesírás alapelvei": {
        "alcim": "A 4 alapelv rendszere és alkalmazásuk a gyakorlatban",
        "kulcsszavak": ["Kiejtés elve", "Szóelemzés elve", "Hagyomány elve", "Egyszerűsítés elve"],
        "audio_szoveg": "A magyar helyesírás négy alapelvre épül: kiejtés, szóelemzés, hagyomány és egyszerűsítés elve...",
        "vazlat": """
### I. A 4 alapelv:
1. **Kiejtés elve:** Úgy írjuk, ahogy ejtjük (*ablak, ember*).
2. **Szóelemzés elve:** Szótő és toldalék eredeti alakban marad (*látja [láttya], barátság*).
3. **Hagyomány elve:** Történelmi nevek és ly (*Kossuth, Széchenyi, király*).
4. **Egyszerűsítés elve:** Kettőzött kétjegyűek (*asszony, mennyi*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Helyesírás célja -> 2. Kiejtés és szóelemzés -> 3. Hagyomány és egyszerűsítés -> 4. Példák.",
        "kviz": [{"k": "A 'látja' szó leírása a szóelemzés elvét követi.", "v": True, "m": "A szótő és toldalék tisztán marad."}]
    },
    "4. Szófajok és mondatrészek rendszere": {
        "alcim": "Alapszófajok, viszonyszók, predikatív viszony és mondattani elemzés",
        "kulcsszavak": ["Ige, Névszó, Igenév", "Viszonyszók", "Alany, Állítmány, Tárgy, Határozó, Jelző"],
        "audio_szoveg": "A szófajok a szavak alaktani és mondattani kategóriái...",
        "vazlat": """
### I. Szófajok: Alapszófajok (ige, főnév, melléknév, számnév, névmás, igenevek), Viszonyszók (névelő, kötőszó, névutó, igekötő), Mondatszók.
### II. Mondatrészek: Alany + Állítmány (predikatív mag) -> Bővítmények: Tárgy, Határozók, Jelzők.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szófaji felosztás -> 2. Alapszófaj vs. viszonyszó -> 3. Mondatrészek hierarchiája.",
        "kviz": [{"k": "A kötőszók az alapszófajok közé tartoznak.", "v": False, "m": "A viszonyszókhoz tartoznak."}]
    },
    "5. Retorika és érvelési technikák": {
        "alcim": "Az érv 3 része, érvtípusok és a klasszikus szónoki beszéd 6 lépése",
        "kulcsszavak": ["Tétel, Bizonyíték, Összekötés", "Szónoki beszéd szerkezete", "Érvtípusok"],
        "audio_szoveg": "A retorika az ékesszólás és meggyőzés művészete. Az érv három alapeleme a tétel, a bizonyíték és az összekötés...",
        "vazlat": """
### I. Az érv szerkezete: Tétel -> Bizonyíték (Adat) -> Összekötő elem.
### II. Érvtípusok: Meghatározásból levezetett, ok-okozati, tekintélyre hivatkozó, analógiás.
### III. Szónoki beszéd: Bevezetés -> Elbeszélés -> Részletezés -> Bizonyítás -> Cáfolás -> Befejezés.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Retorika célja -> 2. Érv 3 része -> 3. Érvtípusok -> 4. Szónoki beszéd felépítése.",
        "kviz": [{"k": "A klasszikus szónoki beszédben a cáfolás megelőzi a befejezést.", "v": True, "m": "A bizonyítás után jön a cáfolat."}]
    },
    "6. Stilisztika: Alakzatok és trópusok": {
        "alcim": "Költői képek (metafora, metonímia, szinesztézia) és szövegalakzatok",
        "kulcsszavak": ["Metafora, Metonímia, Szinekdoché", "Szinesztézia", "Anafora, Párhuzam, Ellentét"],
        "audio_szoveg": "A stilisztika a kifejezőeszközöket vizsgálja. Két fő ága a szóképek és a szövegalakzatok rendszere...",
        "vazlat": """
### I. Trópusok: Metafora (hasonlóság), Metonímia (érintkezés), Szinekdoché (rész-egész), Szinesztézia (érzékkeverés), Megszemélyesítés.
### II. Alakzatok: Anafora (sor eleji ismétlés), Paralelizmus (párhuzam), Antitézis (ellentét), Hiperbola (túlzás).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Képek és alakzatok különbsége -> 2. Metafora vs. metonímia -> 3. Szinesztézia -> 4. Alakzatok.",
        "kviz": [{"k": "A 'sötét csend' szinesztézia.", "v": True, "m": "Látás és hallás összekapcsolása."}]
    },
    "7. A szókészlet rétegződése és változása": {
        "alcim": "Nyelvjárások, társadalmi rétegnyelvek, szleng, archaizmusok és neologizmusok",
        "kulcsszavak": ["Nyelvjárások", "Szaknyelv, Szleng, Argó", "Archaizmus", "Neologizmus"],
        "audio_szoveg": "A szókészlet területi és társadalmi tagolódást mutat...",
        "vazlat": """
### I. Területi rétegződés: Nyelvjárások (dialektusok) és tájszavak.
### II. Társadalmi rétegződés: Szaknyelv, rétegnyelvek, szleng és argó.
### III. Időbeli változás: Archaizmusok (elavult szavak) vs. Neologizmusok (új szavak).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Vízszintes tagozódás -> 2. Függőleges rétegződés -> 3. Időbeli mozgás.",
        "kviz": [{"k": "Az archaizmusok új szavakat jelentenek.", "v": False, "m": "Az archaizmusok a régies szavak."}]
    },
    "8. A magyar nyelv története és a nyelvújítás": {
        "alcim": "A finnugor rokonság, a korai nyelvemlékek és Kazinczy nyelvújítása",
        "kulcsszavak": ["Uráli / Finnugor nyelvcsalád", "Halotti Beszéd (1195)", "Nyelvújítás", "Kazinczy Ferenc"],
        "audio_szoveg": "A magyar nyelv a finnugor nyelvcsalád tagja. Írásbeliségünk legrégebbi emléke a Halotti Beszéd...",
        "vazlat": """
### I. Eredet és nyelvemlékek: Uráli nyelvcsalád, finnugor ág. Tihanyi alapítólevél (1055, szórvány), Halotti Beszéd (1195, összefüggő).
### II. Nyelvújítás (1790–1820): Kazinczy Ferenc; Neológusok vs. Ortológusok; új szavak teremtése (képzés, összetétel, elvonás).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Finnugor rokonság -> 2. Korai nyelvemlékek -> 3. Nyelvújítás célja és Kazinczy szerepe.",
        "kviz": [{"k": "A Halotti Beszéd az első fennmaradt összefüggő magyar szövegemlék.", "v": True, "m": "1195 körül keletkezett."}]
    }
}

# -------------------------------------------------------------
# 3. TÖRTÉNELEM TÉTELTÁR (10 Tétel)
# -------------------------------------------------------------
tetelek_tortenelem = {
    "1. Az athéni demokrácia működése a Kr. e. V. században": {
        "alcim": "Szolón, Kleiszthenész reformjai, Periklész kora és a népgyűlés (ekklészia)",
        "kulcsszavak": ["Népgyűlés (Ekklészia)", "Cserépszavazás (Oszztrakizmosz)", "Sztratégosz", "Napidíj", "Periklész"],
        "audio_szoveg": "Az athéni demokrácia az ókori világ legfejlettebb népuralmi rendszere volt. Kialakulása Szolón vagyoni osztályain és Kleiszthenész területi felosztásán keresztül vezetett Periklész virágkoráig...",
        "vazlat": """
### I. A demokrácia kialakulásának állomásai
- **Szolón (Kr. e. 594):** Teherlerázás (*szeiszakhteia*), vagyoni osztályok (*timokrácia*).
- **Kleiszthenész (Kr. e. 508):** Területi felosztás (10 phülé), Cserépszavazás (*osztrakizmosz*) a zsarnokság ellen.

### II. Intézményrendszer Periklész korában (Kr. e. V. század)
- **Népgyűlés (Ekklészia):** A legfőbb törvényhozó szerv, minden 20 év feletti szabad athéni férfi polgár tagja.
- **500-ak Tanácsa (Bulé):** A népgyűlés elé kerülő javaslatok előkészítése (sorsolással választva).
- **Sztratégoszok:** 10 választott hadvezér (a tényleges végrehajtó hatalom, Periklészt 15 évig újraválasztották).
- **Napidíjak bevezetése:** Lehetővé tette a szegényebb polgárok részvételét az esküdtbíróságokon (*héliaia*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Demokrácia fogalma és előzményei -> 2. Főbb intézmények (Ekklészia, Bulé, Héliaia) -> 3. Periklész reformjai (napidíj) -> 4. Korlátok (nők, rabszolgák, betelepültek kizárása).",
        "kviz": [
            {"k": "Az athéni népgyűlés tagja lehetett minden szabad athéni férfi állampolgár.", "v": True, "m": "A közvetlen demokrácia alapelve volt."},
            {"k": "A sztratégoszokat sorsolással választották Athénban.", "v": False, "m": "A sztratégoszokat szakértelmük miatt szavazással választották."}
        ]
    },
    "2. Szent István államalapítása és az egyházszervezés": {
        "alcim": "A keresztény királyság megszilárdítása, vármegyerendszer és törvények",
        "kulcsszavak": ["Koppány legyőzése (997)", "Koronázás (1000/1001)", "10 egyházmegye", "Vármegyék és ispánok", "Tized"],
        "audio_szoveg": "Géza fejedelem nyugati nyitása után fia, István király 1000 karácsonyán felvette a keresztény királyi koronát a pápától...",
        "vazlat": """
### I. Hatalomra jutás és belső harcok
- Senioratus (Koppány) vs. Primogenitura (István) összecsapása (997) $\rightarrow$ István győzelme német lovagok segítségével.
- Törzsfők legyőzése (Gyula, Ajtony) $\rightarrow$ az ország egyesítése.

### II. Egyházszervezet és törvények
- 10 püspökség (köztük 2 érsekség: Esztergom és Kalocsa), pannonhalmi bencés apátság.
- **Törvények:** Minden 10 falu építsen templomot; egyházi tized (*decima*) fizetése; vasárnapi miselátogatás kötelező; magántulajdon védelme.

### III. Világi közigazgatás
- Királyi vármegyerendszer kiépítése, élükön az *ispán* (*comes*).
- Királyi jövedelmek: várföldek jövedelme, vámok, pénzverés.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trónra jutás és koronázás -> 2. Egyházszervezés (Esztergom, tized) -> 3. Vármegyerendszer -> 4. Történelmi jelentőség.",
        "kviz": [{"k": "Szent István törvényei szerint minden 10 falunak kötelező volt közös templomot építenie.", "v": True, "m": "Ez alapozta meg a falusi keresztény hálózatot."}]
    },
    "3. Az Anjouk kora Magyarországon": {
        "alcim": "Károly Róbert gazdasági reformjai és Nagy Lajos 1351-es törvényei",
        "kulcsszavak": ["Kiskirályok legyőzése", "Bányabér (Urbura)", "Aranyforint", "Kapuadó", "1351: Ősiség és Kilenced"],
        "audio_szoveg": "Az Árpád-ház kihalása után Károly Róbert megszilárdította a királyi hatalmat, legyőzte a tartományurakat, és stabil gazdasági reformokat vezetett be...",
        "vazlat": """
### I. Károly Róbert (1308–1342) gazdasági reformjai
- Kiskirályok (Csák Máté, Aba Amadé) felszámolása.
- **Bányareform:** A bányabér (*urbura*) 1/3-át átengedte a földbirtokosnak $\rightarrow$ Magyarország Európa aranytermelésének élére állt.
- **Pénzügyi stabilitás:** Értékálló aranyforint firenzei mintára; kamara haszna kiesése miatt *kapuadó* bevezetése; harmincadvám.
- **1335: Visegrádi királytalálkozó:** Cseh-lengyel-magyar szövetség, Bécset elkerülő kereskedelmi útvonal.

### II. Nagy Lajos (1342–1382) és az 1351-es törvények
- **Ősiség törvénye (*aviticitas*):** A nemesi birtok nem adható el, nemes halálakor a rokonokra száll (védi a nemesi vagyont).
- **Kilenced:** Kötelező földesúri adó a jobbágyoktól (megakadályozta az elszegényedést).
- **Egy és ugyanazon nemesi szabadság elve:** Egységes jogok a kis- és nagynemeseknek.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Károly Róbert gazdasági újításai (urbura, kapuadó) -> 2. 1335 Visegrádi csúcs -> 3. Nagy Lajos 1351-es törvényei (ősiség, kilenced) -> 4. Összegzés.",
        "kviz": [{"k": "Az 1351-es törvényekben bevezetett ősiség megengedte a nemesi föld szabad eladását.", "v": False, "m": "Pontosan tiltotta az eladást, a birtok a nemzetségen belül öröklődött."}]
    },
    "4. Hunyadi Mátyás uralkodása (1458–1490)": {
        "alcim": "Központosított monarchia, bevételek, Fekete sereg és a reneszánsz udvar",
        "kulcsszavak": ["Füstpénz (Füstpénz / Családonként)", "Rendkívüli hadiadó", "Fekete sereg", "Királyi kancellária", "Bibliotheca Corviniana"],
        "audio_szoveg": "Hunyadi Mátyás a magyar történelem egyik legsikeresebb reneszánsz uralkodója volt, aki erős központosított királyi hatalmat épített ki...",
        "vazlat": """
### I. A központosított királyi hatalom és gazdaság
- Hagyományos adók reformja: Kapuadó helyett *füstpénz* (jobbágyportánként helyett háztartásonként szedve).
- *Rendkívüli hadiadó:* Évente 1 aranyforint portánként (gyakran évente kétszer is beszedve).
- Mátyás éves bevétele elérte az 500-800 ezer forintot.

### II. Hadsereg és külpolitika
- **Fekete sereg:** Állandó zsoldoshadsereg (Kinizsi Pál, Haugwitz vezetésével).
- Déli határvédelem a török ellen (kettős végvári vonal megerősítése).
- Nyugati hadjáratok: Cseh és osztrák területek elfoglalása (1485: Bécs bevétele), cél a német-római császári cím megszerzése.

### III. Reneszánsz kultúra
- Beatrix királyné érkezése, humanista tudósok (Bonfini, Galeotto Marzio).
- *Bibliotheca Corviniana:* Európa egyik legnagyobb könyvtára Budán és Visegrádon.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mátyás trónra lépése -> 2. Gazdasági bevételek és füstpénz -> 3. Fekete sereg és külpolitika -> 4. Reneszánsz kultúra Budán.",
        "kviz": [{"k": "Mátyás zsoldoshadseregét Fekete seregnek nevezték.", "v": True, "m": "Európa egyik legütőképesebb állandó zsoldoshadserege volt."}]
    },
    "5. A reformkor fő kérdései (1830–1848)": {
        "alcim": "Széchenyi István és Kossuth Lajos reformprogramjának összehasonlítása",
        "kulcsszavak": ["1830 Hitel", "Önkéntes és Kötelező örökváltság", "Közteherviselés", "Pesti Hírlap", "Lánchíd"],
        "audio_szoveg": "A magyar reformkor 1830-ban, Széchenyi Hitel című művének megjelenésével vette kezdetét...",
        "vazlat": """
### I. Gróf Széchenyi István programja
- Kiindulópont: 1830 *Hitel*, *Világ*, *Stádium* (12 pont).
- Fő célok: Az ősiség eltörlése (hitelképesség megteremtése), lassú, arisztokrácia által vezetett szerves fejlődés a Habsburg Birodalmon belül.
- Gyakorlati alkotások: Lánchíd, Vaskapu szabályozása, gőzhajózás, Magyar Tudományos Akadémia felajánlása (1825).

### II. Kossuth Lajos és a liberális ellenzék programja
- *Pesti Hírlap* szerkesztése (1841-től) $\rightarrow$ a nyilvánosság ereje, vezércikkek.
- Fő követelések: **Kötelező örökváltság állami kárpótlással** (jobbágyfelszabadítás), **Közteherviselés** (nemesi adómentesség eltörlése), **Érdekegyesítés** (nemesség és jobbágyság összefogása), Sajtószabadság.

### III. Ellenzéki Nyilatkozat (1847)
- Deák Ferenc és Kossuth közös programja: felelős minisztérium, népképviselet, törvény előtti egyenlőség.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Reformkor fogalma (1830-1848) -> 2. Széchenyi arisztokratikus gazdasági programja -> 3. Kossuth társadalmi érdekegyesítése -> 4. A két reformer vitája.",
        "kviz": [{"k": "Kossuth Lajos az önkéntes örökváltság híve volt állami segítség nélkül.", "v": False, "m": "Kossuth a kötelező örökváltságot követelte állami kárpótlással."}]
    },
    "6. Az 1848–49-es forradalom és szabadságharc": {
        "alcim": "Március 15., az Áprilisi törvények és a Tavaszi hadjárat sikerei",
        "kulcsszavak": ["12 pont", "Áprilisi törvények (1848. ápr. 11.)", "Batthyány Lajos kormánya", "Görgei Artúr", "Függetlenségi Nyilatkozat (1849. ápr. 14.)"],
        "audio_szoveg": "1848 tavaszán a pesti forradalom és az Áprilisi törvények szentesítése polgári Magyarországot teremtett...",
        "vazlat": """
### I. 1848. március 15. és az Áprilisi törvények (1848. április 11.)
- Pesti forradalom: Nemzeti dal, 12 pont, Táncsics kiszabadítása.
- **Áprilisi törvények:** Független, felelős magyar minisztérium (Batthyány-kormány); Népképviseleti országgyűlés Pesten; Jobbágyfelszabadítás; Közteherviselés; Sajtószabadság; Unió Erdéllyel.

### II. Az önvédelmi háború és a Tavaszi hadjárat (1849)
- Pákozd (1848. szept. 29. – Jellasics megállítása).
- 1849 tavaszi dicsőséges hadjárat (Görgei Artúr vezetésével: Hatvan, Tápióbicske, Isaszeg, Komárom felmentése, Buda visszavétele május 21-én).
- **1849. április 14. (Debrecen):** Függetlenségi Nyilatkozat és a Habsburg-ház trónfosztása.

### III. A szabadságharc leverése
- I. Ferenc József segítséget kér I. Miklós orosz cártól $\rightarrow$ Világosi fegyverletétel (1849. aug. 13.).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Március 15. és Áprilisi törvények -> 2. Batthyány-kormány és önvédelmi harc -> 3. Tavaszi hadjárat és Trónfosztás -> 4. Orosz intervenció és vereség.",
        "kviz": [{"k": "A Batthyány-kormány volt az első felelős magyar minisztérium.", "v": True, "m": "1848 áprilisában alakult meg."}]
    },
    "7. A dualizmus kora Magyarországon (1867–1914)": {
        "alcim": "A Kiegyezés rendszere, gazdasági felvirágzás és társadalmi rétegződés",
        "kulcsszavak": ["Kiegyezés (1867)", "Ferenc József és Deák Ferenc", "Közös ügyek", "Gazdasági csoda", "Torlódó társadalom"],
        "audio_szoveg": "Az 1867-es kiegyezéssel létrejött az Osztrák-Magyar Monarchia, amely fél évszázados békét és példátlan gazdasági fellendülést hozott...",
        "vazlat": """
### I. A Kiegyezés államszervezete (1867)
- Dualista, kétközpontú monarchia (Bécs és Budapest), Ferenc József megkoronázása.
- **Közös ügyek:** Külügy, Hadügy, és az ezek fedezésére szolgáló Pénzügy (60-60 fős delegációk ellenőrzése mellett).
- Gazdasági kiegyezés (10 évente megújítandó): Vámunió, közös valuta (korona), kvóta (Magyarország 30%-ot vállal).

### II. Gazdasági és infrastrukturális robbanás
- Vasúthálózat kiépülése (Baross Gábor), folyószabályozások (Tisza).
- Malomipar (Budapest a világ malomipari fővárosa), gépgyártás (Ganz, MÁVAG).
- Millenniumi ünnepségek (1896): Földalatti, Hősök tere, Országház építése.

### III. A „torlódó társadalom”
- Egymás mellett él a régi feudális réteg (arisztokraták, dzsentrik, parasztság) és az új polgári kapitalista réteg (nagypolgárság, gyári munkásság).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kiegyezés létrejötte és közös ügyek -> 2. Gazdasági fellendülés (vasút, malomipar) -> 3. Torlódó társadalom modellje -> 4. Etnikai és nemzetiségi kérdés.",
        "kviz": [{"k": "A dualizmus korában a külügy és hadügy közös minisztériumok alá tartozott Bécsben.", "v": True, "m": "A pénzügy biztosította ezek költségvetését."}]
    },
    "8. A Horthy-korszak konszolidációja (1920–1931)": {
        "alcim": "Trianon traumája, a bethleni konszolidáció politikai, gazdasági és kulturális eredményei",
        "kulcsszavak": ["Trianoni béke (1920. jún. 4.)", "Teleki Pál", "Bethlen István", "Népszövetségi kölcsön", "Pengő", "Klebelsberg Kuno"],
        "audio_szoveg": "Az I. világháború és a Trianoni békediktátum után gróf Bethlen István miniszterelnöksége alatt ment végbe a magyar gazdaság és társadalom talpra állítása...",
        "vazlat": """
### I. A Trianoni békeszerződés (1920. június 4.)
- Területvesztés: Az ország 2/3 részét elcsatolták; 3,3 millió magyar rekedt az új határokon túl.
- Hadseregkorlátozás (35 ezer fő, nincs nehézfegyverzet), jóvátétel fizetése.

### II. A Bethleni konszolidáció (1921–1931)
- **Politikai stabilitás:** Bethlen-Peyer paktum (kiegyezés a szociáldemokratákkal); Egységes Párt létrehozása; nyílt szavazás vidéken.
- **Gazdasági talpra állás:** Népszövetségi kölcsön (1924), Magyar Nemzeti Bank felállítása, új értékálló valuta: a *Pengő* (1927).
- **Kultúrpolitika (Klebelsberg Kuno):** Népiskolai program (5000 tanterem építése), egyetemek átköltöztetése (Szeged, Debrecen, Pécs), külföldi Collegium Hungaricumok (Bécs, Róma, Berlin) a nemzeti önbecsülés és tehetséggondozás szolgálatában.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trianoni veszteségek -> 2. Bethlen politikai és gazdasági konszolidációja (Pengő) -> 3. Klebelsberg kulturális reformjai -> 4. Külpolitikai kitörés az elszigeteltségből.",
        "kviz": [{"k": "1927-ben vezették be az új magyar valutát, a Pengőt.", "v": True, "m": "A korona elértéktelenedése után stabilizálta a piacot."}]
    },
    "9. Az 1956-os forradalom és szabadságharc": {
        "alcim": "A Rákosi-diktatúra válsága, október 23., Nagy Imre kormánya és a szovjet intervenció",
        "kulcsszavak": ["MEFESZ", "16 pont", "Október 23.", "Nagy Imre", "Corvin köz", "November 4. Szovjet invázió"],
        "audio_szoveg": "1956. október 23-án a budapesti diákok békés felvonulásával kezdődött a magyar történelem legtisztább forradalma a szovjet megszállás és a kommunista diktatúra ellen...",
        "vazlat": """
### I. Előzmények és a forradalom kitörése (1956. október 23.)
- Rákosi-korszak terrorja (ÁVH, koncepciós perek, padlássöprés). Sztálin halála (1953) utáni erjedés.
- Szegedi egyetemisták (MEFESZ), Petőfi Kör vitái.
- Október 23.: Békés tüntetés (Petőfi-szobor, Bem-tér, Parlament) $\rightarrow$ Rádió ostroma a Bródy Sándor utcában (fegyveres harcok kezdete).

### II. A forradalom győzelme (Okt. 28. – Nov. 3.)
- Nagy Imre miniszterelnök elismeri a felkelést nemzeti demokratikus mozgalomként; ÁVH feloszlatása; többpártrendszer visszaállítása.
- Fegyveres ellenállók (Corvin köz – Pongrátz Gergely, Széna tér).
- **November 1.:** Magyarország kikiáltja semlegességét és kilép a Varsói Szerződésből.

### III. A szovjet agresszió és megtorlás
- **November 4.:** „Forgószél” hadművelet – a szovjet hadsereg lerohanja Budapestet. Kádár János bábkormánya.
- Megtorlás: Nagy Imre, Maléter Pál kivégzése (1958), több száz kivégzett szabadságharcos, 200 ezer emigráns.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Rákosi-diktatúra válsága -> 2. Október 23. eseményei -> 3. Nagy Imre kormánya és a semlegesség -> 4. November 4. szovjet támadás és a megtorlás.",
        "kviz": [{"k": "Magyarország 1956. november 1-jén kinyilvánította semlegességét és kilépését a Varsói Szerződésből.", "v": True, "m": "Nagy Imre kormánya hirdette ki."}]
    },
    "10. A rendszerváltás folyamata Magyarországon (1989–1990)": {
        "alcim": "A Kádár-rendszer válsága, az Ellenzéki Kerekasztal, Nagy Imre újratemetése és a szabad választások",
        "kulcsszavak": ["Kádár János bukása (1988)", "Ellenzéki Kerekasztal (EKA)", "1989. jún. 16. Újratemetés", "1989. okt. 23. Köztársaság", "1990 Szabad választások"],
        "audio_szoveg": "1989-1990-ben békés, tárgyalásos úton ment végbe a kommunista diktatúrából a többpárti demokráciába és piacgazdaságba való átmenet...",
        "vazlat": """
### I. A Kádár-korszak gazdasági csődje és az ellenzék formálódása
- Eladósodás, gazdasági stagnálás. 1988: Kádár János leváltása.
- Új ellenzéki szervezetek: MDF (Lakitelek, 1987), Fidesz (1988), SZDSZ (1988), FKgP, KDNP.

### II. A sorsfordító 1989-es év
- **Ellenzéki Kerekasztal (EKA):** Az ellenzéki erők egységes fellépése az MSZMP-vel szemben.
- **1989. június 16.:** Nagy Imre és mártírtársainak ünnepélyes újratemetése a Hősök terén (Orbán Viktor beszéde: a szovjet csapatok kivonása).
- **1989. szeptember:** Határnyitás a keletnémet menekültek előtt (Páneurópai piknik).
- **1989. október 23.:** Szűrös Mátyás kikiáltja a Magyar Köztársaságot.

### III. 1990: Szabad választások
- Az első szabad, többpárti választások (MDF győzelem) $\rightarrow$ Antall József kormánya. A demokratikus jogállam és piacgazdaság kiépülése.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kádár-rendszer válsága -> 2. Ellenzéki Kerekasztal és Nemzeti Kerekasztal tárgyalások -> 3. 1989 kulcsdátumai (újratemetés, határnyitás, Köztársaság) -> 4. 1990-es szabad választások.",
        "kviz": [{"k": "1989. október 23-án kiáltották ki a harmadik Magyar Köztársaságot.", "v": True, "m": "Szűrös Mátyás ideiglenes köztársasági elnök hirdette ki a Parlament erkélyéről."}]
    }
}

# -------------------------------------------------------------
# 4. MATEMATIKA TÉTELTÁR (8 Témakör)
# -------------------------------------------------------------
tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció és kombináció",
        "kulcsszavak": ["Metszet, Unió, Különbség", "Venn-diagram", "Ismétléses és Ismétlés nélküli permutáció", "Kombináció n alatt a k"],
        "audio_szoveg": "A matematika alapvető nyelve a halmazelmélet és a logika. A kombinatorika a véges halmazok elemeinek elrendezéseit és kiválasztásait vizsgálja...",
        "vazlat": """
### I. Halmazműveletek és Logika
- **Unió ($A \cup B$):** Azon elemek, melyek legalább az egyik halmazban benne vannak.
- **Metszet ($A \cap B$):** Azon elemek, melyek mindkét halmazban egyszerre benne vannak.
- **Különbség ($A \setminus B$):** Benne van $A$-ban, de nincs benne $B$-ben.
- **Komplementer ($\overline{A}$):** Az alaphalmaz azon elemei, melyek nincsenek benne $A$-ban.

### II. Kombinatorika alapképletek
- **Permutáció (Sorrendezés):**
  - *Ismétlés nélküli:* $P_n = n! = n \cdot (n-1) \cdot ... \cdot 1$
  - *Ismétléses:* $P_n^{k_1, k_2...} = \frac{n!}{k_1! \cdot k_2!...}$ (pl. betűk sorrendje a 'MISSISSIPPI' szóban).
- **Variáció (Kiválasztás, ahol A SORREND SZÁMÍT):**
  - $V_n^k = \frac{n!}{(n-k)!}$ (pl. versenyen 1., 2., 3. helyezett).
- **Kombináció (Kiválasztás, ahol A SORREND NEM SZÁMÍT):**
  - $C_n^k = \binom{n}{k} = \frac{n!}{k!(n-k)!}$ (pl. 90-ből 5 lottószám kihúzása: $\binom{90}{5}$).
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Halmazok és műveletek (Venn-diagram) -> 2. Permutáció (minden elem sorrendje) -> 3. Variáció és Kombináció közötti különbség (számít-e a sorrend?) -> 4. Gyakorlati lottópélda.",
        "kviz": [
            {"k": "Az 5-ös lottó összes lehetséges szelvényének száma kombinációval számolható: 90 alatt az 5.", "v": True, "m": "Mert a kihúzás sorrendje nem számít."},
            {"k": "0 faktoriális (0!) értéke 0-val egyenlő.", "v": False, "m": "0! definíció szerint 1."}
        ]
    },
    "2. Algebra: Egyenletek, egyenlőtlenségek és másodfokú formula": {
        "alcim": "Másodfokú egyenlet megoldóképlete, diszkrimináns, gyöktényezős alak és Viéte-formulák",
        "kulcsszavak": ["Diszkrimináns ($b^2 - 4ac$)", "Megoldóképlet", "Gyöktényezős alak", "Kikötések és értelmezési tartomány"],
        "audio_szoveg": "Az algebrai egyenletek megoldásának legfontosabb lépése a helyes kikötés és az ekvivalens átalakítások alkalmazása...",
        "vazlat": """
### I. A másodfokú egyenlet ($ax^2 + bx + c = 0$)
- **Megoldóképlet:** $x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
- **Diszkrimináns ($D = b^2 - 4ac$):**
  - Ha $D > 0$: 2 különböző valós gyök van.
  - Ha $D = 0$: 1 valós gyök van (kétszeres gyök).
  - Ha $D < 0$: Nincs valós gyök.
- **Gyöktényezős szorzatalak:** $a(x - x_1)(x - x_2) = 0$
- **Viéte-formulák:** $x_1 + x_2 = -\frac{b}{a}$, $x_1 \cdot x_2 = \frac{c}{a}$

### II. Egyenletmegoldási alapszabályok
1. **Értelmezési tartomány (Kikötések):** Nevező $\neq 0$; Négyzetgyök alatt $\ge 0$; Logaritmus belső száma $> 0$, alapja $> 0$ és $\neq 1$.
2. **Négyzetre emeléskor** hamis gyökök keletkezhetnek $\rightarrow$ **Ellenőrzés kötelező!**
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Értelmezési tartomány és kikötések -> 2. Másodfokú megoldóképlet és a diszkrimináns szerepe -> 3. Gyöktényezős alak -> 4. Miért kötelező az ellenőrzés négyzetre emelés után?",
        "kviz": [{"k": "Ha a másodfokú egyenlet diszkriminánsa negatív, akkor az egyenletnek nincs valós megoldása.", "v": True, "m": "Mert valós számok körében negatív számból nem vonhatunk páros gyököt."}]
    },
    "3. Függvénytan és analízis alapjai": {
        "alcim": "Lineáris, másodfokú, exponenciális, logaritmikus függvények és jellemzésük",
        "kulcsszavak": ["Értelmezési tartomány (É.T.)", "Értékkészlet (É.K.)", "Zérushely", "Szélsőérték", "Monotonitás"],
        "audio_szoveg": "A függvény egy egyértelmű hozzárendelés két halmaz között. Az érettségin alapvető elvárás a függvények szakszerű és teljes jellemzése...",
        "vazlat": """
### I. Függvényjellemzési szempontok
1. **Értelmezési tartomány ($D_f$):** Azon x értékek, ahol a függvény létezik.
2. **Értékkészlet ($R_f$):** Azon y kimenetek, amiket a függvény felvesz.
3. **Zérushely:** Ahol a grafikon metszi az x-tengelyt ($f(x) = 0$).
4. **Szélsőérték:** Minimum és maximum helye ($x$) és értéke ($y$).
5. **Monotonitás:** Szigorúan monoton növekvő vagy csökkenő intervallumok.
6. **Paritás:** Páros ($f(-x) = f(x)$, y-tengelyre szimmetrikus) vagy Páratlan ($f(-x) = -f(x)$, origóra szimmetrikus).

### II. Alapfüggvények transzformációi
- $f(x) + c$: Eltolás y-tengely mentén ($c$-vel fel/le).
- $f(x - d)$: Eltolás x-tengely mentén ($d$-vel jobbra/balra).
- $a \cdot f(x)$: Nyújtás/zsugorítás y-tengely mentén.
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Függvény fogalma -> 2. Jellemzés lépései (É.T., É.K., zérushely, szélsőérték) -> 3. Alapfüggvények transzformációs szabályai.",
        "kviz": [{"k": "Az f(x) = (x - 3)^2 függvény csúcspontja az x = +3 pontban van.", "v": True, "m": "A zárójelen belüli -3 jobbra tolja el a parabolát."}]
    },
    "4. Sorozatok és Pénzügyi matematika": {
        "alcim": "Számtani és mértani sorozat képletei, kamatos kamat és gyűjtőjáradék",
        "kulcsszavak": ["Differencia ($d$)", "Hányados ($q$)", "$n$-edik tag képlete", "Első $n$ tag összege ($S_n$)", "Kamatos kamat"],
        "audio_szoveg": "A sorozatok olyan függvények, melyek értelmezési tartománya a pozitív egész számok halmaza. Az érettségin leggyakrabban számtani és mértani sorozatokkal, valamint kamatos kamatszámítással találkozunk...",
        "vazlat": """
### I. Számtani sorozat (Differencia: $d$)
- Két szomszédos tag különbsége állandó ($a_{n+1} - a_n = d$).
- **$n$-edik tag:** $a_n = a_1 + (n - 1) \cdot d$
- **Összegképlet:** $S_n = \frac{a_1 + a_n}{2} \cdot n = \frac{2a_1 + (n - 1)d}{2} \cdot n$

### II. Mértani sorozat (Hányados: $q$)
- Két szomszédos tag hányadosa állandó ($\frac{a_{n+1}}{a_n} = q$).
- **$n$-edik tag:** $a_n = a_1 \cdot q^{n-1}$
- **Összegképlet ($q \neq 1$):** $S_n = a_1 \cdot \frac{q^n - 1}{q - 1}$

### III. Kamatos kamatszámítás
- Kezdőtőke: $C_0$, éves kamatláb: $p\%$, kamattényező: $r = 1 + \frac{p}{100}$.
- **$n$ év múlva lévő tőke:** $C_n = C_0 \cdot (1 + \frac{p}{100})^n$
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Számtani sorozat definíciója és képletei -> 2. Mértani sorozat definíciója és összege -> 3. Kamatos kamat gyakorlati alkalmazása.",
        "kviz": [{"k": "Ha egy mértani sorozat első tagja 3, hányadosa q=2, akkor a 4. tag értéke 24.", "v": True, "m": "a4 = 3 * 2^3 = 3 * 8 = 24."}]
    },
    "5. Síkgeometria és Trigonometria": {
        "alcim": "Pitagorasz-tétel, Szinusz- és Koszinusztétel, háromszögek területszámítása",
        "kulcsszavak": ["Pitagorasz-tétel", "Szögfüggvények (sin, cos, tg)", "Szinusztétel", "Koszinusztétel", "Területképletek"],
        "audio_szoveg": "A síkgeometria alapja a derékszögű és általános háromszögek metrikus összefüggéseinek pontos ismerete...",
        "vazlat": """
### I. Derékszögű háromszögek összefüggései
- **Pitagorasz-tétel:** $a^2 + b^2 = c^2$
- **Szögfüggvények:**
  - $\sin\alpha = \frac{\text{szemközti befogó}}{\text{átfogó}}$
  - $\cos\alpha = \frac{\text{melletti befogó}}{\text{átfogó}}$
  - $\text{tg}\alpha = \frac{\text{szemközti befogó}}{\text{melletti befogó}}$

### II. Általános háromszögek tételei
- **Szinusztétel:** $\frac{a}{\sin\alpha} = \frac{b}{\sin\beta} = \frac{c}{\sin\gamma} = 2R$ (ahol $R$ a körülírt kör sugara).
- **Koszinusztétel:** $a^2 = b^2 + c^2 - 2bc \cdot \cos\alpha$ (Pitagorasz-tétel általánosítása).
- **Területképletek:**
  - $T = \frac{a \cdot m_a}{2} = \frac{a \cdot b \cdot \sin\gamma}{2} = \sqrt{s(s-a)(s-b)(s-c)}$ (Héron-képlet).
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Derékszögű háromszögek szögfüggvényei -> 2. Szinusztétel és Koszinusztétel mikor melyiket használjuk? -> 3. Területképletek összefoglalása.",
        "kviz": [{"k": "A koszinusztétel bármilyen általános háromszögre érvényes, ha ismerünk két oldalt és a közbezárt szöget.", "v": True, "m": "Ez a tétel leggyakoribb alkalmazása."}]
    },
    "6. Koordinátageometria": {
        "alcim": "Vektorműveletek, egyenes egyenletei (normálvektoros, irányvektoros) és a kör egyenlete",
        "kulcsszavak": ["Normálvektor $\\vec{n}(A, B)$", "Irányvektor $\\vec{v}(v_1, v_2)$", "Egyenes egyenlete", "Kör egyenlete", "Távolságképlet"],
        "audio_szoveg": "A koordinátageometriában az algebrai eszközöket hívjuk segítségül geometriai alakzatok vizsgálatához a derékszögű koordináta-rendszerben...",
        "vazlat": """
### I. Vektorok és pontok távolsága
- Két pont távolsága: $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$
- Felezőpont koordinátái: $F\left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)$

### II. Az egyenes egyenlete
- **Normálvektoros alak ($\vec{n}(A, B)$ merőleges az egyenesre, $P_0(x_0, y_0)$ pont rajta van):**
  - $Ax + By = Ax_0 + By_0$
- **Irányvektoros alak ($\vec{v}(v_1, v_2)$ párhuzamos az egyenessel):**
  - Mivel $\vec{n} = (v_2, -v_1)$, visszaírható a normálvektoros alakra.

### III. A kör egyenlete
- Középpont: $K(u, v)$, sugár: $r$.
- **Egyenlet:** $(x - u)^2 + (y - v)^2 = r^2$
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Vektorok fogalma és távolságképlet -> 2. Egyenes felírása normálvektorból és pontból -> 3. Kör egyenlete és középpontja.",
        "kviz": [{"k": "A (x - 2)^2 + (y + 5)^2 = 16 egyenletű kör sugara 4, középpontja K(2, -5).", "v": True, "m": "Mert r^2 = 16 -> r = 4, és az előjelek u=2, v=-5."}]
    },
    "7. Térgeometria (Testek felszíne és térfogata)": {
        "alcim": "Hasáb, henger, gúla, kúp és gömb felszín- és térfogatszámítása",
        "kulcsszavak": ["Henger", "Kúp", "Gúla", "Gömb", "Felszín ($A$)", "Térfogat ($V$)"],
        "audio_szoveg": "A térgeometria a 3 dimenziós geometriai testek felszínével és térfogatával foglalkozik...",
        "vazlat": """
### I. Egyenes testek (Hasáb és Henger)
- **Henger (alapsugár $r$, magasság $M$):**
  - $V = T_{\text{alap}} \cdot M = r^2 \pi \cdot M$
  - $A = 2 \cdot T_{\text{alap}} + T_{\text{palást}} = 2r^2\pi + 2r\pi M$

### II. Csúcsos testek (Gúla és Kúp)
- **Kúp (alapsugár $r$, alkotó $a$, magasság $M$ - ahol $r^2 + M^2 = a^2$):**
  - $V = \frac{r^2\pi \cdot M}{3}$
  - $A = r^2\pi + r\pi a$
- **Gúla:** $V = \frac{T_{\text{alap}} \cdot M}{3}$

### III. Gömb (Sugár: $R$)
- **Térfogat:** $V = \frac{4}{3} R^3 \pi$
- **Felszín:** $A = 4 R^2 \pi$
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Hasábok és hengerek térfogata (alapterület * magasság) -> 2. Csúcsos testek harmadoló szabálya -> 3. Gömb képletei.",
        "kviz": [{"k": "A kúp és gúla térfogata a megfelelő henger/hasáb térfogatának harmadrésze.", "v": True, "m": "A csúcsos testek térfogatképletében ott van az 1/3 szorzó."}]
    },
    "8. Valószínűségszámítás és Statisztika": {
        "alcim": "Klasszikus valószínűségi modell, visszatevéses mintavétel, átlag, medián, módusz és szórás",
        "kulcsszavak": ["Kedvező / Összes", "Független események", "Medián", "Módusz", "Átlag", "Szórás"],
        "audio_szoveg": "A valószínűségszámítás a véletlen események törvényszerűségeit kutatja. A klasszikus valószínűség képlete: kedvező esetek osztva az összes esettel...",
        "vazlat": """
### I. Valószínűségszámítás
- **Klasszikus valószínűségi mező:** $P(A) = \frac{\text{Kedvező kimenetelek száma}}{\text{Összes lehetséges kimenetel száma}} = \frac{k}{n}$
- **Komplementer esemény valószínűsége:** $P(\overline{A}) = 1 - P(A)$
- **Binomiális eloszlás ($n$ kísérletből $k$ siker, $p$ valószínűséggel):**
  - $P(X = k) = \binom{n}{k} \cdot p^k \cdot (1-p)^{n-k}$

### II. Statisztika
- **Átlag (Számtani közép):** Az adatok összege osztva az adatok számával ($\overline{x} = \frac{\sum x_i}{n}$).
- **Módusz:** A mintában leggyakrabban előforduló érték.
- **Medián:** Növekvő sorba rendezett adatok pontosan középső értéke (páros darabszámnál a két középső átlaga).
- **Terjedelem:** Legnagyobb és legkisebb adat különbsége ($x_{\max} - x_{\min}$).
- **Szórás:** Az adatok átlagtól való átlagos négyzetes eltérésének gyöke (az adatok szétterültségét méri).
        """,
        "szobeli": "**🎙️ 3 perces elméleti felelet:** 1. Klasszikus valószínűség képlete -> 2. Binomiális eloszlás lényege -> 3. Statisztikai középértékek (Átlag, Módusz, Medián) -> 4. Szórás fogalma.",
        "kviz": [{"k": "A medián meghatározásához először mindig nagyság szerint növekvő sorba kell rendezni az adatokat.", "v": True, "m": "A medián a rendezett minta középső eleme."}]
    }
}

# -------------------------------------------------------------
# FLASHCARDS ADATBÁZIS MIND A 4 TANTÁRGYBÓL
# -------------------------------------------------------------
flashcards_adat = [
    # Irodalom
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra (dalforma), epika (cselekmény) és dráma (konfliktus) sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a legfontosabb irodalmi szerkesztője?", "a": "1908. január 1-jén indult, és Osvát Ernő volt a lap legendás irodalmi szerkesztője."},
    {"q": "Mi a központi szállóige Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.” – Az értelmiségi ember morális felelősségvállalása."},
    # Nyelvtan
    {"q": "Mi a magyar helyesírás 4 alapelve?", "a": "1. Kiejtés elve, 2. Szóelemzés elve, 3. Hagyomány elve, 4. Egyszerűsítés elve."},
    {"q": "Mi a különbség az anafora és a katafora között a szövegtanban?", "a": "Az anafora visszautal egy korábbi szövegelemre, míg a katafora előreutal egy későbbi elemre."},
    # Történelem
    {"q": "Mikor adta ki Nagy Lajos az Ősiség törvényét és mit jelentett az?", "a": "1351-ben. A nemesi birtok nem adható el, nemes kihalásakor a rokonokra, végül a királyra száll vissza."},
    {"q": "Mikor és hol kiáltották ki a Függetlenségi Nyilatkozatot 1849-ben?", "a": "1849. április 14-én a debreceni Nagytemplomban, kimondva a Habsburg-ház trónfosztását."},
    {"q": "Milyen új pénznemet vezetett be Bethlen István 1927-ben a gazdasági stabilitásért?", "a": "A Pengőt."},
    # Matek
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Mi a számtani és a mértani sorozat n-edik tagjának képlete?", "a": "Számtani: an = a1 + (n - 1)d | Mértani: an = a1 * q^(n - 1)"},
    {"q": "Mi a Pitagorasz-tétel és milyen háromszögre érvényes?", "a": "a² + b² = c² (kizárólag derékszögű háromszögekre érvényes)."}
]

# Idővonal
idovonal_adat = [
    {"ev": "Kr. e. V. sz.", "cim": "Az athéni demokrácia virágkora", "leiras": "Periklész kora, a népgyűlés és az esküdtbíróságok működése, a napidíjak bevezetése."},
    {"ev": "1000", "cim": "Szent István király koronázása", "leiras": "A keresztény magyar állam és a vármegyerendszer megalapítása, egyházmegyék kiépítése."},
    {"ev": "1351", "cim": "Nagy Lajos törvényei", "leiras": "Az Aranybulla megújítása, az ősiség törvénye és a kilenced bevezetése."},
    {"ev": "1458–1490", "cim": "Hunyadi Mátyás királysága", "leiras": "Központosított királyi hatalom, füstpénz, a Fekete sereg és a reneszánsz kultúra virágkora."},
    {"ev": "1830–1848", "cim": "A magyar reformkor", "leiras": "Széchenyi Hitel című művével indul, Kossuth érdekegyesítési programja, a polgári átalakulás előkészítése."},
    {"ev": "1848–1849", "cim": "Forradalom és Szabadságharc", "leiras": "Március 15., Áprilisi törvények, függetlenségi háború és az 1849-es tavaszi hadjárat sikerei."},
    {"ev": "1867", "cim": "A Kiegyezés – Dualizmus kora", "leiras": "Az Osztrák-Magyar Monarchia létrejötte, Deák Ferenc, fél évszázados gazdasági és kulturális aranykor."},
    {"ev": "1920–1931", "cim": "Trianon és a Bethleni konszolidáció", "leiras": "Trianoni békediktátum (1920), a gazdasági talpra állás (Pengő, 1927), Klebelsberg Kuno iskolaépítési programja."},
    {"ev": "1956. okt. 23.", "cim": "Forradalom és Szabadságharc", "leiras": "A pesti diákok tüntetése, fegyveres harc a szovjet elnyomás ellen, Nagy Imre kormánya, nov. 4-i invázió."},
    {"ev": "1989–1990", "cim": "A Békés Rendszerváltás", "leiras": "Ellenzéki Kerekasztal, Nagy Imre újratemetése, határnyitás, a Köztársaság kikiáltása és az 1990-es szabad választások."}
]

# Idézet és Képlet detektív
detektiv_adatbazis = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma. / Fölkeltem én hát; megbánva a rest / lapulást...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Ember az embertelenségben", "Arany János: Szondi két apródja", "Radnóti Miklós: Nem tudhatom"], "info": "A prófétai és értelmiségi felelősségvállalás alaptétele."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb, / Mit kény és kedv szerint lök / A sors előbb-tovább.”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János: Toldi", "Ady Endre: Új vizeken járok"], "info": "Petőfi forradalmi felhívó lírájának remeke."},
    {"idezet": "„Mondottam, ember: küzdj és bízva bízzál!”", "helyes": "Madách Imre: Az ember tragédiája", "opciok": ["Madách Imre: Az ember tragédiája", "Arany János: A walesi bárdok", "Vörösmarty: Csongor és Tünde", "Katona József: Bánk bán"], "info": "Az Úr szózata a 15. szín lezárásaként."},
    {"idezet": "a² + b² - 2bc · cos(α)", "helyes": "Koszinusztétel (Általános háromszögekre)", "opciok": ["Koszinusztétel (Általános háromszögekre)", "Szinusztétel", "Pitagorasz-tétel", "Héron-képlet"], "info": "A Pitagorasz-tétel általánosítása tetszőleges háromszögre."}
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
        {"role": "ai", "text": "Szia! Én vagyok a felkészítő mentorod. Kérdezz bátran Irodalomból, Nyelvtanból, Történelemből vagy Matematikából!"}
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
        tiszta_vazlat = adat['vazlat'].replace('###', '').replace('**', '').replace('*', '').replace('$', '')
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
    st.caption("Astra AI Érettségi Felkészítő Központ (Irodalom | Nyelvtan | Történelem | Matematika)")
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
# FŐ TANTÁRGY VÁLASZTÓ (Irodalom vs. Nyelvtan vs. Történelem vs. Matek)
# =============================================================
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox(
    "Válassz tantárgyat:",
    [
        "📖 Magyar Irodalom (11 tétel)",
        "🔤 Magyar Nyelvtan (8 tétel)",
        "🏛️ Történelem (10 tétel)",
        "📐 Matematika (8 témakör)"
    ]
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
        "✍️ Esszé & Feladatmegoldó Labor",
        "🎭 Idézet- & Képlet-Detektív",
        "🧭 Történelmi & Irodalmi Idővonal",
        "🏆 Nagy Próbavizsga",
        "🤖 AI Érettségi Mentor"
    ]
)

# Adatbázis hozzárendelése a tantárgyhoz
if "Irodalom" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_irodalom
    tantargy_cimke = "Magyar Irodalom"
elif "Nyelvtan" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_nyelvtan
    tantargy_cimke = "Magyar Nyelvtan"
elif "Történelem" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_tortenelem
    tantargy_cimke = "Történelem"
else:
    aktiv_adatbazis = tetelek_matek
    tantargy_cimke = "Matematika"

# PDF Letöltés
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Letölthető tananyag")
if st.sidebar.button(f"📄 {tantargy_cimke} PDF Letöltése"):
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
    
    tab1, tab2, tab3 = st.tabs(["📚 Részletes tananyag és levezetés", "🎙️ 3 perces feleletvázlat / Képletgyűjtő", "⚡ Gyors teszt"])
    
    with tab1:
        st.markdown("<div class='deep-text'>", unsafe_allow_html=True)
        st.markdown(adat["vazlat"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='oral-box'>", unsafe_allow_html=True)
        st.markdown(adat["szobeli"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab3:
        st.subheader("Ellenőrizd a tudásod ebből a témakörből!")
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
# 2. MENÜPONT: HANGOSKÖNYV
# -------------------------------------------------------------
elif menupont == "🎧 Hangoskönyv (Monológ)":
    st.title(f"🎧 Hangoskönyv Felkészítő – {tantargy_cimke}")
    st.caption("Hallgasd meg a tételek teljes összefüggő szóbeli elemzését!")
    
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
        if st.button(f"▶️ Hangos összefoglaló indítása ({kivalasztott_hangos})"):
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
    st.caption("Pörgesd át a legfontosabb fogalmakat, évszámokat és képleteket mind a 4 tantárgyból!")
    
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
            {"role": "ai", "text": f"Jó napot kívánok! Húzza ki a tételét... Az Ön tétele: **{valasztott_szim_tetel}**. Kérem, kezdje meg a feleletét a bevezetéssel és a legfontosabb fogalmi alapokkal!"}
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
# 5. MENÜPONT: ESSZÉ & FELADATMEGOLDÓ LABOR
# -------------------------------------------------------------
elif menupont == "✍️ Esszé & Feladatmegoldó Labor":
    st.title("✍️ Esszé & Feladatmegoldó Labor")
    st.caption("Másold be az irodalmi/történelmi esszédet vagy egy nehéz matekfeladat szövegét – az AI kijavítja vagy levezeti a teljes megoldást!")
    
    diak_essze = st.text_area("Másold be a szöveget vagy matematikai feladatot:", height=220)
    
    if st.button("📊 Automatikus ellenőrzés / Megoldás levezetése"):
        if diak_essze:
            with st.spinner("Elemzés és számítás folyamatban..."):
                prompt = f"""
                Tapasztalt magyar középiskolai tanár és érettségi vizsgáztató vagy ({tantargy_cimke}).
                Elemezd / oldd meg az alábbi diákmunkát vagy feladatot:
                ---
                {diak_essze}
                ---
                Ha esszé (Irodalom, Történelem, Nyelvtan):
                - Értékeld a tartalmi pontosságot, forráshasználatot, szerkezetet és nyelvhelyességet.
                - Adj konkrét érettségi pontszámot és érdemjegyet (1-5).
                - Írj 2-3 javítási javaslatot!
                Ha Matematika feladat:
                - Add meg a pontos végeredményt!
                - Írd le a részletes, lépésről lépésre követhető levezetést és indoklást!
                """
                valasz = ai_generalas(prompt)
                st.markdown("<div class='deep-text'>", unsafe_allow_html=True)
                st.markdown(valasz)
                st.markdown("</div>", unsafe_allow_html=True)
                st.session_state.xp += 50
        else:
            st.info("Kérlek előbb másold be a szöveget a fenti mezőbe!")

# -------------------------------------------------------------
# 6. MENÜPONT: IDÉZET- ÉS KÉPLET-DETEKTÍV
# -------------------------------------------------------------
elif menupont == "🎭 Idézet- & Képlet-Detektív":
    st.title("🎭 Idézet- és Képlet-Detektív Játék")
    st.caption("Felismered a legfontosabb irodalmi sorokat, történelmi forrásokat és matematikai képleteket?")
    
    if 'game_idx' not in st.session_state:
        st.session_state.game_idx = 0
        
    feladvany = detektiv_adatbazis[st.session_state.game_idx]
    
    st.markdown(f"""
    <div class='topic-card' style='border-color:#ec4899; text-align:center;'>
        <h3 style='color:#f472b6; font-style:italic;'>{feladvany['idezet']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    valasztott_tipp = st.radio("Válaszd ki a helyes megfejtést:", feladvany['opciok'], key=f"detektiv_{st.session_state.game_idx}")
    
    if st.button("🔍 Tipp ellenőrzése"):
        if valasztott_tipp == feladvany['helyes']:
            st.balloons()
            st.session_state.xp += 30
            st.success(f"TÖKÉLETES! 🎉 Helyes válasz! (+30 XP)\n\n📌 Magyarázat: {feladvany['info']}")
        else:
            st.error(f"Sajnos nem! ❌ A helyes válasz: **{feladvany['helyes']}**\n\n📌 Magyarázat: {feladvany['info']}")
            
    if st.button("➡️ Következő feladvány"):
        st.session_state.game_idx = (st.session_state.game_idx + 1) % len(detektiv_adatbazis)
        st.rerun()

# -------------------------------------------------------------
# 7. MENÜPONT: TÖRTÉNELMI & IRODALMI IDŐVONAL
# -------------------------------------------------------------
elif menupont == "🧭 Történelmi & Irodalmi Idővonal":
    st.title("🧭 Történelmi & Művelődéstörténeti Idővonal (Timeline)")
    st.caption("Lásd át a magyar és világtörténelem, valamint az irodalom korszakait egyben!")
    
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
    st.write(f"Válaszold meg az összes {tantargy_cimke} kérdést a felkészültségi szinted ellenőrzéséhez!")
    
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
    st.caption("Kérdezz bármilyen Irodalmi, Nyelvtani, Történelmi vagy Matematikai témáról, levezetésről, fogalomról!")

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
            prompt = f"Tapasztalt magyar középiskolai érettségi felkészítő tanár vagy. Válaszolj tömören, pontosan és érthetően a diák kérdésére: {felh_kerdes}"
            ai_valasz = ai_generalas(prompt)
            st.session_state.chat_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 10
            st.rerun()
