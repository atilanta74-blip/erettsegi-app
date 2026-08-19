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
# 1. MAGYAR IRODALOM TÉTELTÁR (22 Tétel)
# -------------------------------------------------------------
tetelek_irodalom = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, nagykőrösi és margitszigeti korszak",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja", "A walesi bárdok"],
        "audio_szoveg": "Arany János a magyar irodalom legnagyobb balladaírója. A műfajt Greguss Ágost nyomán tragédia dalban elbeszélveként határozzuk meg, mert egyesíti a líra, epika és dráma sajátosságait...",
        "vazlat": "### I. Műfajelmélet: Líra, epika és dráma szintézise, balladai homály, ellipszis, sűrítés.\n### II. Nagykőrösi korszak: Történelmi ellenállás (A walesi bárdok, Szondi két apródja) és lélektan (Ágnes asszony lepedőmosása).\n### III. Őszikék (1877): Híd-avatás (nagyvárosi haláltánc).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. Nagykőrösi történelmi és lélektani balladák -> 3. Őszikék haláltánca -> 4. Összegzés.",
        "kviz": [{"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A három műnem találkozására utal."}]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus szintézise, polgári meghasonlás és a Senki szigete",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi", "Ali Csorbadzsi", "Krisztyán Tódor"],
        "audio_szoveg": "Jókai Mór 1872-es Az arany ember című regénye az író legszemélyesebb alkotása, melyben a romantika és realizmus elemei ötvöződnek...",
        "vazlat": "### I. Műfaj: Romantikus mesei fordulatok és realista társadalomrajz.\n### II. Timár meghasonlása: Anyagi siker vs. belső boldogtalanság.\n### III. Kettős világ: Komárom (Timea hideg hálája) vs. Senki szigete (Noémi tiszta szerelme).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1872 kontextusa -> 2. Timár jelleme -> 3. Két világmodell -> 4. Balatoni feloldás.",
        "kviz": [{"k": "A Senki szigete pénzmentes természeti utópia a regényben.", "v": True, "m": "A társadalmi konvenciókon kívül áll."}]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény műfaja, eszmék küzdelme és az Úr zárszava",
        "kulcsszavak": ["Drámai költemény", "15 szín", "Ádám, Éva, Lucifer", "Párizs", "London"],
        "audio_szoveg": "Madách Imre Az ember tragédiája című drámai költeménye 1859-60-ban született, vizsgálva az emberi lét és a történelem végső értelmét...",
        "vazlat": "### I. Műfaj: Világdráma hegel-i dialektikával.\n### II. Karakterek: Ádám (hit és tett), Lucifer (hideg ráció), Éva (élet és érzelem).\n### III. Történelem: Párizs (Danton hite) és London (haláltánc). Zárszó: „Küzdj és bízva bízzál!”",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Műfaji sajátosságok -> 2. Szereplők hármassága -> 3. Párizsi és londoni szín -> 4. 15. szín katarzisa.",
        "kviz": [{"k": "Ádám a párizsi színből kiábrándultan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel tér magához."}]
    },
    "4. Mikszáth Kálmán prózája": {
        "alcim": "Anekdotizmus, A tót atyafiak, A jó palócok és a Beszterce ostroma",
        "kulcsszavak": ["Anekdota", "A tót atyafiak", "A jó palócok", "Beszterce ostroma", "Pongrácz István"],
        "audio_szoveg": "Mikszáth Kálmán a 19. és 20. század fordulójának legnagyobb magyar mesélője, akinek művészete az anekdotára épül...",
        "vazlat": "### I. Stílus: Anekdotizmus, szelíd irónia.\n### II. Novellák: A tót atyafiak (4 hosszú elbeszélés) vs. A jó palócok (15 rövid novella).\n### III. Beszterce ostroma: Pongrácz István Don Quijote-i alakja és a dzsentri válság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Anekdotikus stílus -> 2. Két novelláskötet párhuzama -> 3. Pongrácz István Don Quijote-i szerepe -> 4. Összegzés.",
        "kviz": [{"k": "Pongrácz István középkori lovagként rendezi be életét Nedec várában.", "v": True, "m": "Anakronisztikus nemesi figura."}]
    },
    "5. Vajda János költészete": {
        "alcim": "A lírai magány mítosza, a Gina-szerelem és a szimbolizmus előfutára",
        "kulcsszavak": ["Gina-versek", "Montblanc", "A vaáli erdőben", "A virrasztók"],
        "audio_szoveg": "Vajda János a kiegyezés korának legmagányosabb költője, aki a Gina-szerelem és a panteista tájlíra mestere volt...",
        "vazlat": "### I. Magány és társadalmi kiábrándulás (A virrasztók).\n### II. Gina-líra: Húsz év múlva (Montblanc-metafora: jég és láva).\n### III. Csend-líra: A vaáli erdőben (panteista megnyugvás).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Gina-szerelem és a Montblanc-kép -> 3. A vaáli erdőben panteizmusa -> 4. Hatása Adyra.",
        "kviz": [{"k": "A Montblanc-metafora a Húsz év múlva című költemény központi képe.", "v": True, "m": "A fagyos hegy és a belső tűz ellentéte."}]
    },
    "6. XIX. századi dráma: Ibsen és Csehov": {
        "alcim": "Az analitikus dráma (Nóra) és a csehovi hangulatdráma (Sirály, Cseresznyéskert)",
        "kulcsszavak": ["Henrik Ibsen", "Analitikus dráma", "Nóra", "Anton Csehov", "Sirály", "Cseresznyéskert"],
        "audio_szoveg": "A 19. század végén Henrik Ibsen analitikus drámája és Anton Csehov hangulatdrámája forradalmasította a színházat...",
        "vazlat": "### I. Ibsen: Analitikus technika (a múlt titkainak lelepleződése); Nóra női emancipációja.\n### II. Csehov: Hangulatdráma; cselekvésképtelenség, párhuzamos monológok (Sirály, Cseresznyéskert).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Polgári dráma megújulása -> 2. Ibsen analitikája (Nóra) -> 3. Csehov hangulatteremtése -> 4. Színháztörténeti hatás.",
        "kviz": [{"k": "Ibsen darabjaiban a múltban rejtőző titkok robbantják ki a konfliktust.", "v": True, "m": "Ez az analitikus dramaturgia lényege."}]
    },
    "7. A Nyugat folyóirat": {
        "alcim": "A modern magyar irodalom indulása 1908-ban, szerkesztők és a 3 nemzedék",
        "kulcsszavak": ["1908", "Osvát Ernő", "Ignotus", "Mikes-emlékérem", "Három nemzedék"],
        "audio_szoveg": "1908. január 1-jén indult a Nyugat folyóirat, amely a magyar kultúra legfontosabb irodalmi műhelyévé vált...",
        "vazlat": "### I. Indulás: 1908–1941; Mikes-emlékérem, művészi függetlenség.\n### II. Szerkesztők: Ignotus, Osvát Ernő, Hatvany Lajos.\n### III. Nemzedékek: 1. nemzedék (Ady, Babits, Kosztolányi, Móricz), 2. nemzedék (Szabó Lőrinc), 3. nemzedék (Radnóti).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1908 jelentősége -> 2. Osvát Ernő szerkesztői szerepe -> 3. Három nemzedék íve -> 4. Kánonképző hatás.",
        "kviz": [{"k": "A Nyugat folyóirat 1908 és 1941 között működött.", "v": True, "m": "Babits Mihály haláláig létezett."}]
    },
    "8. Ady Endre költészete": {
        "alcim": "Szimbolizmus, magyarságtudat, lírai párharc és háborús apokalipszis",
        "kulcsszavak": ["Új versek 1906", "A magyar Ugaron", "Léda vs. Csinszka", "Harc a Nagyúrral"],
        "audio_szoveg": "Ady Endre 1906-os Új versek című kötetével megteremtette a modern magyar szimbolista költészetet...",
        "vazlat": "### I. 1906: Új versek kötetkompozíciója, ars poetica (Góg és Magóg fia vagyok én...).\n### II. Témák: Ugar-versek (elmaradottság), Pénz-versek (Harc a Nagyúrral), Szerelem (Léda vs. Csinszka).\n### III. Háborús líra: Ember az embertelenségben.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1906 költői forradalma -> 2. Ugar és Disznófejű Nagyúr toposz -> 3. Léda és Csinszka -> 4. Háborús humánum.",
        "kviz": [{"k": "Ady korszakalkotó kötete az Új versek 1906-ban jelent meg.", "v": True, "m": "Ez nyitotta meg a modern magyar lírát."}]
    },
    "9. Babits Mihály: Jónás könyve": {
        "alcim": "A prófétai szerep, a morális felelősségvállalás és a Jónás imája",
        "kulcsszavak": ["Jónás könyve", "Jónás imája", "Ninive", "Cinkos, aki néma", "1938"],
        "audio_szoveg": "Babits Mihály 1938-ban írta meg a Jónás könyvét a gégerákja és a fasizmus fenyegetése idején...",
        "vazlat": "### I. 1938: Babits betegsége és a fasizmus fenyegetése; bibliai parafrázis groteszk elemekkel.\n### II. Jónás útja: Menekülés -> Cethal (megtisztulás) -> Ninive intése -> Kegyelem diadala.\n### III. Alaptétel: „Mert vétkesek közt cinkos, aki néma.” és a Jónás imája.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1938 válsága -> 2. Jónás emberi gyarlósága -> 3. Ninive etikai parancsa -> 4. Jónás imája.",
        "kviz": [{"k": "A Jónás könyve központi szállóigéje: 'Mert vétkesek közt cinkos, aki néma'.", "v": True, "m": "Az értelmiségi felelősségvállalás parancsa."}]
    },
    "10. Móricz Zsigmond prózája": {
        "alcim": "A paraszti és dzsentri világ naturalista és kritikai ábrázolása (Tragédia, Barbárok, Úri muri)",
        "kulcsszavak": ["Naturalizmus", "Tragédia", "Barbárok", "Úri muri", "Szakhmáry Zoltán"],
        "audio_szoveg": "Móricz Zsigmond szakított a hamis népi idillel, és a valóságot a maga kíméletlen ösztönvilágában mutatta be...",
        "vazlat": "### I. Stílusreform: Naturalizmus, biológiai és társadalmi determináció.\n### II. Novellák: Tragédia (Kis János evése), Barbárok (pusztai gyilkosság a szíjért).\n### III. Dzsentri válság: Úri muri (Szakhmáry Zoltán önpusztítása).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szakítás a népiességgel -> 2. Kis János és a Barbárok -> 3. Úri muri csődje -> 4. Összegzés.",
        "kviz": [{"k": "A Tragédia című novellában Kis János a lakodalmi evésbe pusztul bele.", "v": True, "m": "A zsíros hús jelenti vesztét."}]
    },
    "11. Kosztolányi Dezső: Édes Anna": {
        "alcim": "A lélektani regény, a megalázottság tudattalan robbanása és a humanizmus",
        "kulcsszavak": ["Édes Anna", "Vizy család", "Moviszter doktor", "1919", "Freudizmus"],
        "audio_szoveg": "Kosztolányi Dezső 1926-os Édes Anna című regénye az elfojtott sérelmek tudattalan kitörésének lélektani remekműve...",
        "vazlat": "### I. Történelmi keret: 1919 nyara; Sigmund Freud pszichoanalízise.\n### II. Anna dehumanizálása: Mintagépként kezelik, Jancsi eldobja -> Kettős gyilkosság.\n### III. Moviszter doktor: A tiszta részvét és emberi méltóság hangja.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1919 és a lélektan -> 2. Anna tárgyiasítása -> 3. A gyilkosság motivációja -> 4. Moviszter üzenete.",
        "kviz": [{"k": "Moviszter doktor az egyetlen, aki emberi részvéttel tekint Annára.", "v": True, "m": "Ő képviseli a szerző humanista értékrendjét."}]
    },
    "12. Petőfi Sándor forradalmi látomásköltészete": {
        "alcim": "A romantikus látomáslíra, a világforradalom és az önfeláldozás mítosza",
        "kulcsszavak": ["Egy gondolat bánt engemet...", "A XIX. század költői", "Világforradalom", "Kánaán-toposz"],
        "audio_szoveg": "Petőfi Sándor költészetében a forradalmi látomáslíra az egyéni sors és a népszabadság küzdelmének legmagasabb szintézise...",
        "vazlat": "### I. Prófétai szerep: A XIX. század költői (a költő mint a nép vezére a szabadság Kánaánja felé).\n### II. Látomásos halálmítosz: Egy gondolat bánt engemet... (a lassú halál elutasítása, a csatamezei önfeláldozás vágya).\n### III. Politikai líra: Nemzeti dal (1848. március 15.).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Petőfi forradalmi szerepvállalása -> 2. A XIX. század költői prófétai küldetése -> 3. Egy gondolat bánt engemet látomása -> 4. Nemzeti dal.",
        "kviz": [{"k": "Petőfi 'Egy gondolat bánt engemet...' című versében a lassú, ágyban történő halált kívánja elkerülni.", "v": True, "m": "A csatamezőn, a szabadságharcban kívánt elesni."}]
    },
    "13. József Attila kései gondolati lírája": {
        "alcim": "A létösszegzés, a magány és a társadalmi felelősségvállalás versei",
        "kulcsszavak": ["A Dunánál", "Eszmélet", "Téli éjszaka", "Kései sirató", "Karóval jöttél..."],
        "audio_szoveg": "József Attila a 20. századi magyar költészet legmélyebb filozófiai gondolkodója. Kései verseiben a személyes tragédiát az egyetemes emberi léttel egyesítette...",
        "vazlat": "### I. Történelemfilozófia: A Dunánál (magyar és közép-európai népek megbékélése, múlt-jelen-jövő egysége).\n### II. Lételméleti ciklus: Eszmélet (a determináció és a szabadság feszültsége).\n### III. Kései önmegszólító líra: Karóval jöttél..., Tudod, hogy nincs bocsánat.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. József Attila élethelyzete a 30-as években -> 2. A Dunánál megbékélési programja -> 3. Eszmélet létfilozófiája -> 4. Kései önmegszólító versek.",
        "kviz": [{"k": "A Dunánál című költemény a közép-európai népek történelmi megbékélését hirdeti.", "v": True, "m": "„A harcot, amelyet őseink vívtak, békévé oldja az emlékezés.”"}]
    },
    "14. Radnóti Miklós háborús ecloga-költészete": {
        "alcim": "A klasszicizáló forma mint a barbárság elleni menedék a bori noteszben",
        "kulcsszavak": ["Eclogák", "Bori notesz", "Hetedik ecloga", "Erőltetett menet", "Razglednicák"],
        "audio_szoveg": "Radnóti Miklós költészete a második világháború borzalmai közepette a klasszikus antik forma fegyelmével őrizte meg az emberi méltóságot...",
        "vazlat": "### I. Antik hagyomány: Vergiliusi ecloga-forma hexameterben; idill és pusztulás kontrasztja.\n### II. A lágerköltészet: Hetedik ecloga (álom és ébrenlét), Erőltetett menet (a hazatérés reménye).\n### III. Bori notesz és Razglednicák: 4 képeslap a halálmenet állomásairól, Fanni iránti hűség.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszicizálódás a fasizmusban -> 2. Ecloga műfaj és a lágertapasztalat -> 3. Razglednicák stációi -> 4. A humanizmus győzelme.",
        "kviz": [{"k": "Radnóti Miklós utolsó verseit a bori notesz nevű füzetben találták meg a tömegsírban.", "v": True, "m": "A négy Razglednica a halálmenet dokumentuma."}]
    },
    "15. Vörösmarty Mihály: Csongor és Tünde és a Szózat": {
        "alcim": "A romantikus mesejáték filozófiája és a nemzeti identitás kiáltványa",
        "kulcsszavak": ["Csongor és Tünde", "Szózat (1836)", "Éj monológja", "Három vándor", "Nemzeti hűség"],
        "audio_szoveg": "Vörösmarty Mihály a magyar romantika vezéralakja. A Csongor és Tünde az emberi boldogságkeresés mély filozófiai drámája...",
        "vazlat": "### I. Csongor és Tünde (1830): A boldogságkeresés mesei és kozmikus szintje; A három vándor (Kalmár, Fejedelem, Tudós) tévútjai; Az Éj monológja (kozmikus elmúlás).\n### II. Szózat (1836): A nemzet himnikus kiáltványa; hűség a szülőföldhöz, a nagyszerű halál vagy jobb kor víziója.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Vörösmarty romantikája -> 2. Csongor és Tünde boldogságfilozófiája -> 3. Az Éj monológja -> 4. A Szózat nemzeti üzenete.",
        "kviz": [{"k": "A Csongor és Tündében az Éj monológja a világmindenség és az emberi törekvések múlandóságát hirdeti.", "v": True, "m": "„Sötét és semmi voltam: rámeredtem...”"}]
    },
    "16. Csokonai Vitéz Mihály felvilágosult lírája": {
        "alcim": "Stíluskettősség: klasszicizmus, rokokó és szentimentalizmus a Lilla-versekben",
        "kulcsszavak": ["A Reményhez", "A Magánossághoz", "Konstancinápoly", "Lilla-ciklus", "Rokokó"],
        "audio_szoveg": "Csokonai Vitéz Mihály a magyar felvilágosodás legtehetségesebb poétája, aki a debreceni kollégium szelleméből kiindulva az európai stílusirányzatok szintézisét teremtette meg...",
        "vazlat": "### I. Filozofikus költészet: Konstancinápoly, Az estve (természeti idill vs. társadalmi egyenlőtlenség).\n### II. Rokokó dallamosság: Lilla-dalok (Tartózkodó kérelem).\n### III. Szentimentalizmus és csalódás: A Reményhez (a tavaszi virágoskert és a téli puszta ellentéte), A Magánossághoz.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Felvilágosodás és Debrecen -> 2. Filozofikus versek természetszemlélete -> 3. Lilla-líra és A Reményhez -> 4. Stílusszintézis.",
        "kviz": [{"k": "A Reményhez című költemény a szentimentális kiábrándultság remeke.", "v": True, "m": "A remény csalfa istennőjétől való végső búcsú."}]
    },
    "17. Berzsenyi Dániel ódaköltészete": {
        "alcim": "A klasszicista forma és a romantikus életérzés feszültsége a niklai magányban",
        "kulcsszavak": ["A magyarokhoz I.", "A közelítő tél", "Horatiusi eszmények", "Nikla"],
        "audio_szoveg": "Berzsenyi Dániel a niklai remeteségből küldte el lángoló ódáit, amelyek a római Horatius formáit töltötték meg a nemzetféltés és a múlandóság feszültségével...",
        "vazlat": "### I. Nemzetféltő ódák: A magyarokhoz I. (a dicső múlt erkölcsei vs. a jelen erkölcsi züllése, a tölgy-metafora).\n### II. Elégico-ódák és a mulandóság: A közelítő tél (az ifjúság és a természet hervadása).\n### III. Horatiusi életbölcsesség: Osztályrészem (a megelégedés és a belső harmónia dicsérete).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A klasszicista forma és romantikus lélek -> 2. A magyarokhoz I. nemzetostorozása -> 3. A közelítő tél múlandósága -> 4. Nikla jelentősége.",
        "kviz": [{"k": "A magyarokhoz I. című versben a viharokat túlélt tölgy a magyar nemzet szimbóluma.", "v": True, "m": "A belső erkölcsi pusztulás veszélyére figyelmeztet."}]
    },
    "18. Zrínyi Miklós: Szigeti veszedelem": {
        "alcim": "A barokk eposz sajátosságai, a mártíromság és az athleta Christi eszménye",
        "kulcsszavak": ["Barokk eposz", "Szigeti veszedelem (1651)", "Athleta Christi", "Invocatio, Propositio"],
        "audio_szoveg": "Zrínyi Miklós hadvezér és költő 1651-ben írta meg a Szigeti veszedelmet dédapja, Zrínyi Miklós 1566-os szigetvári hősi haláláról...",
        "vazlat": "### I. Barokk eposzi kellékek: Invocatio (Szűz Máriához), Propositio (témamegjelölés), Csodás elemek (angyalok és démonok harca).\n### II. Teológiai keret: Isten büntetése a magyarok bűneiért a török hódítás, de a megtisztulás Zrínyi áldozatával valósul meg.\n### III. Zrínyi alakja: Az Athleta Christi (Krisztus katonája) eszménye; a kitörés és a vértanúhalál dicsősége.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Barokk eposz fogalma és kellékei -> 2. Dédapa hőstette Szigetváron -> 3. Athleta Christi eszménye -> 4. Politikai üzenet: Ne bántsd a magyart!",
        "kviz": [{"k": "A Szigeti veszedelem a magyar barokk irodalom legnagyobb eposza.", "v": True, "m": "15 énekből áll és a szigetvári ostromot dolgozza fel."}]
    },
    "19. Örkény István: Tóték és az egypercesek": {
        "alcim": "A groteszk és az abszurd ábrázolásmódja a 20. századi diktatúrák árnyékában",
        "kulcsszavak": ["Groteszk", "Tóték (1967)", "Őrnagy és Tót Lajos", "Dobozolás", "Egyperces novellák"],
        "audio_szoveg": "Örkény István a magyar groteszk próza megteremtője. A Tóték című kisregény és dráma a hatalomnak való kiszolgáltatottság és az emberi méltóság feladásának tragikomédiája...",
        "vazlat": """
### I. A groteszk esztétikai minősége
- A félelmetes és a nevetséges, a tragikus és a komikus egyidejű jelenléte.
### II. Tóték (1967)
- Kontextus: II. világháború, Mátraszentanna.
- Konfliktus: Az idegbeteg Őrnagy pihenni érkezik Tótékhoz, akik a fronton lévő fiuk életéért minden megaláztatást vállalnak (éjszakai dobozolás, margóvágó).
- Csattanó: A fiú már elesett a fronton; Tót végül a margóvágóval négybe vágja az Őrnagyot.
### III. Egyperces novellák
- Tömörség, a valóság képtelenségeinek leleplezése (*In memoriam dr. K. H. G.*, *Használati utasítás*).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Groteszk fogalma Örkénynél -> 2. Tóték cselekménye és a dobozolás szimbóluma -> 3. A margóvágó és a katarzis -> 4. Egypercesek világa.",
        "kviz": [{"k": "Tót Lajos a regény végén a margóvágóval négy egyforma darabba vágja az Őrnagyot.", "v": True, "m": "Ez az abszurd lázadás egyetlen lehetséges formája."}]
    },
    "20. Ottlik Géza: Iskola a határon": {
        "alcim": "A létezésfilozófiai regény, a zárt katonaiskola világa és a szavak nélküli összetartozás",
        "kulcsszavak": ["Kőszegi katonaiskola", "Medve Gábor, Bébé, Szulovszky", "A szavak elégtelensége", "Belső szabadság"],
        "audio_szoveg": "Ottlik Géza 1959-ben megjelent Iskola a határon című regénye a modern magyar próza alapműve, amely a kőszegi katonaiskolába bekerülő fiúk férfivá érését és a belső autonómia megőrzését mutatja be...",
        "vazlat": "### I. Szerkezet és elbeszélésmód: Többszólamú narráció (Bébé és Medve kéziratai), idősíkváltások.\n### II. A mechanizmus és a megaláztatás: A katonaiskola kegyetlen, zárt rendszere megsemmisíti a civil megszokásokat.\n### III. A túlélés etikája: A szavak nélküli szolidaritás és a belső szabadság megteremtése a megaláztatások dacára.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A regény keletkezése (1959) -> 2. Kőszegi katonaiskola világa -> 3. Bébé és Medve alakja -> 4. A szavak elégtelensége és a belső tartás.",
        "kviz": [{"k": "Az Iskola a határon című regény a kőszegi katonai alreáliskolában játszódik.", "v": True, "m": "A fiúk belső jellemfejlődésének zárt tere."}]
    },
    "21. Krúdy Gyula: Szindbád és a novellisztika": {
        "alcim": "Az impresszionista-szecessziós időszerkezet, az emlékek és az érzékek birodalma",
        "kulcsszavak": ["Szindbád-novellák", "Kulináris és szerelmi emlékek", "Időbontásos technika", "Szecesszió"],
        "audio_szoveg": "Krúdy Gyula a magyar próza legnagyobb varázslója. Szindbád-történeteiben az idő nem lineárisan halad, hanem az emlékek, ízek és szerelmek hullámain lebeg...",
        "vazlat": "### I. Az időkezelés forradalma: Bergsoni szubjektív időélmény; a múlt és jelen összefolyása.\n### II. Szindbád alakja: Az örök utazó, a női szívek meghódítója és a kulináris élvezetek lovagja.\n### III. Stílus: Impresszionista hangulatfestés, szecessziós ornamentika, nosztalgikus elmúlásérzet.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Krúdy stílusának egyedisége -> 2. Szindbád mitikus alakja -> 3. Időbontás és az érzékek szerepe -> 4. A magyar szecesszió csúcsa.",
        "kviz": [{"k": "Krúdy Szindbád-történeteiben az időélmény szubjektív és az emlékekre épül.", "v": True, "m": "A múlt és jelen folyamatosan egymásba csúszik."}]
    },
    "22. Illyés Gyula: Egy mondat a zsarnokságról és a Puszták népe": {
        "alcim": "A szociográfiai próza és a totalitárius diktatúra lélektanának monumentális költeménye",
        "kulcsszavak": ["Egy mondat a zsarnokságról (1950/1956)", "Puszták népe (1936)", "Népi írók mozgalma", "Diktatúra"],
        "audio_szoveg": "Illyés Gyula a magyar népi mozgalom vezéralakja volt. Munkásságának csúcsa a cselédsorsot bemutató Puszták népe és a kommunista diktatúra totális elnyomását feltáró Egy mondat a zsarnokságról...",
        "vazlat": "### I. Puszták népe (1936): Szociográfia és önéletrajz ötvözése; a dunántúli uradalmi cselédek zárt, feudális nyomorának feltárása.\n### II. Egy mondat a zsarnokságról (1950): Egyetlen monumentális körmondat; a zsarnokság nemcsak a börtönökben van, hanem beköltözik a szavakba, az intimitásba és a gondolatokba is.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Népi írók mozgalma -> 2. Puszták népe szociográfiája -> 3. Egy mondat a zsarnokságról totális hatalomrajza -> 4. Történelmi hatás.",
        "kviz": [{"k": "Az 'Egy mondat a zsarnokságról' című vers egyetlen monumentális mondatból épül fel.", "v": True, "m": "A diktatúra mindent átható jelenlétét mutatja be."}]
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
        "vazlat": "### I. Jakobson-modell: Adó, Vevő, Üzenet, Kód, Csatorna, Kontextus, Zaj.\n### II. Nyelvi funkciók: Tájékoztató, Érzelemkifejező, Felhívó, Fatikus (kapcsolattartó), Metanyelvi, Poétikai.\n### III. Nem nyelvi kódok: Gesztusok, mimika, proxemika (térköz).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. A 6 tényező -> 3. Nyelvi funkciók -> 4. Nonverbális jelek.",
        "kviz": [{"k": "A fatikus funkció célja a kapcsolat felvétele és fenntartása.", "v": True, "m": "Ilyenek a köszönések és bejelentkezések."}]
    },
    "2. A szövegtan alapjai és a szövegtípusok": {
        "alcim": "A szöveg kohéziós erői, szerkezeti egységei és típusai",
        "kulcsszavak": ["Globális kohézió", "Lokális kohézió", "Anafora és Katafora", "Elbeszélő, leíró, érvelő"],
        "audio_szoveg": "A szöveg a nyelv legmagasabb szintű, lezárt, kerek egysége...",
        "vazlat": "### I. Kohézió: Lokális (kötőszók, anafora=visszautalás, katafora=előreutalás) vs. Globális (témamegtartás, kulcsszavak).\n### II. Szerkezet: Cím -> Bevezetés -> Tárgyalás -> Befejezés.\n### III. Típusok: Elbeszélő, leíró, érvelő, magyarázó.",
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
        "audio_szoveg": "A retorika az ékesszólás és meggyőzés művészete. Az érv három alapeleme a tétel, a bizonyíték és az összekötés...",
        "vazlat": "### I. Érv: Tétel -> Bizonyíték -> Összekötő elem.\n### II. Típusok: Meghatározásból levezetett, ok-okozati, tekintélyre hivatkozó, analógiás.\n### III. Szónoki beszéd: Exordium -> Narratio -> Divisio -> Confirmatio -> Refutatio -> Peroratio.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Retorika célja -> 2. Érv 3 része -> 3. Érvtípusok -> 4. Szónoki beszéd lépései.",
        "kviz": [{"k": "A klasszikus szónoki beszédben a cáfolás megelőzi a befejezést.", "v": True, "m": "A bizonyítás után jön a cáfolat."}]
    },
    "6. Stilisztika: Alakzatok és trópusok": {
        "alcim": "Költői képek (metafora, metonímia, szinesztézia) és szövegalakzatok",
        "kulcsszavak": ["Metafora, Metonímia, Szinekdoché", "Szinesztézia", "Anafora, Párhuzam, Ellentét"],
        "audio_szoveg": "A stilisztika a kifejezőeszközöket vizsgálja. Két fő ága a szóképek és a szövegalakzatok rendszere...",
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
        "audio_szoveg": "A magyar nyelv a finnugor nyelvcsalád tagja. Írásbeliségünk legrégebbi emléke a Halotti Beszéd...",
        "vazlat": "### I. Eredet: Finnugor nyelvcsalád; Tihanyi alapítólevél (1055, szórvány), Halotti Beszéd (1195, összefüggő).\n### II. Nyelvújítás (1790–1820): Kazinczy Ferenc; Neológusok vs. Ortológusok; új szavak alkotása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Finnugor rokonság -> 2. Korai nyelvemlékek -> 3. Nyelvújítás célja és Kazinczy szerepe.",
        "kviz": [{"k": "A Halotti Beszéd az első fennmaradt összefüggő magyar szövegemlék.", "v": True, "m": "1195 körül keletkezett."}]
    },
    "9. Fonetika: A hangok képzése és a mássalhangzótörvények": {
        "alcim": "Magánhangzók és mássalhangzók rendszere, hasonulás, összeolvadás, kiesés és rövidülés",
        "kulcsszavak": ["Zöngés és Zöngétlen", "Részleges és Teljes hasonulás", "Írásban jelölt és jelöletlen", "Összeolvadás"],
        "audio_szoveg": "A fonetika a beszédhangok képzését és egymásra hatását vizsgálja. A mássalhangzótörvények a kiejtés könnyítését szolgálják...",
        "vazlat": "### I. Hangrendszer: Magánhangzók (hangrendi illeszkedés: magas, mély, vegyes); Mássalhangzók (zöngés-zöngétlen párok: b-p, d-t, g-k, z-sz, zs-s, v-f, gy-ty, dz-ts, dzs-cs).\n### II. Mássalhangzótörvények: 1. Részleges hasonulás (zöngésségi: *vasgolyó [vazsgolyó]*, képzés helye szerinti: *színpad [szímpad]*), 2. Teljes hasonulás (írásban jelölt: *kézzel*, jelöletlen: *anyja [annya]*), 3. Összeolvadás (*barátság [baraccság]*), 4. Kiesés (*mondta [monta]*), 5. Rövidülés (*otthon [othon]*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hangok képzése és csoportosítása -> 2. Zöngésségi hasonulások -> 3. Teljes hasonulás és összeolvadás -> 4. Helyesírási következmények.",
        "kviz": [{"k": "A 'színpad' szó kiejtésekor [szímpad] a képzés helye szerinti részleges hasonulás érvényesül.", "v": True, "m": "A 'p' ajakhang miatt az 'n' hang 'm'-mé alakul."}]
    },
    "10. Morfológia: A szóelemek (morfémák) rendszere": {
        "alcim": "Tőmorfémák, toldalékmorfémák (képző, jel, rag) és a szóelemző helyesírás",
        "kulcsszavak": ["Szótő", "Képző (új szó)", "Jel (módosít)", "Rag (mondatba illeszt)", "Toldalékolási sorrend"],
        "audio_szoveg": "A morfológia vagy alaktan a nyelv legkisebb önálló jelentéssel vagy funkcióval bíró egységeit, a morfémákat vizsgálja...",
        "vazlat": "### I. Morfématípusok: 1. Tőmorféma (lexikális fogalmi jelentés), 2. Toldalékmorféma (nyelvtani funkció).\n### II. Toldalékok kötött sorrendje a magyarban: Szótő + KÉPZŐ + JEL + RAG (pl. *ház-as-ság-ok-at*).\n### III. Toldalékfajták: Képző (megváltoztatja a szófajt/jelentést), Jel (viszonyt fejez ki, pl. többesszám -k, múlt idő -t), Rag (lezárja a szót, mondatrészi szerepet jelöl ki, pl. tárgyrag -t).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Morféma fogalma -> 2. Szótő és toldalékok hármassága -> 3. A toldalékolás szigorú sorrendje -> 4. Példaelemzés.",
        "kviz": [{"k": "Egy szóalakhoz a rag után még kapcsolódhat képző a magyar nyelvben.", "v": False, "m": "A rag mindig lezárja a szóalakot, utána nem jöhet képző."}]
    },
    "11. Szóalkotási módok a magyar nyelvben": {
        "alcim": "Szóösszetétel, szóképzés, mozaikszók, szóelvonás, szóvegyülés és rövidülés",
        "kulcsszavak": ["Szóösszetétel (Szerves és Szervetlen)", "Szóképzés", "Mozaikszók (Betűszó és Szóösszevonás)", "Szóhasadás"],
        "audio_szoveg": "A magyar nyelv rendkívül gazdag belső szóalkotási mechanizmusokkal rendelkezik, amelyek biztosítják a szókészlet folyamatos gyarapodását...",
        "vazlat": "### I. Fő szóalkotási módok: 1. Szóképzés (képző hozzáadása), 2. Szóösszetétel (Alárendelő: alanyi, tárgyas, határozós, jelzős; Mellérendelő: ikerszók, szóismétlések).\n### II. Ritkább szóalkotási módok: Mozaikszók (Betűszó: *MÁV, ELTE*; Szóösszevonás: *GYSEV, Főgáz*), Szóelvonás (*kapa <- kapál*), Szóvegyülés (*csokor + bokréta = csokréta*), Szócsonkítás (*mozi, csoki*), Szóhasadás (*család - cseléd*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Belső szóteremtés jelentősége -> 2. Képzés és összetétel fajtái -> 3. Mozaikszók típusai -> 4. Ritkább módok.",
        "kviz": [{"k": "A 'MÁV' egy betűszó, míg a 'Főgáz' egy szóösszevonás.", "v": True, "m": "A betűszó kezdőbetűkből, a szóösszevonás szótagokból áll."}]
    },
    "12. Mondattan: Az összetett mondatok típusai": {
        "alcim": "Mellérendelő (kapcsolatos, ellentétes, választó, következtető, magyarázó) és alárendelő mondatok",
        "kulcsszavak": ["Mellérendelés", "Alárendelés (Főmondat és Mellékmondat)", "Utalószó és Kötőszó", "Sajátos jelentéstartalom"],
        "audio_szoveg": "Az összetett mondatok két vagy több tagmondat logikai és szintaktikai kapcsolatából jönnek létre...",
        "vazlat": "### I. Mellérendelő összetett mondatok (egyenrangú tagmondatok): 1. Kapcsolatos (*és, s, meg, is*), 2. Ellentétes (*de, azonban, mégis*), 3. Választó (*vagy, akár*), 4. Következtető (*ezért, tehát, így*), 5. Magyarázó (*hiszen, ugyanis, tudniillik*).\n### II. Alárendelő összetett mondatok (Főmondat + hiányzó mondatrészt kifejtő Mellékmondat): Alanyi, Állítmányi, Tárgyi, Határozói, Jelzői alárendelés; Sajátos jelentéstartalmak: feltételes, megengedő, célhatározói.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Összetett mondat fogalma -> 2. 5 mellérendelő típus kötőszavakkal -> 3. Alárendelő tagmondatok és utalószók -> 4. Elemzési módszertan.",
        "kviz": [{"k": "A 'Szakad az eső, ezért nem megyünk kirándulni' mondat következtető mellérendelés.", "v": True, "m": "Az 'ezért' kötőszó logikai következményt fejez ki."}]
    },
    "13. Stílusrétegek és a stílusérték": {
        "alcim": "Hivatalos, tudományos, publicisztikai, társalgási, szónoki és szépirodalmi stílus",
        "kulcsszavak": ["Stílusrétegek", "Denotatív és Konnotatív jelentés", "Közhely és Sallang", "Terminológia"],
        "audio_szoveg": "A stílus a nyelvi eszközök céltudatos kiválasztása és elrendezése a beszédhelyzetnek megfelelően...",
        "vazlat": "### I. Stílusrétegek: 1. Hivatalos (pontosság, sablonok, személytelenség), 2. Tudományos (szakszavak, objektivitás, logikus kifejtés), 3. Publicisztikai (meggyőzés, hatáskeltés, címadás művészete), 4. Társalgási (közvetlenség, szleng, nem nyelvi jelek), 5. Szépirodalmi (egyéni képgazdagság, esztétikum).\n### II. Stílusérték: Alapjelentés (*denotáció*) és Másodlagos hangulati érték (*konnotáció*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Stílus fogalma -> 2. Főbb stílusrétegek jellemzői -> 3. Denotatív vs. konnotatív jelentés -> 4. Stilisztikai hibák.",
        "kviz": [{"k": "A hivatalos stílusra a gazdag költői képek és szinesztéziák használata jellemző.", "v": False, "m": "A hivatalos stílus száraz, tárgyilagos és sablonos."}]
    },
    "14. Névtan (Onomasztika)": {
        "alcim": "Személynevek (keresztnevek, családnevek) és földrajzi nevek rendszere, eredete",
        "kulcsszavak": ["Családnevek típusai", "Földrajzi nevek helyesírása", "Keresztnévadás", "Etimológia"],
        "audio_szoveg": "A névtan a tulajdonnevek eredetét, jelentését és típusait kutató nyelvtudományi ág...",
        "vazlat": "### I. Személynevek: 1. Családnevek kialakulása a 14-15. században (Apai név: *Péterfi*, Származási hely: *Budai*, Foglalkozás: *Kovács, Szabó*, Külső/Belső tulajdonság: *Nagy, Kis, Fekete*, Etnikum: *Tóth, Horváth, Németh*), 2. Keresztnevek (névadási szokások, védőszentek).\n### II. Földrajzi nevek és helyesírásuk: Egyeleműek (*Duna*), Kételemű egybeírt (*Margitsziget*), Különírt típusok (*Fekete-tenger*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Névtan célja -> 2. Magyar családnevek 5 fő eredettípusa -> 3. Keresztnevek története -> 4. Földrajzi nevek helyesírása.",
        "kviz": [{"k": "A 'Kovács' családnév foglalkozásra utaló eredetű.", "v": True, "m": "A mesterségről elnevezett nevek egyik leggyakoribb példája."}]
    },
    "15. Frazeológia: Szólások, közmondások és szállóigék": {
        "alcim": "Állandósult szókapcsolatok fajtái, kulturális háttere és metaforikus jelentése",
        "kulcsszavak": ["Szólás (nem ítélet)", "Közmondás (élettapasztalat/ítélet)", "Szállóige (ismert szerző)", "Közhely"],
        "audio_szoveg": "A frazeológia a nyelv állandósult, kötött szókapcsolatait tanulmányozza...",
        "vazlat": "### I. Frazeologizmusok típusai:\n1. **Szólás:** Képszerű, átvitt értelmű kifejezés, amely nem alkot kerek mondatot (pl. *„feni a fogát valamire”, „kereket old”*).\n2. **Közmondás:** Kerek egész mondat, általános népi élettapasztalatot, erkölcsi tanulságot hordoz (pl. *„Ki korán kel, aranyat lel”, „Nem mind arany, ami fénylik”*).\n3. **Szállóige:** Ismert történelmi személyhez vagy irodalmi műhöz köthető aranyköpés (pl. *„A kocka el van vetve” - Caesar, „Mert vétkesek közt cinkos, aki néma” - Babits*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Állandósult szókapcsolatok fogalma -> 2. Szólás és közmondás éles elhatárolása -> 3. Szállóigék szerepe -> 4. Nyelvi gazdagság.",
        "kviz": [{"k": "A 'Nem mind arany, ami fénylik' kifejezés közmondás.", "v": True, "m": "Kerek egész mondat általános érvényű igazságtartalommal."}]
    },
    "16. Digitális kommunikáció és az infokommunikációs nyelv": {
        "alcim": "Az online nyelvhasználat (netnyelv), emotikonok, hipertext és a közösségi média hatása",
        "kulcsszavak": ["Netnyelv / Netspeak", "Hipertextualitás", "Multimodalitás", "Emotikon és Emoji", "Információs társadalom"],
        "audio_szoveg": "A digitális forradalom gyökeresen átalakította a mindennapi kommunikációs szokásainkat és nyelvhasználatunkat...",
        "vazlat": "### I. A digitális nyelvhasználat sajátosságai: Írott beszéltség (az írás és szóbeli lazaság fúziója), rövidítések, azonnali visszacsatolás.\n### II. Multimodalitás és emotikonok: Képek, hangok, videók és szöveg egybefonódása; Emojik mint az elveszett metakommunikáció és intonáció pótlói.\n### III. Nyelvművelési kérdések: Elszegényíti-e a nyelvet az online csetelés, vagy új kreatív kódrendszert teremt?",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Digitális kommunikáció jellemzői -> 2. Írott beszéltség fogalma -> 3. Emojik és nonverbális pótlékok -> 4. Pozitív és negatív hatások.",
        "kviz": [{"k": "Az online csetelésben az írott és a szóbeli kommunikáció stílusjegyei keverednek.", "v": True, "m": "Ezt nevezzük írott beszéltségnek."}]
    }
}

# -------------------------------------------------------------
# 3. TÖRTÉNELEM TÉTELTÁR (20 Tétel)
# -------------------------------------------------------------
tetelek_tortenelem = {
    "1. Az athéni demokrácia működése a Kr. e. V. században": {
        "alcim": "Szolón, Kleiszthenész reformjai, Periklész kora és a népgyűlés (ekklészia)",
        "kulcsszavak": ["Népgyűlés (Ekklészia)", "Cserépszavazás", "Sztratégosz", "Napidíj", "Periklész"],
        "audio_szoveg": "Az athéni demokrácia az ókori világ legfejlettebb népuralmi rendszere volt...",
        "vazlat": "### I. Fejlődés: Szolón (vagyoni osztályok) -> Kleiszthenész (10 phülé, cserépszavazás).\n### II. Periklész kora: Népgyűlés (Ekklészia) mint fő döntéshozó, 500-ak tanácsa (Bulé), 10 sztratégosz, napidíjak.\n### III. Korlátok: Nők, rabszolgák és metoikoszok kizárása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kialakulás állomásai -> 2. Intézményrendszer -> 3. Periklész napidíjai -> 4. Korlátok.",
        "kviz": [{"k": "Az athéni népgyűlés tagja lehetett minden szabad athéni férfi polgár.", "v": True, "m": "Közvetlen demokrácia volt."}]
    },
    "2. A Római Köztársaság válsága és a Principátus kialakulása": {
        "alcim": "A polgárháborúk kora, Caesar diktatúrája és Augustus principátusa",
        "kulcsszavak": ["Gracchusok", "Marius hadseregreformja", "Julius Caesar", "Augustus (Kr. e. 27)", "Pax Romana"],
        "audio_szoveg": "A Római Köztársaság a hódítások következtében mély társadalmi válságba került, amely a principátus egyeduralmához vezetett...",
        "vazlat": "### I. A köztársaság válsága: A parasztság tönkremenetele, rabszolgafelkelések (Spartacus), Marius zsoldoshadserege.\n### II. Julius Caesar diktatúrája: Kr. e. 48-44; naptárreform, veteránok letelepítése, március idusa (meggyilkolása).\n### III. Augustus principátusa (Kr. e. 27 - Kr. u. 14): Köztársasági formákba bújtatott monarchia (*princeps senatus*), Pax Romana, aranykor.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Válság okai -> 2. Caesar egyeduralma -> 3. Augustus rendszere (Principátus) -> 4. Pax Romana.",
        "kviz": [{"k": "Augustus nyíltan királlyá koronáztatta magát Rómában.", "v": False, "m": "Megtartotta a köztársasági látszatot (első polgárként uralkodott)."}]
    },
    "3. A középkori uradalom és a hűbériség rendszere": {
        "alcim": "Hűbéri lánc (feudalizmus), a jobbágyság kialakulása és a mezőgazdaság technikai fejlődése",
        "kulcsszavak": ["Senior és Vazallus", "Hűbéri lánc", "Jobbágytelek", "Két- és Háromnyomásos gazdálkodás", "Nehézeke"],
        "audio_szoveg": "A középkori Európa társadalmi és gazdasági rendszere a hűbériségen és az uradalmi gazdálkodáson alapult...",
        "vazlat": "### I. Hűbéri rendszer: Hűbérúr (senior) és Hűbéres (vazallus) kapcsolata; földbirtok (*feudum*) adományozása hűségért és katonai szolgálatért cserébe.\n### II. Az uradalom és jobbágyság: Majorság (földesúri kezelésű föld) és Jobbágytelkek; Jobbágyi szolgáltatások (robot, terményjáradék, ajándékok).\n### III. Agrártechnika: Kétnyomásos -> Háromnyomásos gazdálkodás (ugar, őszi, tavaszi), nehézeke, szügyhám, vízimalom.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Feudalizmus piramisa -> 2. Uradalmi felépítés -> 3. Jobbágyok kötelességei -> 4. Háromnyomásos rendszer forradalma.",
        "kviz": [{"k": "A háromnyomásos gazdálkodásban a szántóföld egyharmada mindig ugaron (pihenve) maradt.", "v": True, "m": "Őszi, tavaszi gabona és ugar váltotta egymást."}]
    },
    "4. Szent István államalapítása és az egyházszervezés": {
        "alcim": "A keresztény királyság megszilárdítása, vármegyerendszer és törvények",
        "kulcsszavak": ["Koppány (997)", "Koronázás (1000)", "10 egyházmegye", "Ispánok", "Tized"],
        "audio_szoveg": "Géza fejedelem után fia, István király 1000 karácsonyán felvette a keresztény királyi koronát...",
        "vazlat": "### I. Trónharc: Koppány legyőzése (997) -> Koronázás (1000/1001).\n### II. Egyház: 10 püspökség (Esztergom és Kalocsa érsekség), 10 falunként templom, tized.\n### III. Államszervezet: Királyi vármegyék, ispánok, magántulajdon védelme.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trónra jutás -> 2. Egyházszervezés -> 3. Vármegyerendszer -> 4. Törvények.",
        "kviz": [{"k": "Szent István 10 püspökséget alapított Magyarországon.", "v": True, "m": "Esztergom és Kalocsa érseki rangot kapott."}]
    },
    "5. Az Aranybulla és a rendi társadalom gyökerei (1222)": {
        "alcim": "II. András birtokpolitikája, a szerviensek mozgalma és a nemesi jogok rögzítése",
        "kulcsszavak": ["1222 Aranybulla", "Királyi szerviensek", "Adómentesség", "Birtokvédelem", "Ellenállási záradék"],
        "audio_szoveg": "II. András mértéktelen birtokadományozásai miatt a királyi szerviensek és várjobbágyok fellázadtak, kikényszerítve az 1222-es Aranybullát...",
        "vazlat": "### I. Előzmények: Egész vármegyék eladományozása -> a királyi hatalom és a szerviensek egzisztenciális gyengülése.\n### II. Az 1222-es Aranybulla főbb pontjai: Nemesi adómentesség, bírói ítélet nélkül tilos elfogni a nemest, katonáskodási kötelezettség csak az ország védelmére, méltóságok halmozásának tiltása, 31. cikkely: Ellenállási záradék (*ius resistendi*).\n### III. Jelentőség: A magyar nemesi szabadságjogok alapokmánya.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. II. András reformjai és a válság -> 2. Szerviensek mozgalma -> 3. Aranybulla legfőbb cikkelyei -> 4. Ellenállási záradék.",
        "kviz": [{"k": "Az Aranybulla 31. cikkelye feljogosította a nemeseket a királlyal szembeni fegyveres ellenállásra, ha az megszegi a törvényt.", "v": True, "m": "Ez volt a híres ellenállási záradék."}]
    },
    "6. Az Anjouk kora Magyarországon": {
        "alcim": "Károly Róbert gazdasági reformjai és Nagy Lajos 1351-es törvényei",
        "kulcsszavak": ["Bányabér (Urbura)", "Aranyforint", "Kapuadó", "1351 Ősiség és Kilenced"],
        "audio_szoveg": "Károly Róbert legyőzte a tartományurakat és stabil gazdasági reformokat vezetett be...",
        "vazlat": "### I. Károly Róbert: Bányabér (urbura), értékálló aranyforint, kapuadó, 1335 Visegrádi királytalálkozó.\n### II. Nagy Lajos (1351): Ősiség törvénye (aviticitas - elidegeníthetetlen nemesi birtok), Kilenced, Egy és ugyanazon nemesi szabadság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Károly Róbert gazdasági reformjai -> 2. Visegrádi csúcs -> 3. Nagy Lajos 1351-es törvényei -> 4. Lovagkirály kora.",
        "kviz": [{"k": "Az 1351-es ősiség törvénye védte a nemesi birtokot a felaprózódástól és eladástól.", "v": True, "m": "A nemzetségen belül maradt a föld."}]
    },
    "7. Hunyadi Mátyás uralkodása (1458–1490)": {
        "alcim": "Központosított monarchia, bevételek, Fekete sereg és a reneszánsz udvar",
        "kulcsszavak": ["Füstpénz", "Rendkívüli hadiadó", "Fekete sereg", "Corvinák", "Bécs bevétele"],
        "audio_szoveg": "Hunyadi Mátyás erős központosított királyi hatalmat épített ki gazdasági reformjai és zsoldoshadserege révén...",
        "vazlat": "### I. Pénzügyek: Füstpénz (háztartásonként), Rendkívüli hadiadó (évi 1-2 forint).\n### II. Hadsereg: Fekete sereg (Kinizsi Pál), déli végvárvonal, Bécs elfoglalása (1485).\n### III. Reneszánsz: Beatrix, Bibliotheca Corviniana, humanizmus Budán.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mátyás trónra lépése -> 2. Gazdasági bevételek -> 3. Fekete sereg és hadjáratok -> 4. Reneszánsz kultúra.",
        "kviz": [{"k": "Mátyás kapuadó helyett vezette be a füstpénzt.", "v": True, "m": "Így minden háztartás külön adózott."}]
    },
    "8. A mohácsi csata és az ország három részre szakadása (1526–1541)": {
        "alcim": "A Jagelló-kor gyengesége, Mohács tragédiája, kettős királyválasztás és Buda eleste",
        "kulcsszavak": ["1526. augusztus 29. Mohács", "Szapolyai János és I. Ferdinánd", "1541. augusztus 29. Buda", "Hódoltság"],
        "audio_szoveg": "1526. augusztus 29-én a mohácsi síkon a török sereg megsemmisítette a magyar haderőt, ami az ország három részre szakadásához vezetett...",
        "vazlat": "### I. Mohács (1526. augusztus 29.): II. Lajos halála, a déli védelem összeomlása.\n### II. Kettős királyválasztás: Szapolyai János (nemzeti párt) vs. Habsburg Ferdinánd polgárháborúja.\n### III. Buda eleste (1541. augusztus 29.): Szulejmán csellel elfoglalja Budát -> Három rész: 1. Királyi Magyarország (Habsburg), 2. Török Hódoltság (Oszmán), 3. Erdélyi Fejedelemség (Szapolyai-örökösök).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mohácsi vereség okai -> 2. Polgárháború a trónért -> 3. Buda török kézre kerülése (1541) -> 4. A három országrész berendezkedése.",
        "kviz": [{"k": "Buda 1541-es török elfoglalásával szakadt három részre a Magyar Királyság.", "v": True, "m": "Szulejmán szultán csellel vette be a várat."}]
    },
    "9. A Rákóczi-szabadságharc (1703–1711)": {
        "alcim": "A Habsburg abszolutizmus elleni felkelés, az ónodi trónfosztás és a szatmári béke",
        "kulcsszavak": ["Brezáni kiáltvány", "Kurucok és Labancok", "Ónodi országgyűlés (1707)", "Szatmári béke (1711)"],
        "audio_szoveg": "A török kiűzése utáni Habsburg elnyomás ellen II. Rákóczi Ferenc vezetésével bontakozott ki a magyar nemzet legnagyobb függetlenségi háborúja...",
        "vazlat": "### I. Kiváltó okok: Újszerzeményi Bizottság, fegyverváltság, protestánsüldözés. 1703: Brezáni kiáltvány (*Cum Deo pro Patria et Libertate*).\n### II. Főbb események: Kuruc hadisikerek, 1707 Ónodi országgyűlés (közteherviselés és a Habsburg-ház trónfosztása).\n### III. Hanyatlás és lezárás: Pestisjárvány, nemzetközi elszigetelődés. 1711: Szatmári kompromisszumos béke (amnesztia, rendi alkotmány megerősítése).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szabadságharc okai -> 2. Rákóczi társadalmi szövetsége -> 3. Ónodi trónfosztás -> 4. Szatmári béke kompromisszuma.",
        "kviz": [{"k": "Az 1707-es ónodi országgyűlésen mondták ki a Habsburg-ház trónfosztását.", "v": True, "m": "„Eb ura fakó, József császár nem királyunk!”"}]
    },
    "10. A felvilágosult abszolutizmus Magyarországon": {
        "alcim": "Mária Terézia és II. József rendeletei (Védővám, Urbárium, Ratio Educationis, Türelmi rendelet)",
        "kulcsszavak": ["Mária Terézia", "Kettős vámrendelet (1754)", "Urbárium (1767)", "II. József kalapos király", "Türelmi rendelet (1781)"],
        "audio_szoveg": "A 18. században a Habsburg uralkodók a felvilágosodás eszméit felhasználva, rendeleti úton modernizálták a birodalmat...",
        "vazlat": "### I. Mária Terézia (1740–1780): Kettős vámrendelet (1754 - mezőgazdasági szerepbe szorította Magyarországot), Urbárium (1767 - jobbágyi terhek maximálása), Ratio Educationis (1777 - állami oktatási reform).\n### II. II. József (1780–1790): Kalapos király (nem koronáztatja meg magát); Türelmi rendelet (1781 - szabad vallásgyakorlat protestánsoknak), Jobbágyrendelet (1785 - szabad költözés), Nyelvrendelet (német nyelv erőltetése -> nemzeti ellenállás); halálos ágyán visszavonja rendeleteit a türelmi és jobbágyrendelet kivételével.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Felvilágosult abszolutizmus fogalma -> 2. Mária Terézia rendeletei -> 3. II. József radikális reformjai -> 4. Hatása a magyar nemzeti ébredésre.",
        "kviz": [{"k": "II. József a kalapos király nevet kapta, mert nem koronáztatta meg magát a magyar Szent Koronával.", "v": True, "m": "Hogy ne kelljen felesküdnie a magyar rendi alkotmányra."}]
    },
    "11. A reformkor fő kérdései (1830–1848)": {
        "alcim": "Széchenyi István és Kossuth Lajos reformprogramjának összehasonlítása",
        "kulcsszavak": ["Hitel (1830)", "Örökváltság", "Közteherviselés", "Pesti Hírlap", "Érdekegyesítés"],
        "audio_szoveg": "A magyar reformkor 1830-ban Széchenyi Hitel című művével vette kezdetét...",
        "vazlat": "### I. Széchenyi programja: 1830 Hitel; ősiség eltörlése, lassú szerves reformok az arisztokráciával a birodalmon belül; Lánchíd, Vaskapu, MTA.\n### II. Kossuth programja: Pesti Hírlap (1841); kötelező örökváltság állami kárpótlással, közteherviselés, nemesi és jobbágyi érdekegyesítés, sajtószabadság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Reformkor fogalma -> 2. Széchenyi gazdasági programja -> 3. Kossuth érdekegyesítése -> 4. A két reformer vitája.",
        "kviz": [{"k": "Kossuth a kötelező örökváltságot követelte állami kárpótlással.", "v": True, "m": "A jobbágyság azonnali polgárosodásáért küzdött."}]
    },
    "12. Az 1848–49-es forradalom és szabadságharc": {
        "alcim": "Március 15., az Áprilisi törvények és a Tavaszi hadjárat sikerei",
        "kulcsszavak": ["12 pont", "Áprilisi törvények (1848)", "Batthyány Lajos", "Görgei Artúr", "Függetlenségi Nyilatkozat"],
        "audio_szoveg": "1848 tavaszán a pesti forradalom és az Áprilisi törvények szentesítése polgári Magyarországot teremtett...",
        "vazlat": "### I. 1848. március 15. és Áprilisi törvények (ápr. 11.): Független felelős minisztérium (Batthyány), jobbágyfelszabadítás, közteherviselés, sajtószabadság.\n### II. Önvédelmi háború és Tavaszi hadjárat (1849): Görgei dicsőséges hadjárata, Buda visszavétele; 1849. ápr. 14. Függetlenségi Nyilatkozat.\n### III. Leverés: Orosz cári intervenció -> 1849. aug. 13. Világosi fegyverletétel.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Március 15. és törvények -> 2. Batthyány kormánya -> 3. Tavaszi hadjárat és trónfosztás -> 4. Cári beavatkozás és bukás.",
        "kviz": [{"k": "A Batthyány-kormány volt az első független felelős magyar kormány.", "v": True, "m": "1848 áprilisában alakult meg."}]
    },
    "13. A dualizmus kora Magyarországon (1867–1914)": {
        "alcim": "A Kiegyezés rendszere, gazdasági felvirágzás és társadalmi rétegződés",
        "kulcsszavak": ["Kiegyezés (1867)", "Deák Ferenc", "Közös ügyek", "Gazdasági csoda", "Torlódó társadalom"],
        "audio_szoveg": "Az 1867-es kiegyezéssel létrejött az Osztrák-Magyar Monarchia...",
        "vazlat": "### I. Államszervezet: Ferenc József; Közös ügyek (Külügy, Hadügy, Pénzügy); Vámunió, közös valuta (korona).\n### II. Gazdaság: Vasútépítés (Baross Gábor), malomipar és gépgyártás csúcsa, Millennium (1896).\n### III. Torlódó társadalom: Régi feudális nemesi réteg és új polgári kapitalista réteg együttélése.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kiegyezés közös ügyei -> 2. Gazdasági robbanás -> 3. Torlódó társadalom -> 4. Nemzetiségi kérdés.",
        "kviz": [{"k": "A dualizmus korában a külügy és hadügy közös minisztériumokhoz tartozott.", "v": True, "m": "A pénzügy finanszírozta őket."}]
    },
    "14. Az első világháború és következményei (1914–1918)": {
        "alcim": "A szövetségi rendszerek, az állóháború jellege és a hátország összeomlása",
        "kulcsszavak": ["Szarajevói merénylet (1914)", "Antant és Hármasszövetség", "Állóháború / Lövészárok", "Verdun és Somme"],
        "audio_szoveg": "Az imperialista nagyhatalmi ellentétek 1914-ben a Ferenc Ferdinánd elleni szarajevói merénylettel robbantották ki a Nagy Háborút...",
        "vazlat": "### I. Hadviselő felek: Antant (Nagy-Britannia, Franciaország, Oroszország, később USA) vs. Központi Hatalmak (Németország, Osztrák-Magyar Monarchia, Oszmán Birodalom).\n### II. Hadviselés jellege: Villámháborús tervek kudarca -> Éveken át tartó pusztító állóháború (lövészárkok, gáztámadások, tankok, géppuskák: Verdun, Somme).\n### III. Összeomlás: Orosz forradalmak (1917), USA belépése, a hátországok gazdasági és társadalmi kimerülése -> 1918. november fegyverszünetek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Háború okai és szövetségek -> 2. Állóháború technikai jellege -> 3. Fordulópontok (1917) -> 4. Monarchia szétesése.",
        "kviz": [{"k": "Az I. világháborúban az Egyesült Államok 1917-ben lépett be az Antant oldalán.", "v": True, "m": "A korlátlan tengeralattjáró-háború és a Lusitania elsüllyesztése miatt."}]
    },
    "15. A Horthy-korszak konszolidációja (1920–1931)": {
        "alcim": "Trianon traumája, a bethleni konszolidáció és Klebelsberg kultúrpolitikája",
        "kulcsszavak": ["Trianon (1920. jún. 4.)", "Bethlen István", "Pengő (1927)", "Klebelsberg Kuno"],
        "audio_szoveg": "Az I. világháború és a Trianoni békediktátum után gróf Bethlen István vezetésével stabilizálódott az ország...",
        "vazlat": "### I. Trianoni béke (1920. jún. 4.): Ország 2/3 része elcsatolva, 3,3 millió magyar határon kívül.\n### II. Bethleni konszolidáció: Bethlen-Peyer paktum, Népszövetségi kölcsön (1924), Pengő (1927).\n### III. Kultúra: Klebelsberg Kuno népiskolái (5000 tanterem), szegedi és debreceni egyetemek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trianoni sokk -> 2. Bethlen gazdasági stabilitása (Pengő) -> 3. Klebelsberg iskolafejlesztése -> 4. Külpolitikai kitörés.",
        "kviz": [{"k": "1927-ben vezették be az új értékálló magyar valutát, a Pengőt.", "v": True, "m": "A korona elértéktelenedése után stabilizálta a piacot."}]
    },
    "16. A második világháború főbb fordulópontjai (1939–1945)": {
        "alcim": "A náci agresszió, a szövetségesek koalíciója, Sztálingrád, D-nap és a holokauszt",
        "kulcsszavak": ["1939. szept. 1. Lengyelország", "Sztálingrád (1942-43)", "Normandiai partraszállás (1944. jún. 6.)", "Holokauszt"],
        "audio_szoveg": "A náci Németország lengyelországi lerohanásával 1939-ben kitört a világtörténelem legpusztítóbb háborúja...",
        "vazlat": "### I. A tengelyhatalmak terjeszkedése (1939–1941): Lengyelország lerohanása, Franciaország veresége, Szovjetunió megtámadása (Barbarossa), Pearl Harbor (USA belépése).\n### II. Fordulópontok: Sztálingrádi csata (1942/43 - a keleti front összeomlása), El-Alamein, Kurszki páncéloscsata.\n### III. A náci rendszer bukása és a Holokauszt: 1944. június 6. D-nap (Normandia); 6 millió zsidó ember iparszerű megsemmisítése; 1945. május 8. európai kapituláció, augusztusi atomtámadások (Hirosima, Nagaszaki).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Háború kitörése és villámháborúk -> 2. Sztálingrádi és csendes-óceáni fordulat -> 3. Normandiai partraszállás és holokauszt -> 4. Befejezés és következmények.",
        "kviz": [{"k": "A sztálingrádi csata (1942-1943) jelentette a II. világháború döntő fordulatát Európában.", "v": True, "m": "A német 6. hadsereg megsemmisült."}]
    },
    "17. Magyarország a második világháborúban (1941–1945)": {
        "alcim": "Revíziós sikerek, belépés a háborúba, a doni katasztrófa, a német megszállás és a nyilas terror",
        "kulcsszavak": ["Bécsi döntések", "Teleki öngyilkossága", "2. magyar hadsereg (Don-kanyar)", "1944. márc. 19. Német megszállás", "Szálasi nyilas uralma"],
        "audio_szoveg": "Magyarország a revíziós sikerek áraként sodródott bele a tengelyhatalmak oldalán a második világháborúba...",
        "vazlat": "### I. Út a háborúba: Bécsi döntések (Felvidék, Észak-Erdély visszacsatolása) -> Teleki Pál tragikus öngyilkossága Jugoszlávia megtámadásakor -> Bárdossy hadba lépése Kassa bombázása után (1941. június).\n### II. A doni katasztrófa (1943. január): A 200 ezer fős 2. magyar hadsereg megsemmisülése a Don-kanyarban.\n### III. Megszállás és nyilas uralom: Kállay hintapolitikája -> 1944. március 19. Margarethe-hadművelet (német megszállás), a vidéki zsidóság deportálása Auschwitzba; Horthy sikertelen kiugrási kísérlete (1944. okt. 15.) -> Szálasi nyilas rémuralma, Budapest ostroma.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Revízió és hadbalépés -> 2. Doni tragédia -> 3. Német megszállás és a holokauszt -> 4. Kiugrási kudarc és nyilas terror.",
        "kviz": [{"k": "A 2. magyar hadsereg 1943 januárjában a Don-kanyarban szenvedett katasztrofális vereséget.", "v": True, "m": "Több mint százezer magyar katona esett el vagy fagyott meg."}]
    },
    "18. A hidegháború kialakulása és korszakai (1945–1991)": {
        "alcim": "Kétpólusú világ, fegyverkezési verseny, Truman-doktrína, kubai rakétaválság és a Szovjetunió felbomlása",
        "kulcsszavak": ["Vasfüggöny", "Truman-doktrína és Marshall-terv", "NATO vs. Varsói Szerződés", "Kubai válság (1962)", "Gorbacsov"],
        "audio_szoveg": "A II. világháború után a világ két ellenséges szuperhatalmi blokkra szakadt az Egyesült Államok és a Szovjetunió vezetésével...",
        "vazlat": "### I. A kétpólusú világ születése: Jalta és Potsdam; Churchill fultoni beszéde (1946 - *Vasfüggöny*); Truman-doktrína (feltartóztatás) és Marshall-terv; NATO (1949) és Varsói Szerződés (1955).\n### II. Válsággócok: Koreai háború (1950-53), Berlini fal építése (1961), Kubai rakétaválság (1962 - az atomháború küszöbén), Vietnami háború.\n### III. Enyhülés és összeomlás: Fegyverzetkorlátozási tárgyalások (SALT); Mihail Gorbacsov reformjai (*peresztrojka, glasznoszty*), a szocialista blokk összeomlása (1989), a Szovjetunió felbomlása (1991).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kétpólusú világmodell -> 2. Katonai és gazdasági tömbök -> 3. Kubai válság -> 4. Szovjetunió gazdasági csődje és a hidegháború vége.",
        "kviz": [{"k": "A kubai rakétaválság (1962) idején állt a világ a legközelebb egy közvetlen amerikai-szovjet atomháborúhoz.", "v": True, "m": "Kennedy és Hruscsov végül kompromisszumot kötött."}]
    },
    "19. Az 1956-os forradalom és szabadságharc": {
        "alcim": "A Rákosi-diktatúra válsága, október 23., Nagy Imre kormánya és a szovjet intervenció",
        "kulcsszavak": ["MEFESZ", "16 pont", "Október 23.", "Nagy Imre", "Corvin köz", "November 4. Invázió"],
        "audio_szoveg": "1956. október 23-án a budapesti diákok tüntetésével indult a magyar nép szabadságharca a szovjet elnyomás ellen...",
        "vazlat": "### I. Előzmények: Rákosi terrorja, ÁVH, koncepciós perek. Okt. 23. Békés tüntetés -> Rádió ostroma.\n### II. Győzelem: Nagy Imre kormánya, ÁVH feloszlatása, többpártrendszer, semlegesség és kilépés a Varsói Szerződésből (nov. 1.).\n### III. Leverés: November 4. szovjet tankok támadása (*Forgószél*); Nagy Imre és mártírtársai kivégzése (1958).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Rákosi válsága -> 2. Október 23. forradalma -> 3. Nagy Imre reformjai és semlegesség -> 4. Szovjet invázió és megtorlás.",
        "kviz": [{"k": "Magyarország 1956. november 1-jén kikiáltotta semlegességét és kilépését a Varsói Szerződésből.", "v": True, "m": "Nagy Imre jelentette be."}]
    },
    "20. A rendszerváltás folyamata Magyarországon (1989–1990)": {
        "alcim": "A Kádár-rendszer válsága, az Ellenzéki Kerekasztal, Nagy Imre újratemetése és a szabad választások",
        "kulcsszavak": ["Ellenzéki Kerekasztal (EKA)", "1989. jún. 16. Újratemetés", "1989. okt. 23. Köztársaság", "1990 Szabad választások"],
        "audio_szoveg": "1989-1990-ben békés tárgyalások útján alakult át a kommunista diktatúra demokratikus jogállammá és piacgazdasággá...",
        "vazlat": "### I. Kádár-rendszer csődje: Gazdasági eladósodás, ellenzéki pártok születése (MDF, Fidesz, SZDSZ, FKgP).\n### II. 1989 eseményei: Ellenzéki Kerekasztal (EKA); Nagy Imre újratemetése (jún. 16.); Határnyitás az NDK menekülteknek; Köztársaság kikiáltása (okt. 23.).\n### III. 1990: Első szabad választások -> Antall József kormánya, többpártrendszer megszilárdulása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kádár-rendszer válsága -> 2. Ellenzéki Kerekasztal -> 3. 1989 kulcsdátumai -> 4. 1990-es választások.",
        "kviz": [{"k": "1989. október 23-án kikiáltották a harmadik Magyar Köztársaságot.", "v": True, "m": "Szűrös Mátyás hirdette ki a Parlament erkélyéről."}]
    }
}

# -------------------------------------------------------------
# 4. MATEMATIKA TÉTELTÁR (16 Témakör)
# -------------------------------------------------------------
tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció és kombináció",
        "kulcsszavak": ["Metszet, Unió, Különbség", "Venn-diagram", "Permutáció ($n!$)", "Kombináció ($\binom{n}{k}$)"],
        "audio_szoveg": "A halmazelmélet és a kombinatorika a modern matematika alapvető eszköztára a kiválasztási és sorrendezési feladatok megoldásához...",
        "vazlat": "### I. Halmazműveletek: Unió (legalább az egyik), Metszet (mindkettő), Különbség (csak az egyik), Komplementer.\n### II. Kombinatorika:\n- Permutáció (sorba rendezés): Pn = n!\n- Variáció (kiválasztás, SORREND SZÁMÍT): V = n! / (n-k)!\n- Kombináció (kiválasztás, SORREND NEM SZÁMÍT): C = n alatt a k = n! / (k!(n-k)!).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Halmazok és műveletek -> 2. Permutáció képlete -> 3. Variáció vs. Kombináció (számít-e a sorrend?) -> 4. Lottópélda.",
        "kviz": [{"k": "Az 5-ös lottó kihúzásainak száma kombinációval számítható (90 alatt az 5).", "v": True, "m": "A golyók kihúzásának sorrendje nem számít."}]
    },
    "2. Algebra: Egyenletek, egyenlőtlenségek és másodfokú formula": {
        "alcim": "Megoldóképlet, diszkrimináns, gyöktényezős szorzat és Viéte-formulák",
        "kulcsszavak": ["Diszkrimináns ($b^2 - 4ac$)", "Megoldóképlet", "Gyöktényezős alak", "Kikötések"],
        "audio_szoveg": "A másodfokú egyenletek megoldásának alapeszköze a megoldóképlet és a diszkrimináns vizsgálata...",
        "vazlat": "### I. Megoldóképlet: x1,2 = (-b +- gyök(b^2 - 4ac)) / (2a).\n### II. Diszkrimináns (D = b^2 - 4ac): D > 0 (2 gyök), D = 0 (1 gyök), D < 0 (nincs valós gyök).\n### III. Gyöktényezős alak: a(x - x1)(x - x2) = 0. Kikötések: Nevező != 0, gyök alatt >= 0, logaritmus száma > 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kikötések fontossága -> 2. Másodfokú megoldóképlet és diszkrimináns -> 3. Gyöktényezős felbontás -> 4. Ellenőrzés kötelezettsége.",
        "kviz": [{"k": "Ha a diszkrimináns negatív, a másodfokú egyenletnek nincs valós gyöke.", "v": True, "m": "Valós számok körében negatívból nincs páros gyökvonás."}]
    },
    "3. Hatványozás, gyökvonás és a logaritmus azonosságai": {
        "alcim": "Hatványozási azonosságok, törtkitevő, logaritmus fogalma és műveleti szabályai",
        "kulcsszavak": ["$a^n \cdot a^m = a^{n+m}$", "Törtkitevő ($a^{m/n} = \sqrt[n]{a^m}$)", "Logaritmus azonosságok", "Alapáttérés"],
        "audio_szoveg": "A hatványozás és a logaritmus egymás inverz műveletei. A logaritmus azt a kitevőt adja meg, amelyre az alapot emelve megkapjuk a számot...",
        "vazlat": """
### I. Hatványozási azonosságok
- $a^n \cdot a^m = a^{n+m}$ és $\frac{a^n}{a^m} = a^{n-m}$
- $(a^n)^m = a^{n \cdot m}$ és $(a \cdot b)^n = a^n \cdot b^n$
- $a^{-n} = \frac{1}{a^n}$ és $a^0 = 1$ ($a \neq 0$)
- Törtkitevő: $a^{\frac{m}{n}} = \sqrt[n]{a^m}$

### II. Logaritmus azonosságai ($\log_a b = c \Leftrightarrow a^c = b$, ahol $a>0, a\neq 1, b>0$)
- $\log_a (x \cdot y) = \log_a x + \log_a y$
- $\log_a \left(\frac{x}{y}\right) = \log_a x - \log_a y$
- $\log_a (x^k) = k \cdot \log_a x$
- Alapáttérés: $\log_a b = \frac{\log_c b}{\log_c a}$
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hatványozás műveleti szabályai -> 2. Törtkitevő és negatív hatvány értelmezése -> 3. Logaritmus definíciója és kikötései -> 4. Logaritmus 3 fő azonossága.",
        "kviz": [{"k": "log2(8) értéke pontosan 3.", "v": True, "m": "Mert 2 a 3. hatványon egyenlő 8-cal."}]
    },
    "4. Függvénytan és analízis alapjai": {
        "alcim": "Lineáris, másodfokú, exponenciális, logaritmikus függvények és jellemzésük",
        "kulcsszavak": ["Értelmezési tartomány", "Értékkészlet", "Zérushely", "Szélsőérték", "Monotonitás"],
        "audio_szoveg": "A függvény egy egyértelmű hozzárendelés két halmaz között. Az érettségin alapvető elvárás a függvények teljes körű jellemzése...",
        "vazlat": "### I. Jellemzési lépések: Értelmezési tartomány (Df), Értékkészlet (Rf), Zérushely (f(x)=0), Szélsőérték (min/max helye és értéke), Monotonitás, Paritás.\n### II. Transzformációk: f(x)+c (függőleges eltolás), f(x-d) (vízszintes eltolás), c*f(x) (nyújtás/zsugorítás).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Függvény fogalma -> 2. Jellemzési szempontok sorrendje -> 3. Függvénytranszformációk -> 4. Másodfokú parabola csúcspontja.",
        "kviz": [{"k": "Az f(x) = (x - 4)^2 függvény minimuma az x = +4 pontban van.", "v": True, "m": "A zárójelen belüli -4 jobbra tolja el a csúcsot."}]
    },
    "5. Sorozatok és Pénzügyi matematika": {
        "alcim": "Számtani és mértani sorozat képletei, kamatos kamat és gyűjtőjáradék",
        "kulcsszavak": ["Differencia ($d$)", "Hányados ($q$)", "$n$-edik tag képlete", "Összegképlet ($S_n$)", "Kamatos kamat"],
        "audio_szoveg": "A számtani és mértani sorozatok törvényszerűségei alapozzák meg a pénzügyi kamatszámításokat...",
        "vazlat": "### I. Számtani sorozat (d): an = a1 + (n - 1)d, Sn = ((a1 + an) / 2) * n.\n### II. Mértani sorozat (q): an = a1 * q^(n - 1), Sn = a1 * (q^n - 1) / (q - 1).\n### III. Kamatos kamat: Cn = C0 * (1 + p/100)^n.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Számtani sorozat képletei -> 2. Mértani sorozat képletei -> 3. Kamatos kamat képlete és alkalmazása.",
        "kviz": [{"k": "Ha a1 = 5 és d = 3, akkor a számtani sorozat 10. tagja 32.", "v": True, "m": "a10 = 5 + 9 * 3 = 5 + 27 = 32."}]
    },
    "6. Síkgeometria és Trigonometria": {
        "alcim": "Pitagorasz-tétel, Szinusz- és Koszinusztétel, háromszögek területszámítása",
        "kulcsszavak": ["Pitagorasz-tétel", "Szögfüggvények (sin, cos, tg)", "Szinusztétel", "Koszinusztétel", "Területképletek"],
        "audio_szoveg": "A síkgeometria alapja a derékszögű és általános háromszögek szögfüggvényes összefüggéseinek alkalmazása...",
        "vazlat": "### I. Derékszögű háromszög: a^2 + b^2 = c^2, sin(alfa) = szemközti/átfogó, cos(alfa) = melletti/átfogó, tg(alfa) = szemközti/melletti.\n### II. Általános háromszög: Szinusztétel (a/sinA = b/sinB = 2R), Koszinusztétel (a^2 = b^2 + c^2 - 2bc*cosA).\n### III. Terület: T = (a * ma)/2 = (a*b*sinGamma)/2.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szögfüggvények definíciója -> 2. Szinusz- és Koszinusztétel alkalmazási feltételei -> 3. Területképletek.",
        "kviz": [{"k": "A koszinusztétel bármilyen általános háromszögre alkalmazható két oldal és a közbezárt szög ismeretében.", "v": True, "m": "Pitagorasz általánosítása."}]
    },
    "7. Síkgeometria: Sokszögek, kör és négyszögek tulajdonságai": {
        "alcim": "Szabályos sokszögek belső szögei, deltoid, rombusz, trapéz, kör ívhossza és körcikk területe",
        "kulcsszavak": ["Belső szögek összege ($(n-2)\cdot 180^\circ$)", "Átlók száma", "Trapéz területe", "Rombusz", "Körcikk területe"],
        "audio_szoveg": "A sokszögek és négyszögek geometriája az érettségi írásbeli vizsga egyik leggyakoribb feladattípusa...",
        "vazlat": """
### I. Konvex sokszögek
- **Belső szögek összege:** $S_n = (n - 2) \cdot 180^\circ$
- **Átlók száma:** $A_n = \frac{n(n - 3)}{2}$

### II. Négyszögek területei
- **Paralelogramma:** $T = a \cdot m_a = a \cdot b \cdot \sin\alpha$
- **Rombusz (átlók: $e, f$):** $T = \frac{e \cdot f}{2} = a \cdot m = a^2 \cdot \sin\alpha$
- **Trapéz (párhuzamos oldalak $a, c$, magasság $m$):** $T = \frac{a + c}{2} \cdot m$
- **Deltoid (merőleges átlók):** $T = \frac{e \cdot f}{2}$

### III. Kör részei
- **Kör kerülete és területe:** $K = 2r\pi$, $T = r^2\pi$
- **Ívhossz ($\alpha$ középponti szöghöz):** $i = \frac{2r\pi \cdot \alpha}{360^\circ}$
- **Körcikk területe:** $T_{\text{cikk}} = \frac{r^2\pi \cdot \alpha}{360^\circ} = \frac{i \cdot r}{2}$
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Belső szögek és átlók képletei -> 2. Négyszögek fajtái és területképletei -> 3. Kör és körcikk összefüggései.",
        "kviz": [{"k": "Egy konvex ötszög belső szögeinek összege pontosan 540 fok.", "v": True, "m": "(5 - 2) * 180 = 3 * 180 = 540 fok."}]
    },
    "8. Koordinátageometria": {
        "alcim": "Vektorműveletek, felezőpont, súlypont, az egyenes és a kör egyenlete",
        "kulcsszavak": ["Normálvektor $\\vec{n}(A, B)$", "Irányvektor $\\vec{v}(v_1, v_2)$", "Egyenes egyenlete", "Kör egyenlete"],
        "audio_szoveg": "A koordinátageometria segítségével algebrai egyenletekkel írhatunk le geometriai alakzatokat...",
        "vazlat": "### I. Alapok: Távolság (d = gyök((x2-x1)^2 + (y2-y1)^2)), Felezőpont (F = ((x1+x2)/2, (y1+y2)/2)).\n### II. Egyenes egyenlete: Normálvektoros alak: Ax + By = Ax0 + By0.\n### III. Kör egyenlete: (x - u)^2 + (y - v)^2 = r^2 (Középpont: K(u, v), sugár: r).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Távolság és felezőpont -> 2. Egyenes normálvektoros egyenletének felírása -> 3. Kör egyenlete.",
        "kviz": [{"k": "A (x - 3)^2 + (y + 1)^2 = 25 egyenletű kör sugara r = 5.", "v": True, "m": "Mert r^2 = 25 -> r = 5."}]
    },
    "9. Térgeometria (Testek felszíne és térfogata)": {
        "alcim": "Hasáb, henger, gúla, kúp és gömb felszín- és térfogatszámítása",
        "kulcsszavak": ["Henger", "Kúp", "Gúla", "Gömb", "Felszín ($A$)", "Térfogat ($V$)"],
        "audio_szoveg": "A térgeometria a háromdimenziós testek metrikus tulajdonságaival foglalkozik...",
        "vazlat": "### I. Henger: V = r^2 * pi * M, A = 2*r^2*pi + 2*r*pi*M.\n### II. Kúp és Gúla (csúcsos testek): V = (Talap * M) / 3, Kúp palástja: r * pi * a.\n### III. Gömb: V = 4/3 * R^3 * pi, A = 4 * R^2 * pi.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Egyenes testek térfogata -> 2. Csúcsos testek harmadoló szabálya -> 3. Gömb képletei.",
        "kviz": [{"k": "A kúp térfogata a vele azonos alapsugarú és magasságú henger térfogatának egyharmada.", "v": True, "m": "Ott van az 1/3 szorzó."}]
    },
    "10. Valószínűségszámítás és Statisztika": {
        "alcim": "Klasszikus valószínűség, binomiális eloszlás, átlag, medián, módusz és szórás",
        "kulcsszavak": ["Kedvező / Összes", "Binomiális eloszlás", "Medián", "Módusz", "Átlag", "Szórás"],
        "audio_szoveg": "A valószínűségszámítás a véletlen események modellezését végzi...",
        "vazlat": "### I. Valószínűség: P = Kedvező / Összes. Binomiális: P(X=k) = (n alatt k) * p^k * (1-p)^(n-k).\n### II. Statisztika: Átlag (összeg/db), Módusz (leggyakoribb), Medián (rendezett sor közepe), Terjedelem (max-min), Szórás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszikus valószínűség -> 2. Binomiális modell -> 3. Statisztikai középértékek (átlag, módusz, medián) -> 4. Szórás.",
        "kviz": [{"k": "A medián meghatározásához először mindig nagyság szerinti sorba kell rendezni az adatokat.", "v": True, "m": "A rendezett minta középső eleme."}]
    },
    "11. Gráfelméleti alapfogalmak és alkalmazások": {
        "alcim": "Csúcsok, élek, fokszámok összege, összefüggő gráfok, fák és Euler-vonal",
        "kulcsszavak": ["Fokszámtétel ($\sum d(v) = 2e$)", "Egyszerű gráf", "Összefüggő gráf", "Fa gráf ($n$ csúcs, $n-1$ él)", "Teljes gráf"],
        "audio_szoveg": "A gráfelmélet csúcsok és az azokat összekötő élek hálózatát vizsgálja, ami a modern informatikai hálózatok és logisztikai feladatok alapja...",
        "vazlat": """
### I. Alapfogalmak
- **Gráf:** $G(V, E)$ – $V$: csúcsok halmaza, $E$: élek halmaza.
- **Egyszerű gráf:** Nincs benne hurokél és nincsenek többszörös (párhuzamos) élek.
- **Csúcs fokszáma ($d(v)$):** A csúcsból kiinduló élek száma.
- **Fokszámtétel (Kézfogási lemma):** A gráf csúcsainak fokszámösszege mindig páros, és egyenlő az élek számának kétszeresével ($\sum d(v) = 2 \cdot e$). *Következmény:* Páratlan fokszámú csúcsból csak páros sok lehet!

### II. Speciális gráftípusok
- **Teljes gráf ($K_n$):** Minden csúcs össze van kötve minden más csúccsal. Élek száma: $\binom{n}{2} = \frac{n(n-1)}{2}$.
- **Fa gráf:** Összefüggő és körmentes gráf. Ha $n$ csúcsa van, akkor pontosan $n-1$ éle van!
- **Euler-vonal:** Olyan vonal, amely a gráf minden élén pontosan egyszer halad át (akkor létezik zárt Euler-vonal, ha minden csúcs fokszáma páros).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Gráf fogalma és fokszáma -> 2. Fokszámtétel és következményei -> 3. Teljes gráf és Fa gráf éleinek száma -> 4. Euler-vonal feltétele.",
        "kviz": [{"k": "Egy gráfban nem lehet páratlan számú páratlan fokszámú csúcs.", "v": True, "m": "A fokszámok összege mindig páros, így a páratlan csúcsok száma is csak páros lehet."}]
    },
    "12. Exponenciális és logaritmikus egyenletek": {
        "alcim": "Azonos alapra hozás módszere, logaritmálás, új ismeretlen bevezetése",
        "kulcsszavak": ["Közös alapra hozás", "Szigorú monotonitás", "Új változó ($a^x = u$)", "Értelmezési tartomány"],
        "audio_szoveg": "Az exponenciális és logaritmusos egyenletek megoldásakor a szigorú monotonitás és az értelmezési tartomány pontos ellenőrzése a siker kulcsa...",
        "vazlat": """
### I. Exponenciális egyenletek ($a^{f(x)} = a^{g(x)}$)
1. **Azonos alapra hozás:** Ha az alapok megegyeznek és $a>0, a\neq 1$, az exponenciális függvény szigorú monotonitása miatt az egyenlőség a kitevőkre is érvényes: $f(x) = g(x)$.
2. **Új ismeretlen bevezetése:** Pl. $2^{2x} - 5 \cdot 2^x + 4 = 0 \rightarrow$ legyen $u = 2^x (u>0)$, ekkor $u^2 - 5u + 4 = 0$.
3. **Különböző alapok esete ($2^x = 3^{x-1}$):** Mindkét oldal tízes alapú logaritmálása: $\lg(2^x) = \lg(3^{x-1}) \rightarrow x \lg 2 = (x-1) \lg 3$.

### II. Logaritmikus egyenletek
1. **Kikötések kötelezőek:** Belső szám $> 0$!
2. **Egyetlen logaritmusra rendezés:** Logaritmus azonosságok alkalmazása ($\log x + \log y = \log(xy)$).
3. **Szigorú monotonitás miatt** a belső részek egyenlőek.
4. **Ellenőrzés kötelező!**
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Exponenciális egyenlet azonos alapra hozása -> 2. Új változó bevezetése másodfokúra -> 3. Logaritmikus egyenlet kikötései -> 4. Monotonitás hivatkozása.",
        "kviz": [{"k": "A 2^x = 16 egyenlet egyetlen megoldása x = 4.", "v": True, "m": "Mert 2 a 4. hatványon egyenlő 16-tal."}]
    },
    "13. Trigonometrikus egyenletek": {
        "alcim": "Alap szögfüggvényes egyenletek megoldása a periodicitás figyelembevételével",
        "kulcsszavak": ["Periodicitás ($+ k \cdot 2\pi$ vagy $+ k \cdot 180^\circ$)", "Két megoldássorozat", "Egységkör", "$\sin^2 x + \cos^2 x = 1$"],
        "audio_szoveg": "A szögfüggvényes egyenleteknél a megoldások végtelen periodikus sorozatokat alkotnak a trigonometrikus kör szimmetriái miatt...",
        "vazlat": """
### I. Alapvető azonosság
- $\sin^2 x + \cos^2 x = 1 \rightarrow \sin^2 x = 1 - \cos^2 x$
- $\text{tg} x = \frac{\sin x}{\cos x}$ (Kikötés: $\cos x \neq 0$)

### II. Megoldássorozatok (Periodicitás!)
- **$\sin x = c$ (ahol $-1 \le c \le 1$):**
  - $x_1 = \alpha + k \cdot 360^\circ$
  - $x_2 = 180^\circ - \alpha + k \cdot 360^\circ$ ($k \in \mathbb{Z}$)
- **$\cos x = c$ (ahol $-1 \le c \le 1$):**
  - $x_1 = \alpha + k \cdot 360^\circ$
  - $x_2 = -\alpha + k \cdot 360^\circ$ ($k \in \mathbb{Z}$)
- **$\text{tg} x = c$:**
  - $x = \alpha + k \cdot 180^\circ$ ($k \in \mathbb{Z}$ - periódusa $180^\circ$!)
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Egységkör és szögfüggvények előjelei -> 2. Szinusz két megoldása ($180^\circ-\alpha$) -> 3. Koszinusz két megoldása ($-\alpha$) -> 4. Periodicitás $k \in \mathbb{Z}$ hozzáadása.",
        "kviz": [{"k": "A tg(x) függvény periódusa 180 fok (vagy pi radián).", "v": True, "m": "Míg a sin és cos periódusa 360 fok (2*pi)."}]
    },
    "14. Vektorműveletek és a skaláris szorzat": {
        "alcim": "Összeadás, kivonás, számmal szorzás, skaláris szorzat és két vektor hajlásszöge",
        "kulcsszavak": ["Vektor koordinátái", "Skaláris szorzat ($\vec{a}\cdot\vec{b} = a_1b_1 + a_2b_2$)", "Hajlásszög ($\cos\varphi$)", "Merőlegesség"],
        "audio_szoveg": "A vektorok irányított szakaszok. Két vektor skaláris szorzata valós számot eredményez, amivel könnyen meghatározható a közbezárt szög...",
        "vazlat": """
### I. Vektorműveletek koordinátákkal ($\vec{a}(a_1, a_2), \vec{b}(b_1, b_2)$)
- **Összeg:** $\vec{a} + \vec{b} = (a_1 + b_1, a_2 + b_2)$
- **Hossz (Abszolút érték):** $|\vec{a}| = \sqrt{a_1^2 + a_2^2}$

### II. A skaláris szorzat
- **Geometriai definíció:** $\vec{a} \cdot \vec{b} = |\vec{a}| \cdot |\vec{b}| \cdot \cos\varphi$
- **Koordinátás képlet:** $\vec{a} \cdot \vec{b} = a_1 b_1 + a_2 b_2$
- **Két vektor hajlásszöge:** $\cos\varphi = \frac{a_1 b_1 + a_2 b_2}{\sqrt{a_1^2 + a_2^2} \cdot \sqrt{b_1^2 + b_2^2}}$
- **Merőlegességi feltétel:** Két vektor akkor és csak akkor merőleges egymásra, ha skaláris szorzatuk **0** ($\vec{a} \cdot \vec{b} = 0$).
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Vektor fogalma és hossza -> 2. Skaláris szorzat kétféle kiszámítása -> 3. Hajlásszög képlete -> 4. Merőlegesség vizsgálata nullával.",
        "kviz": [{"k": "Ha két vektor skaláris szorzata 0, akkor a két vektor merőleges egymásra.", "v": True, "m": "Mert cos(90 fok) = 0."}]
    },
    "15. Számelmélet: Oszthatóság, prímek, LNKO és LKKT": {
        "alcim": "Oszthatósági szabályok, a számelmélet alaptétele, legnagyobb közös osztó és legkisebb közös többszörös",
        "kulcsszavak": ["Prímszám", "Számelmélet alaptétele", "LNKO (Legnagyobb közös osztó)", "LKKT (Legkisebb közös többszörös)"],
        "audio_szoveg": "A számelmélet az egész számok tulajdonságait és az oszthatósági relációkat vizsgálja...",
        "vazlat": """
### I. Oszthatósági szabályok
- 2-vel, 5-tel, 10-zel: utolsó számjegy alapján.
- 4-gyel, 25-tel, 100-zal: utolsó 2 számjegyből képzett szám alapján.
- 3-mal, 9-cel: a számjegyek összege osztható 3-mal / 9-cel.

### II. A számelmélet alaptétele
- Minden 1-nél nagyobb összetett egész szám a tényezők sorrendjétől eltekintve **egyértelműen felbontható prímszámok szorzatára**.

### III. LNKO és LKKT kiszámítása prímtényezős alakból
- **LNKO (Legnagyobb közös osztó):** A közös prímtényezők a legkisebb hatványon összeszorozva.
- **LKKT (Legkisebb közös többszörös):** Az összes előforduló prímtényező a legnagyobb hatványon összeszorozva.
- *Összefüggés:* $a \cdot b = \text{LNKO}(a, b) \cdot \text{LKKT}(a, b)$
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Oszthatósági szabályok -> 2. Prímszámok és a számelmélet alaptétele -> 3. LNKO és LKKT algoritmusa -> 4. Törtek egyszerűsítése és közös nevezője.",
        "kviz": [{"k": "A 12 és 18 legnagyobb közös osztója (LNKO) a 6.", "v": True, "m": "Mert 12 = 2^2 * 3 és 18 = 2 * 3^2 -> LNKO = 2 * 3 = 6."}]
    },
    "16. Differenciálszámítás (Deriválás) bevezetése": {
        "alcim": "A differenciahányados, derivált fogalma, hatványfüggvény deriválása és érintő meredeksége",
        "kulcsszavak": ["Érintő meredeksége ($m = f'(x_0)$)", "Deriválási szabályok ($(x^n)' = n\cdot x^{n-1}$)", "Szélsőértékkeresés ($f'(x) = 0$)"],
        "audio_szoveg": "A differenciálszámítás a függvények pillanatnyi változási sebességét és az érintő meredekségét vizsgálja...",
        "vazlat": """
### I. A derivált geometriai jelentése
- Az $f'(x_0)$ derivált az $f(x)$ függvény grafikonjához az $x_0$ pontban húzott **érintő egyenes meredekségét ($m$)** adja meg.

### II. Alapvető deriválási szabályok
- Konstans deriváltja: $(c)' = 0$
- Hatványfüggvény: $(x^n)' = n \cdot x^{n-1}$ (pl. $(x^3)' = 3x^2, (x^2)' = 2x, (x)' = 1$)
- Szorzás konstanssal: $(c \cdot f(x))' = c \cdot f'(x)$
- Összeg deriváltja: $(f(x) + g(x))' = f'(x) + g'(x)$

### III. Alkalmazás: Szélsőérték meghatározása
- Ahol a folytonos függvénynek lokális szélsőértéke (maximuma vagy minimuma) van, ott az érintő vízszintes, vagyis **a derivált értéke 0**: $f'(x) = 0$.
        """,
        "szobeli": "**🎙️ 3 perces felelet:** 1. Derivált geometriai értelmezése (érintő meredeksége) -> 2. Hatványfüggvény deriválási szabálya -> 3. Szélsőértékkeresés feltétele ($f'(x)=0$).",
        "kviz": [{"k": "Az f(x) = x^4 függvény deriváltja f'(x) = 4x^3.", "v": True, "m": "A hatványkitevő szorzóként előre jön, a kitevő eggyel csökken."}]
    }
}

