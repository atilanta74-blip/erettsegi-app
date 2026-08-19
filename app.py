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

# Astra AI stílusú prémium sötét téma és javított kontrasztok
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    
    /* Gombok stílusa */
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
    
    /* Lenyitható dobozok (Expander) fejléce és szövege */
    div[data-testid="stExpander"] {
        background-color: #1f2937 !important;
        border: 1px solid #4b5563 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] details summary {
        background-color: #1e1b4b !important;
        color: #f3f4f6 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    div[data-testid="stExpander"] details summary p, div[data-testid="stExpander"] details summary span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpander"] details div[data-testid="stExpanderDetails"] {
        background-color: #111827 !important;
        color: #f3f4f6 !important;
        padding: 16px !important;
    }
    
    /* Szövegbeviteli mezők és lenyílók */
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
    
    /* Rádiógombok és címkék színe */
    div[data-testid="stRadio"] label p {
        color: #f3f4f6 !important;
        font-size: 1rem !important;
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
# 1. MAGYAR IRODALOM TÉTELTÁR (22 Tétel)
# -------------------------------------------------------------
tetelek_irodalom = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, nagykőrösi és margitszigeti korszak",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja", "A walesi bárdok"],
        "audio_szoveg": "Arany János a magyar irodalom legnagyobb balladaírója. A műfajt Greguss Ágost nyomán tragédia dalban elbeszélveként határozzuk meg...",
        "vazlat": "### I. Műfajelmélet: Líra, epika és dráma szintézise, balladai homály, ellipszis, sűrítés.\n### II. Nagykőrösi korszak: Történelmi ellenállás (A walesi bárdok, Szondi két apródja) és lélektan (Ágnes asszony lepedőmosása).\n### III. Őszikék (1877): Híd-avatás (nagyvárosi haláltánc).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. Nagykőrösi történelmi és lélektani balladák -> 3. Őszikék haláltánca -> 4. Összegzés.",
        "kviz": [{"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A három műnem találkozására utal."}]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus szintézise, polgári meghasonlás és a Senki szigete",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi", "Ali Csorbadzsi", "Krisztyán Tódor"],
        "audio_szoveg": "Jókai Mór 1872-es Az arany ember című regénye az író legszemélyesebb alkotása...",
        "vazlat": "### I. Műfaj: Romantikus mesei fordulatok és realista társadalomrajz.\n### II. Timár meghasonlása: Anyagi siker vs. belső boldogtalanság.\n### III. Kettős világ: Komárom (Timea hideg hálája) vs. Senki szigete (Noémi tiszta szerelme).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1872 kontextusa -> 2. Timár jelleme -> 3. Két világmodell -> 4. Balatoni feloldás.",
        "kviz": [{"k": "A Senki szigete pénzmentes természeti utópia a regényben.", "v": True, "m": "A társadalmi konvenciókon kívül áll."}]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény műfaja, eszmék küzdelme és az Úr zárszava",
        "kulcsszavak": ["Drámai költemény", "15 szín", "Ádám, Éva, Lucifer", "Párizs", "London"],
        "audio_szoveg": "Madách Imre Az ember tragédiája című drámai költeménye 1859-60-ban született...",
        "vazlat": "### I. Műfaj: Világdráma hegel-i dialektikával.\n### II. Karakterek: Ádám (hit és tett), Lucifer (hideg ráció), Éva (élet és érzelem).\n### III. Történelem: Párizs (Danton hite) és London (haláltánc). Zárszó: „Küzdj és bízva bízzál!”",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Műfaji sajátosságok -> 2. Szereplők hármassága -> 3. Párizsi és londoni szín -> 4. 15. szín katarzisa.",
        "kviz": [{"k": "Ádám a párizsi színből kiábrándultan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel tér magához."}]
    },
    "4. Mikszáth Kálmán prózája": {
        "alcim": "Anekdotizmus, A tót atyafiak, A jó palócok és a Beszterce ostroma",
        "kulcsszavak": ["Anekdota", "A tót atyafiak", "A jó palócok", "Beszterce ostroma", "Pongrácz István"],
        "audio_szoveg": "Mikszáth Kálmán a 19. és 20. század fordulójának legnagyobb magyar mesélője...",
        "vazlat": "### I. Stílus: Anekdotizmus, szelíd irónia.\n### II. Novellák: A tót atyafiak vs. A jó palócok.\n### III. Beszterce ostroma: Pongrácz István Don Quijote-i alakja.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Anekdotikus stílus -> 2. Két novelláskötet -> 3. Pongrácz István -> 4. Összegzés.",
        "kviz": [{"k": "Pongrácz István középkori lovagként rendezi be életét Nedec várában.", "v": True, "m": "Anakronisztikus figura."}]
    },
    "5. Vajda János költészete": {
        "alcim": "A lírai magány mítosza, a Gina-szerelem és a szimbolizmus előfutára",
        "kulcsszavak": ["Gina-versek", "Montblanc", "A vaáli erdőben", "A virrasztók"],
        "audio_szoveg": "Vajda János a kiegyezés korának legmagányosabb költője...",
        "vazlat": "### I. Magány és társadalmi kiábrándulás (A virrasztók).\n### II. Gina-líra: Húsz év múlva (Montblanc-metafora).\n### III. Csend-líra: A vaáli erdőben.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Gina-szerelem -> 3. A vaáli erdőben -> 4. Hatása Adyra.",
        "kviz": [{"k": "A Montblanc-metafora a Húsz év múlva című költemény központi képe.", "v": True, "m": "A fagyos hegy és a belső tűz képe."}]
    },
    "6. XIX. századi dráma: Ibsen és Csehov": {
        "alcim": "Az analitikus dráma (Nóra) és a csehovi hangulatdráma (Sirály, Cseresznyéskert)",
        "kulcsszavak": ["Henrik Ibsen", "Analitikus dráma", "Nóra", "Anton Csehov", "Sirály"],
        "audio_szoveg": "A 19. század végén Henrik Ibsen analitikus drámája és Anton Csehov hangulatdrámája forradalmasította a színházat...",
        "vazlat": "### I. Ibsen: Analitikus technika (Nóra).\n### II. Csehov: Hangulatdráma, cselekvésképtelenség (Sirály).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Polgári dráma megújulása -> 2. Ibsen analitikája -> 3. Csehov atmoszférája -> 4. Hatás.",
        "kviz": [{"k": "Ibsen darabjaiban a múltban rejtőző titkok robbantják ki a konfliktust.", "v": True, "m": "Ez az analitikus dramaturgia lényege."}]
    },
    "7. A Nyugat folyóirat": {
        "alcim": "A modern magyar irodalom indulása 1908-ban, szerkesztők és a 3 nemzedék",
        "kulcsszavak": ["1908", "Osvát Ernő", "Ignotus", "Mikes-emlékérem", "Három nemzedék"],
        "audio_szoveg": "1908. január 1-jén indult a Nyugat folyóirat...",
        "vazlat": "### I. Indulás: 1908–1941; Mikes-emlékérem.\n### II. Szerkesztők: Ignotus, Osvát Ernő, Hatvany Lajos.\n### III. Nemzedékek: 1. nemzedék (Ady, Babits), 2. nemzedék (Szabó Lőrinc), 3. nemzedék (Radnóti).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1908 jelentősége -> 2. Osvát Ernő -> 3. Három nemzedék -> 4. Kánonképző hatás.",
        "kviz": [{"k": "A Nyugat folyóirat 1908 és 1941 között működött.", "v": True, "m": "Babits haláláig állt fenn."}]
    },
    "8. Ady Endre költészete": {
        "alcim": "Szimbolizmus, magyarságtudat, lírai párharc és háborús apokalipszis",
        "kulcsszavak": ["Új versek 1906", "A magyar Ugaron", "Léda vs. Csinszka", "Harc a Nagyúrral"],
        "audio_szoveg": "Ady Endre 1906-os Új versek című kötetével megteremtette a modern magyar szimbolista költészetet...",
        "vazlat": "### I. 1906: Új versek (Góg és Magóg...).\n### II. Témák: Ugar-versek, Pénz-versek, Szerelem (Léda vs. Csinszka).\n### III. Háborús líra: Ember az embertelenségben.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1906 költői forradalma -> 2. Ugar és Disznófejű Nagyúr toposz -> 3. Léda és Csinszka -> 4. Háborús versek.",
        "kviz": [{"k": "Ady korszakalkotó kötete az Új versek 1906-ban jelent meg.", "v": True, "m": "Ez nyitotta meg a modern magyar lírát."}]
    },
    "9. Babits Mihály: Jónás könyve": {
        "alcim": "A prófétai szerep, a morális felelősségvállalás és a Jónás imája",
        "kulcsszavak": ["Jónás könyve", "Jónás imája", "Ninive", "Cinkos, aki néma", "1938"],
        "audio_szoveg": "Babits Mihály 1938-ban írta meg a Jónás könyvét a gégerákja és a fasizmus fenyegetése idején...",
        "vazlat": "### I. 1938: Babits betegsége és a fasizmus fenyegetése; bibliai parafrázis.\n### II. Jónás útja: Menekülés -> Cethal -> Ninive intése.\n### III. Alaptétel: „Mert vétkesek közt cinkos, aki néma.”",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1938 válsága -> 2. Jónás esendősége -> 3. Morális parancs -> 4. Jónás imája.",
        "kviz": [{"k": "A Jónás könyve központi szállóigéje: 'Mert vétkesek közt cinkos, aki néma'.", "v": True, "m": "A felelősségvállalás parancsa."}]
    },
    "10. Móricz Zsigmond prózája": {
        "alcim": "A paraszti és dzsentri világ naturalista és kritikai ábrázolása (Tragédia, Barbárok, Úri muri)",
        "kulcsszavak": ["Naturalizmus", "Tragédia", "Barbárok", "Úri muri", "Szakhmáry Zoltán"],
        "audio_szoveg": "Móricz Zsigmond szakított a hamis népi idillel, és a valóságot a maga kíméletlen ösztönvilágában mutatta be...",
        "vazlat": "### I. Stílus: Naturalizmus, biológiai ösztönök.\n### II. Novellák: Tragédia (Kis János evése), Barbárok (pusztai gyilkosság).\n### III. Dzsentri válság: Úri muri (Szakhmáry Zoltán).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szakítás a népiességgel -> 2. Kis János és Barbárok -> 3. Úri muri -> 4. Összegzés.",
        "kviz": [{"k": "A Tragédia című novellában Kis János a lakodalmi evésbe pusztul bele.", "v": True, "m": "A zsíros hús jelenti vesztét."}]
    },
    "11. Kosztolányi Dezső: Édes Anna": {
        "alcim": "A lélektani regény, a megalázottság tudattalan robbanása és a humanizmus",
        "kulcsszavak": ["Édes Anna", "Vizy család", "Moviszter doktor", "1919", "Freudizmus"],
        "audio_szoveg": "Kosztolányi Dezső 1926-os Édes Anna című regénye az elfojtott sérelmek kitörésének lélektani remekműve...",
        "vazlat": "### I. Történelem: 1919 nyara; Freud lélektana.\n### II. Anna dehumanizálása: Mintagépként kezelik -> Kettős gyilkosság.\n### III. Moviszter doktor: A tiszta humanizmus hangja.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1919 történelmi kerete -> 2. Anna tárgyiasítása -> 3. A gyilkosság lélektana -> 4. Moviszter üzenete.",
        "kviz": [{"k": "Moviszter doktor az egyetlen, aki emberi részvéttel tekint Annára.", "v": True, "m": "Ő képviseli az író értékrendjét."}]
    },
    "12. Petőfi Sándor forradalmi látomásköltészete": {
        "alcim": "A romantikus látomáslíra, a világforradalom és az önfeláldozás mítosza",
        "kulcsszavak": ["Egy gondolat bánt engemet...", "A XIX. század költői", "Világforradalom"],
        "audio_szoveg": "Petőfi Sándor költészetében a forradalmi látomáslíra a népszabadság küzdelmének legmagasabb szintézise...",
        "vazlat": "### I. Prófétai szerep: A XIX. század költői (a költő mint a nép vezére).\n### II. Halálmítosz: Egy gondolat bánt engemet... (önfeláldozás a csatamezőn).\n### III. Politikai líra: Nemzeti dal.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Petőfi forradalmi szerepe -> 2. A XIX. század költői -> 3. Egy gondolat bánt engemet -> 4. Nemzeti dal.",
        "kviz": [{"k": "Petőfi 'Egy gondolat bánt engemet...' című versében a lassú halált kívánja elkerülni.", "v": True, "m": "A csatamezőn kívánt elesni."}]
    },
    "13. József Attila kései gondolati lírája": {
        "alcim": "A létösszegzés, a magány és a társadalmi felelősségvállalás versei",
        "kulcsszavak": ["A Dunánál", "Eszmélet", "Téli éjszaka", "Kései sirató"],
        "audio_szoveg": "József Attila a 20. századi magyar költészet legmélyebb filozófiai gondolkodója...",
        "vazlat": "### I. Történelemfilozófia: A Dunánál (közép-európai megbékélés).\n### II. Lételmélet: Eszmélet (szabadság és determináció).\n### III. Önmegszólító líra: Karóval jöttél...",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Élethelyzet a 30-as években -> 2. A Dunánál megbékélése -> 3. Eszmélet -> 4. Kései önmegszólítás.",
        "kviz": [{"k": "A Dunánál a közép-európai népek megbékélését hirdeti.", "v": True, "m": "„Békévé oldja az emlékezés.”"}]
    },
    "14. Radnóti Miklós háborús ecloga-költészete": {
        "alcim": "A klasszicizáló forma mint a barbárság elleni menedék a bori noteszben",
        "kulcsszavak": ["Eclogák", "Bori notesz", "Hetedik ecloga", "Razglednicák"],
        "audio_szoveg": "Radnóti Miklós a második világháború borzalmai közepette a klasszikus antik forma fegyelmével őrizte meg a humánumot...",
        "vazlat": "### I. Antik forma: Vergiliusi hexameteres eclogák.\n### II. Lágerköltészet: Hetedik ecloga, Erőltetett menet.\n### III. Bori notesz: Razglednicák (a halálmenet stációi).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszicizálódás -> 2. Ecloga műfaj -> 3. Razglednicák -> 4. Humanizmus győzelme.",
        "kviz": [{"k": "Radnóti Miklós utolsó verseit a bori noteszben találták meg.", "v": True, "m": "A tömegsírból került elő."}]
    },
    "15. Vörösmarty Mihály: Csongor és Tünde és a Szózat": {
        "alcim": "A romantikus mesejáték filozófiája és a nemzeti identitás kiáltványa",
        "kulcsszavak": ["Csongor és Tünde", "Szózat (1836)", "Éj monológja"],
        "audio_szoveg": "Vörösmarty Mihály a magyar romantika vezéralakja...",
        "vazlat": "### I. Csongor és Tünde: Boldogságkeresés, Három vándor, Éj monológja.\n### II. Szózat (1836): A nemzet kiáltványa, hűség a hazához.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Romantika -> 2. Csongor és Tünde filozófiája -> 3. Éj monológja -> 4. Szózat.",
        "kviz": [{"k": "Az Éj monológja a világmindenség múlandóságát hirdeti.", "v": True, "m": "„Sötét és semmi voltam...”"}]
    },
    "16. Csokonai Vitéz Mihály felvilágosult lírája": {
        "alcim": "Stíluskettősség: klasszicizmus, rokokó és szentimentalizmus a Lilla-versekben",
        "kulcsszavak": ["A Reményhez", "A Magánossághoz", "Konstancinápoly", "Lilla-ciklus"],
        "audio_szoveg": "Csokonai Vitéz Mihály a magyar felvilágosodás legtehetségesebb poétája...",
        "vazlat": "### I. Filozofikus költészet: Konstancinápoly, Az estve.\n### II. Rokokó: Lilla-dalok.\n### III. Szentimentalizmus: A Reményhez, A Magánossághoz.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Felvilágosodás -> 2. Filozofikus versek -> 3. Lilla-líra -> 4. Stílusszintézis.",
        "kviz": [{"k": "A Reményhez a szentimentális kiábrándultság remeke.", "v": True, "m": "Búcsú a reménytől."}]
    },
    "17. Berzsenyi Dániel ódaköltészete": {
        "alcim": "A klasszicista forma és a romantikus életérzés feszültsége a niklai magányban",
        "kulcsszavak": ["A magyarokhoz I.", "A közelítő tél", "Nikla"],
        "audio_szoveg": "Berzsenyi Dániel a niklai remeteségből küldte el lángoló ódáit...",
        "vazlat": "### I. Nemzetféltő ódák: A magyarokhoz I. (tölgy-metafora).\n### II. Elégico-óda: A közelítő tél (elmúlás).\n### III. Horatiusi bölcselet: Osztályrészem.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszicista forma és romantikus lélek -> 2. A magyarokhoz I. -> 3. A közelítő tél -> 4. Nikla.",
        "kviz": [{"k": "A magyarokhoz I. című versben a tölgy a magyar nemzet szimbóluma.", "v": True, "m": "A belső erkölcsi pusztulás veszélyére int."}]
    },
    "18. Zrínyi Miklós: Szigeti veszedelem": {
        "alcim": "A barokk eposz sajátosságai, a mártíromság és az athleta Christi eszménye",
        "kulcsszavak": ["Barokk eposz", "Szigeti veszedelem (1651)", "Athleta Christi"],
        "audio_szoveg": "Zrínyi Miklós 1651-ben írta meg a Szigeti veszedelmet dédapja hősi haláláról...",
        "vazlat": "### I. Eposzi kellékek: Invocatio, Propositio, Csodás elemek.\n### II. Teológia: Isten büntetése a bűnökért a török hódítás.\n### III. Zrínyi: Athleta Christi vértanúsága.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Barokk eposz -> 2. Szigetvár ostroma -> 3. Athleta Christi -> 4. Üzenet.",
        "kviz": [{"k": "A Szigeti veszedelem 15 énekből álló barokk eposz.", "v": True, "m": "1651-ben íródott."}]
    },
    "19. Örkény István: Tóték és az egypercesek": {
        "alcim": "A groteszk és az abszurd ábrázolásmódja a 20. századi diktatúrák árnyékában",
        "kulcsszavak": ["Groteszk", "Tóték (1967)", "Őrnagy és Tót", "Dobozolás"],
        "audio_szoveg": "Örkény István a magyar groteszk próza megteremtője...",
        "vazlat": "### I. Groteszk: Félelmetes és nevetséges egyidejűsége.\n### II. Tóték (1967): Őrnagy terrorja, éjszakai dobozolás, margóvágós végkifejlet.\n### III. Egyperces novellák: Tömörség, abszurd látásmód.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Groteszk fogalma -> 2. Tóték és dobozolás -> 3. Margóvágó katarzisa -> 4. Egypercesek.",
        "kviz": [{"k": "Tót Lajos a mű végén a margóvágóval négy darabba vágja az Őrnagyot.", "v": True, "m": "Az abszurd lázadás végső aktusa."}]
    },
    "20. Ottlik Géza: Iskola a határon": {
        "alcim": "A létezésfilozófiai regény, a zárt katonaiskola világa és a szavak nélküli összetartozás",
        "kulcsszavak": ["Kőszegi katonaiskola", "Medve Gábor, Bébé", "Belső szabadság"],
        "audio_szoveg": "Ottlik Géza 1959-es regénye a zárt katonaiskola világát és a belső autonómia megőrzését mutatja be...",
        "vazlat": "### I. Elbeszélésmód: Bébé és Medve kéziratai.\n### II. Katonaiskola: Zárt rendszer és megaláztatások.\n### III. Túlélés: Szavak nélküli szolidaritás, belső szabadság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1959 Ottlik főműve -> 2. Katonaiskola világa -> 3. Bébé és Medve -> 4. Szavak elégtelensége.",
        "kviz": [{"k": "Az Iskola a határon a kőszegi katonai alreáliskolában játszódik.", "v": True, "m": "Zárt jellemfejlődési tér."}]
    },
    "21. Krúdy Gyula: Szindbád és a novellisztika": {
        "alcim": "Az impresszionista-szecessziós időszerkezet, az emlékek és az érzékek birodalma",
        "kulcsszavak": ["Szindbád-novellák", "Kulináris és szerelmi emlékek", "Időbontás"],
        "audio_szoveg": "Krúdy Gyula Szindbád-történeteiben az idő az emlékek és ízek hullámain lebeg...",
        "vazlat": "### I. Időkezelés: Szubjektív időélmény, múlt és jelen összefolyása.\n### II. Szindbád: Az örök utazó, kulináris és női emlékek gyűjtője.\n### III. Stílus: Impresszionizmus, szecesszió.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Krúdy egyedisége -> 2. Szindbád alakja -> 3. Időbontás és érzékek -> 4. Szecesszió.",
        "kviz": [{"k": "Krúdy Szindbád-történeteiben az időélmény szubjektív és emlékekre épül.", "v": True, "m": "A múlt és jelen összefolyik."}]
    },
    "22. Illyés Gyula: Egy mondat a zsarnokságról és a Puszták népe": {
        "alcim": "A szociográfiai próza és a totalitárius diktatúra lélektanának monumentális költeménye",
        "kulcsszavak": ["Egy mondat a zsarnokságról", "Puszták népe (1936)", "Diktatúra"],
        "audio_szoveg": "Illyés Gyula a magyar népi mozgalom vezéralakja volt...",
        "vazlat": "### I. Puszták népe (1936): Szociográfia a dunántúli cselédek nyomoráról.\n### II. Egy mondat a zsarnokságról (1950): Egyetlen monumentális körmondat a diktatúra mindent átható jelenlétéről.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Népi írók mozgalma -> 2. Puszták népe -> 3. Egy mondat a zsarnokságról -> 4. Hatás.",
        "kviz": [{"k": "Az 'Egy mondat a zsarnokságról' című vers egyetlen körmondatból épül fel.", "v": True, "m": "A diktatúra mindent befonó lényegét fejezi ki."}]
    }
}

