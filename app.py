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

st.set_page_config(page_title="Érettségi Felkészítő Központ - Edited by Nagy Attila", page_icon="🎓", layout="wide")

def get_api_key():
    if "GEMINI_API_KEY" in st.secrets: return st.secrets["GEMINI_API_KEY"].strip()
    return os.environ.get("GEMINI_API_KEY", "")

# Stílusok
st.markdown("""<style>
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    .stSidebar { background-color: #111827 !important; }
    p, label, span, .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: #f3f4f6 !important; }
    .stButton>button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; font-weight: 700 !important; border-radius: 10px !important; }
    .topic-card { background-color: #1f2937; border: 1px solid #374151; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .flashcard { background: linear-gradient(135deg, #1e1b4b, #31104b); border: 2px solid #818cf8; border-radius: 16px; padding: 35px; text-align: center; min-height: 180px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
    .chat-user { background-color: #4f46e5; color: white; padding: 12px; border-radius: 16px; margin-left: auto; width: fit-content; }
    .chat-ai { background-color: #1f2937; color: #f3f4f6; padding: 12px; border-radius: 16px; width: fit-content; }
</style>""", unsafe_allow_html=True)

# ADATBÁZISOK
tetelek_irodalom = {
    "1. Arany János balladái": {"alcim": "Balladaelmélet", "kulcsszavak": ["Ballada"], "vazlat": "### I. Műfaj: Líra, epika, dráma.", "szobeli": "3 perces felelet...", "kviz": [{"k": "Greguss elnevezése igaz?", "v": True, "m": "Tragédia dalban."}]},
    "2. Jókai Mór: Az arany ember": {"alcim": "Romantika és realizmus", "kulcsszavak": ["Timár"], "vazlat": "### I. Kettős világ.", "szobeli": "Timár sorsa.", "kviz": [{"k": "Timea szerelmi házasság?", "v": False, "m": "Hálából."}]},
    "3. Madách: Az ember tragédiája": {"alcim": "Drámai költemény", "kulcsszavak": ["Ádám"], "vazlat": "### I. 15 szín.", "szobeli": "Eszmék harca.", "kviz": [{"k": "15 szín?", "v": True, "m": "Igen."}]},
    "4. Mikszáth: Próza": {"alcim": "Anekdotizmus", "kulcsszavak": ["Mikszáth"], "vazlat": "### I. Tót atyafiak.", "szobeli": "Anekdota.", "kviz": [{"k": "Tót atyafiak?", "v": True, "m": "Igen."}]},
    "5. Vajda János": {"alcim": "Magány", "kulcsszavak": ["Vajda"], "vazlat": "### I. Magány.", "szobeli": "Gina.", "kviz": [{"k": "Montblanc?", "v": True, "m": "Igen."}]},
    "6. Ibsen és Csehov": {"alcim": "Dráma", "kulcsszavak": ["Dráma"], "vazlat": "### I. Analitikus.", "szobeli": "Csehov.", "kviz": [{"k": "Nóra?", "v": True, "m": "Igen."}]},
    "7. Nyugat": {"alcim": "1908", "kulcsszavak": ["Nyugat"], "vazlat": "### I. 3 nemzedék.", "szobeli": "Szerkesztők.", "kviz": [{"k": "1908?", "v": True, "m": "Igen."}]},
    "8. Ady Endre": {"alcim": "Szimbolizmus", "kulcsszavak": ["Ady"], "vazlat": "### I. Új versek.", "szobeli": "Léda.", "kviz": [{"k": "1906?", "v": True, "m": "Igen."}]},
    "9. Babits": {"alcim": "Jónás", "kulcsszavak": ["Babits"], "vazlat": "### I. 1938.", "szobeli": "Felelősség.", "kviz": [{"k": "Cinkos?", "v": True, "m": "Igen."}]},
    "10. Móricz": {"alcim": "Naturalizmus", "kulcsszavak": ["Móricz"], "vazlat": "### I. Barbárok.", "szobeli": "Parasztok.", "kviz": [{"k": "Barbárok?", "v": True, "m": "Igen."}]},
    "11. Kosztolányi": {"alcim": "Anna", "kulcsszavak": ["Anna"], "vazlat": "### I. 1919.", "szobeli": "Lélektan.", "kviz": [{"k": "Anna?", "v": True, "m": "Igen."}]},
    "12. Petőfi": {"alcim": "Látomás", "kulcsszavak": ["Petőfi"], "vazlat": "### I. XIX. sz.", "szobeli": "Nemzeti dal.", "kviz": [{"k": "1848?", "v": True, "m": "Igen."}]},
    "13. József Attila": {"alcim": "Lét", "kulcsszavak": ["József A"], "vazlat": "### I. Dunánál.", "szobeli": "Eszmélet.", "kviz": [{"k": "Dunánál?", "v": True, "m": "Igen."}]},
    "14. Radnóti": {"alcim": "Ecloga", "kulcsszavak": ["Radnóti"], "vazlat": "### I. Bori.", "szobeli": "Razglednicák.", "kviz": [{"k": "Bori notesz?", "v": True, "m": "Igen."}]},
    "15. Vörösmarty": {"alcim": "Romantika", "kulcsszavak": ["Vörösmarty"], "vazlat": "### I. Csongor.", "szobeli": "Szózat.", "kviz": [{"k": "1836?", "v": True, "m": "Igen."}]},
    "16. Csokonai": {"alcim": "Felvilágosodás", "kulcsszavak": ["Csokonai"], "vazlat": "### I. Lilla.", "szobeli": "Remény.", "kviz": [{"k": "Reményhez?", "v": True, "m": "Igen."}]},
    "17. Berzsenyi": {"alcim": "Óda", "kulcsszavak": ["Berzsenyi"], "vazlat": "### I. Magyarokhoz.", "szobeli": "Tél.", "kviz": [{"k": "Tölgy?", "v": True, "m": "Igen."}]},
    "18. Zrínyi": {"alcim": "Barokk", "kulcsszavak": ["Zrínyi"], "vazlat": "### I. Szigeti.", "szobeli": "Athleta.", "kviz": [{"k": "15 ének?", "v": True, "m": "Igen."}]},
    "19. Örkény": {"alcim": "Groteszk", "kulcsszavak": ["Örkény"], "vazlat": "### I. Tóték.", "szobeli": "Egyperces.", "kviz": [{"k": "Tóték?", "v": True, "m": "Igen."}]},
    "20. Ottlik": {"alcim": "Iskola", "kulcsszavak": ["Ottlik"], "vazlat": "### I. Iskola.", "szobeli": "Kőszeg.", "kviz": [{"k": "Határ?", "v": True, "m": "Igen."}]},
    "21. Krúdy": {"alcim": "Szindbád", "kulcsszavak": ["Krúdy"], "vazlat": "### I. Idő.", "szobeli": "Szecesszió.", "kviz": [{"k": "Szindbád?", "v": True, "m": "Igen."}]},
    "22. Illyés": {"alcim": "Zsarnokság", "kulcsszavak": ["Illyés"], "vazlat": "### I. Puszták.", "szobeli": "Zsarnokság.", "kviz": [{"k": "Egy mondat?", "v": True, "m": "Igen."}]}
}

# (Itt folytatódna a Nyelvtan, Történelem és Matek adatbázis definiálása hasonló módon...)
# A helyhiány miatt a továbbiakban csak a logika marad.
