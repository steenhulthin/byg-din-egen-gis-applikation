# First round uses only no-key data sources, on MapLibre with OpenFreeMap

Participants are GIS professionals without programming experience who will repeat the Live demo at home with no help, so every key or account in the first round is a likely point of failure. The first round of an App therefore uses only data sources that need no key and allow browser requests (CORS). The map is MapLibre GL JS on an OpenFreeMap basemap, because those sources deliver lon/lat GeoJSON and OpenFreeMap needs no key. Klimadatastyrelsen's token-protected services, including the official Skærmkort basemap, are only offered in Extension rounds, even though they are the community's everyday data. Their no-key INSPIRE services close on Dataforsyningen on 29 October 2026, and the replacement on Datafordeleren needs a key, so Klimadatastyrelsen has no no-key source in the first round.

## Considered Options

- **Skærmkort as the default basemap**: the obvious choice at a Danish GIS conference, but it needs a Dataforsyningen token for each Participant, and its WMTS is EPSG:25832 only, which would push the library choice to OpenLayers or Leaflet with Proj4Leaflet.
- **Leaflet with OpenStreetMap tiles**: simpler, but the OSM tile usage policy is strict and the result looks less finished.

## Consequences

- DAWA closed on 1 October 2026 and must never be suggested, even though most training data still points to it. Its replacements (Adressevælger, Datafordeleren) are not first-round sources.
- Dataforsyningen is moving its services to `/{servicetype}/{servicename}` URLs through 2026, so the curated list needs rechecking before each Session.
