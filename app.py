import io
import os
import random
import streamlit as st
import datetime
from fpdf import FPDF
from google import genai
from gtts import gTTS

# Beállítás: Hány naponta frissüljenek a kérdések a detektív játékban és a kártyáknál?
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

# Astra AI stílusú prémium sötét téma és tökéletesen olvasható fehér szövegek
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

# -------------------------------------------------------------
# ADATBÁZISOK (Irodalom, Nyelvtan, Történelem 30 tétel, Matek)
# -------------------------------------------------------------
tetelek_irodalom = {
    "1. Arany János balladái": {"alcim": "Balladaelmélet, Nagykőrös, Őszikék", "kulcsszavak": ["Ballada", "Arany"], "vazlat": "### I. Műfaj: Líra, epika, dráma.\n### II. Nagykőrösi balladák.", "szobeli": "3 perces felelet a balladákról.", "kviz": [{"k": "Greguss elnevezése 'tragédia dalban elbeszélve'?", "v": True, "m": "Igen."}]},
    "2. Jókai Mór: Az arany ember": {"alcim": "Romantika és realizmus", "kulcsszavak": ["Timár", "Jókai"], "vazlat": "### I. Kettős világ.", "szobeli": "Timár Mihály sorsa.", "kviz": [{"k": "A Senki szigete utópia?", "v": True, "m": "Igen."}]},
    "3. Madách: Az ember tragédiája": {"alcim": "Drámai költemény", "kulcsszavak": ["Ádám", "Lucifer"], "vazlat": "### I. 15 szín.", "szobeli": "Eszmék harca.", "kviz": [{"k": "15 színből áll?", "v": True, "m": "Igen."}]},
    "4. Mikszáth: Próza": {"alcim": "Anekdotizmus", "kulcsszavak": ["Mikszáth"], "vazlat": "### I. Tót atyafiak.", "szobeli": "Anekdota szerepe.", "kviz": [{"k": "Pongrácz István főhős?", "v": True, "m": "Igen."}]},
    "5. Vajda János": {"alcim": "Magány, Gina-versek", "kulcsszavak": ["Vajda"], "vazlat": "### I. Magány.", "szobeli": "Gina-szerelem.", "kviz": [{"k": "Montblanc metafora?", "v": True, "m": "Igen."}]},
    "6. Ibsen és Csehov": {"alcim": "Drámafejlődés", "kulcsszavak": ["Dráma"], "vazlat": "### I. Analitikus dráma.", "szobeli": "Ibsen vs Csehov.", "kviz": [{"k": "Nóra Ibsen műve?", "v": True, "m": "Igen."}]},
    "7. Nyugat folyóirat": {"alcim": "Modern magyar irodalom", "kulcsszavak": ["Nyugat"], "vazlat": "### I. 1908-1941.", "szobeli": "3 nemzedék.", "kviz": [{"k": "1908-ban indult?", "v": True, "m": "Igen."}]},
    "8. Ady Endre": {"alcim": "Szimbolizmus", "kulcsszavak": ["Ady"], "vazlat": "### I. Új versek.", "szobeli": "Léda vs Csinszka.", "kviz": [{"k": "Új versek 1906?", "v": True, "m": "Igen."}]},
    "9. Babits: Jónás könyve": {"alcim": "Prófétai szerep", "kulcsszavak": ["Babits"], "vazlat": "### I. 1938.", "szobeli": "Jónás imája.", "kviz": [{"k": "Mert vétkesek közt cinkos?", "v": True, "m": "Igen."}]},
    "10. Móricz Zsigmond": {"alcim": "Naturalizmus", "kulcsszavak": ["Móricz"], "vazlat": "### I. Tragédia.", "szobeli": "Paraszti világ.", "kviz": [{"k": "Tragédia: Kis János?", "v": True, "m": "Igen."}]},
    "11. Kosztolányi: Édes Anna": {"alcim": "Lélektani regény", "kulcsszavak": ["Anna"], "vazlat": "### I. 1919.", "szobeli": "Moviszter doktor.", "kviz": [{"k": "Moviszter emberséges?", "v": True, "m": "Igen."}]},
    "12. Petőfi Sándor": {"alcim": "Forradalmi látomás", "kulcsszavak": ["Petőfi"], "vazlat": "### I. XIX. sz. költői.", "szobeli": "Egy gondolat bánt.", "kviz": [{"k": "Nemzeti dal 1848?", "v": True, "m": "Igen."}]},
    "13. József Attila": {"alcim": "Létösszegzés", "kulcsszavak": ["József Attila"], "vazlat": "### I. Dunánál.", "szobeli": "Eszmélet.", "kviz": [{"k": "Dunánál megbékélés?", "v": True, "m": "Igen."}]},
    "14. Radnóti Miklós": {"alcim": "Háborús eclogák", "kulcsszavak": ["Radnóti"], "vazlat": "### I. Bori notesz.", "szobeli": "Razglednicák.", "kviz": [{"k": "Bori notesz?", "v": True, "m": "Igen."}]},
    "15. Vörösmarty": {"alcim": "Romantika", "kulcsszavak": ["Vörösmarty"], "vazlat": "### I. Csongor.", "szobeli": "Szózat.", "kviz": [{"k": "Szózat 1836?", "v": True, "m": "Igen."}]},
    "16. Csokonai": {"alcim": "Felvilágosodás", "kulcsszavak": ["Csokonai"], "vazlat": "### I. Lilla.", "szobeli": "Reményhez.", "kviz": [{"k": "Reményhez szentimentális?", "v": True, "m": "Igen."}]},
    "17. Berzsenyi": {"alcim": "Ódaköltészet", "kulcsszavak": ["Berzsenyi"], "vazlat": "### I. Magyarokhoz.", "szobeli": "Közelítő tél.", "kviz": [{"k": "Tölgy a nemzet?", "v": True, "m": "Igen."}]},
    "18. Zrínyi Miklós": {"alcim": "Barokk", "kulcsszavak": ["Zrínyi"], "vazlat": "### I. Szigeti veszedelem.", "szobeli": "Athleta Christi.", "kviz": [{"k": "15 ének?", "v": True, "m": "Igen."}]},
    "19. Örkény István": {"alcim": "Groteszk", "kulcsszavak": ["Örkény"], "vazlat": "### I. Tóték.", "szobeli": "Egypercesek.", "kviz": [{"k": "Tóték?", "v": True, "m": "Igen."}]},
    "20. Ottlik Géza": {"alcim": "Létezés", "kulcsszavak": ["Ottlik"], "vazlat": "### I. Iskola.", "szobeli": "Bébé.", "kviz": [{"k": "Kőszeg?", "v": True, "m": "Igen."}]},
    "21. Krúdy Gyula": {"alcim": "Szindbád", "kulcsszavak": ["Krúdy"], "vazlat": "### I. Idő.", "szobeli": "Szecesszió.", "kviz": [{"k": "Szindbád?", "v": True, "m": "Igen."}]},
    "22. Illyés Gyula": {"alcim": "Zsarnokság", "kulcsszavak": ["Illyés"], "vazlat": "### I. Puszták népe.", "szobeli": "Zsarnokság.", "kviz": [{"k": "Egy mondat?", "v": True, "m": "Igen."}]}
}

