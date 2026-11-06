"""victseng.com builder (v3).  Usage: python3 build.py <output_dir>
Content: content.py (page copy), data/press.json (media list), notes/<slug>/<lang>.md (site articles)."""
import json, os, re, sys, glob, math
from html import escape as e
from urllib.parse import quote
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import C, LANGS, PATHS, HREFLANG, LANG_LABEL, DOMAIN, EMAIL, LINKEDIN, CAT_KEYS, CAT_PAT, CAT_MOTIF, ORGS

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, ".."))
VER = "20261103d"
PAT = json.load(open(os.path.join(HERE, "patterns.json")))
LINKS = json.load(open(os.path.join(HERE, "data", "links.json"), encoding="utf-8"))
IMAGES = {}
for _f in sorted(glob.glob(os.path.join(HERE, "data", "img", "*.json"))):
    try:
        IMAGES.update({k: v for k, v in json.load(open(_f, encoding="utf-8")).items() if v})
    except Exception as _ex:
        print("skip images file", _f, _ex)
CFG = json.load(open(os.path.join(HERE, "data", "config.json"), encoding="utf-8"))
MAP = json.load(open(os.path.join(HERE, "data", "map.json")))
PRESS = json.load(open(os.path.join(HERE, "data", "press.json"), encoding="utf-8"))
POD = json.load(open(os.path.join(HERE, "data", "podcast.json"), encoding="utf-8"))
if os.environ.get("POD_PREVIEW"):
    POD["live"] = True
POD_LIVE = bool(POD.get("live"))
POD_PLAT = [("spotify", "Spotify"), ("apple", "Apple Podcasts"), ("kkbox", "KKBOX"), ("youtube", "YouTube"), ("firstory", "Firstory")]


def nav_for(c):
    nav = list(c["nav"])
    if POD_LIVE:
        i = [k for k, _ in nav].index("notes") + 1
        nav.insert(i, ("podcast", c["pod_nav"]))
    return nav


def pod_url(url, campaign):
    if not url:
        return url
    return url + ("&" if "?" in url else "?") + "utm_source=victseng&utm_medium=referral&utm_campaign=" + campaign


def podcast_section(lang, c, sh):
    eps = POD.get("episodes") or []
    rows = "".join(f"""<li class="rv"><a class="row" href="{e(pod_url(ep['url'], 'site_home'))}" target="_blank" rel="noopener">
      <span class="row-m"><span>{e(ep.get('code', ''))}</span><time datetime="{ep['date']}">{fmt_date(ep['date'], lang)}</time></span>
      <span class="row-t">{e(ep['title'].get(lang) or ep['title']['zh'])}</span>
      <span class="row-go">{e(c['pod_listen'])} {I_OUT}</span></a></li>""" for ep in eps[:3])
    if not rows:
        rows = f'<li class="rv"><p class="row"><span class="row-m"><span>{e(c["pod_season"])}</span></span><span class="row-t">{e(POD["launch"][lang])}</span></p></li>'
    plats = "".join(f'<a class="tl" href="{e(pod_url(POD["links"][k], "site_home"))}" target="_blank" rel="noopener">{n} {I_OUT}</a>'
                    for k, n in POD_PLAT if POD["links"].get(k))
    return f"""<section id="podcast" class="sec alt pc">
    <div class="wrap">{sh('podcast', c['pod_k'], c['pod_t'], c['pod_n'])}
      <p class="cap pc-s rv">{e(c['pod_season'])}</p>
      <ul class="rows">{rows}
      </ul>
      <div class="pc-pl rv">{plats}</div>
      <aside class="pc-sub rv">
        <div><p class="pc-sub-t">{e(c['pod_sub_t'])}</p><p class="pc-sub-d">{e(c['pod_sub_d'])}</p></div>
        <a class="btn" href="{mailto(c['pod_sub_subject'])}">{e(c['pod_sub_btn'])} {I_ARROW}</a>
      </aside>
    </div>
  </section>"""


def pod_for_note(slug, lang, c):
    if not POD_LIVE:
        return ""
    for ep in POD.get("episodes") or []:
        if slug in (ep.get("notes") or []):
            t = ep["title"].get(lang) or ep["title"]["zh"]
            return f"""<aside class="pc-note"><p class="cap">{e(c['pod_note_k'])}</p><p class="pc-note-t">{e(ep.get('code', ''))} · {e(t)}</p>
      <a class="tl" href="{e(pod_url(ep['url'], 'site_' + slug))}" target="_blank" rel="noopener">{e(c['pod_note_go'])} {I_OUT}</a></aside>"""
    return ""
LANG_NAME = {"zh": "中文", "en": "English", "fr": "Français"}

I_ARROW = '<svg aria-hidden="true" class="ic" viewBox="0 0 24 24" width="16" height="16"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
I_OUT = '<svg aria-hidden="true" class="ic" viewBox="0 0 24 24" width="15" height="15"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
I_SEARCH = '<svg aria-hidden="true" viewBox="0 0 24 24" width="19" height="19"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m16 16 4.5 4.5" stroke="currentColor" stroke-width="1.5"/></svg>'
I_MAIL = '<svg aria-hidden="true" class="ic" viewBox="0 0 24 24" width="17" height="17"><rect x="3.5" y="5.5" width="17" height="13" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
I_LI = '<svg aria-hidden="true" class="ic" viewBox="0 0 24 24" width="15" height="15"><path fill="currentColor" d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-4.95c0-1.18-.02-2.7-1.65-2.7-1.65 0-1.9 1.29-1.9 2.62V21h-4z"/></svg>'


# ---------------------------------------------------------------- helpers
def typo(v, fr):
    if isinstance(v, str):
        if v.startswith("/") or v.startswith("http"):
            return v
        v = v.replace("'", "’")
        if fr:
            for p in (" :", " ;", " !", " ?"):
                v = v.replace(p, " " + p[1])
        return v
    if isinstance(v, list): return [typo(x, fr) for x in v]
    if isinstance(v, tuple): return tuple(typo(x, fr) for x in v)
    if isinstance(v, dict): return {k: typo(x, fr) for k, x in v.items()}
    return v


def L(lang):
    return C[lang] if lang == "zh" else typo(C[lang], lang == "fr")


def mailto(subj):
    return f"mailto:{EMAIL}?subject={quote(subj + ' | victseng.com')}"


def pat(name):
    p = PAT[name]
    return f"background-image:url('data:image/svg+xml,{quote(p['svg'])}');background-size:{p['w']//2}px {p['h']//2}px"


def home(lang):
    return PATHS[lang]


def notes_path(lang):
    return PATHS[lang] + "notes/"


def note_path(lang, slug):
    return PATHS[lang] + "notes/" + slug + "/"


def fmt_date(d, lang):
    y, m, dd = d.split("-")
    if lang == "zh":
        return f"{y}.{m}.{dd}"
    months = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
              "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]}[lang]
    return f"{int(dd)} {months[int(m)-1]} {y}"


