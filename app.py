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
- **A három műnem találkozása:**
  - *Lírai vonások:* Dalforma, rím- és ritmusképlet, erős atmoszféra, szubjektív hangulati töltet.
  - *Epikai vonások:* Cselekményvonal, kibontakozó eseménysor, elbeszélői hang.
  - *Drámai vonások:* Éles sorsfordulók, kiélezett konfliktusok, dialógusos forma, tragikus végkifejlet.
- **Formanyelvi sajátosságok:**
  - **Balladai homály:** Az elbeszélő elhallgat összefüggéseket; az olvasó gondolati társítására (*asszociációjára*) épít.
  - **Ellipszis (kihagyás):** A fordulópontok közötti átvezetések hiánya fokozza a drámaiságot.
  - **Refrén:** Szerkezeti tartóoszlop, mely folyamatosan modulálja a hangulatot (*„Kocog a szekér...”* vagy *„Árva fejem...”*).

---

### II. A nagykőrösi korszak (1850-es évek) – Történelmi és lélektani szintézis

#### 1. Történelmi-allegorikus balladák (Nemzeti ellenállás a Bach-rendszerben)
- **A walesi bárdok (1857):**
  - *Kontextus:* Ferenc József 1857-es magyarországi látogatása. Arany visszautasította az üdvözlő vers megírását.
  - *Mondai keret:* I. Edward király és Montgomery vára.
  - *Üzenet:* Az 500 walesi bárd máglyahalála a magyar értelmiség morális kötelességét hirdeti: a zsarnokot tilos dicsőíteni; a költő feladata az igazság megőrzése a halál árnyékában is.
- **Szondi két apródja (1856):**
  - *Szerkezet:* Párhuzamos, kétszólamú szerkesztés (Drégely romjai vs. Ali pasa dőzsölő sátra).
  - *Konfliktus:* A török küldönc csábító szavai (*hírnév, vagyon, pompa*) állnak szemben az apródok hűséges, Szondi hősies küzdelmét zengő énekével.
  - *Mondandó:* A fizikai vereség dacára a morális győzelem a nemzeté marad.

#### 2. Lélektani balladák (A lelkiismeret drámája)
- **Ágnes asszony (1853):**
  - *Téma:* A bűnrészesség és a lélektani téboly folyamata.
  - *Központi szimbólum:* A patakban mosott véres lepedő – a bűn fizikai tisztítása mint a lelkiismeret tisztára mosásának kudarca.
  - *Szerkezeti hármasság:* 1–4. strófa: helyszín és tett (patak); 5–19. strófa: bírósági tárgyalás (a megbomló elme); 20–26. strófa: a megvénült Ágnes végtelen, céltalan mosása.
  - *Refrén:* *„Könyörülj, Jézus, a sok szegény bűnösön!”* – részvét és ima a bűnbeesett emberért.
- **Tetemre hívás (1877-hez közel / népi hagyomány):** Bárczi Benő meggyilkolása; a középkori istenítélet toposza.

---

### III. Az Őszikék korszaka (1877, Margitsziget, Kapcsos könyv)
- **Korszakjellemzők:** Időskori rezignáció, testi fájdalmak, az urbanizáció és modern polgári társadalom árnyoldalai.
- **Híd-avatás (1877):**
  - *Téma:* A Margit híd avatásához kötődő babona (öngyilkosok ugrása a folyóba).
  - *Műfaji elem:* Modern haláltánc (*danse macabre*).
  - *Társadalomkép:* A kártyavesztett nemes, a megcsalt lány, a csődbe ment alkusz, a reménytelen diák – az elidegenedett modernitás áldozatainak felvonulása.
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat (Vizsgastratégia):**