# -------------------------------------------------------------
# FLASHCARDS ADATBÁZIS
# -------------------------------------------------------------
flashcards_adat = [
    # Irodalom
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra (dalforma), epika (cselekmény) és dráma (konfliktus) sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a legfontosabb irodalmi szerkesztője?", "a": "1908. január 1-jén indult, és Osvát Ernő volt a lap legendás irodalmi szerkesztője."},
    {"q": "Mi a központi szállóige Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.” – Az értelmiségi ember morális felelősségvállalása."},
    {"q": "Hogyan végződik Örkény István 'Tóték' című műve?", "a": "Tót Lajos a dobozvágó margóvágóval négy egyforma darabba vágja az Őrnagyot."},
    # Nyelvtan
    {"q": "Mi a magyar helyesírás 4 alapelve?", "a": "1. Kiejtés elve, 2. Szóelemzés elve, 3. Hagyomány elve, 4. Egyszerűsítés elve."},
    {"q": "Mi a toldalékok szigorú kötött sorrendje a magyar szavakban?", "a": "Szótő + KÉPZŐ + JEL + RAG (pl. ház-as-ság-ok-at)."},
    {"q": "Mi a különbség a szólás és a közmondás között?", "a": "A szólás képszerű kifejezés mondatérték nélkül (pl. feni a fogát), a közmondás kerek egész mondat tanulsággal (pl. Ki korán kel, aranyat lel)."},
    # Történelem
    {"q": "Mikor adta ki Nagy Lajos az Ősiség törvényét és mit jelentett az?", "a": "1351-ben. A nemesi birtok nem adható el, nemes kihalásakor a rokonokra, végül a királyra száll vissza."},
    {"q": "Mikor foglalta el a török csellel Buda várát, amivel 3 részre szakadt az ország?", "a": "1541. augusztus 29-én."},
    {"q": "Milyen új pénznemet vezetett be Bethlen István 1927-ben a gazdasági stabilitásért?", "a": "A Pengőt."},
    # Matek
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Mi a számtani és a mértani sorozat n-edik tagjának képlete?", "a": "Számtani: an = a1 + (n - 1)d | Mértani: an = a1 * q^(n - 1)"},
    {"q": "Mit mond ki a gráfelmélet fokszámtétele?", "a": "A gráf csúcsainak fokszámösszege mindig páros, és egyenlő az élek számának kétszeresével (2e)."},
    {"q": "Mikor merőleges egymásra két vektor?", "a": "Ha a skaláris szorzatuk pontosan 0 (a1*b1 + a2*b2 = 0)."}
]

