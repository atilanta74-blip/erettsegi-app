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

# Sötét téma és vizuális stílusok
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
        padding: 16px;
        border-radius: 8px;
        margin-top: 15px;
    }
    .audio-card {
        background-color: #182234;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 18px;
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

# Bővített tételtár: Részletes háttér, 2 perces hangos monológ, kibővített kvíz
tetelek = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfaja, nagykőrösi korszak és Őszikék lélektana",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja"],
        "audio_szoveg": """
Arany János a magyar irodalom történetének legnagyobb balladaírója. A műfajt Greguss Ágost esztéta nyomán tragédia dalban elbeszélveként szoktuk meghatározni, ami arra utal, hogy a líra, az epika és a dráma műnemi jegyei egyszerre jelennek meg benne. A művek feszültségét az úgynevezett balladai homály, a tömörítés és a kihagyásos szerkesztésmód teremti meg. 
Arany balladaformája két meghatározó alkotói korszakra bontható. Az első az 1850-es évek nagykőrösi korszaka. A szabadságharc leverését követő elnyomás éveiben a költő a történelmi allegóriák eszközével ébresztette a nemzeti öntudatot. Ennek csúcspontja A walesi bárdok és a Szondi két apródja, amelyek a zsarnoksággal szembeni meg nem alkuvás és a hűség örök példái. Ugyanebben az időszakban születtek meg a mély lélektani balladák is, mint az Ágnes asszony vagy a Tetemre hívás, amelyek a bűn és a lelkiismeret-furdalás tébolyító hatását ábrázolják. 
A második korszak a kései, 1877-es Őszikék időszaka a Margitszigeten, amikor a Kapcsos könyvbe lejegyzett műveiben már a modernizálódó, elidegenedő nagyvárosi világ krízisei jelennek meg. A Híd-avatásban az öngyilkosok seregszemléjén keresztül a társadalmi felelősségvállalás kérdését veti fel.
        """,
        "vazlat": """
### 1. A műfaj elméleti háttere
- **Műfaji szintézis:** Lírai forma és dallamosság, epikus történetvezetés, drámai konfliktusok és dialógusok.
- **Formanyelv:** *Balladai homály*, idősíkok váltogatása, kihagyásos szerkesztés (*ellipszis*).

### 2. A nagykőrösi korszak (1850-es évek)
- **Történelmi-allegorikus balladák:** Válasz a Bach-korszak önkényuralmára; hűség és erkölcsi ellenállás (*A walesi bárdok*, *Szondi két apródja* – többszólamúság, kétféle értékrend).
- **Lélektani balladák:** Bűn és megbomló elme (*Ágnes asszony* – a lepedőmosás mint a bűn letörölhetetlenségének szimbóluma; *Tetemre hívás* – istenítélet).
- **Népies-románcos művek:** *Tengeri-hántás*, *Vörös Rébék*.

### 3. Az Őszikék korszaka (1877, Margitsziget)
- Időskori rezignáció, technikai civilizáció és elidegenedés.
- *Híd-avatás:* Haláltánc-motívum (*danse macabre*), a nagyvárosi nyomor és céltalanság társadalomrajza.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** Greguss-féle meghatározás, a három műnem találkozása, Arany helye a műfaj történetében.
2. **Nagykőrös (1 perc):** Nemzeti gyász és burkolt ellenállás (*Szondi két apródja*), valamint a lélektani bűntudat ábrázolása (*Ágnes asszony*).
3. **Őszikék (1 perc):** A nagyvárosi élet válságai és a Margitszigeti kései líra (*Híd-avatás* haláltánca).
4. **Befejezés (30 mp):** A klasszikus magyar ballada nyelvi és formai csúcspontjának értékelése.
        """,
        "kviz": [
            {"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A meghatározás a líra, epika és dráma ötvözésére utal."},
            {"k": "A walesi bárdok nyíltan, burkolás nélkül támadta Ferenc Józsefet.", "v": False, "m": "Allegorikus formában, a walesi monda köntösében fogalmazta meg az ellenállást."},
            {"k": "Az Ágnes asszony a nagykőrösi lélektani balladák sorába tartozik.", "v": True, "m": "A lelkiismeret-furdalás és a megőrülés belső folyamatát bontja ki."},
            {"k": "A Szondi két apródja műben Drégely várának ostroma elevenedik meg.", "v": True, "m": "Szondi György török elleni hősi halálát dolgozza fel."},
            {"k": "A Híd-avatás című kései ballada a Margitszigeten, az Őszikék korszakban született.", "v": True, "m": "1877-ben írta a Margitszigeten a Kapcsos könyvbe."}
        ]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus határán, a polgári meghasonlás kérdése",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi", "Ali Csorbadzsi", "Krisztyán Tódor"],
        "audio_szoveg": """
Jókai Mór 1872-ben megjelent Az arany ember című regénye az író legszemélyesebb és legmélyebb lélektani műve. Bár stílusában a romantika gazdag mesemondása és éles kontrasztjai dominálnak, a mű társadalomrajza és jellemábrázolása már a realizmus felé mutat. 
A regény központi alakja Timár Mihály, a mindent arannyá változtató tehetséges nagypolgár, akit a vagyon megszerzésének körülményei és a kényszerű házassága miatt súlyos lelkiismereti válság gyötör. A cselekmény egy kettős térszerkezetre épül fel. Az egyik oldalon Komárom és a modern kapitalista világ áll a rideg, hálából feleségül vett Timeával, ahol Timár sikeres, de boldogtalan. A másik oldalon a Senki szigete jelenik meg, amely a társadalomból kivonult, pénzmentes, romlatlan természeti idillt képviseli Noémivel és Teréza mamával. 
A regény feloldása csak a civilizációból való kilépéssel, a társadalmi én halálával és az újrakezdéssel valósulhat meg.
        """,
        "vazlat": """
### 1. Stílusszintézis és háttér
- 1872-es megjelenés; a polgári fejlődés árnyoldalainak realista ábrázolása romantikus elbeszélésmóddal ötvözve.
- Timár Mihály tragédiája: az anyagi felemelkedés és az erkölcsi tiszta lelkiismeret összeférhetetlensége.

### 2. Kettős világmodell és karakterpárhuzamok
- **A polgári világ (Komárom, Bécs):** Pénzuralom, rideg konvenciók, látszatboldogság (*Timea* – szoborszerű, hűséges, de szeretetlen hála).
- **A Senki szigete (Természeti utópia):** Társadalmon kívüli éden, pénzmentes tiszta szeretet (*Noémi* – ösztönös, érzelmes természetesség).
- **Ellenpontok:** *Brazovics Athanáz* (mohó spekuláció), *Krisztyán Tódor* (züllött zsarolás).
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** Jókai pályája, az 1872-es mű személyes jellege és stíluskettőssége.
2. **Timár jelleme (1 perc):** Az „arany ember” paradoxona: külső siker vs. belső morális válság.
3. **A két nő és két világ (1 perc):** Timea (Komárom ridegsége) és Noémi (Senki szigete utópiája) kontrasztja.
4. **Befejezés (30 mp):** A Balaton jegén bekövetkező sorsfordulat és a polgári társadalomból való kilépés tanulsága.
        """,
        "kviz": [
            {"k": "Timár Mihály felesége, Timea szerelemből ment hozzá Timárhoz.", "v": False, "m": "Timea csupán hálából kötött házasságot vele."},
            {"k": "A Senki szigete a pénz és ipari forradalom mintaképe a műben.", "v": False, "m": "A pénztől mentes, romantikus természeti menedék jelképe."},
            {"k": "Krisztyán Tódor a Balaton jegének rianásába fullad bele Timár kabátjában.", "v": True, "m": "Ez a véletlen halál teszi lehetővé Timár névtelenségét."},
            {"k": "Ali Csorbadzsi kincsét a Szent Borbála hajó szállította el süllyedése előtt.", "v": True, "m": "A búza közé rejtett kincs alapozza meg Timár vagyonát."},
            {"k": "A regényben a romantikus és a realista stílusjegyek egyszerre vannak jelen.", "v": True, "m": "A mesei fordulatok és a pontos gazdasági-társadalmi rajz ötvöződik."}
        ]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény műfaja, eszmék harca a történelemben",
        "kulcsszavak": ["Világdráma", "15 szín", "Ádám, Éva, Lucifer", "Küzdj és bízva bízzál"],
        "audio_szoveg": """
Madách Imre főműve, Az ember tragédiája 1859 és 1860 között született, a magyar nemzet legsötétebb válságidőszakában. A mű műfaja drámai költemény, más néven világdráma, amely az emberi létezés végső értelmét, a szabadság határait és az eszmék történelmi fejlődését vizsgálja. 
A dráma 15 színből áll. A keretszínekben, az első háromban és a tizenötödikben, a transzcendens világban zajlik az Úr és Lucifer fogadása. A közbülső tizenegy színben Ádám és Lucifer álomutazást tesznek a világtörténelem nagy korszakaiban. Ádám minden színben egy-egy új eszméért lelkesedik, ám Lucifer rámutat ezen eszmék elkorcsosulására. Egyetlen kivétel van: a francia forradalmat bemutató párizsi szín, amelyből Ádám nem csalódottan, hanem hittel telve ébred fel. 
A mű zárásában az Úr zárszava felülírja Lucifer hideg rációját: a küzdelem maga a cél.
        """,
        "vazlat": """
### 1. Műfaj és filozófiai gyökerek
- **Műfaj:** Drámai költemény (világdráma, könyvdráma) – Hegel dialektikája (tézis-antitézis-szintézis).
- **Szereplők filozófiai archetípusai:**
  - *Ádám:* Az örök küzdő emberi szellem, az eszmék keresője.
  - *Lucifer:* A hideg ész, a kritikai ráció, a tagadás és kétely szelleme.
  - *Éva:* Az érzelmek, a természet, az élet folytonossága és a megváltás ígérete.

### 2. A 15 szín szerkezeti íve
- **Keretszínek (1–3. és 15.):** Égi hierarchia, a Paradicsom elvesztése, és a záró feloldás a hófedte pusztaságban.
- **Történelmi színek (4–14.):**
  - Egyiptom (szabadság), Athén (demokrácia), Róma (élvezetek), Bizánc (vallás), Prága (tudomány), Párizs (forradalom), London (kapitalista piac), Falanszter (rideg tudomány), Űr (anyagtalanodás), Eszkimó szín (kihűlő Föld).
- **Konklúzió:** *„Mondottam, ember: küzdj és bízva bízzál!”*
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** A drámai költemény fogalma, a keletkezés kontextusa (szabadságharc utáni kiábrándulás).
2. **Karakterek dialektikája (1 perc):** Ádám cselekvési vágya, Lucifer destruktív logikája és Éva megtisztító jelenléte.
3. **Történelmi körkép (1 perc):** Eszmék felívelése és bukása; miért Párizs a Tragédia tengelye és csúcspontja.
4. **Befejezés (30 mp):** A 15. szín értelmezése: a determinizmus elutasítása és az etikai cselekvés imperatívusza.
        """,
        "kviz": [
            {"k": "Az ember tragédiája összesen 15 színből áll.", "v": True, "m": "4 keretszín és 11 történelmi szín alkotja a művet."},
            {"k": "Ádám a párizsi színből csalódottan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel és lelkesedéssel tér magához."},
            {"k": "A londoni színben a Temze partján a szereplők a nyitott sírba ugranak.", "v": True, "m": "A londoni haláltánc-jelenet a mű egyik legdrámaibb zárása."},
            {"k": "A falanszter színben Michelangelo és Platón büntetést kapnak egyéniségük miatt.", "v": True, "m": "A túlracionalizált társadalom elnyomja a művészi egyéniséget."},
            {"k": "A mű záró mondata: 'Mondottam, ember: küzdj és bízva bízzál!'.", "v": True, "m": "Az Úr szózata a küzdelem erkölcsi kötelességét hirdeti."}
        ]
    },
    "4. Mikszáth Kálmán prózája": {
        "alcim": "Anekdotizmus, novellisztika és a dzsentri világ ábrázolása",
        "kulcsszavak": ["Anekdota", "A tót atyafiak", "A jó palócok", "Beszterce ostroma", "Pongrácz István"],
        "audio_szoveg": """
Mikszáth Kálmán a 19. és 20. század fordulójának legkiválóbb prózaírója. Pályája hídként köti össze a romantika mesélő hagyományát a modern realizmussal. Művészetének alapköve az anekdota, azaz a csattanóra épülő, rövid, közvetlen hangú történetmesélés. 
Az országos hírnevet az 1880-as évek elején megjelent két novelláskötete hozta meg számára. Az 1881-es A tót atyafiak négy hosszabb elbeszélésben mutatja be a zord felvidéki hegyek között élő, tiszta erkölcsű embereket. Az 1882-es A jó palócok tizenöt rövid, tömör novellában ábrázolja a falu zárt, babonákkal teli közösségét és balladisztikus tragédiáit. 
Későbbi korszakának remekműve a Beszterce ostroma, amelyben a Don Quijote-i alakú Pongrácz István gróf tragikomikus történetén keresztül a hanyatló magyar nemesi világot szembesíti a valósággal.
        """,
        "vazlat": """
### 1. Az elbeszélői hang és stílus
- Élőbeszédszerű mesélés, szelíd irónia, empátia, anekdotikus szerkesztés.

### 2. A novelláskötetek párhuzama
- **A tót atyafiak (1881):** 4 terjedelmes elbeszélés; magashegyi ridegség, tiszta lelkű óriások (*Lapaj a híres dudás*, *Az a fekete folt*).
- **A jó palócok (1882):** 15 tömör novella; lenti lankás falu, balladisztikus kihagyások, babonák és bűntudat (*Bede Anna tartozása*).

### 3. A Beszterce ostroma (1895)
- **Pongrácz István gróf:** Anakronisztikus jellem, aki a középkori lovagkorban él a 19. század végén.
- **Társadalomkritika:** A dzsentri illúziók és a kapitalizálódó modern világ összeférhetetlensége.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** Mikszáth stílusa, a romantika és realizmus találkozása az anekdotában.
2. **Két kötet világa (1 perc):** *A tót atyafiak* és *A jó palócok* térbeli, formai és lélektani ellentéte.
3. **Beszterce ostroma (1 perc):** Pongrácz István Don Quijote-i szerepe mint a magyar dzsentri önáltatásának szimbóluma.
4. **Befejezés (30 mp):** Mikszáth hatása a modern magyar regényírás születésére.
        """,
        "kviz": [
            {"k": "A tót atyafiak kötetben 15 rövid novella kapott helyet.", "v": False, "m": "A tót atyafiakban 4 hosszabb, míg A jó palócokban 15 rövid novella van."},
            {"k": "A Bede Anna tartozása című novellában Erzsi megy el elhunyt nővére helyett a bíróságra.", "v": True, "m": "A tiszta palóc erkölcs és bűnbánat példája."},
            {"k": "Pongrácz István a modern vasútépítés élharcosa a Beszterce ostromában.", "v": False, "m": "Középkori várúrként éli életét Nedec várában."},
            {"k": "Mikszáth művészetének alapja az anekdotikus történetmondás.", "v": True, "m": "A szóbeli mesemondásból és apró történetekből építi fel regényeit."}
        ]
    },
    "5. Vajda János költészete": {
        "alcim": "Lírai magány, a Gina-szerelem és a szimbolizmus hajnala",
        "kulcsszavak": ["Gina-versek", "Montblanc", "A vaáli erdőben", "A virrasztók"],
        "audio_szoveg": """
Vajda János a 19. század második felének legmagányosabb magyar költője. Pályája a kiegyezés utáni Magyarország légüres terében bontakozott ki, ahol a meg nem értettség, a politikai passzivitás miatti keserűség és az egyéni elszigeteltség vált lírájának fő témájává. 
Költészetének legfontosabb vonulata a végzetes Gina-szerelem, amely évtizedeken át ihlette legnagyobb verseit. A Húsz év múlva című költeményében a híres Montblanc-metafora segítségével fejezi ki érzelmeit: a külvilág felé fagyos, elérhetetlen hegycsúcs képében mutatja meg a lélek mélyén örökké égő, el nem múló szerelmi tüzet. 
Filozofikus tájlírájának csúcsa A vaáli erdőben, ahol a gyermekkori táj békéje és a panteista természeti csend révén jut el a halállal való megbékélésig. Vajda új szimbólumalkotása már közvetlenül az Ady-féle modern szimbolizmust készíti elő.
        """,
        "vazlat": """
### 1. Történelmi és lélektani háttér
- A kiegyezés utáni csalódottság és politikai kiábrándulás (*A virrasztók*).
- A magány kultusza: az átokverte művész toposza.

### 2. A Gina-líra fejlődése
- Kratochwill Zsuzsanna (Gina) iránti viszonzatlan és pusztító szerelem.
- *Húsz év múlva (1876):* A Montblanc-hasonlat – a fagyos külső és az izzó belső magma kettőssége.
- *Harminc év után (1892):* Kései rezignáció, a vágyak végleges kihűlése.

### 3. Filozofikus csend-versek
- *A vaáli erdőben:* Panteisztikus egység a természettel; a megnyugvás és halálfélelem feloldása.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** Vajda mint híd Petőfi és Ady világa között; a korszak passzivitása.
2. **Gina-szerelem (1 perc):** A Montblanc-metafora elemzése (*Húsz év múlva*) és az örök szerelem mítosza.
3. **Filozofikus magány (1 perc):** *A vaáli erdőben* csend-motívuma és a természeti harmónia.
4. **Befejezés (30 mp):** A modern magyar szimbolizmus előkészítésének méltatása.
        """,
        "kviz": [
            {"k": "Vajda János szerelmi költészetének múzsája Kratochwill Zsuzsanna volt, akit Ginának nevezett.", "v": True, "m": "A Gina-ciklus egész életét végigkísérte."},
            {"k": "A Montblanc-metafora a 'Harminc év után' című vers központi képe.", "v": False, "m": "A Montblanc-hasonlat a Húsz év múlva című költeményben található."},
            {"k": "A vaáli erdőben a halállal való megbékélés és természeti csend verse.", "v": True, "m": "A gyermekkori erdő panteista békéjét énekli meg."}
        ]
    },
    "6. XIX. századi dráma: Ibsen és Csehov": {
        "alcim": "Az analitikus dramaturgia és a csehovi hangulatdráma megújítása",
        "kulcsszavak": ["Henrik Ibsen", "Analitikus dráma", "Nóra", "Anton Csehov", "Sirály", "Cseresznyéskert"],
        "audio_szoveg": """
A 19. század végén a polgári színház gyökeres formai és tartalmi átalakuláson ment keresztül. Két új irányzat határozta meg a modern európai drámafejlődést: a Henrik Ibsen által tökéletesített analitikus dráma és az Anton Csehov nevéhez fűződő hangulatdráma. 
Ibsen a Nóra vagy Babaszoba című művében az antik sorstragédiák szerkesztésmódját ülteti át a modern polgári otthonba. A drámai feszültséget nem a jelen eseményei, hanem a múltban elkövetett tettek fokozatos napvilágra kerülése adja. Nóra felismeri, hogy házasságában csupán játékszer volt, és az egyéni autonómia megteremtéséért elhagyja a családját. 
Ezzel szemben Csehov darabjaiban, mint a Sirály vagy a Cseresznyéskert, nincsenek látványos tettek és nyílt konfliktusok. Hősei cselekvésképtelenek, egymás mellett elbeszélő monológokban élnek. A drámát a belső hangulat, a líraiság és az elmúlás atmoszférája uralja.
        """,
        "vazlat": """
### 1. Henrik Ibsen: Az analitikus technika
- **Módszer:** A cselekmény a múltbeli titkok lépésről lépésre történő kiderüléséből fakad.
- **Nóra (Babaszoba, 1879):** A polgári látszatboldogság lelepleződése; a női emancipáció és az önálló személyiség joga.

### 2. Anton Csehov: A drámaiatlan dráma (Hangulatdráma)
- **Módszer:** Cselekményszegénység, párhuzamos monológok, ki nem mondott gondolatok (*szubtextus*).
- **Fő művek:** *Sirály*, *Három nővér*, *Cseresznyéskert*.
- **Alaptéma:** Az orosz nemesség és értelmiség lecsúszása, életképtelensége és céltalan vágyakozása.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** A klasszikus konfliktusos dráma felbomlása a 19. század végén.
2. **Ibsen analitikája (1 perc):** A múlt feltárása mint konfliktusforrás a *Nóra* példáján keresztül.
3. **Csehov atmoszférateremtése (1 perc):** A cselekvésképtelenség és a párhuzamos monológok technikája.
4. **Befejezés (30 mp):** A modern színjátszásra gyakorolt alapvető hatás összehasonlítása.
        """,
        "kviz": [
            {"k": "Ibsen darabjaiban a drámai robbanást a múltban történt titkok kiderülése idézi elő.", "v": True, "m": "Ez az analitikus dramaturgia lényege."},
            {"k": "Nóra a darab végén megalkuszik férjével és otthon marad.", "v": False, "m": "Nóra elhagyja férjét és gyermekeit, hogy önálló emberré válhasson."},
            {"k": "Csehov színműveire a pergő párbeszédek és folyamatos kardcsaták jellemzőek.", "v": False, "m": "A passzivitás, elvágyódás és a hangulati elemek uralják műveit."}
        ]
    },
    "7. A Nyugat folyóirat": {
        "alcim": "A modern magyar irodalom zászlóbontása, nemzedékek és hatások",
        "kulcsszavak": ["1908", "Osvát Ernő", "Ignotus", "Mikes-emlékérem", "Három nemzedék"],
        "audio_szoveg": """
A huszadik századi magyar kultúra legfontosabb szellemi műhelye a Nyugat folyóirat volt, amely 1908. január elsején indult útjára és Babits Mihály 1941-es haláláig létezett. A lap emblémája Beck Ödön Fülöp Mikes Kelemen-emlékérme lett, amely a hűséget és a művészi elhivatottságot szimbolizálta. 
A lap célja a magyar irodalom felzárkóztatása volt a fejlett nyugat-európai művészeti szintre, megteremtve a teljes esztétikai függetlenséget. A szerkesztőség meghatározó alakja Ignotus főszerkesztő és a zseniális ízlésű szerkesztő, Osvát Ernő volt. 
A folyóirat három egymást követő nemzedék tehetségeit tömörítette. Az első nagy generációhoz tartozott Ady Endre, Babits Mihály, Kosztolányi Dezső és Móricz Zsigmond. A második nemzedéket Szabó Lőrinc és Illyés Gyula fémjelezte, míg a harmadik hullámban tűnt fel Radnóti Miklós, Weöres Sándor és Szerb Antal.
        """,
        "vazlat": """
### 1. A folyóirat indulása és céljai
- **Kezdet:** 1908. január 1. – 1941 (Babits halála).
- **Eszmény:** Európaiság, művészi szabadság (*l'art pour l'art*), szakítás a konzervatív akadémizmussal.
- **Vezetői:** Ignotus (főszerkesztő), Osvát Ernő (irodalmi válogató zseni), Hatvany Lajos (mecénás).

### 2. A Nyugat három nagy nemzedéke
- **1. nemzedék:** Ady Endre, Babits Mihály, Kosztolányi Dezső, Móricz Zsigmond, Tóth Árpád, Juhász Gyula, Kaffka Margit.
- **2. nemzedék (1920-as évek):** Szabó Lőrinc, Illyés Gyula, Németh László, Márai Sándor.
- **3. nemzedék (1930-as évek):** Radnóti Miklós, Weöres Sándor, Vas István, Szerb Antal.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** 1908 mint korszakhatár a magyar kultúrában, a lap indulása.
2. **Szerkesztőségi műhelymunka (1 perc):** Osvát Ernő ízlésformáló szigora és az esztétikai autonómia megteremtése.
3. **A nemzedékek íve (1 perc):** Az 1. nemzedék stílusforradalma és a későbbi nemzedékek beilleszkedése.
4. **Befejezés (30 mp):** A Nyugat kánonképző szerepe a mai magyar műveltségben.
        """,
        "kviz": [
            {"k": "A Nyugat folyóirat címoldalán a Mikes Kelemen-emlékérem szerepelt.", "v": True, "m": "Beck Ödön Fülöp alkotása a bujdosó hűség jelképe."},
            {"k": "A Nyugat folyóirat 1908 és 1941 között működött.", "v": True, "m": "Babits Mihály 1941-es halálával szűnt meg a folyóirat."},
            {"k": "Radnóti Miklós a Nyugat első nemzedékének tagja volt.", "v": False, "m": "Radnóti a harmadik nemzedékhez tartozott."}
        ]
    },
    "8. Ady Endre költészete": {
        "alcim": "Szimbolizmus, magyarságtudat, lírai párharc és háborús apokalipszis",
        "kulcsszavak": ["Új versek 1906", "A magyar Ugaron", "Léda vs. Csinszka", "Harc a Nagyúrral"],
        "audio_szoveg": """
Ady Endre 1906-ban megjelent Új versek című kötetével gyökeresen megújította a magyar költészet nyelvét és szemléletét. Művészetének gerincét a modern szimbolizmus alkotja: egyéni, többrétegű szimbólumrendszert épített fel, amelyben az Ugar, a Bakony, a Hortobágy és a Pénz mitikus jelentést kapnak. 
Költészete több nagy tematikus pillérre támaszkodik. Magyarság-verseiben, mint A magyar Ugaron című szonettben, a nemzeti elmaradottságot és a kultúra pusztulását fájlalja ostorozó hazaszeretettel. Pénz-verseiben a Disznófejű Nagyúrral vív megalázó harcot az alkotói létért és szabadságért. Szerelmi lírája kettős arculatú: a Léda-verseket a gyötrelmes párharc és a pusztulásvágy uralja, míg a Boncza Bertával kötött házassága alatt a Csinszka-versek a menedéket és védelmet jelentik a világháború tombolása idején.
        """,
        "vazlat": """
### 1. Az 1906-os költői forradalom
- *Új versek:* Új költői szerep, provokatív magatartás, kötetkompozíciós tudatosság.
- **Ars poetica:** *Góg és Magóg fia vagyok én...*, *Új vizeken járok* (hagyomány és modernitás feszültsége).

### 2. Főbb tematikus vonulatok
- **A magyarság toposzai:** *A magyar Ugaron*, *A Tisza-parton* (az elmaradott, parlagon heverő táj mint a szellemi pusztulás metaforája).
- **A létharc és pénz:** *Harc a Nagyúrral* (a disznófejű bálvány és az emberi méltóság).
- **A szerelmi líra kettőssége:**
  - *Léda-szerelem:* Diszharmonikus küzdelem, halálhangulat (*Héja-nász az avaron*, *Elbocsátó, szép üzenet*).
  - *Csinszka-szerelem:* Békés menedék és biztonságkeresés (*Őrizem a szemed*).
- **Háborús látomások:** *Ember az embertelenségben*, *Emlékezés egy nyár-éjszakára*.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** 1906: az *Új versek* robbanásszerű hatása és a szimbolizmus térhódítása.
2. **Magyarság és egzisztencia (1 perc):** Az Ugar sár-motívuma és a disznófejű Nagyúr elleni küzdelem.
3. **A szerelmi líra pólusai (1 perc):** A Léda-féle pusztító héjanász és a Csinszka-féle menedéklíra ellentéte.
4. **Befejezés (30 mp):** A háborús költészet humánuma (*Ember az embertelenségben*).
        """,
        "kviz": [
            {"k": "Ady Endre korszakalkotó kötete az Új versek 1906-ban látott napvilágot.", "v": True, "m": "Ez a mű nyitotta meg a modern magyar líra korszakát."},
            {"k": "A Harc a Nagyúrral költeményben a Nagyúr a nemzeti dicsőséget jelképezi.", "v": False, "m": "A sertésfejű Nagyúr a pénz és az anyagi kiszolgáltatottság kegyetlen bálványa."},
            {"k": "A Héja-nász az avaron című vers a Léda-korszak diszharmonikus szerelmét ábrázolja.", "v": True, "m": "A ragadozó madarak násza a halálba zuhanó szerelmet mintázza."}
        ]
    },
    "9. Babits Mihály: Jónás könyve": {
        "alcim": "A prófétai szerep, a morális felelősségvállalás és a Jónás imája",
        "kulcsszavak": ["Jónás könyve", "Jónás imája", "Ninive", "Cinkos, aki néma", "1938"],
        "audio_szoveg": """
Babits Mihály életművének összefoglaló csúcsa az 1938-ban megjelent Jónás könyve és annak lírai függeléke, a Jónás imája. A mű keletkezésekor a költő a gégeműtétje után a halálos kórral küzdött, miközben Európában feltartóztathatatlanul terjedt a fasizmus fenyegetése. 
A mű egy ószövetségi parafrázis, ám Babits a prófétát emberi esendőségekkel ruházza fel. Jónás el akar menekülni az elhívás elől, kényelmes életre vágyik, ám a cethal gyomrában megtisztulva belátja, hogy nem bújhat ki a kötelessége alól. Elmegy a bűnös Ninivébe, hogy hirdesse az igét. A mű legfontosabb etikai imperatívusza így szól: mert vétkesek közt cinkos, aki néma. 
A záró Jónás imája alázatos fohász a tiszta, halálig kitartó költői beszédért.
        """,
        "vazlat": """
### 1. A mű keletkezése és lélektana
- 1938: Babits gégerákja (beszélőfüzetek) és a totalitárius eszmék árnyéka.
- Műfaj: Epikus költemény, bibliai parafrázis öniróniával és groteszk elemekkel.

### 2. A négy rész szerkezeti dinamikája
- **1. rész:** A menekülés és a cethal gyomra (a prófétai sors elkerülhetetlensége).
- **2. rész:** Bűnbánat és ima a hal gyomrában (megtisztulás).
- **3. rész:** Ninive bűnei és kigúnyolt próféciája (az igazság kimondása).
- **4. rész:** A tök növekedése és elszáradása – az Úr tanítása a kegyelemről és a világ fenntartásáról.

### 3. Jónás imája (1939)
- Lírai ars poetica: Alázat a sors és az alkotói küldetés előtt a halál árnyékában.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** 1938 sorsfordító éve, a prófétaszerep megújítása Babits kései korszakában.
2. **Jónás emberi portréja (1 perc):** A feladat elől menekülő kisember groteszk vonásai és a cethal általi beavatás.
3. **Ninive és az etikai imperatívusz (1 perc):** A némák bűnrészessége és az isteni irgalom összefüggése.
4. **Befejezés (30 mp):** A *Jónás imája* mint a halállal szembenéző tiszta költészet vallomása.
        """,
        "kviz": [
            {"k": "A Jónás könyve 1938-ban született Babits súlyos betegsége idején.", "v": True, "m": "A gégeműtétje után írta a fasizmus árnyékában."},
            {"k": "A 'Mert vétkesek közt cinkos, aki néma' gondolat a Jónás könyvében hangzik el.", "v": True, "m": "Az értelmiségi felelősségvállalás legfontosabb etikai parancsa."},
            {"k": "Az Úr végül azonnal elpusztítja Ninivét Jónás követelésére.", "v": False, "m": "Az Úr megkegyelmez Ninivének, megmutatva a teremtés fenntartásának fontosságát."}
        ]
    },
    "10. Móricz Zsigmond prózája": {
        "alcim": "A paraszti világ és dzsentri réteg naturalista és kritikai ábrázolása",
        "kulcsszavak": ["Naturalizmus", "Tragédia", "Barbárok", "Úri muri", "Szakhmáry Zoltán"],
        "audio_szoveg": """
Móricz Zsigmond a magyar kritikai realizmus és naturalizmus legnagyobb elbeszélője. Művészete gyökeres szakítást jelentett a 19. századi idillikus, népieskedő parasztábrázolással. A magyar valóságot a maga kíméletlen, biológiai és társadalmi meztelenségében mutatta be. 
Az 1909-es Tragédia című novellájában Kis János zsellér alakján keresztül a biológiai ösztönökbe és nyomorba szorult ember sorsát ábrázolja, akinek egyetlen lázadása a gazda lakodalmán való mértéktelen evésbe torkollik. Az 1931-es Barbárok balladisztikus tömörséggel mutatja be a pusztai pásztorok nyers, civilizációtól elzárt ösztönvilágát és a kapzsiságból elkövetett gyilkosságot. 
Későbbi nagyregényében, az Úri muriban a magyar dzsentri pusztulásra ítélt világát vizsgálja Szakhmáry Zoltán önsorsrontó mulatozásán keresztül.
        """,
        "vazlat": """
### 1. A realista-naturalista stílusreform
- Szakítás a népszínművek hamis idilljével; ösztönök, éhség, kapzsiság, társadalmi determináció.

### 2. Novellisztika
- **Tragédia (1909):** Kis János karaktere; az ember mint biológiai lény; az evés abszurd bosszúja és a zsíros húsba való belefulladás.
- **Barbárok (1931):** Háromrészes balladisztikus szerkezet; Bodri juhász meggyilkolása a rézkilincses szíjért; a civilizálatlan pusztai ösztönvilág.

### 3. A dzsentri társadalmi csődje
- **Úri muri (1928):** Szakhmáry Zoltán alakja; tenni akarás vs. a talajvesztett nemesi osztály dorbézolása és önpusztítása.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** Móricz fellépése a Nyugatban és a hamis népiesség felszámolása.
2. **A szegénység ösztönei (1 perc):** *Tragédia* (Kis János) és a *Barbárok* naturalista lélektana.
3. **A nemesség válsága (1 perc):** Az *Úri muri* dorbézolása és Szakhmáry Zoltán bukása.
4. **Befejezés (30 mp):** A kritikai realizmus máig ható tanulságai.
        """,
        "kviz": [
            {"k": "A Tragédia című novellában Kis János a túlzott evés miatt fullad meg.", "v": True, "m": "A nyomorban élő zsellér egyetlen groteszk lázadása az evés volt."},
            {"k": "A Barbárok című novellában Bodri juhászt rézkilincses szíjáért ölik meg a veres juhászok.", "v": True, "m": "Az értelmetlen pusztai kapzsiság balladisztikus példája."},
            {"k": "Szakhmáry Zoltán az Úri muriban a sikeres, modern mintagazdaság megalapítója.", "v": False, "m": "Szakhmáry belebukik tehetetlenségébe és felgyújtja saját birtokát."}
        ]
    },
    "11. Kosztolányi Dezső: Édes Anna": {
        "alcim": "A lélektani regény, a megalázottság tudattalan robbanása és a humanizmus",
        "kulcsszavak": ["Édes Anna", "Vizy család", "Moviszter doktor", "1919", "Freudizmus"],
        "audio_szoveg": """
Kosztolányi Dezső 1926-ban megjelent Édes Anna című regénye a magyar lélektani próza remekműve. A történet történelmi kerete pontos: 1919 nyarán, a Tanácsköztársaság bukása és a román megszállás napjaiban indul Budapesten. 
A regény cselekménye a tiszta lelkű cselédlány, Édes Anna és a méltóságos Vizy család kapcsolatát mutatja be. Vizyné büszkén mintagépként kezeli Annát, teljesen megfosztva őt emberi személyiségétől. Amikor a ház úrfi rokona, Jancsi elcsábítja, majd terhesen magára hagyja, a hosszú ideje elfojtott sérelmek és megaláztatások a tudattalan mélyén felhalmozódnak. Egy éjszaka a feszültség ösztönös kettős gyilkosságban robban ki. 
A bírósági tárgyaláson egyedül a halálos beteg Moviszter doktor áll ki Anna mellett, képviselve a tiszta irgalmat és az emberi méltóság sérthetetlenségét.
        """,
        "vazlat": """
### 1. Történelmi keret és pszichoanalízis
- Kezdőpont: 1919. július 31. (Kun Béla elmenekülése Krisztinavárosból).
- Sigmund Freud lélektani hatása: a tudatalatti elfojtások felgyülemlése (*ösztön-én vs. felettes-én*).

### 2. A dehumanizálás folyamata
- **Anna tárgyiasítása:** Mintagép, aki nem eszik, nem alszik, tökéletesen takarít.
- **Vizyné karaktere:** Elvetélt anyaság, lelki sivárság, birtoklási vágy.
- **Jancsi úrfi árulása:** Felelőtlen csábítás és megalázó eldobás.
- **A bűntett:** Nem előre megfontolt gyilkosság, hanem a felgyűlt fojtogató feszültség ösztönös kitörése.

### 3. A regény etikai zárása
- **Moviszter doktor:** A keresztény humanizmus és részvét hangja a rideg bíróság előtt.
        """,
        "szobeli": """
**🎙️ 3 perces strukturált felelet:**
1. **Bevezetés (30 mp):** A freudi lélektan hatása és az 1919-es történelmi háttér jelentősége.
2. **Anna tárgyiasítása (1 perc):** A cselédsors mechanizálása és Vizyné rideg önzése.
3. **A gyilkosság lélektana (1 perc):** Miért nem hidegvérű gaztett a késelés, hanem pszichikai robbanás.
4. **Befejezés (30 mp):** Moviszter doktor humánuma mint Kosztolányi legfőbb üzenete.
        """,
        "kviz": [
            {"k": "Édes Anna a regény cselekménye szerint előre kitervelt politikai bosszúból gyilkol.", "v": False, "m": "Anna tette az elfojtott megaláztatások ösztönös, tudattalan robbanása."},
            {"k": "A regényben Moviszter doktor az egyetlen, aki emberi méltósággal és részvéttel tekint Annára.", "v": True, "m": "Moviszter képviseli az író humanista értékrendjét."},
            {"k": "A regény nyitójelenete Kun Béla repülőgépes elmenekülésének pletykájával indul 1919-ben.", "v": True, "m": "A Tanácsköztársaság bukása a történelmi díszlet."}
        ]
    }
}