# -------------------------------------------------------------
# 2. MAGYAR NYELVTAN TÉTELTÁR (16 Tétel)
# -------------------------------------------------------------
tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, kommunikációs funkciók",
        "kulcsszavak": ["Adó és Vevő", "Kód és Csatorna", "Jakobson modellje", "Metakommunikáció"],
        "audio_szoveg": "A kommunikáció információk, gondolatok és érzelmek átadása valamilyen jelrendszer segítségével...",
        "vazlat": "### I. Jakobson-modell: Adó, Vevő, Üzenet, Kód, Csatorna, Kontextus, Zaj.\n### II. Nyelvi funkciók: Tájékoztató, Érzelemkifejező, Felhívó, Fatikus, Metanyelvi, Poétikai.\n### III. Nem nyelvi kódok: Gesztusok, mimika, proxemika.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. 6 tényező -> 3. Funkciók -> 4. Nonverbális jelek.",
        "kviz": [{"k": "A fatikus funkció célja a kapcsolat felvétele és fenntartása.", "v": True, "m": "Ilyenek a köszönések és bejelentkezések."}]
    },
    "2. A szövegtan alapjai és a szövegtípusok": {
        "alcim": "A szöveg kohéziós erői, szerkezeti egységei és típusai",
        "kulcsszavak": ["Globális kohézió", "Lokális kohézió", "Anafora és Katafora", "Elbeszélő, leíró, érvelő"],
        "audio_szoveg": "A szöveg a nyelv legmagasabb szintű, lezárt, kerek egysége...",
        "vazlat": "### I. Kohézió: Lokális (kötőszók, anafora=visszautalás, katafora=előreutalás) vs. Globális (témamegtartás).\n### II. Szerkezet: Cím -> Bevezetés -> Tárgyalás -> Befejezés.\n### III. Típusok: Elbeszélő, leíró, érvelő, magyarázó.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szöveg fogalma -> 2. Kohéziós erők -> 3. Hármas szerkezet -> 4. Szövegtípusok.",
        "kviz": [{"k": "Az anafora a szövegben visszamutató utalást jelent.", "v": True, "m": "A katafora az előreutalás."}]
    },
    "3. A magyar helyesírás alapelvei": {
        "alcim": "A 4 alapelv rendszere és alkalmazásuk a gyakorlatban",
        "kulcsszavak": ["Kiejtés elve", "Szóelemzés elve", "Hagyomány elve", "Egyszerűsítés elve"],
        "audio_szoveg": "A magyar helyesírás négy alapelvre épül: kiejtés, szóelemzés, hagyomány és egyszerűsítés elve...",
        "vazlat": "### I. A 4 alapelv:\n1. Kiejtés elve (*asztal*).\n2. Szóelemzés elve (*látja, barátság*).\n3. Hagyomány elve (*Kossuth, király*).\n4. Egyszerűsítés elve (*asszony, tollal*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Helyesírás szerepe -> 2. Kiejtés és szóelemzés -> 3. Hagyomány és egyszerűsítés -> 4. Példák.",
        "kviz": [{"k": "A 'látja' szó leírása a szóelemzés elvét követi.", "v": True, "m": "A szótő és toldalék tisztán marad."}]
    },
    "4. Szófajok és mondatrészek rendszere": {
        "alcim": "Alapszófajok, viszonyszók, predikatív viszony és mondattani elemzés",
        "kulcsszavak": ["Ige, Névszó, Igenév", "Viszonyszók", "Alany, Állítmány, Tárgy, Határozó, Jelző"],
        "audio_szoveg": "A szófajok a szavak alaktani és mondattani kategóriái...",
        "vazlat": "### I. Szófajok: Alapszófajok (ige, névszók, igenevek), Viszonyszók (névelő, kötőszó, névutó), Mondatszók.\n### II. Mondatrészek: Alany + Állítmány -> Bővítmények: Tárgy, Határozók, Jelzők.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szófaji felosztás -> 2. Alapszófaj vs. viszonyszó -> 3. Mondatrészek hierarchiája.",
        "kviz": [{"k": "A kötőszók az alapszófajok közé tartoznak.", "v": False, "m": "A viszonyszókhoz tartoznak."}]
    },
    "5. Retorika és érvelési technikák": {
        "alcim": "Az érv 3 része, érvtípusok és a klasszikus szónoki beszéd 6 lépése",
        "kulcsszavak": ["Tétel, Bizonyíték, Összekötés", "Szónoki beszéd szerkezete", "Érvtípusok"],
        "audio_szoveg": "A retorika az ékesszólás és meggyőzés művészete...",
        "vazlat": "### I. Érv: Tétel -> Bizonyíték -> Összekötő elem.\n### II. Típusok: Meghatározásból levezetett, ok-okozati, tekintélyre hivatkozó, analógiás.\n### III. Szónoki beszéd: Exordium -> Narratio -> Divisio -> Confirmatio -> Refutatio -> Peroratio.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Retorika célja -> 2. Érv 3 része -> 3. Érvtípusok -> 4. Szónoki beszéd lépései.",
        "kviz": [{"k": "A klasszikus szónoki beszédben a cáfolás megelőzi a befejezést.", "v": True, "m": "A bizonyítás után jön a cáfolat."}]
    },
    "6. Stilisztika: Alakzatok és trópusok": {
        "alcim": "Költői képek (metafora, metonímia, szinesztézia) és szövegalakzatok",
        "kulcsszavak": ["Metafora, Metonímia, Szinekdoché", "Szinesztézia", "Anafora, Párhuzam, Ellentét"],
        "audio_szoveg": "A stilisztika a kifejezőeszközöket vizsgálja...",
        "vazlat": "### I. Trópusok: Metafora (hasonlóság), Metonímia (érintkezés), Szinekdoché (rész-egész), Szinesztézia (érzékkeverés).\n### II. Alakzatok: Anafora (sor eleji ismétlés), Paralelizmus, Antitézis, Hiperbola.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trópusok vs. alakzatok -> 2. Metafora és metonímia -> 3. Szinesztézia -> 4. Alakzatok.",
        "kviz": [{"k": "A 'sötét csend' szinesztézia.", "v": True, "m": "Látás és hallás összekapcsolása."}]
    },
    "7. A szókészlet rétegződése és változása": {
        "alcim": "Nyelvjárások, társadalmi rétegnyelvek, szleng, archaizmusok és neologizmusok",
        "kulcsszavak": ["Nyelvjárások", "Szaknyelv, Szleng, Argó", "Archaizmus", "Neologizmus"],
        "audio_szoveg": "A szókészlet területi és társadalmi tagolódást mutat...",
        "vazlat": "### I. Területi: Nyelvjárások (dialektusok) és tájszavak.\n### II. Társadalmi: Szaknyelv, szleng, argó.\n### III. Időbeli: Archaizmusok (régies szavak) vs. Neologizmusok (új szavak).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Területi tagolódás -> 2. Társadalmi rétegek -> 3. Időbeli mozgás.",
        "kviz": [{"k": "Az archaizmusok új szavakat jelentenek.", "v": False, "m": "Az archaizmusok a régies szavak."}]
    },
    "8. A magyar nyelv története és a nyelvújítás": {
        "alcim": "A finnugor rokonság, a korai nyelvemlékek és Kazinczy nyelvújítása",
        "kulcsszavak": ["Uráli / Finnugor nyelvcsalád", "Halotti Beszéd (1195)", "Nyelvújítás", "Kazinczy Ferenc"],
        "audio_szoveg": "A magyar nyelv a finnugor nyelvcsalád tagja...",
        "vazlat": "### I. Eredet: Finnugor nyelvcsalád; Tihanyi alapítólevél (1055), Halotti Beszéd (1195).\n### II. Nyelvújítás (1790–1820): Kazinczy Ferenc; Neológusok vs. Ortológusok; új szavak alkotása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Finnugor rokonság -> 2. Korai nyelvemlékek -> 3. Nyelvújítás célja és Kazinczy szerepe.",
        "kviz": [{"k": "A Halotti Beszéd az első fennmaradt összefüggő magyar szövegemlék.", "v": True, "m": "1195 körül keletkezett."}]
    },
    "9. Fonetika: A hangok képzése és a mássalhangzótörvények": {
        "alcim": "Magánhangzók és mássalhangzók rendszere, hasonulás, összeolvadás, kiesés és rövidülés",
        "kulcsszavak": ["Zöngés és Zöngétlen", "Részleges és Teljes hasonulás", "Összeolvadás"],
        "audio_szoveg": "A fonetika a beszédhangok képzését és egymásra hatását vizsgálja...",
        "vazlat": "### I. Hangrendszer: Magánhangzók és mássalhangzók rendszere.\n### II. Mássalhangzótörvények: Részleges hasonulás (vasgolyó [vazsgolyó]), Teljes hasonulás (kézzel, anyja [annya]), Összeolvadás (barátság [baraccság]), Kiesés (mondta [monta]), Rövidülés (otthon [othon]).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hangok képzése -> 2. Zöngésségi hasonulás -> 3. Teljes hasonulás és összeolvadás -> 4. Helyesírás.",
        "kviz": [{"k": "A 'színpad' szóban a képzés helye szerinti részleges hasonulás érvényesül.", "v": True, "m": "Kiejtve [szímpad]."}]
    },
    "10. Morfológia: A szóelemek (morfémák) rendszere": {
        "alcim": "Tőmorfémák, toldalékmorfémák (képző, jel, rag) és a szóelemző helyesírás",
        "kulcsszavak": ["Szótő", "Képző", "Jel", "Rag", "Toldalékolási sorrend"],
        "audio_szoveg": "A morfológia a nyelv legkisebb jelentéssel bíró egységeit, a morfémákat vizsgálja...",
        "vazlat": "### I. Morfématípusok: Tőmorféma és Toldalékmorféma.\n### II. Toldalékolási sorrend: Szótő + KÉPZŐ + JEL + RAG (pl. *ház-as-ság-ok-at*).\n### III. Funkciók: Képző (új szó), Jel (viszony, többesszám), Rag (mondatrészi szerep, lezárja a szót).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Morféma fogalma -> 2. Képző, jel, rag szerepe -> 3. Kötött sorrend -> 4. Példaelemzés.",
        "kviz": [{"k": "A rag után még kapcsolódhat képző a szóhoz.", "v": False, "m": "A rag mindig lezárja a szót."}]
    },
    "11. Szóalkotási módok a magyar nyelvben": {
        "alcim": "Szóösszetétel, szóképzés, mozaikszók, szóelvonás, szóvegyülés és rövidülés",
        "kulcsszavak": ["Szóösszetétel", "Szóképzés", "Mozaikszók (Betűszó és Szóösszevonás)"],
        "audio_szoveg": "A magyar nyelv gazdag belső szóalkotási módokkal rendelkezik...",
        "vazlat": "### I. Fő módok: Szóképzés, Szóösszetétel.\n### II. Ritkább módok: Mozaikszók (Betűszó: *MÁV*, Szóösszevonás: *Főgáz*), Szóelvonás (*kapa <- kapál*), Szóvegyülés (*csokréta*), Szócsonkítás (*mozi*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szóteremtés fontossága -> 2. Képzés és összetétel -> 3. Mozaikszók -> 4. Ritkább módok.",
        "kviz": [{"k": "A 'MÁV' betűszó, a 'Főgáz' szóösszevonás.", "v": True, "m": "A betűszó kezdőbetűkből, a szóösszevonás szótagokból áll."}]
    },
    "12. Mondattan: Az összetett mondatok típusai": {
        "alcim": "Mellérendelő (kapcsolatos, ellentétes, választó, következtető, magyarázó) és alárendelő mondatok",
        "kulcsszavak": ["Mellérendelés", "Alárendelés", "Utalószó és Kötőszó"],
        "audio_szoveg": "Az összetett mondatok két vagy több tagmondat kapcsolatából állnak...",
        "vazlat": "### I. Mellérendelő típusok: Kapcsolatos (*és*), Ellentétes (*de*), Választó (*vagy*), Következtető (*ezért*), Magyarázó (*hiszen*).\n### II. Alárendelő típusok: Főmondat + hiányzó mondatrészt kifejtő mellékmondat.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Összetett mondat fogalma -> 2. 5 mellérendelő típus -> 3. Alárendelés rendszere -> 4. Elemzés.",
        "kviz": [{"k": "A 'Szakad az eső, ezért nem megyünk el' következtető mellérendelés.", "v": True, "m": "Az 'ezért' következtetést fejez ki."}]
    },
    "13. Stílusrétegek és a stílusérték": {
        "alcim": "Hivatalos, tudományos, publicisztikai, társalgási és szépirodalmi stílus",
        "kulcsszavak": ["Stílusrétegek", "Denotatív és Konnotatív", "Terminológia"],
        "audio_szoveg": "A stílus a nyelvi eszközök céltudatos kiválasztása a beszédhelyzetnek megfelelően...",
        "vazlat": "### I. Stílusrétegek: Hivatalos, Tudományos, Publicisztikai, Társalgási, Szépirodalmi.\n### II. Jelentés: Denotáció (alapjelentés) vs. Konnotáció (másodlagos hangulat).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Stílus fogalma -> 2. Stílusrétegek bemutatása -> 3. Denotatív vs. konnotatív jelentés -> 4. Helyes használat.",
        "kviz": [{"k": "A hivatalos stílust a szárazság és a sablonosság jellemzi.", "v": True, "m": "Pontosságra törekszik."}]
    },
    "14. Névtan (Onomasztika)": {
        "alcim": "Személynevek és földrajzi nevek rendszere, eredete",
        "kulcsszavak": ["Családnevek típusai", "Földrajzi nevek helyesírása", "Keresztnevek"],
        "audio_szoveg": "A névtan a tulajdonnevek eredetét és típusait kutató nyelvtudomány...",
        "vazlat": "### I. Családnevek 5 fő eredete: Apai név (*Péterfi*), Származási hely (*Budai*), Foglalkozás (*Kovács*), Tulajdonság (*Nagy*), Etnikum (*Tóth*).\n### II. Földrajzi nevek: Egyelemű (*Duna*), Kételemű egybeírt (*Margitsziget*), Különírt (*Fekete-tenger*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Névtan célja -> 2. Családnevek 5 típusa -> 3. Keresztnevek -> 4. Földrajzi nevek.",
        "kviz": [{"k": "A 'Kovács' családnév foglalkozásra utal.", "v": True, "m": "Mesterségről elnevezett név."}]
    },
    "15. Frazeológia: Szólások, közmondások és szállóigék": {
        "alcim": "Állandósult szókapcsolatok fajtái és metaforikus jelentése",
        "kulcsszavak": ["Szólás", "Közmondás", "Szállóige", "Közhely"],
        "audio_szoveg": "A frazeológia a nyelv állandósult, kötött szókapcsolatait tanulmányozza...",
        "vazlat": "### I. Szólás: Képszerű kifejezés mondatérték nélkül (*feni a fogát*).\n### II. Közmondás: Kerek egész mondat népi tanulsággal (*Nem mind arany, ami fénylik*).\n### III. Szállóige: Ismert szerzőhöz/műhöz köthető aranyköpés (*A kocka el van vetve*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kötött szókapcsolatok -> 2. Szólás vs. közmondás -> 3. Szállóigék -> 4. Kulturális kincs.",
        "kviz": [{"k": "A 'Nem mind arany, ami fénylik' közmondás.", "v": True, "m": "Kerek mondat tanulsággal."}]
    },
    "16. Digitális kommunikáció és az infokommunikációs nyelv": {
        "alcim": "Az online nyelvhasználat, emotikonok, hipertext és a közösségi média hatása",
        "kulcsszavak": ["Netnyelv", "Hipertext", "Multimodalitás", "Emoji", "Írott beszéltség"],
        "audio_szoveg": "A digitális forradalom gyökeresen átalakította mindennapi nyelvhasználatunkat...",
        "vazlat": "### I. Netnyelv: Írott beszéltség (írásbeli és szóbeli lazaság fúziója), rövidítések.\n### II. Multimodalitás és Emojik: Képi jelek mint a hiányzó metakommunikáció pótlói.\n### III. Nyelvművelés: Hatások a nyelvre.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Digitális nyelvhasználat -> 2. Írott beszéltség -> 3. Emojik szerepe -> 4. Nyelvi hatások.",
        "kviz": [{"k": "A digitális kommunikációban az írott beszéltség jelensége figyelhető meg.", "v": True, "m": "Az írás és szóbeliség keveréke."}]
    }
}