# Idővonal
idovonal_adat = [
    {"ev": "Kr. e. V. sz.", "cim": "Az athéni demokrácia virágkora", "leiras": "Periklész kora, a népgyűlés és az esküdtbíróságok működése, a napidíjak bevezetése."},
    {"ev": "Kr. e. 27", "cim": "A Római Principátus születése", "leiras": "Augustus egyeduralma, köztársasági látszat, a Pax Romana békéje."},
    {"ev": "1000", "cim": "Szent István király koronázása", "leiras": "A keresztény magyar állam és a vármegyerendszer megalapítása, egyházmegyék kiépítése."},
    {"ev": "1222", "cim": "Az Aranybulla kiadása", "leiras": "II. András törvénye a szerviensek nemesi jogairól és az ellenállási záradékról."},
    {"ev": "1351", "cim": "Nagy Lajos törvényei", "leiras": "Az ősiség törvénye (aviticitas), a kilenced bevezetése és az egységes nemesi szabadság."},
    {"ev": "1458–1490", "cim": "Hunyadi Mátyás királysága", "leiras": "Központosított királyi hatalom, füstpénz, a Fekete sereg és a reneszánsz kultúra virágkora."},
    {"ev": "1526 / 1541", "cim": "Mohács és az ország 3 részre szakadása", "leiras": "1526 Mohácsi csatavesztés, 1541 Buda török kézre kerülése, Hódoltság és Erdély létrejötte."},
    {"ev": "1703–1711", "cim": "A Rákóczi-szabadságharc", "leiras": "Habsburg-ellenes nemzeti küzdelem, 1707 Ónodi trónfosztás, 1711 Szatmári béke."},
    {"ev": "1830–1848", "cim": "A magyar reformkor", "leiras": "Széchenyi Hitel című művével indul, Kossuth érdekegyesítési programja, a polgári átalakulás előkészítése."},
    {"ev": "1848–1849", "cim": "Forradalom és Szabadságharc", "leiras": "Március 15., Áprilisi törvények, függetlenségi háború és az 1849-es tavaszi hadjárat sikerei."},
    {"ev": "1867", "cim": "A Kiegyezés – Dualizmus kora", "leiras": "Az Osztrák-Magyar Monarchia létrejötte, Deák Ferenc, fél évszázados gazdasági és kulturális aranykor."},
    {"ev": "1914–1918", "cim": "Az Első Világháború", "leiras": "Lövészárok-hadviselés, Osztrák-Magyar Monarchia és a történelmi Magyarország felbomlása."},
    {"ev": "1920–1931", "cim": "Trianon és a Bethleni konszolidáció", "leiras": "Trianoni békediktátum (1920), a gazdasági talpra állás (Pengő, 1927), Klebelsberg Kuno iskolaépítési programja."},
    {"ev": "1939–1945", "cim": "A Második Világháború és Holokauszt", "leiras": "Sztálingrádi fordulat, Don-kanyar katasztrófája, 1944. márc. 19. német megszállás, nyilas terror."},
    {"ev": "1956. okt. 23.", "cim": "Forradalom és Szabadságharc", "leiras": "A pesti diákok tüntetése, fegyveres harc a szovjet elnyomás ellen, Nagy Imre kormánya, nov. 4-i invázió."},
    {"ev": "1989–1990", "cim": "A Békés Rendszerváltás", "leiras": "Ellenzéki Kerekasztal, Nagy Imre újratemetése, határnyitás, a Köztársaság kikiáltása és az 1990-es szabad választások."}
]

