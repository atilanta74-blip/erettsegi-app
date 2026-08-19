elif menupont == "🎭 Tantárgyi Detektív Játék":
    st.title(f"🎭 {tantargy_cimke} Detektív Játék")
    st.caption(f"Felismered a legfontosabb {tantargy_cimke} idézeteket, forrásokat és képleteket?")
    
    # Ha még nincs kiválasztva kérdés a session-ben, inicializáljuk
    if 'detektiv_index' not in st.session_state:
        st.session_state.detektiv_index = 0
    
    # Biztonságos határkezelés
    st.session_state.detektiv_index = st.session_state.detektiv_index % len(aktiv_detektiv)
    idx = st.session_state.detektiv_index
    
    f = aktiv_detektiv[idx]
    
    # Haladási sáv
    st.progress((idx + 1) / len(aktiv_detektiv))
    st.write(f"Feladvány: **{idx + 1} / {len(aktiv_detektiv)}**")
    
    # Véletlenszerű keverés a válaszokhoz
    random.seed(idx + 99) # Hogy ne változzon meg ugrálás közben
    kevert_opciok = f['opciok'].copy()
    random.shuffle(kevert_opciok)
    
    st.markdown(f"""
    <div class='topic-card' style='border-color:#ec4899; text-align:center;'>
        <h3 style='color:#f472b6; font-style:italic;'>{f['idezet']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    valasztott_tipp = st.radio("Válaszd ki a helyes megfejtést:", kevert_opciok, index=None, key=f"detektiv_radio_{idx}")
    
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        if st.button("🔍 Tipp ellenőrzése", use_container_width=True):
            if valasztott_tipp is None:
                st.warning("Kérlek, válassz egy választ először!")
            elif valasztott_tipp == f['helyes']:
                st.balloons()
                st.session_state.xp += 30
                st.success(f"TÖKÉLETES! 🎉 Helyes válasz! (+30 XP)\n\n📌 Magyarázat: {f['info']}")
            else:
                st.error(f"Sajnos nem! ❌ A helyes válasz: **{f['helyes']}**\n\n📌 Magyarázat: {f['info']}")
                
    with col_d2:
        if st.button("➡️ Következő feladvány", use_container_width=True):
            st.session_state.detektiv_index += 1
            st.rerun()
