#!/usr/bin/env python3
"""Maakt uit index.html (de demo met schakelaar) drie afgeleide bestanden:

  nestor-cases-licht.html   volledige testpagina, alleen de lichte versie
  nestor-cases-embed.html   alleen het blok, om in een embed-/HTML-veld van je CMS te plakken
  test-host.html            testpagina die het embed-blok in een "vijandige" site plaatst

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
