"""Motor de reels FRAPS. Uso: SPEC=spec.py WORDS=words.json AUD=seg OUT=proj [MODE=hibrido] python3 gen_reel.py"""
import json, re, os, html
D = os.path.abspath(os.environ.get('OUT', 'proj'))
WORDS = os.environ['WORDS']
W, H = 1080, 1920
AUD = float(os.environ['AUD'])
TOTAL = round(AUD + 0.2, 2)
NAVY, WINE, YEL, CREAM, GREEN, RED, GOLD = '#1B2440', '#801828', '#FFD23C', '#F7F2EA', '#25AA5A', '#CD2D37', '#B08D57'
NL = chr(10)
class _CL(dict):
    def __missing__(self, k): return 5.0
CLIPLEN = _CL()

fix = {'dedusible': 'deducible', 'Frappé': 'FRAPÉ', 'Enfrapé': 'EN FRAPÉ', 'sal': 'SAT'}
words = []
for x in json.load(open(WORDS)):
    t = x['w'].strip(); core = t.strip('.,?¿')
    if core in fix: t = t.replace(core, fix[core])
    words.append(dict(w=t, s=x['s'], e=x['e']))
def norm(t): return re.sub(r'[¿?¡!.,:;…]', '', t).lower()
def at(word, nth=1, back=0):
    k = 0
    for i, w in enumerate(words):
        if norm(w['w']) == word:
            k += 1
            if k == nth: return round(words[i - back]['s'], 2)
    raise SystemExit('anchor missing: ' + word)

G, RD = GREEN, RED
CALC, CTA, labels, key, extra, CHIPS, LABELS_END = {}, {}, [], [], [], None, 0
exec(open(os.environ['SPEC']).read())
S = [(round(max(0, s[0]), 2),) + s[1:] for s in S]
TR = 0.32
ENT = {
    'punch': 'tl.fromTo("#{i}-in", {{scale: 1.14}}, {{scale: 1, duration: 0.4, ease: "expo.out"}}, 0);',
    'whip': 'tl.fromTo("#{i}-in", {{xPercent: 100, filter: "blur(16px)"}}, {{xPercent: 0, filter: "blur(0px)", duration: 0.38, ease: "expo.out"}}, 0);',
    'blur': 'tl.fromTo("#{i}-in", {{opacity: 0, filter: "blur(14px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power2.out"}}, 0);',
    'zoom': 'tl.fromTo("#{i}-in", {{scale: 1.25, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.42, ease: "expo.out"}}, 0);',
}
CHECK = '<svg viewBox="0 0 40 40" class="mk"><path class="mkp" d="M11 21 L17.5 27.5 L29.5 13.5" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
CROSS = '<svg viewBox="0 0 40 40" class="mk"><path class="mkp" d="M13 13 L27 27 M27 13 L13 27" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" pathLength="1"/></svg>'
CHAT = f'<svg viewBox="0 0 200 200" width="230" height="230"><path d="M30 50 C30 38 40 30 52 30 L148 30 C160 30 170 38 170 50 L170 115 C170 127 160 135 148 135 L80 135 L48 165 L52 135 C40 135 30 127 30 115 Z" fill="{GREEN}" stroke="#fff" stroke-width="8"/><path stroke="#fff" stroke-width="10" stroke-linecap="round" d="M70 82 L72 82 M100 82 L102 82 M130 82 L132 82"/></svg>'

