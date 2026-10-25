# Checkpoint A: the App in a browser

Opens one App file in headless Chromium at a desktop and a phone (Pixel 7) size and checks it from the outside only:

- no console errors
- every data request succeeds
- the map renders, and at least one feature (or HTML marker) from the App's own data is drawn
- the page is `lang="da"`, and the title and the App's own credits are Danish text (no common English words; the OpenFreeMap credit is ignored)
- on the phone: the map fills the screen, and a tap on a feature opens a popup

It needs the network, because Apps load MapLibre, OpenFreeMap and their Data sources live.

## Before the Session: check an App saved from a skill run

```sh
npm ci
npx playwright install --with-deps chromium   # once per machine
npm run checkpoint-a -- path/to/index.html
```

Every failed check is listed by name, both viewports included.

## Limits

- It expects a First round App: MapLibre loaded from a `<script>` tag, a vector basemap and the App's own data as GeoJSON sources or HTML markers. A raster basemap such as Skærmkort, or data drawn only as raster or vector tiles, fails "the map renders" or "at least one feature is drawn".
- The Danish check is a heuristic: it catches common English words, not every English text.
- The phone tap hits the first uncovered feature it finds. If that feature's layer has no click handler, it reports a missing popup.

## CI

`.github/workflows/checkpoint-a.yml` runs it against `backup/index.html` once the Backup app exists, and runs `npm test`, which tests Checkpoint A itself against the fixture Apps in `fixtures/`.
