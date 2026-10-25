# Data

## kommuneinddeling.geojson

Danmarks 99 kommuner som polygoner, til brug i apps uden nøgle, fx til at koble tal fra Danmarks Statistik på kommunerne.

- **Kilde:** DAGI (Danmarks Administrative Geografiske Inddeling), `Kommuneinddeling`, hentet fra Datafordeleren.
- **Hentet:** 26. april 2026.
- **Koordinatsystem:** WGS84 (EPSG:4326), forenklet til ca. 0,5 MB.
- **Vigtige felter:**
  - `navn`, fx `"Aalborg"`
  - `kommunekode`: 4-cifret, fx `"0851"`
  - `lau1vaerdi`: 3-cifret, fx `"851"`, som Danmarks Statistik bruger
- **Adresse:** `https://steenhulthin.github.io/byg-din-egen-gis-applikation/data/kommuneinddeling.geojson`

Kreditering, som skal vises i apps, der bruger filen:

> Indeholder data fra Klimadatastyrelsen, DAGI, 26. april 2026
