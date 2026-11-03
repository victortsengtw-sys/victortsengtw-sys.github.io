p = 'build.py'
s = open(p).read()


def R(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b)


R('PRESS = json.load(', 'MAP = json.load(open(os.path.join(HERE, "data", "map.json")))\nPRESS = json.load(')

MAPFN = r'''def map_svg(lang, c):
    w, h = MAP["w"], MAP["h"]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r=".3"/>' for x, y in MAP["dots"])
    keys = ["paris", "dakar", "taipei", "abidjan"]
    P = {k: MAP["cities"][k] for k in keys}

    def arc(a, b, lift):
        (x1, y1), (x2, y2) = P[a], P[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - lift
        return f'<path class="arc" pathLength="1" d="M{x1} {y1} Q{mx:.2f} {my:.2f} {x2} {y2}"/>'
    arcs = arc("paris", "dakar", 5) + arc("dakar", "taipei", 16) + arc("taipei", "abidjan", 12)
    off = {"paris": (1.4, -1.1, "start"), "dakar": (-1.4, 0.4, "end"), "taipei": (0, -1.8, "middle"), "abidjan": (1.5, 2.4, "start")}
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


def banner(lang, c):'''
R('def banner(lang, c):', MAPFN)
R('        <ol class="rt rv" aria-label="route">{route}</ol>', '        {map_svg(lang, c)}')
R('''      <ul class="doms">{doms}</ul>
    </div>
  </section>''', '''      <ul class="doms">{doms}</ul>
      <a class="cue" href="#expertise"><span>{e(c['scroll'])}</span><i aria-hidden="true"></i></a>
    </div>
  </section>''')
R('<div class="sr" role="dialog"', '''<a class="totop" href="#main" aria-label="{e(c['top'])}" title="{e(c['top'])}"><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path d="M12 19V5M6 11l6-6 6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></a>
<div class="sr" role="dialog"''')
R('''data-ok="{e(c['nl_ok'])}" data-err="{e(c['nl_err'])}"''', '''data-ok="{e(c['nl_ok'])}" data-err="{e(c['nl_err'])}" data-sending="{e(c['nl_sending'])}"''')
open(p, 'w').write(s)

p = 'site.js'
s = open(p).read()
a = s[s.index("      btn.disabled = true; msg.textContent = '…';"):s.index("        .then(function () { btn.disabled = false; });")]
b = """      btn.disabled = true; msg.textContent = f.getAttribute('data-sending') || '…';
      fetch(f.getAttribute('data-ajax'), { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return { success: r.ok }; }); })
        .then(function (j) {
          var ok = j && String(j.success) === 'true';
          if (ok) { msg.textContent = f.getAttribute('data-ok'); f.reset(); ev('newsletter_signup'); }
          else { msg.textContent = (j && j.message) ? j.message : f.getAttribute('data-err'); }
        })
        .catch(function () { HTMLFormElement.prototype.submit.call(f); })
"""
s = s.replace(a, b)
s = s.replace("  [].forEach.call(d.querySelectorAll('.nl-f'), function (f) { f.addEventListener('submit', function () { ev('newsletter_signup'); }); });\n", "")
s = s.replace("  /* GA4 events: consultation clicks, outbound works, LinkedIn, article reads */\n  function ev(name, params) { if (typeof w.gtag === 'function') w.gtag('event', name, params || {}); }\n", "  /* GA4 events */\n")
s = s.replace("  var reduce = w.matchMedia", "  function ev(name, params) { if (typeof w.gtag === 'function') w.gtag('event', name, params || {}); }\n  var reduce = w.matchMedia", 1)
s = s.replace("    if (bar) bar.style.transform", "    if (tt) tt.classList.toggle('on', h.scrollTop > 700);\n    if (bar) bar.style.transform")
s = s.replace("var bar = d.querySelector('.prog i'),", "var tt = d.querySelector('.totop'), bar = d.querySelector('.prog i'),")
open(p, 'w').write(s)
print("ok")