# ---------------------------------------------------------------- notes
def load_notes():
    notes = {}
    for f in sorted(glob.glob(os.path.join(HERE, "notes", "*", "*.md"))):
        slug = os.path.basename(os.path.dirname(f))
        lang = os.path.splitext(os.path.basename(f))[0]
        raw = open(f, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        meta, body = {}, raw
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                        v = v[1:-1]
                    meta[k.strip()] = v
            body = m.group(2)
        if meta.get("draft", "").lower() == "true":
            continue
        html = markdown.markdown(body, extensions=["tables", "toc", "sane_lists"])
        def _lab(m):
            t = m.group(0)
            heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
            def _row(r):
                i = [0]
                def _td(mm):
                    lab = heads[i[0]] if i[0] < len(heads) else ""
                    i[0] += 1
                    return f'<td data-label="{e(lab)}"' + mm.group(1) + ">"
                return re.sub(r"<td([^>]*)>", _td, r.group(0))
            return re.sub(r"<tr>.*?</tr>", _row, t, flags=re.S)
        html = re.sub(r"<table>.*?</table>", _lab, html, flags=re.S)
        html = html.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
        text = re.sub(r"<[^>]+>", "", html)
        if lang == "zh":
            mins = max(1, math.ceil(len(re.findall(r"[一-鿿]", text)) / 400))
        else:
            mins = max(1, math.ceil(len(text.split()) / 220))
        meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        notes.setdefault(slug, {})[lang] = dict(meta, slug=slug, lang=lang, html=html, mins=mins, text=text)
    # newest first
    return dict(sorted(notes.items(), key=lambda kv: max(v["date"] for v in kv[1].values()), reverse=True))


NOTES = load_notes()

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
            if re.match(r"^[\x00-\u024F' .-]+$", kw):
                rx = re.compile(r"(?<![\w\-’'])" + re.escape(kw) + r"(?![\w\-])")
            else:
                rx = re.compile(re.escape(kw))
            mm = rx.search(text)
            if not mm:
                continue
            tl = t_lang = lang if lang in NOTES[t] else next(iter(NOTES[t]))
            ph.append(f'<a class="il" href="{note_path(tl, t)}">{mm.group(0)}</a>')
            text = text[:mm.start()] + f"\x00{len(ph)-1}\x00" + text[mm.end():]
            used_t.add(t); made.append(t)
        parts[i] = text
    out = "".join(parts)
    out = re.sub(r"\x00(\d+)\x00", lambda m: ph[int(m.group(1))], out)
    return out + tail, made


def figure(slug, lang):
    im = IMAGES.get(slug)
    if not im:
        return ""
    lic = e(im.get("license", ""))
    lic_html = f'<a href="{e(im["license_url"])}" rel="license noopener" target="_blank">{lic}</a>' if im.get("license_url") else lic
    cap = e((im.get("caption") or {}).get(lang, ""))
    alt = e((im.get("alt") or {}).get(lang, ""))
    credit = f'<a href="{e(im.get("page", ""))}" target="_blank" rel="noopener">{e(im.get("author", ""))}</a> · {lic_html}'
    return (f'<figure class="fig"><img src="{e(im["src"])}" alt="{alt}" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.parentNode.remove()">'
            f'<figcaption><span>{cap}</span><span class="cr">{credit}</span></figcaption></figure>')


FURTHER = {"zh": "延伸閱讀", "en": "Further reading", "fr": "Pour aller plus loin"}


def further(slug, lang, exclude, need):
    key = cat_key(NOTES[slug][lang])
    pool = [s_ for s_ in NOTES if s_ != slug and s_ not in exclude and cat_key(next(iter(NOTES[s_].values()))) == key]
    pool += [s_ for s_ in NOTES if s_ != slug and s_ not in exclude and s_ not in pool]
    # spread choices so different articles suggest different reads
    off = sum(map(ord, slug)) % max(1, len(pool))
    picks = (pool[off:] + pool[:off])[:need]
    items = "".join(f'<li><a class="il" href="{note_path(lang if lang in NOTES[t] else next(iter(NOTES[t])), t)}">{e(note_for(t, lang)["title"])}</a></li>' for t in picks)
    return f'<aside class="further"><p class="cap">{FURTHER[lang]}</p><ul>{items}</ul></aside>'


def enrich(slug, lang, html):
    html, made = autolink(html, slug, lang)
    box = further(slug, lang, set(made), max(3, 5 - len(made)))
    cut = html.find("<hr")
    body, tail = (html[:cut], html[cut:]) if cut >= 0 else (html, "")
    k = body.rfind("<h2")
    body = body[:k] + box + body[k:] if k > 0 else body + box
    html = body + tail
    fig = figure(slug, lang)
    if fig:
        k = html.find("<h2")
        html = html[:k] + fig + html[k:] if k > 0 else fig + html
    return html


def pillar_name(n, lang):
    p = n.get("pillar", "")
    for l in LANGS:
        names = [t for t, _, _ in C[l]["pillars"]]
        if p in names:
            return C[lang]["pillars"][names.index(p)][0]
    return p


def cat_idx(n):
    p = n.get("pillar", "")
    for l in LANGS:
        names = [t for t, _, _ in C[l]["pillars"]]
        if p in names:
            return names.index(p)
    return 0


def cat_key(n):
    return CAT_KEYS[cat_idx(n)]


def cat_path(lang, key):
    return notes_path(lang) + "topic/" + key + "/"


def cat_count(key):
    return sum(1 for s in NOTES if cat_key(next(iter(NOTES[s].values()))) == key)


def cat_tiles(lang, c):
    out = []
    for i, key in enumerate(CAT_KEYS):
        name, line, _ = c["pillars"][i]
        out.append(f"""<li class="rv"><a class="ct-t" href="{cat_path(lang, key)}">
        <span class="ct-m" style="{pat(CAT_PAT[key])}" aria-hidden="true"></span>
        <span class="ct-b"><span class="ct-n">{i+1:02d}</span><span class="ct-h">{e(name)}</span><span class="ct-c">{cat_count(key)} {e(c['n_articles'])}</span></span>
        <span class="ct-go">{e(c['read_cat'])} {I_ARROW}</span></a></li>""")
    return f'<ul class="cts">{"".join(out)}</ul>'


def note_for(slug, lang):
    """the version to show a reader of `lang` (fallback: en, then zh)"""
    vs = NOTES[slug]
    for l in (lang, "en", "zh", "fr"):
        if l in vs:
            return vs[l]


# ---------------------------------------------------------------- shared chrome
def ga_tag():
    gid = CFG.get("ga4", "").strip()
    if not gid:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{gid}');</script>")


def gsc_tag():
    v = CFG.get("googleSiteVerification", "").strip()
    return f'<meta name="google-site-verification" content="{e(v)}">' if v else ""


def head(lang, c, title, desc, url, alts, og_img, og_type="website", ld=None):
    alt_links = "".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{DOMAIN}{u}">' for l, u in alts.items())
    if "zh" in alts:
        alt_links += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{alts["zh"]}">'
    latin = "&family=Noto+Serif:wght@400;500" if lang != "zh" else ""
    return f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="Victor Tseng 曾浩瑜">
<link rel="canonical" href="{DOMAIN}{url}">
{alt_links}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Victor Tseng 曾浩瑜">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{DOMAIN}{url}">
<meta property="og:image" content="{DOMAIN}{og_img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{c['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F4EFE7">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Victor Tseng · {e(c['sec_notes_t'])}" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;400;500&family=IBM+Plex+Mono:wght@400&family=Noto+Serif+TC:wght@400;500;600&family=Noto+Sans+TC:wght@300;400;500{latin}&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
{ga_tag()}{gsc_tag()}
{f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''}
</head>"""


def header(lang, c, alts, on_home):
    langsw = "".join(
        f'<a href="{alts.get(l, PATHS[l])}" hreflang="{HREFLANG[l]}" lang="{C[l]["html_lang"]}"' + (' aria-current="page"' if l == lang else "") + f">{LANG_LABEL[l]}</a>"
        for l in LANGS)
    pre = "" if on_home else home(lang)
    nav = "".join(f'<a href="{pre}#{i}" data-sec="{i}"><span class="n">{n:02d}</span>{e(t)}</a>' for n, (i, t) in enumerate(nav_for(c), 1))
    return f"""<body class="l-{lang}{' is-home' if on_home else ''}">
<a class="skip" href="#main">{e(c['skip'])}</a>
<div class="prog" aria-hidden="true"><i></i></div>
<header class="hd">
  <div class="hd-row wrap">
    <a class="logo" href="{home(lang)}" aria-label="Victor Tseng"><span class="logo-t">VICTOR TSENG</span><span class="logo-z">曾浩瑜</span></a>
    <div class="hd-r">
      <button class="sbtn" type="button" data-open-search aria-label="{e(c['search'])}">{I_SEARCH}</button>
      <nav class="lg" aria-label="{e(c['lang_label'])}">{langsw}</nav>
    </div>
  </div>
  <nav class="an" aria-label="{e(c['menu_label'])}"><div class="an-in wrap">{nav}</div></nav>
</header>
"""


def footer(lang, c, alts, idx):
    langsw = "".join(
        f'<a href="{alts.get(l, PATHS[l])}" hreflang="{HREFLANG[l]}"' + (' aria-current="page"' if l == lang else "") + f">{LANG_NAME[l]}</a>"
        for l in LANGS)
    return f"""
<footer class="ft">
  <div class="band" style="{pat('kita_light')}" aria-hidden="true"></div>
  <div class="wrap ft-g">
    <a class="ft-logo" href="{home(lang)}">VICTOR TSENG</a>
    <p class="ft-s">{e(c['based'])} · <time data-clock>--:--</time></p>
    <nav class="ft-l" aria-label="{e(c['lang_label'])}">{langsw}</nav>
    <p class="ft-c ft-soc"><a href="https://www.linkedin.com/in/victortsengtw/" rel="me noopener" target="_blank">LinkedIn</a> · <a href="https://www.instagram.com/victorinafrica/" rel="me noopener" target="_blank">Instagram</a> · <a href="https://www.youtube.com/@victorinafrica" rel="me noopener" target="_blank">YouTube</a> · <a href="https://www.tiktok.com/@victorinafrica" rel="me noopener" target="_blank">TikTok</a> · <a href="https://www.threads.com/@victorinafrica" rel="me noopener" target="_blank">Threads</a> · <a href="https://www.facebook.com/victortsengtw" rel="me noopener" target="_blank">Facebook</a></p>
    <p class="ft-c">© 2026 Victor Tseng 曾浩瑜 · VicTseng Consult · {e(c['rights'])} · <a href="{PATHS[lang]}copyright/">{e(c['copy_t'])}</a></p>
  </div>
</footer>
<button type="button" class="totop" data-down="{e(c['more'])}" data-up="{e(c['top'])}" aria-label="{e(c['more'])}"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path d="M12 5v14M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg><span class="fab-t">{e(c['more'])}</span></button>
<div class="sr" role="dialog" aria-modal="true" aria-label="{e(c['search'])}" hidden>
  <div class="sr-box">
    <div class="sr-in">{I_SEARCH}<input type="search" placeholder="{e(c['search_ph'])}" autocomplete="off" aria-label="{e(c['search'])}"><button type="button" data-close-search>{e(c['search_close'])}</button></div>
    <ul class="sr-res"></ul>
  </div>
</div>
<script id="sidx" type="application/json">{json.dumps(idx, ensure_ascii=False).replace('</', '<\\/')}</script>
<script>window.UI={json.dumps({'none': c['search_none']}, ensure_ascii=False)}</script>
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
"""


def search_index(lang, c):
    h = home(lang)
    idx = []
    for i, (t, l, tags) in enumerate(c["pillars"]):
        idx.append({"t": t, "s": c["sec_expertise"], "d": l + " " + " ".join(tags), "h": f"{h}#x-{i+1}"})
    for w in c["works"]:
        idx.append({"t": w["name"], "s": c["sec_work"], "d": w["line"] + " " + " ".join(w["facts"]) + " AKWABA Côte d'Ivoire 象牙海岸", "h": w["url"]})
    for slug in NOTES:
        n = note_for(slug, lang)
        idx.append({"t": n["title"], "s": c["sec_notes_t"], "d": n["description"] + " " + " ".join(n["tags"]) + " " + n["text"][:1500], "h": note_path(n["lang"], slug)})
    for p in PRESS:
        idx.append({"t": p["title"][lang], "s": c["sec_press_t"], "d": p["outlet"][lang] + " " + p["date"], "h": p["url"]})
    for k, o, d, wh in c["highlights"]:
        idx.append({"t": o, "s": f"{c['sec_exp']} · {k}", "d": f"{d} {wh}", "h": f"{h}#experience"})
    idx.append({"t": c["edu_line"], "s": c["edu_t"], "d": "MBA IAE HEC", "h": f"{h}#experience"})
    for i, key in enumerate(CAT_KEYS):
        idx.append({"t": c["pillars"][i][0], "s": c["sec_notes_t"], "d": c["pillars"][i][1], "h": cat_path(lang, key)})
    idx.append({"t": c["contact_t"], "s": c["sec_contact"], "d": EMAIL + " LinkedIn email " + c["email_btn"], "h": f"{h}#contact"})
    return idx


def person_ld(lang, c):
    return {"@type": "Person", "@id": DOMAIN + "/#victor", "name": "Victor Tseng",
            "alternateName": ["曾浩瑜", "Hao-yu Tseng", "Hao-yu (Victor) Tseng"],
            "jobTitle": c["job_title"], "url": DOMAIN + "/", "image": DOMAIN + "/assets/img/victor-tseng.jpg",
            "email": "mailto:" + EMAIL,
            "address": {"@type": "PostalAddress", "addressLocality": "Abidjan", "addressCountry": "CI"},
            "worksFor": {"@type": "Organization", "name": "VicTseng Consult", "alternateName": "維策顧問"},
            "alumniOf": [{"@type": "CollegeOrUniversity", "name": n} for n in ("IAE Paris-Est", "HEC Paris", "National Sun Yat-sen University")],
            "knowsLanguage": ["zh", "en", "fr"],
            "knowsAbout": ["African art", "Lifestyle in Abidjan", "Cross-cultural communication", "African business", "Côte d'Ivoire", "International market development"],
            "sameAs": ["https://www.linkedin.com/in/victortsengtw/", "https://www.instagram.com/victorinafrica/", "https://www.tiktok.com/@victorinafrica", "https://www.youtube.com/@victorinafrica", "https://www.threads.com/@victorinafrica", "https://www.facebook.com/victortsengtw", "https://linktr.ee/victsengconsult"] + ["https://maison.victseng.com/", "https://play.victseng.com/"]}


def stat_li(n, t):
    m = re.match(r"^(\D*)(\d[\d,]*)(.*)$", n)
    pre, num, suf = m.group(1), m.group(2).replace(",", ""), m.group(3)
    pre_h = f'<small>{e(pre)}</small>' if pre and not pre.isascii() else e(pre)
    suf_h = f'<small>{e(suf)}</small>' if suf and not suf.isascii() else e(suf)
    return f'<li class="rv"><b data-count="{num}">{pre_h}<span class="v">{e(m.group(2))}</span>{suf_h}</b><span>{e(t)}</span></li>'


def note_row(n, lang, c):
    badge = f'<span class="badge">{LANG_LABEL[n["lang"]]}</span>' if n["lang"] != lang else ""
    return f"""<li class="rv"><a class="row" href="{note_path(n['lang'], n['slug'])}">
      <span class="row-m"><time datetime="{n['date']}">{fmt_date(n['date'], lang)}</time><span>{e(pillar_name(n, lang))}</span><span>{n['mins']} {e(c['min_read'])}</span>{badge}</span>
      <span class="row-t">{e(n['title'])}</span>
      <span class="row-d">{e(n['description'])}</span>
      <span class="row-go">{e(c['read'])} {I_ARROW}</span></a></li>"""


def map_svg(lang, c):
    w, h = MAP["w"], MAP["h"]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r=".3"/>' for x, y in MAP["dots"])
    keys = ["paris", "dakar", "taipei", "abidjan"]
    P = {k: MAP["cities"][k] for k in keys}

    def arc(a, b, lift):
        (x1, y1), (x2, y2) = P[a], P[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - lift
        return f'<path class="arc" pathLength="1" d="M{x1} {y1} Q{mx:.2f} {my:.2f} {x2} {y2}"/>'
    arcs = arc("paris", "dakar", 4) + arc("dakar", "taipei", 14) + arc("taipei", "abidjan", -7)
    off = {"paris": (1.4, -0.9, "start"), "dakar": (-1.2, -1.6, "middle"), "taipei": (-1.2, -1.6, "end"), "abidjan": (1.6, 2.6, "start")}
    cities = ""
    for i, k in enumerate(keys):
        x, y = P[k]
        dx, dy, anc = off[k]
        name, yr = c["route"][i]
        live = k == "abidjan"
        pulse = f'<circle class="pulse" cx="{x}" cy="{y}" r="1"/><circle class="pulse p2" cx="{x}" cy="{y}" r="1"/>' if live else ""
        cls = "city live" if live else "city"
        r = 0.95 if live else 0.7
        cities += (f'<g class="{cls}">{pulse}<circle class="pt" cx="{x}" cy="{y}" r="{r}"/>'
                   f'<text x="{x+dx}" y="{y+dy}" text-anchor="{anc}"><tspan class="cn">{e(name)}</tspan><tspan class="cy" dx=".6">{e(yr)}</tspan></text></g>')
    labs = "".join(f'<text class="cont" x="{MAP["labels"][k][0]}" y="{MAP["labels"][k][1]}" text-anchor="middle">{e(t)}</text>'
                   for k, t in zip(("europe", "africa", "asia"), c["conts"]))
    aria = e(c["map_cap"]) + ": " + e(" → ".join(n for n, _ in c["route"]))
    ax, ay = P["abidjan"]
    return (f'<figure class="map rv"><svg viewBox="-1 -1 {w+2} {h+2}" role="img" aria-label="{aria}">'
            '<defs><radialGradient id="glow"><stop offset="0" stop-color="#C9A86A" stop-opacity=".9"/><stop offset="1" stop-color="#C9A86A" stop-opacity="0"/></radialGradient></defs>'
            f'<g class="dots">{dots}</g>{labs}<g class="arcs">{arcs}</g><circle class="halo" cx="{ax}" cy="{ay}" r="4.5" fill="url(#glow)"/>{cities}</svg>'
            f'<figcaption>{e(c["map_cap"])}</figcaption></figure>')


def banner(lang, c):
    return f"""<aside class="bn rv" aria-label="{e(c['b1_k'])}">
    <div class="wrap"><div class="bn-g">
      <span class="bn-pat" style="{pat('kita_light')}" aria-hidden="true"></span>
      <div class="bn-t"><p class="cap">{e(c['b1_k'])}</p><p class="bn-h">{e(c['b1_t'])}</p><p class="bn-d">{e(c['b1_d'])}</p></div>
      <a class="btn" href="{mailto(c['contact_subject'])}">{e(c['b1_btn'])} {I_ARROW}</a>
    </div></div>
  </aside>"""


def newsletter(lang, c):
    roles = "".join(f'<option value="{e(r)}">{e(r)}</option>' for r in c["roles"])
    checks = "".join(f'<label><input type="checkbox" name="topics" value="{e(t)}"><span>{e(t)}</span></label>' for t, _, _ in c["pillars"])
    return f"""<section class="nl" id="newsletter" aria-label="{e(c['nl_k'])}">
    <div class="wrap nl-g rv">
      <div><p class="cap">{e(c['nl_k'])}</p><h2 class="nl-h">{e(c['nl_t'])}</h2><p class="nl-d">{e(c['nl_d'])}</p><p class="nl-d">{e(c['nl_why'])}</p></div>
      <form class="nl-f" action="{e(CFG.get('newsletterEndpoint', ''))}" method="POST" data-ep="{e(CFG.get('newsletterEndpoint', ''))}" data-ok="{e(c['nl_ok'])}" data-err="{e(c['nl_err'])}" data-sending="{e(c['nl_sending'])}">
        <input type="hidden" name="language" value="{lang}">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="fr2">
          <label class="fl"><span>{e(c['nl_name'])} *</span><input type="text" name="name" required autocomplete="name"></label>
          <label class="fl"><span>{e(c['nl_ph'])} *</span><input type="email" name="email" required autocomplete="email" placeholder="name@example.com"></label>
        </div>
        <div class="fr2">
          <label class="fl"><span>{e(c['nl_role'])} *</span><select name="role" required><option value="">—</option>{roles}</select></label>
          <label class="fl"><span>{e(c['nl_company'])}</span><input type="text" name="company" autocomplete="organization"></label>
        </div>
        <fieldset class="chk"><legend>{e(c['nl_topics'])}</legend>{checks}</fieldset>
        <button class="btn" type="submit">{e(c['nl_btn'])} {I_ARROW}</button>
        <p class="nl-p">{e(c['nl_privacy'])}</p>
        <p class="nl-msg" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>"""


# ---------------------------------------------------------------- home
def home_page(lang):
    c = L(lang)
    alts = {l: PATHS[l] for l in LANGS}
    ld = {"@context": "https://schema.org", "@graph": [person_ld(lang, c),
          {"@type": "ProfilePage", "url": DOMAIN + PATHS[lang], "inLanguage": c["html_lang"], "mainEntity": {"@id": DOMAIN + "/#victor"}}]}
    lines = "".join(f'<span class="ln"><span>{x}</span></span>' for x in c["h1"].split("<br>"))
    doms = "".join(f'<li><a href="#x-{i+1}"><span class="n">{i+1:02d}</span><span class="t">{e(d)}</span>{I_ARROW}</a></li>' for i, d in enumerate(c["domains"]))
    mq_items = "".join(f"<span>{e(x)}</span><i>✦</i>" for x in c["marquee"])
    stats = "".join(
        stat_li(n, t) for n, t in c["stats"])
    pillars = "".join(f"""
      <li class="pl rv" id="x-{i+1}">
        <span class="pl-n">{i+1:02d}</span>
        <h3>{e(t)}</h3>
        <p>{e(l)}</p>
        <p class="pl-s">{' <i>·</i> '.join(e(s) for s in tags)}</p>
        <a class="pl-a" href="{cat_path(lang, CAT_KEYS[i])}">{e(c['read_cat'])} · {cat_count(CAT_KEYS[i])} {e(c['n_articles'])} {I_ARROW}</a>
      </li>""" for i, (t, l, tags) in enumerate(c["pillars"]))
    works = "".join((f"""
      <a class="wk wk-film rv" href="{w['url']}">
        <span class="wk-img"><img src="{w['img']}" width="640" height="800" alt="{e(w['alt'])}" loading="lazy"><span class="wk-new">{e(w['badge'])}</span></span>
        <span class="wk-in">
          <span class="cap">{e(w['sub'])}</span>
          <span class="wk-t">{e(w['name'])}</span>
          <span class="wk-l">{e(w['line'])}</span>
          <span class="wk-f">{' · '.join(e(f) for f in w['facts'])}</span>
          <span class="wk-go">{e(w['cta'])} {I_ARROW}</span>
        </span>
      </a>""" if w.get('img') else f"""
      <a class="wk wk-{w['tone']} rv" href="{w['url']}">
        <span class="wk-b" style="{pat(w['pat'] + ('_light' if w['tone'] == 'ivory' else '_color'))}" aria-hidden="true"></span>
        <span class="wk-in">
          <span class="cap">{e(w['sub'])}</span>
          <span class="wk-t">{e(w['name'])}</span>
          <span class="wk-l">{e(w['line'])}</span>
          <span class="wk-f">{' · '.join(e(f) for f in w['facts'])}</span>
          <span class="wk-go">{e(w['cta'])} {I_ARROW}</span>
        </span>
      </a>""") for w in c["works"])
    picked, seen = [], set()
    for s_ in NOTES:
        pn = pillar_name(note_for(s_, lang), lang)
        if pn not in seen:
            seen.add(pn); picked.append(s_)
    notes = "".join(note_row(note_for(s_, lang), lang, c) for s_ in picked[:4])
    press = "".join(f"""<li class="rv"><a class="row" href="{p['url']}" target="_blank" rel="noopener">
      <span class="row-m"><time datetime="{p['date']}">{fmt_date(p['date'], lang)}</time><span>{e(p['outlet'][lang])}</span>{f'<span class="badge">{LANG_LABEL[p["lang"]]}</span>' if p['lang'] != lang else ''}</span>
      <span class="row-t">{e(p['title'][lang])}</span>
      <span class="row-go">{e(p['outlet'][lang])} {I_OUT}</span></a></li>""" for p in PRESS)

    route = "".join(f'<li><span class="rt-c">{e(ci)}</span><span class="rt-y">{e(y)}</span></li>' for ci, y in c["route"])
    hls = "".join(f"""<li class="hl rv"><p class="cap">{e(k)}</p><h3>{e(o)}</h3><p class="hl-d">{e(d)}</p><p class="hl-w">{e(wh)}</p></li>""" for k, o, d, wh in c["highlights"])
    orgs = "".join(f"<li>{e(o)}</li>" for o in ORGS)
    navl = nav_for(c)
    total = len(navl)
    num = {k: i + 1 for i, (k, _) in enumerate(navl)}

    def sh(n, kicker, title, note=""):
        n = num[n] if isinstance(n, str) else n
        return f'<header class="sh rv"><p class="sh-k"><span>{n:02d} / {total:02d}</span>{e(kicker)}</p><h2>{e(title)}</h2>{f"<p class=sh-n>{e(note)}</p>" if note else ""}</header>'

    body = f"""
<main id="main">
  <section class="hero">
    <div class="wrap hero-g">
      <a class="hero-new" href="{c['works'][0]['url']}"><span class="hero-new-b">{e(c['works'][0]['badge'])}</span><span class="hero-new-t">{e(c['hero_new'])}</span>{I_ARROW}</a>
      <p class="cap hero-k">Africa × Asia — Cross-cultural</p>
      <h1 class="h1">{lines}</h1>
      <div class="hero-who">
        <p class="who"><strong>{e(c['who'])}</strong><span>{e(c['role'])}</span></p>
        <p class="one">{e(c['one'])}</p>
        <div class="ctas">
          <a class="btn" href="{mailto(c['contact_subject'])}">{e(c['cta1'])} {I_ARROW}</a>
          <a class="tl" href="#work">{e(c['cta2'])} {I_ARROW}</a>
        </div>
      </div>
      <figure class="arch">
        <picture><source srcset="/assets/img/victor-tseng.webp" type="image/webp"><img src="/assets/img/victor-tseng.jpg" width="800" height="1000" alt="{e(c['photo_alt'])}" fetchpriority="high"></picture>
      </figure>
      <ul class="doms">{doms}</ul>
    </div>
  </section>

  <div class="mq" aria-hidden="true"><div class="mq-in">{mq_items}{mq_items}</div></div>

  <section class="st" aria-label="Highlights"><ul class="wrap st-g">{stats}</ul></section>

  <section id="expertise" class="sec">
    <div class="wrap">{sh('expertise', c['sec_expertise'], c['sec_expertise_t'])}
      <ol class="pls">{pillars}
      </ol>
    </div>
  </section>

  {banner(lang, c)}

  <section id="work" class="sec dark">
    <div class="wrap">{sh('work', c['sec_work'], c['sec_work_t'])}
      <div class="wks">{works}
      </div>
    </div>
  </section>

  <section id="notes" class="sec">
    <div class="wrap">{sh('notes', c['sec_notes'], c['sec_notes_t'], c['notes_note'])}
      {cat_tiles(lang, c)}
      <ul class="rows">{notes}
      </ul>
      <a class="tl more-l" href="{notes_path(lang)}">{e(c['notes_all'])} · {len(NOTES)} {e(c['n_articles'])} {I_ARROW}</a>
    </div>
  </section>

  {podcast_section(lang, c, sh) if POD_LIVE else ""}

  {newsletter(lang, c)}

  <section id="press" class="sec alt">
    <div class="wrap">{sh('press', c['sec_press'], c['sec_press_t'], c['press_note'])}
      <ul class="rows">{press}
      </ul>
    </div>
  </section>

  <section id="experience" class="sec">
    <div class="wrap">{sh('experience', c['sec_exp'], c['exp_t'])}
      <div class="ex">
        {map_svg(lang, c)}
        <ul class="hls">{hls}</ul>
        <div class="orgs rv"><p class="cap">{e(c['orgs_t'])}</p><ul>{orgs}</ul></div>
        <div class="ex-f rv"><p class="edu">{e(c['edu_line'])}</p><p class="lgs">{e(c['langs'])}</p>
          <a class="tl" href="{mailto(c['cv_subject'])}">{e(c['cv'])} {I_ARROW}</a></div>
      </div>
    </div>
  </section>

  <section id="contact" class="sec dark ct">
    <div class="wrap">{sh('contact', c['sec_contact'], c['contact_t'], c['contact_line'])}
      <div class="ctas rv">
        <a class="btn btn-l" href="{mailto(c['contact_subject'])}">{I_MAIL} {e(c['email_btn'])}</a>
        <a class="tl tl-l" href="{LINKEDIN}" target="_blank" rel="noopener me">{I_LI} LinkedIn {I_OUT}</a>
      </div>
      <p class="mail">{EMAIL}</p>
    </div>
  </section>
</main>"""
    return (head(lang, c, c["title"], c["description"], PATHS[lang], alts, f"/assets/img/og-{lang}.jpg", "profile", ld)
            + header(lang, c, alts, True) + body + footer(lang, c, alts, search_index(lang, c)))


# ---------------------------------------------------------------- notes index
def notes_index(lang):
    c = L(lang)
    alts = {l: notes_path(l) for l in LANGS}
    rows = "".join(note_row(note_for(s, lang), lang, c).replace('<li class="rv">', f'<li class="rv" data-p="{e(pillar_name(note_for(s, lang), lang))}">', 1) for s in NOTES)
    pills = sorted({pillar_name(note_for(s, lang), lang) for s in NOTES} - {""})
    order = [t for t, _, _ in c["pillars"]]
    pills = sorted(pills, key=lambda x: order.index(x) if x in order else 99)
    filt = f'<div class="flt" role="group"><button type="button" class="on" data-f="">{e(c["all_cat"])} <span>{len(NOTES)}</span></button>' + "".join(
        f'<button type="button" data-f="{e(p)}">{e(p)} <span>{sum(1 for s in NOTES if pillar_name(note_for(s, lang), lang) == p)}</span></button>' for p in pills) + "</div>"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": c["notes_page_t"], "url": DOMAIN + notes_path(lang),
          "inLanguage": c["html_lang"], "author": {"@id": DOMAIN + "/#victor"}}
    body = f"""
<main id="main" class="page">
  <div class="wrap">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a><span>/</span><span>{e(c['sec_notes_t'])}</span></nav>
    <header class="sh pg-h"><p class="sh-k">{e(c['sec_notes'])}</p><h1>{e(c['notes_page_t'])}</h1><p class="sh-n">{e(c['notes_note'])}</p></header>
    {cat_tiles(lang, c)}
    {filt}
    <ul class="rows" data-list>{rows}</ul>
  </div>
</main>
{newsletter(lang, c)}"""
    return (head(lang, c, f"{c['notes_page_t']}｜Victor Tseng 曾浩瑜", c["notes_page_d"], notes_path(lang), alts, f"/assets/img/og-{lang}.jpg", "website", ld)
            + header(lang, c, alts, False) + body + footer(lang, c, alts, search_index(lang, c)))


def related(slug, lang, c):
    key = cat_key(NOTES[slug][lang])
    others = [s for s in NOTES if s != slug and cat_key(next(iter(NOTES[s].values()))) == key][:3]
    if not others:
        return ""
    rows = "".join(note_row(note_for(s, lang), lang, c) for s in others)
    return f'<section class="rel"><p class="sh-k">{e(c["related_t"])}</p><ul class="rows">{rows}</ul><a class="tl more-l" href="{cat_path(lang, key)}">{e(c["read_cat"])} {I_ARROW}</a></section>'


def cat_page(lang, key):
    c = L(lang)
    i = CAT_KEYS.index(key)
    name, line, tags = c["pillars"][i]
    alts = {l: cat_path(l, key) for l in LANGS}
    items = [s for s in NOTES if cat_key(next(iter(NOTES[s].values()))) == key]
    rows = "".join(note_row(note_for(s, lang), lang, c) for s in items)
    others = "".join(f'<a href="{cat_path(lang, k)}"{" aria-current=page" if k == key else ""}>{e(c["pillars"][j][0])}</a>' for j, k in enumerate(CAT_KEYS))
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{name} · {c['sec_notes_t']}", "url": DOMAIN + cat_path(lang, key),
          "inLanguage": c["html_lang"], "author": {"@id": DOMAIN + "/#victor"}}
    body = f"""
<main id="main" class="page">
  <div class="cat-hero" style="{pat(CAT_PAT[key])}" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a><span>/</span><a href="{notes_path(lang)}">{e(c['sec_notes_t'])}</a></nav>
    <header class="sh pg-h"><p class="sh-k">{i+1:02d} · {e(c['sec_notes_t'])}</p><h1>{e(name)}</h1><p class="sh-n">{e(line)}</p>
      <p class="motif-n">{e(c['motif_note'].format(m=CAT_MOTIF[lang][key]))} · {len(items)} {e(c['n_articles'])}</p></header>
    <nav class="cat-nav">{others}</nav>
    <ul class="rows">{rows}</ul>
  </div>
</main>
{newsletter(lang, c)}"""
    title = f"{name}｜{c['sec_notes_t']}｜Victor Tseng"
    desc = c["cat_page_d"].format(name=name, line=line)
    return (head(lang, c, title, desc, cat_path(lang, key), alts, f"/assets/img/og-{lang}.jpg", "website", ld)
            + header(lang, c, alts, False) + body + footer(lang, c, alts, search_index(lang, c)))


# ---------------------------------------------------------------- note page
def note_page(slug, lang):
    n = NOTES[slug][lang]
    c = L(lang)
    alts = {l: note_path(l, slug) for l in NOTES[slug]}
    others = [l for l in NOTES[slug] if l != lang]
    avail = (f'<p class="avail">{e(c["avail"])} ' + " · ".join(f'<a href="{note_path(l, slug)}" hreflang="{HREFLANG[l]}">{LANG_NAME[l]}</a>' for l in others) + "</p>") if others else ""
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": n["title"], "description": n["description"],
          "datePublished": n["date"], "dateModified": n.get("updated", n["date"]), "inLanguage": c["html_lang"],
          "mainEntityOfPage": DOMAIN + note_path(lang, slug), "image": (IMAGES.get(slug) or {}).get("src") or DOMAIN + f"/assets/img/og-{lang if lang in C else 'zh'}.jpg",
          "keywords": ", ".join(n["tags"]),
          "author": person_ld(lang, c), "publisher": {"@type": "Person", "name": "Victor Tseng"}}
    tags = "".join(f"<li>{e(t)}</li>" for t in n["tags"])
    body = f"""
<main id="main" class="page">
  <article class="wrap art">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a><span>/</span><a href="{notes_path(lang)}">{e(c['sec_notes_t'])}</a></nav>
    <header class="art-h">
      <span class="art-band" style="{pat(CAT_PAT[cat_key(n)])}" aria-hidden="true"></span>
      <p class="sh-k"><a href="{cat_path(lang, cat_key(n))}">{e(pillar_name(n, lang))}</a></p>
      <h1>{e(n['title'])}</h1>
      <p class="art-m"><span>{e(c['by'])} Victor Tseng 曾浩瑜</span><time datetime="{n['date']}">{fmt_date(n['date'], lang)}</time><span>{n['mins']} {e(c['min_read'])}</span></p>
      {avail}
    </header>
    <div class="prose">{enrich(slug, lang, n['html'])}</div>
    <ul class="art-tags">{tags}</ul>
    <p class="motif-n">{e(c['motif_note'].format(m=CAT_MOTIF[lang][cat_key(n)]))}</p>
    {pod_for_note(slug, lang, c)}
    {related(slug, lang, c)}
    <aside class="art-cta">
      <p>{e(c['note_cta_t'])}</p>
      <a class="btn" href="{mailto(c['contact_subject'] + ' · ' + n['title'])}">{e(c['note_cta'])} {I_ARROW}</a>
    </aside>
  </article>
</main>
{newsletter(lang, c)}"""
    return (head(lang, c, f"{n['title']}｜Victor Tseng", n["description"], note_path(lang, slug), alts, f"/assets/img/og-{lang}.jpg", "article", ld)
            + header(lang, c, alts, False) + body + footer(lang, c, alts, search_index(lang, c)))


def copyright_page(lang):
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


# ---------------------------------------------------------------- 阿南西講古 (animation series, zh + en + fr)
ANANSI_PATH = "/anansi/"
ANANSI_EPS = [
    ("EP1", "智慧罐", "阿坎族", "已上線"),
    ("EP2", "故事是怎麼來的", "阿坎族", "下一集"),
    ("EP3", "我的名字叫「大家」", "伊博族", ""),
    ("EP4", "回頭拿，不丟臉", "阿坎族", ""),
    ("EP5", "小兔 Leuk 與鬣狗 Bouki", "塞內加爾", ""),
    ("EP6", "這句真的是非洲諺語嗎？", "查證特別篇", ""),
]
ANANSI_SRC = [
    ("W. H. Barker & Cecilia Sinclair, West African Folk-Tales (London: Harrap, 1917)", "https://www.gutenberg.org/ebooks/66923"),
    ("Britannica, “Ananse”", "https://www.britannica.com/topic/Ananse"),
    ("R. S. Rattray, Akan-Ashanti Folk-Tales (1930)，引自 Legon Journal of the Humanities 30.1 (2019)", "https://core.ac.uk/download/478450654.pdf"),
    ("Bernard B. Dadié, Le Pagne noir (Présence Africaine, 1955)", "https://catalogue.bnf.fr/ark:/12148/cb329730022"),
    ("Ananse Ntontan，釋義出自 W. Bruce Willis, The Adinkra Dictionary", "https://adinkrasymbols.org/symbols/ananse-ntentan"),
]


def anansi_page(lang="zh"):
    c = L(lang)
    alts = ANANSI_ALTS
    yt = "https://www.youtube.com/@victorinafrica"
    title = "阿南西講古｜西非老故事，黏土動畫說給你聽"
    desc = "用黏土逐格動畫重新講西非阿坎族的阿南西蜘蛛故事。每集附故事出處與文化小筆記。"
    ld = {"@context": "https://schema.org", "@type": "VideoObject", "name": "阿南西講古 EP1 智慧罐",
          "description": "阿南西想把全世界的智慧裝進罐子藏到樹頂，兒子一句話讓他氣到把罐子摔碎。改編自西非阿坎族民間故事。",
          "thumbnailUrl": DOMAIN + "/assets/anansi/ep1-poster.jpg", "contentUrl": DOMAIN + "/assets/anansi/ep1.mp4",
          "uploadDate": "2026-11-06", "duration": "PT1M8S", "inLanguage": "zh-Hant",
          "creator": person_ld(lang, c)}
    eps = "".join(
        f'<li class="an-ep"><span class="an-ep-n">{n}</span><span class="an-ep-t">{e(t)}</span><span class="an-ep-o">{e(o)}</span>'
        + (f'<span class="an-ep-s">{e(s)}</span>' if s else "") + "</li>" for n, t, o, s in ANANSI_EPS)
    srcs = "".join(f'<li><a class="il" href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in ANANSI_SRC)
    game = "https://play.victseng.com/?c=site&utm_source=victseng&utm_medium=website&utm_campaign=anansi"
    maison = "https://maison.victseng.com/?utm_source=victseng&utm_medium=website&utm_campaign=anansi"
    body = f"""
<main id="main" class="page">
  <article class="wrap art anp">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a><span>/</span><span>阿南西講古</span></nav>
    <header class="art-h">
      <span class="art-band" style="{pat('kita_light')}" aria-hidden="true"></span>
      <p class="sh-k">黏土動畫系列</p>
      <h1>阿南西講古</h1>
      <p class="an-lede">阿南西是西非阿坎族民間故事裡的蜘蛛。他聰明、貪心又愛面子，常常被自己的聰明害到。這個系列用黏土逐格動畫重新講他的故事，每一集都寫清楚出自哪個民族、哪本書。</p>
      <p class="art-m"><span>{e(c['by'])} Victor Tseng 曾浩瑜</span><span>每兩週週四 20:00（台灣時間）更新</span></p>
    </header>

    <section class="an-ep1" aria-labelledby="ep1">
      <div class="an-vid"><video controls playsinline preload="metadata" poster="/assets/anansi/ep1-poster.jpg" width="720" height="1280"><source src="/assets/anansi/ep1.mp4" type="video/mp4"></video></div>
      <div class="an-ep1-t">
        <p class="sh-k">EP1 · 68 秒</p>
        <h2 id="ep1" class="an-h2">智慧罐</h2>
        <p>阿南西想把全世界的智慧都收進一個罐子，藏到最高的樹頂。罐子綁在胸前，他怎麼爬都爬不上去。兒子在樹下說了一句話，他氣到把罐子摔碎，智慧從此散到全世界。</p>
        <p class="an-q">你最近一次，從比你年輕的人身上學到什麼？</p>
        <p class="ctas"><a class="btn" href="{yt}" target="_blank" rel="noopener">到 YouTube 留言 {I_ARROW}</a></p>
      </div>
    </section>

    <div class="prose">
      <h2>故事出處</h2>
      <p>改編自西非阿坎族民間故事〈How Wisdom Became the Property of the Human Race〉，收錄於 W. H. Barker 與 Cecilia Sinclair 編的《West African Folk-Tales》（London: Harrap, 1917）。這本書已進入公有領域，可以在 <a class="il" href="https://www.gutenberg.org/ebooks/66923" target="_blank" rel="noopener">Project Gutenberg</a> 免費閱讀。</p>
      <p>原故事裡，阿南西把罐子綁在胸前爬不上樹，兒子提醒他綁在背上，他一氣之下把罐子摔碎。動畫裡「爬樹失敗三次」和「兒子在樹下偷笑」是改編加入的情節。</p>

      <h2>文化小筆記</h2>
      <p><strong>阿坎族是誰。</strong>阿坎人主要住在迦納和象牙海岸，象牙海岸的包勒人（Baoulé）、阿尼人（Agni）都屬於阿坎族群。阿南西的故事，就是他們晚上圍坐著講的故事。</p>
      <p><strong>「蜘蛛故事」。</strong>在阿坎傳說裡，阿南西向天神 Nyame 買下了天上所有的故事，所以這些故事都叫 Anansesem，意思是「蜘蛛故事」。</p>
      <p><strong>在象牙海岸，他叫 Kacou Ananzè。</strong>象牙海岸作家 Bernard B. Dadié 在 1955 年的故事集《Le Pagne noir》裡，蜘蛛主角就叫這個名字。</p>
      <p><strong>蜘蛛網的意思。</strong>阿坎族的 Adinkra 符號裡，有一個叫 Ananse Ntontan，意思是「蜘蛛網」，代表智慧、創意和人生的複雜。</p>
    </div>

    <section class="an-cast" aria-labelledby="cast">
      <h2 id="cast" class="an-h2">角色</h2>
      <div class="an-cast-g">
        <figure><img src="/assets/anansi/anansi.jpg" width="600" height="600" alt="黏土動畫角色阿南西：戴著黃色帽子、繫彩色條紋腰帶的深棕色蜘蛛" loading="lazy"><figcaption><strong>阿南西 Kwaku Ananse</strong>聰明、貪心、愛面子。八隻腳，上面四隻當手用。</figcaption></figure>
        <figure><img src="/assets/anansi/family.jpg" width="600" height="600" alt="夜晚，阿南西坐在地上，兒子恩提庫馬拍著他的背" loading="lazy"><figcaption><strong>恩提庫馬 Ntikuma</strong>阿南西的兒子，敢當面講真話。<br><strong>阿索 Aso</strong>阿南西的妻子，家裡真正的軍師，下一集登場。</figcaption></figure>
      </div>
    </section>

    <section class="an-list" aria-labelledby="season">
      <h2 id="season" class="an-h2">第一季</h2>
      <ol class="an-eps">{eps}</ol>
    </section>

    <section class="an-more" aria-labelledby="more">
      <h2 id="more" class="an-h2">想認識更多非洲</h2>
      <p class="ctas"><a class="btn" href="{game}">玩《Akwaba！非洲大冒險》 {I_ARROW}</a><a class="tl" href="{maison}">逛 AKWABA・非洲品味之家 {I_ARROW}</a></p>
    </section>

    <div class="prose an-src">
      <h2>參考資料</h2>
      <ol>{srcs}</ol>
      <p class="an-note">角色造型為原創設計。© 2026 Victor Tseng 曾浩瑜</p>
    </div>
  </article>
</main>
{newsletter(lang, c)}"""
    return (head(lang, c, title, desc, ANANSI_PATH, alts, "/assets/anansi/og.jpg", "website", ld)
            + header(lang, c, alts, False) + body + footer(lang, c, alts, search_index(lang, c)))


ANANSI_FR_PATH = "/fr/anansi/"
ANANSI_EN_PATH = "/en/anansi/"
ANANSI_ALTS = {"zh": ANANSI_PATH, "en": ANANSI_EN_PATH, "fr": ANANSI_FR_PATH}
ANANSI_EPS_FR = [
    ("EP1", "Le pot de la sagesse", "Akan", "En ligne"),
    ("EP2", "D’où viennent les histoires", "Akan", "Prochain épisode"),
    ("EP3", "Je m’appelle « Tout le monde »", "Igbo", ""),
    ("EP4", "Revenir chercher n’est pas une honte", "Akan", ""),
    ("EP5", "Leuk le lièvre et Bouki l’hyène", "Sénégal", ""),
    ("EP6", "Ce proverbe est-il vraiment africain ?", "Épisode vérification", ""),
]


def anansi_page_fr():
    lang = "fr"
    c = L(lang)
    title = "Les contes d’Anansi · Contes d’Afrique de l’Ouest en pâte à modeler"
    desc = "Les histoires de l’araignée Anansi, tirées des contes akan, racontées en animation image par image en pâte à modeler. Chaque épisode cite ses sources."
    ld = {"@context": "https://schema.org", "@type": "VideoObject", "name": "Les contes d’Anansi EP1 · Le pot de la sagesse",
          "description": "Anansi veut cacher toute la sagesse du monde dans un pot, en haut d’un arbre. Une phrase de son fils le met tellement en colère qu’il brise le pot. Adapté d’un conte akan d’Afrique de l’Ouest.",
          "thumbnailUrl": DOMAIN + "/assets/anansi/ep1-poster-fr.jpg", "contentUrl": DOMAIN + "/assets/anansi/ep1-fr.mp4",
          "uploadDate": "2026-11-06", "duration": "PT1M8S", "inLanguage": "fr",
          "creator": person_ld(lang, c)}
    eps = "".join(
        f'<li class="an-ep"><span class="an-ep-n">{n}</span><span class="an-ep-t">{e(t)}</span><span class="an-ep-o">{e(o)}</span>'
        + (f'<span class="an-ep-s">{e(s)}</span>' if s else "") + "</li>" for n, t, o, s in ANANSI_EPS_FR)
    srcs = "".join(f'<li><a class="il" href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in ANANSI_SRC[:2])
    srcs += '<li><a class="il" href="https://core.ac.uk/download/478450654.pdf" target="_blank" rel="noopener">R. S. Rattray, Akan-Ashanti Folk-Tales (1930), cité dans Legon Journal of the Humanities 30.1 (2019)</a></li>'
    srcs += f'<li><a class="il" href="{ANANSI_SRC[3][1]}" target="_blank" rel="noopener">{e(ANANSI_SRC[3][0])}</a></li>'
    srcs += '<li><a class="il" href="https://adinkrasymbols.org/symbols/ananse-ntentan" target="_blank" rel="noopener">Ananse Ntontan, d’après W. Bruce Willis, The Adinkra Dictionary</a></li>'
    game = "https://play.victseng.com/?c=site&utm_source=victseng&utm_medium=website&utm_campaign=anansi_fr"
    maison = "https://maison.victseng.com/?utm_source=victseng&utm_medium=website&utm_campaign=anansi_fr"
    body = f"""
<main id="main" class="page">
  <article class="wrap art anp">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a><span>/</span><span>Les contes d’Anansi</span></nav>
    <header class="art-h">
      <span class="art-band" style="{pat('kita_light')}" aria-hidden="true"></span>
      <p class="sh-k">Série d’animation en pâte à modeler</p>
      <h1>Les contes d'Anansi</h1>
      <p class="an-lede">Anansi est l’araignée des contes du peuple akan, au Ghana et en Côte d’Ivoire, où on l’appelle aussi Kacou Ananzè. Rusé, gourmand et orgueilleux, il se fait souvent piéger par sa propre malice. Cette série raconte ses histoires en animation image par image, en pâte à modeler, et chaque épisode précise de quel peuple et de quel livre vient le conte.</p>
      <p class="art-m"><span>{e(c['by'])} Victor Tseng 曾浩瑜</span><span>Un nouvel épisode un jeudi sur deux</span></p>
    </header>

    <section class="an-ep1" aria-labelledby="ep1">
      <div class="an-vid"><video controls playsinline preload="metadata" poster="/assets/anansi/ep1-poster-fr.jpg" width="720" height="1280"><source src="/assets/anansi/ep1-fr.mp4" type="video/mp4"></video></div>
      <div class="an-ep1-t">
        <p class="sh-k">EP1 · 68 secondes</p>
        <h2 id="ep1" class="an-h2">Le pot de la sagesse</h2>
        <p>Anansi veut réunir toute la sagesse du monde dans un pot et le cacher en haut du plus grand arbre. Le pot attaché sur le ventre, il n’arrive pas à grimper. En bas, son fils lui glisse une idée toute simple. Vexé, Anansi jette le pot par terre, et la sagesse se répand dans le monde entier.</p>
        <p class="an-q">Qu’as-tu appris récemment d’une personne plus jeune que toi ?</p>
      </div>
    </section>

    <div class="prose">
      <h2>D'où vient ce conte</h2>
      <p>Adapté du conte akan « How Wisdom Became the Property of the Human Race », publié dans <em>West African Folk-Tales</em> de W. H. Barker et Cecilia Sinclair (London, Harrap, 1917). Le livre est dans le domaine public et se lit gratuitement sur <a class="il" href="https://www.gutenberg.org/ebooks/66923" target="_blank" rel="noopener">Project Gutenberg</a>.</p>
      <p>Dans le conte d’origine, Anansi attache le pot sur son ventre et ne peut pas grimper. Son fils lui conseille de le mettre dans son dos, et Anansi, furieux, brise le pot. Les trois tentatives ratées et le fils qui observe depuis le pied de l’arbre ont été ajoutés pour l’animation.</p>

      <h2>Petites notes culturelles</h2>
      <p><strong>Qui sont les Akan.</strong> Les Akan vivent surtout au Ghana et en Côte d’Ivoire. Les Baoulé et les Agni de Côte d’Ivoire font partie de ce groupe. Les histoires d’Anansi, ce sont les contes qu’on se raconte le soir chez eux.</p>
      <p><strong>Les « histoires de l’araignée ».</strong> Selon la tradition akan, Anansi a acheté au dieu du ciel Nyame toutes les histoires du monde. C’est pourquoi on les appelle Anansesem, « histoires de l’araignée ».</p>
      <p><strong>En Côte d’Ivoire, il s’appelle Kacou Ananzè.</strong> C’est le nom de l’araignée dans <em>Le Pagne noir</em> (1955), le recueil de contes de l’écrivain ivoirien Bernard B. Dadié.</p>
      <p><strong>La toile d’araignée.</strong> Parmi les symboles adinkra des Akan, Ananse Ntontan signifie « toile d’araignée ». Il représente la sagesse, la créativité et la complexité de la vie.</p>
    </div>

    <section class="an-cast" aria-labelledby="cast">
      <h2 id="cast" class="an-h2">Les personnages</h2>
      <div class="an-cast-g">
        <figure><img src="/assets/anansi/anansi.jpg" width="600" height="600" alt="Anansi en pâte à modeler : une araignée brun foncé avec un chapeau jaune et une ceinture à rayures colorées" loading="lazy"><figcaption><strong>Anansi · Kwaku Ananse</strong>Malin, gourmand et orgueilleux. Il a huit pattes et se sert des quatre du haut comme de mains.</figcaption></figure>
        <figure><img src="/assets/anansi/family.jpg" width="600" height="600" alt="La nuit, Anansi assis par terre, son fils Ntikuma lui tapote le dos" loading="lazy"><figcaption><strong>Ntikuma</strong>Le fils d’Anansi, qui ose lui dire la vérité en face.<br><strong>Aso</strong>La femme d’Anansi, la vraie stratège de la famille. Elle arrive dans le prochain épisode.</figcaption></figure>
      </div>
    </section>

    <section class="an-list" aria-labelledby="season">
      <h2 id="season" class="an-h2">Saison 1</h2>
      <ol class="an-eps">{eps}</ol>
    </section>

    <section class="an-more" aria-labelledby="more">
      <h2 id="more" class="an-h2">Pour découvrir l'Afrique autrement</h2>
      <p class="ctas"><a class="btn" href="{game}">Jouer à « Akwaba ! Une aventure africaine » {I_ARROW}</a><a class="tl" href="{maison}">Découvrir AKWABA · Maison de Goût Africain {I_ARROW}</a></p>
    </section>

    <div class="prose an-src">
      <h2>Sources</h2>
      <ol>{srcs}</ol>
      <p class="an-note">Personnages créés pour la série. © 2026 Victor Tseng 曾浩瑜</p>
    </div>
  </article>
</main>
{newsletter(lang, c)}"""
    return (head(lang, c, title, desc, ANANSI_FR_PATH, ANANSI_ALTS, "/assets/anansi/og.jpg", "website", ld)
            + header(lang, c, ANANSI_ALTS, False) + body + footer(lang, c, ANANSI_ALTS, search_index(lang, c)))


ANANSI_EPS_EN = [
    ("EP1", "The Pot of Wisdom", "Akan", "Out now"),
    ("EP2", "Where Stories Come From", "Akan", "Next"),
    ("EP3", "My Name Is “All of You”", "Igbo", ""),
    ("EP4", "Going Back Is No Shame", "Akan", ""),
    ("EP5", "Leuk the Hare and Bouki the Hyena", "Senegal", ""),
    ("EP6", "Is That Really an African Proverb?", "Fact-check special", ""),
]


def anansi_page_en():
    lang = "en"
    c = L(lang)
    title = "Anansi Tales · West African folktales in clay animation"
    desc = "Stories of Anansi the spider from Akan folklore, retold in handmade clay stop-motion animation. Every episode names the people and the book the tale comes from."
    ld = {"@context": "https://schema.org", "@type": "VideoObject", "name": "Anansi Tales EP1 · The Pot of Wisdom",
          "description": "Anansi wants to hide all the world's wisdom in a pot at the top of a tree. One sentence from his son makes him so angry that he smashes the pot. Adapted from an Akan folktale of West Africa.",
          "thumbnailUrl": DOMAIN + "/assets/anansi/ep1-poster-en.jpg", "contentUrl": DOMAIN + "/assets/anansi/ep1-en.mp4",
          "uploadDate": "2026-11-06", "duration": "PT1M8S", "inLanguage": "en",
          "creator": person_ld(lang, c)}
    eps = "".join(
        f'<li class="an-ep"><span class="an-ep-n">{n}</span><span class="an-ep-t">{e(t)}</span><span class="an-ep-o">{e(o)}</span>'
        + (f'<span class="an-ep-s">{e(s)}</span>' if s else "") + "</li>" for n, t, o, s in ANANSI_EPS_EN)
    srcs = "".join(f'<li><a class="il" href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in ANANSI_SRC[:2])
    srcs += '<li><a class="il" href="https://core.ac.uk/download/478450654.pdf" target="_blank" rel="noopener">R. S. Rattray, Akan-Ashanti Folk-Tales (1930), cited in Legon Journal of the Humanities 30.1 (2019)</a></li>'
    srcs += f'<li><a class="il" href="{ANANSI_SRC[3][1]}" target="_blank" rel="noopener">{e(ANANSI_SRC[3][0])}</a></li>'
    srcs += '<li><a class="il" href="https://adinkrasymbols.org/symbols/ananse-ntentan" target="_blank" rel="noopener">Ananse Ntontan, as defined in W. Bruce Willis, The Adinkra Dictionary</a></li>'
    game = "https://play.victseng.com/en.html?c=site&utm_source=victseng&utm_medium=website&utm_campaign=anansi_en"
    maison = "https://maison.victseng.com/en/?utm_source=victseng&utm_medium=website&utm_campaign=anansi_en"
    body = f"""
<main id="main" class="page">
  <article class="wrap art anp">
    <nav class="crumb"><a href="{home(lang)}">{e(c['back'])}</a><span>/</span><span>Anansi Tales</span></nav>
    <header class="art-h">
      <span class="art-band" style="{pat('kita_light')}" aria-hidden="true"></span>
      <p class="sh-k">Clay animation series</p>
      <h1>Anansi Tales</h1>
      <p class="an-lede">Anansi is the spider of Akan folktales from Ghana and Côte d'Ivoire, where he is also known as Kacou Ananzè. Clever, greedy and proud, he is often caught out by his own cleverness. This series retells his stories in handmade clay stop-motion, and every episode names the people and the book each tale comes from.</p>
      <p class="art-m"><span>{e(c['by'])} Victor Tseng 曾浩瑜</span><span>A new episode every other Thursday</span></p>
    </header>

    <section class="an-ep1" aria-labelledby="ep1">
      <div class="an-vid"><video controls playsinline preload="metadata" poster="/assets/anansi/ep1-poster-en.jpg" width="720" height="1280"><source src="/assets/anansi/ep1-en.mp4" type="video/mp4"></video></div>
      <div class="an-ep1-t">
        <p class="sh-k">EP1 · 68 seconds</p>
        <h2 id="ep1" class="an-h2">The Pot of Wisdom</h2>
        <p>Anansi wants to gather all the world's wisdom in one pot and hide it at the top of the tallest tree. With the pot tied to his chest, he cannot climb. Down below, his son offers a very simple idea. Stung, Anansi throws the pot to the ground, and wisdom spreads across the whole world.</p>
        <p class="an-q">What did you last learn from someone younger than you?</p>
        <p class="ctas"><a class="btn" href="https://www.youtube.com/@victorinafrica" target="_blank" rel="noopener">Comment on YouTube {I_ARROW}</a></p>
      </div>
    </section>

    <div class="prose">
      <h2>Where the story comes from</h2>
      <p>Adapted from the Akan tale “How Wisdom Became the Property of the Human Race”, published in <em>West African Folk-Tales</em> by W. H. Barker and Cecilia Sinclair (London: Harrap, 1917). The book is in the public domain and free to read on <a class="il" href="https://www.gutenberg.org/ebooks/66923" target="_blank" rel="noopener">Project Gutenberg</a>.</p>
      <p>In the original tale, Anansi ties the pot to his front and cannot climb. His son tells him to tie it on his back, and Anansi smashes the pot in anger. The three failed attempts and the son watching from the foot of the tree were added for the animation.</p>

      <h2>Cultural notes</h2>
      <p><strong>Who the Akan are.</strong> The Akan live mainly in Ghana and Côte d'Ivoire. The Baoulé and Agni peoples of Côte d'Ivoire belong to this group. Anansi stories are the tales told in their homes in the evening.</p>
      <p><strong>“Spider stories”.</strong> In Akan tradition, Anansi bought all the stories in the world from the sky god Nyame. That is why they are called Anansesem, “spider stories”.</p>
      <p><strong>In Côte d'Ivoire, he is Kacou Ananzè.</strong> That is the spider's name in <em>Le Pagne noir</em> (1955), a collection of tales by the Ivorian writer Bernard B. Dadié.</p>
      <p><strong>The spider's web.</strong> Among the Akan adinkra symbols, Ananse Ntontan means “spider's web”. It stands for wisdom, creativity and the complexity of life.</p>
    </div>

    <section class="an-cast" aria-labelledby="cast">
      <h2 id="cast" class="an-h2">Characters</h2>
      <div class="an-cast-g">
        <figure><img src="/assets/anansi/anansi.jpg" width="600" height="600" alt="Anansi in clay: a dark brown spider with a yellow hat and a colourful striped belt" loading="lazy"><figcaption><strong>Anansi · Kwaku Ananse</strong>Clever, greedy and proud. He has eight legs and uses the top four as hands.</figcaption></figure>
        <figure><img src="/assets/anansi/family.jpg" width="600" height="600" alt="At night, Anansi sits on the ground while his son Ntikuma pats his back" loading="lazy"><figcaption><strong>Ntikuma</strong>Anansi's son, who dares to tell him the truth.<br><strong>Aso</strong>Anansi's wife and the family's real strategist. She appears in the next episode.</figcaption></figure>
      </div>
    </section>

    <section class="an-list" aria-labelledby="season">
      <h2 id="season" class="an-h2">Season 1</h2>
      <ol class="an-eps">{eps}</ol>
    </section>

    <section class="an-more" aria-labelledby="more">
      <h2 id="more" class="an-h2">Discover more of Africa</h2>
      <p class="ctas"><a class="btn" href="{game}">Play Akwaba! An African Adventure {I_ARROW}</a><a class="tl" href="{maison}">Visit AKWABA · House of African Taste {I_ARROW}</a></p>
    </section>

    <div class="prose an-src">
      <h2>References</h2>
      <ol>{srcs}</ol>
      <p class="an-note">Characters designed for the series. © 2026 Victor Tseng 曾浩瑜</p>
    </div>
  </article>
</main>
{newsletter(lang, c)}"""
    return (head(lang, c, title, desc, ANANSI_EN_PATH, ANANSI_ALTS, "/assets/anansi/og.jpg", "website", ld)
            + header(lang, c, ANANSI_ALTS, False) + body + footer(lang, c, ANANSI_ALTS, search_index(lang, c)))


# ---------------------------------------------------------------- write
def write(path, text):
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)


urls = []
for l in LANGS:
    write(PATHS[l] + "index.html", home_page(l)); urls.append(({x: PATHS[x] for x in LANGS}, PATHS[l], None))
    write(notes_path(l) + "index.html", notes_index(l)); urls.append(({x: notes_path(x) for x in LANGS}, notes_path(l), None))
    for key in CAT_KEYS:
        write(cat_path(l, key) + "index.html", cat_page(l, key)); urls.append(({x: cat_path(x, key) for x in LANGS}, cat_path(l, key), None))
for l in LANGS:
    write(PATHS[l] + "copyright/index.html", copyright_page(l)); urls.append(({x: PATHS[x] + "copyright/" for x in LANGS}, PATHS[l] + "copyright/", None))
write(ANANSI_PATH + "index.html", anansi_page("zh")); urls.append((ANANSI_ALTS, ANANSI_PATH, None))
write(ANANSI_FR_PATH + "index.html", anansi_page_fr()); urls.append((ANANSI_ALTS, ANANSI_FR_PATH, None))
write(ANANSI_EN_PATH + "index.html", anansi_page_en()); urls.append((ANANSI_ALTS, ANANSI_EN_PATH, None))
for slug, vs in NOTES.items():
    for l in vs:
        write(note_path(l, slug) + "index.html", note_page(slug, l))
        urls.append(({x: note_path(x, slug) for x in vs}, note_path(l, slug), vs[l]["date"]))

_vars = ":root{" + "".join(f"--mt-{k}:url('data:image/svg+xml,{quote(PAT[k + '_light']['svg'])}');" for k in ("modern", "akan", "kita", "dida", "korhogo")) + "}\n"
write("assets/site.css", _vars + open(os.path.join(HERE, "site.css"), encoding="utf-8").read())
write("assets/site.js", open(os.path.join(HERE, "site.js"), encoding="utf-8").read())

sm = []
for alts, u, d in urls:
    al = "".join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[x]}" href="{DOMAIN}{v}"/>' for x, v in alts.items())
    sm.append(f"  <url><loc>{DOMAIN}{u}</loc>{f'<lastmod>{d}</lastmod>' if d else ''}{al}</url>")
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(sm) + "\n</urlset>\n")

items = []
for slug, vs in NOTES.items():
    for l, n in vs.items():
        items.append(f"<item><title>{e(n['title'])}</title><link>{DOMAIN}{note_path(l, slug)}</link><guid>{DOMAIN}{note_path(l, slug)}</guid><pubDate>{n['date']}</pubDate><description>{e(n['description'])}</description></item>")
write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Victor Tseng 曾浩瑜 · Field notes</title><link>{DOMAIN}/</link><description>Africa × Asia, cross-cultural notes</description>{"".join(items)}</channel></rss>\n')
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
write("CNAME", "victseng.com\n")
write("404.html", f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>404 · Victor Tseng</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400&family=Jost:wght@400&display=swap"><link rel="stylesheet" href="/assets/site.css?v={VER}"></head>
<body><main class="nf"><p class="cap">Victor Tseng</p><p class="nf-n">404</p><p>找不到這個頁面 · Page not found · Page introuvable</p><p class="ctas"><a class="btn" href="/">中文</a><a class="tl" href="/en/">English</a><a class="tl" href="/fr/">Français</a></p></main></body></html>
""")
print("built", OUT, "notes:", {k: list(v) for k, v in NOTES.items()})
