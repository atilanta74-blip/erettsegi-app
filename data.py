# -------------------------------------------------------------
# ADATBÁZISOK FÁJL (data.py) - Teljes verzió
# -------------------------------------------------------------

tetelek_irodalom = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, nagykőrösi és margitszigeti korszak",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja", "A walesi bárdok"],
        "audio_szoveg": "Arany János a magyar irodalom legnagyobb balladaírója...",
        "vazlat": "### I. Műfajelmélet: Líra, epika és dráma szintézise.\n### II. Nagykőrösi korszak: Történelmi ellenállás és lélektan.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. Nagykőrösi balladák.",
        "kviz": [{"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A három műnem találkozása."}]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus szintézise, polgári meghasonlás és a Senki szigete",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi"],
        "audio_szoveg": "Jókai Mór 1872-es Az arany ember című regénye...",
        "vazlat": "### I. Műfaj: Romantikus mesei fordulatok és realista társadalomrajz.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1872 kontextusa -> 2. Timár jelleme.",
        "kviz": [{"k": "A Senki szigete pénzmentes természeti utópia a regényben.", "v": True, "m": "A társadalmi konvenciókon kívül áll."}]
    }
}

tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, kommunikációs funkciók",
        "kulcsszavak": ["Adó és Vevő", "Kód és Csatorna", "Jakobson modellje"],
        "audio_szoveg": "A kommunikáció információk átadása...",
        "vazlat": "### I. A Jakobson-féle modell: Adó, Vevő, Üzenet, Kód, Csatorna.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A kommunikáció definíciója -> 2. Jakobson modellje.",
        "kviz": [{"k": "A fatikus funkció célja a kapcsolat felvétele és fenntartása.", "v": True, "m": "Ilyenek a köszönések."}]
    }
}

tetelek_tortenelem = {
    "1. Az athéni demokrácia működése a Kr. e. V. században": {
        "alcim": "Szolón, Kleiszthenész reformjai, Periklész kora",
        "kulcsszavak": ["Népgyűlés (Ekklészia)", "Cserépszavazás", "Periklész"],
        "audio_szoveg": "Az athéni demokrácia az ókori világ legfejlettebb rendszere volt...",
        "vazlat": "### I. Fejlődés: Szolón -> Kleiszthenész -> Periklész kora.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kialakulás -> 2. Intézményrendszer.",
        "kviz": [{"k": "Az athéni népgyűlés tagja lehetett minden szabad férfi polgár.", "v": True, "m": "Közvetlen demokrácia volt."}]
    }
}

tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció, kombináció",
        "kulcsszavak": ["Metszet, Unió", "Permutáció", "Kombináció"],
        "audio_szoveg": "A halmazelmélet és a kombinatorika a modern matematika alapjai...",
        "vazlat": "### I. Halmazműveletek és kombinatorikai képletek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Halmazok -> 2. Kombinatorika.",
        "kviz": [{"k": "Az 5-ös lottó kihúzásainak száma kombinációval számítható.", "v": True, "m": "A sorrend nem számít."}]
    }
}

# Villámkártyák (Flashcards) mind a 4 tárgyhoz
flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra, epika és dráma sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a szerkesztője?", "a": "1908-ban indult, Osvát Ernő szerkesztette."}
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
timeline_irodalom = [{"ev": "1848–1849", "cim": "Forradalom lírája", "leiras": "Petőfi és Arany."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihany", "leiras": "Szórványemlék."}]
timeline_tortenelem = [{"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István."}]
timeline_matek = [{"ev": "Kr. e. VI.", "cim": "Pitagorasz", "leiras": "Derékszögű háromszög."}]

# Detektív Játék kérdések
detektiv_irodalom = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Új versek", "Arany János: Toldi", "Radnóti Miklós"], "info": "A felelősségvállalás parancsa."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb...”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János", "Ady Endre"], "info": "Petőfi forradalmi felhívó lírája."}
]
detektiv_nyelvtan = [
    {"idezet": "„barátság [kiejtve: baraccság]”", "helyes": "Összeolvadás mássalhangzótörvény", "opciok": ["Összeolvadás mássalhangzótörvény", "Zöngésségi részleges hasonulás", "Írásban jelölt teljes hasonulás", "Mássalhangzó-kiesés"], "info": "t + s -> [ccs]."},
    {"idezet": "„lila dalra kelt az éjcsend”", "helyes": "Szinesztézia (Költői kép)", "opciok": ["Szinesztézia (Költői kép)", "Megszemélyesítés", "Metonímia", "Szinekdoché"], "info": "Érzékkeverés."}
]
detektiv_tortenelem = [
    {"idezet": "„Ius resistendi (A nemesek joga az ellenállásra)”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Nagy Lajos 1351", "Szent István", "Kollonics"], "info": "Rendi szabadságjog."},
    {"idezet": "„Eb ura fakó, József császár nem királyunk!”", "helyes": "1707-es Ónodi országgyűlés (Trónfosztás)", "opciok": ["1707-es Ónodi országgyűlés (Trónfosztás)", "1849", "1526", "1608"], "info": "Habsburg-trónfosztás."}
]
detektiv_matek = [
    {"idezet": "a² = b² + c² - 2bc · cos(α)", "helyes": "Koszinusztétel (Általános háromszögekre)", "opciok": ["Koszinusztétel (Általános háromszögekre)", "Szinusztétel", "Pitagorasz", "Héron"], "info": "Pitagorasz általánosítása."},
    {"idezet": "(x^n)' = n · x^(n-1)", "helyes": "Hatványfüggvény deriválási szabálya", "opciok": ["Hatványfüggvény deriválási szabálya", "Logaritmus", "Binomiális", "Sorozat"], "info": "Differenciálás."}
]
