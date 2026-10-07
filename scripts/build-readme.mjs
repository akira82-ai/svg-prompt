#!/usr/bin/env node
// 把 gallery/ 下所有条目自动拼装进 README 的生成区。
// 布局（用户定稿）：每个分类 = 一行 3 张图卡（图 + 纯标题，无链接无摘要）+ 底下直接依次列出完整咒语代码块。
// 图只出现一次；复制按钮由 GitHub 注入在顶层代码块上（table 内 pre 无按钮，平台限制）。
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

// 提示词折行：pre 无 CSS 可用（style 被剥），不折行的长句会横向撑破卡片。
// 按"显示宽度"贪心断行：中文全宽记 1，ASCII 半宽记 0.5，一行约 22 个中文位。
function wrapSpell(text, width = 22) {
  return text
    .split('\n')
    .map((para) => {
      const lines = [];
      let line = '';
      let w = 0;
      for (const ch of para) {
        const cw = /[\x20-\x7e]/.test(ch) ? 0.5 : 1;
        if (w + cw > width) {
          lines.push(line);
          line = '';
          w = 0;
        }
        line += ch;
        w += cw;
      }
      if (line) lines.push(line);
      return lines.join('\n');
    })
    .join('\n');
}

// 图卡：单行 HTML，全部左对齐（GitHub table 是 max-content 收缩布局，不满行自动靠左）
function gridCell(e) {
  const img = `gallery/${e.category}/${e.dir}/index.svg`;
  return (
    `<td width="320" valign="top">` +
    `<img src="${img}" width="300" alt="${e.title}"><br>` +
    `<strong>${e.title}</strong>` +
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

// 提示词：标题下的深色代码块文本框，全文展示；GitHub 只给顶层代码块注入
// 原生复制按钮（点击直接进剪贴板），这是平台上唯一的真·一键复制。
function spellBlock(e) {
  const fence = e.spell.includes('```') ? '````' : '```';
  return [
    `### ${e.title}`,
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
    const catAnchor = slug(name);
    toc.push(`- **[${name}](#${encodeURI(catAnchor)})** <sub>${cat} · ${entries.length} 条</sub>`);
    body.push(`## ${name}`, '');
    if (entries.length === 0) {
      body.push('*暂无条目，欢迎按 `templates/entry/` 投稿。*', '');
      continue;
    }
    body.push(gridTable(entries), '');
    for (const e of entries) body.push(spellBlock(e), '');
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
