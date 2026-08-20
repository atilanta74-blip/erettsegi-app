import io
import streamlit as st
from gtts import gTTS

# --- SZAKMAI HANGOSKÖNYV ADATBÁZIS (Minden tételhez egyedi!) ---
hangoskonyv_adatbazis = {
    "1. Ókori eposzok és a Biblia": "Az ókori eposz az emberiség hőskorszakát idézi meg. Homérosz Iliásza a trójai háború egy rövid szakaszát, az Akhilleusz-haragot helyezi középpontba, míg az Odüsszeia a hazatérés és a próbatételek eposza. A Biblia, mint kulturális kód, a nyugati civilizáció alapja, az Ószövetség a teremtésmítoszokkal és törvényekkel, az Újszövetség pedig az evangéliumok és a krisztusi tanítások révén formálta az európai irodalmat és művészetet.",
    "2. Shakespeare drámái": "Shakespeare a drámaírás csúcsait képviseli. Drámái a reneszánsz emberképét, a hatalom, a szerelem, a féltékenység és a bosszú örök emberi dilemmáit járják körül. A Hamlet a cselekvésképtelenség drámája, a Macbeth a hatalomvágy bukása, a Rómeó és Júlia pedig a tragikus szerelem archetípusa.",
    "11. Jókai Mór regényei": "Jókai Mór a 19. századi magyar romantika legnagyobb alakja. Regényei, mint az Arany ember vagy a Kőszívű ember fiai, egyedi képzeletvilággal, gazdag cselekményszövéssel és gyakran idealizált hősökkel ábrázolják a magyar történelmet és a polgárosodó társadalmat. Művészete a mesélőkedv és a nemzeti romantika ötvözete.",
    # Itt folytathatod a listát a többi tétellel...
}

# --- A HANGOSKÖNYV MODUL JAVÍTÁSA ---
elif menupont == "🎧 Hangoskönyv (Lényegretörő)":
    st.subheader("🎧 Szakmai Hangoskönyv")
    t_nev = st.selectbox("Válassz tételt:", list(aktiv_tetelek.keys()))
    
    # Ha a tétel benne van az adatbázisban, használjuk azt, különben generálunk egyet
    tartalom = hangoskonyv_adatbazis.get(t_nev, f"Ez a tétel a {t_nev} témakörhöz tartozik. A szakmai kifejtéshez kérj részletes esszét az AI Mentortól!")
    
    st.info("⚡ A hangoskönyv a tétel **szakmai lényegét** tartalmazza, sallangok nélkül.")
    
    if st.button("▶️ Lejátszás"):
        tts = gTTS(text=tartalom, lang='hu', slow=False)
        f = io.BytesIO()
        tts.write_to_fp(f)
        f.seek(0)
        st.audio(f, format="audio/mp3")
        st.write(f"**Hallgatott anyag:** {tartalom}")
