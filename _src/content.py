"""victseng.com v2 copy. Short by design.
Rules: current employer never named; media pieces listed as index only (no reuse of submitted text)."""

DOMAIN = "https://victseng.com"
EMAIL = "victseng.consult@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/victortsengtw/"
LANGS = ["zh", "en", "fr"]
PATHS = {"zh": "/", "en": "/en/", "fr": "/fr/"}
HREFLANG = {"zh": "zh-Hant", "en": "en", "fr": "fr"}
LANG_LABEL = {"zh": "中", "en": "EN", "fr": "FR"}
TNL_1 = "https://www.thenewslens.com/article/269647"

C = {}

C["zh"] = dict(
    html_lang="zh-Hant", og_locale="zh_TW",
    title="曾浩瑜 Victor Tseng｜非洲 × 亞洲 跨文化市場開發",
    description="曾浩瑜（Victor Tseng），駐點象牙海岸阿比讓（Abidjan，又譯阿比尚）的跨文化市場開發顧問。專長：非洲藝術與品味、生活風格、跨文化溝通、非洲商業與市場。",
    job_title="跨文化市場開發顧問",
    nav=[("expertise", "專長"), ("work", "作品"), ("notes", "專欄"), ("press", "媒體"), ("experience", "經歷"), ("contact", "聯絡")],
    h1="讀懂非洲的<br>藝術、生活與生意",
    domains=["非洲藝術", "生活風格", "跨文化溝通", "非洲商業"],
    who="曾浩瑜 Victor Tseng",
    role="跨文化市場開發顧問",
    one="在亞洲、歐洲與西非工作過，現在住在阿比讓。幫亞洲的人與企業，看懂一個陌生市場。",
    cta1="預約諮詢", cta2="看作品",
    photo_alt="曾浩瑜在阿比讓街頭，穿著西非窄幅手織布上衣",
    stats=[("€960K", "整合行銷專案預算，由我統籌執行"), ("17場", "展覽與大型活動，一年內完成"), ("11國", "國際市場標竿研究，一次完成"), ("7+年", "國際行銷與市場開發經驗，橫跨歐、亞、非")],
    sec_expertise="專長", sec_expertise_t="四個領域，一個目標：讀懂一個地方。",
    pillars=[
        ("非洲藝術與品味", "看懂作品、工藝與禮儀背後的故事。", ["品味導覽", "文化行程", "送禮建議"]),
        ("生活風格", "阿比讓的餐桌、音樂與夜生活，安排有內容的旅程與接待。", ["客製行程", "VIP 接待", "旅宿體驗"]),
        ("跨文化溝通", "時間觀、說話方式、職場習慣：少誤會，多信任。", ["企業工作坊", "外派前準備", "商務陪同"]),
        ("非洲商業與市場", "用實地觀察，看懂消費者、通路與競爭。", ["市場考察", "在地商業診斷", "夥伴媒合"]),
    ],
    sec_work="作品", sec_work_t="我做的兩個作品",
    work_note="皆由我企劃，並以 AI 協作開發。",
    works=[
        dict(name="AKWABA・非洲品味之家", sub="MAISON DE GOÛT AFRICAIN", line="附出處的象牙海岸文化指南。", facts=["12 章", "36 解讀卡", "8 路線", "9 場合"], url="/akwaba-maison/?utm_source=victseng&utm_medium=website&utm_campaign=works", cta="打開指南", pat="akan", tone="ivory"),
        dict(name="《Akwaba！非洲大冒險》", sub="MOBILE WEB GAME", line="跟著亞洲旅人第一次來到西非。", facts=["15 關", "約 10–15 分鐘", "免費"], url="/akwaba/?c=site&utm_source=victseng&utm_medium=website&utm_campaign=works", cta="開始玩", pat="kita", tone="lagoon"),
    ],
    sec_writing="發表", sec_writing_t="媒體發表",
    writing_note="只列標題與連結，全文請到原媒體閱讀。",
    articles=[("2026.08.15", "關鍵評論網", "在西非職場，我重新理解「效率」", TNL_1, "")],
    sec_exp="經歷", sec_exp_t="從巴黎到阿比讓",
    jobs=[
        ("2026 —", "創辦人・策略與商業創新顧問", "維策顧問 VicTseng Consult", "阿比讓", "協助組織進入新市場、建立亞非跨文化合作。"),
        ("2022 — 26", "資深多渠道行銷專員", "無國界醫生 MSF", "台北", "多渠道行銷，協調約 40 人的外部合作團隊。"),
        ("2021 — 22", "專案經理・整合行銷", "力譔堂整合行銷", "台北", "5 項整合行銷專案，總預算 €960K；一年 17 場展覽與活動。"),
        ("2020 — 21", "數位行銷專員", "雲朗觀光 LDC Hotels", "南投", "經營 FB、IG、LINE 與官網。"),
        ("2020", "國際市場開發經理", "Funique VR", "台北", "開發歐洲策略夥伴。"),
        ("2020", "行銷與活動副理", "Terrou-Bi Resort", "達卡", "觀察亞洲旅客，提出跨文化服務建議。"),
        ("2019", "專案副理", "法國設計學院 IFD", "巴黎", "橫跨 11 國的國際標竿研究。"),
        ("2018", "客房餐飲服務", "巴黎麗茲酒店", "巴黎", "製作新人視覺化培訓指南。"),
        ("2017 — 18", "行銷與傳播助理", "Think & Do International", "巴黎", "跨城市的國際文化專案。"),
    ],
    more_jobs="更早的經歷",
    edu_t="學歷",
    edu=[("2019", "國際工商管理碩士 International MBA", "IAE Paris-Est"), ("2017", "奢侈品管理證書課程", "HEC Paris"), ("2016", "外國語文學系 學士", "國立中山大學")],
    lang_t="語言", langs="中文 母語・英文 母語程度・法文 專業工作",
    cv="完整履歷：來信索取", cv_subject="履歷索取",
    sec_contact="聯絡", contact_t="有一個陌生市場要讀懂？", contact_line="簡單寫下你的需求，我會親自回覆。",
    contact_subject="諮詢預約", email_btn="寫信預約", li_btn="LinkedIn",
    based="駐點 阿比讓・象牙海岸",
    search="搜尋", search_ph="搜尋：藝術、禮儀、市場、MBA…", search_none="找不到相關內容", search_close="關閉",
    menu_label="章節", lang_label="語言", skip="跳到主要內容", local_time="當地時間",
)

