// Tests Checkpoint A itself: it must pass good Apps and fail each broken one.
import { after, test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../..', import.meta.url));
const goodApp = fileURLToPath(new URL('fixtures/good-app.html', import.meta.url));
const work = mkdtempSync(join(tmpdir(), 'checkpoint-a-'));
after(() => rmSync(work, { recursive: true, force: true }));

const MAP_STYLE = '#kort { position: fixed; inset: 0; height: 100dvh; }';
const CREDIT = "'Indeholder data fra Klimadatastyrelsen, DAGI, 25. oktober 2026'";

function checkpointA(appFile) {
  const result = spawnSync('npm', ['run', '--silent', 'checkpoint-a', '--', appFile],
    { cwd: root, encoding: 'utf8', shell: process.platform === 'win32' });
  return { status: result.status, output: result.stdout + result.stderr };
}

// Writes a copy of the good App with one piece of text replaced, and returns its path.
function variantApp(name, from, to) {
  const html = readFileSync(goodApp, 'utf8');
  assert.ok(html.includes(from), `fixture text not found: ${from}`);
  const file = join(work, `${name}.html`);
  writeFileSync(file, html.replace(from, to));
  return file;
}

test('a good App passes', () => {
  const { status, output } = checkpointA(goodApp);
  assert.equal(status, 0, output);
});

test('an App that draws HTML markers instead of a layer passes', () => {
  const { status, output } = checkpointA(variantApp('markers',
    "kort.addSource('kommuner', { type: 'geojson', data: kommuner });",
    `for (const kommune of kommuner.features.filter(k => k.properties.navn === 'Aalborg')) {
    new maplibregl.Marker().setLngLat([9.92, 57.05])
      .setPopup(new maplibregl.Popup().setText(kommune.properties.navn)).addTo(kort);
  }
  return;`));
  assert.equal(status, 0, output);
});

// [what is broken, replaced text, replacement, expected failure message]
const brokenApps = [
  ['logs a console error', "kort.on('load', async () => {",
    "kort.on('load', async () => {\n  console.error('noget gik galt');", /no console errors/],
  ['has a failing data request', 'data/kommuneinddeling.geojson', 'data/missing.geojson',
    /every data request succeeds/],
  ['draws no features', "paint: { 'fill-color'",
    "filter: ['==', 'navn', 'findes ikke'], paint: { 'fill-color'", /at least one feature is drawn/],
  ['has a map that does not render', MAP_STYLE, '#kort { display: none; }', /the map renders/],
  ['creates no map', 'new maplibregl.Map(', 'new Object(', /the App creates a MapLibre map/],
  ['has an English title', '<title>Kommuner i Nordjylland</title>',
    '<title>Quietest hotel in Aalborg</title>', /the title is Danish text/],
  ['is not marked as Danish', '<html lang="da">', '<html lang="en">', /the page is marked as Danish/],
  ['has English credits', CREDIT, "'Contains data from the Danish Climate Data Agency'",
    /the credits are Danish text/],
  ['has no credits of its own', `customAttribution: [${CREDIT}]`, 'customAttribution: []',
    /the App credits its data sources/],
  ['has a map that does not fill a phone screen', MAP_STYLE,
    '#kort { position: fixed; top: 0; left: 0; width: 100%; height: 300px; }',
    /\[phone\][\s\S]*the map fills the screen/],
  ['opens no popup on a tap', "kort.on('click', 'kommuner'", "kort.on('dblclick', 'kommuner'",
    /a tap opens a popup/],
];

for (const [broken, from, to, message] of brokenApps) {
  test(`an App that ${broken} fails`, () => {
    const { status, output } = checkpointA(variantApp(broken.replaceAll(' ', '-'), from, to));
    assert.notEqual(status, 0, output);
    assert.match(output, message);
  });
}