def scene_html(i, dur):
    st, kind, src, ms, ent = S[i]
    sid = f's{i}'
    e = ENT[ent].format(i=sid)
    if kind == 'v':
        rate = min(1.0, (CLIPLEN[src] - ms - 0.05) / dur) if dur > CLIPLEN[src] - ms else 1.0
        rate = max(0.6, round(rate, 2))
        inner = (f'<div id="{sid}-cam" style="position:absolute;inset:0;transform-origin:50% 45%">'
                 f'<video id="{sid}-m" class="clip" src="assets/{src}.mp4" muted playsinline data-start="0" data-duration="{dur:.2f}" '
                 f'data-media-start="{ms}" data-playback-rate="{rate}" data-track-index="0" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover"></video></div>')
        js = f'tl.fromTo("#{sid}-cam", {{scale: 1.0}}, {{scale: 1.0, duration: {dur:.2f}, ease: "none"}}, 0);'
        bg = '#000'
    elif src == 'title':
        bg = YEL
        t1, t2, tv = at('todo') - st, at('es', 2) - st, at('vamos') - st
        inner = f'''<div class="big" id="{sid}-a" style="top:470px;font-size:84px;color:{WINE}">PERO OJO:</div>
<div class="big" id="{sid}-b" style="top:570px;font-size:84px;color:{WINE}">NO TODO CUENTA</div>
<div class="big" id="{sid}-c" style="top:760px;font-size:132px;color:{NAVY}">¿ES DEDUCIBLE</div>
<div class="big" id="{sid}-d" style="top:900px;font-size:132px;color:{NAVY}">O NO?</div>
<div id="{sid}-ok" class="stamp" style="left:250px;top:1110px;background:{GREEN}">{CHECK}</div>
<div id="{sid}-no" class="stamp" style="left:580px;top:1110px;background:{RED}">{CROSS}</div>'''
        js = NL.join([
            f'tl.fromTo("#{sid}-a", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.45, ease: "expo.out"}}, 0.1);',
            f'tl.fromTo("#{sid}-b", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.45, ease: "expo.out"}}, {max(0.3, t1 - 0.05):.2f});',
            f'tl.fromTo("#{sid}-c", {{opacity: 0, scale: 0.85, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out"}}, {t2 - 0.05:.2f});',
            f'tl.fromTo("#{sid}-d", {{opacity: 0, scale: 0.85, filter: "blur(10px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out"}}, {t2 + 0.5:.2f});',
            f'tl.fromTo("#{sid}-ok", {{scale: 0, rotation: -90}}, {{scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2)"}}, {tv - 0.1:.2f});',
            f'tl.fromTo("#{sid}-ok .mkp", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.4}}, {tv + 0.3:.2f});',
            f'tl.fromTo("#{sid}-no", {{scale: 0, rotation: -90}}, {{scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2)"}}, {tv + 0.15:.2f});',
            f'tl.fromTo("#{sid}-no .mkp", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.4}}, {tv + 0.55:.2f});'])
    elif src == 'calc':
        bg = CREAM
        ta, tb = CALC['a_at'] - st, CALC['b_at'] - st
        av, bv = CALC['a_value'], CALC['b_value']
        inner = f'''<div class="big" id="{sid}-t" style="top:330px"><span style="display:inline-block;background:{NAVY};color:#fff;font-size:44px;padding:8px 30px;border-radius:40px;letter-spacing:4px">{html.escape(CALC.get('tag','EJEMPLO'))}</span></div>
<div class="big" id="{sid}-a" style="top:470px;font-size:72px;color:{NAVY}">{html.escape(CALC['a_top'])}</div>
<div class="big" id="{sid}-n1" style="top:555px;font-size:170px;color:{WINE}">$0</div>
<div class="big" id="{sid}-b" style="top:750px;font-size:54px;color:#6b6f7b;font-weight:800">{html.escape(CALC['a_bottom'])}</div>
<div id="{sid}-ar" style="position:absolute;left:490px;top:850px;width:100px;height:110px"><svg viewBox="0 0 100 110" width="100" height="110"><path d="M50 8 L50 88 M18 60 L50 94 L82 60" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="big" id="{sid}-c" style="top:990px;font-size:62px;color:{NAVY}">{html.escape(CALC['b_top'])}</div>
<div class="big" id="{sid}-n2" style="top:1065px;font-size:200px;color:{GREEN}">$0</div>
<div class="big" id="{sid}-f" style="top:1300px;font-size:32px;color:#8a8d96;font-weight:600;letter-spacing:0">{html.escape(CALC.get('foot','*Ejemplo ilustrativo.'))}</div>'''
        js = NL.join([
            f'tl.fromTo("#{sid}-t", {{opacity: 0, y: -16}}, {{opacity: 1, y: 0, duration: 0.4, ease: "expo.out"}}, 0.05);',
            f'tl.fromTo("#{sid}-a", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.45, ease: "expo.out"}}, 0.25);',
            f'tl.fromTo("#{sid}-n1", {{opacity: 0, scale: 0.8}}, {{opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)"}}, {max(0.3, ta - 0.3):.2f});',
            f'const c1 = {{v: 0}}; tl.fromTo(c1, {{v: 0}}, {{v: {av}, duration: 0.9, ease: "power2.out", onUpdate: () => {{ document.querySelector("#{sid}-n1").textContent = "$" + Math.round(c1.v).toLocaleString("en-US"); }}}}, {max(0.3, ta - 0.3):.2f});',
            f'tl.fromTo("#{sid}-b", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {ta + 0.6:.2f});',
            f'tl.fromTo("#{sid}-ar", {{opacity: 0, y: -30}}, {{opacity: 1, y: 0, duration: 0.5, ease: "bounce.out"}}, {tb - 1.2:.2f});',
            f'tl.fromTo("#{sid}-c", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.45, ease: "expo.out"}}, {tb - 1.0:.2f});',
            f'tl.fromTo("#{sid}-n2", {{opacity: 0, scale: 0.6}}, {{opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.2)"}}, {tb - 0.35:.2f});',
            f'const c2 = {{v: 0}}; tl.fromTo(c2, {{v: 0}}, {{v: {bv}, duration: 0.9, ease: "power2.out", onUpdate: () => {{ document.querySelector("#{sid}-n2").textContent = "$" + Math.round(c2.v).toLocaleString("en-US"); }}}}, {tb - 0.35:.2f});',
            f'tl.fromTo("#{sid}-f", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {tb + 0.6:.2f});'])
    else:  # cta
        bg = '#FFFFFF'
        t1, t2, t3 = CTA['t1'] - st, CTA['t2'] - st, CTA['t3'] - st
        inner = f'''<div id="{sid}-lg" style="position:absolute;left:0;width:100%;top:260px;text-align:center"><img src="assets/logo.png" style="width:330px"></div>
<div class="big" id="{sid}-a" style="top:680px;font-size:80px;color:{NAVY}">{html.escape(CTA["l1"])}</div>
<div class="big" id="{sid}-b" style="top:775px;font-size:100px;color:{WINE}">{html.escape(CTA["l2"])}</div>
<div class="big" id="{sid}-c" style="top:960px;"><span style="display:inline-block;background:{YEL};color:{NAVY};font-size:96px;padding:10px 40px;border-radius:24px;box-shadow:0 10px 24px rgba(27,36,64,.18)">{html.escape(CTA["pill"])}</span></div>
<div class="big" id="{sid}-d" style="top:1170px;font-size:56px;color:#6b6f7b;font-weight:800;font-style:italic">{html.escape(CTA["tail"])}</div>'''
        js = NL.join([
            f'tl.fromTo("#{sid}-lg", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: 0.5, ease: "expo.out"}}, 0.05);',
            f'tl.fromTo("#{sid}-a", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.45, ease: "expo.out"}}, 0.2);',
            f'tl.fromTo("#{sid}-b", {{opacity: 0, scale: 0.85}}, {{opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)"}}, {max(0.4, t1 - 0.1):.2f});',
            f'tl.fromTo("#{sid}-c", {{opacity: 0, scale: 0.6}}, {{opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.2)"}}, {t2 - 0.1:.2f});',
            f'tl.fromTo("#{sid}-d", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: 0.4}}, {t3 - 0.05:.2f});'])
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    #{sid}-bg {{ position: absolute; inset: 0; background: {bg}; }}
    #{sid}-in {{ position: absolute; inset: 0; overflow: hidden; }}
    .big {{ position: absolute; left: 0; width: 100%; text-align: center; font-family: "Inter"; font-weight: 900; letter-spacing: -1.5px; white-space: nowrap; }}
    .stamp {{ position: absolute; width: 250px; height: 250px; border-radius: 50%; box-shadow: 0 14px 30px rgba(0,0,0,.2); }}
    .mk {{ width: 100%; height: 100%; }} .mkp {{ stroke-dasharray: 1; stroke-dashoffset: 1; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overflow data-layout-allow-overlap>
    <div id="{sid}-bg"></div>
    <div id="{sid}-in">{inner}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {e}
    {js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
'''

om, oj = [], []
oj.append(f'tl.to("#lg", {{opacity: 0, duration: 0.25}}, {LOGO_HIDE:.2f});')
MODE = os.environ.get('MODE', 'hibrido')
stmts = key + (extra if MODE == 'claves' else [])
stmts.sort(key=lambda x: x[0])
for k, (a, b, lines, pos) in enumerate(stmts):
    y = {'mid': 640, 'top': 400}.get(pos, 0)
    if pos == 'low': y = 1560 - sum(min(sz, int(740 / (len(tx) * 0.64))) * 1.08 for tx, _, _, sz in lines)
    blk = [f'<div id="st{k}" class="clip" data-start="{a:.2f}" data-duration="{b - a:.2f}" style="position:absolute;inset:0">',
           f'<div class="scrim {dict(mid="scm", top="sct", low="scb")[pos]}"></div>']
    for li, (txt, t, col, sz) in enumerate(lines):
        if pos != 'mid': sz = min(sz, int(740 / (len(txt) * 0.64)))
        blk.append(f'<div id="st{k}l{li}" class="bigo" style="top:{y:.0f}px;font-size:{sz}px;color:{col}">{html.escape(txt)}</div>')
        oj.append(f'tl.fromTo("#st{k}l{li}", {{opacity: 0, y: 26, filter: "blur(10px)"}}, {{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out"}}, {max(a + 0.05, t - 0.05):.2f});')
        y += sz * 1.08
    blk.append('</div>')
    om.append(''.join(blk))
chips = []
for k, (a, text, kind, ts) in enumerate(labels):
    nxt = labels[k + 1][0] if k + 1 < len(labels) else LABELS_END
    col = GREEN if kind == 'ok' else RED
    om.append(f'<div id="lb{k}" class="clip lrow" data-start="{a:.2f}" data-duration="{nxt - a - 0.05:.2f}"><div id="lb{k}p" class="pill"><div id="lb{k}c" class="bc" style="background:{col}">{CHECK if kind == "ok" else CROSS}</div><span>{html.escape(text)}</span></div></div>')
    oj.append(f'tl.fromTo("#lb{k}p", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {a + 0.1:.2f});')
    oj.append(f'tl.fromTo("#lb{k}c", {{scale: 0.4, opacity: 0.25}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.4)"}}, {ts - 0.15:.2f});')
    oj.append(f'tl.fromTo("#lb{k}c .mkp", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.35}}, {ts + 0.1:.2f});')
    chips.append((ts + 0.35, kind, text.split(' ')[0]))
cs, ce = CHIPS if CHIPS else (0, 0)
if CHIPS: om.append(f'<div id="chips" class="clip" data-start="{cs:.2f}" data-duration="{ce - cs:.2f}" style="position:absolute;inset:0">' +
          ''.join(f'<div id="ch{k}" class="chip" style="left:{60 + k * 136}px;background:{GREEN if kd == "ok" else RED}">{CHECK if kd == "ok" else CROSS}</div>' for k, (t, kd, _) in enumerate(chips)) + '</div>')
for k, (t, kd, _) in enumerate(chips):
    oj.append(f'tl.fromTo("#ch{k}", {{scale: 0, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.4)"}}, {t:.2f});')
    oj.append(f'tl.set("#ch{k} .mkp", {{strokeDashoffset: 0}}, {t:.2f});')
over = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .scrim {{ position: absolute; left: 0; width: 100%; }}
    .scm {{ top: 0; height: 100%; background: rgba(10,14,30,.45); }}
    .scb {{ bottom: 0; height: 1000px; background: linear-gradient(0deg, rgba(10,14,30,.8) 0%, rgba(10,14,30,.55) 55%, rgba(10,14,30,0) 100%); }}
    .sct {{ top: 0; height: 900px; background: linear-gradient(180deg, rgba(10,14,30,.75) 0%, rgba(10,14,30,.55) 60%, rgba(10,14,30,0) 100%); }}
    #tg {{ position: absolute; left: 0; top: 0; width: 100%; height: 640px; background: linear-gradient(180deg, rgba(10,14,30,.6) 0%, rgba(10,14,30,0) 100%); }}
    .bigo {{ position: absolute; left: 0; width: 100%; text-align: center; font-family: "Inter"; font-weight: 900; letter-spacing: -1.5px; white-space: nowrap; text-shadow: 0 4px 18px rgba(0,0,0,.4); }}
    .lrow {{ position: absolute; left: 60px; top: 300px; }}
    .pill {{ display: inline-flex; align-items: center; gap: 16px; padding: 12px 30px 12px 12px; border-radius: 999px; background: #fff;
             font-family: "Inter"; font-weight: 900; font-size: 46px; color: {NAVY}; white-space: nowrap; box-shadow: 0 8px 22px rgba(0,0,0,.2); }}
    .bc {{ width: 70px; height: 70px; border-radius: 50%; flex: none; }}
    .chip {{ position: absolute; top: 410px; width: 64px; height: 64px; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,.25); }}
    .mk {{ width: 100%; height: 100%; }} .mkp {{ stroke-dasharray: 1; stroke-dashoffset: 1; }}
    #lg {{ position: absolute; right: 40px; top: 230px; }}
    #lg img {{ width: 150px; display: block; filter: drop-shadow(0 0 2px rgba(255,255,255,1)) drop-shadow(0 0 6px rgba(255,255,255,.95)) drop-shadow(0 0 16px rgba(255,255,255,.8)) drop-shadow(0 0 30px rgba(255,255,255,.5)); }}
  </style>
  <div id="root" data-composition-id="over" data-width="{W}" data-height="{H}" data-layout-allow-overflow data-layout-allow-overlap>
    {f'<div id="tg" class="clip" data-start="{cs:.2f}" data-duration="{ce - cs:.2f}"></div>' if CHIPS else ''}
{NL.join('    ' + m for m in om)}
    <div id="lg"><img src="assets/logo_color.png" alt="FRAPÉ"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{NL.join('    ' + j for j in oj)}
    window.__timelines["over"] = tl;
  </script>
</template>
'''
# ---------- captions
groups, cur = [], []
for w in words:
    cur.append(w)
    if len(cur) >= 3 or w['w'][-1] in '.?,': groups.append(cur); cur = []
if cur: groups.append(cur)
groups = [g for g in groups if g[0]['s'] < CAPS_END]
if MODE == 'claves': groups = []
else: groups = [g for g in groups if not any(a - 0.1 <= g[0]['s'] < b for a, b, _, _ in key)]
def clean(t): return html.escape(t.replace('¿', '').rstrip('.,').upper())
cm, cj = [], []
for gi, g in enumerate(groups):
    st = max(0.12, g[0]['s'] - 0.04)
    nxt = groups[gi + 1][0]['s'] - 0.04 if gi + 1 < len(groups) else AUD
    en = max(min(nxt, g[-1]['e'] + 0.35), st + 0.3)
    spans = ' '.join(f'<span id="c{gi}w{wi}">{clean(w["w"])}</span>' for wi, w in enumerate(g))
    cm.append(f'<div id="c{gi}" class="clip cg" data-start="{st:.2f}" data-duration="{en - st:.2f}"><div id="c{gi}i" class="cgi">{spans}</div></div>')
    cj.append(f'tl.fromTo("#c{gi}i", {{opacity: 0, y: 10}}, {{opacity: 1, y: 0, duration: 0.16}}, {st:.2f});')
    for wi, w in enumerate(g):
        cj.append(f'tl.to("#c{gi}w{wi}", {{color: "{YEL}", duration: 0.04}}, {max(st, w["s"] - 0.02):.2f});')
        if wi + 1 < len(g): cj.append(f'tl.to("#c{gi}w{wi}", {{color: "#ffffff", duration: 0.04}}, {g[wi + 1]["s"] - 0.02:.2f});')
    cj.append(f'tl.to("#c{gi}i", {{opacity: 0, duration: 0.08}}, {en - 0.08:.2f});')
caps = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cg {{ position: absolute; left: 0; width: 100%; top: 1420px; text-align: center; }}
    .cgi {{ display: inline-block; padding: 12px 28px 14px; border-radius: 22px; background: rgba(10,14,30,.7); font-family: "Inter"; font-weight: 900; font-size: 60px; color: #fff; }}
  </style>
  <div id="root" data-composition-id="caps" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
{NL.join('    ' + m for m in cm)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{NL.join('    ' + j for j in cj)}
    window.__timelines["caps"] = tl;
  </script>
</template>
'''
os.makedirs(os.path.join(D, 'compositions'), exist_ok=True)
for f in os.listdir(os.path.join(D, 'compositions')): os.remove(os.path.join(D, 'compositions', f))
hosts = []
for i, sc in enumerate(S):
    st = sc[0]
    dur = ((S[i + 1][0] + TR + 0.05) if i + 1 < len(S) else TOTAL) - st
    open(os.path.join(D, 'compositions', f's{i}.html'), 'w').write(scene_html(i, dur))
    hosts.append(f'<div id="s{i}" data-composition-id="s{i}" data-composition-src="compositions/s{i}.html" data-start="{st:.2f}" data-duration="{dur:.2f}" data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{i + 1}"></div>')
for n, b in [('over', over), ('caps', caps)]:
    open(os.path.join(D, 'compositions', f'{n}.html'), 'w').write(b)
hosts.append(f'<div id="over" data-composition-id="over" data-composition-src="compositions/over.html" data-start="0" data-duration="{TOTAL:.2f}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:50"></div>')
hosts.append(f'<div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{AUD:.2f}" data-track-index="4" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:60"></div>')
open(os.path.join(D, 'index.html'), 'w').write(f'''<!doctype html>
<html><head><meta charset="utf-8"><title>FRAPÉ · comercial</title><style>html,body{{margin:0;background:#000;}}</style></head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-fps="30">
{NL.join('    ' + h for h in hosts)}
  </div>
  <script src="assets/gsap.min.js"></script>
  <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
''')
json.dump({'starts': [s[0] for s in S], 'ok': [l[3] - 0.15 for l in labels if l[2] == 'ok'], 'no': [l[3] - 0.15 for l in labels if l[2] == 'no'],
           'money': MONEY, 'aud': AUD, 'total': TOTAL}, open(os.path.join(D, 'timing.json'), 'w'))
print('ok', TOTAL, [s[0] for s in S])
# ---------- assets: copia del kit solo lo que usa este reel
import shutil
KIT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(D, 'assets'), exist_ok=True)
for f in ('gsap.min.js', 'logo.png', 'logo_color.png'):
    shutil.copy(os.path.join(KIT, 'assets', f), os.path.join(D, 'assets', f))
for s in S:
    if s[1] == 'v':
        p = os.path.join(KIT, 'clips', s[2] + '.mp4')
        if not os.path.exists(p): raise SystemExit('clip missing: ' + s[2])
        shutil.copy(p, os.path.join(D, 'assets', s[2] + '.mp4'))
