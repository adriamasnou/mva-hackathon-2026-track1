'use strict';
// Minimal DOM execution checks; not a browser layout/accessibility inspection.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(process.argv[2], 'utf8');
const raw = html.match(/<script id="frozen-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code = html.match(/<script id="viewer-code">([\s\S]*?)<\/script>/)[1];
const data = JSON.parse(raw);
assert(!/<(?:script|link|img|iframe)[^>]+(?:src|href)\s*=/i.test(html), 'External resource found');
assert(!/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(/.test(code), 'Network API found');
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.dataset = {}; this.style = {}; this.attributes = {}; this.events = {}; this.value = ''; this._text = ''; }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(''); }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; this._text = ''; }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  addEventListener(name, fn) { this.events[name] = fn; }
}
const nodes = {};
for (const match of html.matchAll(/<([a-z]+)\b[^>]*\bid="([^"]+)"/g)) {
  assert(!nodes[match[2]], 'Duplicate HTML ID');
  nodes[match[2]] = new Element(match[1]);
}
nodes['frozen-data'].textContent = raw;
const document = {getElementById: id => {assert(nodes[id], `Missing ID ${id}`); return nodes[id];}, createElement: tag => new Element(tag)};
const context = vm.createContext({document});
vm.runInContext(code, context, {timeout: 5000});
const descendants = node => node.children.flatMap(c => [c, ...descendants(c)]);
const baseline = nodes.baselines.textContent;
assert.equal(nodes.cohort.children.length, 6);
assert.equal(nodes.dimension.children.length, 8);
assert.equal(nodes.baselines.children.length, 6);
assert.equal(nodes['source-sha'].textContent, 'ddf90f9eaebab874d45805f2345e05246a9fdd61a0d348259770b3c1d10854a0');
let selections = 0, categoryChecks = 0;
const distinct = new Set(), empty = new Set();
for (const cohort of Object.keys(data.methods.cohorts)) {
  for (const dimension of ['all', ...Object.keys(data.methods.dimensions)]) {
    for (const k of ['1', '5', '10']) {
      nodes.cohort.value = cohort; nodes.dimension.value = dimension; nodes.threshold.value = k;
      nodes.threshold.events.change(); selections++;
      const dims = dimension === 'all' ? Object.keys(data.methods.dimensions) : [dimension];
      assert.equal(nodes.dimensions.children.length, dims.length);
      for (const [i, section] of nodes.dimensions.children.entries()) {
        const dim = dims[i]; assert.equal(section.dataset.dimension, dim);
        const rows = descendants(section).filter(n => n.dataset.category);
        const expected = Object.entries(data.strata[cohort].source_audit_strata[dim]);
        assert.equal(rows.length, expected.length);
        for (const [j, row] of rows.entries()) {
          const [category, s] = expected[j], p = s.paired[k], cells = row.children;
          distinct.add(`${cohort}/${dim}/${category}`);
          if (!s.case_denominator) empty.add(`${cohort}/${dim}/${category}`);
          assert.equal(row.dataset.category, category);
          assert.equal(row.dataset.denominator, String(s.case_denominator));
          assert.equal(cells.length, 9);
          assert.equal(cells[1].textContent, `${s.case_denominator} / ${s.gene_denominator}`);
          for (const [arm, index] of [['original', 2], ['none', 3]]) {
            const n = s.arms[arm].top_k_counts[k];
            assert.equal(cells[index].children[0].textContent, `${n}/${s.case_denominator}`);
            const percent = s.case_denominator ? `${(100*n/s.case_denominator).toFixed(1)}%` : '— (empty)';
            assert.equal(cells[index].children[2].textContent, percent);
            const bar = cells[index].children[3].children[0];
            assert.equal(bar.style.width, `${s.case_denominator ? 100*n/s.case_denominator : 0}%`);
          }
          for (const [offset, name] of ['both_recovered','original_only','none_only','neither_recovered'].entries()) {
            assert.equal(cells[4+offset].textContent, `${p[name]}/${p.paired_case_denominator}`);
          }
          assert.equal(cells[8].textContent, `${p.discordant_pair_denominator}/${p.paired_case_denominator}`);
          categoryChecks++;
        }
        const rosters = descendants(section).filter(n => n.className === 'ids');
        assert.deepEqual(rosters.map(n => n.textContent), expected.map(([,s]) => s.case_ids.join('\n') || 'No cases in this category.'));
      }
      assert.equal(nodes.baselines.textContent, baseline, 'Filtered reference headline');
    }
  }
}
nodes.reset.events.click();
assert.equal(nodes.cohort.value, 'all_713');
assert.equal(nodes.dimension.value, 'all');
assert.equal(nodes.threshold.value, '1');
assert.equal(nodes.dimensions.children.length, 7);
assert.equal(distinct.size, 162); assert.equal(empty.size, 15);
// Explicit adverse-result fixtures: never silently omit or swap arm labels.
for (const [cohort,dim,category,k,original,none] of [
  ['all_713','all_linked_paper_completion','incomplete','5',297,300],
  ['all_713','selected_packet_category','unresolved','5',297,300],
  ['all_713','selected_genotype_status','supported','5',146,147],
]) {
  const s=data.strata[cohort].source_audit_strata[dim][category];
  assert.equal(s.arms.original.top_k_counts[k],original); assert.equal(s.arms.none.top_k_counts[k],none);
}
assert.equal(data.strata.pairs_64.baseline.arms.original.top_k_counts['1'],58);
assert.equal(data.strata.pairs_64.baseline.arms.none.top_k_counts['1'],59);
console.log(JSON.stringify({passed:true,selector_combinations:selections,rendered_category_threshold_checks:categoryChecks,distinct_categories:distinct.size,empty_categories:empty.size,adverse_fixtures:4,layout_review:'Not performed; minimal DOM execution only'}));