1. **Bevezetés (kb. 40 mp):** Greguss Ágost meghatározása (*„Tragédia dalban elbeszélve”*), 3 műnem találkozása, formai eszközök (balladai homály, ellipszis, sűrítés).
2. **Tárgyalás I. – Nagykőrösi történelmi és lélektani balladák (kb. 70 mp):** Bach-korszak ellenállása (*A walesi bárdok*, *Szondi két apródja* kétszólamúsága); *Ágnes asszony* bűntudat-lélektana (a lepedőmosás szimbóluma).
3. **Tárgyalás II. – Az Őszikék korszaka (kb. 40 mp):** 1877, Margitsziget, Kapcsos könyv. A *Híd-avatás* modern nagyvárosi haláltánca.
4. **Befejezés (kb. 30 mp):** A klasszikus magyar ballada nyelvi és formai csúcspontjának értékelése.
        """,
        "kviz": [
            {"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A meghatározás a líra, epika és dráma ötvözésére utal."},
            {"k": "A walesi bárdok nyíltan, burkolás nélkül támadta Ferenc Józsefet.", "v": False, "m": "Allegorikus formában, a walesi monda köntösében fogalmazta meg az ellenállást."},
            {"k": "Az Ágnes asszony lepedőmosása a bűn letörölhetetlenségének lélektani szimbóluma.", "v": True, "m": "A tisztaság kényszeres keresése a lelkiismeret megbomlását mutatja be."},
            {"k": "A Szondi két apródja Drégely várának ostromát idézi fel párhuzamos szólamokkal.", "v": True, "m": "A török küldönc és az apródok éneke éles kontrasztban áll."},
            {"k": "A Híd-avatás című ballada az Őszikék korszakban, a Margitszigeten íródott.", "v": True, "m": "1877-ben került be a híres Kapcsos könyvbe."}
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
### I. A mű keletkezéstörténete és stílusszintézise
- **Keletkezés:** 1872 – a kiegyezést követő magyar kapitalizálódás időszaka.
- **Romantikus elemek:** Mesés véletlenek (a süllyedő Szent Borbála búzaszállítmánya, a kincs, Krisztyán Tódor halála), a Senki szigete természeti idillje.
- **Realista elemek:** Pontos gazdasági és pénzügyi folyamatok (búzakereskedelem, spekuláció, csődeljárás); modern lélektani jellemábrázolás.

---

### II. Timár Mihály belső hasadtsága
- **A név paradoxona:** „Arany ember” – a külvilág szemében sikeres nagypolgár, önmaga szemében tolvaj és álszent csábító.
- **Morális bűnbeesése:** Megtartja Ali Csorbadzsi kincsét, tönkreteszi Brazovicsot, és feleségül veszi a hálás Timeát.
- **A boldogtalanság oka:** A pénzen minden megvehető, csak a valódi szívbéli szeretet nem.

---

### III. Kettős térszerkezet és nőalakok

| Polgári világ (Komárom, Bécs) | Természeti utópia (Senki szigete) |
| :--- | :--- |
| **Képviselője:** Timea | **Képviselője:** Noémi és Teréza mama |
| **Jellemzők:** Pénz, rang, konvenciók, hideg pompa. | **Jellemzők:** Pénzmentesség, tiszta munka, erkölcs. |
| **Érzelmi viszony:** Szoborszerű tisztelet és hála; hidegség. | **Érzelmi viszony:** Ösztönös, odaadó, tiszta szerelem. |
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** 1872, Jókai legszemélyesebb műve; romantika és realizmus találkozása.
2. **Timár jelleme (1 perc):** Anyagi felemelkedés vs. morális meghasonlás (a török kincs terhe).
3. **A két világmodell (1 perc):** Komárom és Timea ridegsége vs. Senki szigete és Noémi utópiája.
4. **Befejezés (30 mp):** A Balaton jegén bekövetkező sorsfordulat és a társadalomból való kilépés.
        """,
        "kviz": [
            {"k": "Timea szerelemből házasodott össze Timárral.", "v": False, "m": "Timea hálából ment hozzá, szívében Kacsukát szerette."},
            {"k": "A Senki szigete pénz- és adómentes, önellátó természeti menedék a regényben.", "v": True, "m": "A társadalmi törvényeken kívül álló romantikus édenkert."},
            {"k": "Krisztyán Tódor a Balaton jegének rianásába zuhanva leli halálát Timár ruhájában.", "v": True, "m": "Így Timár eltűnhet a civilizáció elől és Noémivel élhet."}
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
### I. Műfaji sajátosságok és filozófiai gyökerek
- **Műfaj:** Drámai költemény (világdráma, könyvdráma) – filozófiai kérdések dialógusos formában.
- **Hegeli dialektika:** Tézis (új eszme) $\rightarrow$ Antitézis (elfajulás, csalódás) $\rightarrow$ Szintézis (új korszak).

---

### II. A három archetípus
- **Ádám:** Az örök küzdő emberi szellem, a hit, az eszmék keresője.
- **Lucifer:** A hideg ráció, a kétely és tagadás szelleme.
- **Éva:** A természet, az érzelmek, a költészet és az élet folytonossága.

---

### III. Történelmi színek (4–14. szín)
- Egyiptom (szabadság), Athén (demokrácia), Róma (hedonizmus), Bizánc (vallás), Prága (tudomány), Párizs (forradalom – *nem csalódik!*), London (szabadpiaci kapitalizmus – *haláltánc*), Falanszter (mechanikus tudomány), Űr (anyagtalanodás), Eszkimó szín (kihűlő világ).
- **15. szín:** Az Úr zárszava: *„Mondottam, ember: küzdj és bízva bízzál!”*
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** A drámai költemény műfaja, 1859–60 nemzeti válsága.
2. **Karakterek hármassága (1 perc):** Ádám (hit és tettvágy), Lucifer (ráció és tagadás), Éva (természetesség és anyaság).
3. **Történelmi színek (1 perc):** Eszmék felívelése és bukása; Párizs (Danton) és London (haláltánc) kontrasztja.
4. **Befejezés (30 mp):** A 15. szín feloldása és az Úr etikai parancsa.
        """,
        "kviz": [
            {"k": "Az ember tragédiája 15 színből áll.", "v": True, "m": "4 keretszín és 11 történelmi szín alkotja."},
            {"k": "Ádám a párizsi színből kiábrándultan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel és elszántsággal tér magához."},
            {"k": "A londoni szín végén a szereplők haláltánc kíséretében ugranak a sírba.", "v": True, "m": "A kapitalista piac zűrzavarának allegorikus lezárása."}
        ]
    }
}

# Flashcard adatbázis az érettségi kulcsfogalmakhoz
flashcards_adat = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra (dalforma, rím), epika (cselekmény) és dráma (konfliktus, dialógus) műnemi sajátosságait."},
    {"q": "Mi a balladai homály és az ellipszis lényege?", "a": "Az elbeszélő szándékosan kihagy részleteket és összefüggéseket, ezáltal feszültséget teremt és a befogadó képzeletére bízza a történet kiegészítését."},
    {"q": "Melyik történelmi esemény ihlette Arany 'A walesi bárdok' című balladáját?", "a": "Ferenc József 1857-es magyarországi látogatása. Arany a költői meg nem alkuvás és a zsarnokellenes hűség példájaként írta meg."},
    {"q": "Mit szimbolizál az Ágnes asszonyban a véres lepedő kényszeres mosása?", "a": "A bűn letörölhetetlenségét és a lelkiismeret-furdalás által kiváltott elmezavart."},
    {"q": "Mi a kettős világmodell 'Az arany ember' című regényben?", "a": "Komárom/Bécs (a pénz, a spekuláció és a rideg polgári társadalom világa Timeával) vs. Senki szigete (a pénzmentes, romlatlan természeti utópia Noémivel)."},
    {"q": "Miért különleges a párizsi szín 'Az ember tragédiájában'?", "a": "Ez az egyetlen olyan történelmi szín, amelyből Ádám nem csalódottan és kiábrándultan, hanem hittel és cselekvési vággyal ébred fel."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a legfontosabb irodalmi szerkesztője?", "a": "1908. január 1-jén indult, és Osvát Ernő volt a lap legendás ízlésű irodalmi szerkesztője."},
    {"q": "Mit jelképez a disznófejű Nagyúr Ady Endre költészetében?", "a": "A pénz, az anyagi kiszolgáltatottság és az emberi méltóságot elnyomó tőke kegyetlen bálványát."},
    {"q": "Mi a központi szállóige és tanulság Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.” – Az értelmiségi ember és a művész morális felelősségvállalása a gonosszal szemben."},
    {"q": "Ki képviseli a tiszta humanizmus hangját Kosztolányi 'Édes Anna' című regényében?", "a": "Moviszter doktor, aki egyedüliként tekinti Annát emberi lénynek és szólal fel mellette a bíróság előtt."}
]

stilusiranyzatok = {
    "Realizmus (19. sz. közepe)": """
### Realizmus (19. század dereka)
- **Központi esztétikai cél:** A valóság sallangmentes, tárgyilagos, hiteles és tipikus ábrázolása.
- **Módszertan:**
  - *Tipikus jellemek tipikus körülmények között:* A főhősök a társadalmi rétegük hű képviselői.
  - *Társadalmi determináció:* Az egyén sorsát a környezet és az anyagi helyzet határozza meg.
- **Képviselők:** Honoré de Balzac, Lev Tolsztoj, Mikszáth Kálmán, Jókai Mór.
    """,
    "Naturalizmus (19. sz. vége)": """
### Naturalizmus (19. század vége)
- **Központi esztétikai cél:** A valóság fotószerű, kíméletlen rögzítése, tabutémák (ösztönök, betegség, nyomor) beemelése.
- **Módszertan:** Biológiai determinizmus – az ember az ösztönök és gének rabja.
- **Képviselők:** Émile Zola, Móricz Zsigmond (*Tragédia*, *Barbárok*).
    """,
    "Impresszionizmus (19. sz. vége – 20. sz. eleje)": """
### Impresszionizmus (19–20. század fordulója)
- **Központi esztétikai cél:** A pillanatnyi benyomások, hangulatok és fények megragadása.
- **Stílusjegyek:** Névszói stílus, zeneiség, szinesztézia (*„lila dalra kelt az éjcsend”*).
- **Képviselők:** Kosztolányi Dezső, Tóth Árpád, Juhász Gyula.
    """,
    "Szimbolizmus (19. sz. vége – 20. sz. eleje)": """
### Szimbolizmus (19–20. század fordulója)
- **Központi esztétikai cél:** A látható világ mögötti transzcendens igazságok kifejezése többértelmű szimbólumokkal.
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

# Oldalsáv navigáció (Bővítve az új Astra funkciókkal)
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
    st.caption("Gyakorold a szóbeli feleletet! Az AI vizsgaelnökként meghallgat, belekérdez és leosztályoz.")
    
    api_key_oral = st.text_input("🔑 Google Gemini API kulcs a szimulációhoz:", type="password", key="oral_key")
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
            if api_key_oral:
                try:
                    client = genai.Client(api_key=api_key_oral.strip())
                    prompt = f"""
                    Magyar irodalom szóbeli érettségi elnök vagy. A diák a(z) '{valasztott_szim_tetel}' tételből felel.
                    A diák eddigi felelete: '{felelet_reszlet}'.
                    Feladatod:
                    1. Röviden értékeld az elmondottakat (pontosság, fogalmak).
                    2. Tegyél fel egy célzott, érettségi szintű kérdést a tétel egy másik fontos részletére vonatkozóan, vagy ha a felelet lezárult, adj egy konkrét érdemjegyet (1-5) és részletes vizsgaértékelést.
                    Legyél támogató, de szakmailag szigorú tanár!
                    """
                    
                    cel_modellek = ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
                    ai_valasz = None
                    for m in cel_modellek:
                        try:
                            res = client.models.generate_content(model=m, contents=prompt)
                            if res and res.text:
                                ai_valasz = res.text
                                break
                        except:
                            continue
                    if not ai_valasz:
                        ai_valasz = "Nagyon jó gondolatok! Kérem, térjen ki részletesebben a konkrét művek elemzésére is!"
                except Exception as e:
                    ai_valasz = f"Hiba az API hívásban: {e}"
            else:
                ai_valasz = "Köszönöm! Hallgassuk meg a művek részletes elemzését is: említsen konkrét motívumokat és szereplőket!"
                
            st.session_state.oral_history.append({"role": "ai", "text": ai_valasz})
            st.session_state.xp += 30
            st.rerun()

# 4. Menüpont: Esszé & Elemzés Értékelő
elif menupont == "✍️ Esszé & Elemzés Értékelő":
    st.title("✍️ Esszé & Műelemzés Értékelő Labor")
    st.caption("Másold be az írásbeli fogalmazásodat vagy verselemzés-tervezetedet, és az AI pontozza az érettségi szempontrendszer szerint!")
    
    api_key_essay = st.text_input("🔑 Google Gemini API kulcs az értékeléshez:", type="password", key="essay_key")
    diak_essze = st.text_area("Másold be a fogalmazásodat (műelemzés, összehasonlító elemzés vagy esszé):", height=220)
    
    if st.button("📊 Esszé ellenőrzése és pontozása"):
        if diak_essze:
            if api_key_essay:
                with st.spinner("Az esszé elemzése érettségi szempontok alapján..."):
                    try:
                        client = genai.Client(api_key=api_key_essay.strip())
                        prompt = f"""
                        Magyar nyelv és irodalom érettségi javító tanár vagy. Értékeld az alábbi diákfogalmazást:
                        ---
                        {diak_essze}
                        ---
                        Kérlek, az alábbi szempontok szerint strukturáld az értékelést:
                        1. **Tartalmi minőség & Szakmai pontosság (max 40 pont):** Irodalomtörténeti tények, fogalmak használata.
                        2. **Szerkezet & Logikai felépítés (max 20 pont):** Bevezetés, tárgyalás, befejezés, bekezdések.
                        3. **Nyelvhelyesség & Stílus (max 20 pont):** Szókincs, megfogalmazás.
                        4. **Összesített érettségi pontszám & Érdemjegy (1-5)**
                        5. **Konkrét javítási javaslatok:** 2-3 pontban, mit kell hozzátenni a tökéletes felelethez.
                        """
                        res = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                        st.markdown("<div class='deep-text'>", unsafe_allow_html=True)
                        st.markdown(res.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.session_state.xp += 50
                    except Exception as e:
                        st.error(f"Hiba történt: {e}")
            else:
                st.warning("Kérlek írd be a Gemini API kulcsodat az élő AI javításhoz!")
        else:
            st.info("Kérlek előbb másold be a fogalmazás szövegét!")

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
