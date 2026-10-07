#!/usr/bin/env node
// 把 gallery/ 下所有条目（作品图 + 咒语 + 五维标签）自动拼装进 README 的生成区。
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

const TIME_LABEL = { static: '静态', smil: 'SMIL 动效', css: 'CSS 动效', js: 'JS 动效' };

// GitHub 锚点规则：小写；删去字母/数字/空格/连字符/下划线以外的字符；空格变 -
const slug = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}\-_ ]/gu, '').trim().replace(/ +/g, '-');
const anchor = (s) => '#' + encodeURI(slug(s));

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

function entrySection(e) {
  const tags = [
    `难度 L${e.difficulty}`,
    `咒语 L${e.spellLevel}`,
    TIME_LABEL[e.time] ?? e.time,
    e.space,
    ...e.tech,
  ].map((t) => `\`${t}\``).join(' · ');
  return [
    `### ${e.title}`,
    '',
    tags,
    '',
    `<img src="gallery/${e.category}/${e.dir}/index.svg" width="600" alt="${e.title}">`,
    '',
    '**咒语**（代码块右上角可一键复制）：',
    '',
    '```text',
    e.spell,
    '```',
  ].join('\n');
}

function buildGallery() {
  const toc = [];
  const body = [];
  for (const [cat, name] of CATEGORIES) {
    const entries = readEntries(cat);
    toc.push(`- **[${name}](${anchor(name)})** <sub>${cat} · ${entries.length} 条</sub>`);
    for (const e of entries) {
      toc.push(`  - [${e.title}](${anchor(e.title)}) \`L${e.difficulty}\``);
    }
    body.push(`## ${name}`, '');
    if (entries.length === 0) {
      body.push('*暂无条目，欢迎按 `templates/entry/` 投稿。*', '');
    } else {
      for (const e of entries) {
        body.push(entrySection(e), '', '---', '');
      }
    }
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