stilusiranyzatok = {
    "Realizmus (19. sz. közepe)": """
- **Cél:** A társadalmi valóság tárgyilagos, hiteles ábrázolása.
- **Módszer:** Tipikus jellemek tipikus körülmények között.
- **Képviselők:** Mikszáth Kálmán, Lev Tolsztoj, Honoré de Balzac.
    """,
    "Naturalizmus (19. sz. vége)": """
- **Cél:** A valóság szépítés nélküli, nyers leírása.
- **Emberkép:** Az ember a biológiai ösztönök és öröklődés rabja.
- **Képviselők:** Émile Zola, Móricz Zsigmond (*Tragédia*, *Barbárok*).
    """,
    "Impresszionizmus (19. sz. vége – 20. sz. eleje)": """
- **Cél:** A múló pillanatok, hangulatok, fények megragadása.
- **Stílusjegyek:** Névszói stílus, erős zeneiség, finom asszociációk.
- **Képviselők:** Kosztolányi Dezső, Tóth Árpád, Juhász Gyula.
    """,
    "Szimbolizmus (19. sz. vége – 20. sz. eleje)": """
- **Cél:** A látható világ mögötti magasabb rendű valóság kifejezése többértelmű képekkel.
- **Stílusjegyek:** Rejtettség, titokzatosság, gazdag jelképrendszer.
- **Képviselők:** Baudelaire, Verlaine, Ady Endre, Vajda János.
    """
}

