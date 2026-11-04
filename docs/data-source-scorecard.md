# Data source scorecard

Decides which Data sources stay in the Build skill. The Session assumes chat only: the Participant pastes `SKILL.md` into a chat, and the agent usually cannot make requests (ADR 0002). So the agent writes the App blind from the skill text, and every URL, layer name and field name in it must be right as written. A failure that leaves an empty map with no console error is the worst kind, because the Participant has nothing to paste back.

## How to check

1. **Automatic part:** `python3 -I scripts/qgis/load_skill_sources.py` requests every example URL in the "Datakilder" part of `SKILL.md` as written, plus a sample of each layer or collection the skill only names. It prints status, CORS, feature count, size, time and field names. `scripts/check-data-sources.sh` stays the scheduled check that sources answer at all.
2. **QGIS part:** open the same file in the QGIS Python console editor and press Run. Every answer becomes a layer, grouped by skill section, Statbank is joined onto Kommunegrænser, and OpenFreeMap is added as a vector tile basemap. The QGIS part has not been run yet; the OpenFreeMap vector tile layer is the step most likely to need a fix.
3. Fill in the **QGIS** columns below and the checklist further down, then settle the shortlist with `/grill-with-docs` and record it as an ADR.

## Criteria

Each criterion scores 0–2, for a total out of 10.

| Criterion | 2 | 1 | 0 |
|---|---|---|---|
| **Coverage** | All of Denmark | Several regions or cities | One city |
| **Blind-safe** | Standard GeoJSON, nothing to get wrong | One quirk, documented in the skill | Several steps, or fails silently |
| **Speed and size** for a typical area | Under 1 s and 1 MB | A few s or MB | Over 10 s or 5 MB |
| **Skill length** (lines in its section) | Under 10 | 10–14, or needs another source | 15 or more |
| **Idea value** (judgement) | Serves many Ideas, or enables other sources | Some Ideas, or overlaps another source | Niche |

## Scores

Measured 2026-11-04 from this machine with `load_skill_sources.py`. All sources answered HTTP 200 with `Access-Control-Allow-Origin: *`.

| Data source | Measured (example URL) | Cov. | Blind | Speed | Length | Idea | **Total** | QGIS: example OK | QGIS: fields OK | QGIS notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Kommunegrænser | 99 features, 502 KB, 0.5 s | 2 | 2 | 2 | 1 | 2 | **9** | | | |
| Danmarks Miljøportal | 77 fredninger near Aalborg, 181 KB, 0.2 s; all 12 named layers exist | 2 | 1 | 2 | 0 | 2 | **7** | | | |
| MiljøGIS Natura 2000 | 7 areas near Aalborg, 273 KB, 0.3 s | 2 | 1 | 2 | 2 | 1 | **8** | | | |
| DMI Open Data | 356 stations, 93 KB, 0.2 s; all 4 named collections answer | 2 | 1 | 2 | 1 | 2 | **8** | | | |
| Danmarks Statistik | 105 rows (99 municipalities + regions + country), 1 KB, starts with BOM | 2 | 0 | 2 | 1 | 2 | **7** | | | |
| Vejdirektoratet | Not UTF-8 (ISO-8859-1), 0.7 s; no example URL in the skill | 2 | 1 | 2 | 2 | 1 | **8** | | | |
| Overpass API | 32 hotels in Aalborg, **41.8 s** | 2 | 0 | 0 | 2 | 2 | **6** | | | |
| Københavns Kommune | `legeplads` only; the other ~480 layers are unnamed | 0 | 0 | 2 | 2 | 1 | **5** | | | |
| Road noise | 0 hits at 20 m and test point, hits at 500 m; 50 Lden features = 9.5 MB | 0 | 0 | 1 | 0 | 2 | **3** | | | |

OpenFreeMap is not scored: it is the fixed basemap (ADR 0001). Its positron style answered with 55 layers.

### What the measurements changed

- **Overpass** took 42 s for one municipality. The query has `timeout:60`, so a busy day will time it out in front of the Participant.
- **Vejdirektoratet** scores higher than first guessed: its encoding error is visible, and the skill gives the exact decoding line. The risk is that the skill has no example URL, so the agent composes the bbox itself.
- **Danmarks Miljøportal** loses a point on length: 16 lines, mostly the list of 12 layers.
- **Natura 2000** is the union of habitat areas and bird protection areas, both already in Miljøportal (`dai:habitat_omr`, `dai:fugle_bes_omr`). If QGIS shows they match, MiljøGIS can go.

## QGIS checklist: claims in the skill

Tick each one in QGIS. Any claim that is wrong is a bug in the skill, whatever the source's score.

- **Danmarks Miljøportal**
  - [ ] `Fred_navn` and `Link` hold a readable name and a working link
  - [ ] § 3 lakes example (København) shows lakes, with `Natyp_navn` = "Sø"
  - [ ] Fredninger example lies around Aalborg, not shifted or swapped
- **MiljøGIS Natura 2000**
  - [ ] `n2000_navn` and `n2000_nr` are filled in
  - [ ] Areas match the union of `dai:habitat_omr` and `dai:fugle_bes_omr` (decides whether to drop MiljøGIS)
- **Road noise**
  - [ ] Lden/Lnight bands cover only København, Odense, Aarhus and Aalborg
  - [ ] Bands nest inside each other, so the highest `db_low` is the right value
  - [ ] Building interiors fall in holes in the bands (the reason for the 20 m radius)
- **DMI Open Data**
  - [ ] Observations sit on land stations, and `value` is a plausible temperature
  - [ ] `stationId` in observations matches `stationId` in stations
- **Danmarks Statistik + Kommunegrænser**
  - [ ] The join on `lau1vaerdi` = `OMRÅDE` fills all 99 municipalities, with none left grey
  - [ ] `navn`, `kommunekode` (4 digits) and `lau1vaerdi` (3 digits) look as the skill says
- **Vejdirektoratet**
  - [ ] `AADT`, `GNS_HASTIGHED`, `HAST_GRAENSE`, `LBIL_PCT`, `AAR`, `VEJNAVN` and `KOMMUNE` are filled in
  - [ ] Street names show æ, ø and å correctly
- **Københavns Kommune**
  - [ ] `legeplads` points lie in København; `navn` and `link` are filled in
- **Overpass API**
  - [ ] The hotels lie inside Aalborg Kommune, and most have `name`
- **OpenFreeMap**
  - [ ] Positron draws in QGIS as a vector tile basemap

## Shortlist

To be decided from the scores and checklist. Draft for `/grill-with-docs`: keep Kommunegrænser, Danmarks Miljøportal, DMI and Danmarks Statistik; decide on Natura 2000 (merge into Miljøportal), Vejdirektoratet and road noise; move Københavns Kommune and Overpass to "Andre datakilder" or drop them.
