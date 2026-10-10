# 贡献指南

## 仓库结构

```
svg-prompt/
├── gallery/                      # ★ 内容源文件（一图一目录，README 由这里生成）
│   └── <category>/<entry-slug>/  #   十大用途分类，英文 kebab-case 条目名
│       ├── index.svg             #     作品本体，浏览器可直接打开
│       ├── prompt.md             #     条目详情页：标题 + 分类入口 + 大图 + 提示词代码块
│       └── meta.json             #     分类与时空标签（机器可读）
├── templates/entry/              # 新条目模板：复制这个目录开新条目
├── schema/entry.schema.json      # meta.json 的校验规则
├── scripts/build-readme.mjs      # 扫描 gallery → 生成 README 缩略图画廊
└── archive/demos/                # 立项前的 14 个技术验证 Demo（存档，非图鉴条目）
```

**两级页面结构**：主 README = 缩略图画廊（每卡链接到条目详情页）；条目详情页 = `prompt.md` 的 GitHub 文件页（标题 + 标签 + 分类入口 + 720px 大图 + 提示词代码块，无多余小节标题）。原生复制按钮只存在于详情页的顶层代码块——这是 GitHub 平台规则（table/折叠内必失，实测），所以主页不放提示词正文。

**为什么一图一目录，而不是把内容直接写进 README？** README 是生成物（`<!-- GALLERY:START/END -->` 之间由脚本维护），内容源文件才是唯一事实。目录化让每个投稿是纯增量 PR、详情页与作品同目录自包含——人永远不手写长 README。

## 三件套约定

| 文件 | 要求 |
|---|---|
| `index.svg` | 作品本体；浏览器直接打开即渲染；动效条目优先 SMIL / CSS 实现（零 JS） |
| `prompt.md` | **详情页结构**：`# 中文标题` + `静态`/`动效`/`2D`/`3D` 标签 → 分类链接 `../_about.md` → `<img src="index.svg" width="720">` → 提示词代码块（不加"提示词"等小节标题）；保持这个结构 |
| `prompt.md` 内的提示词 | **多行结构化书写**（不要挤成一行）：首行一句话意图，`-` 列表逐条列结构与风格要求，可替换部分用 `{花括号}` 标注 |
| `meta.json` | 字段见 [schema/entry.schema.json](schema/entry.schema.json)；`slug` 必须与目录名一致；`order`（可选）控制分类内展示位置——在同一用途下编号；数据图表按**分析任务**排列、动画变体紧随静态图，其他分类通常按组件 → 组合 → 完整原型排列，未设时排在已编号条目之后 |

## 分类与时空标签

| 维度 | 字段 | 取值 |
|---|---|---|
| 空间 | `space` | `2d` / `3d` |
| 时间 | `time` | `static` / `smil` / `css` / `js` |
| 主分类 | （所在目录） | 十类之一，不重复存储 |

| 目录 | 主分类 |
|---|---|
| `charts` | 数据图表 |
| `diagrams` | 流程与架构 |
| `maps` | 地图与空间 |
| `science` | 科学与原理 |
| `ui` | 界面与组件 |
| `branding` | 品牌与排版 |
| `icons` | 图标与符号 |
| `illustrations` | 插画与场景 |
| `geometry` | 几何与生成艺术 |
| `backgrounds` | 背景与材质 |

每张图按主要用途只归一个目录，动态作品分布于各分类，不能因为使用动画就单独归类。科学解释与装饰特效按用途区分；抽象地图、虚构数据、简化模型须在作品或提示词中说明。

收录标准见各分类目录的 `_about.md`。首页精选与专题由 `scripts/build-readme.mjs` 引用现有条目，不复制作品；调整目录时同步检查专题引用。技术、时间和空间仍使用现有字段，不把风格或主题混入技术标签。

## 投稿流程

1. Fork → 复制 `templates/entry/` 到目标分类目录，改名为英文 kebab-case 条目名
2. 填好三件套
3. `node scripts/build-readme.mjs`
4. 提交 PR，一个 PR 一个条目

## 数据图表维护

数据图表使用显式模拟数据与标准库生成：先修改 `scripts/build-charts.py`，运行 `python3 scripts/build-charts.py`，再运行 `node scripts/build-readme.mjs` 和 `python3 scripts/check-charts.py`。图形、提示词和元数据必须一致；统计编码和动画终态都须核对。生成脚本仅维护数据图表，不覆盖其他分类。
