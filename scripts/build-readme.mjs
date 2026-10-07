#!/usr/bin/env node
// 把 gallery/ 下所有条目自动拼装进 README 的生成区（缩略图画廊）。
// 布局（用户定稿）：每个分类 = 一行 3 张图卡（图 + 标题，链接到条目详情页 prompt.md）。
// 详情页 = 大图 + 提示词代码块（原生复制按钮只在独立页面的顶层代码块上，table 内必失，实测）。
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

function readEntries(category) {
  const dir = join(root, 'gallery', category);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((d) => !d.startsWith('.') && !d.startsWith('_'))
    .map((entry) => {
      const meta = JSON.parse(readFileSync(join(dir, entry, 'meta.json'), 'utf8'));
      if (meta.slug !== entry) throw new Error(`${category}/${entry}: meta.slug "${meta.slug}" 与目录名不一致`);
      return { ...meta, category, dir: entry };
    });
}

// 图卡：图 + 标题均链接到条目详情页（prompt.md 的 blob 页：大图 + 提示词代码块 + 原生复制按钮）。
// 单行 HTML，全部左对齐（GitHub table 是 max-content 收缩布局，不满行自动靠左）。
// 主 README 不放提示词正文——原生复制按钮只存在于独立页面的顶层代码块（table 内必失，实测）。
function gridCell(e) {
  const href = `gallery/${e.category}/${e.dir}/prompt.md`;
  const img = `gallery/${e.category}/${e.dir}/index.svg`;
  return (
    `<td width="320" valign="top">` +
    `<a href="${href}"><img src="${img}" width="300" alt="${e.title}"></a><br>` +
    `<a href="${href}"><strong>${e.title}</strong></a>` +
    `</td>`
  );
}

function gridTable(entries) {
  const rows = [];
  for (let i = 0; i < entries.length; i += 3) {
    rows.push('<tr>' + entries.slice(i, i + 3).map(gridCell).join('') + '</tr>');
  }
  return ['<table>', ...rows, '</table>'].join('\n');
}

function buildGallery() {
  const toc = [];
  const body = [];
  for (const [cat, name] of CATEGORIES) {
    const entries = readEntries(cat);
    const catAnchor = slug(name);
    toc.push(`- **[${name}](#${encodeURI(catAnchor)})** <sub>${cat} · ${entries.length} 条</sub>`);
    body.push(`## ${name}`, '');
    if (entries.length === 0) {
      body.push('*暂无条目，欢迎按 `templates/entry/` 投稿。*', '');
      continue;
    }
    body.push(gridTable(entries), '');
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
const count = (updated.match(/<td /g) ?? []).length;
console.log(`OK: README 已重新生成，共 ${count} 张卡片`);
