import io
import os
import random
import streamlit as st
import datetime
from fpdf import FPDF
from google import genai
from gtts import gTTS

# Beállítás: Hány naponta frissüljenek a kérdések
FRISSITESI_GYAKORISAG_NAPOKBAN = 1

def get_daily_index(lista_hossza):
    nap_sorszam = datetime.date.today().toordinal() // FRISSITESI_GYAKORISAG_NAPOKBAN
    return nap_sorszam % lista_hossza

st.set_page_config(
    page_title="Érettségi Felkészítő Központ - Edited by Nagy Attila",
    page_icon="🎓",
    layout="wide"
)

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Astra AI stílusú prémium sötét téma és fehér szövegek
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .css-1d391kg, .stSidebar { background-color: #111827 !important; border-right: 1px solid #1f2937; }
    p, label, span, .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: #f3f4f6 !important; }
    .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important; font-weight: 700 !important; border-radius: 10px !important; padding: 10px 24px !important;
    }
    div[data-testid="stExpander"] { background-color: #1f2937 !important; border: 1px solid #4b5563 !important; border-radius: 10px !important; }
    div[data-testid="stExpander"] details summary { background-color: #1e1b4b !important; color: #ffffff !important; font-weight: 700 !important; padding: 12px !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #4b5563 !important; border-radius: 8px !important; }
    .stat-badge { background: linear-gradient(135deg, #6366f1, #a855f7); padding: 8px 16px; border-radius: 20px; font-weight: 700; display: inline-block; margin-right: 8px; }
    .subject-pill { background: #1e1b4b; border: 1px solid #6366f1; padding: 6px 14px; border-radius: 12px; font-weight: 600; display: inline-block; margin-bottom: 12px; }
    .topic-card { background-color: #1f2937; border: 1px solid #374151; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .oral-box { background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 18px; border-radius: 8px; margin-top: 15px; }
    .deep-text { background-color: #111827; border: 1px solid #374151; padding: 24px; border-radius: 12px; line-height: 1.8; }
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 16px; padding: 35px; text-align: center; min-height: 180px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
    .timeline-item { background-color: #1f2937; border-left: 4px solid #a855f7; padding: 16px 20px; margin-bottom: 15px; border-radius: 0 12px 12px 0; }
    .chat-user { background-color: #4f46e5; color: white; padding: 12px 18px; border-radius: 16px 16px 4px 16px; margin-bottom: 12px; max-width: 80%; margin-left: auto; }
    .chat-ai { background-color: #1f2937; color: #f3f4f6; border: 1px solid #374151; padding: 12px 18px; border-radius: 16px 16px 16px 4px; margin-bottom: 12px; max-width: 80%; }
</style>
""", unsafe_allow_html=True)

# ADATBÁZISOK (Irodalom, Nyelvtan, Történelem, Matek)
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

tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, kommunikációs funkciók",
        "kulcsszavak": ["Adó és Vevő", "Kód és Csatorna", "Jakobson modellje", "Metakommunikáció"],
        "audio_szoveg": "A kommunikáció információk, gondolatok és érzelmek átadása valamilyen jelrendszer segítségével...",
        "vazlat": "### I. A Jakobson-féle modell: Adó, Vevő, Üzenet, Kód, Csatorna, Kontextus (helyzet), Zaj.\n### II. Nyelvi funkciók: Tájékoztató (referenciális), Érzelemkifejező (emotív), Felhívó (konatív), Fatikus (kapcsolattartó), Metanyelvi (a kódról szóló), Poétikai (esztétikai).\n### III. Nem nyelvi (nonverbális) kódok: Mimika, testbeszéd, gesztusok, szemkontaktus, proxemika (távolságtartás).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A kommunikáció definíciója -> 2. Roman Jakobson 6 tényezős modellje -> 3. A nyelvi funkciók bemutatása példákkal -> 4. Nonverbális jelek szerepe.",
        "kviz": [{"k": "A fatikus funkció elsődleges célja az üzenet esztétikai formájának kiemelése.", "v": False, "m": "A fatikus funkció a kapcsolat felvételére, fenntartására vagy lezárására szolgál (pl. köszönés)."}]
    },
    "2. A szövegtan alapjai és a szövegtípusok": {
        "alcim": "A szöveg kohéziós erői, szerkezeti egységei és típusai",
        "kulcsszavak": ["Globális kohézió", "Lokális kohézió", "Anafora és Katafora", "Elbeszélő, leíró, érvelő"],
        "audio_szoveg": "A szöveg a nyelv legmagasabb szintű, lezárt, kerek egysége...",
        "vazlat": "### I. A szöveg fogalma: Lezárt, összefüggő, tartalmi és formai egységet alkotó nyelvi megnyilatkozás.\n### II. Kohézió (szövegösszetartás): Lokális kohézió (kötőszók, láncszerű kapcsolódás, anafora=visszautalás, katafora=előreutalás) és globális kohézió (témamegtartás).\n### III. Szerkezet és típusok: Cím, bevezetés, tárgyalás, befejezés; elbeszélő, leíró, magyarázó és érvelő szövegek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A szöveg mint nyelvi egység -> 2. Kohéziós eszközök (anafora, katafora) -> 3. Makrostruktúra -> 4. Szövegtípusok.",
        "kviz": [{"k": "Az anafora a szövegben előreutalást jelent egy még be nem mutatott elemre.", "v": False, "m": "Az anafora visszautaló elem, az előreutalás a katafora."}]
    },
    "3. A magyar helyesírás alapelvei": {
        "alcim": "A 4 alapelv rendszere és alkalmazásuk a gyakorlatban",
        "kulcsszavak": ["Kiejtés elve", "Szóelemzés elve", "Hagyomány elve", "Egyszerűsítés elve"],
        "audio_szoveg": "A magyar helyesírás négy alapelvre épül, amelyek biztosítják az íráskép egységességét...",
        "vazlat": "### I. A kiejtés elve: A hangok tiszta írása, ha nincs nyelvtani akadály (pl. *asztal, fa*).\n### II. A szóelemzés (morfematikus) elve: A morfémák határai felismerhetők maradnak a kiejtéstől függetlenül (pl. *látja, barátság*).\n### III. A hagyomány elve: Történelmi helyesírási formák őrzése (pl. *Kossuth, lyuk, ch*).\n### IV. Az egyszerűsítés elve: A kettőzött betűk egyszerűsítése találkozáskor (pl. *asszony, tollal* vs. kivétel: *juhász*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A helyesírási alapelvek szerepe -> 2. Kiejtés és szóelemzés ellentéte/összhangja -> 3. Hagyomány elve példákkal -> 4. Egyszerűsítés elve.",
        "kviz": [{"k": "A 'barátság' szó leírásakor a kiejtést követjük, ezért írunk 'cs'-t.", "v": False, "m": "A szóelemzés elve érvényesül: barát + ság, ezért marad a 't' és 's' találkozása."}]
    },
    "4. Szófajok és mondatrészek rendszere": {
        "alcim": "Alapszófajok, viszonyszók, predikatív viszony és mondattani elemzés",
        "kulcsszavak": ["Ige, Névszó, Igenév", "Viszonyszók", "Alany, Állítmány", "Bővítmények"],
        "audio_szoveg": "A szófajok a szavak alaktani és mondattani kategóriái, amelyekből a mondatrészek épülnek fel...",
        "vazlat": "### I. Szófaji csoportok: Alapszófajok (ige, főnév, melléknév, számnév, határozószó, igenevek), Viszonyszók (névelő, névmás, kötőszó, névutó, segédige), Mondatszók.\n### II. Alapvető mondattani viszonyok: Predikatív (alany-állítmányi), alárendelő (bővítményi), mellérendelő.\n### III. Mondatrészek: Alany, állítmány, tárgy, hely-, idő-, módhatározó, jelzők (minőségjelző stb.).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Alapszófajok vs. viszonyszók -> 2. Az alany és állítmány predikatív viszonya -> 3. Alárendelő mondatrészek fajtái.",
        "kviz": [{"k": "A névelők önálló mondatrészsé válhatnak a mondatban.", "v": False, "m": "A viszonyszók (így a névelők is) önmagukban nem alanyai vagy tárgyai a mondatnak."}]
    },
    "5. Retorika és érvelési technikák": {
        "alcim": "Az érv 3 része, érvtípusok és a klasszikus szónoki beszéd 6 lépése",
        "kulcsszavak": ["Tétel, Bizonyíték, Összekötés", "Érvtípusok", "Exordium", "Peroratio"],
        "audio_szoveg": "A retorika a meggyőzés művészete, amely hatásos érvelési láncokra épül...",
        "vazlat": "### I. Az érv felépítése: Tétel (állitás) -> Bizonyíték (tény, adat) -> Összekötő elem (magyarázat).\n### II. Érvtípusok: Meghatározásból levezetett, ok-okozati, analógiás (hasonlóság), tekintélyre hivatkozó, ellentétre épülő.\n### III. Klasszikus szónoki beszéd: Exordium (bevezetés) -> Narratio (témafelvetés) -> Divisio (részletezés) -> Confirmatio (bizonyítás) -> Refutatio (cáfolat) -> Peroratio (befejezés).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A retorika fogalma és célja -> 2. Az érv három alkotóeleme -> 3. Gyakoribb érvtípusok -> 4. A klasszikus szónoki felépítés.",
        "kviz": [{"k": "Az analógiás érv két hasonló eset vagy helyzet összehasonlításán alapul.", "v": True, "m": "Igen, a hasonlóságon keresztül bizonyít."}]
    },
    "6. Stilisztika: Alakzatok és trópusok": {
        "alcim": "Költői képek (metafora, metonímia, szinesztézia) és szövegalakzatok",
        "kulcsszavak": ["Metafora", "Metonímia", "Szinesztézia", "Anafora és Párhuzam"],
        "audio_szoveg": "A stilisztika a nyelvi kifejezőeszközök és alakzatok hatásmechanizmusát vizsgálja...",
        "vazlat": "### I. Trópusok (jelentésbeli alakzatok): Metafora (hasonlóságon alapuló névváltoztatás), Metonímia (érintkezésen alapuló: anyag, tér-idő), Szinekdoché (rész-egész), Szinesztézia (különböző érzéki területek összekapcsolása).\n### II. Alakzatok (formai/szerkezeti): Anafora (sor eleji ismétlés), Párhuzam, Ellentét, Fokozás, Halmozás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trópusok vs. alakzatok különbsége -> 2. A metafora fajtái -> 3. Szinesztézia és metonímia -> 4. Szövegalakzatok.",
        "kviz": [{"k": "A 'bársonyos hang' kifejezés egy tipikus szinesztézia, mivel tapintási és hallási érzékelést köt össze.", "v": True, "m": "Igen, a bársony (tapintás) és a hang (hallás) keveredik."}]
    },
    "7. A szókészlet rétegződése és változása": {
        "alcim": "Nyelvjárások, társadalmi rétegnyelvek, szleng, archaizmusok és neologizmusok",
        "kulcsszavak": ["Nyelvjárások", "Szaknyelv és Szleng", "Archaizmus", "Neologizmus"],
        "audio_szoveg": "A magyar nyelv szókészlete folyamatosan változik, és területileg, valamint társadalmilag is rétegződik...",
        "vazlat": "### I. Területi tagozódás: Nyelvjárások (dialektusok) és a tájszavak.\n### II. Társadalmi tagozódás: Szaknyelvek, rétegnyelvek, szleng (laza, fiatalos argó).\n### III. Időbeli változás: Archaizmusok (régies, elavult szavak) és Neologizmusok (új szavak, idegen eredetű vagy belső keletkezésű újítások).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A szókészlet dinamikája -> 2. Területi dialektusok -> 3. Társadalmi rétegnyelvek és szleng -> 4. Archaizmus és neologizmus.",
        "kviz": [{"k": "Az archaizmusok a mai modern kor legújabb szavait jelölik.", "v": False, "m": "Az archaizmusok elavult, régies szavak, míg az újak a neologizmusok."}]
    },
    "8. A magyar nyelv története és a nyelvújítás": {
        "alcim": "A finnugor rokonság, a korai nyelvemlékek és Kazinczy nyelvújítása",
        "kulcsszavak": ["Uráli / Finnugor", "Halotti Beszéd (1195)", "Ómagyar Mária-siralom", "Kazinczy Ferenc"],
        "audio_szoveg": "A magyar nyelv az uráli nyelvcsalád finnugor ágába tartozik, története évezredekre nyúlik vissza...",
        "vazlat": "### I. Eredet: Finnugor nyelvrokonság, ugor kor, honfoglalás kori szókincs.\n### II. Korai nyelvemlékek: Tihanyi apátság alapítólevele (1055 - szórványemlékek), Halotti beszéd és könyörgés (1195 körül - első összefüggő szöveg), Ómagyar Mária-siralom (13. sz. eleje - első lírai emlék).\n### III. A nyelvújítás korszaka (1790–1820): Kazinczy Ferenc; küzdelem a neológusok és ortológusok között; új szavak megalkotása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A finnugor származás bizonyítékai -> 2. Fontosabb korai nyelvemlékek -> 3. A nyelvújítás szükségessége és Kazinczy szerepe.",
        "kviz": [{"k": "A Halotti beszéd és könyörgés az első fennmaradt összefüggő magyar nyelvű szövegemlékünk.", "v": True, "m": "Igen, a Pray-kódexben maradt fenn 1195 körül."}]
    },
    "9. Fonetika: A hangok képzése és a mássalhangzótörvények": {
        "alcim": "Magánhangzók és mássalhangzók rendszere, hasonulás, összeolvadás, kiesés és rövidülés",
        "kulcsszavak": ["Zöngés és Zöngétlen", "Részleges hasonulás", "Teljes hasonulás", "Összeolvadás"],
        "audio_szoveg": "A fonetika a beszédhangok képzését, tulajdonságait és az egymásra ható mássalhangzótörvényeket vizsgálja...",
        "vazlat": "### I. Hangrendszer: Magánhangzók (mély, magas, vegyes; rövid, hosszú) és mássalhangzók (zöngés / zöngétlen párok).\n### II. Mássalhangzótörvények:\n- Zöngésségi részleges hasonulás (pl. *népdal -> népdal [néptal]*).\n- Képzés helye szerinti részleges hasonulás (pl. *színpad -> [szímpad]*).\n- Teljes hasonulás (jelölt: *szabja -> szablya*; jelöletlen: *zsebkendő -> zsebkendő [zsebkendő]* -> *egészség*).\n- Összeolvadás (pl. *barátság -> [baraccság]*).\n- Kiesés és rövidülés.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A hangok csoportosítása -> 2. Zöngésségi és képzés helye szerinti hasonulás -> 3. Teljes hasonulás (jelölt és jelöletlen) -> 4. Összeolvadás.",
        "kviz": [{"k": "A 'színpad' szó kiejtésekor képzés helye szerinti részleges hasonulás érvényesül ('n' m-mûvé alakul).", "v": True, "m": "Igen, az 'n' hang az 'p' előtt 'm'-mû váltódik."}]
    },
    "10. Morfológia: A szóelemek (morfémák) rendszere": {
        "alcim": "Tőmorfémák, toldalékmorfémák (képző, jel, rag) és a szóelemző helyesírás",
        "kulcsszavak": ["Szótő", "Képző", "Jel", "Rag", "Kötött sorrend"],
        "audio_szoveg": "A morfológia a szavak szerkezetét és a legkisebb jelentést hordozó egységeket, a morfémákat vizsgálja...",
        "vazlat": "### I. Morféma típusok: Tőmorféma (szótő) és toldalékmorféma.\n### II. A toldalékok szigorú sorrendje: Szótő + KÉPZŐ + JEL + RAG (pl. *ház-as-ság-ok-at*).\n### III. Funkciók: Képző (új szót hoz létre, szófajt válthat), Jel (módosítja a jelentést: múlt idő, többes szám, birtokos jel), Rag (lezárja a szót, mondatrészi szerepet ad).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Morféma fogalma -> 2. A képző, jel, rag különbségei -> 3. A szigorú toldalékolási sorrend -> 4. Szóelemző helyesírás.",
        "kviz": [{"k": "A rag a toldalékolási sorban mindig a szó legvégén, a képzők és jelek után áll.", "v": True, "m": "Igen, a rag zárja le a morfémasort."}]
    },
    "11. Szóalkotási módok a magyar nyelvben": {
        "alcim": "Szóösszetétel, szóképzés, mozaikszók, szóelvonás, szóvegyülés és rövidülés",
        "kulcsszavak": ["Szóképzés", "Szóösszetétel", "Mozaikszók", "Szóelvonás"],
        "audio_szoveg": "A magyar nyelv rendkívül gazdag belső szóalkotási módokban, amelyek révén folyamatosan bővül...",
        "vazlat": "### I. Fő szóalkotási módok: Szóképzés (új szó képzővel) és Szóösszetétel (alárendelő és mellérendelő összetételek).\n### II. Egyéb módok: Mozaikszók (betűszók: *MÁV*, szóösszevonások: *Főgáz*), Szóelvonás (*kapa <- kapál*), Szóvegyülés (*csokréta*), Szócsonkítás (*mozi*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Képzés és összetétel szerepe -> 2. Összetételek fajtái (alárendelő, mellérendelő) -> 3. Mozaikszók és ritkább szóalkotási módok.",
        "kviz": [{"k": "A 'kapa' szónak a 'kapál' igéből való visszaképzése (szóelvonás) tipikus példája az új szóalkotásnak.", "v": True, "m": "Igen, itt a hosszabb szóból vonják el a rövidebbet."}]
    },
    "12. Mondattan: Az összetett mondatok típusai": {
        "alcim": "Mellérendelő (kapcsolatos, ellentétes, választó, következtető, magyarázó) és alárendelő mondatok",
        "kulcsszavak": ["Mellérendelő összetett mondat", "Alárendelő összetett mondat", "Főmondat és Mellékmondat"],
        "audio_szoveg": "Az összetett mondatok két vagy több tagmondatból állnak, amelyek viszonya lehet mellérendelő vagy alárendelő...",
        "vazlat": "### I. Mellérendelő összetett mondatok: Tagmondatok egyenrangúak; fajtái: kapcsolatos, ellentétes, választó, következtető, magyarázó.\n### II. Alárendelő összetett mondatok: Főmondat + utalószóval kapcsolódó mellékmondat; a mellékmondat pótolja valamelyik hiányzó mondatrészt (alanyi, tárgyi, határozói, jelzői mellékmondatok).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Alapfogalmak (tagmondatok) -> 2. A 5 féle mellérendelő kapcsolat kötőszavakkal -> 3. Az alárendelő mondatok struktúrája (utalószó szerepe).",
        "kviz": [{"k": "A 'Szakad az eső, ezért otthon maradtunk' mondat következtető mellérendelő összetett mondat.", "v": True, "m": "Igen, az 'ezért' kötőszó következtetést fejez ki."}]
    },
    "13. Stílusrétegek és a stílusérték": {
        "alcim": "Hivatalos, tudományos, publicisztikai, társalgási és szépirodalmi stílus",
        "kulcsszavak": ["Stílusrétegek", "Hivatalos és Tudományos", "Publicisztika", "Denotáció és Konnotáció"],
        "audio_szoveg": "A stílusrétegek a beszédhelyzetnek megfelelő nyelvi eszközök és kifejezésmódok egységei...",
        "vazlat": "### I. Főbb stílusrétegek:\n- Társalgási (köznyelvi, laza, szubjektív).\n- Szépirodalmi (képszerű, érzelmi hatásra törekvő, konnotatív).\n- Tudományos (pontos, szakszavak, tárgyilagos, denotatív).\n- Hivatalos (száraz, sablonos, törvények, kérvények nyelve).\n- Publicisztikai (sajtó, rádió, TV, figyelemfelkeltő, véleményformáló).\n### II. Jelentésrétegek: Denotáció (alapjelentés) és konnotáció (mellékjelentés, hangulat).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Stílusrétegek fogalma és szerepe -> 2. Hivatalos és tudományos stílus jellemzői -> 3. Publicisztikai és társalgási stílus -> 4. Denotáció vs konnotáció.",
        "kviz": [{"k": "A hivatalos stílusra a magas fokú szubjektivitás és a költői képek halmozása jellemző.", "v": False, "m": "A hivatalos stílus sablonos, tárgyilagos és mentes a szubjektív képektől."}]
    },
    "14. Névtan (Onomasztika)": {
        "alcim": "Személynevek és földrajzi nevek rendszere, eredete",
        "kulcsszavak": ["Családnevek típusai", "Keresztnevek", "Földrajzi nevek helyesírása"],
        "audio_szoveg": "A névtan a tulajdonnevek rendszereivel, eredetével és helyesírásával foglalkozó nyelvtudományi ág...",
        "vazlat": "### I. Személynevek rendszere:\n- Családnevek 5 fő forrása: Apai név (*Péterfi*), származási hely (*Budai*), foglalkozás (*Kovács*), külső/belső tulajdonság (*Nagy*), etnikum (*Tóth*).\n- Keresztnevek (történelmi nevek, új nevek antropológiai gyökerei).\n### II. Földrajzi nevek helyesírása: Egyelemű (*Duna*), kételemű egybeírt (*Margitsziget*), kételemű különírt (*Velencei-tó* vagy *Fekete-tenger*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A névtan mint tudomány -> 2. A családnevek 5 nagy kategóriája -> 3. Földrajzi tulajdonnevek írásmódja.",
        "kviz": [{"k": "A 'Kovács' családnév a foglalkozásból/mesterségből származó nevek csoportjába tartozik.", "v": True, "m": "Igen, a kovácsmesterségre utal."}]
    },
    "15. Frazeológia: Szólások, közmondások és szállóigék": {
        "alcim": "Állandósult szókapcsolatok fajtái és metaforikus jelentése",
        "kulcsszavak": ["Szólás", "Közmondás", "Szállóige", "Közhely"],
        "audio_szoveg": "A frazeológia a nyelv állandósult, metaforikus értelmű szókapcsolatait kutatja...",
        "vazlat": "### I. Szólás: Képszerű, állandósult kifejezés, amely önmagában nem mondatértékű (pl. *éles esze van, feni a fogát*).\n### II. Közmondás: Kerek egész mondat, amelynek tanulsága, népiöltsége van (pl. *Nem minden arany, ami fénylik*).\n### III. Szállóige: Ismert szerzőhöz vagy irodalmi műhöz köthető idézet, amely közkinccsé vált (pl. *A kocka el van vetve*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Állandósult szókapcsolatok lényege -> 2. Szólás és közmondás különbsége -> 3. Szállóigék szerepe a kultúrában.",
        "kviz": [{"k": "A 'Lassan járj, tovább érsz' egy tipikus közmondás, mert kerek mondat tanulsággal.", "v": True, "m": "Igen, a népi bölcsesség megtestesítője."}]
    },
    "16. Digitális kommunikáció és az infokommunikációs nyelv": {
        "alcim": "Az online nyelvhasználat, emotikonok, hipertext és a közösségi média hatása",
        "kulcsszavak": ["Netnyelv", "Hipertext", "Multimodalitás", "Írott beszéltség"],
        "audio_szoveg": "Az internet és a digitális forradalom teljesen átalakította a modern ember nyelvhasználatát...",
        "vazlat": "### I. Az online nyelvhasználat jellemzői: Írott beszéltség (az írás és a szóbeliség sajátos keveréke), gyorsaság, tömörség, szleng hatása.\n### II. Multimodalitás és Emojik: Képek, emojik és gifek mint a hiányzoló metakommunikáció (hangszín, mimika) pótlói a neten.\n### III. Hipertext és linkek: Nemlineáris szövegolvasás, hálózatos struktúrák.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A digitális kultúra hatása a nyelvre -> 2. Az 'írott beszéltség' jelensége -> 3. Emojik és nonverbális pótlékok -> 4. Hipertext struktúra.",
        "kviz": [{"k": "Az 'írott beszéltség' azt jelenti, hogy a netes csevegésben az írott formák átveszik a kötetlen beszéd stílusát.", "v": True, "m": "Igen, az írás médiumán keresztül folytatunk spontán társalgást."}]
    }
}# -------------------------------------------------------------
# 4. MATEMATIKA TÉTELTÁR (16 Részletesen Kidolgozott Témakör)
# -------------------------------------------------------------
tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció és kombináció",
        "kulcsszavak": ["Metszet, Unió, Különbség", "Venn-diagram", "Permutáció ($n!$)", "Kombináció ($\binom{n}{k}$)"],
        "audio_szoveg": "A halmazelmélet és a kombinatorika a modern matematika alapvető eszköztára a logikai rendszerezéshez és a kiválasztási feladatokhoz...",
        "vazlat": "### I. Halmazműveletek: Unió (összes elem), Metszet (közös elemek), Különbség, Komplementer; Venn-diagramok.\n### II. Kombinatorikai alapfogalmak:\n- Permutáció (sorbarendezés): $P_n = n!$\n- Variáció (sorrend számít, ismétlés nélkül vagy azzal): $V_n^k = \\frac{n!}{(n-k)!}$\n- Kombináció (sorrend NEM számít): $C_n^k = \\binom{n}{k} = \\frac{n!}{k!(n-k)!}$.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Halmazok és alapegységeik -> 2. De Morgan azonosságok -> 3. Kombinatorikai képletek kiválasztása (számít-e a sorrend?) -> 4. Gyakorlati lottószámítás.",
        "kviz": [{"k": "Az 5-ös lottó esetében a sorrend nem számít a kihúzott számoknál, ezért kombinációt kell használni.", "v": True, "m": "Igen, 90 alatt az 5 kombinációja adja az összes lehetséges alapszelvényt."}]
    },
    "2. Algebra: Egyenletek, egyenlőtlenségek és másodfokú formula": {
        "alcim": "Megoldóképlet, diszkrimináns, gyöktényezős szorzat és Viéte-formulák",
        "kulcsszavak": ["Diszkrimináns ($b^2 - 4ac$)", "Megoldóképlet", "Gyöktényezős alak", "Kikötések"],
        "audio_szoveg": "Az algebrai egyenletek és egyenlőtlenségek megoldásának kulcsa a másodfokú formula és a kikötések ismerete...",
        "vazlat": "### I. Másodfokú egyenlet: $ax^2 + bx + c = 0$.\n### II. Megoldóképlet: $x_{1,2} = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$.\n### III. Diszkrimináns ($D = b^2 - 4ac$): Ha $D > 0$ (2 valós gyök), ha $D = 0$ (1 valós gyök), ha $D < 0$ (nincs valós gyök).\n### IV. Gyöktényezős alak: $a(x - x_1)(x - x_2) = 0$.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Értelmezési tartomány és kikötések -> 2. A megoldóképlet levezetése és a diszkrimináns szerepe -> 3. Gyöktényezős felbontás.",
        "kviz": [{"k": "Ha egy másodfokú egyenlet diszkriminánsa negatív, akkor az egyenletnek nincsen semmilyen gyöke a valós számok halmazán.", "v": True, "m": "A valós számok halmazán nincs gyök, mivel negatívból nincs valós négyzetgyök."}]
    },
    "3. Hatványozás, gyökvonás és a logaritmus azonosságai": {
        "alcim": "Hatványozási azonosságok, törtkitevő, logaritmus fogalma és műveleti szabályai",
        "kulcsszavak": ["$a^n \\cdot a^m = a^{n+m}$", "Törtkitevő", "Logaritmus azonosságok", "Alapáttérés"],
        "audio_szoveg": "A hatványozás, a gyökvonás és a logaritmus szoros kapcsolatban állnak, egymás inverz műveletei...",
        "vazlat": "### I. Hatványozás és gyökvonás azonosságai: $a^n \\cdot a^m = a^{n+m}$, $\\frac{a^n}{a^m} = a^{n-m}$, $(a^n)^m = a^{n \\cdot m}$, valamint a törtkitevő: $n^{\\frac{m}{k}} = \\sqrt[k]{n^m}$.\n### II. Logaritmus definíciója: $\\log_a(b) = c$, ha $a^c = b$ (ahol $a > 0, a \\neq 1, b > 0$).\n### III. Főbb logaritmus azonosságok: $\\log(xy) = \\log x + \\log y$, $\\log(x/y) = \\log x - \\log y$, $\\log(x^k) = k \\cdot \\log x$.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hatványozási szabályok áttekintése -> 2. A gyök mint törtkitevő -> 3. A logaritmus mint inverz művelet -> 4. Logaritmus azonosságok.",
        "kviz": [{"k": "A $\\log_2(8)$ kifejezés értéke pontosan 3.", "v": True, "m": "Mivel 2 a 3. hatványon ($2^3$) éppen 8."}]
    },
    "4. Függvénytan és analízis alapjai": {
        "alcim": "Lineáris, másodfokú, exponenciális, logaritmikus függvények és jellemzésük",
        "kulcsszavak": ["Értelmezési tartomány", "Értékkészlet", "Zérushely", "Szélsőérték", "Transzformáció"],
        "audio_szoveg": "A függvénytan a változók közötti kölcsönös kapcsolatokat és azok grafikus tulajdonságait vizsgálja...",
        "vazlat": "### I. Alapvető függvényjellemzési szempontok: Értelmezési tartomány ($D_f$), Értékkészlet ($R_f$), Zérushely ($f(x)=0$), Szélsőértékek (minimum, maximum), Monotonitás (növekedő/csökkenő), Paritás (páros/páratlan).\n### II. Alapfüggvények: Lineáris ($mx+b$), Másodfokú (parabola), Exponenciális ($a^x$), Logaritmikus ($\\log_ax$).\n### III. Grafikon-transzformációk: Eltolások, nyújtások, zsugorítások.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Függvény fogalma -> 2. A teljeskörű függvényjellemzés lépései -> 3. Nevezetes alapfüggvények -> 4. Transzformációs szabályok.",
        "kviz": [{"k": "Az $f(x) = (x - 3)^2 + 2$ függvény minimumhelye az $x = 3$ pontban van.", "v": True, "m": "A zárójelben lévő $-3$ jobbra tolja a parabolacsúcsot a 3-as helyre."}]
    },
    "5. Sorozatok és Pénzügyi matematika": {
        "alcim": "Számtani és mértani sorozat képletei, kamatos kamat és gyűjtőjáradék",
        "kulcsszavak": ["Differencia ($d$)", "Hányados ($q$)", "Számtani/mértani összeg", "Kamatos kamat"],
        "audio_szoveg": "A sorozatok olyan sorba rendezett számok, amelyek törvényszerűen követik egymást, alapozva a pénzügyi számításokat...",
        "vazlat": "### I. Számtani sorozat: Minden elem a előzőhöz adott $d$ differenciával kapható meg. $a_n = a_1 + (n-1)d$. Összegképlet: $S_n = \\frac{a_1 + a_n}{2} \\cdot n$.\n### II. Mértani sorozat: Minden elem a előző $q$ hányadossal szorzódik. $a_n = a_1 \\cdot q^{n-1}$. Összegképlet: $S_n = a_1 \\cdot \\frac{q^n - 1}{q - 1}$.\n### III. Pénzügyi matematika: Kamatos kamat képlete: $C_n = C_0 \\cdot \\left(1 + \\frac{p}{100}\\right)^n$.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Számtani sorozat definíciója és képletei -> 2. Mértani sorozat szabályai -> 3. Kamatos kamatszámítás a gazdaságban.",
        "kviz": [{"k": "Ha egy számtani sorozat első eleme 2, a differenciája pedig 4, akkor a 5. tag értéke 18.", "v": True, "m": "$a_5 = 2 + (5-1) \\cdot 4 = 2 + 16 = 18$."}]
    },
    "6. Síkgeometria és Trigonometria": {
        "alcim": "Pitagorasz-tétel, Szinusz- és Koszinusztétel, háromszögek területszámítása",
        "kulcsszavak": ["Pitagorasz-tétel", "Szögfüggvények", "Szinusztétel", "Koszinusztétel", "Területképletek"],
        "audio_szoveg": "A síkgeometria és a trigonometria a síkbeli alakzatok méreteit, szögeit és oldalarányait köti össze...",
        "vazlat": "### I. Derékszögű háromszög: $a^2 + b^2 = c^2$ (Pitagorasz); szögfüggvények: $\\sin = \\frac{szemben}{átló}$, $\\cos = \\frac{mellette}{átló}$, $\\tan = \\frac{szemben}{mellette}$.\n### II. Általános háromszög:\n- Szinusztétel: $\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R$.\n- Koszinusztétel: $a^2 = b^2 + c^2 - 2bc \\cos A$.\n### III. Terület: $T = \\frac{a \\cdot m_a}{2} = \\frac{ab \\sin \\gamma}{2}$.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Pitagorasz-tétel és derékszögű háromszögek -> 2. Trigonometrikus alapfüggvények -> 3. Szinusz- és koszinusztétel alkalmazási esetei.",
        "kviz": [{"k": "A koszinusztétel lényegében a Pitagorasz-tétel általánosítása tetszőleges háromszögekre.", "v": True, "m": "Igen, a $-2bc \\cos Atag$ korrigálja a nem derékszöget."}]
    },
    "7. Síkgeometria: Sokszögek, kör és négyszögek tulajdonságai": {
        "alcim": "Szabályos sokszögek belső szögei, deltoid, rombusz, trapéz, kör ívhossza és körcikk területe",
        "kulcsszavak": ["Belső szögek összege", "Trapéz és rombusz területe", "Kör kerülete és területe", "Körcikk"],
        "audio_szoveg": "A sokszögek, a négyszögek és a kör különleges geometriai tulajdonságai kulcsfontosságúak az érettségin...",
        "vazlat": "### I. Sokszögek: Belső szögek összege: $(n-2) \\cdot 180^\\circ$; átlók száma: $\\frac{n(n-3)}{2}$.\n### II. Négyszög területek:\n- Trapéz: $T = \\frac{a+c}{2} \\cdot m$.\n- Rombusz és Deltoid: $T = \\frac{e \\cdot f}{2}$.\n### III. Kör: Kerület $K = 2r\\pi$, Terület $T = r^2\\pi$. Körcikk ívhossza és területe a középponti szög arányában számolható.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Sokszögek átlói és belső szögei -> 2. Négyszög-családok területképletei -> 3. Kör, körcikk és körív számításai.",
        "kviz": [{"k": "Egy konvex hétszög belső szögeinek összege pontosan $900^\\circ$.", "v": True, "m": "$(7-2) \\cdot 180^\\circ = 5 \\cdot 180^\\circ = 900^\\circ$."}]
    },
    "8. Koordinátageometria": {
        "alcim": "Vektorműveletek, felezőpont, súlypont, az egyenes és a kör egyenlete",
        "kulcsszavak": ["Két pont távolsága", "Felezőpont", "Egyenes normálvektoros egyenlete", "Kör egyenlete"],
        "audio_szoveg": "A koordinátageometria algebrai egyenletekkel írja le a geometriai síkidomokat és azok helyzetét...",
        "vazlat": "### I. Alapképletek: Két pont távolsága ($d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$), szakasz felezőpontja ($F = \\left(\\frac{x_1+x_2}{2}, \\frac{y_1+y_2}{2}\\right)$).\n### II. Egyenes egyenlete: Normálvektoros alak: $A(x-x_0) + B(y-y_0) = 0$, ahol $\\vec{n}(A,B)$ a normálvektor.\n### III. Kör egyenlete: Középpontos kör: $(x-u)^2 + (y-v)^2 = r^2$, ahol $K(u,v)$ a középpont és $r$ a sugár.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Távolság és felezőpont képlete -> 2. Az egyenes normálvektoros és irányvektoros alakja -> 3. A kör egyenletének felírása.",
        "kviz": [{"k": "Az $(x-2)^2 + (y+3)^2 = 16$ egyenletű kör sugara 4 egység.", "v": True, "m": "Mivel a jobb oldalon $r^2 = 16 áll, a sugár $r = 4$."}]
    },
    "9. Térgeometria (Testek felszíne és térfogata)": {
        "alcim": "Hasáb, henger, gúla, kúp és gömb felszín- és térfogatszámítása",
        "kulcsszavak": ["Henger", "Kúp", "Gúla", "Gömb", "Felszín és Térfogat"],
        "audio_szoveg": "A térgeometria a háromdimenziós testek metrikus tulajdonságaival, felszínével és térfogatával foglalkozik...",
        "vazlat": "### I. Henger és Hasáb: $V = T_{alap} \\cdot M$, $F_eszín = 2 \\cdot T_{alap} + T_{palást}$.\n### II. Gúla és Kúp (csúcsos testek): $V = \\frac{T_{alap} \\cdot M}{3}$. Kúp palástja: $r \\cdot \\pi \\cdot alkotó$.\n### III. Gömb: Térfogat $V = \\frac{4}{3}R^3\\pi$, Felszín $F = 4R^2\\pi$.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hasábok és hengerek egységes térfogatszámítása -> 2. A csúcsos testek $\\frac{1}{3}$-os szabálya -> 3. A gömb egyedi képletei.",
        "kviz": [{"k": "Egy egyenes körkúp térfogata pontosan harmada az azonos alappal és magassággal rendelkező hengerének.", "v": True, "m": "Igen, a csúcsos testek miatt ott szerepel az $1/3$-os szorzó."}]
    },
    "10. Valószínűségszámítás és Statisztika": {
        "alcim": "Klasszikus valószínűség, binomiális eloszlás, átlag, medián, módusz és szórás",
        "kulcsszavak": ["Klasszikus valószínűség", "Binomiális eloszlás", "Átlag", "Medián és Módusz", "Szórás"],
        "audio_szoveg": "A valószínűségszámítás és a statisztika a véletlen események és a tömegjelenségek elemzésének tudománya...",
        "vazlat": "### I. Klasszikus valószínűség: $P(A) = \\frac{\\text{kedvező esetek}}{\\text{összes lehetséges eset}}$. Binomiális eloszlás képlete ismétlődő kísérletekre.\n### II. Statisztikai középértékek:\n- Átlag (összeg / darabszám).\n- Medián (nagyság szerinti sorrend közepe).\n- Módusz (leggyakrabban előforduló elem).\n### III. Szórás: Az adatok átlagtól való eltérésének mérőszáma.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszikus valószínűség modellje -> 2. Statisztikai középértékek (átlag, medián, módusz) jelentése -> 3. Szórás fogalma.",
        "kviz": [{"k": "A medián kiszámításához a statisztikai adatokat először nagyság szerint sorba kell rendezni.", "v": True, "m": "Igen, a medián a sorozat középső eleme."}]
    },
    "11. Gráfelméleti alapfogalmak és alkalmazások": {
        "alcim": "Csúcsok, élek, fokszámok összege, összefüggő gráfok, fák és Euler-vonal",
        "kulcsszavak": ["Csúcsok és élek", "Fokszámtétel", "Fa gráf", "Euler-út"],
        "audio_szoveg": "A gráfelmélet pontok (csúcsok) és az azokat összekötő vonalak (élek) hálózatainak szerkezetét vizsgálja...",
        "vazlat": "### I. Alapfogalmak: Csúcsok halmaza ($V$), élek halmaza ($E$); csúcs fokszáma ($d(v)$ - belőle kiinduló élek száma).\n### II. Fokszámtétel (kézfogási lemma): A csúcsok fokszámainak összege pontosan kétszerese az élek számának ($\\sum d(v) = 2e$). Ennek következtében a páratlan fokszámú csúcsok száma mindig páros.\n### III. Különleges gráfok: Teljes gráf ($K_n$), Fa gráf (összefüggő, körmentes, $n$ csúcshoz $n-1$ él tartozik), Euler-vonal (minden élen egyszer megy át).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Gráfok definíciója és elemei -> 2. A fokszámtétel és következményei -> 3. Fa gráfok tulajdonságai -> 4. Euler-út létezésének feltétele.",
        "kviz": [{"k": "Egy véges gráfban a páratlan fokszámú csúcsok száma mindig páros szám.", "v": True, "m": "A fokszámtétel miatt ez matematikai törvényszerűség."}]
    },
    "12. Exponenciális és logaritmikus egyenletek": {
        "alcim": "Azonos alapra hozás módszere, logaritmálás, új ismeretlen bevezetése",
        "kulcsszavak": ["Azonos alapra hozás", "Új ismeretlen bevezetése ($u = a^x$)", "Kikötések", "Monotonitás"],
        "audio_szoveg": "Az exponenciális és logaritmusos egyenletek megoldásakor a hatványozási és logaritmikai szabályokat alkalmazzuk...",
        "vazlat": "### I. Exponenciális egyenletek: Azonos alapra hozás ($a^{f(x)} = a^{g(x)} \\implies f(x) = g(x)$), vagy új ismeretlen bevezetése ($u = a^x$ helyettesítéssel másodfokúvá alakítás).\n### II. Logaritmikus egyenletek: Szigorú kikötések (a logaritmus alapja $>0, \\neq 1$, a logaritmus alatti kifejezés $>0$); azonos alapú logaritmusok összevonása vagy egyenlőséggé alakítása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Exponenciális egyenletek megoldási technikái -> 2. Helyettesítéses módszer -> 3. Logaritmikus egyenletek kötelező kikötései.",
        "kviz": [{"k": "Logaritmikus egyenlet megoldásakor nem szükséges ellenőrizni a gyököket, ha a logaritmus alatti kifejezést nem vizsgáltuk előre.", "v": False, "m": "De igen, a kikötések (belső kifejezés $>0$) elmulasztása hamis gyökökhöz vezethet."}]
    },
    "13. Trigonometrikus egyenletek": {
        "alcim": "Alap szögfüggvényes egyenletek megoldása a periodicitás figyelembevételével",
        "kulcsszavak": ["Egységkör", "Periodicitás ($360^\\circ$ vagy $2\\pi$)", "Alapazonosságok", "Megoldássorozatok"],
        "audio_szoveg": "A trigonometrikus egyenletek olyan egyenletek, amelyekben az ismeretlen szög szögfüggvény alatt szerepel...",
        "vazlat": "### I. Alapösszefüggések: $\\sin^2(x) + \\cos^2(x) = 1$, $\\tan(x) = \\frac{\\sin(x)}{\\cos(x)}$.\n### II. Megoldás menete: Az egyenlet visszavezetése egy alap szögfüggvényes értékre (pl. $\\sin(x) = 0.5$).\n### III. Periodicitás: Mivel a szinusz és koszinusz $360^\\circ$-onként ($2\\pi$-nként) ismétlődik, a teljes megoldássorozatot fel kell írni (pl. $x = 30^\\circ + k \\cdot 360^\\circ$ és $x = 150^\\circ + k \\cdot 360^\\circ$, ahol $k \\in \\mathbb{Z}$).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trigonometrikus alapazonosságok -> 2. Az egységkör szerepe a gyökök keresésében -> 3. A periodikus megoldássorozatok felírása.",
        "kviz": [{"k": "A szinuszfüggvény értéke $180^\\circ$-onként ismétlődik teljes ciklusban.", "v": False, "m": "A szinusz és koszinusz alapciklusa $360^\\circ$ ($2\\pi$)."}]
    },
    "14. Vektorműveletek és a skaláris szorzat": {
        "alcim": "Összeadás, kivonás, számmal szorzás, skaláris szorzat és két vektor hajlásszöge",
        "kulcsszavak": ["Vektorműveletek", "Skaláris szorzat", "Merőlegesség feltétele", "Hajlásszög"],
        "audio_szoveg": "A vektorok nagysággal és iránnyal rendelkező mennyiségek, amelyek algebrai úton is remekül kezelhetők...",
        "vazlat": "### I. Vektorműveletek koordinátákban: $\\vec{a} + \\vec{b} = (a_1+b_1, a_2+b_2)$, vektor hossza (abszolút értéke): $|\\vec{a}| = \\sqrt{a_1^2 + a_2^2}$.\n### II. Skaláris szorzat: $\\vec{a} \\cdot \\vec{b} = a_1b_1 + a_2b_2 = |\\vec{a}| \\cdot |\\vec{b}| \\cdot \\cos(\\alpha)$.\n### III. Merőlegesség: Két vektor akkor és csak akkor merőleges egymásra, ha a skaláris szorzatuk pontosan 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Vektorok definíciója és koordinátás műveletei -> 2. A skaláris szorzat kétféle kiszámítási módja -> 3. Merőlegesség és hajlásszög meghatározása.",
        "kviz": [{"k": "Ha két nem nulla vektor skaláris szorzata 0, akkor a két vektor merőleges egymásra.", "v": True, "m": "Mivel $\\cos(90^\\circ) = 0$, a szorzat is zéró lesz."}]
    },
    "15. Számelmélet: Oszthatóság, prímek, LNKO és LKKT": {
        "alcim": "Oszthatósági szabályok, a számelmélet alaptétele, legnagyobb közös osztó és legkisebb közös többszörös",
        "kulcsszavak": ["Prímszámok", "Számelmélet alaptétele", "LNKO", "LKKT"],
        "audio_szoveg": "A számelmélet az egész számok oszthatósági törvényszerűségeit, a prímeket és a közös osztókat vizsgálja...",
        "vazlat": "### I. Oszthatósági szabályok: 2, 3, 4, 5, 9, 10-zel való oszthatóság jegyei.\n### II. A számelmélet alaptétele: Minden 1-nél nagyobb egész szám egyértelműen felírható prímszámok szorzataként (prímtényezős felbontás).\n### III. LNKO és LKKT: Legnagyobb közös osztó (közös prímek legkisebb kitevőjű szorzata) és Legkisebb közös többszörös (összes prím legnagyobb kitevőjű szorzata). Két szám szorzata egyenlő az LNKO és az LKKT szorzatával ($a \\cdot b = \\text{LNKO} \\cdot \\text{LKKT}$).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Oszthatósági szabályok összefoglalása -> 2. A számelmélet alaptétele és prímtényezős felbontás -> 3. LNKO és LKKT számítása.",
        "kviz": [{"k": "A 12 és a 18 legnagyobb közös osztója (LNKO) a 6.", "v": True, "m": "$12 = 2^2 \\cdot 3$ és $18 = 2 \\cdot 3^2$, a közös elemek legkisebb kitevővel: $2^1 \\cdot 3^1 = 6$."}]
    },
    "16. Differenciálszámítás (Deriválás) bevezetése": {
        "alcim": "A differenciahányados, derivált fogalma, hatványfüggvény deriválása és érintő meredeksége",
        "kulcsszavak": ["Derivált", "Érintő meredeksége", "Deriválási szabályok", "Szélsőérték ($f'(x)=0$)"],
        "audio_szoveg": "A differenciálszámítás a függvények változási sebességét, növekedési ütemét és a görbék érintőit vizsgálja...",
        "vazlat": "### I. Geometriai jelentés: Egy függvény grafikus pontjában vett derivált értéke megegyezik az adott ponthoz húzott érintő meredekségével ($m = f'(x_0)$).\n### II. Alapvető deriválási szabályok:\n- Konstans deriváltja: $(c)' = 0$.\n- Hatványfüggvény: $(x^n)' = n \\cdot x^{n-1}$.\n- Összeg/különbség deriváltja a tagok deriváltjának összege/különbsége.\n### III. Alkalmazás (Szélsőérték): Ahol a függvénynek lokális minimuma vagy maximuma van, ott a derivált értéke 0 ($f'(x) = 0$).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A derivált geometriai jelentése (érintő) -> 2. Hatványfüggvények deriválási szabálya -> 3. Szélsőértékek keresése a derivált segítségével.",
        "kviz": [{"k": "Az $f(x) = x^4$ függvény deriváltja $f'(x) = 4x^3$.", "v": True, "m": "A kitevő előrekerül szorzóként, a hatvány pedig eggyel csökken."}]
    }
}

# Villámkártyák (Flashcards)
flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra, epika és dráma sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a szerkesztője?", "a": "1908-ban indult, Osvát Ernő szerkesztette."},
    {"q": "Mi a központi szállóige Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.”"}
]
flashcards_nyelvtan = [
    {"q": "Mi a 4 helyesírási alapelv?", "a": "Kiejtés, szóelemzés, hagyomány, egyszerűsítés."},
    {"q": "Mi a toldalékok sorrendje?", "a": "Tő + Képző + Jel + Rag."}
]
flashcards_tortenelem = [
    {"q": "Mikor adta ki Nagy Lajos az Ősiség törvényét?", "a": "1351-ben."},
    {"q": "Mikor esett el Buda (török kéz)?", "a": "1541. augusztus 29."}
]
flashcards_matek = [
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Melyik tétel általánosítja Pitagoraszt?", "a": "Koszinusztétel."}
]

# Idővonalak
timeline_irodalom = [{"ev": "1848–1849", "cim": "Forradalom lírája", "leiras": "Petőfi és Arany."}, {"ev": "1908", "cim": "Nyugat", "leiras": "Ady és a modern líra."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihany", "leiras": "Szórványemlék."}, {"ev": "1790–1820", "cim": "Nyelvújítás", "leiras": "Kazinczy."}]
timeline_tortenelem = [{"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István."}, {"ev": "1526", "cim": "Mohács", "leiras": "Középkori állam bukása."}]
timeline_matek = [{"ev": "Kr. e. VI.", "cim": "Pitagorasz", "leiras": "Derékszögű háromszög."}, {"ev": "1687", "cim": "Newton", "leiras": "Deriválás."}]

# Detektív Játék (10-10 kérdés)
detektiv_irodalom = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Új versek", "Arany János: Toldi", "Radnóti Miklós"], "info": "A felelősségvállalás parancsa."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb...”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János", "Ady Endre"], "info": "Petőfi forradalmi felhívó lírája."},
    {"idezet": "„Mondottam, ember: küzdj és bízva bízzál!”", "helyes": "Madách Imre: Az ember tragédiája", "opciok": ["Madách Imre: Az ember tragédiája", "Arany János", "Vörösmarty", "Katona József"], "info": "Az Úr szózata a 15. színben."},
    {"idezet": "„Góg és Magóg fia vagyok én, / Hiába döngetek kaput, falat...”", "helyes": "Ady Endre: Góg és Magóg fia vagyok én...", "opciok": ["Ady Endre: Góg és Magóg fia vagyok én...", "Babits Mihály", "József Attila", "Kosztolányi"], "info": "Ady 1906-os kötetének nyitóverse."},
    {"idezet": "„Békévé oldja az emlékezés, / hogy tamáskodunk s jól van ez így errefelé.”", "helyes": "József Attila: A Dunánál", "opciok": ["József Attila: A Dunánál", "Radnóti Miklós", "Babits Mihály", "Vajda János"], "info": "Történelmi szembenézés verse."},
    {"idezet": "„Isten csodája vagyok, / Fényes, tiszta láng...”", "helyes": "Csokonai Vitéz Mihály: A Reményhez", "opciok": ["Csokonai Vitéz Mihály: A Reményhez", "Berzsenyi Dániel", "Petőfi Sándor", "Vörösmarty"], "info": "A remény elvesztésének mesterműve."},
    {"idezet": "„Itt ül a nyakunkon a német, / Koreszmék kútfejénél lassan rág...”", "helyes": "Vajda János: A virrasztók", "opciok": ["Vajda János: A virrasztók", "Ady Endre", "Illyés Gyula", "Petőfi Sándor"], "info": "Vajda társadalombírálata."},
    {"idezet": "„Rám zúdult a kietlen, nyers valóság, / S a mindenség szörnyű titka megütött.”", "helyes": "Kosztolányi Dezső: Boldog, szomorú dal", "opciok": ["Kosztolányi Dezső: Boldog, szomorú dal", "Babits Mihály", "Tóth Árpád", "Juhász Gyula"], "info": "Létösszegző versek."},
    {"idezet": "„Hol sírjaink domborulnak, / Unokáink lesiratják...”", "helyes": "Vörösmarty Mihály: Szózat", "opciok": ["Vörösmarty Mihály: Szózat", "Petőfi Sándor", "Kölcsey Ferenc", "Berzsenyi Dániel"], "info": "Nemzeti összetartozás kiáltványa."},
    {"idezet": "„Oly korban éltem e földön, / mikor az ember úgy elvadult...”", "helyes": "Radnóti Miklós: Töredék", "opciok": ["Radnóti Miklós: Töredék", "Babits Mihály", "József Attila", "Kosztolányi"], "info": "Megőrzött humánum."}
]

detektiv_nyelvtan = [
    {"idezet": "„barátság [kiejtve: baraccság]”", "helyes": "Összeolvadás mássalhangzótörvény", "opciok": ["Összeolvadás mássalhangzótörvény", "Zöngésségi részleges hasonulás", "Írásban jelölt teljes hasonulás", "Mássalhangzó-kiesés"], "info": "t + s -> [ccs]."},
    {"idezet": "„lila dalra kelt az éjcsend”", "helyes": "Szinesztézia (Költői kép)", "opciok": ["Szinesztézia (Költői kép)", "Megszemélyesítés", "Metonímia", "Szinekdoché"], "info": "Érzékkeverés."},
    {"idezet": "„vasgolyó [vazsgolyó]”", "helyes": "Zöngésség szerinti részleges hasonulás", "opciok": ["Zöngésség szerinti részleges hasonulás", "Képzés helye szerinti hasonulás", "Teljes hasonulás", "Összeolvadás"], "info": "Zöngésítés."},
    {"idezet": "„ház-as-ság-ok-at”", "helyes": "Szótő + Képző + Képző + Jel + Rag", "opciok": ["Szótő + Képző + Képző + Jel + Rag", "Szótő + Jel + Rag + Képző", "Szótő + Rag + Jel + Képző", "Szótő + Képző + Rag + Jel"], "info": "Kötött sorrend."},
    {"idezet": "„MÁV, OTP, ELTE”", "helyes": "Betűszók (Mozaikszók)", "opciok": ["Betűszók (Mozaikszók)", "Szóösszevonások", "Szóelvonások", "Betűszerkezetek"], "info": "Kezdőbetűk."},
    {"idezet": "„Főgáz, Malév”", "helyes": "Szóösszevonások", "opciok": ["Szóösszevonások", "Betűszók", "Mozaikszók", "Csonkítások"], "info": "Szótagok."},
    {"idezet": "„A kutyából nem lesz szalonna.”", "helyes": "Közmondás", "opciok": ["Közmondás", "Szólás", "Szállóige", "Kontextus"], "info": "Tanulság."},
    {"idezet": "„Feni a fogát valamire.”", "helyes": "Szólás", "opciok": ["Szólás", "Közmondás", "Szállóige", "Metafora"], "info": "Képszerű."},
    {"idezet": "„A kocka el van vetve.”", "helyes": "Szállóige", "opciok": ["Szállóige", "Közmondás", "Szólás", "Közhely"], "info": "Caesar."},
    {"idezet": "„egészségünkre / egéssségünkre”", "helyes": "Helyesírás és kiejtés eltérése (Kiejtés elve)", "opciok": ["Helyesírás és kiejtés eltérése (Kiejtés elve)", "Hagyomány elve", "Szóelemzés elve", "Egyszerűsítés elve"], "info": "Kiejtés."}
]

detektiv_tortenelem = [
    {"idezet": "„Ius resistendi (A nemesek joga az ellenállásra)”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Nagy Lajos 1351", "Szent István", "Kollonics"], "info": "Rendi szabadságjog."},
    {"idezet": "„Eb ura fakó, József császár nem királyunk!”", "helyes": "1707-es Ónodi országgyűlés (Trónfosztás)", "opciok": ["1707-es Ónodi országgyűlés (Trónfosztás)", "1849", "1526", "1608"], "info": "Habsburg-trónfosztás."},
    {"idezet": "„Aki nincs ellenünk, az velünk van.”", "helyes": "Kádár-rendszer konszolidációs politikája", "opciok": ["Kádár-rendszer konszolidációs politikája", "Rákosi-diktatúra", "Horthy", "Bethlen"], "info": "Megegyezés."},
    {"idezet": "„Minden tíz falu építsen egy templomot...”", "helyes": "Szent István király törvényei", "opciok": ["Szent István király törvényei", "Szent László", "Könyves Kálmán", "II. András"], "info": "Egyházszervezet."},
    {"idezet": "„Segédlettel, pénzzel támogatjuk a szabad nemzeteket...”", "helyes": "Truman-doktrína (1947)", "opciok": ["Truman-doktrína (1947)", "Brezsnyev", "Marshall", "Molotov"], "info": "Megfékezési politika."},
    {"idezet": "„Békévé oldja az emlékezés...”", "helyes": "A reformkor és polgári átalakulás", "opciok": ["A reformkor és polgári átalakulás", "Kiegyezés", "Trianon", "Rendszerváltás"], "info": "Megbékélés."},
    {"idezet": "„Az ország területének 2/3 része elcsatolva.”", "helyes": "Trianoni békediktátum (1920)", "opciok": ["Trianoni békediktátum (1920)", "Párizsi béke", "Szatmár", "Pozsony"], "info": "Katasztrofális béke."},
    {"idezet": "„Cél a proletárdiktatúra és földek államosítása.”", "helyes": "1919-es Magyar Tanácsköztársaság", "opciok": ["1919-es Magyar Tanácsköztársaság", "1956", "1989", "1848"], "info": "Kommunista kísérlet."},
    {"idezet": "„Szabad, felelős magyar kormány Batthyány vezetésével.”", "helyes": "1848-as forradalom és áprilisi törvények", "opciok": ["1848-as forradalom és áprilisi törvények", "1867", "1918", "1944"], "info": "Független Magyarország."},
    {"idezet": "„A szocialista tábor védelmében katonai beavatkozás.”", "helyes": "Brezsnyev-doktrína", "opciok": ["Brezsnyev-doktrína", "Truman", "Eisenhower", "Monroe"], "info": "Korlátozott szuverenitás."}
]

detektiv_matek = [
    {"idezet": "a² = b² + c² - 2bc · cos(α)", "helyes": "Koszinusztétel (Általános háromszögekre)", "opciok": ["Koszinusztétel (Általános háromszögekre)", "Szinusztétel", "Pitagorasz", "Héron"], "info": "Pitagorasz általánosítása."},
    {"idezet": "(x^n)' = n · x^(n-1)", "helyes": "Hatványfüggvény deriválási szabálya", "opciok": ["Hatványfüggvény deriválási szabálya", "Logaritmus", "Binomiális", "Sorozat"], "info": "Differenciálás."},
    {"idezet": "V = (r²π · M) / 3", "helyes": "Egyenes körkúp térfogatképlete", "opciok": ["Egyenes körkúp térfogatképlete", "Henger", "Gömb", "Gúla"], "info": "Körkúp térfogat."},
    {"idezet": "∑ d(v) = 2 · e", "helyes": "Gráfelméleti fokszámtétel (Kézfogási lemma)", "opciok": ["Gráfelméleti fokszámtétel (Kézfogási lemma)", "Euler", "De Morgan", "Binomiális"], "info": "Fokszámtétel."},
    {"idezet": "x1,2 = (-b ± √(b² - 4ac)) / (2a)", "helyes": "Másodfokú egyenlet megoldóképlete", "opciok": ["Másodfokú egyenlet megoldóképlete", "Viéte", "Diszkrimináns", "Gyöktényezős"], "info": "Megoldóképlet."},
    {"idezet": "an = a1 + (n - 1)d", "helyes": "Számtani sorozat n-edik tagjának képlete", "opciok": ["Számtani sorozat n-edik tagjának képlete", "Mértani", "Kamatos", "Összegképlet"], "info": "Számtani sorozat."},
    {"idezet": "P(A) = Kedvező / Összes", "helyes": "Klasszikus valószínűség kiszámítása", "opciok": ["Klasszikus valószínűség kiszámítása", "Binomiális", "Szórás", "Kombináció"], "info": "Valószínűség."},
    {"idezet": "sin²(x) + cos²(x) = 1", "helyes": "Trigonometrikus alapazonosság", "opciok": ["Trigonometrikus alapazonosság", "Szinusz", "Koszinusz", "Tangens"], "info": "Alapazonosság."},
    {"idezet": "a · b = |a| · |b| · cos(α)", "helyes": "Két vektor skaláris szorzata", "opciok": ["Két vektor skaláris szorzata", "Összeadás", "Vektorhossz", "Hajlásszög"], "info": "Skaláris szorzat."},
    {"idezet": "Cn = C0 · (1 + p/100)^n", "helyes": "Kamatos kamat számítási képlete", "opciok": ["Kamatos kamat számítási képlete", "Egyszerű kamat", "Gyűjtőjáradék", "Mértani összeg"], "info": "Kamatos kamat."}
]

# Állapotkezelés
if 'xp' not in st.session_state: st.session_state.xp = 180
if 'level' not in st.session_state: st.session_state.level = 2
if 'streak' not in st.session_state: st.session_state.streak = 4
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
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

def ai_generalas(prompt_text, audio_bytes=None, mime_type=None):
    api_k = get_api_key()
    if not api_k: return "⚠️ Nincs beállítva a GEMINI_API_KEY kulcs!"
    try:
        client = genai.Client(api_key=api_k)
        contents_input = [prompt_text]
        if audio_bytes and mime_type:
            contents_input.append({"inline_data": {"mime_type": mime_type, "data": audio_bytes}})
        res = client.models.generate_content(model='gemini-2.0-flash', contents=contents_input)
        return res.text if res and res.text else "Nincs válasz."
    except Exception as e: return f"Hiba: {e}"

# Oldalsáv & Tantárgy választó
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
        "📚 Tételek & Vázlatok", "🎧 Hangoskönyv (Monológ)", "🎴 Villámkártyák (Flashcards)",
        "🎙️ Szóbeli Szimulátor (Beszéd / Írás)", "✍️ Esszé & Feladatmegoldó Labor",
        "🎭 Tantárgyi Detektív Játék", "🧭 Tantárgyi Idővonal & Térkép",
        "🏆 Nagy Próbavizsga", "🤖 AI Érettségi Mentor"
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

# Menüpontok logikája
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

elif menupont == "🎧 Hangoskönyv (Monológ)":
    tetel = st.selectbox("Válassz tételt hangoskönyvhöz:", list(aktiv_adatbazis.keys()))
    if st.button("▶️ Hangos indítás"):
        tts = gTTS(text=f"{tetel}. {aktiv_adatbazis[tetel]['alcim']}", lang='hu', slow=False)
        f = io.BytesIO(); tts.write_to_fp(f); f.seek(0); st.audio(f, format="audio/mp3")

elif menupont == "🎴 Villámkártyák (Flashcards)":
    idx = get_daily_index(len(aktiv_flashcards))
    k = aktiv_flashcards[idx]
    st.subheader(f"Napi Villámkártya ({tantargy_cimke})")
    if not st.session_state.card_flipped:
        st.markdown(f"<div class='flashcard'>❓ {k['q']}</div>", unsafe_allow_html=True)
        if st.button("🔄 Megfordítás"): st.session_state.card_flipped = True; st.rerun()
    else:
        st.markdown(f"<div class='flashcard' style='background:linear-gradient(135deg, #064e3b, #065f46);'>💡 {k['a']}</div>", unsafe_allow_html=True)
        if st.button("Következő"): st.session_state.card_flipped = False; st.rerun()

elif menupont == "🎙️ Szóbeli Szimulátor (Beszéd / Írás)":
    st.subheader("Szóbeli vizsga szimuláció")
    tetel = st.selectbox("Vizsgatétel:", list(aktiv_adatbazis.keys()))
    audio = st.audio_input("Mondd el a feleleted:")
    if audio and st.button("Vizsga értékelése"):
        st.write(ai_generalas(f"Értékeld ezt a szóbeli választ a(z) {tetel} tételben:", audio_bytes=audio.read(), mime_type="audio/wav"))

elif menupont == "✍️ Esszé & Feladatmegoldó Labor":
    munka = st.text_area("Másold be az esszét vagy matek feladatot:")
    if st.button("Elemzés és javítás") and munka:
        st.markdown(f"<div class='deep-text'>{ai_generalas(f'Elemezd és javítsd ki: {munka}')}</div>", unsafe_allow_html=True)

elif menupont == "🎭 Tantárgyi Detektív Játék":
    st.title(f"🎭 {tantargy_cimke} Detektív Játék")
    st.caption(f"Felismered a legfontosabb {tantargy_cimke} idézeteket, forrásokat és képleteket?")
    
    idx = get_daily_index(len(aktiv_detektiv))
    f = aktiv_detektiv[idx]
    
    random.seed(datetime.date.today().toordinal() // FRISSITESI_GYAKORISAG_NAPOKBAN)
    kevert_opciok = f['opciok'].copy()
    random.shuffle(kevert_opciok)
    
    st.markdown(f"""
    <div class='topic-card' style='border-color:#ec4899; text-align:center;'>
        <h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    valasztott_tipp = st.radio("Válaszd ki a helyes megfejtést:", kevert_opciok, index=None, key=f"detektiv_radio_{idx}")
    
    if st.button("🔍 Tipp ellenőrzése"):
        if valasztott_tipp is None:
            st.warning("Kérlek, válassz egy választ először!")
        elif valasztott_tipp == f['helyes']:
            st.balloons()
            st.session_state.xp += 30
            st.success(f"TÖKÉLETES! 🎉 Helyes válasz! (+30 XP)\n\n📌 Magyarázat: {f['info']}")
        else:
            st.error(f"Sajnos nem! ❌ A helyes válasz: **{f['helyes']}**\n\n📌 Magyarázat: {f['info']}")

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
        v = ai_generalas("Vlaszolj a diák hangüzenetére érettségi tanárként", audio_bytes=audio_k.read(), mime_type="audio/wav")
        st.session_state.chat_history.append({"role": "user", "text": "🎙️ *(Hangüzenet)*"})
        st.session_state.chat_history.append({"role": "ai", "text": v})
        st.rerun()

    k = st.text_input("Írj a mentornak:")
    if st.button("Írásbeli küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        v = ai_generalas(f"Vlaszolj érettségi tanárként: {k}")
        st.session_state.chat_history.append({"role": "ai", "text": v})
        st.rerun()
