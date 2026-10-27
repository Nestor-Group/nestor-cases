#!/usr/bin/env python3
"""Maakt uit index.html (de demo met schakelaar) drie afgeleide bestanden:

  nestor-cases-licht.html   volledige testpagina, alleen de lichte versie
  nestor-cases-embed.html   alleen het blok, om in een embed-/HTML-veld van je CMS te plakken
  test-host.html            testpagina die het embed-blok in een "vijandige" site plaatst

En uit diensten.html (het blok "Dit is wat Nestor voor jou kan betekenen"):

  dist/diensten.css, dist/diensten.js, dist/diensten-snippet.html (laadt van GitHub Pages)
  dist/diensten-embed.html  alles-in-één snippet zonder GitHub (aanbevolen voor dit blok)
  test-diensten.html        vijandige testpagina met schakelaar voor de containerbreedte

Uitvoeren:  python3 build.py
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE / "index.html").read_text(encoding="utf-8")

# ---- lichte versie: demo-schakelaar en oranje variant weg ----
light = re.sub(r"\n  \.demo-switch \{.*?\n  \.demo-switch button\.is-active \{[^\n]*\n", "\n", src, flags=re.S)
light = re.sub(r"<!-- Alleen voor deze demo-pagina: schakel tussen de lichte en de oranje versie -->.*?</script>\n\n", "", light, flags=re.S)
light = re.sub(r"  \.nc--oranje \{.*?\n  \}\n", "", light, flags=re.S)
light = light.replace('/* ---- Kleuren (Nestor-huisstijl, lichte versie). Voor de oranje versie: class "nc--oranje" op de section ---- */',
                      "/* ---- Kleuren (Nestor-huisstijl) ---- */")
light = light.replace("<title>Nestor cases</title>", "<title>Nestor cases (lichte versie)</title>")
assert "demo-switch" not in light and "nc--oranje" not in light
(HERE / "nestor-cases-licht.html").write_text(light, encoding="utf-8")

REPO = "Nestor-Group/nestor-cases"          # GitHub-repository
PAGES = "https://nestor-group.github.io/nestor-cases"   # GitHub Pages van de repository

# ---- embed: alleen het blok ----
start = light.index("<!-- BLOK START -->")
end = light.index("<!-- BLOK EINDE -->") + len("<!-- BLOK EINDE -->")
block = light[start:end]

# afbeeldingen en video's: src -> data-src, zodat het script ze laadt vanaf data-media
block = re.sub(r'<(img|video)([^>]*?)\ssrc="media/', r'<\1\2 data-src="media/', block)
assert 'src="media/' not in block.replace('data-src="media/', "")

# instelbare media-locatie op de section
block = block.replace('<section class="nc" id="nestor-cases">',
                      '<section class="nc" id="nestor-cases" data-media="media/">')
HUBSPOT_MEDIA = "https://7551812.fs1.hubspotusercontent-eu1.net/hubfs/7551812/Nestor/NE%20-%20Website/"   # HubSpot File Manager, map "NE - Website"
MEDIA_CDN = HUBSPOT_MEDIA   # standaard media-locatie in de snippet (alternatief: f"{PAGES}/media/")

intro = """<!--
  NESTOR CASES-BLOK (embed-versie)

  Plak dit volledige bestand in het HTML-/embed-veld van je CMS. Niets anders nodig:
  geen <html>, <head> of <body>, en geen extra stylesheet. De fonts (Baloo Paaji 2 en
  Source Sans Pro) staan al op nestor.be.

  MEDIA: zet de map "media" ergens op je site (of CDN) en vul de URL van die map in bij
  data-media op de <section> hieronder, met een slash op het einde. Bijvoorbeeld:
      data-media="https://nestor.be/uploads/cases/media/"
  Alle foto's, logo's en video's worden dan vanaf die locatie geladen.

  YOUTUBE: per videokaart zet je de YouTube-link in data-video (zie de VERVANG-opmerkingen).
