"""Portada 1080x1920 + 1080x1440 (feed 3:4). Uso: python3 portada.py portada.json salida_sin_ext
portada.json: {"color":"#2F6B4F","t1":"¿ES DEDUCIBLE","t2":"O NO?","sub":"EL SAT TE **DEBE** DINERO",
               "clip":"hook","sec":2.5,"pos":"50% 30%","marks":true}"""
import sys, json, os, re, subprocess, html
from playwright.sync_api import sync_playwright
K = os.path.dirname(os.path.abspath(__file__)); c = json.load(open(sys.argv[1])); out = os.path.abspath(sys.argv[2])
tmp = out + '_portada'; os.makedirs(tmp, exist_ok=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(c.get('sec', 2)), '-i', os.path.join(K, 'clips', c['clip'] + '.mp4'), '-frames:v', '1', os.path.join(tmp, 'f.png')], check=True)
sub = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(c.get('sub', '')))
marks = '''<div class="ok"><svg width="90" height="90" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="no"><svg width="80" height="80" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/></svg></div>''' if c.get('marks') else ''
fs = min(112, int(900 / (max(len(c['t1']), len(c.get('t2', ''))) * 0.62)))
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:#F7F2EA;font-family:Inter,Arial,sans-serif;position:relative;overflow:hidden}}
.band{{position:absolute;left:0;top:0;width:100%;height:520px;background:{c.get('color', '#1B2440')}}}
.serie{{position:absolute;top:150px;width:100%;text-align:center;color:#F7F2EA;font-weight:800;font-size:34px;letter-spacing:6px}}
.gold{{position:absolute;top:212px;left:50%;width:90px;height:5px;margin-left:-45px;background:#C9A45C;border-radius:3px}}
.t{{position:absolute;width:100%;text-align:center;font-weight:900;font-size:{fs}px;letter-spacing:-2px;line-height:1}}
.circ{{position:absolute;top:620px;left:50%;width:820px;height:820px;margin-left:-410px;border-radius:50%;background:#fff;overflow:hidden;border:10px solid #fff;box-shadow:0 20px 50px rgba(27,36,64,.15)}}
.circ img{{width:100%;height:100%;object-fit:cover;object-position:{c.get('pos', '50% 30%')}}}
.sub{{position:absolute;top:1470px;width:100%;text-align:center;color:#1B2440;font-weight:900;font-size:{min(76, int(950 / (len(c.get('sub', 'x')) * 0.6)))}px;letter-spacing:-1px}}
.sub b{{color:#801828}}
.logo{{position:absolute;bottom:110px;left:50%;width:170px;margin-left:-85px}}
.ok,.no{{position:absolute;width:150px;height:150px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(0,0,0,.18)}}
.ok{{background:#25AA5A;left:110px;top:1290px}}.no{{background:#CD2D37;right:110px;top:1290px}}
</style></head><body>
<div class="band"></div><div class="serie">FRAPÉ · SERIES</div><div class="gold"></div>
<div class="t" style="top:250px;color:#fff">{html.escape(c['t1'])}</div><div class="t" style="top:368px;color:#FFD23C">{html.escape(c.get('t2', ''))}</div>
<div class="circ"><img src="f.png"></div>{marks}
<div class="sub">{sub}</div><img class="logo" src="file://{K}/portada/logo_color.png">
</body></html>'''
open(os.path.join(tmp, 'p.html'), 'w').write(page)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + os.path.join(tmp, 'p.html')); pg.wait_for_timeout(400)
    pg.screenshot(path=out + '.png'); pg.screenshot(path=out + '_feed.png', clip={'x': 0, 'y': 240, 'width': 1080, 'height': 1440}); b.close()
print('portada ok', out + '.png')
