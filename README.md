# svg-prompt

> **AI 生成 SVG 的图形图鉴** —— 每个作品都带可复制的提示词咒语。
> Every SVG ships with its prompt.

GitHub 上从不缺 SVG 画廊：[svg-spinners](https://github.com/n3r4zzurr0/svg-spinners)（7k★）、[logos](https://github.com/gilbarbara/logos)（6.8k★）、[awesome-svg](https://github.com/willianjusten/awesome-svg)……但它们全是"平铺画廊 / 链接清单"——**你看得见作品，拿不到让它诞生的提示词**。

本项目把两者耦合在一起：**每个条目 = 可视 SVG 作品 + 可复制提示词模板 + 五维标签**。调研了 GitHub 全站后确认：这么做的仓库，此前不存在。

## 📁 目录结构

```
svg-prompt/
├── gallery/                      # ★ 图鉴内容主体（按八大分类，一图一目录）
│   ├── basics/                   #   教学基础
│   ├── ui/                       #   UI 组件
│   ├── branding/                 #   品牌排版
│   ├── charts/                   #   图表报表
│   ├── infographics/             #   信息可视化
│   ├── materials/                #   实物模拟
│   ├── motion/                   #   动效艺术
│   └── math/                     #   高级数学
│       └── <entry-slug>/         #   每个条目一个目录（英文 kebab-case）
│           ├── index.svg         #     作品本体，浏览器可直接打开
│           ├── prompt.md         #     提示词咒语 + 复现要点
│           └── meta.json         #     五维标签（机器可读）
├── templates/entry/              # 新条目模板：复制这个目录开新条目
├── schema/entry.schema.json      # meta.json 的校验规则
├── scripts/build-data.mjs        # 聚合所有 meta.json → site/data.js
├── site/                         # 单页筛选站（GitHub Pages，建设中）
├── docs/research-notes.md        # 研究底稿：SVG 能力地图与 Agent×SVG 流派
└── archive/demos/                # 14 个技术验证 Demo 存档（立项前产物）
```

**为什么一图一目录，而不是全塞进一个大文档？** 条目会持续增长、面向社区投稿：目录化让每个投稿是纯增量 PR；"复制咒语"是文件级交互，打开一个条目复制即可、链接可分享；单页筛选体验不受影响——站点由各条目的 `meta.json` 聚合生成（`scripts/build-data.mjs`）。

## 🧭 五维标签体系

每个条目的 `meta.json` 用五个维度描述：

| 维度 | 字段 | 取值 | 说明 |
|---|---|---|---|
| **空间** | `space` | 2d / 3d | 是否使用三维投影、光照、拓扑变换 |
| **时间** | `time` | static / smil / css / js | 动效按依赖分层：SMIL 内嵌（零依赖）→ CSS → JS |
| **主分类** | （所在目录） | 八类之一 | 目录即分类，不重复存储 |
| **难度** | `difficulty` | L1–L6 | 从基础形状到拓扑形变的实现难度 |
| **咒语等级** | `spellLevel` | L1 / L2 / L3 | 复现所需提示词复杂度：**L1** 一句话直出 · **L2** 结构化模板 · **L3** 系统化流水线（语义 JSON → 布局引擎 → 渲染） |

> 「咒语等级」是本项目的首创维度：同样的图形，用多复杂的咒语才能让 AI 稳定复现，本身就是图鉴要回答的问题。

字段约束见 [schema/entry.schema.json](schema/entry.schema.json)。

## 🗂️ 八大主分类

| 目录 | 分类 | 收录内容 |
|---|---|---|
| `gallery/basics` | 教学基础 | 形状、坐标系、渐变、路径等入门原型 |
| `gallery/ui` | UI 组件 | 按钮、图标、加载器、玻璃拟态卡片 |
| `gallery/branding` | 品牌排版 | Logo、徽章、文字特效、图案纹理 |
| `gallery/charts` | 图表报表 | 架构图、仪表盘、流程图（继承 [Data-to-Viz](https://www.data-to-viz.com/) 与 FT Visual Vocabulary） |
| `gallery/infographics` | 信息可视化 | 关系图、地图、层级图 |
| `gallery/materials` | 实物模拟 | 玻璃、金属、木纹、光影等材质拟真 |
| `gallery/motion` | 动效艺术 | 描边动画、Morph、gooey、SMIL 自包含动图 |
| `gallery/math` | 高级数学 | 参数曲线、拓扑形变、分形、3D 投影 |

每个分类目录内的 `_about.md` 写明收录标准。

## ✍️ 如何新增一个条目

1. 复制 `templates/entry/` 到对应分类目录下，改名为英文 kebab-case 条目名（如 `gallery/charts/architecture-diagram/`）
2. `index.svg` 放作品（浏览器可直接打开渲染）；`prompt.md` 写咒语（用 `{花括号}` 标占位符）；`meta.json` 填五维标签（`slug` 必须与目录名一致）
3. 跑 `node scripts/build-data.mjs` 重新聚合，提交 PR

## 📄 许可

- 代码（脚本、站点）：[MIT](LICENSE)
- 图鉴内容（SVG 作品、提示词模板、文档）：CC BY 4.0 —— 注明出处即可自由使用