# -------------------------------------------------------------
# 3. TÖRTÉNELEM TÉTELTÁR (30 Tétel)
# -------------------------------------------------------------
tetelek_tortenelem = {
    "1. Az athéni demokrácia működése a Kr. e. V. században": {
        "alcim": "Szolón, Kleiszthenész reformjai, Periklész kora és a népgyűlés (ekklészia)",
        "kulcsszavak": ["Népgyűlés (Ekklészia)", "Cserépszavazás", "Sztratégosz", "Napidíj", "Periklész"],
        "audio_szoveg": "Az athéni demokrácia az ókori világ legfejlettebb népuralmi rendszere volt...",
        "vazlat": "### I. Fejlődés: Szolón -> Kleiszthenész (10 phülé, cserépszavazás).\n### II. Periklész kora: Népgyűlés (Ekklészia), Bulé, Sztratégoszok, napidíjak.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kialakulás -> 2. Intézményrendszer -> 3. Napidíjak.",
        "kviz": [{"k": "Az athéni népgyűlés tagja lehetett minden szabad athéni férfi polgár.", "v": True, "m": "Közvetlen demokrácia volt."}]
    },
    "2. A Római Köztársaság válsága és a Principátus kialakulása": {
        "alcim": "A polgárháborúk kora, Caesar diktatúrája és Augustus principátusa",
        "kulcsszavak": ["Gracchusok", "Marius", "Julius Caesar", "Augustus", "Pax Romana"],
        "audio_szoveg": "A Római Köztársaság a hódítások következtében mély válságba került...",
        "vazlat": "### I. Válság: Parasztság tönkremenetele, rabszolgafelkelések.\n### II. Caesar és Augustus principátusa (Kr. e. 27), Pax Romana.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Válság okai -> 2. Caesar -> 3. Augustus.",
        "kviz": [{"k": "Augustus megtartotta a köztársasági intézményeket.", "v": True, "m": "Princepsként uralkodott."}]
    },
    "3. A kereszténység születése és elterjedése az ókorban": {
        "alcim": "Jézus tanításai, az őskeresztény gyülekezetek és a milánói ediktum (313)",
        "kulcsszavak": ["Názáreti Jézus", "Szent Pál", "Milánói ediktum (313)", "Nicaea"],
        "audio_szoveg": "A kereszténység a Római Birodalom keleti tartományában indult ki...",
        "vazlat": "### I. Tanítások: Szeretet, megváltás.\n### II. Milánói ediktum (313): Constantinus engedélyezi a vallást.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Jézus -> 2. Pál apostol -> 3. Milánói ediktum.",
        "kviz": [{"k": "313-ban a milánói ediktummal engedélyezték a kereszténységet.", "v": True, "m": "Constantinus császár tette."}]
    },
    "4. A középkori uradalom és a hűbériség rendszere": {
        "alcim": "Hűbéri lánc (feudalizmus), a jobbágyság és a háromnyomásos gazdálkodás",
        "kulcsszavak": ["Senior és Vazallus", "Feudum", "Majorság", "Háromnyomásos gazdálkodás"],
        "audio_szoveg": "A középkori Európa társadalmi és gazdasági rendszere a hűbériségen alapult...",
        "vazlat": "### I. Hűbériség: Földért katonai szolgálat.\n### II. Uradalom: Majorság, jobbágytelek, robot.\n### III. Technika: Háromnyomásos gazdálkodás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Feudalizmus -> 2. Uradalom -> 3. Technika.",
        "kviz": [{"k": "A háromnyomásos gazdálkodásban a föld 1/3-a pihent.", "v": True, "m": "Az ugar."}]
    },
    "5. Az Iszlám vallás születése és az arab-iszlám világ expanziója": {
        "alcim": "Mohamed próféta, a Korán, az iszlám öt oszlopa és a kalifátusok terjeszkedése",
        "kulcsszavak": ["Mohamed", "Hegidzsra (622)", "Korán", "Öt oszlop", "Kalifátus"],
        "audio_szoveg": "Az iszlám vallás a 7. század elején született meg az Arab-félszigeten...",
        "vazlat": "### I. Alapítás: Mohamed, 622 hegidzsra.\n### II. Öt oszlop: Hitvallás, ima, adakozás, böjt, zarándoklat.\n### III. Kalifátusok hódításai.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mohamed -> 2. 5 oszlop -> 3. Hódítások.",
        "kviz": [{"k": "Az iszlám időszámítás kezdete 622.", "v": True, "m": "A hegizsra éve."}]
    },
    "6. Szent István államalapítása és az egyházszervezés": {
        "alcim": "A keresztény királyság megszilárdítása, vármegyerendszer és törvények",
        "kulcsszavak": ["Koppány", "Koronázás (1000)", "10 egyházmegye", "Ispánok", "Tized"],
        "audio_szoveg": "Géza fejedelem után fia, István király 1000 karácsonyán felvette a koronát...",
        "vazlat": "### I. Koppány legyőzése -> Koronázás (1000/1001).\n### II. Egyház: 10 püspökség, tized.\n### III. Vármegyerendszer, ispánok.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Koronázás -> 2. Egyház -> 3. Vármegyék.",
        "kviz": [{"k": "Szent István 10 püspökséget alapított.", "v": True, "m": "Esztergom és Kalocsa érsekség lett."}]
    },
    "7. Az Aranybulla és a rendi társadalom gyökerei (1222)": {
        "alcim": "II. András birtokpolitikája, a szerviensek mozgalma és a nemesi jogok rögzítése",
        "kulcsszavak": ["1222 Aranybulla", "Szerviensek", "Adómentesség", "Ellenállási záradék"],
        "audio_szoveg": "II. András adományai miatt a szerviensek kikényszerítették az Aranybullát...",
        "vazlat": "### I. Aranybulla (1222): Adómentesség, bírói ítélet védelme.\n### II. 31. cikkely: Ellenállási záradék (ius resistendi).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Előzmény -> 2. Aranybulla -> 3. Ellenállási záradék.",
        "kviz": [{"k": "Az Aranybulla 31. cikkelye tartalmazta az ellenállási záradékot.", "v": True, "m": "Jog a király ellen."}]
    },
    "8. Az Anjouk kora Magyarországon": {
        "alcim": "Károly Róbert gazdasági reformjai és Nagy Lajos 1351-es törvényei",
        "kulcsszavak": ["Bányabér (Urbura)", "Aranyforint", "Kapuadó", "1351 Ősiség és Kilenced"],
        "audio_szoveg": "Károly Róbert legyőzte a tartományurakat és gazdasági reformokat hozott...",
        "vazlat": "### I. Károly Róbert: Urbura, aranyforint, kapuadó, 1335 Visegrád.\n### II. Nagy Lajos (1351): Ősiség, Kilenced.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Károly Róbert -> 2. Visegrád -> 3. Nagy Lajos.",
        "kviz": [{"k": "Az 1351-es ősiség törvénye védte a nemesi birtokot.", "v": True, "m": "Nem lehetett eladni."}]
    },
    "9. Hunyadi Mátyás uralkodása (1458–1490)": {
        "alcim": "Központosított monarchia, bevételek, Fekete sereg és a reneszánsz udvar",
        "kulcsszavak": ["Füstpénz", "Rendkívüli hadiadó", "Fekete sereg", "Corvinák", "Bécs bevétele"],
        "audio_szoveg": "Hunyadi Mátyás erős központosított királyi hatalmat épített ki...",
        "vazlat": "### I. Bevételek: Füstpénz, rendkívüli hadiadó.\n### II. Fekete sereg, Bécs elfoglalása (1485).\n### III. Reneszánsz: Corvinák.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevételek -> 2. Fekete sereg -> 3. Reneszánsz.",
        "kviz": [{"k": "Mátyás füstpénzt vezetett be a kapuadó helyett.", "v": True, "m": "Háztartásonként szedték."}]
    },
    "10. A mohácsi csata és az ország három részre szakadása (1526–1541)": {
        "alcim": "A Jagelló-kor gyengesége, Mohács tragédiája, kettős királyválasztás és Buda eleste",
        "kulcsszavak": ["1526 Mohács", "Szapolyai és Ferdinánd", "1541 Buda eleste", "Három országrész"],
        "audio_szoveg": "1526. augusztus 29-én a mohácsi síkon megsemmisült a magyar haderő...",
        "vazlat": "### I. Mohács (1526) -> II. Kettős királyválasztás -> III. Buda eleste (1541): 3 részre szakadás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mohács -> 2. Kettős királyság -> 3. Buda eleste.",
        "kviz": [{"k": "Buda 1541-es elfoglalásával szakadt három részre az ország.", "v": True, "m": "Szulejmán csellel vette be."}]
    },
    "11. A Rákóczi-szabadságharc (1703–1711)": {
        "alcim": "A Habsburg abszolutizmus elleni felkelés, az ónodi trónfosztás és a szatmári béke",
        "kulcsszavak": ["Brezáni kiáltvány", "Kurucok", "Ónod (1707)", "Szatmári béke (1711)"],
        "audio_szoveg": "II. Rákóczi Ferenc vezetésével bontakozott ki a függetlenségi háború...",
        "vazlat": "### I. Brezáni kiáltvány (1703) -> II. 1707 Ónodi trónfosztás -> III. 1711 Szatmári béke.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kezdet -> 2. Ónod -> 3. Szatmár.",
        "kviz": [{"k": "1707-ben mondták ki az ónodi országgyűlésen a trónfosztást.", "v": True, "m": "Habsburg-ház elűzése."}]
    },
    "12. A felvilágosult abszolutizmus Magyarországon": {
        "alcim": "Mária Terézia és II. József rendeletei (Védővám, Urbárium, Ratio Educationis, Türelmi rendelet)",
        "kulcsszavak": ["Mária Terézia", "Urbárium (1767)", "II. József", "Türelmi rendelet (1781)"],
        "audio_szoveg": "A 18. században a Habsburg uralkodók rendeleti úton modernizáltak...",
        "vazlat": "### I. Mária Terézia: Vámrendelet, Urbárium, Ratio Educationis.\n### II. II. József: Türelmi rendelet, Jobbágyrendelet.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mária Terézia -> 2. II. József reformjai.",
        "kviz": [{"k": "II. József a kalapos király nevet kapta.", "v": True, "m": "Nem koronáztatta meg magát."}]
    },
    "13. A reformkor fő kérdései (1830–1848)": {
        "alcim": "Széchenyi István és Kossuth Lajos reformprogramjának összehasonlítása",
        "kulcsszavak": ["Hitel (1830)", "Örökváltság", "Közteherviselés", "Pesti Hírlap"],
        "audio_szoveg": "A magyar reformkor Széchenyi Hitel című művével indult...",
        "vazlat": "### I. Széchenyi: Hitel, gazdasági modernizáció.\n### II. Kossuth: Kötelező örökváltság, közteherviselés, sajtószabadság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Széchenyi -> 2. Kossuth -> 3. Vita.",
        "kviz": [{"k": "Kossuth a kötelező örökváltságot követelte állami kárpótlással.", "v": True, "m": "Jobbágyfelszabadítás."}]
    },
    "14. Az 1848–49-es forradalom és szabadságharc": {
        "alcim": "Március 15., az Áprilisi törvények és a Tavaszi hadjárat sikerei",
        "kulcsszavak": ["12 pont", "Áprilisi törvények", "Batthyány Lajos", "Görgei", "Trónfosztás (1849)"],
        "audio_szoveg": "1848 tavaszán a pesti forradalom polgári Magyarországot teremtett...",
        "vazlat": "### I. Március 15., Áprilisi törvények -> II. Tavaszi hadjárat (1849) -> III. Világos.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Forradalom -> 2. Tavaszi hadjárat -> 3. Bukás.",
        "kviz": [{"k": "A Batthyány-kormány volt az első független felelős magyar kormány.", "v": True, "m": "1848 április."}]
    },
    "15. A dualizmus kora Magyarországon (1867–1914)": {
        "alcim": "A Kiegyezés rendszere, gazdasági felvirágzás és társadalmi rétegződés",
        "kulcsszavak": ["Kiegyezés (1867)", "Közös ügyek", "Gazdasági csoda", "Torlódó társadalom"],
        "audio_szoveg": "Az 1867-es kiegyezéssel létrejött az Osztrák-Magyar Monarchia...",
        "vazlat": "### I. Közös ügyek -> II. Gazdasági robbanás (vasút, malomipar) -> III. Torlódó társadalom.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kiegyezés -> 2. Gazdaság -> 3. Társadalom.",
        "kviz": [{"k": "A dualizmus korában a külügy és hadügy közös volt.", "v": True, "m": "Közös ügyek."}]
    },
    "16. Az első világháború és következményei (1914–1918)": {
        "alcim": "A szövetségi rendszerek, az állóháború jellege és a hátország összeomlása",
        "kulcsszavak": ["Szarajevó (1914)", "Antant", "Állóháború", "Trianon (1920)"],
        "audio_szoveg": "Az 1914-es merénylet kirobbantotta a Nagy Háborút...",
        "vazlat": "### I. Állóháború a lövészárkokban -> II. 1918 összeomlás -> III. 1920 Trianon.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Okok -> 2. Hadviselés -> 3. Trianon.",
        "kviz": [{"k": "Az I. világháborúban az USA 1917-ben lépett be.", "v": True, "m": "Antant oldalán."}]
    },
    "17. A Horthy-korszak konszolidációja (1920–1931)": {
        "alcim": "Trianon traumája, a bethleni konszolidáció és Klebelsberg kultúrpolitikája",
        "kulcsszavak": ["Trianon", "Bethlen István", "Pengő (1927)", "Klebelsberg Kuno"],
        "audio_szoveg": "Trianon után Bethlen István vezetésével stabilizálódott az ország...",
        "vazlat": "### I. Bethleni konszolidáció (Pengő, kölcsön) -> II. Klebelsberg iskolaépítése.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trianon -> 2. Bethlen -> 3. Klebelsberg.",
        "kviz": [{"k": "1927-ben vezették be a Pengőt.", "v": True, "m": "Stabil valuta lett."}]
    },
    "18. A második világháború főbb fordulópontjai (1939–1945)": {
        "alcim": "A náci agresszió, a szövetségesek koalíciója, Sztálingrád, D-nap és a holokauszt",
        "kulcsszavak": ["1939 Lengyelország", "Sztálingrád", "D-nap (1944)", "Holokauszt"],
        "audio_szoveg": "1939-ben kitört a II. világháború...",
        "vazlat": "### I. Sztálingrádi fordulat -> II. Normandiai partraszállás -> III. Holokauszt.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kitörés -> 2. Sztálingrád -> 3. Holokauszt.",
        "kviz": [{"k": "A sztálingrádi csata a II. vh döntő fordulata volt.", "v": True, "m": "Keleti front."}]
    },
    "19. Magyarország a második világháborúban (1941–1945)": {
        "alcim": "Revíziós sikerek, belépés a háborúba, a doni katasztrófa, a német megszállás és a nyilas terror",
        "kulcsszavak": ["Bécsi döntések", "Don-kanyar (1943)", "1944. március 19.", "Nyilas terror"],
        "audio_szoveg": "Magyarország a revízió áraként sodródott a háborúba...",
        "vazlat": "### I. Doni katasztrófa -> II. 1944 német megszállás -> III. Nyilas terror.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hadbalépés -> 2. Don-kanyar -> 3. Megszállás.",
        "kviz": [{"k": "A 2. magyar hadsereg 1943-ban a Donnál pusztult el.", "v": True, "m": "Tragikus vereség."}]
    },
    "20. A hidegháború kialakulása és korszakai (1945–1991)": {
        "alcim": "Kétpólusú világ, fegyverkezési verseny, Truman-doktrína, kubai rakétaválság és szovjet összeomlás",
        "kulcsszavak": ["Vasfüggöny", "NATO és Varsói Szerződés", "Kubai válság (1962)", "Gorbacsov"],
        "audio_szoveg": "A II. vh után a világ két szuperhatalmi blokkra szakadt...",
        "vazlat": "### I. NATO és Varsói Szerződés -> II. Kubai válság -> III. Szovjetunió felbomlása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kétpólusú világ -> 2. Válságok -> 3. Összeomlás.",
        "kviz": [{"k": "1962-ben volt a kubai rakétaválság.", "v": True, "m": "Atomháború veszélye."}]
    },
    "21. Az 1956-os magyar forradalom és szabadságharc": {
        "alcim": "A Rákosi-diktatúra válsága, október 23., Nagy Imre kormánya és a szovjet intervenció",
        "kulcsszavak": ["Október 23.", "Nagy Imre", "Semlegesség", "November 4. Szovjet invázió"],
        "audio_szoveg": "1956. október 23-án indult a forradalom a szovjet elnyomás ellen...",
        "vazlat": "### I. Október 23. -> II. Nagy Imre kormánya, semlegesség -> III. Nov. 4. szovjet támadás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Előzmény -> 2. Forradalom napjai -> 3. Leverés.",
        "kviz": [{"k": "1956. november 4-én indult meg a szovjet invázió.", "v": True, "m": "Forgószél hadművelet."}]
    },
    "22. A Kádár-rendszer korszaka és a „gulyáskommunizmus”": {
        "alcim": "Az 1956 utáni konszolidáció, a Kádár-féle politika és az életszínvonal-politika",
        "kulcsszavak": ["Konszolidáció", "„Aki nincs ellenünk, az velünk van”", "Gulyáskommunizmus"],
        "audio_szoveg": "1956 után Kádár János nevéhez fűződik a gulyáskommunizmus korszaka...",
        "vazlat": "### I. Kádári alku (csendes befelé fordulásért anyagi jólét) -> II. Gulyáskommunizmus.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Konszolidáció -> 2. Életszínvonal-politika.",
        "kviz": [{"k": "A Kádár-korszakban a szlogen így szólt: 'Aki nincs ellenünk, az velünk van'.", "v": True, "m": "Enyhítés."}]
    },
    "23. A békés rendszerváltás Magyarországon (1989–1990)": {
        "alcim": "A Kádár-rendszer válsága, az Ellenzéki Kerekasztal, Nagy Imre újratemetése és a szabad választások",
        "kulcsszavak": ["Ellenzéki Kerekasztal", "1989. jún. 16. Újratemetés", "1989. okt. 23. Köztársaság"],
        "audio_szoveg": "1989-1990-ben békés tárgyalások útján alakult át a diktatúra...",
        "vazlat": "### I. EKA -> II. 1989 újratemetés és határnyitás -> III. 1990 szabad választások.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Ellenzék -> 2. 1989 eseményei -> 3. Választások.",
        "kviz": [{"k": "1989. október 23-án kiáltották ki a köztársaságot.", "v": True, "m": "Szűrös Mátyás."}]
    },
    "24. A nagy földrajzi felfedezések és a kapitalizmus hajnala": {
        "alcim": "A karavella, iránytű, Kolumbusz, Vasco da Gama és a globális kereskedelem",
        "kulcsszavak": ["Kolumbusz (1492)", "Vasco da Gama", "Árforradalom", "Gyarmatosítás"],
        "audio_szoveg": "A 15. század végén új tengeri utakat kerestek az európaiak...",
        "vazlat": "### I. Okok -> II. Kolumbusz (1492), Vasco da Gama -> III. Árforradalom, gyarmatosítás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Okok -> 2. Új utak -> 3. Következmények.",
        "kviz": [{"k": "Kolumbusz 1492-ben érte el Amerikát.", "v": True, "m": "Spanyol támogatással."}]
    },
    "25. A reformáció és a katolikus megújulás (ellenreformáció)": {
        "alcim": "Luther Márton, Kálvin János, hitviták, új felekezetek és a barokk művészet",
        "kulcsszavak": ["Luther (1517)", "Kálvin János", "Jezsuiták", "Trentói zsinat"],
        "audio_szoveg": "A 16. században a katolikus egyház bírálatából kiindulva kibontakozott a reformáció...",
        "vazlat": "### I. Luther (1517, 95 tétel) -> II. Kálvin -> III. Trentói zsinat és barokk.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Luther -> 2. Kálvin -> 3. Ellenreformáció.",
        "kviz": [{"k": "Luther 1517-ben tűzte ki 95 tételét Wittenbergben.", "v": True, "m": "Reformáció kezdete."}]
    },
    "26. Az angol alkotmányos monarchia kialakulása a XVII. században": {
        "alcim": "A Stuart-házi absolutizmus kísérlete, polgárháború, Cromwell és az 1689-es Jognyilatkozat",
        "kulcsszavak": ["Angol polgárháború", "Cromwell", "Dicsőséges forradalom (1688)", "Jognyilatkozat (1689)"],
        "audio_szoveg": "A 17. századi Angliában a parlament és a király összecsapásából született az alkotmányos monarchia...",
        "vazlat": "### I. Polgárháború, Cromwell -> II. 1688 Dicsőséges forradalom -> III. 1689 Jognyilatkozat.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Polgárháború -> 2. Dicsőséges forradalom -> 3. Jognyilatkozat.",
        "kviz": [{"k": "Az 1689-es Jognyilatkozat fektette le az alkotmányos monarchia alapjait.", "v": True, "m": "Parlament fennhatósága."}]
    },
    "27. A francia polgári forradalom és Napóleon bukása": {
        "alcim": "A rendi gyűlés összehívása (1789), Emberi és Polgári Jogok Nyilatkozata, jakobinus diktatúra és Napóleon",
        "kulcsszavak": ["1789 Bastille", "Jogok Nyilatkozata", "Jakobinus terror", "Napóleon"],
        "audio_szoveg": "1789-ben Franciaországban kitört a modern európai történelem legnagyobb forradalma...",
        "vazlat": "### I. 1789 júliusa, Bastille -> II. Jakobinus terror -> III. Napóleon birodalma.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Forradalom -> 2. Terror -> 3. Napóleon.",
        "kviz": [{"k": "A Bastille ostromával kezdődött az 1789-es francia forradalom.", "v": True, "m": "Július 14."}]
    },
    "28. Az ipari forradalmak hullámai és a munkáskérdés": {
        "alcim": "Gőzgép, gyári ipar, urbanizáció, vasútépítés és a szocialista eszmék születése",
        "kulcsszavak": ["Watt gőzgépe", "Második ipari forradalom", "Urbanizáció", "Marxizmus"],
        "audio_szoveg": "Az ipari forradalmak átalakították az emberiség termelési módját...",
        "vazlat": "### I. I. ipari forradalom (gőzgép, vasút) -> II. II. ipari forradalom (elektromosság) -> III. Munkáskérdés, marxizmus.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Gőzgép -> 2. Urbanizáció -> 3. Munkáskérdés.",
        "kviz": [{"k": "James Watt tökéletesítette a gőzgépet.", "v": True, "m": "Ipari forradalom alapja."}]
    },
    "29. Az európai integráció és a globalizáció kezdetei": {
        "alcim": "A Schuman-terv, az EGK, az Európai Unió megalakulása (Maastrichti szerződés) és globalizáció",
        "kulcsszavak": ["Schuman-terv (1950)", "Római szerződés (1957)", "Maastricht (1992)", "Globalizáció"],
        "audio_szoveg": "A II. vh után Európa államai elindították az integrációs folyamatot...",
        "vazlat": "### I. Schuman-terv, EGK -> II. 1992 Maastrichti szerződés (EU) -> III. Globalizáció.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kezdetek -> 2. EU megalakulása -> 3. Globalizáció.",
        "kviz": [{"k": "Az 1992-es Maastrichti szerződés hozta létre az EU-t.", "v": True, "m": "Megalapozta az uniót."}]
    },
    "30. A jelenkori világ globális kihívásai (klímaváltozás, migráció, információs társadalom)": {
        "alcim": "Környezeti válság, demográfiai folyamatok és a digitális kor kérdései",
        "kulcsszavak": ["Klímaváltozás", "Fenntartható fejlődés", "Migráció", "Információs társadalom"],
        "audio_szoveg": "A 21. század elején az emberiség globális kihívásokkal szembesül...",
        "vazlat": "### I. Klímaváltozás és fenntarthatóság -> II. Migrációs hullámok -> III. Információs társadalom (AI, fake news).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klímaválság -> 2. Migráció -> 3. Digitális kor.",
        "kviz": [{"k": "A fenntartható fejlődés védi a jövő generációinak esélyeit.", "v": True, "m": "Ökológiai alapelv."}]
    }
}

