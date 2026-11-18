#!/usr/bin/env node
// Usage: node check_site.mjs <site-directory>
// Exits 1 and lists every problem found in the static site's HTML files.
import {existsSync, readFileSync, readdirSync, statSync} from 'node:fs';
import {dirname, join, relative, resolve} from 'node:path';

const site = resolve(process.argv[2] ?? 'site');
if (!existsSync(join(site, 'index.html'))) {
  console.error(`No index.html in ${site}. Pass the directory GitHub Pages will publish.`);
  process.exit(1);
}

const files = dir => readdirSync(dir).flatMap(name => {
  const path = join(dir, name);
  return statSync(path).isDirectory() ? files(path) : [path];
});
const problems = [];

for (const file of files(site).filter(path => path.endsWith('.html'))) {
  const html = readFileSync(file, 'utf8');
  const where = relative(site, file);
  const report = message => problems.push(`${where}: ${message}`);

  for (const placeholder of new Set(html.match(/\{\{[A-Z_]+\}\}/g) ?? [])) report(`unfilled placeholder ${placeholder}`);
  if (!/<html[^>]*\slang="[^"]+"/.test(html)) report('missing <html lang>');
  if (!/<title>[^<]+<\/title>/.test(html)) report('missing <title>');
  if (!/<meta name="description" content="[^"]+"/.test(html)) report('missing meta description');
  for (const [, tag] of html.matchAll(/<img\b([^>]*)>/g)) if (!/\salt=/.test(tag)) report('image without alt text');
  for (const [, src] of html.matchAll(/<script\b[^>]*\ssrc="([^"]+)"/g)) {
    if (/^(?:https?:)?\/\//.test(src)) report(`third-party script ${src}`);
  }

  for (const [, url] of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    if (/^(?:[a-z][a-z0-9+.-]*:|#|\/\/)/i.test(url)) continue;
    if (url.startsWith('/')) { report(`root-absolute path ${url} breaks under https://<owner>.github.io/<repo>/`); continue; }
    const path = resolve(dirname(file), decodeURI(url.split(/[?#]/)[0]));
    if (!path.startsWith(site)) report(`link leaves the published directory: ${url}`);
    else if (!existsSync(path)) report(`missing local file ${url}`);
  }
}

if (problems.length) {
  console.error(problems.join('\n'));
  process.exit(1);
}
console.log(`Site check passed for ${relative(process.cwd(), site) || '.'}.`);