-->
"""
embed = intro + block + "\n"
(HERE / "nestor-cases-embed.html").write_text(embed, encoding="utf-8")

# ---- testpagina met vijandige site-CSS en een smalle container ----
host = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Testpagina: embed in een vreemde site</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+Paaji+2:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  /* Opzettelijk lelijke site-CSS om te testen of het blok zich daartegen verdedigt */
  body {{ margin: 0; background: #223; color: #0f0; font-family: Georgia, serif; font-size: 22px; }}
  a {{ color: #ff0 !important; text-decoration: underline; font-size: 30px; }}
  a span {{ color: #0ff; }}
  button {{ background: lime; color: purple; border: 4px dotted red; font-size: 40px; padding: 30px; }}
  img {{ max-width: 40%; border: 5px solid magenta; }}
  h2 {{ font-size: 70px; text-transform: uppercase; margin: 80px; color: pink; }}
  p {{ margin: 40px; font-style: italic; }}
  .site-container {{ max-width: 760px; margin: 40px auto; background: #fff; padding: 20px; }}
</style>
</head>
<body>
<div class="site-container">
  <h2>Site-kop boven het blok</h2>
{embed}
  <p>Site-tekst onder het blok.</p>
</div>
</body>
</html>
"""
(HERE / "test-host.html").write_text(host, encoding="utf-8")

# ---- dist: losse CSS, JS en HTML-snippet, voor hosting via GitHub (jsDelivr) ----
CDN = f"{PAGES}/dist"
JSDELIVR = f"https://cdn.jsdelivr.net/gh/{REPO}"
dist = HERE / "dist"
dist.mkdir(exist_ok=True)

css = re.search(r"<style>\n(.*?)</style>", block, flags=re.S).group(1)
js = re.search(r"<script>\n(.*?)</script>", block, flags=re.S).group(1)
html = block
html = re.sub(r"<style>.*?</style>\n", "", html, flags=re.S)
html = re.sub(r"<script>.*?</script>\n", "", html, flags=re.S)
html = html.replace("<!-- BLOK START -->\n", "").replace("<!-- BLOK EINDE -->", "").strip()

(dist / "nestor-cases.css").write_text(css, encoding="utf-8")
(dist / "nestor-cases.js").write_text(js, encoding="utf-8")

def snippet(css_url, js_url):
    return (f'<link rel="stylesheet" href="{css_url}">\n'
            f"{html}\n"
            f'<script src="{js_url}" defer></script>\n')

snippet_intro = f"""<!--
  NESTOR CASES-BLOK (snippet voor HubSpot / CMS)

  Plak dit in het HTML-/embed-veld. CSS en script worden geladen van GitHub Pages:
      {CDN}/nestor-cases.css
      {CDN}/nestor-cases.js
  Pas je iets aan in de code, dan push je naar GitHub en staat het binnen ongeveer 10 minuten op de site.

  MEDIA: foto's, logo's en video's komen uit de HubSpot File Manager (map "NE - Website",
  met submap "klanten"), via data-media op de <section>. Een ander adres? Pas data-media aan,
  met een slash op het einde. GitHub Pages heeft dezelfde bestanden als reserve: {PAGES}/media/

  YOUTUBE: per videokaart de YouTube-link in data-video (zie de VERVANG-opmerkingen).
-->
"""
snippet_html = snippet(f"{CDN}/nestor-cases.css", f"{CDN}/nestor-cases.js").replace('data-media="media/"', f'data-media="{MEDIA_CDN}"')
(dist / "nestor-cases-snippet.html").write_text(snippet_intro + snippet_html, encoding="utf-8")

# testpagina die de losse bestanden lokaal gebruikt (zelfde vijandige site-CSS)
host_local = host.replace(embed, snippet("dist/nestor-cases.css", "dist/nestor-cases.js"))
assert host_local != host
(HERE / "test-dist.html").write_text(host_local, encoding="utf-8")

# ---- V2: drie rijen van twee (groot quote-blok naast een video), zelfde kaarten, class "nc--v2" ----
def _grid_items(h):
    g0 = h.index('  <div class="nc__grid">'); g1 = h.index('  <!-- ===== LOGO-RIJ')
    grid = h[g0:g1]
    items = ['      <div class="nc__item' + x for x in grid.split('      <div class="nc__item')[1:]]
    clean = []
    for it in items:
        it = re.split(r"\n    (?:</div>|<!-- ===== RIJ|<div class=\"nc__row\">)", it)[0]   # knip af bij het einde van de rij
        lines = it.rstrip("\n").split("\n")
        while lines and (re.fullmatch(r" {0,8}</div>\s*", lines[-1]) or lines[-1].strip() == ""):
            lines.pop()
        clean.append("\n".join(lines) + "\n        </div>\n      </div>\n")
    return g0, g1, clean