# -------------------------------------------------------------
# 4. MATEMATIKA TÉTELTÁR (16 Témakör)
# -------------------------------------------------------------
tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció és kombináció",
        "kulcsszavak": ["Metszet, Unió, Különbség", "Venn-diagram", "Permutáció ($n!$)", "Kombináció ($\binom{n}{k}$)"],
        "audio_szoveg": "A halmazelmélet és a kombinatorika a modern matematika alapvető eszköztára a kiválasztási feladatokhoz...",
        "vazlat": "### I. Halmazműveletek: Unió, Metszet, Különbség, Komplementer.\n### II. Kombinatorika:\n- Permutáció: Pn = n!\n- Variáció (sorrend számít): V = n! / (n-k)!\n- Kombináció (sorrend NEM számít): C = n alatt a k = n! / (k!(n-k)!).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Halmazok és műveletek -> 2. Permutáció képlete -> 3. Variáció vs. Kombináció -> 4. Lottópélda.",
        "kviz": [{"k": "Az 5-ös lottó kihúzásainak száma kombinációval számítható (90 alatt az 5).", "v": True, "m": "A sorrend nem számít."}]
    },
    "2. Algebra: Egyenletek, egyenlőtlenségek és másodfokú formula": {
        "alcim": "Megoldóképlet, diszkrimináns, gyöktényezős szorzat és Viéte-formulák",
        "kulcsszavak": ["Diszkrimináns ($b^2 - 4ac$)", "Megoldóképlet", "Gyöktényezős alak", "Kikötések"],
        "audio_szoveg": "A másodfokú egyenletek megoldásának alapeszköze a megoldóképlet és a diszkrimináns vizsgálata...",
        "vazlat": "### I. Megoldóképlet: x1,2 = (-b +- gyök(b^2 - 4ac)) / (2a).\n### II. Diszkrimináns (D = b^2 - 4ac): D > 0 (2 gyök), D = 0 (1 gyök), D < 0 (nincs valós gyök).\n### III. Gyöktényezős alak: a(x - x1)(x - x2) = 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kikötések -> 2. Másodfokú megoldóképlet és diszkrimináns -> 3. Gyöktényezős alak -> 4. Ellenőrzés.",
        "kviz": [{"k": "Ha a diszkrimináns negatív, a másodfokú egyenletnek nincs valós gyöke.", "v": True, "m": "Negatívból nincs valós négyzetgyök."}]
    },
    "3. Hatványozás, gyökvonás és a logaritmus azonosságai": {
        "alcim": "Hatványozási azonosságok, törtkitevő, logaritmus fogalma és műveleti szabályai",
        "kulcsszavak": ["$a^n \cdot a^m = a^{n+m}$", "Törtkitevő", "Logaritmus azonosságok", "Alapáttérés"],
        "audio_szoveg": "A hatványozás és a logaritmus egymás inverz műveletei...",
        "vazlat": "### I. Hatványozás: a^n * a^m = a^(n+m), a^n / a^m = a^(n-m), (a^n)^m = a^(n*m), a^-n = 1/a^n, Törtkitevő: a^(m/n) = n-edik gyök(a^m).\n### II. Logaritmus: log_a(x * y) = log_a(x) + log_a(y), log_a(x / y) = log_a(x) - log_a(y), log_a(x^k) = k * log_a(x).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hatványozás szabályai -> 2. Törtkitevő -> 3. Logaritmus definíciója -> 4. Logaritmus azonosságai.",
        "kviz": [{"k": "log2(8) értéke pontosan 3.", "v": True, "m": "Mert 2 a 3. hatványon 8."}]
    },
    "4. Függvénytan és analízis alapjai": {
        "alcim": "Lineáris, másodfokú, exponenciális, logaritmikus függvények és jellemzésük",
        "kulcsszavak": ["Értelmezési tartomány", "Értékkészlet", "Zérushely", "Szélsőérték", "Monotonitás"],
        "audio_szoveg": "A függvény egy egyértelmű hozzárendelés két halmaz között...",
        "vazlat": "### I. Jellemzési lépések: Értelmezési tartomány (Df), Értékkészlet (Rf), Zérushely (f(x)=0), Szélsőérték (min/max), Monotonitás, Paritás.\n### II. Transzformációk: f(x)+c (függőleges), f(x-d) (vízszintes), c*f(x) (nyújtás).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Függvény fogalma -> 2. Jellemzési szempontok -> 3. Transzformációk -> 4. Parabola csúcsa.",
        "kviz": [{"k": "Az f(x) = (x - 4)^2 függvény minimuma az x = +4 pontban van.", "v": True, "m": "A zárójelen belüli -4 jobbra tolja el a csúcsot."}]
    },
    "5. Sorozatok és Pénzügyi matematika": {
        "alcim": "Számtani és mértani sorozat képletei, kamatos kamat és gyűjtőjáradék",
        "kulcsszavak": ["Differencia ($d$)", "Hányados ($q$)", "$n$-edik tag képlete", "Összegképlet ($S_n$)", "Kamatos kamat"],
        "audio_szoveg": "A számtani és mértani sorozatok törvényszerűségei alapozzák meg a pénzügyi kamatszámításokat...",
        "vazlat": "### I. Számtani sorozat (d): an = a1 + (n - 1)d, Sn = ((a1 + an) / 2) * n.\n### II. Mértani sorozat (q): an = a1 * q^(n - 1), Sn = a1 * (q^n - 1) / (q - 1).\n### III. Kamatos kamat: Cn = C0 * (1 + p/100)^n.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Számtani sorozat -> 2. Mértani sorozat -> 3. Kamatos kamat képlete.",
        "kviz": [{"k": "Ha a1 = 5 és d = 3, akkor a számtani sorozat 10. tagja 32.", "v": True, "m": "a10 = 5 + 9 * 3 = 32."}]
    },
    "6. Síkgeometria és Trigonometria": {
        "alcim": "Pitagorasz-tétel, Szinusz- és Koszinusztétel, háromszögek területszámítása",
        "kulcsszavak": ["Pitagorasz-tétel", "Szögfüggvények (sin, cos, tg)", "Szinusztétel", "Koszinusztétel", "Területképletek"],
        "audio_szoveg": "A síkgeometria alapja a derékszögű és általános háromszögek összefüggéseinek ismerete...",
        "vazlat": "### I. Derékszögű háromszög: a^2 + b^2 = c^2, sin, cos, tg definíciói.\n### II. Általános háromszög: Szinusztétel (a/sinA = b/sinB = 2R), Koszinusztétel (a^2 = b^2 + c^2 - 2bc*cosA).\n### III. Terület: T = (a * ma)/2 = (a*b*sinGamma)/2.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szögfüggvények -> 2. Szinusz- és Koszinusztétel -> 3. Területképletek.",
        "kviz": [{"k": "A koszinusztétel bármilyen általános háromszögre alkalmazható két oldal és a közbezárt szög ismeretében.", "v": True, "m": "Pitagorasz általánosítása."}]
    },
    "7. Síkgeometria: Sokszögek, kör és négyszögek tulajdonságai": {
        "alcim": "Szabályos sokszögek belső szögei, deltoid, rombusz, trapéz, kör ívhossza és körcikk területe",
        "kulcsszavak": ["Belső szögek összege ($(n-2)\cdot 180^\circ$)", "Átlók száma", "Trapéz területe", "Rombusz", "Körcikk területe"],
        "audio_szoveg": "A sokszögek és négyszögek geometriája az érettségi írásbeli vizsga gyakori feladattípusa...",
        "vazlat": "### I. Sokszögek: Belső szögek összege: (n - 2) * 180 fok; Átlók száma: n(n - 3) / 2.\n### II. Négyszögek: Trapéz területe: ((a + c)/2) * m; Rombusz/Deltoid területe: (e * f) / 2.\n### III. Kör részei: Ívhossz: i = (2r*pi*alfa)/360; Körcikk területe: T = (r^2*pi*alfa)/360.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Belső szögek és átlók -> 2. Négyszögek területképletei -> 3. Kör és körcikk.",
        "kviz": [{"k": "Egy konvex ötszög belső szögeinek összege pontosan 540 fok.", "v": True, "m": "(5 - 2) * 180 = 540 fok."}]
    },
    "8. Koordinátageometria": {
        "alcim": "Vektorműveletek, felezőpont, súlypont, az egyenes és a kör egyenlete",
        "kulcsszavak": ["Normálvektor $\\vec{n}(A, B)$", "Irányvektor $\\vec{v}(v_1, v_2)$", "Egyenes egyenlete", "Kör egyenlete"],
        "audio_szoveg": "A koordinátageometria segítségével algebrai egyenletekkel írhatunk le geometriai alakzatokat...",
        "vazlat": "### I. Alapok: Távolság (d = gyök((x2-x1)^2 + (y2-y1)^2)), Felezőpont.\n### II. Egyenes egyenlete: Normálvektoros alak: Ax + By = Ax0 + By0.\n### III. Kör egyenlete: (x - u)^2 + (y - v)^2 = r^2 (Középpont: K(u, v), sugár: r).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Távolság és felezőpont -> 2. Egyenes egyenlete -> 3. Kör egyenlete.",
        "kviz": [{"k": "A (x - 3)^2 + (y + 1)^2 = 25 egyenletű kör sugara r = 5.", "v": True, "m": "Mert r^2 = 25 -> r = 5."}]
    },
    "9. Térgeometria (Testek felszíne és térfogata)": {
        "alcim": "Hasáb, henger, gúla, kúp és gömb felszín- és térfogatszámítása",
        "kulcsszavak": ["Henger", "Kúp", "Gúla", "Gömb", "Felszín ($A$)", "Térfogat ($V$)"],
        "audio_szoveg": "A térgeometria a háromdimenziós testek metrikus tulajdonságaival foglalkozik...",
        "vazlat": "### I. Henger: V = r^2 * pi * M, A = 2*r^2*pi + 2*r*pi*M.\n### II. Kúp és Gúla: V = (Talap * M) / 3, Kúp palástja: r * pi * a.\n### III. Gömb: V = 4/3 * R^3 * pi, A = 4 * R^2 * pi.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Egyenes testek -> 2. Csúcsos testek harmadoló szabálya -> 3. Gömb képletei.",
        "kviz": [{"k": "A kúp térfogata a henger térfogatának egyharmada.", "v": True, "m": "Ott van az 1/3 szorzó."}]
    },
    "10. Valószínűségszámítás és Statisztika": {
        "alcim": "Klasszikus valószínűség, binomiális eloszlás, átlag, medián, módusz és szórás",
        "kulcsszavak": ["Kedvező / Összes", "Binomiális eloszlás", "Medián", "Módusz", "Átlag", "Szórás"],
        "audio_szoveg": "A valószínűségszámítás a véletlen események modellezését végzi...",
        "vazlat": "### I. Valószínűség: P = Kedvező / Összes. Binomiális: P(X=k) = (n alatt k) * p^k * (1-p)^(n-k).\n### II. Statisztika: Átlag, Módusz (leggyakoribb), Medián (rendezett sor közepe), Terjedelem, Szórás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszikus valószínűség -> 2. Binomiális modell -> 3. Statisztikai középértékek -> 4. Szórás.",
        "kviz": [{"k": "A medián meghatározásához először mindig nagyság szerinti sorba kell rendezni az adatokat.", "v": True, "m": "A rendezett minta középső eleme."}]
    },
    "11. Gráfelméleti alapfogalmak és alkalmazások": {
        "alcim": "Csúcsok, élek, fokszámok összege, összefüggő gráfok, fák és Euler-vonal",
        "kulcsszavak": ["Fokszámtétel ($\sum d(v) = 2e$)", "Egyszerű gráf", "Összefüggő gráf", "Fa gráf", "Teljes gráf"],
        "audio_szoveg": "A gráfelmélet csúcsok és az azokat összekötő élek hálózatát vizsgálja...",
        "vazlat": "### I. Alapok: Csúcsok (V), Élek (E), Csúcs fokszáma (d(v)). Fokszámtétel: Fokszámok összege = 2 * élek száma.\n### II. Típusok: Teljes gráf (Kn = n*(n-1)/2 él), Fa gráf (összefüggő, körmentes, n csúcshoz n-1 él), Euler-vonal.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Gráf fogalma -> 2. Fokszámtétel -> 3. Teljes gráf és Fa gráf -> 4. Euler-vonal.",
        "kviz": [{"k": "Egy gráfban nem lehet páratlan számú páratlan fokszámú csúcs.", "v": True, "m": "A fokszámösszeg mindig páros."}]
    },
    "12. Exponenciális és logaritmikus egyenletek": {
        "alcim": "Azonos alapra hozás módszere, logaritmálás, új ismeretlen bevezetése",
        "kulcsszavak": ["Közös alapra hozás", "Szigorú monotonitás", "Új változó", "Értelmezési tartomány"],
        "audio_szoveg": "Az exponenciális és logaritmusos egyenletek megoldásakor a szigorú monotonitás a kulcs...",
        "vazlat": "### I. Exponenciális: Azonos alapra hozás (a^f(x) = a^g(x) -> f(x) = g(x)), Új ismeretlen bevezetése (u = a^x).\n### II. Logaritmusos: Kikötés kötelező (belső szám > 0!), logaritmus azonosságok összevonása, ellenőrzés.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Exponenciális azonos alapra hozása -> 2. Új változó -> 3. Logaritmusos kikötések -> 4. Monotonitás.",
        "kviz": [{"k": "A 2^x = 16 egyenlet megoldása x = 4.", "v": True, "m": "Mert 2 a 4. hatványon 16."}]
    },
    "13. Trigonometrikus egyenletek": {
        "alcim": "Alap szögfüggvényes egyenletek megoldása a periodicitás figyelembevételével",
        "kulcsszavak": ["Periodicitás", "Két megoldássorozat", "Egységkör", "$\sin^2 x + \cos^2 x = 1$"],
        "audio_szoveg": "A szögfüggvényes egyenleteknél a megoldások periodikus sorozatokat alkotnak...",
        "vazlat": "### I. Azonosság: sin^2(x) + cos^2(x) = 1, tg(x) = sin(x)/cos(x).\n### II. Megoldások periodicitással:\n- sin(x) = c -> x1 = alfa + k*360 fok, x2 = 180 - alfa + k*360 fok.\n- cos(x) = c -> x1 = alfa + k*360 fok, x2 = -alfa + k*360 fok.\n- tg(x) = c -> x = alfa + k*180 fok.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Egységkör szimmetriái -> 2. Szinusz két ága -> 3. Koszinusz két ága -> 4. Periodicitás.",
        "kviz": [{"k": "A tg(x) függvény periódusa 180 fok.", "v": True, "m": "Míg a sin és cos periódusa 360 fok."}]
    },
    "14. Vektorműveletek és a skaláris szorzat": {
        "alcim": "Összeadás, kivonás, számmal szorzás, skaláris szorzat és két vektor hajlásszöge",
        "kulcsszavak": ["Vektor koordinátái", "Skaláris szorzat", "Hajlásszög", "Merőlegesség"],
        "audio_szoveg": "Két vektor skaláris szorzata valós számot eredményez...",
        "vazlat": "### I. Vektorműveletek: a + b = (a1+b1, a2+b2), |a| = gyök(a1^2 + a2^2).\n### II. Skaláris szorzat: a * b = a1*b1 + a2*b2 = |a| * |b| * cos(fi).\n### III. Merőlegesség: Két vektor merőleges, ha skaláris szorzatuk 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Vektor koordinátái -> 2. Skaláris szorzat -> 3. Hajlásszög -> 4. Merőlegesség.",
        "kviz": [{"k": "Ha két vektor skaláris szorzata 0, a két vektor merőleges egymásra.", "v": True, "m": "Mert cos(90 fok) = 0."}]
    },
    "15. Számelmélet: Oszthatóság, prímek, LNKO és LKKT": {
        "alcim": "Oszthatósági szabályok, a számelmélet alaptétele, legnagyobb közös osztó és legkisebb közös többszörös",
        "kulcsszavak": ["Prímszám", "Számelmélet alaptétele", "LNKO", "LKKT"],
        "audio_szoveg": "A számelmélet az egész számok oszthatósági tulajdonságait vizsgálja...",
        "vazlat": "### I. Oszthatóság: 2, 5, 10; 4, 25; 3, 9 szabályai.\n### II. Számelmélet alaptétele: Egyértelmű prímtényezős felbontás.\n### III. LNKO (közös prímek legkisebb hatványon), LKKT (összes prím legnagyobb hatványon).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Oszthatósági szabályok -> 2. Prímtényezős felbontás -> 3. LNKO és LKKT -> 4. Törtek egyszerűsítése.",
        "kviz": [{"k": "A 12 és 18 legnagyobb közös osztója (LNKO) a 6.", "v": True, "m": "12 = 2^2 * 3 és 18 = 2 * 3^2 -> LNKO = 6."}]
    },
    "16. Differenciálszámítás (Deriválás) bevezetése": {
        "alcim": "A differenciahányados, derivált fogalma, hatványfüggvény deriválása és érintő meredeksége",
        "kulcsszavak": ["Érintő meredeksége", "Deriválási szabályok", "Szélsőértékkeresés ($f'(x) = 0$)"],
        "audio_szoveg": "A differenciálszámítás a függvények változási sebességét és az érintő meredekségét vizsgálja...",
        "vazlat": "### I. Geometriai jelentés: f'(x0) az érintő meredeksége (m).\n### II. Szabályok: (c)' = 0, (x^n)' = n * x^(n-1).\n### III. Szélsőérték: Ahol a függvénynek szélsőértéke van, ott f'(x) = 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Derivált geometriai jelentése -> 2. Hatványfüggvény deriválása -> 3. Szélsőérték feltétele.",
        "kviz": [{"k": "Az f(x) = x^4 függvény deriváltja f'(x) = 4x^3.", "v": True, "m": "A kitevő szorzóvá válik, a hatvány 1-gyel csökken."}]
    }
}