C["en"] = dict(
    html_lang="en", og_locale="en_US",
    title="Victor Tseng | Africa × Asia Cross-cultural Market Development",
    description="Victor Tseng (曾浩瑜), a cross-cultural market development consultant based in Abidjan, Côte d'Ivoire. African art & taste, lifestyle, cross-cultural communication, African business & markets.",
    job_title="Cross-cultural Market Development Consultant",
    nav=[("expertise", "Expertise"), ("work", "Work"), ("notes", "Column"), ("press", "Press"), ("experience", "Experience"), ("contact", "Contact")],
    h1="Reading Africa:<br>art, lifestyle and business",
    domains=["African art", "Lifestyle", "Cross-cultural", "African business"],
    who="Victor Tseng 曾浩瑜",
    role="Cross-cultural market development",
    one="I've worked in Asia, Europe and West Africa, and now live in Abidjan. I help Asian companies and people read an unfamiliar market.",
    cta1="Book a consultation", cta2="See my work",
    photo_alt="Victor Tseng on a street in Abidjan, wearing a West African strip-woven shirt",
    stats=[("€960K", "in integrated marketing budgets managed"), ("17", "exhibitions and public events delivered in one year"), ("11", "countries benchmarked in one international study"), ("7+", "years in international marketing and market development, across Europe, Asia and Africa")],
    sec_expertise="Expertise", sec_expertise_t="Four fields, one goal: understanding a place.",
    pillars=[
        ("African Art & Taste", "The stories behind artworks, crafts and etiquette.", ["Art & taste tours", "Cultural itineraries", "Gifting advice"]),
        ("Lifestyle", "Abidjan's tables, music and nightlife, for trips and hosting with substance.", ["Tailored trips", "VIP hosting", "Hospitality"]),
        ("Cross-cultural Communication", "Time, tone and workplace habits: fewer misunderstandings, more trust.", ["Workshops", "Pre-assignment briefings", "Meeting support"]),
        ("African Business & Markets", "Field insight on consumers, channels and competitors.", ["Market visits", "Local business diagnostics", "Partner matchmaking"]),
    ],
    sec_work="Work", sec_work_t="Two projects I made",
    work_note="Both conceived by me and built with AI-assisted development.",
    works=[
        dict(name="AKWABA · House of African Taste", sub="MAISON DE GOÛT AFRICAIN", line="A sourced guide to Ivorian culture.", facts=["12 chapters", "36 cards", "8 routes", "9 occasions"], url="/akwaba-maison/en/?utm_source=victseng&utm_medium=website&utm_campaign=works", cta="Open the guide", pat="akan", tone="ivory"),
        dict(name="Akwaba! An African Adventure", sub="MOBILE WEB GAME", line="An Asian traveller's first trip to West Africa.", facts=["15 stages", "~10–15 min", "Free"], url="/akwaba/en.html?c=site&utm_source=victseng&utm_medium=website&utm_campaign=works", cta="Play now", pat="kita", tone="lagoon"),
    ],
    sec_writing="Writing", sec_writing_t="Published articles",
    writing_note="Index only. Articles are in Chinese, on the publisher's site.",
    articles=[("2026.08.15", "The News Lens", "Rethinking “efficiency” in a West African workplace", TNL_1, "ZH")],
    sec_exp="Experience", sec_exp_t="From Paris to Abidjan",
    jobs=[
        ("2026 —", "Founder, Strategy & Business Innovation", "VicTseng Consult", "Abidjan", "Helping organisations enter new markets and build Asia–Africa partnerships."),
        ("2022 — 26", "Senior Multichannel Marketing Officer", "Médecins Sans Frontières", "Taipei", "Multichannel marketing; coordinated an external partner team of about 40."),
        ("2021 — 22", "Project Manager, Integrated Marketing", "CSR-TAIWAN Summit", "Taipei", "Five campaigns, €960K total budget; 17 exhibitions and events in a year."),
        ("2020 — 21", "Digital Marketing Specialist", "LDC Hotels & Resorts", "Nantou", "Ran Facebook, Instagram, LINE and web channels."),
        ("2020", "International Business Development Manager", "Funique VR", "Taipei", "Built strategic partnerships in Europe."),
        ("2020", "Marketing & Events Assistant Manager", "Terrou-Bi Resort", "Dakar", "Advised on service adaptation for Asian guests."),
        ("2019", "Assistant Project Manager", "Institut Français du Design", "Paris", "Benchmarking study across 11 countries."),
        ("2018", "Room Service", "Ritz Paris", "Paris", "Created a visual onboarding guide."),
        ("2017 — 18", "Marketing & Communication Assistant", "Think & Do International", "Paris", "International cultural projects across cities."),
    ],
    more_jobs="Earlier roles",
    edu_t="Education",
    edu=[("2019", "International MBA", "IAE Paris-Est"), ("2017", "Certificate, Luxury Management", "HEC Paris"), ("2016", "BA, Foreign Languages & Literature", "National Sun Yat-sen University")],
    lang_t="Languages", langs="Mandarin native · English native/bilingual · French full professional",
    cv="Full CV on request", cv_subject="CV request",
    sec_contact="Contact", contact_t="Is there a market you need to read?", contact_line="Tell me briefly what you need. I'll reply personally.",
    contact_subject="Consultation request", email_btn="Email me", li_btn="LinkedIn",
    based="Based in Abidjan · Côte d'Ivoire",
    search="Search", search_ph="Search: art, etiquette, market, MBA…", search_none="Nothing found", search_close="Close",
    menu_label="Sections", lang_label="Language", skip="Skip to content", local_time="Local time",
)

