import streamlit as st

st.set_page_config(page_title="Astra Pro - Részletes Tananyag Teszt", layout="wide")

# Itt már sokkal hosszabb, részletesebb akadémiai kidolgozás szerepel fixen
tetelek_részletes = {
    "1. Ókori eposzok és a Biblia": {
        "alcim": "Homérosz és az európai kultúra alapkövei",
        "tartalom": """
### I. Bevezetés: Az eposz műfaja és antik gyökerei
Az eposz a klasszikus ókori irodalom legnagyobb terjedelmű verses epikai műfaja. Jellemzője az emelkedett stílus, a pátosz, valamint az, hogy a cselekmény egész közösségek, sőt az egész emberiség sorsát befolyásoló események köré épül. A klasszikus eposz elengedhetetlen sajátossága a természetfeletti erők (istenek) aktív beavatkozása a halandók harcaiba.

### II. Eposzi kellékek rendszere
A műfaj szabályait Homérosz teremtette meg, a Kódexek és a későbbi költők (Vergilius, Milton, Zrínyi) ezt követték:
- **Invokáció:** Segítségkérés (általában a múzsák valamelyikétől) a mű megírásához.
- **Propozíció:** A téma megjelölése, a főbb motívumok előrevetítése.
- **In medias res kezdés:** A történet sűrűjébe, a konfliktus közepébe vágó indítás, amely utólagos visszatekintésekkel (retrospektív szerkezet) mutatja be az előzményeket.
- **Enumeráció (Seregszemle):** A szemben álló felek erőinek, hőseinek részletes bemutatása.
- **Csodás elemek:** Isteni beavatkozások, természetfeletti lények jelenléte.

### III. Homérosz: Iliász és Odüsszeia
Az *Iliász* a Trójai háború utolsó évének néhány hetét beszéli el. Középpontjában nem maga Trója bevétele áll, hanem egyetlen morális fordulat: **Akhilleusz haragja** Agamemnónnal szemben, majd annak feloldása Hektór holttestének kiadásakor. Ezzel szemben az *Odüsszeia* a békeidők világába vezet, az egyéni helytállást, a hazatérést és a lelkierőt helyezi előtérbe.

### IV. A Biblia mint kulturális kód
A nyugati civilizáció alapköve az Ó- és Újszövetség. Műfajilag rendkívül vegyes: tartalmaz törvényeket, próféciákat, lírai zsoltárokat (Dávid zsoltárai), evangéliumokat és példabeszédeket (parabolákat). Hatása minden európai irodalmi korszakban tetten érhető.
        """,
        "szobeli": "🎙️ **3 perces felelet vázlata:** 1. Definiáld az eposz fogalmát -> 2. Sorold fel és magyarázd el az eposzi kellékeket -> 3. Hasonlítsd össze az Iliász és az Odüsszeia emberképét.",
        "kviz": [
            {"k": "Az eposz az antik irodalom lírai műfaja.", "v": False, "m": "Nem, az eposz verses epikai (elbeszélő) műfaj."},
            {"k": "Az in medias res azt jelenti, hogy a cselekmény sűrűjébe vágva kezdődik a mű.", "v": True, "m": "Igen, ez az egyik legfontosabb eposzi kellék."}
        ]
    },
    "2. Shakespeare drámái és a Hamlet": {
        "alcim": "A reneszánsz színház, az emberi kétségbeesés és a drámai szerkezet",
        "tartalom": """
### I. Az Erzsébet-kori színház és Shakespeare világa
William Shakespeare (1564–1616) a angol reneszánsz drámairodalom óriása. Műveit a londoni **Globe Színház** számára írta. Drámáiban megbomlik a középkori zárt világkép; a középpontba az individuális (egyéni) ember, a belső vívódások, a morális felelősség és a hatalomvágy kérdései kerülnek.

### II. A Hamlet, dán királyfi szerkezete és konfliktusa
A *Hamlet* (1601) a világdráma egyik legjelentősebb alkotása. 
- **Alaphelyzet:** Hamlet herceg atyját meggyilkolták, a trónust Claudius bitorolja, és Hamlet édesanyját (Gertrúd) is feleségül veszi. A szellem bosszút követel.
- **A drámai konfliktus:** Nem csupán külső (megbosszulni a gyilkosságot Claudiuson), hanem mélyen **belső, egzisztenciális konfliktus**: *„Lenni vagy nem lenni: az a kérdés.”* Hamlet értelmiségi alkat, aki látja a dán udvar rothadását, de képtelen gépiesen cselekedni; megkérdőjelezi a bosszú igazságosságát és a világ erkölcsi rendjét.

### III. Kulcsfontosságú motívumok
- **A színház a színházban (Egérfogó jelenet):** Hamlet színészekkel játszatja el a gyilkosságot, hogy leleplezze Claudiust.
- **A tettek halasztása (Prokrastináció):** Hamlet folyamatosan halogatja a döntést, ami végül mindenkinek a pusztulásához vezet (párbajjelenet, mérgezett tőr és bor).
- **Tragikus hős:** Hamlet magányos gondolkodó, aki messze túllép a hagyományos bosszúdrámák keretein.
        """,
        "szobeli": "🎙️ **3 perces felelet vázlata:** 1. Mutasd be az Erzsébet-kori színházat -> 2. Ismertesd a Hamlet alaphelyzetét -> 3. Elemezd a főhős belső vívódását.",
        "kviz": [
            {"k": "A Hamlet hagyományos, egyszerű bosszúdráma, ahol a hős habozás nélkül cselekszik.", "v": False, "m": "Nem, a Hamlet éppen a tett halasztásáról és a mély filozófiai dilemmákról szól."},
            {"k": "Az 'Egérfogó' jelenetben Hamlet a színészekkel leplezi le a király bűnét.", "v": True, "m": "Igen, ez a dráma egyik kulcsjelenete."}
        ]
    }
}

st.title("⚡ Astra Villámgyors Részletes Tananyag")
st.write("Ez a verzió **azonnal, várakozási idő nélkül** betölti a hosszú, részletes érettségi tételt.")

tetel = st.selectbox("Válassz tételt:", list(tetelek_részletes.keys()))
t_adat = tetelek_részletes[tetel]

st.markdown(f"## {tetel}")
st.caption(t_adat["alcim"])

tab1, tab2, tab3 = st.tabs(["📚 Részletes Akadémiai Tananyag", "🎙️ 3 Perces Felelet", "⚡ Kvíz"])

with tab1:
    # Itt van a részletes tartalom, ami azonnal megjelenik
    st.markdown(f"<div style='background-color:#111827; padding:25px; border-radius:12px; line-height:1.8;'>{t_adat['tartalom']}</div>", unsafe_allow_html=True)

with tab2:
    st.info(t_adat["szobeli"])

with tab3:
    for i, q in enumerate(t_adat["kviz"]):
        st.write(f"**{i+1}. {q['k']}**")
        c1, c2 = st.columns(2)
        if c1.button("✅ Igaz", key=f"t_{i}"): st.success(f"Helyes! {q['m']}")
        if c2.button("❌ Hamis", key=f"f_{i}"): st.error(f"Nem helyes. {q['m']}")
