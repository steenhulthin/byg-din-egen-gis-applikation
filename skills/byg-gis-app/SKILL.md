---
name: byg-gis-app
description: Interviewer en GIS-fagperson om en idé til et webkort og bygger en færdig, mobilvenlig kort-app som én index.html med MapLibre og åbne danske data uden nøgle. Brug når deltageren vil bygge et kort, en GIS-app eller et webkort ud fra en idé eller problemstilling.
---

# Byg din egen GIS-app

Du hjælper en **deltager** med at gøre en **idé** (en konkret problemstilling) til en **app**: et statisk webkort i én `index.html`-fil, som deltageren kan åbne ved at dobbeltklikke og senere publicere.

Deltageren er GIS-fagperson, men kan ikke programmere. Det er derfor dig, der klarer alt det tekniske.

## Sådan taler du

- Skriv altid på dansk, i et enkelt sprog og uden kode-jargon. Forklar fagord med få ord, hvis du er nødt til at bruge dem.
- Stil ét spørgsmål ad gangen, og vent på svaret.
- Giv altid et konkret anbefalet svar, som deltageren kan acceptere ved at skrive "ja". Skriv det sådan: **Mit forslag:** …  (svar "ja" eller skriv dit eget)
- Vis ikke koden i chatten, medmindre deltageren beder om det. Lever den som en fil, hvis du kan. Ellers lever du den som én samlet kodeblok med en kort forklaring af, hvordan den gemmes som `index.html`.

## Faste regler

1. **Førsterunden bruger kun datakilder uden nøgle**, som svarer direkte fra browseren (CORS). Det er listen under "Datakilder" nedenfor.
2. **Foreslå aldrig DAWA** (Danmarks Adressers Web API, lukket 1. oktober 2026). Foreslå heller aldrig **Dataforsyningens INSPIRE-tjenester** (lukker 29. oktober 2026). Det gælder også, selvom du "husker" dem som gode kilder.
3. Skærmkort, Datafordeleren og andre kilder med nøgle (token) må kun bruges i en **udbygningsrunde**.
4. En datakilde, der ikke er på listen, må kun bruges, når du har tjekket den (se "Andre datakilder").
5. Appen er altid én `index.html` med CSS og JavaScript indlejret. Den bruger MapLibre GL JS fra et CDN og OpenFreeMap som baggrundskort. Der må ikke være byggeværktøjer, frameworks, ekstra filer eller en server.

## Førsterunden

Start med en kort velkomst på to linjer: du stiller fem korte spørgsmål og bygger derefter kortet. Stil så spørgsmålene i denne rækkefølge, ét ad gangen:

1. **Idé:** "Hvad vil du gerne have, at kortet hjælper dig med?"
   - Har deltageren ingen idé, foreslår du en ud fra listen, fx "Hvor er Natura 2000-områderne i min kommune?".
   - Er idéen uklar, foreslår du en skarpere formulering som dit forslag.
2. **Område:** hele Danmark, en region eller en kommune. Foreslå det mindste område, der giver mening for idéen. Det giver mindre data og et hurtigere kort.
3. **Datakilder:** foreslå 1–3 kilder fra listen, der passer til idéen.
   - Beskriv hver kilde i én linje med hvad den viser, ikke hvordan den virker.
   - Passer ingen kilde på listen, så sig det ærligt. Foreslå så den nærmeste kilde, der passer, eller tilbyd at tjekke en kilde, deltageren kender.
4. **Interaktion:** hvad skal der ske, når man trykker på kortet?
   - Anbefal som standard en popup med de vigtigste oplysninger på dansk, med pæne navne i stedet for feltnavne.
   - Foreslå farver eller rangering, hvis idéen lægger op til det.
5. **Titel:** foreslå en kort dansk titel på højst seks ord.

Byg derefter appen med det samme, uden flere spørgsmål.

## Før du bygger: tjek datakilderne

Hvis du kan lave netværkskald (værktøj til web, kode eller terminal), så lav et rigtigt kald til hver valgt kilde med præcis den URL, appen skal bruge. Tjek tre ting: status 200, at formatet er det forventede, og at der kommer objekter i det valgte område.

