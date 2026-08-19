import io
import os
import random
import streamlit as st
import datetime
from fpdf import FPDF
from google import genai
from gtts import gTTS

FRISSITESI_GYAKORISAG_NAPOKBAN = 1

def get_daily_index(lista_hossza):
    nap_sorszam = datetime.date.today().toordinal() // FRISSITESI_GYAKORISAG_NAPOKBAN
    return nap_sorszam % lista_hossza

st.set_page_config(page_title="Érettségi Felkészítő", page_icon="🎓", layout="wide")

st.markdown("""<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .stSidebar { background-color: #111827 !important; }
    .stButton>button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; font-weight: 700 !important; }
    .topic-card { background-color: #1f2937; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #818cf8; }
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); padding: 40px; text-align: center; border-radius: 15px; font-size: 1.2rem; }
    .chat-user { background-color: #4f46e5; color: white; padding: 10px; border-radius: 10px; margin-bottom: 5px; width: fit-content; margin-left: auto; }
    .chat-ai { background-color: #1f2937; color: #f3f4f6; padding: 10px; border-radius: 10px; margin-bottom: 5px; width: fit-content; }
</style>""", unsafe_allow_html=True)

tetelek_irodalom = {
    "1. Arany János balladái": {"alcim": "Balladaelmélet, Nagykőrös, Őszikék", "kulcsszavak": ["Ballada", "Arany"], "vazlat": "### I. Műfaj: Líra, epika, dráma.\n### II. Balladák.", "szobeli": "3 perces felelet...", "kviz": [{"k": "Greguss elnevezése igaz?", "v": True, "m": "Tragédia dalban."}]},
    "2. Jókai Mór: Az arany ember": {"alcim": "Romantika és realizmus", "kulcsszavak": ["Timár", "Jókai"], "vazlat": "### I. Kettős világ.", "szobeli": "Timár Mihály sorsa.", "kviz": [{"k": "Timea szerelmi házasság?", "v": False, "m": "Hálából."}]},
    "3. Madách: Az ember tragédiája": {"alcim": "Drámai költemény", "kulcsszavak": ["Ádám", "Lucifer"], "vazlat": "### I. 15 szín.", "szobeli": "Eszmék harca.", "kviz": [{"k": "15 színből áll?", "v": True, "m": "Igen."}]},
    "4. Mikszáth: Próza": {"alcim": "Anekdotizmus", "kulcsszavak": ["Mikszáth"], "vazlat": "### I. Tót atyafiak.", "szobeli": "Anekdota szerepe.", "kviz": [{"k": "Tót atyafiak 4 novella?", "v": True, "m": "Igen."}]},
    "5. Vajda János": {"alcim": "Magány, Gina-versek", "kulcsszavak": ["Vajda"], "vazlat": "### I. Magány.", "szobeli": "Gina-szerelem.", "kviz": [{"k": "Montblanc metafora?", "v": True, "m": "Jég és tűz."}]},
    "6. Ibsen és Csehov": {"alcim": "Drámafejlődés", "kulcsszavak": ["Dráma"], "vazlat": "### I. Analitikus dráma.", "szobeli": "Ibsen vs Csehov.", "kviz": [{"k": "Nóra Ibsen műve?", "v": True, "m": "Igen."}]},
    "7. Nyugat folyóirat": {"alcim": "Modern magyar irodalom", "kulcsszavak": ["Nyugat"], "vazlat": "### I. 1908-1941.", "szobeli": "3 nemzedék.", "kviz": [{"k": "1908-ban indult?", "v": True, "m": "Igen."}]},
    "8. Ady Endre": {"alcim": "Szimbolizmus", "kulcsszavak": ["Ady"], "vazlat": "### I. Új versek.", "szobeli": "Léda vs Csinszka.", "kviz": [{"k": "Új versek 1906?", "v": True, "m": "Igen."}]},
    "9. Babits: Jónás könyve": {"alcim": "Prófétai szerep", "kulcsszavak": ["Babits"], "vazlat": "### I. 1938.", "szobeli": "Jónás imája.", "kviz": [{"k": "Mert vétkesek közt cinkos?", "v": True, "m": "Igen."}]},
    "10. Móricz Zsigmond": {"alcim": "Naturalizmus", "kulcsszavak": ["Móricz"], "vazlat": "### I. Tragédia.", "szobeli": "Paraszti világ.", "kviz": [{"k": "Tragédia: Kis János?", "v": True, "m": "Igen."}]},
    "11. Kosztolányi: Édes Anna": {"alcim": "Lélektani regény", "kulcsszavak": ["Anna"], "vazlat": "### I. 1919.", "szobeli": "Moviszter doktor.", "kviz": [{"k": "Anna politikai gyilkos?", "v": False, "m": "Lélektani."}]},
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

# (Folytatódik a 2. részletben...)
# -------------------------------------------------------------
# 3. TÖRTÉNELEM TÉTELTÁR (30 Tétel)
# -------------------------------------------------------------
tetelek_tortenelem = {
    "1. Az athéni demokrácia": {"alcim": "Periklész kora", "kulcsszavak": ["Athén"], "vazlat": "### I. Szolón/Kleiszthenész.", "szobeli": "Intézmények.", "kviz": [{"k": "Népgyűlés?", "v": True, "m": "Igen."}]},
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

# -------------------------------------------------------------
# 4. MATEMATIKA TÉTELTÁR (16 Témakör)
# -------------------------------------------------------------
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
# -------------------------------------------------------------
# VILLÁMKÁRTYÁK (FLASHCARDS) TANTÁRGYANKÉNT
# -------------------------------------------------------------
flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra, epika és dráma sajátosságait."},
    {"q": "Melyik évben indult a Nyugat és ki volt a szerkesztője?", "a": "1908-ban, Osvát Ernő szerkesztette."},
    {"q": "Mi a központi szállóige Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.”"},
    {"q": "Mit szimbolizál az Ágnes asszony véres lepedője?", "a": "A bűn letörölhetetlenségét és a tébolyt."},
    {"q": "Miért különleges a párizsi szín a Tragédiában?", "a": "Az egyetlen történelmi szín, amiből Ádám hittel ébred."},
    {"q": "Ki a modern magyar próza megalapozója anekdotáival?", "a": "Mikszáth Kálmán."},
    {"q": "Mi a Montblanc-metafora Vajdánál?", "a": "A külső hideg és a belső vulkanikus érzelem ellentéte."},
    {"q": "Melyik kötet nyitotta Ady költői forradalmát?", "a": "Új versek (1906)."}
]

flashcards_nyelvtan = [
    {"q": "Mi a 4 helyesírási alapelv?", "a": "Kiejtés, szóelemzés, hagyomány, egyszerűsítés."},
    {"q": "Mi a toldalékok sorrendje?", "a": "Tő + Képző + Jel + Rag."},
    {"q": "Mi a különbség az anafora és a katafora között?", "a": "Anafora: visszautalás, Katafora: előreutalás."},
    {"q": "Mi az 'egyperces' novella stílusa?", "a": "Groteszk és tömör."},
    {"q": "Milyen törvény a 'barátság' -> 'baraccság'?", "a": "Összeolvadás."},
    {"q": "Mi a fatikus funkció?", "a": "Kapcsolattartás."},
    {"q": "Ki a nyelvújítás vezéralakja?", "a": "Kazinczy Ferenc."}
]

flashcards_tortenelem = [
    {"q": "Mikor adta ki Nagy Lajos az Ősiséget?", "a": "1351-ben."},
    {"q": "Mikor esett el Buda (török kéz)?", "a": "1541. augusztus 29."},
    {"q": "Mikor volt a mohácsi csata?", "a": "1526. augusztus 29."},
    {"q": "Melyik pénznemet vezette be Bethlen?", "a": "Pengő."},
    {"q": "Mikor volt a Kiegyezés?", "a": "1867."},
    {"q": "Mikor volt a forradalom kitörése?", "a": "1848. március 15."},
    {"q": "Mikor indult a szovjet invázió '56-ban?", "a": "1956. november 4."}
]

flashcards_matek = [
    {"q": "Mi a másodfokú egyenlet megoldóképlete?", "a": "x1,2 = (-b ± √(b² - 4ac)) / (2a)"},
    {"q": "Melyik tétel általánosítja Pitagoraszt?", "a": "Koszinusztétel."},
    {"q": "Mi a gömb térfogata?", "a": "4/3 * R³ * π"},
    {"q": "Mi a 0! értéke?", "a": "1."},
    {"q": "Mi a deriváltja x^n-nek?", "a": "n * x^(n-1)."},
    {"q": "Mit jelent az LNKO?", "a": "Legnagyobb közös osztó."}
]

# -------------------------------------------------------------
# IDŐVONALAK
# -------------------------------------------------------------
timeline_irodalom = [{"ev": "1848", "cim": "Forradalom lírája", "leiras": "Petőfi, Arany."}, {"ev": "1908", "cim": "Nyugat", "leiras": "Ady, Babits."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihany", "leiras": "Szórványemlék."}, {"ev": "1790", "cim": "Nyelvújítás", "leiras": "Kazinczy."}]
timeline_tortenelem = [
    {"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István."},
    {"ev": "1222", "cim": "Aranybulla", "leiras": "II. András."},
    {"ev": "1526", "cim": "Mohács", "leiras": "Vereség."},
    {"ev": "1848", "cim": "Forradalom", "leiras": "Szabadságharc."},
    {"ev": "1956", "cim": "Forradalom", "leiras": "Szovjet invázió."}
]
timeline_matek = [
    {"ev": "Kr.e. VI.", "cim": "Pitagorasz", "leiras": "Tétel."},
    {"ev": "1687", "cim": "Newton", "leiras": "Deriválás."}
]

# -------------------------------------------------------------
# DETEKTÍV JÁTÉK
# -------------------------------------------------------------
detektiv_irodalom = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre", "Arany János"], "info": "Felelősség."},
    {"idezet": "„Ha férfi vagy, légy férfi...”", "helyes": "Petőfi Sándor", "opciok": ["Petőfi Sándor", "Vörösmarty", "Ady"], "info": "Forradalmi vers."}
]
detektiv_nyelvtan = [
    {"idezet": "„barátság [baraccság]”", "helyes": "Összeolvadás", "opciok": ["Összeolvadás", "Hasonulás", "Kiesés"], "info": "t+s -> ccs."},
    {"idezet": "„lila dal”", "helyes": "Szinesztézia", "opciok": ["Szinesztézia", "Metafora", "Megszemélyesítés"], "info": "Érzékkeverés."}
]
detektiv_tortenelem = [
    {"idezet": "„Ellenállási záradék”", "helyes": "1222 Aranybulla", "opciok": ["1222 Aranybulla", "1351 Ősiség", "István törvényei"], "info": "Jog a király ellen."},
    {"idezet": "„Aki nincs ellenünk, az velünk van”", "helyes": "Kádár-rendszer", "opciok": ["Kádár-rendszer", "Rákosi-korszak", "Horthy-korszak"], "info": "Konszolidáció."}
]
detektiv_matek = [
    {"idezet": "a² + b² - 2bc*cos(alfa)", "helyes": "Koszinusztétel", "opciok": ["Koszinusztétel", "Pitagorasz", "Szinusztétel"], "info": "Általános háromszög."},
    {"idezet": "f'(x) = n*x^(n-1)", "helyes": "Deriválási szabály", "opciok": ["Deriválási szabály", "Hatványozás", "Logaritmus"], "info": "Hatványfüggvény."}
]
# -------------------------------------------------------------
# AI ÉRETTSÉGI MENTOR ÉS MENÜPONT KEZELÉS
# -------------------------------------------------------------

# Adatbázisok szétválasztása
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
if st.sidebar.button(f"📄 {tantargy_cimke} PDF Letöltése"):
    pdf_bytes = letoltheto_pdf_generalas(aktiv_adatbazis, tantargy_cimke)
    st.sidebar.download_button("⬇️ Letöltés", data=pdf_bytes, file_name=f"{tantargy_cimke}_Puska.pdf", mime="application/pdf")

# Menüpontok logikája
if menupont == "📚 Tételek & Vázlatok":
    st.markdown(f"<div class='subject-pill'>🎯 {tantargy_cimke}</div>", unsafe_allow_html=True)
    tetel = st.selectbox("Válassz tételt:", list(aktiv_adatbazis.keys()))
    adat = aktiv_adatbazis[tetel]
    st.markdown(f"<div class='topic-card'><h2>{tetel}</h2><p>{adat['alcim']}</p></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📚 Tananyag", "🎙️ Feleletvázlat", "⚡ Kvíz"])
    with tab1: st.markdown(f"<div class='deep-text'>{adat['vazlat']}</div>", unsafe_allow_html=True)
    with tab2: st.markdown(f"<div class='oral-box'>{adat['szobeli']}</div>", unsafe_allow_html=True)
    with tab3:
        for i, q in enumerate(adat["kviz"]):
            st.write(f"**{i+1}. {q['k']}**")
            if st.button("✅ Igaz", key=f"t_{i}"): st.success("Helyes!")
            if st.button("❌ Hamis", key=f"f_{i}"): st.error("Hibás!")

elif menupont == "🎧 Hangoskönyv (Monológ)":
    tetel = st.selectbox("Tétel:", list(aktiv_adatbazis.keys()))
    if st.button("▶️ Hangos indítás"):
        tts = gTTS(text=aktiv_adatbazis[tetel]["audio_szoveg"], lang='hu', slow=False)
        f = io.BytesIO(); tts.write_to_fp(f); st.audio(f)

elif menupont == "🎴 Villámkártyák (Flashcards)":
    idx = get_daily_index(len(aktiv_flashcards))
    k = aktiv_flashcards[idx]
    if not st.session_state.card_flipped:
        st.markdown(f"<div class='flashcard'>❓ {k['q']}</div>", unsafe_allow_html=True)
        if st.button("🔄 Megfordítás"): st.session_state.card_flipped = True; st.rerun()
    else:
        st.markdown(f"<div class='flashcard'>💡 {k['a']}</div>", unsafe_allow_html=True)
        if st.button("Újra"): st.session_state.card_flipped = False; st.rerun()

elif menupont == "🎙️ Szóbeli Szimulátor (Beszéd / Írás)":
    st.subheader("Szóbeli vizsga szimuláció")
    audio = st.audio_input("Mondd el a feleleted:")
    if audio:
        if st.button("Értékelés"):
            st.write(ai_generalas("Értékeld ezt a szóbeli választ:", audio_bytes=audio.read(), mime_type="audio/wav"))

elif menupont == "✍️ Esszé & Feladatmegoldó Labor":
    munka = st.text_area("Másold be:")
    if st.button("Javítás"): st.write(ai_generalas(f"Javítsd ezt: {munka}"))

elif menupont == "🎭 Tantárgyi Detektív Játék":
    idx = get_daily_index(len(aktiv_detektiv))
    f = aktiv_detektiv[idx]
    st.markdown(f"<div class='topic-card'><h3>{f['idezet']}</h3></div>", unsafe_allow_html=True)
    if st.radio("Válasz:", f['opciok']) == f['helyes']: st.success("Helyes!")

elif menupont == "🧭 Tantárgyi Idővonal & Térkép":
    for item in aktiv_timeline:
        st.markdown(f"<div class='timeline-item'><b>{item['ev']}</b>: {item['cim']} - {item['leiras']}</div>", unsafe_allow_html=True)

elif menupont == "🏆 Nagy Próbavizsga":
    st.write("Vizsga indul!") # Itt a kvíz logika
    
elif menupont == "🤖 AI Érettségi Mentor":
    k = st.text_input("Kérdés:")
    if st.button("Küldés"): st.write(ai_generalas(k))
    audio_k = st.audio_input("Hangalapú kérdés:")
    if audio_k: st.write(ai_generalas("Válaszolj a kérdésre", audio_bytes=audio_k.read(), mime_type="audio/wav"))
