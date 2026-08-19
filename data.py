# -------------------------------------------------------------
# ADATBÁZISOK FÁJL (data.py)
# -------------------------------------------------------------

tetelek_irodalom = {
    "1. Arany János balladái": {
        "alcim": "A ballada műfajelmélete, nagykőrösi és margitszigeti korszak",
        "kulcsszavak": ["Tragédia dalban elbeszélve", "Nagykőrös", "Őszikék", "Ágnes asszony", "Szondi két apródja", "A walesi bárdok"],
        "audio_szoveg": "Arany János a magyar irodalom legnagyobb balladaírója. A műfajt Greguss Ágost nyomán tragédia dalban elbeszélveként határozzuk meg...",
        "vazlat": "### I. Műfajelmélet: Líra, epika és dráma szintézise, balladai homály, ellipszis, sűrítés.\n### II. Nagykőrösi korszak: Történelmi ellenállás (A walesi bárdok, Szondi két apródja) és lélektan (Ágnes asszony lepedőmosása).\n### III. Őszikék (1877): Híd-avatás (nagyvárosi haláltánc).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Definíció -> 2. Nagykőrösi történelmi és lélektani balladák -> 3. Őszikék haláltánca -> 4. Összegzés.",
        "kviz": [{"k": "A balladát Greguss Ágost 'tragédia dalban elbeszélve' névvel illette.", "v": True, "m": "A három műnem találkozására utal."}]
    },
    "2. Jókai Mór: Az arany ember": {
        "alcim": "Romantika és realizmus szintézise, polgári meghasonlás és a Senki szigete",
        "kulcsszavak": ["Timár Mihály", "Senki szigete", "Timea és Noémi", "Ali Csorbadzsi", "Krisztyán Tódor"],
        "audio_szoveg": "Jókai Mór 1872-es Az arany ember című regénye az író legszemélyesebb alkotása...",
        "vazlat": "### I. Műfaj: Romantikus mesei fordulatok és realista társadalomrajz.\n### II. Timár meghasonlása: Anyagi siker vs. belső boldogtalanság.\n### III. Kettős világ: Komárom (Timea hideg hálája) vs. Senki szigete (Noémi tiszta szerelme).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1872 kontextusa -> 2. Timár jelleme -> 3. Két világmodell -> 4. Balatoni feloldás.",
        "kviz": [{"k": "A Senki szigete pénzmentes természeti utópia a regényben.", "v": True, "m": "A társadalmi konvenciókon kívül áll."}]
    },
    "3. Madách Imre: Az ember tragédiája": {
        "alcim": "A drámai költemény műfaja, eszmék küzdelme és az Úr zárszava",
        "kulcsszavak": ["Drámai költemény", "15 szín", "Ádám, Éva, Lucifer", "Párizs", "London"],
        "audio_szoveg": "Madách Imre Az ember tragédiája című drámai költeménye 1859-60-ban született...",
        "vazlat": "### I. Műfaj: Világdráma hegel-i dialektikával.\n### II. Karakterek: Ádám (hit és tett), Lucifer (hideg ráció), Éva (élet és érzelem).\n### III. Történelem: Párizs (Danton hite) és London (haláltánc). Zárszó: „Küzdj és bízva bízzál!”",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Műfaji sajátosságok -> 2. Szereplők hármassága -> 3. Párizsi és londoni szín -> 4. 15. szín katarzisa.",
        "kviz": [{"k": "Ádám a párizsi színből kiábrándultan ébred fel.", "v": False, "m": "Párizs az egyetlen szín, amiből Ádám hittel tér magához."}]
    },
    "4. Mikszáth Kálmán prózája": {
        "alcim": "Anekdotizmus, A tót atyafiak, A jó palócok és a Beszterce ostroma",
        "kulcsszavak": ["Anekdota", "A tót atyafiak", "A jó palócok", "Beszterce ostroma", "Pongrácz István"],
        "audio_szoveg": "Mikszáth Kálmán a 19. és 20. század fordulójának legnagyobb magyar mesélője...",
        "vazlat": "### I. Stílus: Anekdotizmus, szelíd irónia.\n### II. Novellák: A tót atyafiak vs. A jó palócok.\n### III. Beszterce ostroma: Pongrácz István Don Quijote-i alakja.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Anekdotikus stílus -> 2. Két novelláskötet -> 3. Pongrácz István -> 4. Összegzés.",
        "kviz": [{"k": "Pongrácz István középkori lovagként rendezi be életét Nedec várában.", "v": True, "m": "Anakronisztikus figura."}]
    },
    "5. Vajda János költészete": {
        "alcim": "A lírai magány mítosza, a Gina-szerelem és a szimbolizmus előfutára",
        "kulcsszavak": ["Gina-versek", "Montblanc", "A vaáli erdőben", "A virrasztók"],
        "audio_szoveg": "Vajda János a kiegyezés korának legmagányosabb költője...",
        "vazlat": "### I. Magány és társadalmi kiábrándulás (A virrasztók).\n### II. Gina-líra: Húsz év múlva (Montblanc-metafora).\n### III. Csend-líra: A vaáli erdőben.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevezetés -> 2. Gina-szerelem -> 3. A vaáli erdőben -> 4. Hatása Adyra.",
        "kviz": [{"k": "A Montblanc-metafora a Húsz év múlva című költemény központi képe.", "v": True, "m": "A fagyos hegy és a belső tűz képe."}]
    },
    "6. XIX. századi dráma: Ibsen és Csehov": {
        "alcim": "Az analitikus dráma (Nóra) és a csehovi hangulatdráma (Sirály, Cseresznyéskert)",
        "kulcsszavak": ["Henrik Ibsen", "Analitikus dráma", "Nóra", "Anton Csehov", "Sirály"],
        "audio_szoveg": "A 19. század végén Henrik Ibsen analitikus drámája és Anton Csehov hangulatdrámája forradalmasította a színházat...",
        "vazlat": "### I. Ibsen: Analitikus technika (Nóra).\n### II. Csehov: Hangulatdráma, cselekvésképtelenség (Sirály).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Polgári dráma megújulása -> 2. Ibsen analitikája -> 3. Csehov atmoszférája -> 4. Hatás.",
        "kviz": [{"k": "Ibsen darabjaiban a múltban rejtőző titkok robbantják ki a konfliktust.", "v": True, "m": "Ez az analitikus dramaturgia lényege."}]
    },
    "7. A Nyugat folyóirat": {
        "alcim": "A modern magyar irodalom indulása 1908-ban, szerkesztők és a 3 nemzedék",
        "kulcsszavak": ["1908", "Osvát Ernő", "Ignotus", "Mikes-emlékérem", "Három nemzedék"],
        "audio_szoveg": "1908. január 1-jén indult a Nyugat folyóirat...",
        "vazlat": "### I. Indulás: 1908–1941; Mikes-emlékérem.\n### II. Szerkesztők: Ignotus, Osvát Ernő, Hatvany Lajos.\n### III. Nemzedékek: 1. nemzedék (Ady, Babits), 2. nemzedék (Szabó Lőrinc), 3. nemzedék (Radnóti).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1908 jelentősége -> 2. Osvát Ernő -> 3. Három nemzedék -> 4. Kánonképző hatás.",
        "kviz": [{"k": "A Nyugat folyóirat 1908 és 1941 között működött.", "v": True, "m": "Babits haláláig állt fenn."}]
    },
    "8. Ady Endre költészete": {
        "alcim": "Szimbolizmus, magyarságtudat, lírai párharc és háborús apokalipszis",
        "kulcsszavak": ["Új versek 1906", "A magyar Ugaron", "Léda vs. Csinszka", "Harc a Nagyúrral"],
        "audio_szoveg": "Ady Endre 1906-os Új versek című kötetével megteremtette a modern magyar szimbolista költészetet...",
        "vazlat": "### I. 1906: Új versek (Góg és Magóg...).\n### II. Témák: Ugar-versek, Pénz-versek, Szerelem (Léda vs. Csinszka).\n### III. Háborús líra: Ember az embertelenségben.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1906 költői forradalma -> 2. Ugar és Disznófejű Nagyúr toposz -> 3. Léda és Csinszka -> 4. Háborús versek.",
        "kviz": [{"k": "Ady korszakalkotó kötete az Új versek 1906-ban jelent meg.", "v": True, "m": "Ez nyitotta meg a modern magyar lírát."}]
    },
    "9. Babits Mihály: Jónás könyve": {
        "alcim": "A prófétai szerep, a morális felelősségvállalás és a Jónás imája",
        "kulcsszavak": ["Jónás könyve", "Jónás imája", "Ninive", "Cinkos, aki néma", "1938"],
        "audio_szoveg": "Babits Mihály 1938-ban írta meg a Jónás könyvét a gégerákja és a fasizmus fenyegetése idején...",
        "vazlat": "### I. 1938: Babits betegsége és a fasizmus fenyegetése; bibliai parafrázis.\n### II. Jónás útja: Menekülés -> Cethal -> Ninive intése.\n### III. Alaptétel: „Mert vétkesek közt cinkos, aki néma.”",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1938 válsága -> 2. Jónás esendősége -> 3. Morális parancs -> 4. Jónás imája.",
        "kviz": [{"k": "A Jónás könyve központi szállóigéje: 'Mert vétkesek közt cinkos, aki néma'.", "v": True, "m": "A felelősségvállalás parancsa."}]
    },
    "10. Móricz Zsigmond prózája": {
        "alcim": "A paraszti és dzsentri világ naturalista és kritikai ábrázolása (Tragédia, Barbárok, Úri muri)",
        "kulcsszavak": ["Naturalizmus", "Tragédia", "Barbárok", "Úri muri", "Szakhmáry Zoltán"],
        "audio_szoveg": "Móricz Zsigmond szakított a hamis népi idillel, és a valóságot a maga kíméletlen ösztönvilágában mutatta be...",
        "vazlat": "### I. Stílus: Naturalizmus, biológiai ösztönök.\n### II. Novellák: Tragédia (Kis János evése), Barbárok (pusztai gyilkosság).\n### III. Dzsentri válság: Úri muri (Szakhmáry Zoltán).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szakítás a népiességgel -> 2. Kis János és Barbárok -> 3. Úri muri -> 4. Összegzés.",
        "kviz": [{"k": "A Tragédia című novellában Kis János a lakodalmi evésbe pusztul bele.", "v": True, "m": "A zsíros hús jelenti vesztét."}]
    },
    "11. Kosztolányi Dezső: Édes Anna": {
        "alcim": "A lélektani regény, a megalázottság tudattalan robbanása és a humanizmus",
        "kulcsszavak": ["Édes Anna", "Vizy család", "Moviszter doktor", "1919", "Freudizmus"],
        "audio_szoveg": "Kosztolányi Dezső 1926-os Édes Anna című regénye az elfojtott sérelmek kitörésének lélektani remekműve...",
        "vazlat": "### I. Történelem: 1919 nyara; Freud lélektana.\n### II. Anna dehumanizálása: Mintagépként kezelik -> Kettős gyilkosság.\n### III. Moviszter doktor: A tiszta humanizmus hangja.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1919 történelmi kerete -> 2. Anna tárgyiasítása -> 3. A gyilkosság lélektana -> 4. Moviszter üzenete.",
        "kviz": [{"k": "Moviszter doktor az egyetlen, aki emberi részvéttel tekint Annára.", "v": True, "m": "Ő képviseli az író értékrendjét."}]
    },
    "12. Petőfi Sándor forradalmi látomásköltészete": {
        "alcim": "A romantikus látomáslíra, a világforradalom és az önfeláldozás mítosza",
        "kulcsszavak": ["Egy gondolat bánt engemet...", "A XIX. század költői", "Világforradalom"],
        "audio_szoveg": "Petőfi Sándor költészetében a forradalmi látomáslíra a népszabadság küzdelmének legmagasabb szintézise...",
        "vazlat": "### I. Prófétai szerep: A XIX. század költői (a költő mint a nép vezére).\n### II. Halálmítosz: Egy gondolat bánt engemet... (önfeláldozás a csatamezőn).\n### III. Politikai líra: Nemzeti dal.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Petőfi forradalmi szerepe -> 2. A XIX. század költői -> 3. Egy gondolat bánt engemet -> 4. Nemzeti dal.",
        "kviz": [{"k": "Petőfi 'Egy gondolat bánt engemet...' című versében a lassú halált kívánja elkerülni.", "v": True, "m": "A csatamezőn kívánt elesni."}]
    },
    "13. József Attila kései gondolati lírája": {
        "alcim": "A létösszegzés, a magány és a társadalmi felelősségvállalás versei",
        "kulcsszavak": ["A Dunánál", "Eszmélet", "Téli éjszaka", "Kései sirató"],
        "audio_szoveg": "József Attila a 20. századi magyar költészet legmélyebb filozófiai gondolkodója...",
        "vazlat": "### I. Történelemfilozófia: A Dunánál (közép-európai megbékélés).\n### II. Lételmélet: Eszmélet (szabadság és determináció).\n### III. Önmegszólító líra: Karóval jöttél...",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Élethelyzet a 30-as években -> 2. A Dunánál megbékélése -> 3. Eszmélet -> 4. Kései önmegszólítás.",
        "kviz": [{"k": "A Dunánál a közép-európai népek megbékélését hirdeti.", "v": True, "m": "„Békévé oldja az emlékezés.”"}]
    },
    "14. Radnóti Miklós háborús ecloga-költészete": {
        "alcim": "A klasszicizáló forma mint a barbárság elleni menedék a bori noteszben",
        "kulcsszavak": ["Eclogák", "Bori notesz", "Hetedik ecloga", "Razglednicák"],
        "audio_szoveg": "Radnóti Miklós a második világháború borzalmai közepette a klasszikus antik forma fegyelmével őrizte meg a humánumot...",
        "vazlat": "### I. Antik forma: Vergiliusi hexameteres eclogák.\n### II. Lágerköltészet: Hetedik ecloga, Erőltetett menet.\n### III. Bori notesz: Razglednicák (a halálmenet stációi).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszicizálódás -> 2. Ecloga műfaj -> 3. Razglednicák -> 4. Humanizmus győzelme.",
        "kviz": [{"k": "Radnóti Miklós utolsó verseit a bori noteszben találták meg.", "v": True, "m": "A tömegsírból került elő."}]
    },
    "15. Vörösmarty Mihály: Csongor és Tünde és a Szózat": {
        "alcim": "A romantikus mesejáték filozófiája és a nemzeti identitás kiáltványa",
        "kulcsszavak": ["Csongor és Tünde", "Szózat (1836)", "Éj monológja"],
        "audio_szoveg": "Vörösmarty Mihály a magyar romantika vezéralakja...",
        "vazlat": "### I. Csongor és Tünde: Boldogságkeresés, Három vándor, Éj monológja.\n### II. Szózat (1836): A nemzet kiáltványa, hűség a hazához.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Romantika -> 2. Csongor és Tünde filozófiája -> 3. Éj monológja -> 4. Szózat.",
        "kviz": [{"k": "Az Éj monológja a világmindenség múlandóságát hirdeti.", "v": True, "m": "„Sötét és semmi voltam...”"}]
    },
    "16. Csokonai Vitéz Mihály felvilágosult lírája": {
        "alcim": "Stíluskettősség: klasszicizmus, rokokó és szentimentalizmus a Lilla-versekben",
        "kulcsszavak": ["A Reményhez", "A Magánossághoz", "Konstancinápoly", "Lilla-ciklus"],
        "audio_szoveg": "Csokonai Vitéz Mihály a magyar felvilágosodás legtehetségesebb poétája...",
        "vazlat": "### I. Filozofikus költészet: Konstancinápoly, Az estve.\n### II. Rokokó: Lilla-dalok.\n### III. Szentimentalizmus: A Reményhez, A Magánossághoz.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Felvilágosodás -> 2. Filozofikus versek -> 3. Lilla-líra -> 4. Stílusszintézis.",
        "kviz": [{"k": "A Reményhez a szentimentális kiábrándultság remeke.", "v": True, "m": "Búcsú a reménytől."}]
    },
    "17. Berzsenyi Dániel ódaköltészete": {
        "alcim": "A klasszicista forma és a romantikus életérzés feszültsége a niklai magányban",
        "kulcsszavak": ["A magyarokhoz I.", "A közelítő tél", "Nikla"],
        "audio_szoveg": "Berzsenyi Dániel a niklai remeteségből küldte el lángoló ódáit...",
        "vazlat": "### I. Nemzetféltő ódák: A magyarokhoz I. (tölgy-metafora).\n### II. Elégico-óda: A közelítő tél (elmúlás).\n### III. Horatiusi bölcselet: Osztályrészem.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszicista forma és romantikus lélek -> 2. A magyarokhoz I. -> 3. A közelítő tél -> 4. Nikla.",
        "kviz": [{"k": "A magyarokhoz I. című versben a tölgy a magyar nemzet szimbóluma.", "v": True, "m": "A belső erkölcsi pusztulás veszélyére int."}]
    },
    "18. Zrínyi Miklós: Szigeti veszedelem": {
        "alcim": "A barokk eposz sajátosságai, a mártíromság és az athleta Christi eszménye",
        "kulcsszavak": ["Barokk eposz", "Szigeti veszedelem (1651)", "Athleta Christi"],
        "audio_szoveg": "Zrínyi Miklós 1651-ben írta meg a Szigeti veszedelmet dédapja hősi haláláról...",
        "vazlat": "### I. Eposzi kellékek: Invocatio, Propositio, Csodás elemek.\n### II. Teológia: Isten büntetése a bűnökért a török hódítás.\n### III. Zrínyi: Athleta Christi vértanúsága.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Barokk eposz -> 2. Szigetvár ostroma -> 3. Athleta Christi -> 4. Üzenet.",
        "kviz": [{"k": "A Szigeti veszedelem 15 énekből álló barokk eposz.", "v": True, "m": "1651-ben íródott."}]
    },
    "19. Örkény István: Tóték és az egypercesek": {
        "alcim": "A groteszk és az abszurd ábrázolásmódja a 20. századi diktatúrák árnyékában",
        "kulcsszavak": ["Groteszk", "Tóték (1967)", "Őrnagy és Tót", "Dobozolás"],
        "audio_szoveg": "Örkény István a magyar groteszk próza megteremtője...",
        "vazlat": "### I. Groteszk: Félelmetes és nevetséges egyidejűsége.\n### II. Tóték (1967): Őrnagy terrorja, éjszakai dobozolás, margóvágós végkifejlet.\n### III. Egyperces novellák: Tömörség, abszurd látásmód.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Groteszk fogalma -> 2. Tóték és dobozolás -> 3. Margóvágó katarzisa -> 4. Egypercesek.",
        "kviz": [{"k": "Tót Lajos a mű végén a margóvágóval négy darabba vágja az Őrnagyot.", "v": True, "m": "Az abszurd lázadás végső aktusa."}]
    },
    "20. Ottlik Géza: Iskola a határon": {
        "alcim": "A létezésfilozófiai regény, a zárt katonaiskola világa és a szavak nélküli összetartozás",
        "kulcsszavak": ["Kőszegi katonaiskola", "Medve Gábor, Bébé", "Belső szabadság"],
        "audio_szoveg": "Ottlik Géza 1959-es regénye a zárt katonaiskola világát és a belső autonómia megőrzését mutatja be...",
        "vazlat": "### I. Elbeszélésmód: Bébé és Medve kéziratai.\n### II. Katonaiskola: Zárt rendszer és megaláztatások.\n### III. Túlélés: Szavak nélküli szolidaritás, belső szabadság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. 1959 Ottlik főműve -> 2. Katonaiskola világa -> 3. Bébé és Medve -> 4. Szavak elégtelensége.",
        "kviz": [{"k": "Az Iskola a határon a kőszegi katonai alreáliskolában játszódik.", "v": True, "m": "Zárt jellemfejlődési tér."}]
    },
    "21. Krúdy Gyula: Szindbád és a novellisztika": {
        "alcim": "Az impresszionista-szecessziós időszerkezet, az emlékek és az érzékek birodalma",
        "kulcsszavak": ["Szindbád-novellák", "Kulináris és szerelmi emlékek", "Időbontás"],
        "audio_szoveg": "Krúdy Gyula Szindbád-történeteiben az idő az emlékek és ízek hullámain lebeg...",
        "vazlat": "### I. Időkezelés: Szubjektív időélmény, múlt és jelen összefolyása.\n### II. Szindbád: Az örök utazó, kulináris és női emlékek gyűjtője.\n### III. Stílus: Impresszionizmus, szecesszió.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Krúdy egyedisége -> 2. Szindbád alakja -> 3. Időbontás és érzékek -> 4. Szecesszió.",
        "kviz": [{"k": "Krúdy Szindbád-történeteiben az időélmény szubjektív és emlékekre épül.", "v": True, "m": "A múlt és jelen összefolyik."}]
    },
    "22. Illyés Gyula: Egy mondat a zsarnokságról és a Puszták népe": {
        "alcim": "A szociográfiai próza és a totalitárius diktatúra lélektanának monumentális költeménye",
        "kulcsszavak": ["Egy mondat a zsarnokságról", "Puszták népe (1936)", "Diktatúra"],
        "audio_szoveg": "Illyés Gyula a magyar népi mozgalom vezéralakja volt...",
        "vazlat": "### I. Puszták népe (1936): Szociográfia a dunántúli cselédek nyomoráról.\n### II. Egy mondat a zsarnokságról (1950): Egyetlen monumentális körmondat a diktatúra mindent átható jelenlétéről.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Népi írók mozgalma -> 2. Puszták népe -> 3. Egy mondat a zsarnokságról -> 4. Hatás.",
        "kviz": [{"k": "Az 'Egy mondat a zsarnokságról' című vers egyetlen körmondatból épül fel.", "v": True, "m": "A diktatúra mindent befonó lényegét fejezi ki."}]
    }
}