# Detektív játék adatbázis
detektiv_adatbazis = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma. / Fölkeltem én hát; megbánva a rest / lapulást...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Ember az embertelenségben", "Arany János: Szondi két apródja", "Radnóti Miklós: Nem tudhatom"], "info": "A prófétai és értelmiségi felelősségvállalás alaptétele."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb, / Mit kény és kedv szerint lök / A sors előbb-tovább.”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János: Toldi", "Ady Endre: Új vizeken járok"], "info": "Petőfi forradalmi felhívó lírájának remeke."},
    {"idezet": "„Mondottam, ember: küzdj és bízva bízzál!”", "helyes": "Madách Imre: Az ember tragédiája", "opciok": ["Madách Imre: Az ember tragédiája", "Arany János: A walesi bárdok", "Vörösmarty: Csongor és Tünde", "Katona József: Bánk bán"], "info": "Az Úr szózata a 15. szín lezárásaként."},
    {"idezet": "„Ius resistendi (A nemesek joga a királlyal szembeni ellenállásra)”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Nagy Lajos 1351-es törvényei", "Szent István I. törvénykönyve", "Kollonics Lipót rendelete"], "info": "A magyar rendi nemesi szabadságjogok sarokköve."},
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
# FŐ TANTÁRGY VÁLASZTÓ (2x annyi tétel tantárgyanként)
# =============================================================
st.sidebar.markdown("<h2 style='color:#818cf8;'>📚 Tantárgy Választó</h2>", unsafe_allow_html=True)
kivalasztott_tantargy = st.sidebar.selectbox(
    "Válassz tantárgyat:",
    [
        "📖 Magyar Irodalom (22 tétel)",
        "🔤 Magyar Nyelvtan (16 tétel)",
        "🏛️ Történelem (20 tétel)",
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
