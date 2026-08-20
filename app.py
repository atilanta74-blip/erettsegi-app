import io
import os
import random
import streamlit as st
import datetime
from google import genai
from gtts import gTTS
import PyPDF2
import docx

# ... (stílusok és a db marad változatlan) ...

def read_file(uploaded_file):
    """Kivonatolja a szöveget a feltöltött fájlból."""
    text = ""
    try:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        else: # TXT vagy egyéb
            text = uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        text = f"Hiba a fájl olvasásakor: {e}"
    return text

# ... a get_api_key és generalo_tetelek változatlan ...

# --- MODULOK JAVÍTOTT FÁJLKEZELÉSSEL ---
elif menupont == "📂 Saját Fájlok & Képek":
    st.subheader("📂 Dokumentum és Kép AI Elemzés")
    fajl = st.file_uploader("Fájl feltöltése", type=["txt", "pdf", "docx", "jpg", "jpeg", "png"])
    
    if fajl and st.button("🚀 Elemzés"):
        with st.spinner("Fájl olvasása és elemzése folyamatban..."):
            szoveg = read_file(fajl)
            if szoveg:
                st.write("### Elemzés eredménye:")
                eredmeny = ai_generalas(f"Elemezd az alábbi tananyagot és készíts belőle részletes, érettségire felkészítő összefoglalót: {szoveg[:10000]}") # 10k karakter limit
                st.markdown(eredmeny)
            else:
                st.error("Nem sikerült szöveget kivonatolni a fájlból.")

# ... a többi kód változatlan ...
