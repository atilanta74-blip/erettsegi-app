import streamlit as st

st.set_page_config(page_title="Astra Pro - Jól Olvasható", layout="wide")

# --- JAVÍTOTT, KONTRASTOS STÍLUS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e5e7eb; }
    
    /* A részletes tananyag doboza: Világosabb háttérrel, tiszta fehér szöveggel */
    .deep-text { 
        background-color: #111827; 
        color: #ffffff !important; 
        padding: 30px; 
        border-radius: 15px; 
        border: 1px solid #374151;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    /* Fejlécek a szövegben legyenek kontrasztosak */
    .deep-text h3 { color: #818cf8 !important; }
    
    /* Általános szöveg a dobozon kívül */
    p, div { color: #d1d5db !important; }
    
    /* Tabok betűszíne */
    button[data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    
</style>
""", unsafe_allow_html=True)

# Teszt adat
tetelek_részletes = {
    "1. Ókori eposzok": {
        "tartalom": """
### I. Bevezetés: Az eposz műfaja
Az eposz nagy terjedelmű, emelkedett stílusú verses epikai mű. Főhőse emberfeletti képességekkel rendelkezik.

### II. Eposzi kellékek
- **Invokáció:** Segítségkérés a múzsától.
- **In medias res:** A cselekmény sűrűjébe vágó kezdés.
        """
    }
}

tetel = st.selectbox("Válassz tételt:", list(tetelek_részletes.keys()))
t_adat = tetelek_részletes[tetel]

# A kategória (tab) nézete a javított CSS-sel
st.markdown(f"<div class='deep-text'>{t_adat['tartalom']}</div>", unsafe_allow_html=True)