# -------------------------------------------------------------
# TANTÁRGYANKÉNT KÜLÖNVÁLASZTOTT VILLÁMKÁRTYÁK (FLASHCARDS)
# -------------------------------------------------------------
flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra (dalforma), epika (cselekmény) és dráma (konfliktus) sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a legfontosabb irodalmi szerkesztője?", "a": "1908. január 1-jén indult, és Osvát Ernő volt a lap legendás irodalmi szerkesztője."},
    {"q": "Mi a központi szállóige Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.” – Az értelmiségi ember morális felelősségvállalása."},
    {"q": "Hogyan végződik Örkény István 'Tóték' című műve?", "a": "Tót Lajos a dobozvágó margóvágóval négy egyforma darabba vágja az Őrnagyot."},
    {"q": "Mit szimbolizál az Ágnes asszonyban a véres lepedő kényszeres mosása?", "a": "A bűn letörölhetetlenségét és a lelkiismeret-furdalás által kiváltott elmezavart."},
    {"q": "Miért különleges a párizsi szín 'Az ember tragédiájában'?", "a": "Ez az egyetlen olyan történelmi szín, amelyből Ádám nem csalódottan, hanem hittel és tettre készen ébred fel."},
    {"q": "Ki képviseli a tiszta humanizmus hangját Kosztolányi 'Édes Anna' című regényében?", "a": "Moviszter doktor, aki egyedüliként tekinti Annát érző emberi lénynek."},
    {"q": "Melyik kötet nyitotta meg Ady Endre szimbolista költői forradalmát?", "a": "Az 1906-ban megjelent Új versek című kötet."}
]