def _pick(items, key):
    m = [i for i in items if key in i]
    assert len(m) == 1, (key, len(m))
    return m[0]

def _wide(item, on):
    item = item.replace('<div class="nc__item nc__item--wide">', '<div class="nc__item">', 1)
    return item.replace('<div class="nc__item">', '<div class="nc__item nc__item--wide">', 1) if on else item

g0, g1, items = _grid_items(html)
V2_TOM = ("“Het was effectief een schot in de roos! Intussen beschikken we over een pool van een zestal Nestors "
          "die vertrouwd zijn met onze werking en die we vrij snel en flexibel kunnen inzetten.”")
tom = re.sub(r"<p class=\"nc__quote\">.*?</p>", '<p class="nc__quote">' + V2_TOM + "</p>", _pick(items, "Tom Vanden"), flags=re.S)
v2_rows = [
    ("RIJ 1: video links, groot quote-blok rechts", [_wide(_pick(items, "maatkasten-johan"), False), _wide(_pick(items, "Emilie Deboo"), True)]),
    ("RIJ 2: groot quote-blok links, video rechts", [_wide(tom, True), _wide(_pick(items, "topmotors-nestor"), False)]),
    ("RIJ 3: video links, groot quote-blok rechts", [_wide(_pick(items, "plopsa-nestor"), False), _wide(_pick(items, "Bart Verkeyn"), True)]),
]
v2_grid = '  <div class="nc__grid">\n\n'
for title, its in v2_rows:
    v2_grid += f'    <!-- ===== {title} ===== -->\n    <div class="nc__row">\n\n' + "\n".join(its) + "\n    </div>\n\n"
v2_grid += "  </div>\n\n"
v2_html = (html[:g0] + v2_grid + html[g1:]).replace('<section class="nc" id="nestor-cases"', '<section class="nc nc--v2" id="nestor-cases"', 1)
assert 'nc nc--v2' in v2_html and v2_html.count('class="nc__item') == 6

v2_snippet = (f'<link rel="stylesheet" href="{CDN}/nestor-cases.css">\n{v2_html}\n'
              f'<script src="{CDN}/nestor-cases.js" defer></script>\n').replace('data-media="media/"', f'data-media="{MEDIA_CDN}"')
v2_intro = snippet_intro.replace("NESTOR CASES-BLOK (snippet voor HubSpot / CMS)",
    "NESTOR CASES-BLOK, VERSIE 2 (snippet voor HubSpot / CMS)\n\n"
    "  Drie rijen van twee kaarten: telkens een groot quote-blok naast een video. Zelfde CSS en script\n"
    "  als versie 1; het verschil zit in de class nc--v2 op de <section> en de kaartindeling.")
(dist / "nestor-cases-v2-snippet.html").write_text(v2_intro + v2_snippet, encoding="utf-8")
v2_local = f'<link rel="stylesheet" href="dist/nestor-cases.css">\n{v2_html}\n<script src="dist/nestor-cases.js" defer></script>\n'
(HERE / "test-v2.html").write_text(host.replace(embed, v2_local).replace("<title>Testpagina: embed in een vreemde site</title>", "<title>Testpagina: cases-blok V2</title>"), encoding="utf-8")
print("ok: dist/nestor-cases-v2-snippet.html | test-v2.html")

# ---- vastgepinde snippet: verwijst naar één commit, werkt meteen (jsDelivr cachet de branch tot 12 uur) ----
import subprocess
try:
    sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, text=True).strip()
except Exception:
    sha = None
if sha:
    pinned = (snippet_intro + snippet_html).replace(f"{PAGES}/", f"{JSDELIVR}@{sha}/")
    pinned = pinned.replace("NESTOR CASES-BLOK (snippet voor HubSpot / CMS)",
        f"NESTOR CASES-BLOK (snippet voor HubSpot / CMS, vastgepind op commit {sha})\n\n"
        "  Deze versie verwijst naar één vaste commit en werkt dus meteen. Nadeel: na een code-wijziging\n"
        "  op GitHub moet je deze snippet opnieuw genereren (python3 build.py) en opnieuw plakken.\n"
        "  De gewone snippet (nestor-cases-snippet.html) laadt van GitHub Pages en volgt de branch main.")
    (dist / "nestor-cases-snippet-vast.html").write_text(pinned, encoding="utf-8")

