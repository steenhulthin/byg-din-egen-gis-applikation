// Render the session slides (index.html) to a PDF, one slide per landscape A4 page.
// Usage: node scripts/slides-til-pdf.mjs [output.pdf]
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const output = process.argv[2] ?? join(root, 'slides.pdf');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto('file://' + join(root, 'index.html'));
await page.waitForLoadState('load');

// Wait for the inlined QR generator to draw the codes.
await page.waitForFunction(() => document.querySelectorAll('.qr canvas, .qr img, .qr svg').length >= 2);

// Print stylesheet: one slide per page, no navigation chrome.
await page.addStyleTag({
  content: `
    html, body { height: auto !important; overflow: visible !important; }
    .fod, .fremdrift { display: none !important; }
    .slide {
      display: flex !important;
      position: static !important;
      height: 178mm !important;
      page-break-after: always !important;
      break-after: page !important;
    }
    .slide:last-of-type { page-break-after: auto !important; }
  `,
});

await page.pdf({
  path: output,
  format: 'A4',
  landscape: true,
  printBackground: true,
  margin: { top: '8mm', bottom: '8mm', left: '10mm', right: '10mm' },
});

await browser.close();
console.log('Wrote ' + output);
