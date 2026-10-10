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

// 按作品用途展示；动效和空间形式属于独立标签。
const CATEGORIES = [
  ['charts', '数据图表'],
  ['diagrams', '流程与架构'],
  ['maps', '地图与空间'],
  ['science', '科学与原理'],
  ['ui', '界面与组件'],
  ['branding', '品牌与排版'],
  ['icons', '图标与符号'],
  ['illustrations', '插画与场景'],
  ['geometry', '几何与生成艺术'],
  ['backgrounds', '背景与材质'],
];

// 专题只引用原作品，不复制条目或改变主分类。
const COLLECTIONS = [
  ['精选作品', ['diagrams/system-architecture', 'science/bezier-de-casteljau', 'illustrations/cyber-city']],
  ['数据分析', ['charts/sankey', 'charts/matrix-heatmap', 'charts/interval']],
  ['系统图解', ['diagrams/animated-architecture', 'diagrams/data-pipeline', 'diagrams/network-pulse']],
  ['科学机制', ['science/fourier-build', 'science/catenary', 'science/koch-snowflake']],
  ['未来界面', ['ui/hud-interface', 'ui/dark-ops-dashboard', 'ui/wave-analyzer']],
  ['动效实验室', ['geometry/shape-morph', 'branding/letter-morph', 'backgrounds/rain-ripples']],
];

// GitHub 锚点规则：小写；删去字母/数字/空格/连字符/下划线以外的字符；空格变 -
const slug = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}\-_ ]/gu, '').trim().replace(/ +/g, '-');

// 分类内默认排序：order（策展顺序：分析任务或复杂度）优先，未设 order 的按 静态 2D → 动态 2D → 静态 3D → 动态 3D
const TIME_RANK = { static: 0, smil: 1, css: 2, js: 3 };
const SPACE_RANK = { '2d': 0, '3d': 1 };
const TIME_LABEL = { static: '静态', smil: 'SMIL 动效', css: 'CSS 动效', js: 'JS 动效' };
const byOrderThenTime = (a, b) =>
  (a.order ?? 999) - (b.order ?? 999) ||
  (TIME_RANK[a.time] ?? 9) - (TIME_RANK[b.time] ?? 9) ||
  (SPACE_RANK[a.space] ?? 9) - (SPACE_RANK[b.space] ?? 9);

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
  const tag = `<code>${TIME_LABEL[e.time] ?? e.time}</code> <code>${(e.space || '2d').toUpperCase()}</code>`;
  return (
    `<td width="350" align="center" valign="top">` +
    `<a href="${href}"><img src="${img}" width="336" alt="${e.title}"></a><br>` +
    `<a href="${href}"><strong>${e.title}</strong></a> ${tag}` +
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
  const all = CATEGORIES.flatMap(([cat]) => readEntries(cat));
  const known = new Set(CATEGORIES.map(([cat]) => cat));
  for (const dir of readdirSync(join(root, 'gallery'), { withFileTypes: true })) {
    if (dir.isDirectory() && !known.has(dir.name)) throw new Error(`未注册分类：${dir.name}`);
  }
  toc.push('- **[精选与专题](#精选与专题)** <sub>跨分类策展入口</sub>');
  body.push('## 精选与专题', '', '按用途浏览下方分类；静态 / 动效、2D / 3D 及具体技术见卡片与条目元数据。专题中的作品同时保留在各自主分类中。', '');
  for (const [name, paths] of COLLECTIONS) {
    const entries = paths.map((path) => {
      const entry = all.find((e) => `${e.category}/${e.dir}` === path);
      if (!entry) throw new Error(`专题「${name}」引用不存在的条目：${path}`);
      return entry;
    });
    body.push(`### ${name}`, '', gridTable(entries), '');
  }
  for (const [cat, name] of CATEGORIES) {
    const entries = all.filter((e) => e.category === cat).sort(byOrderThenTime);
    const catAnchor = slug(name);
    toc.push(`- **[${name}](#${encodeURI(catAnchor)})** <sub>${cat} · ${entries.length} 条</sub>`);
    const about = readFileSync(join(root, 'gallery', cat, '_about.md'), 'utf8');
    const description = about.split('\n\n')[1];
    if (!description) throw new Error(`${cat}/_about.md 缺少分类说明`);
    body.push(`## ${name}`, '', description, '');
    if (entries.length === 0) {
      body.push('*暂无条目，欢迎按 `templates/entry/` 投稿。*', '');
      continue;
    }
    body.push(gridTable(entries), '');
  }
  return { toc: toc.join('\n'), body: body.join('\n').replace(/\n+$/, '\n'), count: all.length };
}

const readme = readFileSync(readmePath, 'utf8');
const START = '<!-- GALLERY:START -->';
const END = '<!-- GALLERY:END -->';
if (!readme.includes(START) || !readme.includes(END)) {
  throw new Error('README.md 缺少 GALLERY:START / GALLERY:END 标记');
}
const { toc, body, count } = buildGallery();
const updated = readme.replace(
  new RegExp(`${START}[\\s\\S]*${END}`),
  `${START}\n${toc}\n\n${body}${END}`
);
writeFileSync(readmePath, updated);
console.log(`OK: README 已重新生成，共 ${count} 个作品，${COLLECTIONS.length} 个专题`);