tetelek_nyelvtan = {
    "1. A kommunikáció folyamata és tényezői": {
        "alcim": "A kommunikációs modell, nyelvi és nem nyelvi jelek, kommunikációs funkciók",
        "kulcsszavak": ["Adó és Vevő", "Kód és Csatorna", "Jakobson modellje", "Metakommunikáció"],
        "audio_szoveg": "A kommunikáció információk, gondolatok és érzelmek átadása valamilyen jelrendszer segítségével...",
        "vazlat": "### I. A Jakobson-féle modell: Adó, Vevő, Üzenet, Kód, Csatorna, Kontextus (helyzet), Zaj.\n### II. Nyelvi funkciók: Tájékoztató (referenciális), Érzelemkifejező (emotív), Felhívó (konatív), Fatikus (kapcsolattartó), Metanyelvi (a kódról szóló), Poétikai (esztétikai).\n### III. Nem nyelvi (nonverbális) kódok: Mimika, testbeszéd, gesztusok, szemkontaktus, proxemika (távolságtartás).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A kommunikáció definíciója -> 2. Roman Jakobson 6 tényezős modellje -> 3. A nyelvi funkciók bemutatása példákkal -> 4. Nonverbális jelek szerepe.",
        "kviz": [{"k": "A fatikus funkció elsődleges célja az üzenet esztétikai formájának kiemelése.", "v": False, "m": "A fatikus funkció a kapcsolat felvételére, fenntartására vagy lezárására szolgál (pl. köszönés)."}]
    },
    "2. A szövegtan alapjai és a szövegtípusok": {
        "alcim": "A szöveg kohéziós erői, szerkezeti egységei és típusai",
        "kulcsszavak": ["Globális kohézió", "Lokális kohézió", "Anafora és Katafora", "Elbeszélő, leíró, érvelő"],
        "audio_szoveg": "A szöveg a nyelv legmagasabb szintű, lezárt, kerek egysége...",
        "vazlat": "### I. A szöveg fogalma: Lezárt, összefüggő, tartalmi és formai egységet alkotó nyelvi megnyilatkozás.\n### II. Kohézió (szövegösszetartás): Lokális kohézió (kötőszók, láncszerű kapcsolódás, anafora=visszautalás, katafora=előreutalás) és globális kohézió (témamegtartás).\n### III. Szerkezet és típusok: Cím, bevezetés, tárgyalás, befejezés; elbeszélő, leíró, magyarázó és érvelő szövegek.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A szöveg mint nyelvi egység -> 2. Kohéziós eszközök (anafora, katafora) -> 3. Makrostruktúra -> 4. Szövegtípusok.",
        "kviz": [{"k": "Az anafora a szövegben előreutalást jelent egy még be nem mutatott elemre.", "v": False, "m": "Az anafora visszautaló elem, az előreutalás a katafora."}]
    },
    "3. A magyar helyesírás alapelvei": {
        "alcim": "A 4 alapelv rendszere és alkalmazásuk a gyakorlatban",
        "kulcsszavak": ["Kiejtés elve", "Szóelemzés elve", "Hagyomány elve", "Egyszerűsítés elve"],
        "audio_szoveg": "A magyar helyesírás négy alapelvre épül, amelyek biztosítják az íráskép egységességét...",
        "vazlat": "### I. A kiejtés elve: A hangok tiszta írása, ha nincs nyelvtani akadály (pl. *asztal, fa*).\n### II. A szóelemzés (morfematikus) elve: A morfémák határai felismerhetők maradnak a kiejtéstől függetlenül (pl. *látja, barátság*).\n### III. A hagyomány elve: Történelmi helyesírási formák őrzése (pl. *Kossuth, lyuk, ch*).\n### IV. Az egyszerűsítés elve: A kettőzött betűk egyszerűsítése találkozáskor (pl. *asszony, tollal* vs. kivétel: *juhász*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A helyesírási alapelvek szerepe -> 2. Kiejtés és szóelemzés ellentéte/összhangja -> 3. Hagyomány elve példákkal -> 4. Egyszerűsítés elve.",
        "kviz": [{"k": "A 'barátság' szó leírásakor a kiejtést követjük, ezért írunk 'cs'-t.", "v": False, "m": "A szóelemzés elve érvényesül: barát + ság, ezért marad a 't' és 's' találkozása."}]
    },
    "4. Szófajok és mondatrészek rendszere": {
        "alcim": "Alapszófajok, viszonyszók, predikatív viszony és mondattani elemzés",
        "kulcsszavak": ["Ige, Névszó, Igenév", "Viszonyszók", "Alany, Állítmány", "Bővítmények"],
        "audio_szoveg": "A szófajok a szavak alaktani és mondattani kategóriái, amelyekből a mondatrészek épülnek fel...",
        "vazlat": "### I. Szófaji csoportok: Alapszófajok (ige, főnév, melléknév, számnév, határozószó, igenevek), Viszonyszók (névelő, névmás, kötőszó, névutó, segédige), Mondatszók.\n### II. Alapvető mondattani viszonyok: Predikatív (alany-állítmányi), alárendelő (bővítményi), mellérendelő.\n### III. Mondatrészek: Alany, állítmány, tárgy, hely-, idő-, módhatározó, jelzők (minőségjelző stb.).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Alapszófajok vs. viszonyszók -> 2. Az alany és állítmány predikatív viszonya -> 3. Alárendelő mondatrészek fajtái.",
        "kviz": [{"k": "A névelők önálló mondatrészsé válhatnak a mondatban.", "v": False, "m": "A viszonyszók (így a névelők is) önmagukban nem alanyai vagy tárgyai a mondatnak."}]
    },
    "5. Retorika és érvelési technikák": {
        "alcim": "Az érv 3 része, érvtípusok és a klasszikus szónoki beszéd 6 lépése",
        "kulcsszavak": ["Tétel, Bizonyíték, Összekötés", "Érvtípusok", "Exordium", "Peroratio"],
        "audio_szoveg": "A retorika a meggyőzés művészete, amely hatásos érvelési láncokra épül...",
        "vazlat": "### I. Az érv felépítése: Tétel (állitás) -> Bizonyíték (tény, adat) -> Összekötő elem (magyarázat).\n### II. Érvtípusok: Meghatározásból levezetett, ok-okozati, analógiás (hasonlóság), tekintélyre hivatkozó, ellentétre épülő.\n### III. Klasszikus szónoki beszéd: Exordium (bevezetés) -> Narratio (témafelvetés) -> Divisio (részletezés) -> Confirmatio (bizonyítás) -> Refutatio (cáfolat) -> Peroratio (befejezés).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A retorika fogalma és célja -> 2. Az érv három alkotóeleme -> 3. Gyakoribb érvtípusok -> 4. A klasszikus szónoki felépítés.",
        "kviz": [{"k": "Az analógiás érv két hasonló eset vagy helyzet összehasonlításán alapul.", "v": True, "m": "Igen, a hasonlóságon keresztül bizonyít."}]
    },
    "6. Stilisztika: Alakzatok és trópusok": {
        "alcim": "Költői képek (metafora, metonímia, szinesztézia) és szövegalakzatok",
        "kulcsszavak": ["Metafora", "Metonímia", "Szinesztézia", "Anafora és Párhuzam"],
        "audio_szoveg": "A stilisztika a nyelvi kifejezőeszközök és alakzatok hatásmechanizmusát vizsgálja...",
        "vazlat": "### I. Trópusok (jelentésbeli alakzatok): Metafora (hasonlóságon alapuló névváltoztatás), Metonímia (érintkezésen alapuló: anyag, tér-idő), Szinekdoché (rész-egész), Szinesztézia (különböző érzéki területek összekapcsolása).\n### II. Alakzatok (formai/szerkezeti): Anafora (sor eleji ismétlés), Párhuzam, Ellentét, Fokozás, Halmozás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trópusok vs. alakzatok különbsége -> 2. A metafora fajtái -> 3. Szinesztézia és metonímia -> 4. Szövegalakzatok.",
        "kviz": [{"k": "A 'bársonyos hang' kifejezés egy tipikus szinesztézia, mivel tapintási és hallási érzékelést köt össze.", "v": True, "m": "Igen, a bársony (tapintás) és a hang (hallás) keveredik."}]
    },
    "7. A szókészlet rétegződése és változása": {
        "alcim": "Nyelvjárások, társadalmi rétegnyelvek, szleng, archaizmusok és neologizmusok",
        "kulcsszavak": ["Nyelvjárások", "Szaknyelv és Szleng", "Archaizmus", "Neologizmus"],
        "audio_szoveg": "A magyar nyelv szókészlete folyamatosan változik, és területileg, valamint társadalmilag is rétegződik...",
        "vazlat": "### I. Területi tagozódás: Nyelvjárások (dialektusok) és a tájszavak.\n### II. Társadalmi tagozódás: Szaknyelvek, rétegnyelvek, szleng (laza, fiatalos argó).\n### III. Időbeli változás: Archaizmusok (régies, elavult szavak) és Neologizmusok (új szavak, idegen eredetű vagy belső keletkezésű újítások).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A szókészlet dinamikája -> 2. Területi dialektusok -> 3. Társadalmi rétegnyelvek és szleng -> 4. Archaizmus és neologizmus.",
        "kviz": [{"k": "Az archaizmusok a mai modern kor legújabb szavait jelölik.", "v": False, "m": "Az archaizmusok elavult, régies szavak, míg az újak a neologizmusok."}]
    },
    "8. A magyar nyelv története és a nyelvújítás": {
        "alcim": "A finnugor rokonság, a korai nyelvemlékek és Kazinczy nyelvújítása",
        "kulcsszavak": ["Uráli / Finnugor", "Halotti Beszéd (1195)", "Ómagyar Mária-siralom", "Kazinczy Ferenc"],
        "audio_szoveg": "A magyar nyelv az uráli nyelvcsalád finnugor ágába tartozik, története évezredekre nyúlik vissza...",
        "vazlat": "### I. Eredet: Finnugor nyelvrokonság, ugor kor, honfoglalás kori szókincs.\n### II. Korai nyelvemlékek: Tihanyi apátság alapítólevele (1055 - szórványemlékek), Halotti beszéd és könyörgés (1195 körül - első összefüggő szöveg), Ómagyar Mária-siralom (13. sz. eleje - első lírai emlék).\n### III. A nyelvújítás korszaka (1790–1820): Kazinczy Ferenc; küzdelem a neológusok és ortológusok között; új szavak megalkotása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A finnugor származás bizonyítékai -> 2. Fontosabb korai nyelvemlékek -> 3. A nyelvújítás szükségessége és Kazinczy szerepe.",
        "kviz": [{"k": "A Halotti beszéd és könyörgés az első fennmaradt összefüggő magyar nyelvű szövegemlékünk.", "v": True, "m": "Igen, a Pray-kódexben maradt fenn 1195 körül."}]
    },
    "9. Fonetika: A hangok képzése és a mássalhangzótörvények": {
        "alcim": "Magánhangzók és mássalhangzók rendszere, hasonulás, összeolvadás, kiesés és rövidülés",
        "kulcsszavak": ["Zöngés és Zöngétlen", "Részleges hasonulás", "Teljes hasonulás", "Összeolvadás"],
        "audio_szoveg": "A fonetika a beszédhangok képzését, tulajdonságait és az egymásra ható mássalhangzótörvényeket vizsgálja...",
        "vazlat": "### I. Hangrendszer: Magánhangzók (mély, magas, vegyes; rövid, hosszú) és mássalhangzók (zöngés / zöngétlen párok).\n### II. Mássalhangzótörvények:\n- Zöngésségi részleges hasonulás (pl. *népdal -> népdal [néptal]*).\n- Képzés helye szerinti részleges hasonulás (pl. *színpad -> [szímpad]*).\n- Teljes hasonulás (jelölt: *szabja -> szablya*; jelöletlen: *zsebkendő -> zsebkendő [zsebkendő]* -> *egészség*).\n- Összeolvadás (pl. *barátság -> [baraccság]*).\n- Kiesés és rövidülés.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A hangok csoportosítása -> 2. Zöngésségi és képzés helye szerinti hasonulás -> 3. Teljes hasonulás (jelölt és jelöletlen) -> 4. Összeolvadás.",
        "kviz": [{"k": "A 'színpad' szó kiejtésekor képzés helye szerinti részleges hasonulás érvényesül ('n' m-mûvé alakul).", "v": True, "m": "Igen, az 'n' hang az 'p' előtt 'm'-mû váltódik."}]
    },
    "10. Morfológia: A szóelemek (morfémák) rendszere": {
        "alcim": "Tőmorfémák, toldalékmorfémák (képző, jel, rag) és a szóelemző helyesírás",
        "kulcsszavak": ["Szótő", "Képző", "Jel", "Rag", "Kötött sorrend"],
        "audio_szoveg": "A morfológia a szavak szerkezetét és a legkisebb jelentést hordozó egységeket, a morfémákat vizsgálja...",
        "vazlat": "### I. Morféma típusok: Tőmorféma (szótő) és toldalékmorféma.\n### II. A toldalékok szigorú sorrendje: Szótő + KÉPZŐ + JEL + RAG (pl. *ház-as-ság-ok-at*).\n### III. Funkciók: Képző (új szót hoz létre, szófajt válthat), Jel (módosítja a jelentést: múlt idő, többes szám, birtokos jel), Rag (lezárja a szót, mondatrészi szerepet ad).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Morféma fogalma -> 2. A képző, jel, rag különbségei -> 3. A szigorú toldalékolási sorrend -> 4. Szóelemző helyesírás.",
        "kviz": [{"k": "A rag a toldalékolási sorban mindig a szó legvégén, a képzők és jelek után áll.", "v": True, "m": "Igen, a rag zárja le a morfémasort."}]
    },
    "11. Szóalkotási módok a magyar nyelvben": {
        "alcim": "Szóösszetétel, szóképzés, mozaikszók, szóelvonás, szóvegyülés és rövidülés",
        "kulcsszavak": ["Szóképzés", "Szóösszetétel", "Mozaikszók", "Szóelvonás"],
        "audio_szoveg": "A magyar nyelv rendkívül gazdag belső szóalkotási módokban, amelyek révén folyamatosan bővül...",
        "vazlat": "### I. Fő szóalkotási módok: Szóképzés (új szó képzővel) és Szóösszetétel (alárendelő és mellérendelő összetételek).\n### II. Egyéb módok: Mozaikszók (betűszók: *MÁV*, szóösszevonások: *Főgáz*), Szóelvonás (*kapa <- kapál*), Szóvegyülés (*csokréta*), Szócsonkítás (*mozi*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Képzés és összetétel szerepe -> 2. Összetételek fajtái (alárendelő, mellérendelő) -> 3. Mozaikszók és ritkább szóalkotási módok.",
        "kviz": [{"k": "A 'kapa' szónak a 'kapál' igéből való visszaképzése (szóelvonás) tipikus példája az új szóalkotásnak.", "v": True, "m": "Igen, itt a hosszabb szóból vonják el a rövidebbet."}]
    },
    "12. Mondattan: Az összetett mondatok típusai": {
        "alcim": "Mellérendelő (kapcsolatos, ellentétes, választó, következtető, magyarázó) és alárendelő mondatok",
        "kulcsszavak": ["Mellérendelő összetett mondat", "Alárendelő összetett mondat", "Főmondat és Mellékmondat"],
        "audio_szoveg": "Az összetett mondatok két vagy több tagmondatból állnak, amelyek viszonya lehet mellérendelő vagy alárendelő...",
        "vazlat": "### I. Mellérendelő összetett mondatok: Tagmondatok egyenrangúak; fajtái: kapcsolatos, ellentétes, választó, következtető, magyarázó.\n### II. Alárendelő összetett mondatok: Főmondat + utalószóval kapcsolódó mellékmondat; a mellékmondat pótolja valamelyik hiányzó mondatrészt (alanyi, tárgyi, határozói, jelzői mellékmondatok).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Alapfogalmak (tagmondatok) -> 2. A 5 féle mellérendelő kapcsolat kötőszavakkal -> 3. Az alárendelő mondatok struktúrája (utalószó szerepe).",
        "kviz": [{"k": "A 'Szakad az eső, ezért otthon maradtunk' mondat következtető mellérendelő összetett mondat.", "v": True, "m": "Igen, az 'ezért' kötőszó következtetést fejez ki."}]
    },
    "13. Stílusrétegek és a stílusérték": {
        "alcim": "Hivatalos, tudományos, publicisztikai, társalgási és szépirodalmi stílus",
        "kulcsszavak": ["Stílusrétegek", "Hivatalos és Tudományos", "Publicisztika", "Denotáció és Konnotáció"],
        "audio_szoveg": "A stílusrétegek a beszédhelyzetnek megfelelő nyelvi eszközök és kifejezésmódok egységei...",
        "vazlat": "### I. Főbb stílusrétegek:\n- Társalgási (köznyelvi, laza, szubjektív).\n- Szépirodalmi (képszerű, érzelmi hatásra törekvő, konnotatív).\n- Tudományos (pontos, szakszavak, tárgyilagos, denotatív).\n- Hivatalos (száraz, sablonos, törvények, kérvények nyelve).\n- Publicisztikai (sajtó, rádió, TV, figyelemfelkeltő, véleményformáló).\n### II. Jelentésrétegek: Denotáció (alapjelentés) és konnotáció (mellékjelentés, hangulat).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Stílusrétegek fogalma és szerepe -> 2. Hivatalos és tudományos stílus jellemzői -> 3. Publicisztikai és társalgási stílus -> 4. Denotáció vs konnotáció.",
        "kviz": [{"k": "A hivatalos stílusra a magas fokú szubjektivitás és a költői képek halmozása jellemző.", "v": False, "m": "A hivatalos stílus sablonos, tárgyilagos és mentes a szubjektív képektől."}]
    },
    "14. Névtan (Onomasztika)": {
        "alcim": "Személynevek és földrajzi nevek rendszere, eredete",
        "kulcsszavak": ["Családnevek típusai", "Keresztnevek", "Földrajzi nevek helyesírása"],
        "audio_szoveg": "A névtan a tulajdonnevek rendszereivel, eredetével és helyesírásával foglalkozó nyelvtudományi ág...",
        "vazlat": "### I. Személynevek rendszere:\n- Családnevek 5 fő forrása: Apai név (*Péterfi*), származási hely (*Budai*), foglalkozás (*Kovács*), külső/belső tulajdonság (*Nagy*), etnikum (*Tóth*).\n- Keresztnevek (történelmi nevek, új nevek antropológiai gyökerei).\n### II. Földrajzi nevek helyesírása: Egyelemű (*Duna*), kételemű egybeírt (*Margitsziget*), kételemű különírt (*Velencei-tó* vagy *Fekete-tenger*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A névtan mint tudomány -> 2. A családnevek 5 nagy kategóriája -> 3. Földrajzi tulajdonnevek írásmódja.",
        "kviz": [{"k": "A 'Kovács' családnév a foglalkozásból/mesterségből származó nevek csoportjába tartozik.", "v": True, "m": "Igen, a kovácsmesterségre utal."}]
    },
    "15. Frazeológia: Szólások, közmondások és szállóigék": {
        "alcim": "Állandósult szókapcsolatok fajtái és metaforikus jelentése",
        "kulcsszavak": ["Szólás", "Közmondás", "Szállóige", "Közhely"],
        "audio_szoveg": "A frazeológia a nyelv állandósult, metaforikus értelmű szókapcsolatait kutatja...",
        "vazlat": "### I. Szólás: Képszerű, állandósult kifejezés, amely önmagában nem mondatértékű (pl. *éles esze van, feni a fogát*).\n### II. Közmondás: Kerek egész mondat, amelynek tanulsága, népiöltsége van (pl. *Nem minden arany, ami fénylik*).\n### III. Szállóige: Ismert szerzőhöz vagy irodalmi műhöz köthető idézet, amely közkinccsé vált (pl. *A kocka el van vetve*).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Állandósult szókapcsolatok lényege -> 2. Szólás és közmondás különbsége -> 3. Szállóigék szerepe a kultúrában.",
        "kviz": [{"k": "A 'Lassan járj, tovább érsz' egy tipikus közmondás, mert kerek mondat tanulsággal.", "v": True, "m": "Igen, a népi bölcsesség megtestesítője."}]
    },
    "16. Digitális kommunikáció és az infokommunikációs nyelv": {
        "alcim": "Az online nyelvhasználat, emotikonok, hipertext és a közösségi média hatása",
        "kulcsszavak": ["Netnyelv", "Hipertext", "Multimodalitás", "Írott beszéltség"],
        "audio_szoveg": "Az internet és a digitális forradalom teljesen átalakította a modern ember nyelvhasználatát...",
        "vazlat": "### I. Az online nyelvhasználat jellemzői: Írott beszéltség (az írás és a szóbeliség sajátos keveréke), gyorsaság, tömörség, szleng hatása.\n### II. Multimodalitás és Emojik: Képek, emojik és gifek mint a hiányzoló metakommunikáció (hangszín, mimika) pótlói a neten.\n### III. Hipertext és linkek: Nemlineáris szövegolvasás, hálózatos struktúrák.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. A digitális kultúra hatása a nyelvre -> 2. Az 'írott beszéltség' jelensége -> 3. Emojik és nonverbális pótlékok -> 4. Hipertext struktúra.",
        "kviz": [{"k": "Az 'írott beszéltség' azt jelenti, hogy a netes csevegésben az írott formák átveszik a kötetlen beszéd stílusát.", "v": True, "m": "Igen, az írás médiumán keresztül folytatunk spontán társalgást."}]
    }
}

