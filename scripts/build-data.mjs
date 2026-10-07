#!/usr/bin/env node
// 扫描 gallery/<category>/<entry>/meta.json，聚合生成 site/data.js（单页筛选站的数据源）。
// 用法：node scripts/build-data.mjs
import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const galleryDir = join(root, 'gallery');
const entries = [];

for (const category of readdirSync(galleryDir).filter(d => !d.startsWith('.') && !d.startsWith('_'))) {
  const catDir = join(galleryDir, category);
  for (const entry of readdirSync(catDir).filter(d => !d.startsWith('.') && !d.startsWith('_'))) {
    const metaPath = join(catDir, entry, 'meta.json');
    if (!existsSync(metaPath)) continue;
    const meta = JSON.parse(readFileSync(metaPath, 'utf8'));
    if (meta.slug !== entry) {
      console.warn(`⚠ ${category}/${entry}: meta.slug "${meta.slug}" 与目录名不一致`);
    }
    entries.push({ ...meta, category, path: `gallery/${category}/${entry}` });
  }
}

writeFileSync(
  join(root, 'site', 'data.js'),
  `// 由 scripts/build-data.mjs 自动生成，勿手改\nwindow.SVG_PROMPT_DATA = ${JSON.stringify(entries, null, 2)};\n`
);
console.log(`OK: ${entries.length} entries → site/data.js`);
