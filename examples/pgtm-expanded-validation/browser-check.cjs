#!/usr/bin/env node
// Render the local navigator in an isolated browser profile. No live sources or uploads.
const fs = require('node:fs'), path = require('node:path'), assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url'), crypto = require('node:crypto');
const {chromium} = require(process.env.PGTM_PLAYWRIGHT_PATH || 'playwright');
const repo = path.resolve(__dirname, '../..');
const html = path.join(repo, 'submissions/pgtm-navigator.html');
const resultPath = path.join(repo, 'submissions/pgtm-expanded-validation.json');
const evaluated = JSON.parse(fs.readFileSync(resultPath, 'utf8'));
const digest = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const viewports = [{width: 1440, height: 1000}, {width: 390, height: 844}, {width: 320, height: 740}];
const queries = ['CFTR', 'QDPR', 'BRCA1', 'BRCA2', 'CHEK2', 'HBB'];
assert.equal(evaluated.input_sha256['pgtm-navigator.html'], digest(html), 'Evaluation must cover this exact navigator');

(async () => {
  const browser = await chromium.launch({headless: true,
    ...(process.env.PGTM_CHROMIUM_PATH ? {executablePath: process.env.PGTM_CHROMIUM_PATH} : {})});
  const checks = [], errors = [], blockedRequests = [];
  try {
    const context = await browser.newContext();
    await context.route('**/*', route => {
      if (/^https?:/.test(route.request().url())) {
        blockedRequests.push(route.request().url()); return route.abort();
      }
      return route.continue();
    });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(String(error)));
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.goto(pathToFileURL(html).href);
      for (const query of queries) {
        await page.locator('#query').fill(query);
        await page.locator('#form button').click();
        const wanted = evaluated.raw_query_results.find(item => item.query === query);
        assert(wanted, 'Query must have a completed frozen source evaluation');
        const rendered = await page.locator('#results .card').evaluateAll(cards => cards.map(card => ({
          condition: card.querySelector('h2').textContent,
          status: card.querySelector('.tag').textContent,
          groups: [...card.querySelectorAll('.gene-group')].map(group => ({
            gene: group.querySelector('h3').textContent,
            labels: [...group.querySelectorAll('.gene-roles li')].map(item => item.textContent)
          })),
          visibleText: card.innerText,
          raw: JSON.parse(card.querySelector('pre').textContent),
          closed: !card.querySelector('details').open,
          rolesVisible: [...card.querySelectorAll('.gene-roles li')].every(item => {
            const style = getComputedStyle(item), bounds = item.getBoundingClientRect();
            return !item.closest('details') && style.display !== 'none' && style.visibility === 'visible'
              && Number(style.opacity) > 0 && bounds.width > 0 && bounds.height > 0;
          }),
          clipped: [card, ...card.querySelectorAll('.gene-group,.gene-roles,li,h2,h3')]
            .some(item => item.scrollWidth > item.clientWidth + 1)
        })));
        assert.equal(rendered.length, wanted.rows.length);
        for (const [index, card] of rendered.entries()) {
          const row = wanted.rows[index];
          assert.equal(card.condition, row.condition);
          assert.equal(card.status, 'Condition status: ' + row.hfea_status);
          assert.deepEqual(card.groups, wanted.geneGroups[index]);
          assert.deepEqual(card.raw, JSON.parse(row.gene_evidence));
          assert(card.closed && card.rolesVisible && !card.clipped);
          assert(!card.visibleText.includes('association_type') && !card.visibleText.includes('field:'));
        }
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
        assert(!overflow, 'Horizontal viewport overflow');
        checks.push({viewport, query, cards: rendered.length, horizontalOverflow: overflow,
          groupedRolesVisible: true, rawEvidenceUnchanged: true, status: 'PASS'});
        if (process.env.PGTM_QA_SCREENSHOT_DIR && query === 'CFTR' && viewport.width !== 320) {
          fs.mkdirSync(process.env.PGTM_QA_SCREENSHOT_DIR, {recursive: true});
          await page.locator('#results').screenshot({path: path.join(process.env.PGTM_QA_SCREENSHOT_DIR, `cftr-${viewport.width}.png`)});
        }
      }
      const details = page.locator('#results .card').first().locator('details');
      await details.locator('summary').click();
      assert.equal(await details.getAttribute('open'), '');
      assert(await details.locator('pre').isVisible());
    }
    assert.deepEqual(errors, []);
    assert.deepEqual(blockedRequests, []);
    const receipt = {executed_utc: new Date().toISOString(), browser: browser.version(),
      navigator_sha256: digest(html), script_sha256: digest(__filename), checks,
      javascriptErrors: errors, attemptedHttpRequests: blockedRequests, rawJsonExpandsAtAllViewports: true,
      status: 'PASS', limits: 'Local headless Chromium rendering of selected source-reviewed queries. Not a physical-device, cross-browser, accessibility, usability or clinical validation. Final presentation captures are separate.'};
    fs.writeFileSync(path.join(__dirname, 'browser-check-results.json'), JSON.stringify(receipt, null, 2) + '\n');
    console.log(JSON.stringify({status: receipt.status, browser: receipt.browser, checks: checks.length}));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