tetelek_tortenelem = {
    "1. Az athéni demokrácia működése a Kr. e. V. században": {
        "alcim": "Szolón, Kleiszthenész reformjai, Periklész kora és a népgyűlés (ekklészia)",
        "kulcsszavak": ["Népgyűlés (Ekklészia)", "Cserépszavazás", "Sztratégosz", "Napidíj", "Periklész"],
        "audio_szoveg": "Az athéni demokrácia az ókori világ legfejlettebb népuralmi rendszere volt...",
        "vazlat": "### I. Fejlődés: Szolón -> Kleiszthenész (10 phülé, cserépszavazás).\n### II. Periklész kora: Népgyűlés (Ekklészia), Bulé, Sztratégoszok, napidíjak.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kialakulás -> 2. Intézményrendszer -> 3. Napidíjak.",
        "kviz": [{"k": "Az athéni népgyűlés tagja lehetett minden szabad athéni férfi polgár.", "v": True, "m": "Közvetlen demokrácia volt."}]
    },
    "2. A Római Köztársaság válsága és a Principátus kialakulása": {
        "alcim": "A polgárháborúk kora, Caesar diktatúrája és Augustus principátusa",
        "kulcsszavak": ["Gracchusok", "Marius", "Julius Caesar", "Augustus", "Pax Romana"],
        "audio_szoveg": "A Római Köztársaság a hódítások következtében mély válságba került...",
        "vazlat": "### I. Válság: Parasztság tönkremenetele, rabszolgafelkelések.\n### II. Caesar és Augustus principátusa (Kr. e. 27), Pax Romana.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Válság okai -> 2. Caesar -> 3. Augustus.",
        "kviz": [{"k": "Augustus megtartotta a köztársasági intézményeket.", "v": True, "m": "Princepsként uralkodott."}]
    },
    "3. A kereszténység születése és elterjedése az ókorban": {
        "alcim": "Jézus tanításai, az őskeresztény gyülekezetek és a milánói ediktum (313)",
        "kulcsszavak": ["Názáreti Jézus", "Szent Pál", "Milánói ediktum (313)", "Nicaea"],
        "audio_szoveg": "A kereszténység a Római Birodalom keleti tartományában indult ki...",
        "vazlat": "### I. Tanítások: Szeretet, megváltás.\n### II. Milánói ediktum (313): Constantinus engedélyezi a vallást.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Jézus -> 2. Pál apostol -> 3. Milánói ediktum.",
        "kviz": [{"k": "313-ban a milánói ediktummal engedélyezték a kereszténységet.", "v": True, "m": "Constantinus császár tette."}]
    },
    "4. A középkori uradalom és a hűbériség rendszere": {
        "alcim": "Hűbéri lánc (feudalizmus), a jobbágyság és a háromnyomásos gazdálkodás",
        "kulcsszavak": ["Senior és Vazallus", "Feudum", "Majorság", "Háromnyomásos gazdálkodás"],
        "audio_szoveg": "A középkori Európa társadalmi és gazdasági rendszere a hűbériségen alapult...",
        "vazlat": "### I. Hűbériség: Földért katonai szolgálat.\n### II. Uradalom: Majorság, jobbágytelek, robot.\n### III. Agrártechnika: Háromnyomásos gazdálkodás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Feudalizmus -> 2. Uradalom -> 3. Technika.",
        "kviz": [{"k": "A háromnyomásos gazdálkodásban a föld 1/3-a pihent.", "v": True, "m": "Az ugar."}]
    },
    "5. Az Iszlám vallás születése és az arab-iszlám világ expanziója": {
        "alcim": "Mohamed próféta, a Korán, az iszlám öt oszlopa és a kalifátusok terjeszkedése",
        "kulcsszavak": ["Mohamed", "Hegidzsra (622)", "Korán", "Öt oszlop", "Kalifátus"],
        "audio_szoveg": "Az iszlám vallás a 7. század elején született meg az Arab-félszigeten...",
        "vazlat": "### I. Alapítás: Mohamed, 622 hegidzsra.\n### II. Öt oszlop: Hitvallás, ima, adakozás, böjt, zarándoklat.\n### III. Kalifátusok hódításai.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mohamed -> 2. 5 oszlop -> 3. Hódítások.",
        "kviz": [{"k": "Az iszlám időszámítás kezdete 622.", "v": True, "m": "A hegizsra éve."}]
    },
    "6. Szent István államalapítása és az egyházszervezés": {
        "alcim": "A keresztény királyság megszilárdítása, vármegyerendszer és törvények",
        "kulcsszavak": ["Koppány", "Koronázás (1000)", "10 egyházmegye", "Ispánok", "Tized"],
        "audio_szoveg": "Géza fejedelem után fia, István király 1000 karácsonyán felvette a koronát...",
        "vazlat": "### I. Koppány legyőzése -> Koronázás (1000/1001).\n### II. Egyház: 10 püspökség, tized.\n### III. Vármegyerendszer, ispánok.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Koronázás -> 2. Egyház -> 3. Vármegyék.",
        "kviz": [{"k": "Szent István 10 püspökséget alapított.", "v": True, "m": "Esztergom és Kalocsa érsekség lett."}]
    },
    "7. Az Aranybulla és a rendi társadalom gyökerei (1222)": {
        "alcim": "II. András birtokpolitikája, a szerviensek mozgalma és a nemesi jogok rögzítése",
        "kulcsszavak": ["1222 Aranybulla", "Szerviensek", "Adómentesség", "Ellenállási záradék"],
        "audio_szoveg": "II. András adományai miatt a szerviensek kikényszerítették az Aranybullát...",
        "vazlat": "### I. Aranybulla (1222): Adómentesség, bírói ítélet védelme.\n### II. 31. cikkely: Ellenállási záradék (ius resistendi).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Előzmény -> 2. Aranybulla -> 3. Ellenállási záradék.",
        "kviz": [{"k": "Az Aranybulla 31. cikkelye tartalmazta az ellenállási záradékot.", "v": True, "m": "Jog a király ellen."}]
    },
    "8. Az Anjouk kora Magyarországon": {
        "alcim": "Károly Róbert gazdasági reformjai és Nagy Lajos 1351-es törvényei",
        "kulcsszavak": ["Bányabér (Urbura)", "Aranyforint", "Kapuadó", "1351 Ősiség és Kilenced"],
        "audio_szoveg": "Károly Róbert legyőzte a tartományurakat és stabil gazdasági reformokat vezetett be...",
        "vazlat": "### I. Károly Róbert: Urbura, aranyforint, kapuadó, 1335 Visegrád.\n### II. Nagy Lajos (1351): Ősiség, Kilenced.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Károly Róbert -> 2. Visegrád -> 3. Nagy Lajos.",
        "kviz": [{"k": "Az 1351-es ősiség törvénye védte a nemesi birtokot.", "v": True, "m": "Nem lehetett eladni."}]
    },
    "9. Hunyadi Mátyás uralkodása (1458–1490)": {
        "alcim": "Központosított monarchia, bevételek, Fekete sereg és a reneszánsz udvar",
        "kulcsszavak": ["Füstpénz", "Rendkívüli hadiadó", "Fekete sereg", "Corvinák", "Bécs bevétele"],
        "audio_szoveg": "Hunyadi Mátyás erős központosított királyi hatalmat épített ki...",
        "vazlat": "### I. Bevételek: Füstpénz, rendkívüli hadiadó.\n### II. Fekete sereg, Bécs elfoglalása (1485).\n### III. Reneszánsz: Corvinák.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Bevételek -> 2. Fekete sereg -> 3. Reneszánsz.",
        "kviz": [{"k": "Mátyás füstpénzt vezetett be a kapuadó helyett.", "v": True, "m": "Háztartásonként szedték."}]
    },
    "10. A mohácsi csata és az ország három részre szakadása (1526–1541)": {
        "alcim": "A Jagelló-kor gyengesége, Mohács tragédiája, kettős királyválasztás és Buda eleste",
        "kulcsszavak": ["1526 Mohács", "Szapolyai és Ferdinánd", "1541 Buda eleste", "Három országrész"],
        "audio_szoveg": "1526. augusztus 29-én a mohácsi síkon megsemmisült a magyar haderő...",
        "vazlat": "### I. Mohács (1526) -> II. Kettős királyság -> III. Buda eleste (1541): 3 részre szakadás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mohács -> 2. Kettős királyság -> 3. Buda eleste.",
        "kviz": [{"k": "Buda 1541-es elfoglalásával szakadt három részre az ország.", "v": True, "m": "Szulejmán csellel vette be."}]
    },
    "11. A Rákóczi-szabadságharc (1703–1711)": {
        "alcim": "A Habsburg abszolutizmus elleni felkelés, az ónodi trónfosztás és a szatmári béke",
        "kulcsszavak": ["Brezáni kiáltvány", "Kurucok", "Ónod (1707)", "Szatmári béke (1711)"],
        "audio_szoveg": "II. Rákóczi Ferenc vezetésével bontakozott ki a függetlenségi háború...",
        "vazlat": "### I. Brezáni kiáltvány (1703) -> II. 1707 Ónodi trónfosztás -> III. 1711 Szatmári béke.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kezdet -> 2. Ónod -> 3. Szatmár.",
        "kviz": [{"k": "1707-ben mondták ki az ónodi országgyűlésen a trónfosztást.", "v": True, "m": "Habsburg-ház elűzése."}]
    },
    "12. A felvilágosult abszolutizmus Magyarországon": {
        "alcim": "Mária Terézia és II. József rendeletei (Védővám, Urbárium, Ratio Educationis, Türelmi rendelet)",
        "kulcsszavak": ["Mária Terézia", "Urbárium (1767)", "II. József", "Türelmi rendelet (1781)"],
        "audio_szoveg": "A 18. században a Habsburg uralkodók rendeleti úton modernizáltak...",
        "vazlat": "### I. Mária Terézia: Vámrendelet, Urbárium, Ratio Educationis.\n### II. II. József: Türelmi rendelet, Jobbágyrendelet.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Mária Terézia -> 2. II. József reformjai.",
        "kviz": [{"k": "II. József a kalapos király nevet kapta.", "v": True, "m": "Nem koronáztatta meg magát."}]
    },
    "13. A reformkor fő kérdései (1830–1848)": {
        "alcim": "Széchenyi István és Kossuth Lajos reformprogramjának összehasonlítása",
        "kulcsszavak": ["Hitel (1830)", "Örökváltság", "Közteherviselés", "Pesti Hírlap"],
        "audio_szoveg": "A magyar reformkor Széchenyi Hitel című művével indult...",
        "vazlat": "### I. Széchenyi: Hitel, gazdasági modernizáció.\n### II. Kossuth: Kötelező örökváltság, közteherviselés, sajtószabadság.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Széchenyi -> 2. Kossuth -> 3. Vita.",
        "kviz": [{"k": "Kossuth a kötelező örökváltságot követelte állami kárpótlással.", "v": True, "m": "Jobbágyfelszabadítás."}]
    },
    "14. Az 1848–49-es forradalom és szabadságharc": {
        "alcim": "Március 15., az Áprilisi törvények és a Tavaszi hadjárat sikerei",
        "kulcsszavak": ["12 pont", "Áprilisi törvények", "Batthyány Lajos", "Görgei", "Trónfosztás (1849)"],
        "audio_szoveg": "1848 tavaszán a pesti forradalom polgári Magyarországot teremtett...",
        "vazlat": "### I. Március 15., Áprilisi törvények -> II. Tavaszi hadjárat (1849) -> III. Világos.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Forradalom -> 2. Tavaszi hadjárat -> 3. Bukás.",
        "kviz": [{"k": "A Batthyány-kormány volt az első független felelős magyar kormány.", "v": True, "m": "1848 április."}]
    },
    "15. A dualizmus kora Magyarországon (1867–1914)": {
        "alcim": "A Kiegyezés rendszere, gazdasági felvirágzás és társadalmi rétegződés",
        "kulcsszavak": ["Kiegyezés (1867)", "Közös ügyek", "Gazdasági csoda", "Torlódó társadalom"],
        "audio_szoveg": "Az 1867-es kiegyezéssel létrejött az Osztrák-Magyar Monarchia...",
        "vazlat": "### I. Közös ügyek -> II. Gazdasági robbanás (vasút, malomipar) -> III. Torlódó társadalom.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kiegyezés -> 2. Gazdaság -> 3. Társadalom.",
        "kviz": [{"k": "A dualizmus korában a külügy és hadügy közös volt.", "v": True, "m": "Közös ügyek."}]
    },
    "16. Az első világháború és következményei (1914–1918)": {
        "alcim": "A szövetségi rendszerek, az állóháború jellege és a hátország összeomlása",
        "kulcsszavak": ["Szarajevó (1914)", "Antant", "Állóháború", "Trianon (1920)"],
        "audio_szoveg": "Az 1914-es merénylet kirobbantotta a Nagy Háborút...",
        "vazlat": "### I. Állóháború a lövészárkokban -> II. 1918 összeomlás -> III. 1920 Trianon.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Okok -> 2. Hadviselés -> 3. Trianon.",
        "kviz": [{"k": "Az I. világháborúban az USA 1917-ben lépett be.", "v": True, "m": "Antant oldalán."}]
    },
    "17. A Horthy-korszak konszolidációja (1920–1931)": {
        "alcim": "Trianon traumája, a bethleni konszolidáció és Klebelsberg kultúrpolitikája",
        "kulcsszavak": ["Trianon", "Bethlen István", "Pengő (1927)", "Klebelsberg Kuno"],
        "audio_szoveg": "Trianon után Bethlen István vezetésével stabilizálódott az ország...",
        "vazlat": "### I. Bethleni konszolidáció (Pengő, kölcsön) -> II. Klebelsberg iskolaépítése.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Trianon -> 2. Bethlen -> 3. Klebelsberg.",
        "kviz": [{"k": "1927-ben vezették be a Pengőt.", "v": True, "m": "Stabil valuta lett."}]
    },
    "18. A második világháború főbb fordulópontjai (1939–1945)": {
        "alcim": "A náci agresszió, a szövetségesek koalíciója, Sztálingrád, D-nap és a holokauszt",
        "kulcsszavak": ["1939 Lengyelország", "Sztálingrád", "D-nap (1944)", "Holokauszt"],
        "audio_szoveg": "1939-ben kitört a II. világháború...",
        "vazlat": "### I. Sztálingrádi fordulat -> II. Normandiai partraszállás -> III. Holokauszt.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kitörés -> 2. Sztálingrád -> 3. Holokauszt.",
        "kviz": [{"k": "A sztálingrádi csata a II. vh döntő fordulata volt.", "v": True, "m": "Keleti front."}]
    },
    "19. Magyarország a második világháborúban (1941–1945)": {
        "alcim": "Revíziós sikerek, belépés a háborúba, a doni katasztrófa, a német megszállás és a nyilas terror",
        "kulcsszavak": ["Bécsi döntések", "Don-kanyar (1943)", "1944. március 19.", "Nyilas terror"],
        "audio_szoveg": "Magyarország a revízió áraként sodródott a háborúba...",
        "vazlat": "### I. Doni katasztrófa -> II. 1944 német megszállás -> III. Nyilas terror.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hadbalépés -> 2. Don-kanyar -> 3. Megszállás.",
        "kviz": [{"k": "A 2. magyar hadsereg 1943-ban a Donnál pusztult el.", "v": True, "m": "Tragikus vereség."}]
    },
    "20. A hidegháború kialakulása és korszakai (1945–1991)": {
        "alcim": "Kétpólusú világ, fegyverkezési verseny, Truman-doktrína, kubai rakétaválság és szovjet összeomlás",
        "kulcsszavak": ["Vasfüggöny", "NATO és Varsói Szerződés", "Kubai válság (1962)", "Gorbacsov"],
        "audio_szoveg": "A II. vh után a világ két szuperhatalmi blokkra szakadt...",
        "vazlat": "### I. NATO és Varsói Szerződés -> II. Kubai válság -> III. Szovjetunió felbomlása.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kétpólusú világ -> 2. Válságok -> 3. Összeomlás.",
        "kviz": [{"k": "1962-ben volt a kubai rakétaválság.", "v": True, "m": "Atomháború veszélye."}]
    },
    "21. Az 1956-os magyar forradalom és szabadságharc": {
        "alcim": "A Rákosi-diktatúra válsága, október 23., Nagy Imre kormánya és a szovjet intervenció",
        "kulcsszavak": ["Október 23.", "Nagy Imre", "Semlegesség", "November 4. Szovjet invázió"],
        "audio_szoveg": "1956. október 23-án indult a forradalom a szovjet elnyomás ellen...",
        "vazlat": "### I. Október 23. -> II. Nagy Imre kormánya, semlegesség -> III. Nov. 4. szovjet támadás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Előzmény -> 2. Forradalom napjai -> 3. Leverés.",
        "kviz": [{"k": "1956. november 4-én indult meg a szovjet invázió.", "v": True, "m": "Forgószél hadművelet."}]
    },
    "22. A Kádár-rendszer korszaka és a „gulyáskommunizmus”": {
        "alcim": "Az 1956 utáni konszolidáció, a Kádár-féle politika és az életszínvonal-politika",
        "kulcsszavak": ["Konszolidáció", "„Aki nincs ellenünk, az velünk van”", "Gulyáskommunizmus"],
        "audio_szoveg": "1956 után Kádár János nevéhez fűződik a gulyáskommunizmus korszaka...",
        "vazlat": "### I. Kádári alku (csendes befelé fordulásért anyagi jólét) -> II. Gulyáskommunizmus.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Konszolidáció -> 2. Életszínvonal-politika.",
        "kviz": [{"k": "A Kádár-korszakban a szlogen így szólt: 'Aki nincs ellenünk, az velünk van'.", "v": True, "m": "Enyhítés."}]
    },
    "23. A békés rendszerváltás Magyarországon (1989–1990)": {
        "alcim": "A Kádár-rendszer válsága, az Ellenzéki Kerekasztal, Nagy Imre újratemetése és a szabad választások",
        "kulcsszavak": ["Ellenzéki Kerekasztal", "1989. jún. 16. Újratemetés", "1989. okt. 23. Köztársaság"],
        "audio_szoveg": "1989-1990-ben békés tárgyalások útján alakult át a diktatúra...",
        "vazlat": "### I. EKA -> II. 1989 újratemetés és határnyitás -> III. 1990 szabad választások.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Ellenzék -> 2. 1989 eseményei -> 3. Választások.",
        "kviz": [{"k": "1989. október 23-án kiáltották ki a köztársaságot.", "v": True, "m": "Szűrös Mátyás."}]
    },
    "24. A nagy földrajzi felfedezések és a kapitalizmus hajnala": {
        "alcim": "A karavella, iránytű, Kolumbusz, Vasco da Gama és a globális kereskedelem",
        "kulcsszavak": ["Kolumbusz (1492)", "Vasco da Gama", "Árforradalom", "Gyarmatosítás"],
        "audio_szoveg": "A 15. század végén új tengeri utakat kerestek az európaiak...",
        "vazlat": "### I. Okok -> II. Kolumbusz (1492), Vasco da Gama -> III. Árforradalom, gyarmatosítás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Okok -> 2. Új utak -> 3. Következmények.",
        "kviz": [{"k": "Kolumbusz 1492-ben érte el Amerikát.", "v": True, "m": "Spanyol támogatással."}]
    },
    "25. A reformáció és a katolikus megújulás (ellenreformáció)": {
        "alcim": "Luther Márton, Kálvin János, hitviták, új felekezetek és a barokk művészet",
        "kulcsszavak": ["Luther (1517)", "Kálvin János", "Jezsuiták", "Trentói zsinat"],
        "audio_szoveg": "A 16. században a katolikus egyház bírálatából kiindulva kibontakozott a reformáció...",
        "vazlat": "### I. Luther (1517, 95 tétel) -> II. Kálvin -> III. Trentói zsinat és barokk.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Luther -> 2. Kálvin -> 3. Ellenreformáció.",
        "kviz": [{"k": "Luther 1517-ben tűzte ki 95 tételét Wittenbergben.", "v": True, "m": "Reformáció kezdete."}]
    },
    "26. Az angol alkotmányos monarchia kialakulása a XVII. században": {
        "alcim": "A Stuart-házi absolutizmus kísérlete, polgárháború, Cromwell és az 1689-es Jognyilatkozat",
        "kulcsszavak": ["Angol polgárháború", "Cromwell", "Dicsőséges forradalom (1688)", "Jognyilatkozat (1689)"],
        "audio_szoveg": "A 17. századi Angliában a parlament és a király összecsapásából született az alkotmányos monarchia...",
        "vazlat": "### I. Polgárháború, Cromwell -> II. 1688 Dicsőséges forradalom -> III. 1689 Jognyilatkozat.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Polgárháború -> 2. Dicsőséges forradalom -> 3. Jognyilatkozat.",
        "kviz": [{"k": "Az 1689-es Jognyilatkozat fektette le az alkotmányos monarchia alapjait.", "v": True, "m": "Parlament fennhatósága."}]
    },
    "27. A francia polgári forradalom és Napóleon bukása": {
        "alcim": "A rendi gyűlés összehívása (1789), Emberi és Polgári Jogok Nyilatkozata, jakobinus diktatúra és Napóleon",
        "kulcsszavak": ["1789 Bastille", "Jogok Nyilatkozata", "Jakobinus terror", "Napóleon"],
        "audio_szoveg": "1789-ben Franciaországban kitört a modern európai történelem legnagyobb forradalma...",
        "vazlat": "### I. 1789 júliusa, Bastille -> II. Jakobinus terror -> III. Napóleon birodalma.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Forradalom -> 2. Terror -> 3. Napóleon.",
        "kviz": [{"k": "A Bastille ostromával kezdődött az 1789-es francia forradalom.", "v": True, "m": "Július 14."}]
    },
    "28. Az ipari forradalmak hullámai és a munkáskérdés": {
        "alcim": "Gőzgép, gyári ipar, urbanizáció, vasútépítés és a szocialista eszmék születése",
        "kulcsszavak": ["Watt gőzgépe", "Második ipari forradalom", "Urbanizáció", "Marxizmus"],
        "audio_szoveg": "Az ipari forradalmak átalakították az emberiség termelési módját...",
        "vazlat": "### I. I. ipari forradalom (gőzgép, vasút) -> II. II. ipari forradalom (elektromosság) -> III. Munkáskérdés, marxizmus.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Gőzgép -> 2. Urbanizáció -> 3. Munkáskérdés.",
        "kviz": [{"k": "James Watt tökéletesítette a gőzgépet.", "v": True, "m": "Ipari forradalom alapja."}]
    },
    "29. Az európai integráció és a globalizáció kezdetei": {
        "alcim": "A Schuman-terv, az EGK, az Európai Unió megalakulása (Maastrichti szerződés) és globalizáció",
        "kulcsszavak": ["Schuman-terv (1950)", "Római szerződés (1957)", "Maastricht (1992)", "Globalizáció"],
        "audio_szoveg": "A II. vh után Európa államai elindították az integrációs folyamatot...",
        "vazlat": "### I. Schuman-terv, EGK -> II. 1992 Maastrichti szerződés (EU) -> III. Globalizáció.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kezdetek -> 2. EU megalakulása -> 3. Globalizáció.",
        "kviz": [{"k": "Az 1992-es Maastrichti szerződés hozta létre az EU-t.", "v": True, "m": "Megalapozta az uniót."}]
    },
    "30. A jelenkori világ globális kihívásai (klímaváltozás, migráció, információs társadalom)": {
        "alcim": "Környezeti válság, demográfiai folyamatok és a digitális kor kérdései",
        "kulcsszavak": ["Klímaváltozás", "Fenntartható fejlődés", "Migráció", "Információs társadalom"],
        "audio_szoveg": "A 21. század elején az emberiség globális kihívásokkal szembesül...",
        "vazlat": "### I. Klímaváltozás és fenntarthatóság -> II. Migrációs hullámok -> III. Információs társadalom (AI, fake news).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klímaválság -> 2. Migráció -> 3. Digitális kor.",
        "kviz": [{"k": "A fenntartható fejlődés védi a jövő generációinak esélyeit.", "v": True, "m": "Ökológiai alapelv."}]
    }
}