tetelek_nyelvtan = {
    "1. Kommunikáció": {"alcim": "Modell", "kulcsszavak": ["Adó"], "vazlat": "### I. Jakobson.", "szobeli": "6 tényező.", "kviz": [{"k": "Jakobson?", "v": True, "m": "Igen."}]},
    "2. Szövegtan": {"alcim": "Kohézió", "kulcsszavak": ["Szöveg"], "vazlat": "### I. Kohézió.", "szobeli": "Szerkezet.", "kviz": [{"k": "Anafora?", "v": True, "m": "Igen."}]},
    "3. Helyesírás": {"alcim": "Alapelvek", "kulcsszavak": ["Kiejtés"], "vazlat": "### I. 4 elv.", "szobeli": "Példák.", "kviz": [{"k": "Látja?", "v": True, "m": "Igen."}]},
    "4. Szófajok": {"alcim": "Mondattan", "kulcsszavak": ["Ige"], "vazlat": "### I. Szófajok.", "szobeli": "Mondatrészek.", "kviz": [{"k": "Ige?", "v": True, "m": "Igen."}]},
    "5. Retorika": {"alcim": "Érvelés", "kulcsszavak": ["Érv"], "vazlat": "### I. Tétel.", "szobeli": "Beszéd részei.", "kviz": [{"k": "Cáfolás?", "v": True, "m": "Igen."}]},
    "6. Stilisztika": {"alcim": "Képek", "kulcsszavak": ["Metafora"], "vazlat": "### I. Trópusok.", "szobeli": "Képek.", "kviz": [{"k": "Szinesztézia?", "v": True, "m": "Igen."}]},
    "7. Szókészlet": {"alcim": "Rétegek", "kulcsszavak": ["Szleng"], "vazlat": "### I. Nyelvjárás.", "szobeli": "Időbeli változás.", "kviz": [{"k": "Archaizmus?", "v": False, "m": "Régi."}]},
    "8. Nyelvtörténet": {"alcim": "Finnugor", "kulcsszavak": ["Kazinczy"], "vazlat": "### I. Eredet.", "szobeli": "Nyelvújítás.", "kviz": [{"k": "Halotti beszéd?", "v": True, "m": "Igen."}]},
    "9. Fonetika": {"alcim": "Hangok", "kulcsszavak": ["Zöngés"], "vazlat": "### I. Hasonulás.", "szobeli": "Hasonulás.", "kviz": [{"k": "Színpad?", "v": True, "m": "Igen."}]},
    "10. Morfológia": {"alcim": "Morfémák", "kulcsszavak": ["Tő"], "vazlat": "### I. Sorrend.", "szobeli": "Képző.", "kviz": [{"k": "Rag?", "v": False, "m": "Nem."}]},
    "11. Szóalkotás": {"alcim": "Módok", "kulcsszavak": ["Képzés"], "vazlat": "### I. Összetétel.", "szobeli": "Szóképzés.", "kviz": [{"k": "MÁV?", "v": True, "m": "Betűszó."}]},
    "12. Mondattan": {"alcim": "Összetett", "kulcsszavak": ["Mellérendelő"], "vazlat": "### I. Alárendelés.", "szobeli": "Mellérendelés.", "kviz": [{"k": "Ezért?", "v": True, "m": "Következtető."}]},
    "13. Stílusrétegek": {"alcim": "Rétegek", "kulcsszavak": ["Tudományos"], "vazlat": "### I. Hivatalos.", "szobeli": "Denotáció.", "kviz": [{"k": "Hivatalos?", "v": True, "m": "Száraz."}]},
    "14. Névtan": {"alcim": "Tulajdonnevek", "kulcsszavak": ["Családnév"], "vazlat": "### I. Eredet.", "szobeli": "Keresztnevek.", "kviz": [{"k": "Kovács?", "v": True, "m": "Mesterség."}]},
    "15. Frazeológia": {"alcim": "Szólások", "kulcsszavak": ["Szólás"], "vazlat": "### I. Közmondás.", "szobeli": "Szállóige.", "kviz": [{"k": "Arany?", "v": True, "m": "Közmondás."}]},
    "16. Digitális": {"alcim": "Netnyelv", "kulcsszavak": ["Netnyelv"], "vazlat": "### I. Emojik.", "szobeli": "Írott beszéltség.", "kviz": [{"k": "Írott beszéltség?", "v": True, "m": "Igen."}]}
}