print("ok:", "nestor-cases-licht.html", len(light), "| nestor-cases-embed.html", len(embed),
      "| test-host.html | dist/nestor-cases.css", len(css), "| dist/nestor-cases.js", len(js),
      "| dist/nestor-cases-snippet.html | test-dist.html")


# =====================================================================
# DIENSTEN-BLOK: "Dit is wat Nestor voor jou kan betekenen" (bron: diensten.html, prefix .nd)
# =====================================================================
dsrc = (HERE / "diensten.html").read_text(encoding="utf-8")
dstart = dsrc.index("<!-- BLOK START -->")
dend = dsrc.index("<!-- BLOK EINDE -->") + len("<!-- BLOK EINDE -->")
dblock = dsrc[dstart:dend]

# eventuele afbeeldingen: src -> data-src, zodat het script ze laadt vanaf data-media
dblock = re.sub(r'<(img|video)([^>]*?)\ssrc="media/', r'<\1\2 data-src="media/', dblock)
dblock = dblock.replace('<section class="nd" id="nestor-diensten">',
                        '<section class="nd" id="nestor-diensten" data-media="media/">')

dcss = re.search(r"<style>\n(.*?)</style>", dblock, flags=re.S).group(1)
djs = re.search(r"<script>\n(.*?)</script>", dblock, flags=re.S).group(1)
dhtml = dblock
dhtml = re.sub(r"<style>.*?</style>\n", "", dhtml, flags=re.S)
dhtml = re.sub(r"<script>.*?</script>\n", "", dhtml, flags=re.S)
dhtml = dhtml.replace("<!-- BLOK START -->\n", "").replace("<!-- BLOK EINDE -->", "").strip()

(dist / "diensten.css").write_text(dcss, encoding="utf-8")
(dist / "diensten.js").write_text(djs, encoding="utf-8")

def dsnippet(css_url, js_url):
    return (f'<link rel="stylesheet" href="{css_url}">\n'
            f"{dhtml}\n"
            f'<script src="{js_url}" defer></script>\n')

dsnippet_intro = f"""<!--
  NESTOR DIENSTEN-BLOK: "Dit is wat Nestor voor jou kan betekenen" (snippet voor HubSpot / CMS)

  Plak dit in het HTML-/embed-veld. CSS en script worden geladen van GitHub Pages:
      {CDN}/diensten.css
      {CDN}/diensten.js
  Pas je iets aan in diensten.html, draai python3 build.py, push naar GitHub en het staat
  binnen ongeveer 10 minuten op de site. Verandert de HTML van de kaarten zelf (tekst, volgorde,
  een kaart meer of minder), plak dan deze snippet opnieuw.

  FOTO'S: de foto's op de kaarten (media/diensten-*.jpg) staan in de HubSpot File Manager,
  map "NE - Website". Hun adres staat volledig in de HTML hieronder.
-->
"""
dsnippet_html = dsnippet(f"{CDN}/diensten.css", f"{CDN}/diensten.js").replace('data-media="media/"', f'data-media="{MEDIA_CDN}"').replace('data-src="media/', f'src="{MEDIA_CDN}')
(dist / "diensten-snippet.html").write_text(dsnippet_intro + dsnippet_html, encoding="utf-8")

# alles-in-één: CSS, HTML en script in één bestand, zonder iets van GitHub (voor een blok hoog op de pagina)
dembed_intro = f"""<!--
  NESTOR DIENSTEN-BLOK: "Dit is wat Nestor voor jou kan betekenen" (alles-in-één, aanbevolen)

  Plak dit volledige bestand in het HTML-/embed-veld. CSS, HTML en script zitten erin;
  er wordt niets van GitHub geladen, dus het blok staat meteen goed, ook als eerste blok
  onder de hero. De fonts (Baloo Paaji 2 en Source Sans Pro) staan al op nestor.be.

  FOTO'S: de foto's op de kaarten (media/diensten-*.jpg) staan in de HubSpot File Manager,
  map "NE - Website". Hun adres staat volledig in de HTML hieronder.

  Iets aanpassen? Pas diensten.html aan, draai python3 build.py en plak dit bestand opnieuw.
  (dist/diensten-snippet.html is de variant die CSS en script van GitHub Pages laadt.)
-->
"""
dembed_local = dblock.replace("<!-- BLOK START -->\n", "").replace("<!-- BLOK EINDE -->", "").strip()
# in de snippets staan de foto's met hun volledige adres (geen script nodig om ze te laden)
dembed = dembed_local.replace('data-media="media/"', f'data-media="{MEDIA_CDN}"').replace('data-src="media/', f'src="{MEDIA_CDN}')
(dist / "diensten-embed.html").write_text(dembed_intro + dembed + "\n", encoding="utf-8")