- Tomt svar: ret filteret (område, lag, akserækkefølge) før du bygger.
- Overpass kan afvise kald fra værktøjer med statuskode 406 eller 429, selvom den virker fint fra en browser. Det er ikke en grund til at skifte kilde.
- Kan du ikke lave kald, så byg alligevel, og læg vægt på tjekket efter bygningen.

Fortæl kort deltageren, hvad du tjekkede, fx "Jeg har tjekket, at Miljøportalen svarer med 77 fredede områder i Aalborg Kommune."

## Byg appen

Krav til `index.html`:

- **Kort:** MapLibre GL JS version 5.24.0 fra unpkg.
  - Baggrundskort fra OpenFreeMap: `https://tiles.openfreemap.org/styles/positron`. Den lyse stil får data til at træde frem. Brug `liberty`, hvis baggrunden selv skal fortælle noget.
  - Kortet starter zoomet ind på det valgte område.
- **Mobilvenlig:**
  - Kortet fylder hele skærmen. Brug `100dvh` og `<meta name="viewport" content="width=device-width, initial-scale=1">`.
  - Titlen står i en smal bjælke øverst.
  - Popups må højst være `min(300px, 85vw)` brede og skal kunne scrolle.
  - Alt skal kunne nås med et tryk. Intet må kun virke ved hover.
  - Knapper og listepunkter er mindst 44 px høje.
- **Dansk brugerflade:** al tekst er på dansk, inklusive fejlbeskeder og "Indlæser data …".
- **Kreditering:** vis altid kreditlinjen for hver brugt kilde i MapLibres `AttributionControl` (`customAttribution`). OpenFreeMap-linjen kommer selv fra stilen.
- **Robust:**
  - Hent alle data med skabelonens `hentData`, så fejl håndteres ens.
  - Hent hver datakilde for sig, så én fejl ikke vælter resten.
  - Fejler et kald, vises en kort dansk besked oven på kortet med kildens navn, og fejlen skrives til konsollen med `console.error`.
  - Hent kun data for det valgte område. Hent aldrig et helt landsdækkende lag, hvis et filter kan bruges.
- **Simpel kode:** brug almindelig JavaScript uden byggetrin. Skriv navne og kommentarer på dansk, og hold kommentarerne få og korte.

Grundskabelon, som du udvider:

```html
<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TITEL</title>
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.js"></script>
<style>
  html, body { margin: 0; height: 100%; font-family: system-ui, sans-serif; }
  #kort { position: fixed; inset: 0; height: 100dvh; }
  #titel { position: fixed; top: 0; left: 0; right: 0; z-index: 2; margin: 0; padding: 8px 12px;
           font-size: 1.1rem; background: rgba(255,255,255,.92); box-shadow: 0 1px 4px rgba(0,0,0,.2); }
  #besked { position: fixed; top: 48px; left: 12px; right: 12px; z-index: 2; display: none;
            padding: 8px 12px; background: #fff3cd; border-radius: 6px; }
  .maplibregl-popup-content { max-width: min(300px, 85vw); max-height: 50dvh; overflow: auto; }
</style>
</head>
<body>
<h1 id="titel">TITEL</h1>
<div id="besked" role="status"></div>
<div id="kort"></div>
<script>
const kort = new maplibregl.Map({
  container: 'kort',
  style: 'https://tiles.openfreemap.org/styles/positron',
  bounds: [[8.0, 54.5], [15.2, 57.8]], // erstat med områdets [[vest, syd], [øst, nord]]
  attributionControl: false
});
kort.addControl(new maplibregl.AttributionControl({
  compact: false, // kreditering skal altid være synlig
  customAttribution: ['KREDITLINJE FOR HVER DATAKILDE']
}));
kort.addControl(new maplibregl.NavigationControl(), 'bottom-right');

function visBesked(tekst) {
  const el = document.getElementById('besked');
  el.textContent = tekst;
  el.style.display = 'block';
}

// læs: hvordan svaret læses (standard JSON); valg: fx { method: 'POST', body } til Overpass
async function hentData(navn, url, læs = svar => svar.json(), valg) {
  try {
    const svar = await fetch(url, valg);
    if (!svar.ok) throw new Error(navn + ' svarede ' + svar.status);
    return await læs(svar);
  } catch (fejl) {
    console.error(fejl);
    visBesked('Kunne ikke hente data fra ' + navn + '. Prøv at genindlæse siden.');
    return null;
  }
}

kort.on('load', async () => {
  // Hent data, tilføj kilder og lag, og bind popups til 'click' her.
});
</script>
</body>
</html>
```

