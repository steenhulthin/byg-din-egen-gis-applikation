# Apps reference their Data sources directly by URL

The agent usually writes the App blind (ADR 0002), and every line of data handling it writes is a place for a silent failure. So every Data source on the curated list must be usable as a URL handed straight to a MapLibre source: a `geojson` source with `data: URL`, or a `raster` source with WMS `tiles` in EPSG:3857. The App has no `fetch`, parsing, decoding, joining or conversion code, and the Participant never downloads a data file. The template's `hentData` is replaced by `tilføjKilde`, which only records a source's Danish name for the error message raised by MapLibre's `error` event.

This keeps Kommunegrænser, Danmarks Miljøportal (WFS, plus WMS for layers too large for GeoJSON), MiljøGIS Natura 2000, DMI Open Data observations and Københavns Kommune, and drops the sources that cannot be referenced directly:

- **Danmarks Statistik**: CSV without geometry, which has to be joined onto Kommunegrænser in code.
- **Vejdirektoratet**: answers in ISO-8859-1, so MapLibre's own loader garbles æ, ø and å.
- **Overpass API**: needs a POST and a conversion to GeoJSON, and took 42 s for one municipality.
- **Road noise (MiljøGIS)**: needs one DWITHIN request per point, and MiljøGIS has WMS disabled.

## Consequences

- Ideas built on numbers per municipality, traffic counts, OpenStreetMap features or road noise are no longer First round Ideas. The Backup app (quietest hotels by road noise) was built before this decision and still uses Overpass and road noise.
- Features that need the data in JavaScript, such as a ranked list or a search in the App's own data, are no longer suggested as Extension rounds. Colours, filters and layer toggles in MapLibre expressions still are.
- "Andre datakilder" now requires a source to be referenceable directly, in UTF-8 with a plain GET.