C["fr"] = dict(
    html_lang="fr", og_locale="fr_FR",
    title="Victor Tseng | Afrique × Asie, développement de marchés et interculturel",
    description="Victor Tseng (曾浩瑜), consultant en développement de marchés et interculturel basé à Abidjan, Côte d'Ivoire. Art africain, art de vivre, communication interculturelle, business et marchés africains.",
    job_title="Consultant en développement de marchés et interculturel",
    nav=[("expertise", "Expertise"), ("work", "Projets"), ("notes", "Chroniques"), ("press", "Presse"), ("experience", "Parcours"), ("contact", "Contact")],
    h1="Lire l'Afrique :<br>son art, sa vie, ses affaires",
    domains=["Art africain", "Art de vivre", "Interculturel", "Business africain"],
    who="Victor Tseng 曾浩瑜",
    role="Développement de marchés · Interculturel",
    one="J'ai travaillé en Asie, en Europe et en Afrique de l'Ouest ; je vis aujourd'hui à Abidjan. J'aide les entreprises et les professionnels asiatiques à décrypter un marché inconnu.",
    cta1="Prendre rendez-vous", cta2="Voir mes projets",
    photo_alt="Victor Tseng dans une rue d'Abidjan, vêtu d'une chemise en bandes tissées d'Afrique de l'Ouest",
    stats=[("960K€", "de budgets marketing intégré pilotés"), ("17", "salons et événements publics en un an"), ("11", "pays étudiés dans un benchmark international"), ("7+", "ans de marketing international et de développement de marchés, entre Europe, Asie et Afrique")],
    sec_expertise="Expertise", sec_expertise_t="Quatre domaines, un but : comprendre un lieu.",
    pillars=[
        ("Art africain et goût", "Les histoires derrière les œuvres, l'artisanat et les codes.", ["Visites art et goût", "Itinéraires culturels", "Conseils cadeaux"]),
        ("Art de vivre", "Tables, musique et nuits d'Abidjan, pour des séjours et un accueil qui ont du sens.", ["Séjours sur mesure", "Accueil VIP", "Hôtellerie"]),
        ("Communication interculturelle", "Temps, ton, habitudes de travail : moins de malentendus, plus de confiance.", ["Ateliers", "Préparation à l'expatriation", "Rendez-vous d'affaires"]),
        ("Business et marchés africains", "Le terrain : consommateurs, distribution, concurrence.", ["Visites de marché", "Diagnostic local", "Mise en relation"]),
    ],
    sec_work="Projets", sec_work_t="Deux projets que j'ai créés",
    work_note="Conçus par moi, développés avec l'aide de l'IA.",
    works=[
        dict(name="AKWABA · Maison de goût africain", sub="MAISON DE GOÛT AFRICAIN", line="Un guide sourcé de la culture ivoirienne.", facts=["12 chapitres", "36 fiches", "8 itinéraires", "9 occasions"], url="/akwaba-maison/fr/?utm_source=victseng&utm_medium=website&utm_campaign=works", cta="Ouvrir le guide", pat="akan", tone="ivory"),
        dict(name="Akwaba ! Une aventure africaine", sub="JEU WEB MOBILE", line="Le premier voyage d'un Asiatique en Afrique de l'Ouest.", facts=["15 étapes", "10 à 15 min", "Gratuit"], url="/akwaba/fr.html?c=site&utm_source=victseng&utm_medium=website&utm_campaign=works", cta="Jouer", pat="kita", tone="lagoon"),
    ],
    sec_writing="Articles", sec_writing_t="Articles publiés",
    writing_note="Index seulement. Articles en chinois, sur le site de l'éditeur.",
    articles=[("2026.08.15", "The News Lens", "Repenser « l'efficacité » dans un bureau d'Afrique de l'Ouest", TNL_1, "ZH")],
    sec_exp="Parcours", sec_exp_t="De Paris à Abidjan",
    jobs=[
        ("2026 —", "Fondateur, stratégie et innovation", "VicTseng Consult", "Abidjan", "Accompagner l'entrée sur de nouveaux marchés et les partenariats Asie–Afrique."),
        ("2022 — 26", "Chargé de marketing multicanal senior", "Médecins Sans Frontières", "Taipei", "Marketing multicanal ; coordination d'une équipe partenaire d'environ 40 personnes."),
        ("2021 — 22", "Chef de projet, marketing intégré", "CSR-TAIWAN Summit", "Taipei", "Cinq campagnes, 960 K€ de budget ; 17 salons et événements en un an."),
        ("2020 — 21", "Spécialiste marketing digital", "LDC Hotels & Resorts", "Nantou", "Facebook, Instagram, LINE et site web."),
        ("2020", "Responsable développement international", "Funique VR", "Taipei", "Partenariats stratégiques en Europe."),
        ("2020", "Assistant manager marketing et événements", "Terrou-Bi Resort", "Dakar", "Adaptation du service à la clientèle asiatique."),
        ("2019", "Assistant chef de projet", "Institut Français du Design", "Paris", "Benchmark international dans 11 pays."),
        ("2018", "Room service", "Ritz Paris", "Paris", "Guide visuel d'intégration."),
        ("2017 — 18", "Assistant marketing et communication", "Think & Do International", "Paris", "Projets culturels internationaux."),
    ],
    more_jobs="Expériences antérieures",
    edu_t="Formation",
    edu=[("2019", "International MBA", "IAE Paris-Est"), ("2017", "Certificat, Luxury Management", "HEC Paris"), ("2016", "Licence, langues étrangères", "Université nationale Sun Yat-sen")],
    lang_t="Langues", langs="Mandarin maternel · Anglais bilingue · Français courant professionnel",
    cv="CV complet sur demande", cv_subject="Demande de CV",
    sec_contact="Contact", contact_t="Un marché à décrypter ?", contact_line="Décrivez-moi brièvement votre besoin. Je vous répondrai personnellement.",
    contact_subject="Demande de rendez-vous", email_btn="M'écrire", li_btn="LinkedIn",
    based="Basé à Abidjan · Côte d'Ivoire",
    search="Rechercher", search_ph="Rechercher : art, codes, marché, MBA…", search_none="Aucun résultat", search_close="Fermer",
    menu_label="Sections", lang_label="Langue", skip="Aller au contenu", local_time="Heure locale",
)

