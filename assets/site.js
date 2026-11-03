(function () {
  var d = document, w = window;
  function ev(name, params) { if (typeof w.gtag === 'function') w.gtag('event', name, params || {}); }
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* hero entrance */
  requestAnimationFrame(function () { setTimeout(function () { var h = d.querySelector('.hero'); if (h) h.classList.add('ld'); }, 60); });

  /* Abidjan clock (GMT+0) */
  var clks = d.querySelectorAll('[data-clock]');
  function tick() { var n = new Date(), t = ('0' + n.getUTCHours()).slice(-2) + ':' + ('0' + n.getUTCMinutes()).slice(-2) + ' GMT'; [].forEach.call(clks, function (c) { c.textContent = t; }); }
  tick(); setInterval(tick, 20000);

  /* scroll progress + gentle arch parallax */
  var cue = d.querySelector('.cue'), tt = d.querySelector('.totop'), bar = d.querySelector('.prog i'), arch = d.querySelector('.arch img'), ticking = false;
  function onScroll() {
    var h = d.documentElement, max = h.scrollHeight - h.clientHeight;
    if (tt) {
      var nearEnd = h.scrollTop + h.clientHeight > h.scrollHeight - 320;
      tt.classList.add('on');
      if (tt._up !== nearEnd) { tt._up = nearEnd; tt.classList.toggle('up', nearEnd); var lab = tt.getAttribute(nearEnd ? 'data-up' : 'data-down'); tt.setAttribute('aria-label', lab); tt.querySelector('.fab-t').textContent = lab; }
    }
    if (cue) cue.classList.toggle('off', h.scrollTop > 160);
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? h.scrollTop / max : 0) + ')';
    if (arch && !reduce) { var y = Math.min(h.scrollTop, 700); arch.style.transform = 'translateY(' + (y * 0.06) + 'px) scale(' + (1 + y * 0.00012) + ')'; }
    ticking = false;
  }
  w.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* floating button: keep reading (down) / back to top (up) */
  if (tt) tt.addEventListener('click', function () {
    var h = d.documentElement;
    if (tt.classList.contains('up')) { w.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); return; }
    var offs = (d.querySelector('.hd') || {}).offsetHeight || 0, y = h.scrollTop + offs + 24, target = null;
    var marks = d.querySelectorAll('main section, .prose h2, .art-cta, .rel, footer');
    for (var i = 0; i < marks.length; i++) { var t = marks[i].getBoundingClientRect().top + h.scrollTop; if (t > y + 40) { target = t - offs - 12; break; } }
    if (target === null || target - h.scrollTop > h.clientHeight * 1.6) target = h.scrollTop + h.clientHeight * 0.8;
    w.scrollTo({ top: target, behavior: reduce ? 'auto' : 'smooth' });
  });

  /* count-up numbers */
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10), v0 = el.querySelector('.v');
    if (!target || reduce || el._done || !v0) return; el._done = true;
    var t0 = null, dur = 2600;
    function fmt(v) { return v >= 1000 ? v.toLocaleString('en-US') : String(v); }
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      v0.textContent = fmt(Math.round(target * (1 - Math.pow(1 - p, 4))));
      if (p < 1) requestAnimationFrame(step);
    }
    v0.textContent = '0'; requestAnimationFrame(step);
  }

  /* newsletter → Google Sheet (Apps Script web app) */
  [].forEach.call(d.querySelectorAll('.nl-f'), function (f) {
    f.addEventListener('submit', function (ev0) {
      ev0.preventDefault();
      var msg = f.querySelector('.nl-msg'), btn = f.querySelector('button[type=submit]'), ep = f.getAttribute('data-ep');
      if (f.elements._honey && f.elements._honey.value) return;
      if (!ep) { msg.textContent = f.getAttribute('data-err'); return; }
      var body = new URLSearchParams();
      [].forEach.call(f.elements, function (x) { if (!x.name || (x.type === 'checkbox' && !x.checked)) return; body.append(x.name, x.value); });
      body.append('page', location.href);
      btn.disabled = true; msg.textContent = f.getAttribute('data-sending') || '…';
      var done = false, timer = setTimeout(function () { if (!done) { done = true; btn.disabled = false; msg.textContent = f.getAttribute('data-err'); } }, 20000);
      fetch(ep, { method: 'POST', mode: 'no-cors', body: body })
        .then(function () { if (done) return; done = true; clearTimeout(timer); msg.textContent = f.getAttribute('data-ok'); f.reset(); ev('newsletter_signup'); })
        .catch(function () { if (done) return; done = true; clearTimeout(timer); msg.textContent = f.getAttribute('data-err'); })
        .then(function () { btn.disabled = false; });
    });
  });

  /* GA4 events */
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a'); if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^mailto:/.test(href)) ev('contact_email', { link_text: (a.textContent || '').trim().slice(0, 60), page_location: location.href });
    else if (/linkedin\.com/.test(href)) ev('contact_linkedin');
    else if (/\/akwaba-maison\//.test(href)) ev('open_work', { work: 'akwaba_maison' });
    else if (/\/akwaba\//.test(href)) ev('open_work', { work: 'akwaba_game' });
    else if (/thenewslens\.com/.test(href)) ev('open_press', { url: href });
  });
  if (d.querySelector('.art') && 'IntersectionObserver' in w) {
    var endEl = d.querySelector('.art-tags');
    if (endEl) { var ro = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { ev('article_read', { article: location.pathname }); ro.disconnect(); } }); ro.observe(endEl); }
  }

  /* column filters */
  var flt = d.querySelector('.flt'), list = d.querySelector('[data-list]');
  if (flt && list) flt.addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    [].forEach.call(flt.children, function (x) { x.classList.toggle('on', x === b); });
    var f = b.getAttribute('data-f');
    [].forEach.call(list.children, function (li) { li.hidden = !!f && li.getAttribute('data-p') !== f; if (!li.hidden) li.classList.add('in'); });
  });

  var links = [].slice.call(d.querySelectorAll('.an a[data-sec]'));
  var navIn = d.querySelector('.an-in');
  var isHome = d.body.classList.contains('is-home');

  if ('IntersectionObserver' in w) {
    /* reveal with stagger */
    var rv = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, sib = el.parentNode ? [].indexOf.call(el.parentNode.children, el) : 0;
        el.style.transitionDelay = Math.min(sib, 5) * 70 + 'ms';
        el.classList.add('in'); rv.unobserve(el);
        [].forEach.call(el.querySelectorAll('[data-count]'), countUp);
      });
    }, { rootMargin: '0px 0px -6% 0px' });
    [].forEach.call(d.querySelectorAll('.rv'), function (el) { rv.observe(el); });

    /* active section in the anchor bar */
    if (isHome && links.length) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          links.forEach(function (a) {
            var on = a.getAttribute('data-sec') === en.target.id;
            a.classList.toggle('on', on);
            if (on && navIn && navIn.scrollWidth > navIn.clientWidth) navIn.scrollTo({ left: a.offsetLeft - 20, behavior: 'smooth' });
          });
        });
      }, { rootMargin: '-40% 0px -55% 0px' });
      links.forEach(function (a) { var s = d.getElementById(a.getAttribute('data-sec')); if (s) io.observe(s); });
    }
  } else {
    [].forEach.call(d.querySelectorAll('.rv'), function (el) { el.classList.add('in'); });
  }

  /* search */
  var box = d.querySelector('.sr'), inp = box && box.querySelector('input'), res = box && box.querySelector('.sr-res');
  var idx = [];
  try { idx = JSON.parse(d.getElementById('sidx').textContent); } catch (e) {}
  var norm = function (s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  idx.forEach(function (it) { it.n = norm(it.t + ' ' + it.s + ' ' + it.d); it.nt = norm(it.t); });
  var last = null;
  function render(q) {
    q = norm(q.trim()); res.innerHTML = '';
    if (!q) return;
    var terms = q.split(/\s+/);
    var hits = idx.filter(function (it) { return terms.every(function (t) { return it.n.indexOf(t) > -1; }); })
      .sort(function (a, b) { return (b.nt.indexOf(terms[0]) > -1) - (a.nt.indexOf(terms[0]) > -1); }).slice(0, 12);
    if (!hits.length) { res.innerHTML = '<li class="sr-none">' + ((w.UI && w.UI.none) || '—') + '</li>'; return; }
    hits.forEach(function (it) {
      var li = d.createElement('li'), a = d.createElement('a');
      a.href = it.h; if (/^https?:/.test(it.h)) { a.target = '_blank'; a.rel = 'noopener'; }
      var s = d.createElement('span'); s.className = 's'; s.textContent = it.s;
      var t = d.createElement('span'); t.className = 'sr-t'; t.textContent = it.t;
      a.appendChild(s); a.appendChild(t); a.addEventListener('click', close);
      li.appendChild(a); res.appendChild(li);
    });
  }
  function open() { if (!box) return; last = d.activeElement; box.hidden = false; d.body.classList.add('noscroll'); setTimeout(function () { inp.focus(); }, 20); }
  function close() { if (!box || box.hidden) return; box.hidden = true; d.body.classList.remove('noscroll'); if (last && last.focus) last.focus(); }
  [].forEach.call(d.querySelectorAll('[data-open-search]'), function (b) { b.addEventListener('click', open); });
  if (box) {
    box.querySelector('[data-close-search]').addEventListener('click', close);
    box.addEventListener('click', function (ev) { if (ev.target === box) close(); });
    inp.addEventListener('input', function () { render(inp.value); });
    inp.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { var f = res.querySelector('a'); if (f) f.click(); }
      if (ev.key === 'ArrowDown') { var g = res.querySelector('a'); if (g) { ev.preventDefault(); g.focus(); } }
    });
    res.addEventListener('keydown', function (ev) {
      var a = d.activeElement; if (!a || a.tagName !== 'A') return; var li = a.parentNode;
      if (ev.key === 'ArrowDown' && li.nextElementSibling) { ev.preventDefault(); li.nextElementSibling.firstChild.focus(); }
      if (ev.key === 'ArrowUp') { ev.preventDefault(); (li.previousElementSibling ? li.previousElementSibling.firstChild : inp).focus(); }
    });
  }
  d.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') close();
    var tag = (d.activeElement && d.activeElement.tagName) || '';
    if ((ev.key === '/' || ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 'k')) && !/INPUT|TEXTAREA/.test(tag)) { ev.preventDefault(); open(); }
  });
})();