tetelek_matek = {
    "1. Halmazok, logika és kombinatorika": {
        "alcim": "Halmazműveletek, De Morgan azonosságok, permutáció, variáció és kombináció",
        "kulcsszavak": ["Metszet, Unió, Különbség", "Venn-diagram", "Permutáció ($n!$)", "Kombináció ($\binom{n}{k}$)"],
        "audio_szoveg": "A halmazelmélet és a kombinatorika a modern matematika alapvető eszköztára a kiválasztási feladatokhoz...",
        "vazlat": "### I. Halmazműveletek: Unió, Metszet, Különbség, Komplementer.\n### II. Kombinatorika:\n- Permutáció: Pn = n!\n- Variáció (sorrend számít): V = n! / (n-k)!\n- Kombináció (sorrend NEM számít): C = n alatt a k = n! / (k!(n-k)!).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Halmazok és műveletek -> 2. Permutáció képlete -> 3. Variáció vs. Kombináció -> 4. Lottópélda.",
        "kviz": [{"k": "Az 5-ös lottó kihúzásainak száma kombinációval számítható (90 alatt az 5).", "v": True, "m": "A sorrend nem számít."}]
    },
    "2. Algebra: Egyenletek, egyenlőtlenségek és másodfokú formula": {
        "alcim": "Megoldóképlet, diszkrimináns, gyöktényezős szorzat és Viéte-formulák",
        "kulcsszavak": ["Diszkrimináns ($b^2 - 4ac$)", "Megoldóképlet", "Gyöktényezős alak", "Kikötések"],
        "audio_szoveg": "A másodfokú egyenletek megoldásának alapeszköze a megoldóképlet és a diszkrimináns vizsgálata...",
        "vazlat": "### I. Megoldóképlet: x1,2 = (-b +- gyök(b^2 - 4ac)) / (2a).\n### II. Diszkrimináns (D = b^2 - 4ac): D > 0 (2 gyök), D = 0 (1 gyök), D < 0 (nincs valós gyök).\n### III. Gyöktényezős alak: a(x - x1)(x - x2) = 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Kikötések -> 2. Másodfokú megoldóképlet és diszkrimináns -> 3. Gyöktényezős alak -> 4. Ellenőrzés.",
        "kviz": [{"k": "Ha a diszkrimináns negatív, a másodfokú egyenletnek nincs valós gyöke.", "v": True, "m": "Negatívból nincs valós négyzetgyök."}]
    },
    "3. Hatványozás, gyökvonás és a logaritmus azonosságai": {
        "alcim": "Hatványozási azonosságok, törtkitevő, logaritmus fogalma és műveleti szabályai",
        "kulcsszavak": ["$a^n \\cdot a^m = a^{n+m}$", "Törtkitevő", "Logaritmus azonosságok", "Alapáttérés"],
        "audio_szoveg": "A hatványozás és a logaritmus egymás inverz műveletei...",
        "vazlat": "### I. Hatványozás: a^n * a^m = a^(n+m), a^n / a^m = a^(n-m), (a^n)^m = a^(n*m), a^-n = 1/a^n, Törtkitevő: a^(m/n) = n-edik gyök(a^m).\n### II. Logaritmus: log_a(x * y) = log_a(x) + log_a(y), log_a(x / y) = log_a(x) - log_a(y), log_a(x^k) = k * log_a(x).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Hatványozás szabályai -> 2. Törtkitevő -> 3. Logaritmus definíciója -> 4. Logaritmus azonosságai.",
        "kviz": [{"k": "log2(8) értéke pontosan 3.", "v": True, "m": "Mert 2 a 3. hatványon 8."}]
    },
    "4. Függvénytan és analízis alapjai": {
        "alcim": "Lineáris, másodfokú, exponenciális, logaritmikus függvények és jellemzésük",
        "kulcsszavak": ["Értelmezési tartomány", "Értékkészlet", "Zérushely", "Szélsőérték", "Monotonitás"],
        "audio_szoveg": "A függvény egy egyértelmű hozzárendelés két halmaz között...",
        "vazlat": "### I. Jellemzési lépések: Értelmezési tartomány (Df), Értékkészlet (Rf), Zérushely (f(x)=0), Szélsőérték (min/max), Monotonitás, Paritás.\n### II. Transzformációk: f(x)+c (függőleges), f(x-d) (vízszintes), c*f(x) (nyújtás).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Függvény fogalma -> 2. Jellemzési szempontok -> 3. Transzformációk -> 4. Parabola csúcsa.",
        "kviz": [{"k": "Az f(x) = (x - 4)^2 függvény minimuma az x = +4 pontban van.", "v": True, "m": "A zárójelen belüli -4 jobbra tolja el a csúcsot."}]
    },
    "5. Sorozatok és Pénzügyi matematika": {
        "alcim": "Számtani és mértani sorozat képletei, kamatos kamat és gyűjtőjáradék",
        "kulcsszavak": ["Differencia ($d$)", "Hányados ($q$)", "$n$-edik tag képlete", "Összegképlet ($S_n$)", "Kamatos kamat"],
        "audio_szoveg": "A számtani és mértani sorozatok törvényszerűségei alapozzák meg a pénzügyi kamatszámításokat...",
        "vazlat": "### I. Számtani sorozat (d): an = a1 + (n - 1)d, Sn = ((a1 + an) / 2) * n.\n### II. Mértani sorozat (q): an = a1 * q^(n - 1), Sn = a1 * (q^n - 1) / (q - 1).\n### III. Kamatos kamat: Cn = C0 * (1 + p/100)^n.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Számtani sorozat -> 2. Mértani sorozat -> 3. Kamatos kamat képlete.",
        "kviz": [{"k": "Ha a1 = 5 és d = 3, akkor a számtani sorozat 10. tagja 32.", "v": True, "m": "a10 = 5 + 9 * 3 = 32."}]
    },
    "6. Síkgeometria és Trigonometria": {
        "alcim": "Pitagorasz-tétel, Szinusz- és Koszinusztétel, háromszögek területszámítása",
        "kulcsszavak": ["Pitagorasz-tétel", "Szögfüggvények (sin, cos, tg)", "Szinusztétel", "Koszinusztétel", "Területképletek"],
        "audio_szoveg": "A síkgeometria alapja a derékszögű és általános háromszögek összefüggéseinek ismerete...",
        "vazlat": "### I. Derékszögű háromszög: a^2 + b^2 = c^2, sin, cos, tg definíciói.\n### II. Általános háromszög: Szinusztétel (a/sinA = b/sinB = 2R), Koszinusztétel (a^2 = b^2 + c^2 - 2bc*cosA).\n### III. Terület: T = (a * ma)/2 = (a*b*sinGamma)/2.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Szögfüggvények -> 2. Szinusz- és Koszinusztétel -> 3. Területképletek.",
        "kviz": [{"k": "A koszinusztétel bármilyen általános háromszögre alkalmazható két oldal és a közbezárt szög ismeretében.", "v": True, "m": "Pitagorasz általánosítása."}]
    },
    "7. Síkgeometria: Sokszögek, kör és négyszögek tulajdonságai": {
        "alcim": "Szabályos sokszögek belső szögei, deltoid, rombusz, trapéz, kör ívhossza és körcikk területe",
        "kulcsszavak": ["Belső szögek összege ($(n-2)\\cdot 180^\\circ$)", "Átlók száma", "Trapéz területe", "Rombusz", "Körcikk területe"],
        "audio_szoveg": "A sokszögek és négyszögek geometriája az érettségi írásbeli vizsga gyakori feladattípusa...",
        "vazlat": "### I. Sokszögek: Belső szögek összege: (n - 2) * 180 fok; Átlók száma: n(n - 3) / 2.\n### II. Négyszögek: Trapéz területe: ((a + c)/2) * m; Rombusz/Deltoid területe: (e * f) / 2.\n### III. Kör részei: Ívhossz: i = (2r*pi*alfa)/360; Körcikk területe: T = (r^2*pi*alfa)/360.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Belső szögek és átlók -> 2. Négyszögek területképletei -> 3. Kör és körcikk.",
        "kviz": [{"k": "Egy konvex ötszög belső szögeinek összege pontosan 540 fok.", "v": True, "m": "(5 - 2) * 180 = 540 fok."}]
    },
    "8. Koordinátageometria": {
        "alcim": "Vektorműveletek, felezőpont, súlypont, az egyenes és a kör egyenlete",
        "kulcsszavak": ["Normálvektor $\\vec{n}(A, B)$", "Irányvektor $\\vec{v}(v_1, v_2)$", "Egyenes egyenlete", "Kör egyenlete"],
        "audio_szoveg": "A koordinátageometria segítségével algebrai egyenletekkel írhatunk le geometriai alakzatokat...",
        "vazlat": "### I. Alapok: Távolság (d = gyök((x2-x1)^2 + (y2-y1)^2)), Felezőpont.\n### II. Egyenes egyenlete: Normálvektoros alak: Ax + By = Ax0 + By0.\n### III. Kör egyenlete: (x - u)^2 + (y - v)^2 = r^2 (Középpont: K(u, v), sugár: r).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Távolság és felezőpont -> 2. Egyenes egyenlete -> 3. Kör egyenlete.",
        "kviz": [{"k": "A (x - 3)^2 + (y + 1)^2 = 25 egyenletű kör sugara r = 5.", "v": True, "m": "Mert r^2 = 25 -> r = 5."}]
    },
    "9. Térgeometria (Testek felszíne és térfogata)": {
        "alcim": "Hasáb, henger, gúla, kúp és gömb felszín- és térfogatszámítása",
        "kulcsszavak": ["Henger", "Kúp", "Gúla", "Gömb", "Felszín ($A$)", "Térfogat ($V$)"],
        "audio_szoveg": "A térgeometria a háromdimenziós testek metrikus tulajdonságaival foglalkozik...",
        "vazlat": "### I. Henger: V = r^2 * pi * M, A = 2*r^2*pi + 2*r*pi*M.\n### II. Kúp és Gúla: V = (Talap * M) / 3, Kúp palástja: r * pi * a.\n### III. Gömb: V = 4/3 * R^3 * pi, A = 4 * R^2 * pi.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Egyenes testek -> 2. Csúcsos testek harmadoló szabálya -> 3. Gömb képletei.",
        "kviz": [{"k": "A kúp térfogata a henger térfogatának egyharmada.", "v": True, "m": "Ott van az 1/3 szorzó."}]
    },
    "10. Valószínűségszámítás és Statisztika": {
        "alcim": "Klasszikus valószínűség, binomiális eloszlás, átlag, medián, módusz és szórás",
        "kulcsszavak": ["Kedvező / Összes", "Binomiális eloszlás", "Medián", "Módusz", "Átlag", "Szórás"],
        "audio_szoveg": "A valószínűségszámítás a véletlen események modellezését végzi...",
        "vazlat": "### I. Valószínűség: P = Kedvező / Összes. Binomiális: P(X=k) = (n alatt k) * p^k * (1-p)^(n-k).\n### II. Statisztika: Átlag, Módusz (leggyakoribb), Medián (rendezett sor közepe), Terjedelem, Szórás.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Klasszikus valószínűség -> 2. Binomiális modell -> 3. Statisztikai középértékek -> 4. Szórás.",
        "kviz": [{"k": "A medián meghatározásához először mindig nagyság szerinti sorba kell rendezni az adatokat.", "v": True, "m": "A rendezett minta középső eleme."}]
    },
    "11. Gráfelméleti alapfogalmak és alkalmazások": {
        "alcim": "Csúcsok, élek, fokszámok összege, összefüggő gráfok, fák és Euler-vonal",
        "kulcsszavak": ["Fokszámtétel ($\\sum d(v) = 2e$)", "Egyszerű gráf", "Összefüggő gráf", "Fa gráf", "Teljes gráf"],
        "audio_szoveg": "A gráfelmélet csúcsok és az azokat összekötő élek hálózatát vizsgálja...",
        "vazlat": "### I. Alapok: Csúcsok (V), Élek (E), Csúcs fokszáma (d(v)). Fokszámtétel: Fokszámok összege = 2 * élek száma.\n### II. Típusok: Teljes gráf (Kn = n*(n-1)/2 él), Fa gráf (összefüggő, körmentes, n csúcshoz n-1 él), Euler-vonal.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Gráf fogalma -> 2. Fokszámtétel -> 3. Teljes gráf és Fa gráf -> 4. Euler-vonal.",
        "kviz": [{"k": "Egy gráfban nem lehet páratlan számú páratlan fokszámú csúcs.", "v": True, "m": "A fokszámösszeg mindig páros."}]
    },
    "12. Exponenciális és logaritmikus egyenletek": {
        "alcim": "Azonos alapra hozás módszere, logaritmálás, új ismeretlen bevezetése",
        "kulcsszavak": ["Közös alapra hozás", "Szigorú monotonitás", "Új változó", "Értelmezési tartomány"],
        "audio_szoveg": "Az exponenciális és logaritmusos egyenletek megoldásakor a szigorú monotonitás a kulcs...",
        "vazlat": "### I. Exponenciális: Azonos alapra hozás (a^f(x) = a^g(x) -> f(x) = g(x)), Új ismeretlen bevezetése (u = a^x).\n### II. Logaritmusos: Kikötés kötelező (belső szám > 0!), logaritmus azonosságok összevonása, ellenőrzés.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Exponenciális azonos alapra hozása -> 2. Új változó -> 3. Logaritmusos kikötések -> 4. Monotonitás.",
        "kviz": [{"k": "A 2^x = 16 egyenlet megoldása x = 4.", "v": True, "m": "Mert 2 a 4. hatványon 16."}]
    },
    "13. Trigonometrikus egyenletek": {
        "alcim": "Alap szögfüggvényes egyenletek megoldása a periodicitás figyelembevételével",
        "kulcsszavak": ["Periodicitás", "Két megoldássorozat", "Egységkör", "$\\sin^2 x + \\cos^2 x = 1$"],
        "audio_szoveg": "A szögfüggvényes egyenleteknél a megoldások periodikus sorozatokat alkotnak...",
        "vazlat": "### I. Azonosság: sin^2(x) + cos^2(x) = 1, tg(x) = sin(x)/cos(x).\n### II. Megoldások periodicitással:\n- sin(x) = c -> x1 = alfa + k*360 fok, x2 = 180 - alfa + k*360 fok.\n- cos(x) = c -> x1 = alfa + k*360 fok, x2 = -alfa + k*360 fok.\n- tg(x) = c -> x = alfa + k*180 fok.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Egységkör szimmetriái -> 2. Szinusz két ága -> 3. Koszinusz két ága -> 4. Periodicitás.",
        "kviz": [{"k": "A tg(x) függvény periódusa 180 fok.", "v": True, "m": "Míg a sin és cos periódusa 360 fok."}]
    },
    "14. Vektorműveletek és a skaláris szorzat": {
        "alcim": "Összeadás, kivonás, számmal szorzás, skaláris szorzat és két vektor hajlásszöge",
        "kulcsszavak": ["Vektor koordinátái", "Skaláris szorzat", "Hajlásszög", "Merőlegesség"],
        "audio_szoveg": "Két vektor skaláris szorzata valós számot eredményez...",
        "vazlat": "### I. Vektorműveletek: a + b = (a1+b1, a2+b2), |a| = gyök(a1^2 + a2^2).\n### II. Skaláris szorzat: a * b = a1*b1 + a2*b2 = |a| * |b| * cos(fi).\n### III. Merőlegesség: Két vektor merőleges, ha skaláris szorzatuk 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Vektor koordinátái -> 2. Skaláris szorzat -> 3. Hajlásszög -> 4. Merőlegesség.",
        "kviz": [{"k": "Ha két vektor skaláris szorzata 0, a két vektor merőleges egymásra.", "v": True, "m": "Mert cos(90 fok) = 0."}]
    },
    "15. Számelmélet: Oszthatóság, prímek, LNKO és LKKT": {
        "alcim": "Oszthatósági szabályok, a számelmélet alaptétele, legnagyobb közös osztó és legkisebb közös többszörös",
        "kulcsszavak": ["Prímszám", "Számelmélet alaptétele", "LNKO", "LKKT"],
        "audio_szoveg": "A számelmélet az egész számok oszthatósági tulajdonságait vizsgálja...",
        "vazlat": "### I. Oszthatóság: 2, 5, 10; 4, 25; 3, 9 szabályai.\n### II. Számelmélet alaptétele: Egyértelmű prímtényezős felbontás.\n### III. LNKO (közös prímek legkisebb hatványon), LKKT (összes prím legnagyobb hatványon).",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Oszthatósági szabályok -> 2. Prímtényezős felbontás -> 3. LNKO és LKKT -> 4. Törtek egyszerűsítése.",
        "kviz": [{"k": "A 12 és 18 legnagyobb közös osztója (LNKO) a 6.", "v": True, "m": "12 = 2^2 * 3 és 18 = 2 * 3^2 -> LNKO = 6."}]
    },
    "16. Differenciálszámítás (Deriválás) bevezetése": {
        "alcim": "A differenciahányados, derivált fogalma, hatványfüggvény deriválása és érintő meredeksége",
        "kulcsszavak": ["Érintő meredeksége", "Deriválási szabályok", "Szélsőértékkeresés ($f'(x) = 0$)"],
        "audio_szoveg": "A differenciálszámítás a függvények változási sebességét és az érintő meredekségét vizsgálja...",
        "vazlat": "### I. Geometriai jelentés: f'(x0) az érintő meredeksége (m).\n### II. Szabályok: (c)' = 0, (x^n)' = n * x^(n-1).\n### III. Szélsőérték: Ahol a függvénynek szélsőértéke van, ott f'(x) = 0.",
        "szobeli": "**🎙️ 3 perces felelet:** 1. Derivált geometriai jelentése -> 2. Hatványfüggvény deriválása -> 3. Szélsőérték feltétele.",
        "kviz": [{"k": "Az f(x) = x^4 függvény deriváltja f'(x) = 4x^3.", "v": True, "m": "A kitevő szorzóvá válik, a hatvány 1-gyel csökken."}]
    }
}

