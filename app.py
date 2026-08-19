import io
import streamlit as st
from fpdf import FPDF
from google import genai

st.set_page_config(
    page_title="Astra Study Pro - Irodalom Érettségi",
    page_icon="✨",
    layout="wide"
)

# Astra AI stílusú UI sötét téma
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

# 11 érettségi tétel adatbázisa
tetelek = {
    "1. Arany János balladái": {
        "alcim": "A ballada fogalma, nagykőrösi évek, Őszikék, csoportosítás",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony"],
        "vazlat": """
### 1. A műfaj sajátosságai
- Definíció: „Tragédia dalban elbeszélve” (Greguss Ágost) – egyesíti a líra, epika és dráma sajátosságait.
- Szerkezet: Sűrítés, balladai homály, kihagyásos technika (ellipszis).

### 2. Korszakok és típusok
- Nagykőrösi balladák (1850-es évek):
  - Történelmi: Allegorikus ellenállás a Bach-rendszer ellen (A walesi bárdok, Szondi két apródja).
  - Lélektani: Bűn és bűnhődés, lélektani téboly (Ágnes asszony, Tetemre hívás).
  - Népies/románcos: Tengeri-hántás, Vörös Rébék.
- Őszikék korszak (1877, Margitsziget, Kapcsos könyv):
  - Időskori líra, nagyvárosi motívumok (Híd-avatás).
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Műfaji definíció (Greguss Ágost), hármas műnemi határ.
2. **Nagykőrös (1 perc):** Nemzeti gyász és ellenállás (A walesi bárdok), lélektani fókusz (Ágnes asszony).
3. **Őszikék (1 perc):** Időskori rezignáció, a technikai civilizáció veszélyei (Híd-avatás).
4. **Befejezés (30 mp):** Nyelvi gazdagság és a balladai forma csúcsa.
        """,
        "kviz": [
            {"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A definíció a három műnem találkozására utal."},
            {"k": "A walesi bárdok nyíltan, burkolás nélkül támadta az uralkodót.", "v": False, "m": "Allegorikusan, a walesi monda képében fogalmazta meg a kritikát."},
            {"k": "Az Ágnes asszony a nagykőrösi lélektani balladák közé tartozik.", "v": True, "m": "A lelkiismeret-furdalás és téboly folyamatát mutatja be."}
        ]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Jókai regényeinek sajátosságai, Az arany ember elemzése",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea vs. Noémi", "Romantika és realizmus"],
        "vazlat": """
### 1. Jókai regénystílusa
- Romantikus vonások: eszményítés, éles kontrasztok, mesés fordulatok.
- Realista elemek: pontos társadalom- és természetrajz, anekdotizmus.

### 2. Az arany ember (1872)
- Timár Mihály belső hasadtsága: A sikeres nagypolgár vs. a lelkifurdalással küzdő ember.
- Kettős térszerkezet: Komárom/Bécs (hideg polgári világ, Timea) <-> Senki szigete (természeti paradicsom, Noémi).
- Megoldás: A társadalomból való kilépés a valódi boldogság feltétele.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Jókai korszaka, a regény személyes ihletettsége.
2. **Timár alakja (1 perc):** Az anyagi siker és morális meghasonlás konfliktusa.
3. **A két világ (1 perc):** Timea és Noémi, Komárom ridegsége és a Senki szigete utópiája.
4. **Befejezés (30 mp):** A romantikus illúziók és a polgári valóság szembesítése.
        """,
        "kviz": [
            {"k": "Timár Mihály a Senki szigetén Noémivel él.", "v": True, "m": "Ott találja meg az őszinte, pénzmentes boldogságot."},
            {"k": "A Senki szigete a modern iparosodás szimbóluma.", "v": False, "m": "A Senki szigete a pénztől független természetközeli idill jelképe."}
        ]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény fogalma, színek elemzése",
        "kulcsszavak": ["Drámai köktemény", "15 szín", "Ádám és Lucifer", "Küzdj és bízva bízzál"],
        "vazlat": """
### 1. Műfaj
- Drámai költemény (világdráma): Emberiség- és létezésfilozófiai kérdések dialógusos formában.

### 2. Szerkezet (15 szín)
- Keretszínek (1–3., 15.): Menny, Paradicsom, pálmafás táj.
- Történelmi színek (4–14.): Tézis-antitézis fejlődés; Párizs az egyetlen szín, amiből Ádám nem csalódottan ébred.
- Zárszó: „Mondottam, ember: küzdj és bízva bízzál!”
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Műfaj meghatározása, 1859–60 történelmi válsága.
2. **Karakterek (1 perc):** Ádám (hit és tettvágy), Lucifer (ráció és tagadás), Éva (természetesség és megújulás).
3. **Történelmi ív (1 perc):** Eszmék felvirágzása és elkorcsosulása (Párizs és London szerepe).
4. **Befejezés (30 mp):** A 15. szín: a küzdelem önértéke.
        """,
        "kviz": [
            {"k": "Az ember tragédiája 15 színből áll.", "v": True, "m": "4 keretszín és 11 történelmi szín."},
            {"k": "Ádám a párizsi színből csalódottan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, melyből Ádám lelkesülten ébred."}
        ]
    },
    "4. Mikszáth Kálmán prózája": {
        "alcim": "Beszterce ostroma, A tót atyafiak, A jó palócok",
        "kulcsszavak": ["Anekdota", "Palócföld", "Pongrácz István", "Élőbeszéd"],
        "vazlat": """
### 1. Stílusjegyek
- Anekdotizmus, közvetlen mesélői stílus, szelíd irónia, realista megfigyelés romantikus bájjal.

### 2. Kötetek és regények
- A tót atyafiak (1881): 4 hosszú elbeszélés, monumentális lelkivilágú hegyi emberek (Lapaj).
- A jó palócok (1882): 15 rövid novella, tömörség, balladisztikus kihagyások (Bede Anna tartozása).
- Beszterce ostroma: Pongrácz István anakronisztikus, lovagkorban rekedt alakjának bemutatása.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Átmenet a romantika és a realizmus határán.
2. **Novelláskötetek (1 perc):** Tót atyafiak zárt hegyvidéke vs. Jó palócok érzelmes faluja.
3. **Beszterce ostroma (1 perc):** Pongrácz István Don Quijote-i jelleme és a dzsentri világ kritikája.
4. **Befejezés (30 mp):** Az anekdotikus próza megújítása.
        """,
        "kviz": [
            {"k": "A tót atyafiak kötetben kevesebb, de hosszabb novella található, mint A jó palócokban.", "v": True, "m": "4 terjedelmes elbeszélésből áll."},
            {"k": "Pongrácz István a modern gyáriparosok életét éli.", "v": False, "m": "Középkori lovagként viselkedik a 19. század végén."}
        ]
    },
    "5. Vajda János költészete": {
        "alcim": "Költészetének újdonsága, lírai magány, Gina-szerelem",
        "kulcsszavak": ["Gina-versek", "Montblanc", "A vaáli erdőben", "Szimbolizmus előfutára"],
        "vazlat": """
### 1. Irodalomtörténeti szerepe
- Átmenet a romantika és a modernség között; a meg nem értett művész magánya.

### 2. Főbb lírai témái
- Gina-ciklus: Évtizedes reménytelen szerelem (Húsz év múlva, Harminc év után).
- Filozofikus tájlíra: Panteizmus, természeti csend és megbékélés (A vaáli erdőben).
- Közéleti líra: A kiegyezés korának passzivitását bíráló művek (A virrasztók).
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** A magány költője; híd a romantika és a Nyugat nemzedéke között.
2. **Gina-szerelem (1 perc):** A Montblanc-metafora (Húsz év múlva) és a beteljesületlenség élménye.
3. **Filozofikus magány (1 perc):** A vaáli erdőben csend-élménye és a halállal való megbékélés.
4. **Befejezés (30 mp):** Hatása az Ady-féle modern szimbolizmusra.
        """,
        "kviz": [
            {"k": "Vajda János a modern magyar szimbolizmus közvetlen előfutára.", "v": True, "m": "Egyéni szimbólumai már a 20. századi modernitást jelzik."},
            {"k": "A Montblanc-metafora a 'Húsz év múlva' központi képe.", "v": True, "m": "A külső fagyos nyugalom és belső izzás ellentéte."}
        ]
    },
    "6. XIX. századi dráma: Ibsen és Csehov": {
        "alcim": "Analitikus dráma és drámaiatlan dráma fogalma",
        "kulcsszavak": ["Analitikus dráma", "Nóra", "Drámaiatlan dráma", "Csehov atmoszféra"],
        "vazlat": """
### 1. Henrik Ibsen: Analitikus dráma
- A múltban rejtőző titkok fokozatos felszínre kerülése robbantja ki a jelen krízisét (Nóra / Babaszoba, Vadkacsa).

### 2. Anton Csehov: Drámaiatlan (hangulat)dráma
- Nincsenek látványos fordulatok; a cselekvésképtelenség, a belső elvágyódás és a hangulat (atmoszféra) dominál (Sirály, Három nővér, Cseresznyéskert).
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** A polgári dráma megújulásának kényszere a 19. század végén.
2. **Ibsen analitikája (1 perc):** Nóra önállósodása és a múlt feltárása mint drámai mozgatórugó.
3. **Csehov hangulatdrámája (1 perc):** A monológok párhuzamossága, a tehetetlenség és a 'Moszkvába!' vágy tragikuma.
4. **Befejezés (30 mp):** A kétféle drámatípus hatása a modern színházművészetre.
        """,
        "kviz": [
            {"k": "Ibsen analitikus drámáiban a múlt rejtélyei robbantják fel a jelent.", "v": True, "m": "Ez az analitikus dramaturgia alapja."},
            {"k": "Csehov darabjaira a gyors akciók és hirtelen csaták jellemzőek.", "v": False, "m": "A passzivitás és a belső hangulatok ábrázolása a meghatározó."}
        ]
    },
    "7. A Nyugat folyóirat": {
        "alcim": "A folyóirat jelentősége, szerkesztői, nemzedékei",
        "kulcsszavak": ["1908", "Osvát Ernő", "Ignotus", "Három nemzedék"],
        "vazlat": """
### 1. Indulás és eszmeiség
- 1908. január 1-jén indult; emblémája a Beck Ö. Fülöp-féle Mikes-emlékérem.
- Cél: felzárkózás a nyugat-európai polgári kultúrához és a művészi autonómia megteremtése.

### 2. Főbb szerkesztők
- Ignotus (főszerkesztő), Osvát Ernő (irodalmi szerkesztő), Hatvany Lajos (mecénás).

### 3. A nemzedékek
- 1. nemzedék: Ady, Babits, Kosztolányi, Móricz, Juhász Gyula, Tóth Árpád.
- 2. nemzedék: Szabó Lőrinc, Illyés Gyula, Németh László.
- 3. nemzedék: Radnóti Miklós, Weöres Sándor, Szerb Antal.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** A konzervatív irodalomszemlélet meghaladása és a lap indulása 1908-ban.
2. **Szerkesztőség (1 perc):** Osvát Ernő ízlésformáló, szigorú szerkesztői szerepe.
3. **Nemzedékek (1 perc):** Az 1. nemzedék stiláris forradalma és a későbbi nemzedékek kibontakozása.
4. **Befejezés (30 mp):** A folyóirat irodalmi kánonformáló öröksége.
        """,
        "kviz": [
            {"k": "A Nyugat folyóirat 1908-ban indult útjára.", "v": True, "m": "1941-ig, Babits haláláig működött."},
            {"k": "Osvát Ernő volt a lap legfontosabb irodalmi szerkesztője.", "v": True, "m": "Ő fedezte fel a korszak meghatározó tehetségeit."}
        ]
    },
    "8. Ady Endre költészete": {
        "alcim": "Szimbolizmus, ars poetica, szerelmi líra, pénz, háborúellenesség",
        "kulcsszavak": ["Új versek 1906", "A magyar Ugaron", "Léda vs. Csinszka", "Harc a Nagyúrral"],
        "vazlat": """
### 1. Új versek (1906) & Szimbolizmus
- Egyéni szimbólumrendszer (Ugar, Bakony, Én, Halál).
- Ars poetica: Góg és Magóg fia vagyok én..., Új vizeken járok.

### 2. Főbb tematikus vonulatok
- Magyarság-versek: A magyar Ugaron (elmaradottság, művészsors).
- Pénz és létküzdelem: Harc a Nagyúrral (disznófejű Nagyúr).
- Szerelmi líra: Léda (küzdelmes párharc: Héja-nász az avaron) vs. Csinszka (védelmező menedék: Őrizem a szemed).
- Háborús líra: Ember az embertelenségben.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Az 1906-os kötet jelentősége a modern magyar költészetben.
2. **Magyarság és egzisztencia (1 perc):** Az Ugar toposza és a pénzért vívott küzdelem a disznófejű Nagyúrral.
3. **A szerelmi líra kettőssége (1 perc):** Léda pusztító szenvedélye és Csinszka háború alatti biztonsága.
4. **Befejezés (30 mp):** Az emberség védelme a világháború borzalmai közepette.
        """,
        "kviz": [
            {"k": "A Harc a Nagyúrral versben a disznófejű Nagyúr a pénz bálványa.", "v": True, "m": "A költő megalázkodik az anyagi túlélésért."},
            {"k": "A Léda-verseket a békés polgári harmónia jellemzi.", "v": False, "m": "Végletes feszültség és gyötrelmes párharc bontakozik ki bennük."}
        ]
    },
    "9. Babits Mihály: Jónás könyve": {
        "alcim": "Jónás könyve és Jónás imája – prófétai felelősségvállalás",
        "kulcsszavak": ["Jónás könyve", "Jónás imája", "Ninive", "Cinkos, aki néma"],
        "vazlat": """
### 1. Háttér és keletkezés
- 1938: Súlyos betegsége (gégeműtét) és a fasizmus előretörésének idején született.

### 2. Jónás könyve & Jónás imája
- Ószövetségi parafrázis öniróniával és groteszk elemekkel.
- Alaptézis: „Mert vétkesek közt cinkos, aki néma.”
- A záró Jónás imája alázatos könyörgés a tiszta kifejezésért a halál árnyékában.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** A kései Babits tragikus élethelyzete (1938).
2. **A menekülő próféta (1 perc):** Jónás emberi gyarlósága, a cet gyomra mint belső megtisztulás állomása.
3. **Ninive és a morális tanulság (1 perc):** A prófétai kötelesség elől nem lehet elzárkózni.
4. **Befejezés (30 mp):** A Jónás imája mint az alkotó ember végső hitvallása.
        """,
        "kviz": [
            {"k": "A Jónás könyve bibliai parafrázis önironikus felhangokkal.", "v": True, "m": "Babits saját írói gyengeségeit vetíti Jónásra."},
            {"k": "A 'mert vétkesek közt cinkos, aki néma' szállóige ebből a műből származik.", "v": True, "m": "A felelősségvállalás központi etikai parancsa."}
        ]
    },
    "10. Móricz Zsigmond prózája": {
        "alcim": "Úri muri, Barbárok, Tragédia – a magyar valóság és naturalizmus",
        "kulcsszavak": ["Naturalizmus", "Tragédia", "Barbárok", "Szakhmáry Zoltán"],
        "vazlat": """
### 1. Írói stílus
- Realizmus és naturalizmus: ösztönök, biológiai kiszolgáltatottság, társadalmi és morális válság.

### 2. Főbb művek
- Tragédia (1909): Kis János abszurd, evésbe fulladó lázadása.
- Barbárok (1931): Pusztai pásztorok brutális rablógyilkossága balladisztikus formában.
- Úri muri (1928): Szakhmáry Zoltán dzsentri vergődése és önpusztító mulatozása.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** Szakítás a népies idillel, a rideg magyar valóság ábrázolása.
2. **A szegénység ösztönvilága (1 perc):** Kis János biológiai elnyomottsága és a Barbárok primitív ösztönvilága.
3. **A dzsentri társadalmi csődje (1 perc):** Szakhmáry Zoltán tehetetlensége és tragédiája az Úri muriban.
4. **Befejezés (30 mp):** A 20. századi magyar kritikai realizmus megteremtése.
        """,
        "kviz": [
            {"k": "A Tragédia című novellában Kis János az evésbe pusztul bele.", "v": True, "m": "Az evés jelentette számára az egyetlen ösztönös bosszút."},
            {"k": "Az Úri muri központi karaktere Szakhmáry Zoltán.", "v": True, "m": "A talaját vesztett, illúziókban élő magyar dzsentri példája."}
        ]
    },
    "11. Kosztolányi Dezső: Édes Anna": {
        "alcim": "Lélektani regény, emberi méltóság és kiszolgáltatottság",
        "kulcsszavak": ["Lélektani regény", "Édes Anna", "Vizy család", "Moviszter doktor"],
        "vazlat": """
### 1. Történelmi háttér és lélektan
- Megjelenés: 1926; keret: 1919 nyara (Tanácsköztársaság bukása).
- Freud hatása: tudattalan feszültségek, elfojtások felhalmozódása.

### 2. Cselekmény és konfliktus
- Anna mintagépként működik Vizyéknél, de emberi méltóságától megfosztják.
- Jancsi úrfi elcsábítja, majd cserbenhagyja.
- A gyilkosság ösztönös reakció az elnyomásra.
- Moviszter doktor: A tiszta humanizmus és empátia képviselője.
        """,
        "szobeli": """
**🎙️ 3 perces szóbeli feleletvázlat:**
1. **Bevezetés (30 mp):** A mű keletkezési közege (1919) és a pszichoanalízis hatása.
2. **Anna dehumanizálása (1 perc):** Tárgyiasított cselédsors, Vizyné önzése és Jancsi úrfi árulása.
3. **A bűntett lélektana (1 perc):** Az elfojtott megaláztatások váratlan robbanása.
4. **Befejezés (30 mp):** Moviszter doktor embersége és a humánum üzenete.
        """,
        "kviz": [
            {"k": "Moviszter doktor képviseli az empátiát a regényben.", "v": True, "m": "Ő az egyetlen, aki nem gépként, hanem emberként látja Annát."},
            {"k": "Anna előre eltervezett politikai indíttatásból gyilkol.", "v": False, "m": "Tette ösztönös reflex a tartós elfojtások után."}
        ]
    }
}