flashcards_nyelvtan = [
    {"q": "Mi a magyar helyesírás 4 alapelve?", "a": "1. Kiejtés elve, 2. Szóelemzés elve, 3. Hagyomány elve, 4. Egyszerűsítés elve."},
    {"q": "Mi a toldalékok szigorú kötött sorrendje a magyar szavakban?", "a": "Szótő + KÉPZŐ + JEL + RAG (pl. ház-as-ság-ok-at)."},
    {"q": "Mi a különbség a szólás és a közmondás között?", "a": "A szólás képszerű kifejezés mondatérték nélkül (pl. feni a fogát), a közmondás kerek egész mondat tanulsággal (pl. Ki korán kel, aranyat lel)."},
    {"q": "Mi a különbség az anafora és a katafora között a szövegtanban?", "a": "Az anafora visszautal egy korábbi szövegelemre, míg a katafora előreutal egy későbbi elemre."},
    {"q": "Melyik a legkorábbi fennmaradt összefüggő magyar szövegemlék?", "a": "A Halotti Beszéd és Könyörgés (1195 körül, a Pray-kódexben)."},
    {"q": "Mi a szónoki beszéd 6 klasszikus szerkezeti része?", "a": "Bevezetés (Exordium) -> Elbeszélés (Narratio) -> Részletezés -> Bizonyítás -> Cáfolás -> Befejezés (Peroratio)."},
    {"q": "Milyen mássalhangzótörvény érvényesül a 'barátság' szóban?", "a": "Összeolvadás: a t + s hangokból hosszú [ccs] hang keletkezik [baraccság]."}
]

