// Checkpoint A: opens an App file and checks it from the outside only.
import { test, expect } from '@playwright/test';
import { pathToFileURL } from 'node:url';

const app = process.env.CHECKPOINT_APP;
if (!app) throw new Error('Set CHECKPOINT_APP, or run: npm run checkpoint-a -- path/to/index.html');

// Records the first MapLibre map the App creates, without touching the App's own code.
function recordMap() {
  let lib;
  Object.defineProperty(window, 'maplibregl', {
    configurable: true,
    get: () => lib,
    set(value) {
      const Original = value.Map;
      value.Map = class extends Original {
        constructor(...args) {
          super(...args);
          window.__checkpointMap ??= this;
        }
      };
      lib = value;
    },
  });
}

// Common English words that should not appear in a Danish App. A heuristic: Danish
// has no reliable test without a language library. Words that are also Danish
// (for, to, at, by, is, over, data) are left out. Letters, not \b, mark word edges,
// so æ, ø and å count as letters.
const ENGLISH_WORDS =
  /(?<!\p{L})(the|and|of|in|on|from|with|are|your|contains|contributors|loading|error|map|near|where|which)(?!\p{L})/giu;

function englishWords(text) {
  return text.match(ENGLISH_WORDS) ?? [];
}

// The App's own credit lines, without the basemap credit that comes from the
// OpenFreeMap style and is in English.
async function appCredits(page) {
  const [text = ''] = await page.locator('.maplibregl-ctrl-attrib-inner').allTextContents();
  return text.split(' | ').map(line => line.trim())
    .filter(line => line !== '' && !line.includes('OpenFreeMap'));
}

function isDataRequest(request) {
  return ['fetch', 'xhr'].includes(request.resourceType());
}

// Counts what the first map draws: basemap features, features from the App's own
// GeoJSON sources, and HTML markers.
function countDrawn() {
  const map = window.__checkpointMap;
  const canvas = map.getCanvas();
  const counts = { basemapFeatures: 0, dataFeatures: 0, markers: 0 };
  if (canvas.clientWidth === 0 || canvas.clientHeight === 0) return counts;
  for (const feature of map.queryRenderedFeatures()) {
    if (map.getSource(feature.source)?.type === 'geojson') counts.dataFeatures++;
    else counts.basemapFeatures++;
  }
  counts.markers = map.getContainer().querySelectorAll('.maplibregl-marker').length;
  return counts;
}

// Finds a point on screen where a tap hits something the App drew and nothing else
// covers it: an HTML marker, a projected point feature, or a point on a grid.
function findTapTarget() {
  const map = window.__checkpointMap;
  const canvas = map.getCanvas();
  const box = canvas.getBoundingClientRect();
  for (const marker of map.getContainer().querySelectorAll('.maplibregl-marker')) {
    const m = marker.getBoundingClientRect();
    const x = m.left + m.width / 2;
    const y = m.top + m.height / 2;
    if (marker.contains(document.elementFromPoint(x, y))) return { x, y };
  }
  const layers = map.getStyle().layers
    .filter(layer => map.getSource(layer.source)?.type === 'geojson')
    .map(layer => layer.id);
  const candidates = map.queryRenderedFeatures({ layers })
    .filter(feature => feature.geometry.type === 'Point')
    .map(feature => map.project(feature.geometry.coordinates));
  for (let gy = 0.5; gy < 40; gy++) {
    for (let gx = 0.5; gx < 20; gx++) {
      candidates.push({ x: (gx / 20) * box.width, y: (gy / 40) * box.height });
    }
  }
  for (const point of candidates) {
    const x = box.left + point.x;
    const y = box.top + point.y;
    if (document.elementFromPoint(x, y) === canvas &&
        map.queryRenderedFeatures([point.x, point.y], { layers }).length > 0) {
      return { x, y };
    }
  }
  return null;
}

// Waits until the App has loaded its data and the map has finished drawing.
async function openApp(page) {
  await page.addInitScript(recordMap);
  await page.goto(pathToFileURL(app).href);
  await page.waitForLoadState('networkidle');
  const created = await page.evaluate(() => window.__checkpointMap !== undefined);
  if (!created) return false;
  await page.evaluate(() => new Promise(done => {
    const map = window.__checkpointMap;
    if (map.loaded()) done(); else map.once('idle', done);
  }));
  return true;
}

test('the App works', async ({ page, isMobile }) => {
  const consoleErrors = [];
  page.on('console', message => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  page.on('pageerror', error => consoleErrors.push(error.message));

  const failedRequests = [];
  page.on('response', response => {
    if (isDataRequest(response.request()) && response.status() >= 400) {
      failedRequests.push(`${response.status()} ${response.url()}`);
    }
  });
  page.on('requestfailed', request => {
    const reason = request.failure()?.errorText ?? '';
    // MapLibre cancels tile requests it no longer needs; that is not a failure.
    if (isDataRequest(request) && !reason.includes('ERR_ABORTED')) {
      failedRequests.push(`${reason} ${request.url()}`);
    }
  });

  const created = await openApp(page);

  expect.soft(consoleErrors, 'no console errors').toEqual([]);
  expect.soft(failedRequests, 'every data request succeeds').toEqual([]);
  expect(created, 'the App creates a MapLibre map').toBe(true);

  const drawn = await page.evaluate(countDrawn);
  expect.soft(drawn.basemapFeatures, 'the map renders').toBeGreaterThan(0);
  expect.soft(drawn.dataFeatures + drawn.markers, 'at least one feature is drawn').toBeGreaterThan(0);

  expect.soft(await page.locator('html').getAttribute('lang'), 'the page is marked as Danish').toBe('da');
  const title = (await page.title()).trim();
  expect.soft(title, 'the title is Danish text').not.toBe('');
  expect.soft(englishWords(title), 'the title is Danish text').toEqual([]);
  const credits = await appCredits(page);
  expect.soft(credits, 'the App credits its data sources').not.toEqual([]);
  expect.soft(credits.flatMap(englishWords), 'the credits are Danish text').toEqual([]);

  if (!isMobile) return;

  const share = await page.evaluate(() => {
    const box = window.__checkpointMap.getContainer().getBoundingClientRect();
    return { width: box.width / innerWidth, height: box.height / innerHeight };
  });
  expect.soft(share.width, 'the map fills the screen (width share)').toBeGreaterThanOrEqual(0.99);
  expect.soft(share.height, 'the map fills the screen (height share)').toBeGreaterThanOrEqual(0.95);

  const target = await page.evaluate(findTapTarget);
  expect.soft(target, 'a tap opens a popup (no tappable feature found)').not.toBeNull();
  if (target) {
    await page.touchscreen.tap(target.x, target.y);
    await expect.soft(page.locator('.maplibregl-popup'), 'a tap opens a popup').toBeVisible();
  }
});