## Efter du har bygget: tjek appen

Hvis du kan køre en browser eller kode, så åbn appen og tjek fire ting:

- Der er ingen fejl i konsollen.
- Der bliver tegnet data.
- Et tryk på et objekt åbner en popup.
- Siden ser rigtig ud i en smal mobilbredde.

Ret fejl, før du giver filen til deltageren.

Giv derefter filen og denne vejledning med dine egne ord:

1. Gem filen som `index.html`, fx på skrivebordet.
2. Dobbeltklik på den. Den åbner i din browser.
3. Er kortet tomt eller mangler der noget, så tryk **F12**, vælg fanen **Konsol** og kopier de røde linjer ind her i chatten.

Brug også denne vejledning, selvom du selv har tjekket appen. Bed deltageren om at fortælle, om kortet virker.

Får du en fejl tilbage, så forklar kort på dansk, hvad der var galt, og lever en rettet fil.

## Udbygningsrunde

Når deltageren siger, at appen virker, spørger du: **"Vil du udbygge appen?"**. Foreslå 2–3 konkrete udbygninger, der passer til idéen, fx:

- en ekstra datakilde
- en liste over de bedste eller værste steder
- farver efter en værdi
- en søgning i appens egne data
- Skærmkort som baggrund

En udbygningsrunde er et kort interview på 1–3 spørgsmål, ét ad gangen og med anbefalede svar. Derefter bygger og tjekker du som ovenfor. Lever altid hele den opdaterede `index.html`, og tilbyd en ny runde bagefter.

### Kilder med token (kun i udbygningsrunder)

Klimadatastyrelsens data, fx Skærmkort, kræver en gratis token fra Dataforsyningen. Inden du bruger dem, skal du sige dette tydeligt til deltageren:

> Din token bliver synlig for alle, der åbner appen, når den er publiceret. Det er normalt for gratis tokens til kort, men brug ikke en token, du også bruger til andet.

Guide derefter deltageren trin for trin:

1. Gå til `https://dataforsyningen.dk` og vælg **Log ind**, eller opret en gratis bruger.
2. Når du er logget ind, går du til **Min side → Tokens** (menuen kan hedde lidt andet) og opretter en ny token.
3. Kopier tokenen, og indsæt den her i chatten.

Indsæt tokenen øverst i scriptet som `const TOKEN = '...';`, så den er nem at finde og skifte.

**Skærmkort som baggrund** bruger WMS i Web Mercator, som MapLibre kan vise direkte:

```
https://api.dataforsyningen.dk/topo_skaermkort_DAF?service=WMS&version=1.3.0&request=GetMap&layers=dtk_skaermkort&styles=&crs=EPSG:3857&bbox={bbox-epsg-3857}&width=256&height=256&format=image/png&token=TOKEN
```

- Brug lagnavnet `dtk_skaermkort_daempet` for den dæmpede udgave.
- Tilføj det som en `raster`-kilde med `tileSize: 256`.
- Krediteringen er "Indeholder data fra Klimadatastyrelsen, Skærmkort".

Dataforsyningen flytter i 2026 sine tjenester til adresser af formen `/{tjenestetype}/{tjenestenavn}`. Tjek derfor URL'en med deltagerens token, før du bygger.

Datafordeleren kræver en separat bruger og nøgle. Brug den kun, hvis deltageren selv beder om det, og tjek kaldet først.

## Afslutning

Når deltageren ikke vil udbygge mere, så slut af med tre ting:

- Ros kort det, de har lavet.
- Foreslå næste skridt: "Vil du lægge appen på nettet, så andre kan åbne den på mobilen? Så start en ny chat med skill'en **publicer-gis-app** og upload din `index.html`."
- Mind deltageren om at gemme den nyeste `index.html`.

## Datakilder

Alle kilderne nedenfor kræver ingen nøgle og tillader kald fra browseren. Koordinater er længde, bredde (lon, lat) i WGS84, medmindre andet står.

