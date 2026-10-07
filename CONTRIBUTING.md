# 贡献指南

## 仓库结构

```
svg-prompt/
├── gallery/                      # ★ 内容源文件（一图一目录，README 由这里生成）
│   └── <category>/<entry-slug>/  #   八大分类，英文 kebab-case 条目名
│       ├── index.svg             #     作品本体，浏览器可直接打开
│       ├── prompt.md             #     提示词咒语（第一个代码块会被注入 README）
│       └── meta.json             #     五维标签（机器可读）
├── templates/entry/              # 新条目模板：复制这个目录开新条目
├── schema/entry.schema.json      # meta.json 的校验规则
├── scripts/build-readme.mjs      # 扫描 gallery → 生成 README 目录与条目区
└── archive/demos/                # 立项前的 14 个技术验证 Demo（存档，非图鉴条目）
```

**为什么一图一目录，而不是把内容直接写进 README？** README 是生成物（`<!-- GALLERY:START/END -->` 之间由脚本维护），内容源文件才是唯一事实。目录化让每个投稿是纯增量 PR、文件级复制咒语、锚点导航由脚本统一生成——人永远不手写长 README。

## 三件套约定

| 文件 | 要求 |
|---|---|
| `index.svg` | 作品本体；浏览器直接打开即渲染；动效条目优先 SMIL / CSS 实现（零 JS） |
| `prompt.md` | 第一个代码块 = 咒语正文，会被注入 README；可替换部分用 `{花括号}` 标注；正文附复现要点 |
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
