# 贡献指南

## 仓库结构

```
svg-prompt/
├── gallery/                      # ★ 内容源文件（一图一目录，README 由这里生成）
│   └── <category>/<entry-slug>/  #   八大分类，英文 kebab-case 条目名
│       ├── index.svg             #     作品本体，浏览器可直接打开
│       ├── prompt.md             #     条目详情页：标题 + 大图 + 提示词代码块（三段式）
│       └── meta.json             #     五维标签（机器可读）
├── templates/entry/              # 新条目模板：复制这个目录开新条目
├── schema/entry.schema.json      # meta.json 的校验规则
├── scripts/build-readme.mjs      # 扫描 gallery → 生成 README 缩略图画廊
└── archive/demos/                # 立项前的 14 个技术验证 Demo（存档，非图鉴条目）
```

**两级页面结构**：主 README = 缩略图画廊（每卡链接到条目详情页）；条目详情页 = `prompt.md` 的 GitHub 文件页（标题 + 720px 大图 + 提示词代码块）。原生复制按钮只存在于详情页的顶层代码块——这是 GitHub 平台规则（table/折叠内必失，实测），所以主页不放提示词正文。

**为什么一图一目录，而不是把内容直接写进 README？** README 是生成物（`<!-- GALLERY:START/END -->` 之间由脚本维护），内容源文件才是唯一事实。目录化让每个投稿是纯增量 PR、详情页与作品同目录自包含——人永远不手写长 README。

## 三件套约定

| 文件 | 要求 |
|---|---|
| `index.svg` | 作品本体；浏览器直接打开即渲染；动效条目优先 SMIL / CSS 实现（零 JS） |
| `prompt.md` | **三段式详情页**：`# 中文标题` + `静态`/`动效`/`2D`/`3D` 标签 → `<img src="index.svg" width="720">` → `## 提示词` + 代码块；保持这个结构，不要加别的小节 |
| `prompt.md` 内的提示词 | **多行结构化书写**（不要挤成一行）：首行一句话意图，`-` 列表逐条列结构与风格要求，可替换部分用 `{花括号}` 标注 |
| `meta.json` | 字段见 [schema/entry.schema.json](schema/entry.schema.json)；`slug` 必须与目录名一致 |

## 五维标签

| 维度 | 字段 | 取值 |
|---|---|---|
| 空间 | `space` | `2d` / `3d` |
| 时间 | `time` | `static` / `smil` / `css` / `js` |
| 主分类 | （所在目录） | 八类之一，不重复存储 |
| 难度 | `difficulty` | L1–L6（基础形状 → 拓扑形变/系统级） |
| 咒语等级 | `spellLevel` | L1 一句话直出 / L2 结构化模板 / L3 系统化流水线 |

收录标准见各分类目录的 `_about.md`。

## 投稿流程

1. Fork → 复制 `templates/entry/` 到目标分类目录，改名为英文 kebab-case 条目名
2. 填好三件套
3. `node scripts/build-readme.mjs`
4. 提交 PR，一个 PR 一个条目