tetelek_tortenelem = {
    "1. Az athéni demokrácia": {"alcim": "Periklész kora", "kulcsszavak": ["Athén"], "vazlat": "### I. Szolón.", "szobeli": "Intézmények.", "kviz": [{"k": "Népgyűlés?", "v": True, "m": "Igen."}]},
    "2. Római Köztársaság válsága": {"alcim": "Caesar és Augustus", "kulcsszavak": ["Róma"], "vazlat": "### I. Principátus.", "szobeli": "Pax Romana.", "kviz": [{"k": "Augustus?", "v": True, "m": "Igen."}]},
    "3. Kereszténység születése": {"alcim": "Ókor", "kulcsszavak": ["Jézus"], "vazlat": "### I. Milánói ediktum.", "szobeli": "Missziók.", "kviz": [{"k": "313?", "v": True, "m": "Igen."}]},
    "4. Középkori uradalom": {"alcim": "Feudalizmus", "kulcsszavak": ["Jobbágy"], "vazlat": "### I. Hűbériség.", "szobeli": "Technika.", "kviz": [{"k": "Ugar?", "v": True, "m": "Igen."}]},
    "5. Iszlám vallás": {"alcim": "Mohamed", "kulcsszavak": ["Korán"], "vazlat": "### I. Hegidzsra.", "szobeli": "Hódítások.", "kviz": [{"k": "622?", "v": True, "m": "Igen."}]},
    "6. Szent István államalapítása": {"alcim": "Keresztény királyság", "kulcsszavak": ["István"], "vazlat": "### I. Vármegyék.", "szobeli": "Egyház.", "kviz": [{"k": "1000?", "v": True, "m": "Igen."}]},
    "7. Aranybulla (1222)": {"alcim": "Nemesi jogok", "kulcsszavak": ["András"], "vazlat": "### I. 31. cikkely.", "szobeli": "Ellenállás.", "kviz": [{"k": "Jog a király ellen?", "v": True, "m": "Igen."}]},
    "8. Anjouk kora": {"alcim": "Károly Róbert, Nagy Lajos", "kulcsszavak": ["Anjou"], "vazlat": "### I. Urbura.", "szobeli": "Ősiség.", "kviz": [{"k": "1351?", "v": True, "m": "Igen."}]},
    "9. Hunyadi Mátyás": {"alcim": "Központosítás", "kulcsszavak": ["Mátyás"], "vazlat": "### I. Fekete sereg.", "szobeli": "Reneszánsz.", "kviz": [{"k": "Bibliotheca?", "v": True, "m": "Igen."}]},
    "10. Mohács és 3 részre szakadás": {"alcim": "1526, 1541", "kulcsszavak": ["Mohács"], "vazlat": "### I. Buda eleste.", "szobeli": "Török.", "kviz": [{"k": "1541?", "v": True, "m": "Igen."}]},
    "11. Rákóczi-szabadságharc": {"alcim": "Kurucok", "kulcsszavak": ["Rákóczi"], "vazlat": "### I. Ónod.", "szobeli": "Szatmár.", "kviz": [{"k": "1707 trónfosztás?", "v": True, "m": "Igen."}]},
    "12. Felvilágosult abszolutizmus": {"alcim": "MT, II. József", "kulcsszavak": ["II. József"], "vazlat": "### I. Türelmi rendelet.", "szobeli": "Reformok.", "kviz": [{"k": "1781?", "v": True, "m": "Igen."}]},
    "13. Reformkor": {"alcim": "Széchenyi, Kossuth", "kulcsszavak": ["Kossuth"], "vazlat": "### I. Hitel.", "szobeli": "Vita.", "kviz": [{"k": "Örökváltság?", "v": True, "m": "Igen."}]},
    "14. 1848-49": {"alcim": "Forradalom", "kulcsszavak": ["Batthyány"], "vazlat": "### I. Áprilisi törvények.", "szobeli": "Hadjárat.", "kviz": [{"k": "1848?", "v": True, "m": "Igen."}]},
    "15. Dualizmus": {"alcim": "Monarchia", "kulcsszavak": ["Kiegyezés"], "vazlat": "### I. Közös ügyek.", "szobeli": "Millennium.", "kviz": [{"k": "1867?", "v": True, "m": "Igen."}]},
    "16. I. világháború": {"alcim": "Trianon", "kulcsszavak": ["Lövészárok"], "vazlat": "### I. Trianon.", "szobeli": "Okok.", "kviz": [{"k": "1914?", "v": True, "m": "Igen."}]},
    "17. Horthy-korszak": {"alcim": "Konszolidáció", "kulcsszavak": ["Bethlen"], "vazlat": "### I. Pengő.", "szobeli": "Klebelsberg.", "kviz": [{"k": "1927?", "v": True, "m": "Igen."}]},
    "18. II. világháború": {"alcim": "Fordulópontok", "kulcsszavak": ["Sztálingrád"], "vazlat": "### I. D-nap.", "szobeli": "Holokauszt.", "kviz": [{"k": "Sztálingrád?", "v": True, "m": "Igen."}]},
    "19. Magyarország a II. vh-ban": {"alcim": "Don-kanyar", "kulcsszavak": ["Don"], "vazlat": "### I. 1944 márc 19.", "szobeli": "Kiugrás.", "kviz": [{"k": "1943?", "v": True, "m": "Igen."}]},
    "20. Hidegháború": {"alcim": "Bipoláris világ", "kulcsszavak": ["NATO"], "vazlat": "### I. Válságok.", "szobeli": "Gorbacsov.", "kviz": [{"k": "1962?", "v": True, "m": "Igen."}]},
    "21. 1956": {"alcim": "Forradalom", "kulcsszavak": ["Nagy Imre"], "vazlat": "### I. Nov 4.", "szobeli": "Semlegesség.", "kviz": [{"k": "1956?", "v": True, "m": "Igen."}]},
    "22. Kádár-korszak": {"alcim": "Konszolidáció", "kulcsszavak": ["Gulyás"], "vazlat": "### I. Alku.", "szobeli": "1968.", "kviz": [{"k": "Aki nincs ellenünk?", "v": True, "m": "Igen."}]},
    "23. Rendszerváltás": {"alcim": "1989", "kulcsszavak": ["Antall"], "vazlat": "### I. EKA.", "szobeli": "Választások.", "kviz": [{"k": "1989 okt 23?", "v": True, "m": "Igen."}]},
    "24. Felfedezések": {"alcim": "Kolumbusz", "kulcsszavak": ["Amerika"], "vazlat": "### I. 1492.", "szobeli": "Árforradalom.", "kviz": [{"k": "1492?", "v": True, "m": "Igen."}]},
    "25. Reformáció": {"alcim": "Luther", "kulcsszavak": ["95 tétel"], "vazlat": "### I. Trentó.", "szobeli": "Jezsuiták.", "kviz": [{"k": "1517?", "v": True, "m": "Igen."}]},
    "26. Angol polgári forradalom": {"alcim": "1689", "kulcsszavak": ["Cromwell"], "vazlat": "### I. Jognyilatkozat.", "szobeli": "Dicsőséges.", "kviz": [{"k": "1689?", "v": True, "m": "Igen."}]},
    "27. Francia forradalom": {"alcim": "1789", "kulcsszavak": ["Napóleon"], "vazlat": "### I. Bastille.", "szobeli": "Terror.", "kviz": [{"k": "1789?", "v": True, "m": "Igen."}]},
    "28. Ipari forradalmak": {"alcim": "Technika", "kulcsszavak": ["Gőzgép"], "vazlat": "### I. Marx.", "szobeli": "Urbanizáció.", "kviz": [{"k": "Watt?", "v": True, "m": "Igen."}]},
    "29. Európai integráció": {"alcim": "EU", "kulcsszavak": ["Maastricht"], "vazlat": "### I. EGK.", "szobeli": "Globalizáció.", "kviz": [{"k": "1992?", "v": True, "m": "Igen."}]},
    "30. Globális kihívások": {"alcim": "Klímaváltozás", "kulcsszavak": ["Migráció"], "vazlat": "### I. Fenntarthatóság.", "szobeli": "AI.", "kviz": [{"k": "Fenntartható?", "v": True, "m": "Igen."}]}
}