flashcards_irodalom = [
    {"q": "Mit jelent a ballada Greguss Ágost-féle meghatározása?", "a": "„Tragédia dalban elbeszélve” – egyesíti a líra, epika és dráma sajátosságait."},
    {"q": "Melyik évben indult a Nyugat folyóirat és ki volt a szerkesztője?", "a": "1908-ban indult, Osvát Ernő szerkesztette."},
    {"q": "Mi a központi szállóige Babits 'Jónás könyvében'?", "a": "„Mert vétkesek közt cinkos, aki néma.”"}
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

timeline_irodalom = [{"ev": "1848–1849", "cim": "Forradalom lírája", "leiras": "Petőfi és Arany."}, {"ev": "1908", "cim": "Nyugat", "leiras": "Ady és a modern líra."}]
timeline_nyelvtan = [{"ev": "1055", "cim": "Tihany", "leiras": "Szórványemlék."}, {"ev": "1790–1820", "cim": "Nyelvújítás", "leiras": "Kazinczy."}]
timeline_tortenelem = [{"ev": "1000", "cim": "Államalapítás", "leiras": "Szent István."}, {"ev": "1526", "cim": "Mohács", "leiras": "Középkori állam bukása."}]
timeline_matek = [{"ev": "Kr. e. VI.", "cim": "Pitagorasz", "leiras": "Derékszögű háromszög."}, {"ev": "1687", "cim": "Newton", "leiras": "Deriválás."}]

detektiv_irodalom = [
    {"idezet": "„Mert vétkesek közt cinkos, aki néma...”", "helyes": "Babits Mihály: Jónás könyve", "opciok": ["Babits Mihály: Jónás könyve", "Ady Endre: Új versek", "Arany János: Toldi", "Radnóti Miklós"], "info": "A felelősségvállalás parancsa."},
    {"idezet": "„Ha férfi vagy, légy férfi, / S ne hitvány, lomha báb...”", "helyes": "Petőfi Sándor: Ha férfi vagy, légy férfi", "opciok": ["Petőfi Sándor: Ha férfi vagy, légy férfi", "Vörösmarty Mihály: Szózat", "Arany János", "Ady Endre"], "info": "Petőfi forradalmi felhívó lírája."},
    {"idezet": "„Mondottam, ember: küzdj és bízva bízzál!”", "helyes": "Madách Imre: Az ember tragédiája", "opciok": ["Madách Imre: Az ember tragédiája", "Arany János", "Vörösmarty", "Katona József"], "info": "Az Úr szózata a 15. színben."},
    {"idezet": "„Góg és Magóg fia vagyok én, / Hiába döngetek kaput, falat...”", "helyes": "Ady Endre: Góg és Magóg fia vagyok én...", "opciok": ["Ady Endre: Góg és Magóg fia vagyok én...", "Babits Mihály", "József Attila", "Kosztolányi"], "info": "Ady 1906-os kötetének nyitóverse."},
    {"idezet": "„Békévé oldja az emlékezés, / hogy tamáskodunk s jól van ez így errefelé.”", "helyes": "József Attila: A Dunánál", "opciok": ["József Attila: A Dunánál", "Radnóti Miklós", "Babits Mihály", "Vajda János"], "info": "Történelmi szembenézés verse."},
    {"idezet": "„Isten csodája vagyok, / Fényes, tiszta láng...”", "helyes": "Csokonai Vitéz Mihály: A Reményhez", "opciok": ["Csokonai Vitéz Mihály: A Reményhez", "Berzsenyi Dániel", "Petőfi Sándor", "Vörösmarty"], "info": "A remény elvesztésének mesterműve."},
    {"idezet": "„Itt ül a nyakunkon a német, / Koreszmék kútfejénél lassan rág...”", "helyes": "Vajda János: A virrasztók", "opciok": ["Vajda János: A virrasztók", "Ady Endre", "Illyés Gyula", "Petőfi Sándor"], "info": "Vajda társadalombírálata."},
    {"idezet": "„Rám zúdult a kietlen, nyers valóság, / S a mindenség szörnyű titka megütött.”", "helyes": "Kosztolányi Dezső: Boldog, szomorú dal", "opciok": ["Kosztolányi Dezső: Boldog, szomorú dal", "Babits Mihály", "Tóth Árpád", "Juhász Gyula"], "info": "Létösszegző versek."},
    {"idezet": "„Hol sírjaink domborulnak, / Unokáink lesiratják...”", "helyes": "Vörösmarty Mihály: Szózat", "opciok": ["Vörösmarty Mihály: Szózat", "Petőfi Sándor", "Kölcsey Ferenc", "Berzsenyi Dániel"], "info": "Nemzeti összetartozás kiáltványa."},
    {"idezet": "„Oly korban éltem e földön, / mikor az ember úgy elvadult...”", "helyes": "Radnóti Miklós: Töredék", "opciok": ["Radnóti Miklós: Töredék", "Babits Mihály", "József Attila", "Kosztolányi"], "info": "Megőrzött humánum."}
]

detektiv_nyelvtan = [
    {"idezet": "„barátság [kiejtve: baraccság]”", "helyes": "Összeolvadás mássalhangzótörvény", "opciok": ["Összeolvadás mássalhangzótörvény", "Zöngésségi részleges hasonulás", "Írásban jelölt teljes hasonulás", "Mássalhangzó-kiesés"], "info": "t + s -> [ccs]."},
    {"idezet": "„lila dalra kelt az éjcsend”", "helyes": "Szinesztézia (Költői kép)", "opciok": ["Szinesztézia (Költői kép)", "Megszemélyesítés", "Metonímia", "Szinekdoché"], "info": "Érzékkeverés."},
    {"idezet": "„vasgolyó [vazsgolyó]”", "helyes": "Zöngésség szerinti részleges hasonulás", "opciok": ["Zöngésség szerinti részleges hasonulás", "Képzés helye szerinti hasonulás", "Teljes hasonulás", "Összeolvadás"], "info": "Zöngésítés."},
    {"idezet": "„ház-as-ság-ok-at”", "helyes": "Szótő + Képző + Képző + Jel + Rag", "opciok": ["Szótő + Képző + Képző + Jel + Rag", "Szótő + Jel + Rag + Képző", "Szótő + Rag + Jel + Képző", "Szótő + Képző + Rag + Jel"], "info": "Kötött sorrend."},
    {"idezet": "„MÁV, OTP, ELTE”", "helyes": "Betűszók (Mozaikszók)", "opciok": ["Betűszók (Mozaikszók)", "Szóösszevonások", "Szóelvonások", "Betűszerkezetek"], "info": "Kezdőbetűk."},
    {"idezet": "„Főgáz, Malév”", "helyes": "Szóösszevonások", "opciok": ["Szóösszevonások", "Betűszók", "Mozaikszók", "Csonkítások"], "info": "Szótagok."},
    {"idezet": "„A kutyából nem lesz szalonna.”", "helyes": "Közmondás", "opciok": ["Közmondás", "Szólás", "Szállóige", "Kontextus"], "info": "Tanulság."},
    {"idezet": "„Feni a fogát valamire.”", "helyes": "Szólás", "opciok": ["Szólás", "Közmondás", "Szállóige", "Metafora"], "info": "Képszerű."},
    {"idezet": "„A kocka el van vetve.”", "helyes": "Szállóige", "opciok": ["Szállóige", "Közmondás", "Szólás", "Közhely"], "info": "Caesar."},
    {"idezet": "„egészségünkre / egéssségünkre”", "helyes": "Helyesírás és kiejtés eltérése (Kiejtés elve)", "opciok": ["Helyesírás és kiejtés eltérése (Kiejtés elve)", "Hagyomány elve", "Szóelemzés elve", "Egyszerűsítés elve"], "info": "Kiejtés."}
]

detektiv_tortenelem = [
    {"idezet": "„Ius resistendi (A nemesek joga az ellenállásra)”", "helyes": "Az 1222-es Aranybulla 31. cikkelye", "opciok": ["Az 1222-es Aranybulla 31. cikkelye", "Nagy Lajos 1351", "Szent István", "Kollonics"], "info": "Rendi szabadságjog."},
    {"idezet": "„Eb ura fakó, József császár nem királyunk!”", "helyes": "1707-es Ónodi országgyűlés (Trónfosztás)", "opciok": ["1707-es Ónodi országgyűlés (Trónfosztás)", "1849", "1526", "1608"], "info": "Habsburg-trónfosztás."},
    {"idezet": "„Aki nincs ellenünk, az velünk van.”", "helyes": "Kádár-rendszer konszolidációs politikája", "opciok": ["Kádár-rendszer konszolidációs politikája", "Rákosi-diktatúra", "Horthy", "Bethlen"], "info": "Megegyezés."},
    {"idezet": "„Minden tíz falu építsen egy templomot...”", "helyes": "Szent István király törvényei", "opciok": ["Szent István király törvényei", "Szent László", "Könyves Kálmán", "II. András"], "info": "Egyházszervezet."},
    {"idezet": "„Segédlettel, pénzzel támogatjuk a szabad nemzeteket...”", "helyes": "Truman-doktrína (1947)", "opciok": ["Truman-doktrína (1947)", "Brezsnyev", "Marshall", "Molotov"], "info": "Megfékezési politika."},
    {"idezet": "„Békévé oldja az emlékezés...”", "helyes": "A reformkor és polgári átalakulás", "opciok": ["A reformkor és polgári átalakulás", "Kiegyezés", "Trianon", "Rendszerváltás"], "info": "Megbékélés."},
    {"idezet": "„Az ország területének 2/3 része elcsatolva.”", "helyes": "Trianoni békediktátum (1920)", "opciok": ["Trianoni békediktátum (1920)", "Párizsi béke", "Szatmár", "Pozsony"], "info": "Katasztrofális béke."},
    {"idezet": "„Cél a proletárdiktatúra és földek államosítása.”", "helyes": "1919-es Magyar Tanácsköztársaság", "opciok": ["1919-es Magyar Tanácsköztársaság", "1956", "1989", "1848"], "info": "Kommunista kísérlet."},
    {"idezet": "„Szabad, felelős magyar kormány Batthyány vezetésével.”", "helyes": "1848-as forradalom és áprilisi törvények", "opciok": ["1848-as forradalom és áprilisi törvények", "1867", "1918", "1944"], "info": "Független Magyarország."},
    {"idezet": "„A szocialista tábor védelmében katonai beavatkozás.”", "helyes": "Brezsnyev-doktrína", "opciok": ["Brezsnyev-doktrína", "Truman", "Eisenhower", "Monroe"], "info": "Korlátozott szuverenitás."}
]

detektiv_matek = [
    {"idezet": "a² = b² + c² - 2bc · cos(α)", "helyes": "Koszinusztétel (Általános háromszögekre)", "opciok": ["Koszinusztétel (Általános háromszögekre)", "Szinusztétel", "Pitagorasz", "Héron"], "info": "Pitagorasz általánosítása."},
    {"idezet": "(x^n)' = n · x^(n-1)", "helyes": "Hatványfüggvény deriválási szabálya", "opciok": ["Hatványfüggvény deriválási szabálya", "Logaritmus", "Binomiális", "Sorozat"], "info": "Differenciálás."},
    {"idezet": "V = (r²π · M) / 3", "helyes": "Egyenes körkúp térfogatképlete", "opciok": ["Egyenes körkúp térfogatképlete", "Henger", "Gömb", "Gúla"], "info": "Körkúp térfogat."},
    {"idezet": "∑ d(v) = 2 · e", "helyes": "Gráfelméleti fokszámtétel (Kézfogási lemma)", "opciok": ["Gráfelméleti fokszámtétel (Kézfogási lemma)", "Euler", "De Morgan", "Binomiális"], "info": "Fokszámtétel."},
    {"idezet": "x1,2 = (-b ± √(b² - 4ac)) / (2a)", "helyes": "Másodfokú egyenlet megoldóképlete", "opciok": ["Másodfokú egyenlet megoldóképlete", "Viéte", "Diszkrimináns", "Gyöktényezős"], "info": "Megoldóképlet."},
    {"idezet": "an = a1 + (n - 1)d", "helyes": "Számtani sorozat n-edik tagjának képlete", "opciok": ["Számtani sorozat n-edik tagjának képlete", "Mértani", "Kamatos", "Összegképlet"], "info": "Számtani sorozat."},
    {"idezet": "P(A) = Kedvező / Összes", "helyes": "Klasszikus valószínűség kiszámítása", "opciok": ["Klasszikus valószínűség kiszámítása", "Binomiális", "Szórás", "Kombináció"], "info": "Valószínűség."},
    {"idezet": "sin²(x) + cos²(x) = 1", "helyes": "Trigonometrikus alapazonosság", "opciok": ["Trigonometrikus alapazonosság", "Szinusz", "Koszinusz", "Tangens"], "info": "Alapazonosság."},
    {"idezet": "a · b = |a| · |b| · cos(α)", "helyes": "Két vektor skaláris szorzata", "opciok": ["Két vektor skaláris szorzata", "Összeadás", "Vektorhossz", "Hajlásszög"], "info": "Skaláris szorzat."},
    {"idezet": "Cn = C0 · (1 + p/100)^n", "helyes": "Kamatos kamat számítási képlete", "opciok": ["Kamatos kamat számítási képlete", "Egyszerű kamat", "Gyűjtőjáradék", "Mértani összeg"], "info": "Kamatos kamat."}
]
