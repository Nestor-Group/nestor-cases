# Nestor cases-blok

Een nabouw van het casestudies-blok van metaview.ai, gevuld met quotes uit de cases op nestor.be.

## Bestanden

- `index.html`: de demo met schakelaar tussen de lichte en de oranje versie. Dit is het bronbestand.
- `nestor-cases-embed.html`: **dit plak je in je website.** Alleen het blok (CSS, HTML, JS), zonder `html`, `head`
  of `body`. Bovenaan staat uitleg over de media-locatie en de YouTube-links.
- `nestor-cases-licht.html`: volledige testpagina met alleen de lichte versie, om lokaal te openen.
- `test-host.html`: testpagina die het embed-blok in een opzettelijk lelijke site met een smalle container zet,
  om te controleren dat het blok zich tegen vreemde CSS verdedigt.
- `dist/`: de opgesplitste versie: `nestor-cases.css`, `nestor-cases.js` en `nestor-cases-snippet.html`
  (de HTML die in HubSpot komt en de CSS en JS van GitHub laadt).
- `test-dist.html`: zelfde vijandige testpagina, maar met de losse bestanden uit `dist`.
- `build.py`: maakt alle afgeleide bestanden opnieuw uit `index.html` (`python3 build.py`).
  Pas dus altijd `index.html` aan en draai daarna dit script.
- `media/`: foto's, logo's en video's. Per short drie bestanden:
  - `naam.jpg`: posterbeeld van de kaart
  - `naam-loop.mp4`: stille loop van 6 seconden die afspeelt bij hover
  - `naam.mp4`: de volledige short, gebruikt in de popup zolang er geen YouTube-link is
- `quotes-cases.md`: alle quotes uit de cases, met het gebruikte voorstel onderaan.

## In de website zetten (aanbevolen: media in HubSpot, code op GitHub)

1. **Media in HubSpot.** Upload de map `media` in de HubSpot File Manager (Marketing > Files), bijvoorbeeld in een
   map `cases/media`. Noteer de URL van die map, iets als `https://www.nestor.be/hubfs/cases/media/`.
2. **Code op GitHub.** Deze map staat in de repository `Nestor-Group/nestor-cases`, met GitHub Pages aan.
   De map `dist` bevat `nestor-cases.css` en `nestor-cases.js`; die worden geladen van
   `https://nestor-group.github.io/nestor-cases/dist/nestor-cases.css` (idem voor `.js`). De media komen
   standaard ook van Pages (`https://nestor-group.github.io/nestor-cases/media/`).
3. **Snippet in HubSpot.** Open `dist/nestor-cases-snippet.html`, vul de media-URL in bij `data-media="..."` op de
   `<section>` (met slash op het einde) en plak de volledige inhoud in het HTML-/embed-veld van de pagina.

Daarna: iets aanpassen in `index.html`, `python3 build.py` draaien, committen en pushen. GitHub Pages bouwt de
site opnieuw (een paar minuten) en serveert met een cache van 10 minuten.
Alleen als de HTML van de kaarten zelf verandert (nieuwe quote, andere volgorde), plak je de snippet opnieuw.
`dist/nestor-cases-snippet-vast.html` is een variant die via jsDelivr naar één vaste commit verwijst, voor als
Pages ooit niet beschikbaar is.

**Alternatief zonder GitHub:** plak `nestor-cases-embed.html` in zijn geheel in het embed-veld. Zelfde resultaat,
maar bij elke aanpassing moet je opnieuw plakken.

Het blok kijkt naar de breedte van de container waarin het staat: breed genoeg (vanaf 960px) wordt het een grid
van drie rijen, smaller wordt het een carrousel. De fonts staan al op nestor.be, er is geen extra stylesheet nodig.

## Hoe het werkt

- **Desktop (vanaf 1024px)**: drie rijen van vier kaarten. Per rij is één kaart breder (`nc__item--wide`),
  telkens één positie verder dan in de rij erboven.
- **Tablet en mobiel**: dezelfde kaarten als horizontale carrousel met snap-points en twee pijlknoppen.
- **Quote-kaart**: citaat, avatar, naam, functie en bedrijfslogo.
- **Stat-kaart**: groot logo, bedrijfsnaam en resultaat.
- **Video-kaart**: poster uit de short, loop bij hover, popup bij klik.

## Video's koppelen aan YouTube

Elke videokaart heeft een `data-video`-attribuut. Zet daar de YouTube-link in, bijvoorbeeld:

```html
<div class="nc__card nc__card--video" role="button" tabindex="0"
     data-video="https://www.youtube.com/watch?v=XXXXXXXXXXX" ...>
```

De popup toont dan de YouTube-speler in 16:9. Voor een YouTube Short voeg je `data-ratio="9/16"` toe.
Vimeo-links en mp4-bestanden werken ook.

## Placeholders vervangen

Zoek in `index.html` op `VERVANG`. Je vindt per kaart een uitgecommentarieerde `<img>` die je in de plaats
van de placeholder zet:

- `nc__ph-avatar` (initialen) wordt `<img class="nc__avatar" src="..." alt="...">`
- `nc__ph-logo` (gestippeld kader) wordt `<img class="nc__logo" src="..." alt="...">`
- `nc__ph-logo--big` (stat-kaart) wordt `<img class="nc__biglogo" src="..." alt="...">`

Logo's liefst wit op transparant (SVG of PNG). Zodra alle placeholders weg zijn, mag het CSS-blok
"Placeholders" eruit.

## Kleuren en fonts

Het blok volgt de Nestor-huisstijl: gebroken wit (#F6F4EF) als achtergrond, witte kaarten, grijze tekst (#575757)
en oranje-rood (#F73109) voor de kleine kop, de functies, de resultaatregels en de knoppen.

- **Lichte versie** (standaard): `<section class="nc" id="nestor-cases">`
- **Oranje versie**: `<section class="nc nc--oranje" id="nestor-cases">` geeft een oranje achtergrond met witte knoppen.

De demo-pagina heeft linksboven een schakelaar om beide te vergelijken. Die schakelaar hoort niet bij het blok.

Alle kleuren staan als CSS-variabelen bovenaan de `<style>` (`--nc-bg`, `--nc-card`, `--nc-accent`, `--nc-btn-bg` …).
Logo's: in de witte kaarten staan de originele (gekleurde) logo's, op de video- en fotokaarten de witte versies.
