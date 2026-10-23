#!/usr/bin/env node
// Execute this repository's shipped search function with a minimal DOM adapter.
// This checks JavaScript behavior and emitted text, not browser layout/usability.
const fs = require('node:fs'), vm = require('node:vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const queries = JSON.parse(fs.readFileSync(0, 'utf8'));
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)];
const dataset = scripts.filter(s => /id="dataset"/.test(s[1]));
const executable = scripts.filter(s => !/application\/json/.test(s[1]));
if (dataset.length !== 1 || executable.length !== 1) throw Error('Unexpected script structure');
class Element {
  constructor(tag = '') { this.tag = tag; this.textContent = ''; this.children = []; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  addEventListener() {}
}
const ids = Object.fromEntries(['dataset','stats','dates','results','status','form','query'].map(id => [id,new Element()]));
ids.dataset.textContent = dataset[0][2];
const context = vm.createContext({window:{},document:{
  getElementById: id => { if (!ids[id]) throw Error('Unknown element: '+id); return ids[id]; },
  createElement: tag => new Element(tag), querySelectorAll: () => []
}});
vm.runInContext(executable[0][2],context,{timeout:5000});
function texts(el) { return [String(el.textContent),...el.children.flatMap(texts)]; }
function visibleTexts(el) { return el.tag === 'details' ? [] : [String(el.textContent),...el.children.flatMap(visibleTexts)]; }
function visibleGeneGroups(el) {
  if (el.tag === 'details') return [];
  if (el.className === 'gene-group') return [{
    gene: String(el.children.find(child => child.tag === 'h3')?.textContent || ''),
    labels: el.children.filter(child => child.className === 'gene-roles').flatMap(list => list.children.map(item => String(item.textContent)))
  }];
  return el.children.flatMap(visibleGeneGroups);
}
const results = queries.map(query => {
  context.queryForAudit = query;
  const rows = vm.runInContext('window.pgtmSearch(queryForAudit)',context,{timeout:5000});
  return {query,rows,status:ids.status.textContent,cards:ids.results.children.map(texts),visibleCards:ids.results.children.map(visibleTexts),geneGroups:ids.results.children.map(visibleGeneGroups)};
});
process.stdout.write(JSON.stringify(results));
