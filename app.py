import streamlit as st
import json

# JSON fájl betöltése
def load_data():
    try:
        with open("tananyag.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"Irodalom": [], "Történelem": []}

data = load_data()

st.title("Astra Érettségi - Profi Verzió")
tantargy = st.sidebar.selectbox("Tantárgy", list(data.keys()))

if tantargy:
    valasztott = st.selectbox("Tétel:", [t["cim"] for t in data[tantargy]])
    tetel_adat = next((t for t in data[tantargy] if t["cim"] == valasztott), None)
    
    if tetel_adat:
        st.subheader(tetel_adat["alcim"])
        st.markdown(tetel_adat["vazlat"])