stilusiranyzatok = {
    "Realizmus (19. sz. közepe)": """
- Cél: A valóság tárgyilagos, hiteles ábrázolása.
- Módszer: Tipikus jellemek tipikus körülmények között.
- Képviselők: Mikszáth Kálmán, Tolsztoj, Balzac.
    """,
    "Naturalizmus (19. sz. vége)": """
- Cél: A valóság szépítés nélküli, nyers leírása.
- Emberkép: Az ember az ösztönök és öröklődés rabja.
- Képviselők: Émile Zola, Móricz Zsigmond (Tragédia, Barbárok).
    """,
    "Impresszionizmus (19. sz. vége – 20. sz. eleje)": """
- Cél: A múló pillanatok, benyomások, fények megragadása.
- Stílusjegyek: Névszói stílus, zeneiség, vizuális finomságok.
- Képviselők: Kosztolányi Dezső, Tóth Árpád, Juhász Gyula.
    """,
    "Szimbolizmus (19. sz. vége – 20. sz. eleje)": """
- Cél: A mélyebb valóság kifejezése többértelmű szimbólumokkal.
- Stílusjegyek: Rejtettség, sejtetés, zeneiség.
- Képviselők: Baudelaire, Verlaine, Ady Endre.
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
    st.title("✨ Astra Study Pro")
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
    ["📖 Tételek & Vázlatok", "🎨 Stílusirányzatok", "🏆 Nagy Próbavizsga", "🤖 AI Érettségi Mentor"]
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
    
    tab1, tab2, tab3 = st.tabs(["📝 Írásbeli vázlat", "🎙️ 3 perces szóbeli felelet", "⚡ Gyors teszt"])
    
    with tab1:
        st.markdown(adat["vazlat"])
        
    with tab2:
        st.markdown("<div class='oral-box'>", unsafe_allow_html=True)
        st.markdown(adat["szobeli"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab3:
        st.subheader("Ellenőrizd a tudásod!")
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

# 2. Menüpont: Stílusirányzatok
elif menupont == "🎨 Stílusirányzatok":
    st.title("Kulcs Stílusirányzatok")
    for nev, leiras in stilusiranyzatok.items():
        with st.expander(f"📌 {nev}", expanded=True):
            st.markdown(leiras)

# 3. Menüpont: Nagy Próbavizsga
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

# 4. Menüpont: AI Érettségi Mentor Chat
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
                    
                    # Automatikus modellkeresés a fiókodban engedélyezett modellek közül
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
