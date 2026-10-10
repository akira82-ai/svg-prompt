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
  ['系统图解', ['diagrams/sequence-diagram', 'diagrams/rag-pipeline', 'diagrams/agent-loop']],
  ['空间分析', ['maps/origin-destination', 'maps/service-coverage', 'maps/campus-floorplan']],
  ['科学机制', ['science/fourier-build', 'science/catenary', 'science/koch-snowflake']],
  ['AI 产品', ['ui/ai-chat-workbench', 'ui/agent-execution', 'ui/knowledge-citations']],
  ['产品设计', ['ui/data-table', 'ui/pricing-usage', 'ui/kanban-board']],
  ['品牌设计', ['branding/wordmark', 'branding/magazine-cover', 'branding/product-launch']],
  ['未来界面', ['ui/hud-interface', 'ui/dark-ops-dashboard', 'ui/wave-analyzer']],
  ['动效实验室', ['geometry/shape-morph', 'branding/brand-intro', 'backgrounds/rain-ripples']],
];

// GitHub 锚点规则：小写；删去字母/数字/空格/连字符/下划线以外的字符；空格变 -
const slug = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}\-_ ]/gu, '').trim().replace(/ +/g, '-');

// 分类内默认排序：order（策展顺序：分析任务或复杂度）优先，未设 order 的按 静态 2D → 动态 2D → 静态 3D → 动态 3D
const TIME_RANK = { static: 0, smil: 1, css: 2, js: 3 };
const SPACE_RANK = { '2d': 0, '3d': 1 };
// Slugs supply conventional English names; overrides clarify scene-specific titles.
const ENGLISH_NAMES = {
  'backgrounds/grainy-gradient': 'Grainy Gradient',
  'backgrounds/transparency-blend': 'Translucent Layers',
  'backgrounds/gradient-spheres': 'Soft Sphere Background',
  'backgrounds/spotlight-scan': 'Ambient Spotlight',
  'backgrounds/pattern-tile': 'Technical Grid',
  'backgrounds/pattern-fill': 'Geometric Pattern',
  'backgrounds/fabric': 'Woven Fabric',
  'backgrounds/carbon-fiber': 'Carbon Fiber Weave',
  'backgrounds/frosted-glass': 'Frosted Glass',
  'backgrounds/filter-materials': 'Liquid Metal',
  'backgrounds/brushed-metal': 'Brushed Metal',
  'backgrounds/gold': 'Gold Reflection',
  'backgrounds/rusted-iron': 'Weathered Metal',
  'backgrounds/marble': 'Marble Veins',
  'backgrounds/concrete': 'Concrete Texture',
  'backgrounds/kraft-paper': 'Kraft Paper',
  'backgrounds/wood-grain': 'Wood Grain',
  'backgrounds/water-drop': 'Leaf Droplets',
  'backgrounds/starry-sky': 'Procedural Starfield',
  'backgrounds/water-shimmer': 'Water Shimmer',
  'backgrounds/rain-ripples': 'Rain Ripples',
  'backgrounds/lava': 'Lava Fissures',
  'backgrounds/digital-rain': 'Digital Streams',
  'backgrounds/confetti': 'Celebration Confetti',

  'geometry/geometric-composition': 'Geometric Composition',
  'geometry/regular-polygons': 'Polygon Composition',
  'geometry/stars-and-flowers': 'Stars and Petals',
  'geometry/boolean-shapes': 'Boolean Geometry',
  'geometry/rotational-patterns': 'Radial Symmetry',
  'geometry/polar-rose': 'Polar Garden',
  'geometry/sunflower': 'Golden-angle Phyllotaxis',
  'geometry/spiral-composition': 'Spiral Composition',
  'geometry/wave-superposition': 'Wave Superposition',
  'geometry/lissajous-curves': 'Lissajous Curves',
  'geometry/flow-field': 'Flow Field',
  'geometry/voronoi-tessellation': 'Voronoi Tessellation',
  'geometry/triangulated-art': 'Triangulated Art',
  'geometry/moire-patterns': 'Moiré Patterns',
  'geometry/fractal-tree': 'Recursive Fractal Tree',
  'geometry/iso-cubes': 'Isometric Blocks',
  'geometry/shape-morph': 'Geometric Morphing',
  'geometry/blob-morph': 'Organic Morphing',

  'illustrations/human-ai': 'Human–AI Collaboration',
  'illustrations/knowledge-discovery': 'Knowledge Discovery',
  'illustrations/cloud-computing': 'Cloud Computing',
  'illustrations/data-security': 'Data Security',
  'illustrations/creative-workspace': 'Creative Workspace',
  'illustrations/robot-assistant': 'Robot Assistant',
  'illustrations/line-drawing': 'Space Exploration',
  'illustrations/hologram': 'Holographic Projection',
  'illustrations/energy-core': 'Future Energy Device',
  'illustrations/cyber-city': 'Future City',
  'illustrations/tech-campus': 'Isometric Tech Campus',
  'illustrations/sunrise-scene': 'Mountain Sunrise',
  'illustrations/snow-globe': 'Winter Snow Globe',
  'illustrations/campfire': 'Forest Campfire',
  'illustrations/sticker-pack': 'Technology Stickers',

  'icons/icon-construction': 'Icon Construction',
  'icons/icon-set': 'Outline Icons',
  'icons/solid-icons': 'Solid Icons',
  'icons/duotone-icons': 'Duotone Icons',
  'icons/small-size-icons': 'Small-size Icons',
  'icons/arrows': 'Directional Symbols',
  'icons/status-symbols': 'Status Symbols',
  'icons/file-type-icons': 'File Type Icons',
  'icons/technology-icons': 'Technology Icons',
  'icons/app-icon': 'App Icon Family',
  'icons/wayfinding-symbols': 'Wayfinding Symbols',
  'icons/symbol-morph': 'Animated State Transitions',

  'branding/brand-intro': 'Brand Intro Animation',
  'branding/typewriter': 'Brand Copy Reveal',
  'branding/circular-badge': 'Circular Brand Badge',
  'branding/packaging-dieline': 'Packaging Structure and Branding',
  'branding/social-kit': 'Social Brand Kit',
  'branding/business-card': 'Business Card Front and Back',
  'branding/stat-numbers': 'Gallery Statistics',
  'branding/comparison-vs': 'Comparison Layout',
  'branding/poster': 'Editorial Brand Poster',
  'branding/presentation-title': 'Presentation Title Slide',
  'branding/article-header': 'Article Header and Cropping',
  'branding/product-launch': 'Product Launch Poster',
  'branding/report-cover': 'Technical Report Cover',
  'branding/magazine-cover': 'Magazine Cover',
  'branding/text-on-path': 'Type on a Path',
  'branding/type-effects': 'Expressive Typography',
  'branding/editorial-grid': 'Editorial Grid Systems',
  'branding/bilingual-type': 'Bilingual Typography',
  'branding/type-scale': 'Type Scale and Hierarchy',
  'branding/brand-guidelines': 'Brand Guidelines',
  'branding/brand-palette': 'Brand Color System',
  'branding/brand-lockup': 'Brand Lockups',
  'branding/wordmark': 'Geometric Wordmark',
  'branding/logo-grid': 'Logo Construction Grid',
  'charts/pie-donut': 'Pie and Donut Charts',
  'charts/bar': 'Bar Chart', 'charts/bar-growth': 'Bar Chart Animation',
  'charts/line': 'Line Chart', 'charts/line-draw': 'Line Chart Animation',
  'charts/area': 'Area Chart', 'charts/area-expand': 'Area Chart Animation',
  'charts/scatter': 'Scatter Plot', 'charts/bubble': 'Bubble Chart',
  'charts/boxplot': 'Box Plot', 'charts/violin': 'Violin Plot',
  'charts/waterfall': 'Waterfall Chart', 'charts/interval': 'Interval Plot',
  'charts/radar': 'Radar Chart', 'charts/funnel': 'Funnel Chart',
  'charts/funnel-steps': 'Funnel Animation', 'charts/sankey': 'Sankey Diagram',
  'charts/sankey-flow': 'Sankey Flow Animation', 'charts/gantt': 'Gantt Chart',
  'charts/gantt-progress': 'Gantt Progress Animation',
  'charts/combo-dual-axis': 'Dual-Axis Combo Chart',
  'charts/ranking-lollipop': 'Lollipop Ranking',
  'charts/histogram-boxplot': 'Histogram and Box Plot',
  'charts/dumbbell': 'Dumbbell Chart', 'charts/sunburst': 'Sunburst Chart',
  'diagrams/system-architecture': 'Application Architecture',
  'diagrams/animated-architecture': 'Architecture Flow Animation',
  'diagrams/timeline-svg': 'Timeline', 'diagrams/timeline-reveal': 'Timeline Animation',
  'diagrams/process-walk': 'Process Flow Animation',
  'diagrams/network-pulse': 'Network Flow Animation',
  'diagrams/process-steps': 'Process Flow', 'diagrams/deployment': 'Deployment Diagram',
  'diagrams/entity-relationship': 'Entity Relationship Diagram',
  'maps/china-grid-map': 'Regional Tile Grid',
  'maps/choropleth': 'Choropleth Map',
  'maps/proportional-symbols': 'Proportional Symbol Map',
  'maps/point-distribution': 'Campus Point Distribution',
  'maps/spatial-density': 'Spatial Density Map',
  'maps/regional-events': 'Regional Event Map',
  'maps/map-ripple': 'Regional Event Animation',
  'maps/origin-destination': 'Origin–Destination Flows',
  'maps/route-stations': 'Routes and Transfers',
  'maps/service-coverage': 'Distance-Based Service Coverage',
  'maps/campus-floorplan': 'Floor Plan and Devices',
  'maps/spatial-comparison': 'Spatial Snapshots',
  'science/lissajous': 'Lissajous Curves',
  'science/golden-spiral': 'Fibonacci Spiral Approximation',
  'science/catenary': 'Catenary vs. Parabola',
  'science/bezier-de-casteljau': 'Bézier Construction',
  'science/sierpinski': 'Sierpiński Triangle',
  'science/koch-snowflake': 'Koch Snowflake',
  'science/fourier-square': 'Fourier Square-Wave Approximation',
  'science/fourier-build': 'Fourier Harmonic Construction',
  'science/wave-interference': 'Wave Superposition and Interference',
  'science/standing-wave': 'Standing Waves',
  'science/thin-lens': 'Thin-Lens Imaging',
  'science/orbit-gravity': 'Keplerian Orbit',
  'science/solar-system': 'Orbital Period Comparison',
  'science/three-d': '3D Projection Comparison',
  'science/topology-deform': 'Möbius Strip Construction',
  'ui/buttons': 'Button States', 'ui/toggle': 'Toggle States',
  'ui/toggle-animated': 'Toggle Transitions',
  'ui/checkbox-radio': 'Checkboxes and Radio Buttons',
  'ui/input-states': 'Input and Validation', 'ui/dropdown': 'Dropdown Selection',
  'ui/chips': 'Tags and Filter Chips', 'ui/avatar-badge': 'Avatars and Badges',
  'ui/elevation': 'Cards and Elevation', 'ui/date-range': 'Date Range Picker',
  'ui/file-upload': 'File Upload States', 'ui/login-verification': 'Login and Verification',
  'ui/tabs': 'Tabs and Segmented Navigation', 'ui/pagination': 'Pagination',
  'ui/tooltip': 'Tooltips', 'ui/breadcrumb': 'Breadcrumb Navigation',
  'ui/global-search': 'Global Search', 'ui/command-palette': 'Command Palette',
  'ui/filter-sort': 'Filtering and Sorting',
  'ui/settings-preferences': 'Settings and Preferences',
  'ui/help-feedback': 'Help and Feedback', 'ui/alerts': 'Status Alerts',
  'ui/alert-blink': 'Alert Emphasis', 'ui/spinners': 'Loading Indicators',
  'ui/skeleton-shimmer': 'Skeleton Loading', 'ui/typing-indicator': 'Typing Indicator',
  'ui/audio-wave': 'Voice Input States', 'ui/status-patrol': 'Service Status Inspection',
  'ui/task-stepper': 'Task Progress Steps', 'ui/request-retry': 'Request and Retry States',
  'ui/empty-error': 'Empty and Error States', 'ui/modal-confirm': 'Confirmation Dialog',
  'ui/product-onboarding': 'Product Onboarding',
  'ui/progress-slider': 'Progress Bars and Sliders', 'ui/kpi-cards': 'KPI Cards',
  'ui/number-roll': 'Metric Value Transitions', 'ui/data-table': 'Data Table',
  'ui/detail-drawer': 'Detail Drawer', 'ui/pricing-usage': 'Plans and Usage',
  'ui/ai-chat-workbench': 'AI Chat Workspace',
  'ui/model-parameters': 'Model and Parameter Selection',
  'ui/agent-execution': 'Agent Execution',
  'ui/knowledge-citations': 'Knowledge Search and Citations',
  'ui/generation-compare': 'Generation Comparison', 'ui/todo-today': 'Daily Tasks',
  'ui/chat-messenger': 'Team Chat', 'ui/ecommerce-home': 'Product Catalog',
  'ui/kanban-board': 'Task Kanban', 'ui/members-permissions': 'Members and Permissions',
  'ui/checkout-payment': 'Checkout and Payment',
  'ui/bi-dashboard': 'Business Analytics Workspace',
  'ui/dashboard': 'Business Analytics Entrance',
  'ui/dark-ops-dashboard': 'Operations Monitoring Workspace',
  'ui/live-ops-dashboard': 'Operations Inspection Animation',
  'ui/fitness-dashboard': 'Activity and Training', 'ui/music-player': 'Music Workspace',
  'ui/hud-interface': 'HUD Navigation Concept', 'ui/wave-analyzer': 'Waveform Analyzer',


};
const ENGLISH_WORDS = { ai: 'AI', bi: 'BI', kpi: 'KPI', hud: 'HUD', rag: 'RAG', svg: 'SVG', vs: 'vs.' };
function englishName(e) {
  return ENGLISH_NAMES[`${e.category}/${e.dir}`] ?? e.dir.split('-')
    .map((word) => ENGLISH_WORDS[word] ?? word[0].toUpperCase() + word.slice(1)).join(' ');
}
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
  const english = englishName(e);
  return (
    `<td width="350" align="center" valign="top">` +
    `<a href="${href}"><img src="${img}" width="336" alt="${e.title}"></a><br>` +
    `<a href="${href}"><strong>${e.title}</strong><br><sub>${english}</sub></a>` +
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
  body.push('## 精选与专题', '', '按用途浏览下方分类；卡片显示中英文名称。专题中的作品同时保留在各自主分类中。', '');
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