# Állapot inicializálása
if 'xp' not in st.session_state:
    st.session_state.xp = 180
if 'level' not in st.session_state:
    st.session_state.level = 2
if 'streak' not in st.session_state:
    st.session_state.streak = 4
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "text": "Szia! Én vagyok az érettségi mentorod. Kérdezz bátran bármelyik tételről, versről vagy szerzőről!"}
    ]

# Biztos és elcsúszásmentes szövegformázó a beépített PDF motorhoz
def tiszta_pdf_szoveg(szoveg):
    cserel = {
        'ő': 'o', 'Ő': 'O',
        'ű': 'u', 'Ű': 'U',
        'á': 'a', 'Á': 'A',
        'é': 'e', 'É': 'E',
        'í': 'i', 'Í': 'I',
        'ó': 'o', 'Ó': 'O',
        'ö': 'o', 'Ö': 'O',
        'ú': 'u', 'Ú': 'U',
        'ü': 'u', 'Ü': 'U',
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
    
    # Cím
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_x(15)
    pdf.cell(180, 8, 'Magyar Irodalom Erettsegi Tetelvazlatok', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    for cim, adat in tetelek_adat.items():
        # Tétel címe
        pdf.set_font('Helvetica', 'B', 10.5)
        pdf.set_x(15)
        fejlec = tiszta_pdf_szoveg(f"{cim} - {adat['alcim']}")
        pdf.multi_cell(180, 5.5, fejlec, align='L')
        pdf.ln(1)
        
        # Vázlat sorai
        pdf.set_font('Helvetica', '', 8.5)
        tiszta_vazlat = adat['vazlat'].replace('###', '').replace('**', '').replace('*', '')
        for sor in tiszta_vazlat.strip().split('\n'):
            sor_tiszta = tiszta_pdf_szoveg(sor.strip())
            if sor_tiszta:
                pdf.set_x(15)
                pdf.multi_cell(180, 4.2, sor_tiszta, align='L')
        pdf.ln(3)
        
    return bytes(pdf.output())

# Felső fejlécek & Gamifikáció
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title("✨ Edited by Nagy Attila")
    st.caption("Komplett Magyar Irodalom Érettségi Platform")
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
    ["📖 Tételek & Vázlatok", "🎧 Hangoskönyv (Monológ)", "🎨 Stílusirányzatok", "🏆 Nagy Próbavizsga", "🤖 AI Érettségi Mentor"]
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

# 1. Menüpont: Tételek, Vázlatok, Szóbeli és Kvíz
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
    
    tab1, tab2, tab3 = st.tabs(["📝 Részletes írásbeli vázlat", "🎙️ 3 perces szóbeli feleletvázlat", "⚡ Gyors teszt"])
    
    with tab1:
        st.markdown(adat["vazlat"])
        
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

# 2. Menüpont: Hangoskönyv (2 perces összefüggő tanári monológ)
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
        if st.button(f"▶️ Hangos összefoglaló elindítása ({kivalasztott_hangos})"):
            with st.spinner("Hangfájl előkészítése és generálása magyar nyelven..."):
                tts = gTTS(text=adat_hangos["audio_szoveg"].strip(), lang='hu', slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
                st.session_state.xp += 25
                st.success("Jó hallgatást! (+25 XP) 🎧")
                
    with st.expander("📖 A monológ szöveges változata (olvasáshoz és követéshez)", expanded=True):
        st.write(adat_hangos["audio_szoveg"].strip())

# 3. Menüpont: Stílusirányzatok
elif menupont == "🎨 Stílusirányzatok":
    st.title("Kulcs Stílusirányzatok")
    for nev, leiras in stilusiranyzatok.items():
        with st.expander(f"📌 {nev}", expanded=True):
            st.markdown(leiras)

# 4. Menüpont: Nagy Próbavizsga
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

# 5. Menüpont: AI Érettségi Mentor Chat
elif menupont == "🤖 AI Érettségi Mentor":
    st.title("🤖 AI Érettségi Mentor")
    st.caption("Kérdezz bármilyen irodalmi műről, versről vagy szerzőről!")

    api_key = st.text_input("🔑 Google Gemini API kulcs (opcionális az élő válaszokhoz):", type="password")

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
            
            if api_key:
                ai_valasz = None
                try:
                    client = genai.Client(api_key=api_key.strip())
                    prompt = f"Magyar irodalom szakos érettségi felkészítő tanár vagy. Válaszolj tömören, lényegretörően egy 18 éves diák kérdésére: {felh_kerdes}"
                    
                    cel_modellek = []
                    try:
                        for m in client.models.list():
                            if "flash" in m.name.lower() or "gemini" in m.name.lower():
                                cel_modellek.append(m.name.replace("models/", ""))
                    except Exception:
                        pass
                        
                    if not cel_modellek:
                        cel_modellek = ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
                        
                    for model_nev in cel_modellek:
                        try:
                            response = client.models.generate_content(
                                model=model_nev,
                                contents=prompt
                            )
                            if response and response.text:
                                ai_valasz = response.text
                                break
                        except Exception:
                            continue
                            
                    if not ai_valasz:
                        ai_valasz = "Nem sikerült választ kapni az AI modelltől. Kérlek ellenőrizd az API kulcsodat!"
                except Exception as e:
                    ai_valasz = f"Hiba az API hívás közben: {e}"
            else:
                k_kis = felh_kerdes.lower()
                if "anna" in k_kis or "gyilkosság" in k_kis:
                    ai_valasz = "Édes Anna tette nem előre eltervezett bűntény, hanem a hosszú ideje tartó megalázás és tárgyiasítás ösztönös, tudattalan robbanása. Moviszter doktor képviseli az empátia hangját."
                elif "montblanc" in k_kis or "vajda" in k_kis:
                    ai_valasz = "A Montblanc-hasonlat Vajda 'Húsz év múlva' című versében a megközelíthetetlen, kívülről hidegnek tűnő, de mélyén izzó szerelmet ábrázolja."
                elif "senki" in k_kis or "arany ember" in k_kis:
                    ai_valasz = "A Senki szigete Az arany emberben egy pénzmentes, romantikus utópia, ahol Timár Mihály a természet közvetlen közelében valódi békére lel Noémivel."
                else:
                    ai_valasz = "Nagyszerű kérdés! Az érettségin érdemes ezt a kortörténeti háttérrel, a szerző művészi szándékával és a formai jegyekkel alátámasztani."
                    
            st.session_state.chat_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 10
            st.rerun()