tetelek_matek = {
    "1. Halmazok": {"alcim": "Alapok", "kulcsszavak": ["Halmaz"], "vazlat": "### I. Unió.", "szobeli": "Logika.", "kviz": [{"k": "Lottó?", "v": True, "m": "Igen."}]},
    "2. Algebra": {"alcim": "Másodfokú", "kulcsszavak": ["Egyenlet"], "vazlat": "### I. D.", "szobeli": "Megoldóképlet.", "kviz": [{"k": "D < 0?", "v": True, "m": "Igen."}]},
    "3. Hatvány/Logaritmus": {"alcim": "Azonosságok", "kulcsszavak": ["log"], "vazlat": "### I. log.", "szobeli": "Hatvány.", "kviz": [{"k": "log2(8)=3?", "v": True, "m": "Igen."}]},
    "4. Függvények": {"alcim": "Elemzés", "kulcsszavak": ["f(x)"], "vazlat": "### I. Transzformáció.", "szobeli": "Jellemzés.", "kviz": [{"k": "Minimum x=4?", "v": True, "m": "Igen."}]},
    "5. Sorozatok": {"alcim": "Számtani/Mértani", "kulcsszavak": ["d", "q"], "vazlat": "### I. Kamat.", "szobeli": "Képletek.", "kviz": [{"k": "10. tag 32?", "v": True, "m": "Igen."}]},
    "6. Síkgeometria": {"alcim": "Trigonometria", "kulcsszavak": ["sin"], "vazlat": "### I. Koszinusz.", "szobeli": "Szinusz.", "kviz": [{"k": "Koszinusztétel?", "v": True, "m": "Igen."}]},
    "7. Négyszögek": {"alcim": "Terület", "kulcsszavak": ["Sokszög"], "vazlat": "### I. Trapéz.", "szobeli": "Kör.", "kviz": [{"k": "540 fok?", "v": True, "m": "Igen."}]},
    "8. Koordinátageometria": {"alcim": "Vektorok", "kulcsszavak": ["Kör"], "vazlat": "### I. Egyenes.", "szobeli": "Felezőpont.", "kviz": [{"k": "Sugár 5?", "v": True, "m": "Igen."}]},
    "9. Térgeometria": {"alcim": "Testek", "kulcsszavak": ["Gömb"], "vazlat": "### I. Henger.", "szobeli": "Csúcsos.", "kviz": [{"k": "1/3 térfogat?", "v": True, "m": "Igen."}]},
    "10. Valószínűség": {"alcim": "Statisztika", "kulcsszavak": ["Átlag"], "vazlat": "### I. Szórás.", "szobeli": "Medián.", "kviz": [{"k": "Medián?", "v": True, "m": "Igen."}]},
    "11. Gráfok": {"alcim": "Hálózat", "kulcsszavak": ["Fokszám"], "vazlat": "### I. Fa.", "szobeli": "Euler.", "kviz": [{"k": "Páros összeg?", "v": True, "m": "Igen."}]},
    "12. Exponenciális": {"alcim": "Ekvációk", "kulcsszavak": ["Alap"], "vazlat": "### I. u=a^x.", "szobeli": "Kikötés.", "kviz": [{"k": "2^4=16?", "v": True, "m": "Igen."}]},
    "13. Trigonometrikus": {"alcim": "Periodikus", "kulcsszavak": ["sin"], "vazlat": "### I. Egységkör.", "szobeli": "Periodicitás.", "kviz": [{"k": "tg(x)=180?", "v": True, "m": "Igen."}]},
    "14. Vektorok": {"alcim": "Szorzat", "kulcsszavak": ["Skalár"], "vazlat": "### I. Merőleges.", "szobeli": "Hajlásszög.", "kviz": [{"k": "Szorzat 0?", "v": True, "m": "Igen."}]},
    "15. Számelmélet": {"alcim": "Prímek", "kulcsszavak": ["LNKO"], "vazlat": "### I. Prímek.", "szobeli": "Oszthatóság.", "kviz": [{"k": "LNKO 6?", "v": True, "m": "Igen."}]},
    "16. Deriválás": {"alcim": "Változás", "kulcsszavak": ["Érintő"], "vazlat": "### I. Szabály.", "szobeli": "Szélsőérték.", "kviz": [{"k": "4x^3?", "v": True, "m": "Igen."}]}
}