flashcards_tortenelem = [
    {"q": "Mikor adta ki Nagy Lajos az Ősiség törvényét és mit jelentett az?", "a": "1351-ben. A nemesi birtok nem adható el, nemes kihalásakor a rokonokra, végül a királyra száll vissza."},
    {"q": "Mikor foglalta el a török csellel Buda várát, amivel 3 részre szakadt az ország?", "a": "1541. augusztus 29-én."},
    {"q": "Milyen új pénznemet vezetett be Bethlen István 1927-ben a gazdasági stabilitásért?", "a": "A Pengőt."},
    {"q": "Mikor és hol adta ki II. András az Aranybullát?", "a": "1222-ben Fehérváron, rögzítve a szerviensek nemesi szabadságjogait és az ellenállási záradékot."},
    {"q": "Mikor és hol kiáltották ki a Függetlenségi Nyilatkozatot 1849-ben?", "a": "1849. április 14-én a debreceni Nagytemplomban, kimondva a Habsburg-ház trónfosztását."},
    {"q": "Melyek voltak az Osztrák-Magyar Monarchia közös ügyei az 1867-es Kiegyezés után?", "a": "A külügy, a hadügy és az ezek fedezésére szolgáló pénzügy."},
    {"q": "Mikor robbant ki az 1956-os forradalom és mi volt a szovjet megtorlás kezdőnapja?", "a": "1956. október 23-án robbant ki, és 1956. november 4-én indult meg a szovjet invázió."}
]

flashcards_matek = [
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Mi a számtani és a mértani sorozat n-edik tagjának képlete?", "a": "Számtani: an = a1 + (n - 1)d | Mértani: an = a1 * q^(n - 1)"},
    {"q": "Mit mond ki a gráfelmélet fokszámtétele?", "a": "A gráf csúcsainak fokszámösszege mindig páros, és egyenlő az élek számának kétszeresével (2e)."},
    {"q": "Mikor merőleges egymásra két vektor?", "a": "Ha a skaláris szorzatuk pontosan 0 (a1*b1 + a2*b2 = 0)."},
    {"q": "Mennyi a konvex n-szög belső szögeinek összege?", "a": "Sn = (n - 2) * 180°"},
    {"q": "Mi a koszinusztétel képlete általános háromszögre?", "a": "a² = b² + c² - 2bc · cos(α)"},
    {"q": "Mi a henger és a kúp térfogatképlete?", "a": "Henger: V = r²π · M | Kúp: V = (r²π · M) / 3"},
    {"q": "Hogyan deriváljuk a hatványfüggvényt (x^n)?", "a": "(x^n)' = n · x^(n - 1)"},
    {"q": "Mi a klasszikus valószínűség kiszámítási képlete?", "a": "P(A) = Kedvező esetek száma / Összes lehetséges eset száma (k / n)"}
]

# Idővonalak tantárgyanként
timeline_irodalom = [
    {"ev": "1848–1849", "cim": "A forradalom és szabadságharc lírája", "leiras": "Petőfi forradalmi látomásköltészete (A XIX. század költői, Nemzeti dal); Arany János korai korszaka."},
    {"ev": "1850-es évek", "cim": "A nagykőrösi balladák korszaka", "leiras": "Arany János allegorikus nemzeti ellenállása (A walesi bárdok, Szondi két apródja) és mély lélektana (Ágnes asszony)."},
    {"ev": "1859–1860", "cim": "Az ember tragédiája születése", "leiras": "Madách Imre drámai költeménye az emberiség eszméinek és küzdelmének filozófiájáról."},
    {"ev": "1872", "cim": "Az arany ember megjelenése", "leiras": "Jókai Mór érett romantikus-realista regénye a polgári meghasonlásról és a Senki szigetéről."},
    {"ev": "1877", "cim": "Arany János Őszikék korszaka", "leiras": "Margitszigeti kései líra a Kapcsos könyvben; nagyvárosi haláltánc a Híd-avatásban."},
    {"ev": "1906–1908", "cim": "A modern magyar irodalom robbanása", "leiras": "Ady Endre: Új versek (1906) és a Nyugat folyóirat indulása (1908) Osvát Ernő és Babits vezetésével."},
    {"ev": "1926", "cim": "Édes Anna és a lélektani próza", "leiras": "Kosztolányi Dezső regénye az 1919-es történelmi háttérben az elfojtott sérelmek robbanásáról."},
    {"ev": "1938–1944", "cim": "A fasizmus árnyékában", "leiras": "Babits megírja a Jónás könyvét (1938); Radnóti Miklós bori noteszének kései eclogái és Razglednicái."}
]

timeline_nyelvtan = [
    {"ev": "Kr. e. 3000-től", "cim": "Az uráli és finnugor együttélés kora", "leiras": "Alapvető szókészletünk (testrészek, természeti jelenségek, számok) és a ragozó (agglutináló) nyelvtan kialakulása."},
    {"ev": "1055", "cim": "A Tihanyi apátság alapítólevele", "leiras": "Legkorábbi magyar szórványemlékünk ('feheruuaru rea meneh hodu utu rea')."},
    {"ev": "1195 körül", "cim": "A Halotti Beszéd és Könyörgés", "leiras": "A Pray-kódexben fennmaradt legkorábbi összefüggő magyar szövegemlék."},
    {"ev": "1300 körül", "cim": "Ómagyar Mária-siralom", "leiras": "Az első fennmaradt magyar nyelvű verses nyelvemlék (Leuveni kódex)."},
    {"ev": "1790–1820", "cim": "A Nyelvújítás korszaka", "leiras": "Kazinczy Ferenc és a neológusok harca az ortológusokkal; több mint tízezer új magyar szó teremtése."},
    {"ev": "1832", "cim": "Az első hivatalos Helyesírási Szabályzat", "leiras": "A Magyar Tudományos Akadémia rögzíti a 4 alapelvet és a hivatalos akadémiai normát."},
    {"ev": "2000-től", "cim": "A digitális kommunikáció kora", "leiras": "Az online kommunikáció, az írott beszéltség, a rövidítések és az emojik elterjedése."}
]

timeline_tortenelem = [
    {"ev": "Kr. e. V. sz.", "cim": "Az athéni demokrácia virágkora", "leiras": "Periklész kora, a népgyűlés és az esküdtbíróságok működése, a napidíjak bevezetése."},
    {"ev": "1000", "cim": "Szent István király koronázása", "leiras": "A keresztény magyar állam és a vármegyerendszer megalapítása, egyházmegyék kiépítése."},
    {"ev": "1222", "cim": "Az Aranybulla kiadása", "leiras": "II. András törvénye a szerviensek nemesi jogairól és az ellenállási záradékról."},
    {"ev": "1351", "cim": "Nagy Lajos törvényei", "leiras": "Az ősiség törvénye (aviticitas), a kilenced bevezetése és az egységes nemesi szabadság."},
    {"ev": "1458–1490", "cim": "Hunyadi Mátyás királysága", "leiras": "Központosított királyi hatalom, füstpénz, a Fekete sereg és a reneszánsz kultúra virágkora."},
    {"ev": "1526 / 1541", "cim": "Mohács és az ország 3 részre szakadása", "leiras": "1526 Mohácsi csatavesztés, 1541 Buda török kézre kerülése, Hódoltság és Erdély létrejötte."},
    {"ev": "1703–1711", "cim": "A Rákóczi-szabadságharc", "leiras": "Habsburg-ellenes nemzeti küzdelem, 1707 Ónodi trónfosztás, 1711 Szatmári béke."},
    {"ev": "1830–1848", "cim": "A magyar reformkor", "leiras": "Széchenyi Hitel című művével indul, Kossuth érdekegyesítési programja, a polgári átalakulás előkészítése."},
    {"ev": "1848–1849", "cim": "Forradalom és Szabadságharc", "leiras": "Március 15., Áprilisi törvények, függetlenségi háború és az 1849-es tavaszi hadjárat sikerei."},
    {"ev": "1867", "cim": "A Kiegyezés – Dualizmus kora", "leiras": "Az Osztrák-Magyar Monarchia létrejötte, Deák Ferenc, fél évszázados gazdasági és kulturális aranykor."},
    {"ev": "1920", "cim": "A Trianoni békediktátum", "leiras": "Az ország területének 2/3 része elcsatolva, 3,3 millió magyar rekedt a határokon túl."},
    {"ev": "1956. okt. 23.", "cim": "Forradalom és Szabadságharc", "leiras": "Fegyveres harc a szovjet elnyomás ellen, Nagy Imre kormánya, nov. 4-i invázió."},
    {"ev": "1989–1990", "cim": "A Békés Rendszerváltás", "leiras": "Ellenzéki Kerekasztal, Nagy Imre újratemetése, határnyitás, a Köztársaság kikiáltása és az 1990-es szabad választások."}
]

