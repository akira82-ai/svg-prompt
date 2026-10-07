#!/usr/bin/env node
// 把 gallery/ 下所有条目自动拼装进 README 的生成区。
// 布局：每个分类 = 4 列卡片网格（图 + 标题 + 咒语摘要）+ 详情区（图 + 完整咒语代码块）。
// 卡片锚点跳详情；复制按钮只存在于顶层代码块（GitHub 平台限制，实测 table 内 pre 无按钮）。
// README 中 <!-- GALLERY:START --> 与 <!-- GALLERY:END --> 之间的内容由本脚本维护，勿手改。
// 用法：node scripts/build-readme.mjs
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const readmePath = join(root, 'README.md');

// 展示顺序 = 难度进阶顺序，与 gallery/ 目录名一一对应
const CATEGORIES = [
  ['basics', '教学基础'],
  ['ui', 'UI 组件'],
  ['branding', '品牌排版'],
  ['charts', '图表报表'],
  ['infographics', '信息可视化'],
  ['materials', '实物模拟'],
  ['motion', '动效艺术'],
  ['math', '高级数学'],
];

// GitHub 锚点规则：小写；删去字母/数字/空格/连字符/下划线以外的字符；空格变 -
const slug = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}\-_ ]/gu, '').trim().replace(/ +/g, '-');
const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// 重复标题的锚点加 -2/-3 后缀（与 GitHub 的重复标题消歧一致）
const usedAnchors = new Map();
function anchorOf(title) {
  const base = slug(title) || 'entry';
  const n = (usedAnchors.get(base) ?? 0) + 1;
  usedAnchors.set(base, n);
  return n === 1 ? base : `${base}-${n}`;
}

function readEntries(category) {
  const dir = join(root, 'gallery', category);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((d) => !d.startsWith('.') && !d.startsWith('_'))
    .map((entry) => {
      const meta = JSON.parse(readFileSync(join(dir, entry, 'meta.json'), 'utf8'));
      if (meta.slug !== entry) throw new Error(`${category}/${entry}: meta.slug "${meta.slug}" 与目录名不一致`);
      const promptMd = readFileSync(join(dir, entry, 'prompt.md'), 'utf8');
      const m = promptMd.match(/```\w*\n([\s\S]*?)```/); // prompt.md 的第一个代码块 = 咒语
      return { ...meta, category, dir: entry, spell: m ? m[1].trim() : '（待补充）' };
    });
}

// 摘要：压平空白取前 60 字，超出加省略号（约等于 245px 卡片里的 3 行）
function summarize(spell) {
  const flat = spell.replace(/\s+/g, ' ').trim();
  return flat.length > 60 ? flat.slice(0, 60) + '…' : flat;
}

function gridCell(e) {
  const href = `#${encodeURI(e.anchor)}`;
  const img = `gallery/${e.category}/${e.dir}/index.svg`;
  // td 内容保持单行 HTML：GitHub 表格单元格里只适合简单内容，多块级结构会撑破布局
  // 全部左对齐（不设 align）：一行不满 4 卡时其余留白，卡片依旧靠左
  return (
    `<td width="260" valign="top">` +
    `<a href="${href}"><img src="${img}" width="220" alt="${e.title}"></a><br>` +
    `<strong><a href="${href}">${e.title}</a></strong><br>` +
    `<sub>${escapeHtml(summarize(e.spell))}</sub>` +
    `</td>`
  );
}

function gridTable(entries) {
  const rows = [];
  for (let i = 0; i < entries.length; i += 4) {
    rows.push('<tr>' + entries.slice(i, i + 4).map(gridCell).join('') + '</tr>');
  }
  return ['<table>', ...rows, '</table>'].join('\n');
}

function detailSection(e) {
  const img = `gallery/${e.category}/${e.dir}/index.svg`;
  // 咒语本身含 ``` 时换四反引号围栏，避免提前闭合
  const fence = e.spell.includes('```') ? '````' : '```';
  return [
    `### ${e.title}`,
    '',
    `<img src="${img}" width="400" alt="${e.title}">`,
    '',
    `${fence}text`,
    e.spell,
    `${fence}`,
    '',
  ].join('\n');
}

function buildGallery() {
  const toc = [];
  const body = [];
  for (const [cat, name] of CATEGORIES) {
    const entries = readEntries(cat);
    const catAnchor = anchorOf(name);
    toc.push(`- **[${name}](#${encodeURI(catAnchor)})** <sub>${cat} · ${entries.length} 条</sub>`);
    for (const e of entries) {
      e.anchor = anchorOf(e.title);
      toc.push(`  - [${e.title}](#${encodeURI(e.anchor)})`);
    }
    body.push(`## ${name}`, '');
    if (entries.length === 0) {
      body.push('*暂无条目，欢迎按 `templates/entry/` 投稿。*', '');
      continue;
    }
    body.push(gridTable(entries), '');
    for (const e of entries) body.push(detailSection(e), '');
  }
  return { toc: toc.join('\n'), body: body.join('\n').replace(/\n+$/, '\n') };
}

const readme = readFileSync(readmePath, 'utf8');
const START = '<!-- GALLERY:START -->';
const END = '<!-- GALLERY:END -->';
if (!readme.includes(START) || !readme.includes(END)) {
  throw new Error('README.md 缺少 GALLERY:START / GALLERY:END 标记');
}
const { toc, body } = buildGallery();
const updated = readme.replace(
  new RegExp(`${START}[\\s\\S]*${END}`),
  `${START}\n${toc}\n\n${body}${END}`
);
writeFileSync(readmePath, updated);
const count = (updated.match(/^### /gm) ?? []).length;
console.log(`OK: README 已重新生成，共 ${count} 个条目`);
