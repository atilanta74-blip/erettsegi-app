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

# Sötét téma és prémium stílusok
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
- **Tetemre hívás (1877-hez közel / népi hagyomány):**
  - Bárczi Benő meggyilkolása; a középkori istenítélet toposza. Kund Abigél kacaja a bűn lelepleződésének pillanatában.

---

### III. Az Őszikék korszaka (1877, Margitsziget, Kapcsos könyv)
- **Korszakjellemzők:** Időskori rezignáció, testi fájdalmak, az urbanizáció és modern polgári társadalom árnyoldalai.
- **Híd-avatás (1877):**
  - *Téma:* A Margit híd avatásához kötődő babona (öngyilkosok ugrása a folyóba).
  - *Műfaji elem:* Modern haláltánc (*danse macabre*).
  - *Társadalomkép:* A kártyavesztett nemes, a megcsalt lány, a csődbe ment alkusz, a reménytelen szegény diák – az elidegenedett modernitás áldozatainak felvonulása.
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat (Vizsgastratégia):**

1. **Bevezetés (kb. 40 másodperc):**
   * Határozd meg a ballada műfaját Greguss Ágost híres formulájával (*„Tragédia dalban elbeszélve”*).
   * Emeld ki a három műnem (líra, epika, dráma) egybefonódását és a legfontosabb formanyelvi eszközöket (balladai homály, kihagyás/ellipszis, sűrítés, refrén).

2. **Tárgyalás I. – Nagykőrösi történelmi és lélektani balladák (kb. 70 másodperc):**
   * *Történelmi vonal:* Említsd meg a Bach-korszak politikai válságát. Elemezd *A walesi bárdok* zsarnokellenes magatartását és a *Szondi két apródja* kétszólamú, hűséget hirdető felépítését.
   * *Lélektani vonal:* Részletezd az *Ágnes asszony* belső drámáját! Hangsúlyozd a lepedőmosás motívumát: a fizikai tisztogatás nem képes eltörölni a lelkiismeret-furdalást, ami végül elmezavarhoz vezet.

3. **Tárgyalás II. – Az Őszikék korszaka (kb. 40 másodperc):**
   * Ismertesd az 1877-es margitszigeti alkotói periódust és a Kapcsos könyv jelentőségét.
   * Elemezd a *Híd-avatás* modern nagyvárosi haláltáncát, ahol a modern kapitalista világ céltalansága sodorja végzetbe a különböző társadalmi rétegeket.

