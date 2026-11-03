import re
p = 'build.py'
s = open(p).read()


def R(a, b, cnt=1):
    global s
    assert a in s, a[:100]
    s = s.replace(a, b, cnt)


# 1. remove motif icon from expertise items
R('''        <span class="pl-m" style="{pat(CAT_PAT[CAT_KEYS[i]])}" aria-hidden="true"></span>\n''', '')
# 2. remove work note
R('''{sh(2, c['sec_work'], c['sec_work_t'], c['work_note'])}''', '''{sh(2, c['sec_work'], c['sec_work_t'])}''')
# remove scroll cue (floating button replaces it)
R('''      <a class="cue" href="#expertise"><span>{e(c['scroll'])}</span><i aria-hidden="true"></i></a>\n''', '')

# 3. internal links + images, applied in load_notes after markdown
R('''CFG = json.load(''', '''LINKS = json.load(open(os.path.join(HERE, "data", "links.json"), encoding="utf-8"))
IMAGES = {}
for _f in sorted(glob.glob(os.path.join(HERE, "data", "img", "*.json"))):
    try:
        IMAGES.update({k: v for k, v in json.load(open(_f, encoding="utf-8")).items() if v})
    except Exception as _ex:
        print("skip images file", _f, _ex)
CFG = json.load(''')

R('''NOTES = load_notes()''', '''NOTES = load_notes()

SKIP_TAGS = ("a", "h1", "h2", "h3", "h4", "th", "code", "figcaption")


def autolink(html, slug, lang):
    """Link the first mention of other articles' keywords (max 6 per article), never inside headings or links."""
    cut = html.find("<hr")
    head, tail = (html[:cut], html[cut:]) if cut >= 0 else (html, "")
    pairs = sorted(((kw, t) for t, kws in LINKS.items() if t != slug and t in NOTES for kw in kws), key=lambda x: -len(x[0]))
    used_t, made, ph = set(), [], []
    parts = re.split(r"(<[^>]+>)", head)
    depth = 0
    for i, part in enumerate(parts):
        if part.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", part)
            if m and m.group(2).lower() in SKIP_TAGS:
                depth += -1 if m.group(1) else 1
            continue
        if depth > 0 or not part.strip():
            continue
        text = part
        for kw, t in pairs:
            if len(made) >= 6:
                break
            if t in used_t:
                continue
            if re.match(r"^[\\x00-\\u024F' .-]+$", kw):
                rx = re.compile(r"(?<![\\w\\-’'])" + re.escape(kw) + r"(?![\\w\\-])")
            else:
                rx = re.compile(re.escape(kw))
            mm = rx.search(text)
            if not mm:
                continue
            tl = t_lang = lang if lang in NOTES[t] else next(iter(NOTES[t]))
            ph.append(f'<a class="il" href="{note_path(tl, t)}">{mm.group(0)}</a>')
            text = text[:mm.start()] + f"\\x00{len(ph)-1}\\x00" + text[mm.end():]
            used_t.add(t); made.append(t)
        parts[i] = text
    out = "".join(parts)
    out = re.sub(r"\\x00(\\d+)\\x00", lambda m: ph[int(m.group(1))], out)
    return out + tail


def figure(slug, lang):
    im = IMAGES.get(slug)
    if not im:
        return ""
    lic = e(im.get("license", ""))
    lic_html = f'<a href="{e(im["license_url"])}" rel="license noopener" target="_blank">{lic}</a>' if im.get("license_url") else lic
    cap = e((im.get("caption") or {}).get(lang, ""))
    alt = e((im.get("alt") or {}).get(lang, ""))
    credit = f'<a href="{e(im.get("page", ""))}" target="_blank" rel="noopener">{e(im.get("author", ""))}</a> · {lic_html}'
    return (f'<figure class="fig"><img src="{e(im["src"])}" alt="{alt}" loading="lazy" decoding="async" referrerpolicy="no-referrer">'
            f'<figcaption><span>{cap}</span><span class="cr">{credit}</span></figcaption></figure>')


def enrich(slug, lang, html):
    html = autolink(html, slug, lang)
    fig = figure(slug, lang)
    if fig:
        k = html.find("<h2")
        html = html[:k] + fig + html[k:] if k > 0 else fig + html
    return html''')

R('''    <div class="prose">{n['html']}</div>''', '''    <div class="prose">{enrich(slug, lang, n['html'])}</div>''')

# image into Article JSON-LD when available
R('''"mainEntityOfPage": DOMAIN + note_path(lang, slug), "image": DOMAIN + f"/assets/img/og-{lang if lang in C else 'zh'}.jpg",''',
  '''"mainEntityOfPage": DOMAIN + note_path(lang, slug), "image": (IMAGES.get(slug) or {}).get("src") or DOMAIN + f"/assets/img/og-{lang if lang in C else 'zh'}.jpg",''')