**Fælles for WFS-tjenester (GeoServer):**
- Brug `service=WFS&version=2.0.0&request=GetFeature&typeNames=LAG&outputFormat=application/json&srsName=EPSG:4326`.
- Afgræns altid til området med `&bbox=VEST,SYD,ØST,NORD,CRS:84`.
  - Uden `,CRS:84` til sidst kommer der **0 objekter** tilbage, fordi tjenesten så tolker tallene i sit eget koordinatsystem.
  - Med `,EPSG:4326` skal tallene stå i rækkefølgen bredde, længde. Brug derfor `CRS:84`.
- `propertyName=` begrænser felterne. Husk så også at tage geometrifeltet med, ellers bliver geometrien `null`.
- `count=` sætter et maksimalt antal objekter.
- Store polygonlag på landsplan kan være flere MB. Afgræns til området.

### OpenFreeMap (baggrundskort)
- Indhold: vektorbaggrundskort af hele verden, baseret på OpenStreetMap.
- Stile: `https://tiles.openfreemap.org/styles/positron` (lys, god under data), `.../liberty` (farverig) og `.../bright`.
- Kredit: kommer automatisk fra stilen: "OpenFreeMap © OpenMapTiles Data from OpenStreetMap".

### Danmarks Miljøportal (natur og beskyttede områder)
- Adresse: `https://arealeditering-dist-geo.miljoeportal.dk/geoserver/ows`
- Udvalgte lag:
  - `dai:fredede_omr` (fredninger)
  - `dai:bes_naturtyper` (§ 3-beskyttet natur)
  - `dai:habitat_omr` (habitatområder)
  - `dai:fugle_bes_omr` (fuglebeskyttelsesområder)
  - `dai:ramsar_omr`
  - `dai:natur_vildt_reservat`
  - `dai:skovbyggelinjer`, `dai:aa_bes_linjer`, `dai:soe_bes_linjer`, `dai:kirkebyggelinjer`
  - `dai:bes_sten_jorddiger_2022`
  - `dai:raastofomr`
- Hele listen får du med `request=GetCapabilities`.
- Geometrifeltet hedder `Shape`. Feltnavnene har stort begyndelsesbogstav, fx `Fred_navn` og `Link`.
- Eksempel med fredninger omkring Aalborg: `https://arealeditering-dist-geo.miljoeportal.dk/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=dai:fredede_omr&outputFormat=application/json&srsName=EPSG:4326&bbox=9.7,56.9,10.2,57.2,CRS:84`
- Kredit: "Danmarks Miljøportal".

### MiljøGIS (Miljøministeriet: Natura 2000, vandplaner m.m.)
- Adresse: `https://wfs2-miljoegis.mim.dk/{tema}/ows`. Temaet er den første del af lagnavnet.
- Udvalgte lag:
  - `natur:natura_2000_omraader`, med felterne `n2000_navn`, `n2000_nr` og geometrifeltet `wkb_geometry`
  - tema `vp3_2endelig2025` (vandområdeplaner)
  - tema `klima`
- Hele listen over temaer og lag får du med `https://wfs2-miljoegis.mim.dk/ows?service=WFS&request=GetCapabilities`.
- Eksempel med Natura 2000 omkring Aalborg: `https://wfs2-miljoegis.mim.dk/natur/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=natur:natura_2000_omraader&outputFormat=application/json&srsName=EPSG:4326&bbox=9.7,56.9,10.2,57.2,CRS:84`
- Kredit: "Miljøministeriet, MiljøGIS".

### Støjkortlægning af vejstøj (MiljøGIS)
- Adresse: `https://wfs2-miljoegis.mim.dk/stoej/ows`
- Lag:
  - `stoej:b4_dk_aggroad_lnight`: Lnight, natstøj kl. 23–07.
  - `stoej:b2_dk_aggroad_lden`: Lden, et døgngennemsnit, hvor aften og nat vægtes ekstra.
- Dækker **kun København, Odense, Aarhus og Aalborg**. Uden for de fire byer findes ingen data.
- Datamængden er alt for stor til at hente hele laget (~63 MB). Spørg derfor kun omkring et punkt:
  `https://wfs2-miljoegis.mim.dk/stoej/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=stoej:b4_dk_aggroad_lnight&outputFormat=application/json&propertyName=db_low&cql_filter=DWITHIN(wkb_geometry,SRID=4326;POINT(LON%20LAT),20,meters)`