4. **Befejezés és összegzés (kb. 30 másodperc):**
   * Zárd a gondolatmenetet azzal, hogy Arany János a népköltészeti alapokból világirodalmi rangra emelte a magyar balladát, és formaművészetével felkészítette a modern költészetet a 20. századi lélekábrázolásra.
        """,
        "kviz": [
            {"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A meghatározás a líra, epika és dráma ötvözésére utal."},
            {"k": "A walesi bárdok nyíltan, burkolás nélkül támadta Ferenc Józsefet.", "v": False, "m": "Allegorikus formában, a walesi monda köntösében fogalmazta meg az ellenállást."},
            {"k": "Az Ágnes asszony lepedőmosása a bűn letörölhetetlenségének lélektani szimbóluma.", "v": True, "m": "A tisztaság kényszeres keresése a lelkiismeret megbomlását mutatja be."},
            {"k": "A Szondi két apródja című ballada Drégely várának ostromát idézi fel párhuzamos szólamokkal.", "v": True, "m": "A török küldönc és az apródok éneke éles kontrasztban áll."},
            {"k": "A Híd-avatás című ballada az Őszikék korszakban, a Margitszigeten íródott.", "v": True, "m": "1877-ben került be a híres Kapcsos könyvbe."},
            {"k": "A Tetemre hívásban az istenítélet középkori babonája leplezi le a gyilkost.", "v": True, "m": "Kund Abigél jelenlétében a seb újra vérezni kezd."}
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
- **Keletkezés:** 1872 – a kiegyezést követő magyar kapitalizálódás és polgári felvirágzás időszaka. Jókai személyes házassági válsága (Laborfalvi Róza mellett a fiatal Lukanics Ottília iránti vonzalma) ihlette a kettős nőalakot.
- **Romantikus elemek:** Mesés véletlenek (a süllyedő Szent Borbála búzaszállítmánya, a rejtett kincs, Krisztyán Tódor végzetes halála), éles jellembeli kontrasztok, a Senki szigete rousseau-i idillje.
- **Realista elemek:** Pontos gazdasági, hajózási és pénzügyi folyamatok (búzakereskedelem, spekuláció, csődeljárás); mély, modern lélektani jellemfejlődés.

---

### II. Timár Mihály belső hasadtsága (A meghasonlott polgár)
- **A név paradoxona:** „Arany ember” – a külvilág szemében sikeres, jótékony nábob, önmaga szemében tolvaj és álszent csábító.
- **Morális bűnbeesése:** Elveszi az elhunyt Ali Csorbadzsi kincsét, majd a vagyont felhasználva megalázza Brazovicsot, és elveszi a védtelen, hálás Timeát.
- **A boldogtalanság oka:** Rájön, hogy a pénzen minden megvehető, csak az őszinte, szívből jövő szeretet nem.

---

### III. Kettős térszerkezet és nőalakok

| Polgári világ (Komárom, Bécs, Levetinc) | Természeti utópia (Senki szigete) |
| :--- | :--- |
| **Képviselője:** Timea | **Képviselője:** Noémi és Teréza mama |
| **Jellemzők:** Pénz, rang, társadalmi konvenciók, hideg pompa. | **Jellemzők:** Pénzmentesség, önfenntartó munka, tiszta erkölcs. |
| **Érzelmi kapcsolat:** Szoborszerű tisztelet, hűség és hála; hiányzó intimitás. | **Érzelmi kapcsolat:** Ösztönös, odaadó, feltétel nélküli szerelem. |
| **Társadalomkép:** Brazovics mohósága, Krisztyán Tódor zsarolása. | **Társadalomkép:** Törvényen és államhatárokon kívüli béke. |

---

### IV. A cselekmény zárlata és megoldása
- **A krízis:** Timár kettős életének fenntarthatatlansága; az öngyilkosság gondolata a Balaton jegénél.
- **A fordulat:** Krisztyán Tódor lezuhan a Balaton rianásában Timár kabátjában $\rightarrow$ a társadalom Timárt halottnak hiszi.
- **Végső tanulság:** Az anyagi javak és a társadalmi pozíció feladása az egyetlen út a valódi lelki békéhez.
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**

1. **Bevezetés (30 mp):**
   * Ismertesd a mű keletkezési idejét (1872) és jelentőségét Jókai életművében.
   * Emeld ki a romantikus regénytechnika és a realista társadalomábrázolás ötvöződését.

2. **Tárgyalás I. – Timár alakja és lélektani válsága (1 perc):**
   * Mutasd be Timár Mihály figuráját: az ügyes nagypolgár, akit kísért a bűntudat a török kincs megtartása és a Timeával kötött érdekházasság miatt.
   * Magyarázd el a polgári meghasonlás folyamatát: a külső anyagi siker nem hozhat belső harmóniát.

3. **Tárgyalás II. – A kettős térszerkezet és a két női eszmény (1 perc):**
   * Állítsd szembe Komáromot (Timea szoborszerű, rideg világa) a Senki szigetével (Noémi természetes, tiszta szerelme).
   * Elemezd a Senki szigetét mint rousseau-i természetközeli utópiát, ahol nincsenek pénzügyi vagy jogi kötöttségek.

4. **Befejezés (30 mp):**
   * Ismertesd a Balaton jegén lezajló feloldást és Timár társadalomból való kilépését mint az emberi boldogság megtalálásának egyetlen útját.
        """,
        "kviz": [
            {"k": "Timár Mihály felesége, Timea szerelemből házasodott össze Timárral.", "v": False, "m": "Timea hálából ment hozzá, szívében Kacsuka kapitányt szerette."},
            {"k": "A Senki szigete pénz- és adómentes, önellátó természeti menedék a regényben.", "v": True, "m": "A társadalmi törvényeken kívül álló romantikus édenkert."},
            {"k": "Krisztyán Tódor a Balaton jegének rianásába zuhanva leli halálát.", "v": True, "m": "Timár ruhájában hal meg, így Timár eltűnhet a civilizáció elől."},
            {"k": "A Szent Borbála nevű hajó a Duna fenekére süllyed a búzaszállítmánnyal.", "v": True, "m": "A megázott búzában találja meg Timár Ali Csorbadzsi kincsét."},
            {"k": "A regényben a romantikus mesei fordulatok pontos realista gazdasági leírásokkal párosulnak.", "v": True, "m": "A búzakereskedelem és az üzleti világ leírása mélyen realista."}
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
- **Műfaj:** Drámai költemény (világdráma, könyvdráma) – a színpadra állítás helyett az eszmék dialógusos ütköztetésére koncentrál.
- **Filozófiai háttér:**
  - *Hegeli dialektika:* Tézis (egy új eszme fellobbanása), Antitézis (az eszme elfajulása és kiábrándulás), Szintézis (továbblépés a következő szintre).
  - *Pozitivizmus és mechanikus materializmus:* Az ember biológiai és fizikai determináltsága.

---

### II. A három archetípus szerepe és viszonyrendszere
- **Ádám:** Az örök emberi szellem, a hit, az eszmékért küzdő és folyton újrakezdő teremtő erő.
- **Lucifer:** A hideg ész, az abszolút tagadás és szkepszis szelleme; célja a teremtés értelmetlenségének bizonyítása és Isten megbuktatása Ádám öngyilkossága révén.
- **Éva:** A természet, az érzelmek, a költészet és a megújulás hordozója; ő testesíti meg az eszmék tisztaságát és az anyaság révén az élet folytonosságát.

---

### III. A történelmi színek tematikus struktúrája (4–14. szín)

1. **Egyiptom (4. szín):** *Eszme:* Szabadság. *Bukás:* A fáraó ráébred, hogy a piramist építő milliók rabszolgasága érvényteleníti a nagyságot.
2. **Athén (5. szín):** *Eszme:* Demokrácia. *Bukás:* A nép hálátlan és megvesztegethető (Miltiadész halála).
3. **Róma (6. szín):** *Eszme:* Érzéki örömök, hedonizmus. *Bukás:* Erkölcsi züllés, pestis és a hit hiánya.
4. **Bizánc (7. szín):** *Eszme:* Keresztény hit. *Bukás:* Fanatizmus, vallásháború és dogmatikus viták (homousion vs. homoiusion).
5. **Prága I. (8. szín):** *Eszme:* Tudomány. *Bukás:* Kepler kénytelen horoszkópkészítésből élni a császári udvarban.
6. **Párizs (9. szín – Álom az álomban):** *Eszme:* Egyenlőség, testvériség, szabadság (Danton). **Kivétel:** Ádám nem csalódik, tettre készen ébred.
7. **Prága II. (10. szín):** Kepler felismeri a szabad gondolat és a jövő diákjainak erejét.
8. **London (11. szín):** *Eszme:* Szabadversenyes kapitalizmus. *Bukás:* Pénzuralom, emberi elszemélytelenedés $\rightarrow$ Haláltánc a Temze partján.
9. **Falanszter (12. szín):** *Eszme:* Racionális tudomány és egyenlőség. *Bukás:* Az egyéniség, érzelmek és művészet (Platón, Michelangelo) teljes elfojtása.
10. **Űr (13. szín):** *Eszme:* Az anyagtól való elszakadás. *Bukás:* A Föld szelleme visszahívja Ádámot.
11. **Eszkimó szín (14. szín):** *Eszme:* Puszta túlélés a kihűlt világban. *Bukás:* Az ember állati sorba való visszasüllyedése.

---

### IV. A 15. záró szín katarzisa
- Ádám az öngyilkossággal akarja megcáfolni Istent és megállítani a történelmet.
- Éva anyasága elvágja Lucifer tervét.
- **Az Úr zárszava:** Nem ad tételes választ a jövőre, de kijelöli az erkölcsi kötelességet: *„Mondottam, ember: küzdj és bízva bízzál!”*
        """,
        "szobeli": """
**🎙️ Részletes 3 perces szóbeli feleletvázlat:**

1. **Bevezetés (30 mp):**
   * Határozd meg a drámai költemény fogalmát és helyezd el a művet az 1859–60-as nemzeti válság kontextusában.
   * Mutasd be a mű alapkoncepcióját: a teremtés értelmének filozófiai vizsgálata.

2. **Tárgyalás I. – A szereplők hármassága és a dialektika (1 perc):**
   * Jellemezd Ádámot (a tettvágy és a hit képviselője), Lucifert (a destruktív hideg ráció) és Évát (az élet és az érzelem elve).
   * Magyarázd el a hegel-i dialektikus fejlődést: hogyan vezet minden történelmi eszme az elkorcsosuláshoz.

3. **Tárgyalás II. – A történelmi színek csomópontjai (1 perc):**
   * Emeld ki, miért Párizs a Tragédia tengelye (egyetlen szín, ami nem kiábrándulással zárul).
   * Állítsd szembe London szabad piacát és a Falanszter mechanikus tudományát mint a modern társadalom két végletét.

4. **Befejezés (30 mp):**
   * Elemezd a 15. szín feloldását: Éva anyaságát és az Úr híres zárszavát, amely a determinizmus helyett a morális küzdelem értékét hirdeti.
        """,
        "kviz": [
            {"k": "Az ember tragédiája összesen 15 színből áll.", "v": True, "m": "4 keretszín és 11 történelmi szín alkotja."},
            {"k": "Ádám a párizsi színből kiábrándultan és csalódottan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel és harci kedvvel ébred."},
            {"k": "A londoni szín végén a szereplők haláltánc kíséretében ugranak a nyitott sírba.", "v": True, "m": "A kapitalista piac zűrzavarának allegorikus lezárása."},
            {"k": "A falanszter színben Michelangelo és Platón elismerést kapnak zseniális alkotásaikért.", "v": False, "m": "Büntetést kapnak, mert a társadalom tiltja az egyéniséget."},
            {"k": "Az Úr végső mondata: 'Mondottam, ember: küzdj és bízva bízzál!'.", "v": True, "m": "Az emberi cselekvés örök erkölcsi parancsa."}
        ]
    }
}

stilusiranyzatok = {
    "Realizmus (19. sz. közepe)": """
### Realizmus (19. század dereka)
- **Történelmi háttér:** Az ipari forradalom kibontakozása, a polgári társadalmak megszilárdulása és a természettudományos gondolkodás térnyerése.
- **Központi esztétikai cél:** A valóság sallangmentes, tárgyilagos, hiteles és tipikus ábrázolása.
- **Módszertan:**
  - *Tipikus jellemek tipikus körülmények között:* A főhősök nem rendkívüli romantikus titánok, hanem koruk társadalmi rétegének hű képviselői.
  - *Társadalmi determináció:* Az egyén jellemét és sorsát környezete, neveltetése és anyagi helyzete határozza meg.
  - *Részletező leírások:* A tárgyi környezet, ruházat, enteriőr és pénzügyi folyamatok aprólékos bemutatása.
- **Kulcsszerzők:** Honoré de Balzac (*Goriot apó*), Lev Tolsztoj (*Anna Karenina*), Mikszáth Kálmán, Jókai Mór késői korszakának regényei.
    """,
    "Naturalizmus (19. sz. vége)": """
### Naturalizmus (19. század vége)
- **Történelmi és filozófiai háttér:** Darwin evolúcióelmélete, Taine környezetelmélete és a pozitivizmus.
- **Központi esztétikai cél:** A valóság fotószerű, klinikai és kíméletlen rögzítése, tabutémák (ösztönök, szexualitás, betegség, nyomor) beemelése.
- **Módszertan:**
  - *Biológiai determinizmus:* Az ember az öröklött gének, ösztönök és a környezet kiszolgáltatottja.
  - *A társadalmi mélyrétegek feltárása:* Bűnözés, alkoholizmus, züllés és a nyomor leírása tudományos objektivitással.
- **Kulcsszerzők:** Émile Zola (*Germinal*, *Nana*), Móricz Zsigmond (*Tragédia*, *Barbárok*).
    """,
    "Impresszionizmus (19. sz. vége – 20. sz. eleje)": """
### Impresszionizmus (19–20. század fordulója)
- **Központi esztétikai cél:** A pillanatnyi benyomások, tovatűnő hangulatok, színek és fények lírai megragadása.
- **Formanyelvi sajátosságok:**
  - Névszói és jelzős stílus, melléknevek halmozása.
  - Erős zeneiség, alliterációk, asszonáncok, hangulatfestő szavak.
  - Szinesztézia (érzékelési területek összekapcsolása, pl. *„lila dalra kelt az éjcsend”*).
- **Kulcsszerzők:** Kosztolányi Dezső, Tóth Árpád, Juhász Gyula, Paul Verlaine.
    """,
    "Szimbolizmus (19. sz. vége – 20. sz. eleje)": """
### Szimbolizmus (19–20. század fordulója)
- **Központi esztétikai cél:** A látható világ mögött rejtőző mélyebb, transzcendens igazságok és lelki állapotok sejtetése többértelmű szimbólumokkal.
- **Formanyelvi sajátosságok:**
  - Rejtélyesség, titokzatosság és látomásszerűség.
  - Egyéni, mítoszteremtő jelképrendszer kialakítása.
  - Zeneiség mint a lélek legközvetlenebb kifejezőeszköze (*„Zenét minékünk, csak zenét!”*).
- **Kulcsszerzők:** Charles Baudelaire (*A romlás virágai*), Arthur Rimbaud, Ady Endre, Vajda János.
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
        if st.button(f"▶️ Hangos monológ elindítása ({kivalasztott_hangos})"):
            with st.spinner("Hangfájl előkészítése és generálása magyar nyelven..."):
                tts = gTTS(text=adat_hangos["audio_szoveg"].strip(), lang='hu', slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
                st.session_state.xp += 25
                st.success("Jó tanulást és hallgatást! (+25 XP) 🎧")
                
    with st.expander("📖 A monológ teljes szövege (olvasáshoz és követéshez)", expanded=True):
        st.write(adat_hangos["audio_szoveg"].strip())

# 3. Menüpont: Stílusirányzatok
elif menupont == "🎨 Stílusirányzatok":
    st.title("Kulcs Stílusirányzatok Mélyelemzése")
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