# testpagina: vijandige site-CSS, met schakelaar voor de containerbreedte (375, 700, 1027 en vol)
dhost = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Testpagina: diensten-blok in een vreemde site</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+Paaji+2:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  /* Opzettelijk lelijke site-CSS om te testen of het blok zich daartegen verdedigt */
  body {{ margin: 0; background: #223; color: #0f0; font-family: Georgia, serif; font-size: 22px; }}
  a {{ color: #ff0 !important; text-decoration: underline; font-size: 30px; }}
  a span {{ color: #0ff; }}
  button {{ background: lime; color: purple; border: 4px dotted red; font-size: 40px; padding: 30px; }}
  img, svg {{ max-width: 40%; border: 5px solid magenta; margin: 32px 0; height: auto; }}
  h2 {{ font-size: 70px; text-transform: uppercase; margin: 80px; color: pink; }}
  h3 {{ font-size: 50px; text-transform: uppercase; margin: 60px; color: orange; font-style: italic; }}
  p {{ margin: 40px; font-style: italic; }}
  /* Echte prose-regels van nestor.be (main.css) */
  .prose a {{ padding-bottom: .125rem; font-weight: 600; color: rgba(247,49,9,1); text-decoration: underline; }}
  .prose h3 {{ font-size: 1.25em; margin-top: 1.6em; margin-bottom: .6em; line-height: 1.6; color: #010306; font-weight: 600; }}
  .prose h2 {{ font-size: 2.5rem; line-height: 3rem; margin-top: 2em; margin-bottom: 1em; }}
  .prose p {{ margin-top: 1.25em; margin-bottom: 1.25em; }}
  .prose img, .prose video {{ margin-top: 2em; margin-bottom: 2em; }}
  .site-container {{ width: 700px; max-width: 100%; margin: 40px auto; background: #fff; padding: 20px; }}
  .site-container.w-375 {{ width: 375px; }}
  .site-container.w-1027 {{ width: 1027px; }}
  .site-container.w-full {{ width: 1400px; }}
  .demo-switch {{ position: fixed; top: 12px; left: 12px; z-index: 10000; display: flex; gap: 6px; background: rgba(0,0,0,.7); padding: 6px; border-radius: 9999px; }}
  .demo-switch button {{ font: 600 12px/1 "Baloo Paaji 2", sans-serif; padding: 8px 12px; border: 0; border-radius: 9999px; background: transparent; color: #fff; cursor: pointer; }}
  .demo-switch button.is-active {{ background: #fff; color: #000; }}
</style>
</head>
<body>
<div class="demo-switch">
  <button type="button" data-w="w-375">375</button>
  <button type="button" data-w="" class="is-active">700</button>
  <button type="button" data-w="w-1027">1027</button>
  <button type="button" data-w="w-full">vol</button>
</div>
<script>
  document.querySelectorAll('.demo-switch button').forEach(function (b) {{
    b.addEventListener('click', function () {{
      var c = document.querySelector('.site-container');
      c.className = 'site-container prose ' + b.dataset.w;
      document.querySelectorAll('.demo-switch button').forEach(function (x) {{ x.classList.toggle('is-active', x === b); }});
    }});
  }});
</script>
<div class="site-container prose">
  <h2>Site-kop boven het blok</h2>
{dembed_local}
  <p>Site-tekst onder het blok.</p>
</div>
</body>
</html>
"""
(HERE / "test-diensten.html").write_text(dhost, encoding="utf-8")
print("ok: dist/diensten.css", len(dcss), "| dist/diensten.js", len(djs), "| dist/diensten-snippet.html | dist/diensten-embed.html", len(dembed), "| test-diensten.html")