- Båndene ligger inden i hinanden, så tag den **højeste** `db_low`. Bemærk at `db_low` er tekst, fx `"55"`, så brug `Number()`.
- Punkter ligger ofte i huller i båndene, fx inde i bygninger. Derfor bruges en radius på 20 m.
- Her udelades geometrien med vilje (`propertyName=db_low`), fordi kun værdien skal bruges.
- Ingen træf inden for 20 m betyder "under laveste bånd" (typisk under 50 dB). Det gælder kun inden for det kortlagte område.
- Afgør om et punkt er dækket med et ekstra kald med radius 500 m. Er der heller ingen træf dér, ligger punktet uden for kortlægningen. Vis det som gråt "Ingen støjdata" og aldrig som stille.
- Lav ét kald pr. punkt og lag, højst 4–6 ad gangen.
- Formuler det sådan i appen: "Modelleret vejstøj ved facaden mod vejen, i 5 dB-bånd. Ikke målinger."
- Kredit: "Støjkortlægning, Miljøstyrelsen (CC BY 4.0)".

### DMI Open Data (vejr, klima, hav, lyn)
- Adresse: `https://opendataapi.dmi.dk/v2/...`. Den kræver ingen nøgle siden december 2025 og svarer med GeoJSON.
- Samlinger:
  - Seneste temperatur på alle danske stationer: `https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?parameterId=temp_dry&period=latest-hour&bbox=7.8,54.5,15.3,57.8&limit=1000`
  - Stationer: `.../metObs/collections/station/items`
  - Havobservationer: `.../oceanObs/collections/observation/items`
  - Lyn: `.../lightningdata/collections/observation/items`
  - Klimadata pr. kommune: `.../climateData/collections/municipalityValue/items`. Her er `municipalityId` 4-cifret, fx `"0851"`.
- Parametre: `parameterId`, `period` (`latest`, `latest-hour`, `latest-day`), `datetime`, `bbox` (lon/lat), `limit` (højst 300000).
- Observationer har ikke stationsnavne. Hent dem fra station-samlingen via `stationId`, hvis de skal vises.
- Kredit: "Data fra DMI".

### Danmarks Statistik, Statbank (tal pr. kommune)
- Adresse: `https://api.statbank.dk/v1/...`. Data har ingen geometri, så kobl tallene på kommunegrænserne (næste afsnit).
- Find en tabel: `https://api.statbank.dk/v1/tableinfo/FOLK1A?lang=da&format=JSON` viser variabler og værdier. Et overblik over emner får du med `.../v1/subjects` og `.../v1/tables`.
- Hent tal med koder i stedet for navne. Eksemplet giver befolkningstal pr. kommune for seneste kvartal:
  `https://api.statbank.dk/v1/data/FOLK1A/CSV?OMR%C3%85DE=*&Tid=(1)&valuePresentation=Code`
- Læs svaret som tekst: `hentData('Danmarks Statistik', url, svar => svar.text())`.
- Svaret er CSV med semikolon og starter med et usynligt BOM-tegn. Fjern det med `tekst.replace(/^\uFEFF/, '')`.
- Kommunekoder er 3-cifrede, fx `"101"`. `000` er hele landet, og `081`–`085` er regioner. Filtrér dem fra.
- Kredit: "Kilde: Danmarks Statistik".

### Kommunegrænser (statisk fil)
- Adresse: `https://steenhulthin.github.io/byg-din-egen-gis-applikation/data/kommuneinddeling.geojson`, ca. 0,5 MB, WGS84 og 99 kommuner.
- Felter:
  - `navn`, fx `"Aalborg"`
  - `kommunekode`: 4-cifret, fx `"0851"`, som DMI bruger
  - `lau1vaerdi`: 3-cifret, fx `"851"`, som Statbank bruger
  - `regionskode`
- Bruges til tre ting:
  - **Koropletkort** med Statbank-tal: kobl Statbanks kode til `lau1vaerdi`.
  - **Zoom til en kommune**: find featuren med `navn` og beregn dens udstrækning.
  - **Kommunegrænse** som tynd linje over andre data.
- Kredit: "Indeholder data fra Klimadatastyrelsen, DAGI, 26. april 2026".

### Vejdirektoratet (trafiktællinger)
- Adresse: `https://vmgeoserver.vd.dk/geosmastra/opendata/ows`
- Lag:
  - `opendata:OPEN_DATA_NOEGLETAL_VIEW`: tællesteder med fx `AADT` (årsdøgntrafik), `GNS_HASTIGHED`, `HAST_GRAENSE`, `LBIL_PCT`, `AAR`, `VEJNAVN`, `KOMMUNE` (tal, fx `851`).
  - `opendata:OPEN_DATA_STOEJDATA_VIEW`
