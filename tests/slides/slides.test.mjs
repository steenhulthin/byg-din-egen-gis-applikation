// Tests the Session slides (index.html) from the outside in headless Chromium.
import { after, before, test } from 'node:test';
import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import jsQR from 'jsqr';

const slidesUrl = new URL('../../index.html', import.meta.url).href;
const PAGES = 'https://steenhulthin.github.io/byg-din-egen-gis-applikation/';

let browser;
before(async () => { browser = await chromium.launch(); });
after(async () => { await browser?.close(); });

// Opens slide number in a new page, runs check on it and closes the page again.
async function onSlide(number, check, viewport = { width: 1280, height: 720 }) {
  const page = await browser.newPage({ viewport });
  try {
    await page.goto(`${slidesUrl}#${number}`);
    return await check(page);
  } finally {
    await page.close();
  }
}

// Screenshots the visible QR code and returns the text it decodes to, or null.
async function decodeQr(page) {
  const qr = page.getByRole('img', { name: /QR-kode/ }).filter({ visible: true });
  const png = await qr.screenshot();
  const pixels = await page.evaluate(async (dataUrl) => {
    const image = new Image();
    image.src = dataUrl;
    await image.decode();
    const canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    const { data, width, height } = context.getImageData(0, 0, image.width, image.height);
    return { data: Array.from(data), width, height };
  }, `data:image/png;base64,${png.toString('base64')}`);
  return jsQR(Uint8ClampedArray.from(pixels.data), pixels.width, pixels.height)?.data ?? null;
}

test('the QR code on slide 6 leads to the Participant guide', async () => {
  assert.equal(await onSlide(6, decodeQr), `${PAGES}deltag.html`);
});

test('the QR code on slide 5 leads to the Backup app until a demo App is entered', async () => {
  assert.equal(await onSlide(5, decodeQr), `${PAGES}backup/`);
});

test('the QR code on slide 5 leads to the demo App entered on stage', async () => {
  const decoded = await onSlide(5, async (page) => {
    const address = page.getByLabel('Demo-appens adresse');
    await address.fill('kortdage-demo.github.io/legepladser/');
    await address.press('Enter');
    return decodeQr(page);
  });
  assert.equal(decoded, 'https://kortdage-demo.github.io/legepladser/');
});

// Lists slide text that is too small to read on a projector or reaches outside the screen.
async function projectorProblems(page) {
  return page.evaluate(() => {
    const slide = [...document.querySelectorAll('section')].find((s) => s.checkVisibility());
    const problems = [];
    for (const element of slide.querySelectorAll('h1, h2, p, li, dt, dd, figure')) {
      const box = element.getBoundingClientRect();
      const name = `"${element.textContent.trim().slice(0, 40)}"`;
      if (box.left < 0 || box.top < 0 || box.right > innerWidth || box.bottom > innerHeight) {
        problems.push(`${name} reaches outside the screen`);
      }
      const size = parseFloat(getComputedStyle(element).fontSize);
      if (element.tagName !== 'FIGURE' && size < 24) problems.push(`${name} is ${size}px`);
    }
    return problems;
  });
}

for (const viewport of [{ width: 1920, height: 1080 }, { width: 1280, height: 720 }, { width: 1024, height: 768 }]) {
  test(`every slide fits a ${viewport.width}x${viewport.height} projector with text of at least 24px`, async () => {
    const problems = [];
    for (let number = 1; number <= 6; number++) {
      const found = await onSlide(number, projectorProblems, viewport);
      problems.push(...found.map((problem) => `slide ${number}: ${problem}`));
    }
    assert.deepEqual(problems, []);
  });
}