# 4. copyright line + page
R('''    <p class="ft-c">© 2026 Victor Tseng 曾浩瑜 · VicTseng Consult</p>''',
  '''    <p class="ft-c">© 2026 Victor Tseng 曾浩瑜 · VicTseng Consult · {e(c['rights'])} · <a href="{PATHS[lang]}copyright/">{e(c['copy_t'])}</a></p>''')

R('''# ---------------------------------------------------------------- write''', '''def copyright_page(lang):
    c = L(lang)
    alts = {l: PATHS[l] + "copyright/" for l in LANGS}
    secs = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{x}</p>" for x in ps) for h, ps in c["copy_body"])
    body = f"""
<main id="main" class="page">
  <article class="wrap art">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a></nav>
    <header class="art-h"><p class="sh-k">© 2026</p><h1>{e(c['copy_t'])}</h1></header>
    <div class="prose">{secs}</div>
  </article>
</main>"""
    return (head(lang, c, f"{c['copy_t']}｜Victor Tseng", c["copy_t"], PATHS[lang] + "copyright/", alts, f"/assets/img/og-{lang}.jpg", "website", None)
            + header(lang, c, alts, False) + body + footer(lang, c, alts, search_index(lang, c)))


# ---------------------------------------------------------------- write''')
R('''for slug, vs in NOTES.items():
    for l in vs:
        write(note_path(l, slug) + "index.html", note_page(slug, l))''', '''for l in LANGS:
    write(PATHS[l] + "copyright/index.html", copyright_page(l)); urls.append(({x: PATHS[x] + "copyright/" for x in LANGS}, PATHS[l] + "copyright/", None))
for slug, vs in NOTES.items():
    for l in vs:
        write(note_path(l, slug) + "index.html", note_page(slug, l))''')
open(p, 'w').write(s)

# ---------------------------------------------------------------- content
p = 'content.py'
s = open(p).read()
R('h1="Reading Africa:<br>art, lifestyle and business"', 'h1="Reading Africa:<br>art, life, business"')
R('h1="Lire l\'Afrique :<br>son art, sa vie, ses affaires"', 'h1="Lire l\'Afrique :<br>art, vie, affaires"')
R('one="I\'ve worked in Asia, Europe and West Africa, and now live in Abidjan. I help Asian companies and people read an unfamiliar market."',
  'one="Asia, Europe, West Africa, now Abidjan. I help Asian companies read unfamiliar markets."')
R('one="J\'ai travaillé en Asie, en Europe et en Afrique de l\'Ouest ; je vis aujourd\'hui à Abidjan. J\'aide les entreprises et les professionnels asiatiques à décrypter un marché inconnu."',
  'one="Asie, Europe, Afrique de l\'Ouest, aujourd\'hui Abidjan. J\'aide les entreprises asiatiques à décrypter un marché inconnu."')
