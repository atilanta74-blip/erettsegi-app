import streamlit as st

# Ez egy teszt adatbázis: 20 tétel, előre megírt, azonnali tartalommal
tetelek_db = {
    "1. Ókori eposzok": {
        "tartalom": "### I. Bevezetés: Az eposz műfaja\nAz eposz nagy terjedelmű, emelkedett stílusú verses epikai mű. Főhőse emberfeletti képességekkel rendelkezik, sorsát istenek irányítják.\n### II. Eposzi kellékek\n- **Invokáció:** Segítségkérés a múzsától.\n- **Propozíció:** A téma megjelölése.\n- **In medias res:** A cselekmény sűrűjébe vágó kezdés.\n### III. Homérosz: Iliász\nTrója ostroma, Akhilleusz haragja. Emberi sorsok és isteni beavatkozás.",
        "szobeli": "Felelj a műfaji sajátosságokról!",
        "kviz": "Igaz-e, hogy az Iliász in medias res kezdődik? (Igen)"
    },
    "2. Shakespeare: Hamlet": {
        "tartalom": "### I. Reneszánsz dráma\nShakespeare a korszak legnagyobb drámaírója. A Hamlet (1601) a drámairodalom egyik csúcsa.\n### II. A Hamlet dilemmája\n'Lenni vagy nem lenni' - az egzisztenciális kérdés. A cselekvésképtelenség és a morális válság összefonódása.\n### III. Szerkezet\nBosszúdráma keretbe ágyazott filozófiai monológok.",
        "szobeli": "Elemezd a híres monológ jelentőségét!",
        "kviz": "Hamlet dán királyfi? (Igen)"
    }
}

st.title("⚡ Astra Villámgyors Teszt")
st.write("Ez a verzió nem vár az AI-ra, azonnal tölti a tartalmat.")

tetel = st.selectbox("Válassz tételt:", list(tetelek_db.keys()))
t_adat = tetelek_db[tetel]

st.markdown(t_adat["tartalom"])
st.info(f"🎙️ Szóbeli tipp: {t_adat['szobeli']}")
st.warning(f"⚡ Kvíz kérdés: {t_adat['kviz']}")