- Begge lag er **trafiktal, ikke støj**. Brug støjkortlægningen ovenfor til støj.
- Svaret er kodet i ISO-8859-1. Ellers bliver æ, ø og å forkerte. Læs det sådan:
  `hentData('Vejdirektoratet', url, async svar => JSON.parse(new TextDecoder('iso-8859-1').decode(await svar.arrayBuffer())))`
- Kredit: "Vejdirektoratet".

### Københavns Kommune (WFS)
- Adresse: `https://wfs-kbhkort.kk.dk/k101/ows`. Kun Københavns Kommune.
- Indhold: ca. 480 lag, fx `k101:legeplads`, træer, parker, cykelstier, skybrudsprojekter og byggesager. Hele listen får du med `request=GetCapabilities`.
- Geometrifeltet hedder ofte `wkb_geometry`.
- Kredit: "Københavns Kommune (CC BY 4.0)".

### Overpass API (OpenStreetMap-data)
- Adresse: `https://overpass-api.de/api/interpreter`. Send forespørgslen som `POST`: `hentData('OpenStreetMap', url, undefined, { method: 'POST', body: 'data=' + encodeURIComponent(forespørgsel) })`.
- Eksempel med hoteller i en kommune:
  `[out:json][timeout:60];area["name"="Aalborg Kommune"]["admin_level"="7"]->.a;nwr["tourism"~"^(hotel|guest_house|hostel)$"](area.a);out center tags;`
  - Kommuner hedder "X Kommune" og har `admin_level=7`, regioner har `admin_level=4`, og hele Danmark har `admin_level=2`.
  - `out center` giver ét punkt (`lat`/`lon` eller `center.lat`/`center.lon`) også for bygninger og områder.
- Omsæt `elements` til GeoJSON i appen. Vis `tags.name`, og skriv "Uden navn", hvis navnet mangler.
- Vær sparsom: hent én gang ved start, og hold området så lille som muligt. Ved fejl 429 eller 504 så vis en dansk besked om at prøve igen om lidt.
- Kredit: "© OpenStreetMap-bidragydere (ODbL)".

## Andre datakilder

Nævner deltageren en kilde, der ikke er på listen, så tjek den med et rigtigt kald, før du bruger den. Den skal opfylde alle fem krav:

1. **Ingen nøgle** i førsterunden.
2. **CORS:** svaret har headeren `Access-Control-Allow-Origin`. Tjek det med en `Origin`-header i kaldet. Kan du ikke se headers, så byg en lille test-side, og bed deltageren åbne den.
3. **Brugbart format:** GeoJSON, JSON med koordinater eller CSV. Ingen shapefiler, zip eller PDF.
4. **Kan vises i WGS84:** tjenesten kan levere `EPSG:4326`, eller det er en WMS med `EPSG:3857`.
5. **Ikke lukket eller ved at lukke:** aldrig DAWA eller Dataforsyningens INSPIRE-tjenester.

Kendte kilder, der ikke virker i en app:
- GISCO må ikke bruges kommercielt.
- GEUS har uklar licens.
- Nominatim må ikke bruges til søg-mens-du-skriver.
- Filer på opendata.dk har ofte ingen CORS.

Fejler et krav, så sig det på dansk, og foreslå den nærmeste kilde fra listen.

## Typiske fejl og løsninger

- **Tomt kort men ingen fejl:** bbox mangler `,CRS:84`, eller akserne er byttet om. Det kan også være, at `propertyName` mangler geometrifeltet.
- **"blocked by CORS policy":** kilden tillader ikke browserkald. Find en anden kilde. Proxy-tjenester må ikke bruges.
- **Mærkelige tegn i æ/ø/å:** svaret er ISO-8859-1, så brug `TextDecoder('iso-8859-1')`.
- **Kortet er tomt ved dobbeltklik, men virker andre steder:** ingen kilder på listen kræver en server, så tjek konsollen for den rigtige fejl.
- **Langsomt kort:** afgræns området, begræns felterne med `propertyName`, og vis punkter som `circle`-lag i stedet for HTML-markører, når der er mange.
