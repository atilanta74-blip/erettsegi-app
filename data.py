# data.py

def gener_tetelek(tantargy, temak):
    """Egyedi témákat rendel az egyes tételekhez."""
    return {f"{i+1}. {tema}": {
        "alcim": f"Részletek a(z) {tema} témakörhöz",
        "vazlat": f"### {tema} vázlat\n- Alapfogalmak és összefüggések a tételhez.",
        "szobeli": "🎙️ 3 perces feleletvázlat a vizsgához.",
        "kviz": [{"k": f"Az {tema} témakörhöz kapcsolódó alapvető kérdés?", "v": True, "m": "Helyes válasz és magyarázat."}]
    } for i, tema in enumerate(temak)}

# Itt a teljes lista, mostantól ezek fognak megjelenni a legördülő menüben:
tetelek_irodalom = gener_tetelek("Irodalom", [
    "Ókori eposzok", "Shakespeare drámái", "Balassi Bálint", "Zrínyi Miklós", 
    "Mikes Kelemen", "Csokonai Vitéz Mihály", "Katona József: Bánk bán", 
    "Kölcsey és Vörösmarty", "Petőfi Sándor", "Arany János", "Jókai Mór", 
    "Madách Imre", "Mikszáth Kálmán", "Ady Endre", "Móricz Zsigmond", 
    "Babits Mihály", "Kosztolányi Dezső", "József Attila", "Radnóti Miklós", 
    "Örkény István", "Pilinszky és Nagy László", "Kortárs irodalom"
])

tetelek_nyelvtan = gener_tetelek("Nyelvtan", [
    "Kommunikáció", "Helyesírás alapelvei", "Szófajok rendszere", "Mondattan", 
    "Jelentéstan", "Stilisztika", "Nyelv és társadalom", "Nyelvtörténet",
    "Szövegtan", "Retorika", "Érvelés", "Vita kultúra", "Hivatalos levelek",
    "Sajtónyelv", "Szaknyelvek", "Nyelvi babonák"
])

tetelek_tortenelem = gener_tetelek("Történelem", [
    "Athéni demokrácia", "Honfoglalás", "Szent István", "Aranybulla", 
    "Anjou-kor", "Hunyadiak", "Mohács", "Reformáció", "Rákóczi szabadságharc",
    "Felvilágosult abszolutizmus", "Reformkor", "1848-as forradalom", "Kiegyezés",
    "Dualizmus", "I. világháború", "Trianon", "Horthy-korszak", "II. világháború",
    "Rákosi-korszak", "1956-os forradalom", "Kádár-korszak", "Rendszerváltás",
    "EU csatlakozás", "Hidegháború", "Ipari forradalom", "Kolonializmus",
    "Nacionalizmus", "Liberalizmus", "Totalitárius rendszerek", "Globalizáció"
])

tetelek_matek = gener_tetelek("Matek", [
    "Halmazok", "Logika", "Másodfokú egyenletek", "Függvények",
    "Trigonometria", "Geometria", "Vektorok", "Kombinatorika",
    "Valószínűségszámítás", "Sorozatok", "Hatványozás", "Logaritmus",
    "Differenciálszámítás", "Integrálszámítás", "Statistika", "Pénzügyi matek"
])