flashcards_irodalom = [{"q": "Mit jelent a ballada?", "a": "Tragédia dalban elbeszélve."}]
flashcards_nyelvtan = [{"q": "Helyesírási alapelvek?", "a": "Kiejtés, szóelemzés, hagyomány, egyszerűsítés."}]
flashcards_tortenelem = [{"q": "Mikor volt a mohácsi csata?", "a": "1526. augusztus 29."}]
flashcards_matek = [{"q": "Másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"}]

timeline_irodalom = [{"ev": "1848", "cim": "Forradalom", "leiras": "Petőfi."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihany", "leiras": "Szórványemlék."}]
timeline_tortenelem = [{"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István."}]
timeline_matek = [{"ev": "Kr.e. VI.", "cim": "Pitagorasz", "leiras": "Tétel."}]

detektiv_irodalom = [{"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály", "opciok": ["Babits Mihály", "Ady"], "info": "Felelősség."}]
detektiv_nyelvtan = [{"idezet": "„barátság [baraccság]”", "helyes": "Összeolvadás", "opciok": ["Összeolvadás", "Hasonulás"], "info": "t+s -> ccs."}]
detektiv_tortenelem = [{"idezet": "„Ellenállási záradék”", "helyes": "1222 Aranybulla", "opciok": ["1222 Aranybulla", "1351 Ősiség"], "info": "Jog."}]
detektiv_matek = [{"idezet": "a² + b² - 2bc*cos(alfa)", "helyes": "Koszinusztétel", "opciok": ["Koszinusztétel", "Pitagorasz"], "info": "Háromszög."}]

# Állapotkezelés
if 'xp' not in st.session_state: st.session_state.xp = 180
if 'level' not in st.session_state: st.session_state.level = 2
if 'streak' not in st.session_state: st.session_state.streak = 4
if 'card_flipped' not in st.session_state: st.session_state.card_flipped = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Szia! Én vagyok a felkészítő mentorod."}]

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
            if c2.button("❌ Hamis", key=f"f_{i}N"): st.error(f"Nem jó. {q['m']}")

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
    idx = get_daily_index(len(aktiv_detektiv))
    f = aktiv_detektiv[idx]
    st.subheader(f"Napi Detektív Feladvány ({tantargy_cimke})")
    st.markdown(f"<div class='topic-card'><h3>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    tipp = st.radio("Válaszd ki a helyeset:", f['opciok'])
    if st.button("Tipp ellenőrzése"):
        if tipp == f['helyes']: st.success(f"Pontos! 🎉 {f['info']}")
        else: st.error(f"Nem találat! A helyes: {f['helyes']}")

elif menupont == "🧭 Tantárgyi Idővonal & Térkép":
    st.subheader(f"{tantargy_cimke} Idővonal")
    for item in aktiv_timeline:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: <h3>{item['cim']}</h3><p>{item['leiras']}</p></div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.subheader(f"Próbavizsga ({tantargy_cimke})")
    st.write("Teszteld le magad!")
    if st.button("Próbavizsga indítása"):
        st.info("A próbavizsga modul aktiválva. Válaszolj a kvízekre a Témakörök menüpontban!")

elif menupont == "🤖 AI Érettségi Mentor":
    st.subheader("AI Érettségi Mentor")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user": st.markdown(f"<div class='chat-user'>🧑‍🎓 {msg['text']}</div>", unsafe_allow_html=True)
        else: st.markdown(f"<div class='chat-ai'>🤖 {msg['text']}</div>", unsafe_allow_html=True)
    
    k = st.text_input("Írj a mentornak:")
    if st.button("Küldés") and k:
        st.session_state.chat_history.append({"role": "user", "text": k})
        v = ai_generalas(f"Vlaszolj érettségi tanárként: {k}")
        st.session_state.chat_history.append({"role": "ai", "text": v})
        st.rerun()
