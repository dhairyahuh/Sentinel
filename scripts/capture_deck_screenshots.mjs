import puppeteer from 'puppeteer-core';
import path from 'path';
import fs from 'fs';

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE_URL = 'https://sentinel-sand-two.vercel.app';
const OUT_DIR = path.resolve('docs/media');

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function capture() {
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: true,
    defaultViewport: {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2,
    },
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const page = await browser.newPage();

  // 1. Console
  console.log('Capturing Console...');
  await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('#tour-stream', { timeout: 10000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(OUT_DIR, 'screen_console.png') });

  // 2. Inspector
  console.log('Capturing Inspector...');
  // Click on the first row in the stream table to open the inspector slide-over
  const rows = await page.$$('tbody tr');
  if (rows.length > 0) {
    await rows[0].click();
    await page.waitForSelector('aside[role="dialog"]', { timeout: 10000 });
    await new Promise(r => setTimeout(r, 1500));
    await page.screenshot({ path: path.join(OUT_DIR, 'screen_inspector.png') });
  }

  // 3. Identify / Crime Pattern Map
  console.log('Capturing Map (/identify)...');
  await page.goto(`${BASE_URL}/identify`, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('#tour-killchain', { timeout: 10000 });
  // Click a cell to show pattern detail
  const cells = await page.$$('button[title]');
  if (cells.length > 5) {
    await cells[3].click();
  }
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, 'screen_identify.png') });

  // 4. Defend
  console.log('Capturing Defend (/defend)...');
  await page.goto(`${BASE_URL}/defend`, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('#tour-operating', { timeout: 10000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(OUT_DIR, 'screen_defend.png') });

  // 5. Loop / Evolve
  console.log('Capturing Loop (/loop)...');
  await page.goto(`${BASE_URL}/loop`, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('#tour-armsrace', { timeout: 10000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(OUT_DIR, 'screen_loop.png') });

  await browser.close();
  console.log('All screenshots captured successfully in 2x resolution!');
}

capture().catch(err => {
  console.error('Error capturing screenshots:', err);
  process.exit(1);
});
