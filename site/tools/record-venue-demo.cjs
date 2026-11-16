// SPDX-License-Identifier: MIT
// Run against an OSRI preview. Requires an existing Playwright installation.
// OSRI_DEMO_OUTPUT must be outside the checkout. No outreach or policy changes.
const { chromium } = require(process.env.OSRI_PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'), path = require('path'), assert = require('assert/strict');
const base = (process.env.OSRI_SITE_URL || 'http://127.0.0.1:8797').replace(/\/$/, '');
const output = process.env.OSRI_DEMO_OUTPUT;
assert(output && path.isAbsolute(output), 'Set OSRI_DEMO_OUTPUT to an absolute scratch directory');
const cues = [
  [0, 8, 'Find a publication route. Start with author costs, research fit and the venue’s conditions.'],
  [8, 18, 'Choose a field. The default shows free author routes with core editorial standards documented.'],
  [18, 28, 'Select up to three venues. A shortlist helps compare possibilities; scope still needs checking.'],
  [28, 40, 'View the comparison. Submission cost and publication cost are separate fields.'],
  [40, 54, 'Read the cost conditions and sources. Optional open access and reader subscriptions are separate.'],
  [54, 70, 'Read AI disclosure and restrictions. Follow the venue’s official instructions; people remain responsible.'],
  [70, 80, 'Copy the directory URL to save the filters and selected venues. Reopening it restores the shortlist.'],
  [80, 90, 'Help with a short source note or a use report. The starter tasks need no coding or installation.']
];
const timestamp = seconds => `00:${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}.000`;
(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, ...(process.env.OSRI_CHROMIUM ? { executablePath: process.env.OSRI_CHROMIUM } : {}) });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce', recordVideo: { dir: output, size: { width: 1440, height: 1000 } } });
  const page = await context.newPage(), errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const video = page.video(), start = Date.now();
  const holdUntil = async second => {
    const remaining = second * 1000 - (Date.now() - start);
    if (remaining > 0) await page.waitForTimeout(remaining);
  };
  const caption = async i => {
    await page.evaluate(text => {
      let box = document.querySelector('#demo-caption');
      if (!box) {
        box = document.createElement('div'); box.id = 'demo-caption';
        box.style.cssText = 'position:fixed;z-index:9999;top:0;left:0;right:0;background:#112b42;color:white;padding:18px 38px;font:23px/1.4 sans-serif;min-height:86px;box-sizing:border-box;pointer-events:none;border-bottom:4px solid #55d1be';
        document.body.prepend(box); document.body.style.paddingTop = '104px';
      }
      box.textContent = 'OSRI walkthrough · ' + text;
    }, cues[i][2]);
  };
  await page.goto(base + '/venues/');
  assert.equal(await page.locator('.venue').count(), 57);
  await caption(0);
  await page.screenshot({ path: path.join(output, 'venue-directory-poster.jpg'), type: 'jpeg', quality: 85 });
  await holdUntil(8); await caption(1);
  await page.selectOption('#subfield', 'public-health');
  assert.equal(await page.locator('.venue').count(), 6);
  await page.locator('#filters').scrollIntoViewIfNeeded();
  await holdUntil(18); await caption(2);
  for (let i = 0; i < 3; i++) await page.locator('.venue').nth(i).locator('[data-select]').check();
  const shortlist = page.url();
  await holdUntil(28); await caption(3);
  await page.click('#show-comparison');
  assert(await page.getByRole('table').isVisible());
  await page.locator('#comparison').scrollIntoViewIfNeeded();
  await holdUntil(40); await caption(4);
  const costs = page.locator('#comparison tr').filter({ has: page.getByRole('rowheader', { name: 'Cost conditions', exact: true }) });
  await costs.locator('summary').first().click();
  await costs.scrollIntoViewIfNeeded();
  await holdUntil(54); await caption(5);
  const ai = page.locator('#comparison tr').filter({ has: page.getByRole('rowheader', { name: 'AI use and disclosure', exact: true }) });
  await ai.locator('summary').first().click();
  await ai.scrollIntoViewIfNeeded();
  await holdUntil(70); await page.goto(shortlist); await caption(6);
  assert.equal(await page.locator('[data-select]:checked').count(), 3);
  await page.click('#show-comparison');
  await holdUntil(80); await page.goto(base + '/contribute/'); await caption(7);
  await page.getByRole('link', { name: 'Choose a starter task', exact: true }).click(); await caption(7);
  assert.equal(await page.locator('main a[href*="/free-publication-directory/issues/"]').count() >= 6, true);
  await holdUntil(90);
  assert.deepEqual(errors, []);
  await context.close();
  await video.saveAs(path.join(output, 'venue-directory-demo.webm'));
  await browser.close();
  fs.writeFileSync(path.join(output, 'venue-directory-demo.vtt'), 'WEBVTT\n\n' + cues.map(([a,b,text]) => `${timestamp(a)} --> ${timestamp(b)}\n${text}\n`).join('\n'));
  const metadata = { recorded_on: '2026-11-16', source_url: base, intended_seconds: 90, kind: 'scripted browser walkthrough, not an external researcher trial', viewport: '1440x1000', captions: 'burned-in text plus optional WebVTT', browser: 'Playwright; Browser plugin not available', checks: ['57 default routes', '6 public-health routes', 'three selections', 'comparison', 'cost and AI source details', 'shortlist restored', 'six starter links', 'no page errors'], errors };
  fs.writeFileSync(path.join(output, 'recording.json'), JSON.stringify(metadata, null, 2) + '\n');
  console.log(JSON.stringify(metadata));
})().catch(e => { console.error(e); process.exit(1); });