s += '''
COPY = {
    "zh": dict(rights="版權所有", copy_t="版權聲明", copy_body=[
        ("網站內容", ["本網站的文字、版面設計、照片與「讀懂非洲」專欄文章，著作權屬於 Victor Tseng 曾浩瑜（維策顧問 VicTseng Consult），另有標示者除外。"]),
        ("引用與轉載", ["歡迎引用不超過 150 字的段落，請註明「Victor Tseng 曾浩瑜／victseng.com」並附上原文連結。", "全文轉載、改寫、翻譯或商業使用，請先來信取得書面同意：<a href=\\"mailto:victseng.consult@gmail.com\\">victseng.consult@gmail.com</a>。"]),
        ("圖片", ["文章中的圖片只使用公有領域（Public Domain、CC0）或 Creative Commons 姓名標示（CC BY、CC BY-SA）授權的作品，來源、作者與授權條款標示在每張圖下方。使用這些圖片時，請依原授權條款辦理，不受本站版權聲明限制。", "本站人像照片為 Victor Tseng 本人所有，未經同意請勿使用。"]),
        ("作品與商標", ["「AKWABA・非洲品味之家／Maison de Goût Africain」與《Akwaba！非洲大冒險》為 Victor Tseng 的原創作品。其中使用的象牙海岸紋樣均經查證來源，詳見各作品說明。"]),
        ("資料正確性", ["專欄文章為公開資料的整理，每篇附上出處，力求正確，但法規、數據與日期可能變動。涉及法律、稅務或投資決策時，請以主管機關公告或專業意見為準。若發現錯誤，歡迎來信指正。"]),
    ]),
    "en": dict(rights="All rights reserved", copy_t="Copyright", copy_body=[
        ("Site content", ["Unless otherwise stated, the text, design, photographs and Reading Africa articles on this site are © Victor Tseng (VicTseng Consult)."]),
        ("Quoting and republishing", ["You are welcome to quote up to 100 words with credit to “Victor Tseng / victseng.com” and a link to the original page.", "For full republication, adaptation, translation or commercial use, please ask for written permission first: <a href=\\"mailto:victseng.consult@gmail.com\\">victseng.consult@gmail.com</a>."]),
        ("Images", ["Article images are public domain (incl. CC0) or licensed under Creative Commons Attribution (CC BY, CC BY-SA); source, author and licence are credited under each image. Reuse of those images follows their original licence, not this notice.", "The portrait photographs of Victor Tseng belong to him and may not be used without permission."]),
        ("Projects and names", ["“AKWABA · Maison de Goût Africain” and “Akwaba! An African Adventure” are original works by Victor Tseng. The Ivorian motifs they use were researched for their origins; see each project for details."]),
        ("Accuracy", ["Articles compile public sources and cite them, but laws, figures and dates change. For legal, tax or investment decisions, rely on official notices or professional advice. Corrections are welcome by email."]),
    ]),
    "fr": dict(rights="Tous droits réservés", copy_t="Droits d'auteur", copy_body=[
        ("Contenus du site", ["Sauf mention contraire, les textes, la mise en page, les photographies et les chroniques « Lire l'Afrique » sont © Victor Tseng (VicTseng Consult)."]),
        ("Citation et reprise", ["Vous pouvez citer jusqu'à 100 mots en mentionnant « Victor Tseng / victseng.com » avec un lien vers la page d'origine.", "Pour toute reprise intégrale, adaptation, traduction ou utilisation commerciale, merci de demander une autorisation écrite : <a href=\\"mailto:victseng.consult@gmail.com\\">victseng.consult@gmail.com</a>."]),
        ("Images", ["Les images des articles sont dans le domaine public (dont CC0) ou sous licence Creative Commons Attribution (CC BY, CC BY-SA) ; la source, l'auteur et la licence figurent sous chaque image. Leur réutilisation suit leur licence d'origine, et non la présente mention.", "Les portraits de Victor Tseng lui appartiennent et ne peuvent être utilisés sans autorisation."]),
        ("Projets et noms", ["« AKWABA · Maison de Goût Africain » et « Akwaba ! Une aventure africaine » sont des œuvres originales de Victor Tseng. Les motifs ivoiriens utilisés ont été documentés quant à leur origine ; voir chaque projet."]),
        ("Exactitude", ["Les chroniques compilent des sources publiques citées, mais lois, chiffres et dates évoluent. Pour toute décision juridique, fiscale ou d'investissement, référez-vous aux communications officielles ou à un professionnel. Les corrections sont les bienvenues par e-mail."]),
    ]),
}
for _l in LANGS:
    C[_l].update(COPY[_l])
'''
open(p, 'w').write(s)

# ---------------------------------------------------------------- css / js
p = 'site.css'
s = open(p).read()
s = s.replace("/* ---------- pages & article ---------- */", """/* ---------- inline links & figures ---------- */
.prose a.il{border-bottom:1px solid var(--gold);transition:background .25s}
.prose a.il:hover{background:rgba(168,135,74,.14)}
.fig{margin:1.6em 0 2em}
.fig img{display:block;width:100%;height:auto;max-height:520px;object-fit:cover;background:var(--iv2);border:1px solid var(--line)}
.fig figcaption{display:grid;gap:4px;margin-top:10px;font-size:12.5px;line-height:1.6;color:var(--taupe)}
.fig .cr{font:400 10.5px/1.5 var(--mono);letter-spacing:.02em}
.fig .cr a{border-bottom:1px solid var(--line2)}
.ft-c a{border-bottom:1px solid var(--line2)}
.ft-c a:hover{color:var(--ink)}

/* ---------- pages & article ---------- */""", 1)
s = s.replace(".l-en .h1,.l-fr .h1{font-family:var(--disp);font-weight:400;letter-spacing:0;line-height:1.02;font-size:clamp(42px,10.5vw,84px)}",
              ".l-en .h1,.l-fr .h1{font-family:var(--disp);font-weight:400;letter-spacing:0;line-height:1.02;font-size:clamp(38px,10vw,84px)}")
s += """
@media (max-width:719px){
  .l-en .one,.l-fr .one{font-size:14px;margin:10px auto 18px}
  .l-en .hero .ctas,.l-fr .hero .ctas{gap:12px 18px}
  .l-en .hero .btn,.l-fr .hero .btn{padding:0 18px;letter-spacing:.18em;font-size:11px;min-height:46px}
  .l-en .who,.l-fr .who{gap:6px}
  .l-en .arch,.l-fr .arch{margin-top:30px;width:min(48vw,200px)}
}
"""
open(p, 'w').write(s)

p = 'site.js'
s = open(p).read()
R_js = "      tt.classList.toggle('on', h.scrollTop > 160);"
assert R_js in s
s = s.replace(R_js, "      tt.classList.add('on');")
open(p, 'w').write(s)
print("patched")