EXTRA = {
    "zh": dict(
        sec_notes="專欄", sec_notes_t="讀懂非洲", notes_note="藝術、生活、跨文化與商業，每篇三到五分鐘，附出處。本站獨家，不與媒體投稿重複。",
        notes_all="看全部專欄文章", read="閱讀", min_read="分鐘",
        sec_press="媒體", sec_press_t="媒體露出", press_note="外部媒體刊出的文章，點擊到原刊登處閱讀。",
        marquee=["非洲藝術", "生活風格", "跨文化溝通", "非洲商業", "ABIDJAN", "PARIS", "TAIPEI"],
        back="回首頁", note_cta_t="想把這些變成你的行動方案？", note_cta="預約諮詢",
        notes_page_t="讀懂非洲・專欄", notes_page_d="曾浩瑜 Victor Tseng 的「讀懂非洲」專欄：非洲藝術、生活風格、跨文化溝通與非洲商業。",
        avail="也有其他語言版本", by="文", toc="目錄",
    ),
    "en": dict(
        sec_notes="Column", sec_notes_t="Reading Africa", notes_note="Art, lifestyle, cross-cultural and business: three-to-five-minute reads, always sourced. Exclusive to this site.",
        notes_all="See all articles", read="Read", min_read="min",
        sec_press="Press", sec_press_t="In the media", press_note="Articles published by other outlets. Opens on the publisher's site.",
        marquee=["African art", "Lifestyle", "Cross-cultural", "African business", "Abidjan", "Paris", "Taipei"],
        back="Home", note_cta_t="Want to turn this into a plan?", note_cta="Book a consultation",
        notes_page_t="Reading Africa · Column", notes_page_d="The Reading Africa column by Victor Tseng on African art, lifestyle, cross-cultural communication and African business.",
        avail="Also available in", by="By", toc="Contents",
    ),
    "fr": dict(
        sec_notes="Chroniques", sec_notes_t="Lire l'Afrique", notes_note="Art, art de vivre, interculturel et business : des lectures de trois à cinq minutes, toujours sourcées. Exclusives à ce site.",
        notes_all="Toutes les chroniques", read="Lire", min_read="min",
        sec_press="Presse", sec_press_t="Dans les médias", press_note="Articles publiés par d'autres médias, à lire sur le site de l'éditeur.",
        marquee=["Art africain", "Art de vivre", "Interculturel", "Business africain", "Abidjan", "Paris", "Taipei"],
        back="Accueil", note_cta_t="Envie d'en faire un plan d'action ?", note_cta="Prendre rendez-vous",
        notes_page_t="Lire l'Afrique · Chroniques", notes_page_d="Les chroniques « Lire l'Afrique » de Victor Tseng : art africain, art de vivre, interculturel et business africain.",
        avail="Aussi disponible en", by="Par", toc="Sommaire",
    ),
}
for _l in LANGS:
    C[_l].update(EXTRA[_l])

