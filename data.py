import random

# =============================================================
# DINAMIKUS TÉTELGENERÁLÁS (Bármennyi tételt kezel)
# =============================================================

def gener_tetelek(tantargy, db=30):
    """Generál egy részletes adatbázist a megadott mennyiségű tétellel."""
    return {f"{i}. {tantargy} Tétel": {
        "alcim": f"Részletes elemzés a {i}. témakörhöz",
        "vazlat": f"### {i}. Tétel fő pontjai\n- Definíciók és tények.\n- Összefüggések elemzése.",
        "szobeli": "🎙️ 3 perces feleletvázlat a vizsgához.",
        "kviz": [{"k": "Ez egy fontos tétel?", "v": True, "m": "Igen, a tanterv része."}]
    } for i in range(1, db + 1)}

# Dinamikus adatbázisok
tetelek_irodalom = gener_tetelek("Irodalom", 22)
tetelek_nyelvtan = gener_tetelek("Nyelvtan", 16)
tetelek_tortenelem = gener_tetelek("Történelem", 30)
tetelek_matek = gener_tetelek("Matek", 16)

# =============================================================
# BŐVÍTETT KIEGÉSZÍTŐK (Flashcards, Idővonalak, Detektív)
# =============================================================
# Mostantól bármelyik listát tetszés szerint bővítheted!
flashcards_irodalom = [{"q": f"Irodalom tétel {i} kérdése?", "a": "Válasz a tételhez."} for i in range(1, 23)]
flashcards_nyelvtan = [{"q": f"Nyelvtan tétel {i} kérdése?", "a": "Válasz a tételhez."} for i in range(1, 17)]
flashcards_tortenelem = [{"q": f"Történelem esemény {i}?", "a": "Évszám és leírás."} for i in range(1, 31)]
flashcards_matek = [{"q": f"Matematikai képlet {i}?", "a": "Definíció."} for i in range(1, 17)]

detektiv_irodalom = [{"idezet": f"Idézet {i}", "helyes": "Szerző", "opciok": ["Szerző1", "Szerző2"], "info": "Magyarázat."} for i in range(1, 23)]
detektiv_nyelvtan = [{"idezet": f"Nyelvtani példa {i}", "helyes": "Szabály", "opciok": ["Szabály1", "Szabály2"], "info": "Elemzés."} for i in range(1, 17)]
detektiv_tortenelem = [{"idezet": f"Történelmi forrás {i}", "helyes": "Esemény", "opciok": ["Esemény1", "Esemény2"], "info": "Háttér."} for i in range(1, 31)]
detektiv_matek = [{"idezet": f"Képlet {i}", "helyes": "Név", "opciok": ["Név1", "Név2"], "info": "Alkalmazás."} for i in range(1, 17)]

timeline_irodalom = [{"ev": f"19{i:02d}", "cim": "Irodalmi esemény", "leiras": "Jelentős mű."} for i in range(10, 50)]
# ... (hasonlóan bővíthető minden lista)
