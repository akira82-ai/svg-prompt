# svg-prompt

> **AI 生成 SVG 的图形图鉴** —— 每个作品都带可复制的提示词咒语。
> GitHub 上"看得见作品、拿不到提示词"的 SVG 画廊千千万，把两者耦合在一起的图鉴，此前不存在。

**用法**：看中哪张图 → 复制图下方的咒语 → 粘贴给任意模型复现。本页即全部内容，无需跳转。

**图例**：`难度 L1–L6` 实现难度 · `咒语 L1/L2/L3` 复现所需提示词复杂度（L1 一句话直出 → L2 结构化模板 → L3 系统化流水线）· 静态 / SMIL / CSS / JS 动效实现方式（前三种零 JS，单文件即动）· 2d / 3d 空间维度

## 目录

<!-- GALLERY:START -->
- **[教学基础](#%E6%95%99%E5%AD%A6%E5%9F%BA%E7%A1%80)** <sub>basics · 1 条</sub>
  - [七大基础图形](#%E4%B8%83%E5%A4%A7%E5%9F%BA%E7%A1%80%E5%9B%BE%E5%BD%A2) `L1`
- **[UI 组件](#ui-%E7%BB%84%E4%BB%B6)** <sub>ui · 0 条</sub>
- **[品牌排版](#%E5%93%81%E7%89%8C%E6%8E%92%E7%89%88)** <sub>branding · 0 条</sub>
- **[图表报表](#%E5%9B%BE%E8%A1%A8%E6%8A%A5%E8%A1%A8)** <sub>charts · 0 条</sub>
- **[信息可视化](#%E4%BF%A1%E6%81%AF%E5%8F%AF%E8%A7%86%E5%8C%96)** <sub>infographics · 0 条</sub>
- **[实物模拟](#%E5%AE%9E%E7%89%A9%E6%A8%A1%E6%8B%9F)** <sub>materials · 0 条</sub>
- **[动效艺术](#%E5%8A%A8%E6%95%88%E8%89%BA%E6%9C%AF)** <sub>motion · 1 条</sub>
  - [线稿描边动画](#%E7%BA%BF%E7%A8%BF%E6%8F%8F%E8%BE%B9%E5%8A%A8%E7%94%BB) `L2`
- **[高级数学](#%E9%AB%98%E7%BA%A7%E6%95%B0%E5%AD%A6)** <sub>math · 0 条</sub>

## 教学基础

### 七大基础图形

`难度 L1` · `咒语 L1` · `静态` · `2d` · `rect` · `circle` · `ellipse` · `line` · `polyline` · `polygon` · `path` · `text`

<img src="gallery/basics/basic-shapes/index.svg" width="600" alt="七大基础图形">

**咒语**（代码块右上角可一键复制）：

```text
用 SVG 画一张基础图形教学图：并排展示 rect、circle、ellipse、line、polyline、polygon、path 七种基本形状，每种形状下方用小字标注英文名。统一风格：深灰描边 2px、半透明蓝色填充、浅米色背景，画布 1200×800，构图整齐留白均匀。
```

---

## UI 组件

*暂无条目，欢迎按 `templates/entry/` 投稿。*

## 品牌排版

*暂无条目，欢迎按 `templates/entry/` 投稿。*

## 图表报表

*暂无条目，欢迎按 `templates/entry/` 投稿。*

## 信息可视化

*暂无条目，欢迎按 `templates/entry/` 投稿。*

## 实物模拟

*暂无条目，欢迎按 `templates/entry/` 投稿。*

## 动效艺术

### 线稿描边动画

`难度 L2` · `咒语 L2` · `CSS 动效` · `2d` · `stroke-dasharray` · `stroke-dashoffset` · `keyframes` · `path`

<img src="gallery/motion/line-drawing/index.svg" width="600" alt="线稿描边动画">

**咒语**（代码块右上角可一键复制）：

```text
用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐"画出来"。
要求：
- 单文件自包含，零 JS，动画用 CSS keyframes 实现
- 所有轮廓只用 stroke 绘制，fill:none，统一 stroke-width:{2}、stroke-linecap:round
- 每条 path 的 stroke-dasharray 等于自身长度，dashoffset 从满值补间到 0
- 各条 path 依次延迟 {0.3s} 开始描边，总时长 {6s}，动画结束后停留在线稿完成状态（forwards）
- 画布 {1000×700}，{深蓝夜色} 背景衬托 {浅金色} 线条
```

---

## 高级数学

*暂无条目，欢迎按 `templates/entry/` 投稿。*
<!-- GALLERY:END -->

## 贡献

复制 `templates/entry/` 到对应分类目录，填好三件套（`index.svg` 作品 / `prompt.md` 咒语 / `meta.json` 标签），跑 `node scripts/build-readme.mjs` 重新生成本页。收录标准见各分类目录的 `_about.md`，完整指南见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

代码 [MIT](LICENSE) · 图鉴内容 CC BY 4.0（注明出处即可自由使用）