BANNERS = {
    "zh": dict(b1_k="諮詢", b1_t="有一個陌生市場要讀懂？", b1_d="從第一次拜會到在地夥伴，先談 30 分鐘，看看從哪裡開始。", b1_btn="預約諮詢",
               nl_k="通訊", nl_t="訂閱《讀懂非洲》通訊", nl_d="新文章上線時寄給你。不寄廣告，隨時可以取消。",
               nl_ph="你的 Email", nl_btn="訂閱", nl_int="最想讀的主題（可不填）", nl_ok="謝謝！已收到你的訂閱。", nl_err="送出失敗，請稍後再試，或直接寫信給我。",
               nl_privacy="你的 Email 只用來寄送通訊。", all_cat="全部", n_articles="篇文章"),
    "en": dict(b1_k="Consulting", b1_t="Is there a market you need to read?", b1_d="From a first meeting to a local partner: start with a 30-minute conversation.", b1_btn="Book a consultation",
               nl_k="Newsletter", nl_t="Get the Reading Africa letter", nl_d="An email when a new article goes live. No ads, unsubscribe anytime.",
               nl_ph="Your email", nl_btn="Subscribe", nl_int="Topic you care about (optional)", nl_ok="Thank you, you're subscribed.", nl_err="Something went wrong. Please try again or email me directly.",
               nl_privacy="Your email is used only to send the letter.", all_cat="All", n_articles="articles"),
    "fr": dict(b1_k="Conseil", b1_t="Un marché à décrypter ?", b1_d="Du premier rendez-vous au partenaire local : commençons par 30 minutes d'échange.", b1_btn="Prendre rendez-vous",
               nl_k="Lettre", nl_t="Recevez la lettre « Lire l'Afrique »", nl_d="Un e-mail à chaque nouvel article. Sans publicité, désinscription à tout moment.",
               nl_ph="Votre e-mail", nl_btn="S'abonner", nl_int="Sujet préféré (facultatif)", nl_ok="Merci, votre inscription est enregistrée.", nl_err="L'envoi a échoué. Réessayez ou écrivez-moi directement.",
               nl_privacy="Votre e-mail sert uniquement à l'envoi de la lettre.", all_cat="Tous", n_articles="articles"),
}
for _l in LANGS:
    C[_l].update(BANNERS[_l])