timeline_matek = [
    {"ev": "Kr. e. VI. sz.", "cim": "Pitagorasz és a derékszögű háromszögek", "leiras": "A Pitagorasz-tétel (a² + b² = c²) felfedezése és a geometriai bizonyítások kezdete."},
    {"ev": "Kr. e. III. sz.", "cim": "Euklidész és a geometriai axiómák", "leiras": "Az 'Elemek' című mű: a síkgeometria, a párhuzamossági axióma és a prímek végtelenségének bizonyítása."},
    {"ev": "IX. század", "cim": "Al-Hvárizmi és az Algebra születése", "leiras": "A másodfokú egyenletek szisztematikus megoldási módszere és az algoritmus fogalmának alapjai."},
    {"ev": "1637", "cim": "René Descartes és a Koordinátageometria", "leiras": "A derékszögű koordináta-rendszer megalkotása: geometriai alakzatok leírása algebrai egyenletekkel."},
    {"ev": "1687", "cim": "Newton és Leibniz: Differenciálszámítás", "leiras": "A derivált és a határérték felfedezése: a függvények pillanatnyi változási sebességének kiszámítása."},
    {"ev": "1736", "cim": "Leonhard Euler és a Gráfelmélet", "leiras": "A königsbergi hidak problémájának megoldása: a csúcsok, élek és fokszámok összefüggései."}
]

# Detektív játék adatbázisok tantárgyanként különválasztva
detektiv_irodalom = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma. / Fölkeltem én hát; megbánva a rest / lapulást...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Ember az embertelenségben", "Arany János: Szondi két apródja", "Radnóti Miklós: Nem tudhatom"], "info": "A prófétai és értelmiségi felelősségvállalás alaptétele."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb, / Mit kény és kedv szerint lök / A sors előbb-tovább.”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János: Toldi", "Ady Endre: Új vizeken járok"], "info": "Petőfi forradalmi felhívó lírájának remeke."}
]

detektiv_nyelvtan = [
    {"idezet": "„barátság [kiejtve: baraccság]”", "helyes": "Összeolvadás mássalhangzótörvény", "opciok": ["Összeolvadás mássalhangzótörvény", "Zöngésségi részleges hasonulás", "Írásban jelölt teljes hasonulás", "Mássalhangzó-kiesés"], "info": "A t + s hangokból egy harmadik, hosszú [ccs] hang keletkezik."},
    {"idezet": "„lila dalra kelt az éjcsend”", "helyes": "Szinesztézia (Költői kép)", "opciok": ["Szinesztézia (Költői kép)", "Megszemélyesítés", "Metonímia", "Szinekdoché"], "info": "Látási (lila), hallási (dal) és csend érzékterületek összekapcsolása."}
]

detektiv_tortenelem = [
    {"idezet": "„Ius resistendi (A nemesek joga a királlyal szembeni ellenállásra)”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Nagy Lajos 1351-es törvényei", "Szent István I. törvénykönyve", "Kollonics Lipót rendelete"], "info": "A magyar rendi nemesi szabadságjogok sarokköve."},
    {"idezet": "„Eb ura fakó, József császár nem királyunk!”", "helyes": "1707-es Ónodi országgyűlés (Trónfosztás)", "opciok": ["1707-es Ónodi országgyűlés (Trónfosztás)", "1849-es Debreceni trónfosztás", "1526-os Rákosi gyűlés", "1608-as koronázási cikkelyek"], "info": "A Rákóczi-szabadságharc alatt kimondott Habsburg-trónfosztás jelszava."}
]

detektiv_matek = [
    {"idezet": "a² = b² + c² - 2bc · cos(α)", "helyes": "Koszinusztétel (Általános háromszögekre)", "opciok": ["Koszinusztétel (Általános háromszögekre)", "Szinusztétel", "Pitagorasz-tétel", "Héron-képlet"], "info": "A Pitagorasz-tétel általánosítása tetszőleges háromszögre."},
    {"idezet": "(x^n)' = n · x^(n-1)", "helyes": "Hatványfüggvény deriválási szabálya", "opciok": ["Hatványfüggvény deriválási szabálya", "Logaritmus azonosság", "Binomiális tétel", "Sorozat összegképlet"], "info": "A differenciálszámítás legalapvetőbb műveleti szabálya."}
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

# AI hívás szöveges és hang bemenethez
def ai_generalas(prompt_text, audio_bytes=None, mime_type=None):
    api_k = get_api_key()
    if not api_k:
        return "⚠️ Nincs beállítva a Secrets-ben a GEMINI_API_KEY kulcs!"
    try:
        client = genai.Client(api_key=api_k)
        contents_input = [prompt_text]
        if audio_bytes and mime_type:
            contents_input.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": audio_bytes
                }
            })
            
        modellek = ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
        for m in modellek:
            try:
                res = client.models.generate_content(model=m, contents=contents_input)
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
# FŐ TANTÁRGY VÁLASZTÓ
# =============================================================
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox(
    "Válassz tantárgyat:",
    [
        "📖 Magyar Irodalom (22 tétel)",
        "🔤 Magyar Nyelvtan (16 tétel)",
        "🏛️ Történelem (30 tétel)",
        "📐 Matematika (16 témakör)"
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
        "🎙️ Szóbeli Szimulátor (Beszéd / Írás)",
        "✍️ Esszé & Feladatmegoldó Labor",
        "🎭 Tantárgyi Detektív Játék",
        "🧭 Tantárgyi Idővonal & Térkép",
        "🏆 Nagy Próbavizsga",
        "🤖 AI Érettségi Mentor"
    ]
)

# Adatbázisok szétválasztása a választott tantárgyhoz
if "Irodalom" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_irodalom
    aktiv_flashcards = flashcards_irodalom
    aktiv_timeline = timeline_irodalom
    aktiv_detektiv = detektiv_irodalom
    tantargy_cimke = "Magyar Irodalom"
elif "Nyelvtan" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_nyelvtan
    aktiv_flashcards = flashcards_nyelvtan
    aktiv_timeline = timeline_nyelvtan
    aktiv_detektiv = detektiv_nyelvtan
    tantargy_cimke = "Magyar Nyelvtan"
elif "Történelem" in kivalasztott_tantargy:
    aktiv_adatbazis = tetelek_tortenelem
    aktiv_flashcards = flashcards_tortenelem
    aktiv_timeline = timeline_tortenelem
    aktiv_detektiv = detektiv_tortenelem
    tantargy_cimke = "Történelem"
else:
    aktiv_adatbazis = tetelek_matek
    aktiv_flashcards = flashcards_matek
    aktiv_timeline = timeline_matek
    aktiv_detektiv = detektiv_matek
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
    st.markdown(f"<div class='subject-pill'>🎯 Aktuális tantárgy: {tantargy_cimke} ({len(aktiv_adatbazis)} db tétel)</div>", unsafe_allow_html=True)
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
    st.title(f"🎴 {tantargy_cimke} Villámkártyák (Astra Flashcards)")
    st.caption(f"Pörgesd át a legfontosabb {tantargy_cimke} fogalmakat és szabályokat!")
    
    card_index = st.session_state.card_idx % len(aktiv_flashcards)
    aktualis_kartya = aktiv_flashcards[card_index]
    
    st.progress((card_index + 1) / len(aktiv_flashcards))
    st.write(f"Kártya: {card_index + 1} / {len(aktiv_flashcards)}")
    
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
            st.session_state.card_idx = (card_index + 1) % len(aktiv_flashcards)
            st.rerun()
        if col_b2.button("❌ Ismételni kell", use_container_width=True):
            st.session_state.card_flipped = False
            st.session_state.card_idx = (card_index + 1) % len(aktiv_flashcards)
            st.rerun()

# -------------------------------------------------------------
# 4. MENÜPONT: SZÓBELI SZIMULÁTOR (MIKROFONOS HANGFELVÉTEL + ÍRÁS)
# -------------------------------------------------------------
elif menupont == "🎙️ Szóbeli Szimulátor (Beszéd / Írás)":
    st.title(f"🎙️ {tantargy_cimke} Szóbeli Szimulátor (Mock Exam)")
    st.caption("Gyakorold a feleletet szóban vagy írásban! Nyomd meg a mikrofont és mondd el a feleletedet, az AI meghallgatja és értékeli.")
    
    valasztott_szim_tetel = st.selectbox(f"Válassz {tantargy_cimke} tételt a próbavizsgához:", list(aktiv_adatbazis.keys()))
    
    if st.button("🏁 Új szóbeli felelet indítása"):
        st.session_state.oral_history = [
            {"role": "ai", "text": f"Jó napot kívánok! Húzza ki a tételét... Az Ön tétele: **{valasztott_szim_tetel}**. Kérem, mondja el vagy írja le a feleletének bevezetését és a legfontosabb alapfogalmakat!"}
        ]
        st.rerun()
        
    for msg in st.session_state.oral_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑‍🎓 <strong>Ön feleli:</strong><br>{msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>👨‍🏫 <strong>Vizsgaelnök (AI):</strong><br>{msg['text']}</div>", unsafe_allow_html=True)
            
    st.markdown("---")
    st.subheader("🎤 1. Lehetőség: Szóbeli válaszadás mikrofonnal")
    audio_valasz = st.audio_input("Mondd el a feleletedet (kattints a mikrofonra a felvételhez):")
    
    if audio_valasz is not None:
        if st.button("🚀 Hangfelvétel beküldése és értékelése"):
            with st.spinner("A hangfelvétel meghallgatása és szakmai értékelése..."):
                hang_bytes = audio_valasz.read()
                prompt_audio = f"""
                {tantargy_cimke} szóbeli érettségi elnök vagy. A diák a(z) '{valasztott_szim_tetel}' tételből felel szóban a csatolt hangfelvételen.
                Feladatod:
                1. Röviden írd le, mit mondott a diák (1-2 mondatos összefoglaló).
                2. Szakmailag értékeld a választ (pontosság, szakszavak használata).
                3. Tegyél fel egy célzott, érettségi szintű kérdést a tétel egy másik fontos részletére, vagy adj konkrét érdemjegyet (1-5) és záróértékelést.
                Legyél támogató és precíz tanár!
                """
                ai_valasz = ai_generalas(prompt_audio, audio_bytes=hang_bytes, mime_type="audio/wav")
                st.session_state.oral_history.append({"role": "user", "text": "🎙️ *(Szóbeli hangfelvétel beküldve)*"})
                st.session_state.oral_history.append({"role": "ai", "text": ai_valasz})
                st.session_state.xp += 40
                st.rerun()

    st.markdown("---")
    st.subheader("⌨️ 2. Lehetőség: Írásbeli válaszadás")
    with st.form("oral_form", clear_on_submit=True):
        felelet_reszlet = st.text_area("Vagy gépeld be a feleleted részletét:")
        kuld_felelet = st.form_submit_button("Írott felelet beküldése")
        
        if kuld_felelet and felelet_reszlet:
            st.session_state.oral_history.append({"role": "user", "text": felelet_reszlet})
            prompt = f"""
            {tantargy_cimke} szóbeli érettségi elnök vagy. A diák a(z) '{valasztott_szim_tetel}' tételből felel.
            A diák válasza: '{felelet_reszlet}'.
            Feladatod:
            1. Röviden értékeld az elmondottakat.
            2. Tegyél fel egy célzott kérdést vagy adj konkrét érdemjegyet (1-5).
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
    st.caption(f"Másold be a(z) {tantargy_cimke} fogalmazásodat vagy egy feladat szövegét – az AI kijavítja vagy levezeti a teljes megoldást!")
    
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
# 6. MENÜPONT: TANTÁRGYI DETEKTÍV JÁTÉK
# -------------------------------------------------------------
elif menupont == "🎭 Tantárgyi Detektív Játék":
    st.title(f"🎭 {tantargy_cimke} Detektív Játék")
    st.caption(f"Felismered a legfontosabb {tantargy_cimke} idézeteket, forrásokat és képleteket?")
    
    if 'game_idx' not in st.session_state:
        st.session_state.game_idx = 0
        
    game_index = st.session_state.game_idx % len(aktiv_detektiv)
    feladvany = aktiv_detektiv[game_index]
    
    st.markdown(f"""
    <div class='topic-card' style='border-color:#ec4899; text-align:center;'>
        <h3 style='color:#f472b6; font-style:italic;'>{feladvany['idezet']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    valasztott_tipp = st.radio("Válaszd ki a helyes megfejtést:", feladvany['opciok'], key=f"detektiv_{tantargy_cimke}_{game_index}")
    
    if st.button("🔍 Tipp ellenőrzése"):
        if valasztott_tipp == feladvany['helyes']:
            st.balloons()
            st.session_state.xp += 30
            st.success(f"TÖKÉLETES! 🎉 Helyes válasz! (+30 XP)\n\n📌 Magyarázat: {feladvany['info']}")
        else:
            st.error(f"Sajnos nem! ❌ A helyes válasz: **{feladvany['helyes']}**\n\n📌 Magyarázat: {feladvany['info']}")
            
    if st.button("➡️ Következő feladvány"):
        st.session_state.game_idx = (game_index + 1) % len(aktiv_detektiv)
        st.rerun()

# -------------------------------------------------------------
# 7. MENÜPONT: TANTÁRGYI IDŐVONAL & TÉRKÉP
# -------------------------------------------------------------
elif menupont == "🧭 Tantárgyi Idővonal & Térkép":
    st.title(f"🧭 {tantargy_cimke} Idővonal & Tudástérkép")
    st.caption(f"Lásd át a(z) {tantargy_cimke} fejlődésének, tételeinek és korszakainak összefüggéseit!")
    
    for item in aktiv_timeline:
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
                key=f"probavizsga_{tantargy_cimke}_{idx}",
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