CAT_KEYS = ["art", "lifestyle", "cross-cultural", "business"]
CAT_PAT = {"art": "korhogo_light", "lifestyle": "kita_light", "cross-cultural": "dida_light", "business": "akan_light"}
CAT_MOTIF = {  # which documented Ivorian motif each category uses (from AKWABA's sourced motif set)
    "zh": {"art": "Korhogo 手繪布的魚紋", "lifestyle": "窄幅手織布", "cross-cultural": "Dida 紮染布的圓紋", "business": "Akan 金砝碼紋"},
    "en": {"art": "Korhogo cloth fish motif", "lifestyle": "Strip-woven cloth", "cross-cultural": "Dida tie-dye rings", "business": "Akan goldweight motif"},
    "fr": {"art": "Motif de poisson des toiles de Korhogo", "lifestyle": "Tissage en bandes", "cross-cultural": "Cercles des tissus dida", "business": "Motif des poids à peser l'or akan"},
}

MORE = {
    "zh": dict(
        topics_t="四個分類", read_cat="看這一類的文章", related_t="同一類的其他文章", cat_page_d="「讀懂非洲」專欄的{name}文章：{line}",
        motif_note="紋樣：{m}",
        nl_name="怎麼稱呼你", nl_role="你是", nl_company="公司或單位（可不填）", nl_topics="想讀的主題（可複選）",
        roles=["企業主管或決策者", "創業者", "旅人或收藏者", "學生或研究者", "媒體", "其他"],
        nl_why="留下稱呼和身分，我寄給你的內容會更對題。",
        exp_t="在四座城市，學會讀懂市場",
        route=[("巴黎", "2017"), ("達卡", "2020"), ("台北", "2020"), ("阿比讓", "2026")],
        highlights=[
            ("國際組織", "無國界醫生 MSF", "負責多渠道行銷，並主導約 40 人外部合作團隊的營運。", "台北 · 2022–2026"),
            ("品牌與大型活動", "力譔堂整合行銷", "統籌 5 項整合行銷專案、總預算 €960K，一年完成 17 場展覽與活動。", "台北 · 2021–2022"),
            ("奢華旅宿", "巴黎麗茲酒店 · 雲朗觀光 · Terrou-Bi Resort", "從巴黎麗茲到達卡的五星度假村，熟悉高端客人的期待。", "巴黎 · 南投 · 達卡"),
            ("國際市場與夥伴", "法國設計學院 · Funique VR · 維策顧問", "完成 11 國國際標竿研究、開發歐洲策略夥伴；現在在阿比讓推動亞非合作。", "巴黎 · 台北 · 阿比讓"),
        ],
        orgs_t="合作與任職過的機構",
        edu_line="International MBA · IAE Paris-Est　｜　HEC Paris 奢侈品管理證書　｜　國立中山大學 外國語文學系",
    ),
    "en": dict(
        topics_t="Four topics", read_cat="Read this topic", related_t="More in this topic", cat_page_d="{name} articles in the Reading Africa column: {line}",
        motif_note="Motif: {m}",
        nl_name="Your name", nl_role="You are", nl_company="Company or organisation (optional)", nl_topics="Topics you want (choose any)",
        roles=["Executive or decision-maker", "Entrepreneur", "Traveller or collector", "Student or researcher", "Media", "Other"],
        nl_why="Your name and role help me send you what's relevant.",
        exp_t="Four cities, one craft: reading markets",
        route=[("Paris", "2017"), ("Dakar", "2020"), ("Taipei", "2020"), ("Abidjan", "2026")],
        highlights=[
            ("International NGO", "Médecins Sans Frontières", "Multichannel marketing, and led an external partner operation of about 40 people.", "Taipei · 2022–2026"),
            ("Brands & large events", "CSR-TAIWAN Summit", "Ran five integrated campaigns with €960K in total budget; 17 exhibitions and events in one year.", "Taipei · 2021–2022"),
            ("Luxury hospitality", "Ritz Paris · LDC Hotels · Terrou-Bi Resort", "From the Ritz in Paris to a five-star resort in Dakar: fluent in what high-end guests expect.", "Paris · Nantou · Dakar"),
            ("Markets & partnerships", "Institut Français du Design · Funique VR · VicTseng Consult", "An 11-country benchmarking study, European partnerships, and now Asia–Africa work from Abidjan.", "Paris · Taipei · Abidjan"),
        ],
        orgs_t="Organisations I have worked with",
        edu_line="International MBA · IAE Paris-Est　|　HEC Paris, Luxury Management certificate　|　BA Foreign Languages, National Sun Yat-sen University",
    ),
    "fr": dict(
        topics_t="Quatre thèmes", read_cat="Lire ce thème", related_t="Dans le même thème", cat_page_d="Les chroniques « Lire l'Afrique » sur le thème {name} : {line}",
        motif_note="Motif : {m}",
        nl_name="Votre nom", nl_role="Vous êtes", nl_company="Entreprise ou organisation (facultatif)", nl_topics="Thèmes souhaités (plusieurs choix)",
        roles=["Dirigeant ou décideur", "Entrepreneur", "Voyageur ou collectionneur", "Étudiant ou chercheur", "Média", "Autre"],
        nl_why="Votre nom et votre profil m'aident à vous envoyer l'essentiel.",
        exp_t="Quatre villes, un métier : lire les marchés",
        route=[("Paris", "2017"), ("Dakar", "2020"), ("Taipei", "2020"), ("Abidjan", "2026")],
        highlights=[
            ("ONG internationale", "Médecins Sans Frontières", "Marketing multicanal et pilotage d'une opération partenaire d'environ 40 personnes.", "Taipei · 2022–2026"),
            ("Marques et grands événements", "CSR-TAIWAN Summit", "Cinq campagnes intégrées, 960 K€ de budget ; 17 salons et événements en un an.", "Taipei · 2021–2022"),
            ("Hôtellerie de luxe", "Ritz Paris · LDC Hotels · Terrou-Bi Resort", "Du Ritz à Paris à un resort cinq étoiles à Dakar : les attentes d'une clientèle exigeante.", "Paris · Nantou · Dakar"),
            ("Marchés et partenariats", "Institut Français du Design · Funique VR · VicTseng Consult", "Un benchmark dans 11 pays, des partenariats en Europe, et aujourd'hui l'Asie–Afrique depuis Abidjan.", "Paris · Taipei · Abidjan"),
        ],
        orgs_t="Organisations avec lesquelles j'ai travaillé",
        edu_line="International MBA · IAE Paris-Est　|　HEC Paris, certificat Luxury Management　|　Licence de langues étrangères, Université Sun Yat-sen",
    ),
}
ORGS = ["Médecins Sans Frontières", "Ritz Paris", "HEC Paris", "IAE Paris-Est", "Institut Français du Design", "Terrou-Bi Resort", "LDC Hotels & Resorts", "Funique VR"]
for _l in LANGS:
    C[_l].update(MORE[_l])

UX = {
    "zh": dict(scroll="往下探索", top="回到頂部", more="往下閱讀", map_cap="三大洲・四座城市", conts=("歐洲", "非洲", "亞洲"), nl_sending="送出中…"),
    "en": dict(scroll="Scroll to explore", top="Back to top", more="Keep reading", map_cap="Three continents, four cities", conts=("EUROPE", "AFRICA", "ASIA"), nl_sending="Sending…"),
    "fr": dict(scroll="Découvrir", top="Haut de page", more="Lire la suite", map_cap="Trois continents, quatre villes", conts=("EUROPE", "AFRIQUE", "ASIE"), nl_sending="Envoi…"),
}
for _l in LANGS:
    C[_l].update(UX[_l])
