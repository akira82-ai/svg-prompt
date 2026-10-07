# SVG 研究笔记（磊叔 · SVG 教程/100 问 项目资料底稿）

> 2026-10-06 用 ego lite 搜集于 Google + X。原始文章全文在 `raw/` 目录。
> 目标：后续整理《SVG 完整教程》或《关于 SVG 的 100 个问题》。本文是能力地图 + 高级玩法 + Agent 视角的研究底稿。

## 一、为什么 Agent 场景偏爱 SVG（而非"画图"）

1. **文本即图像**：SVG 是 XML 文本，LLM 原生按 token 输出，不需要像素级渲染引擎。
2. **分辨率无关**：无限缩放不失真，一张图适配所有屏幕和打印。
3. **元素级可编辑**：每个形状/文字都是带 id 的节点，Agent 或人可以精确改局部。
4. **轻量 + 通用**：可内嵌到网页、Markdown 预览、文档，也可转 PDF/PNG/PPTX。
5. **渲染确定性**：同一份 SVG 在任何浏览器渲染结果一致，便于 Agent 自检与迭代。

参考：dev.to《Why AI agents can't draw SVG》指出 LLM 直接手写 SVG 的两大死穴——
**盲坐标放置**（无视觉皮层，靠猜 x/y）与**无碰撞检测**（文字溢出、箭头穿框）。
文中给出的工程解法：**模型只输出语义 JSON → 确定性布局引擎（ELK/d3-hierarchy/d3-sankey）
算坐标 → resvg（Rust，无需 Chromium）编译成 SVG/PNG → JSON Schema 校验错误回喂模型**。

## 二、SVG 能力地图（规范层）

### 基础层
- 形状：rect / circle / ellipse / line / polyline / polygon / **path**（贝塞尔+圆弧，一切之本）
- **viewBox 坐标系变换**：逻辑坐标系与物理像素解耦，SVG 伸缩魔法的核心
- 描边与填充：stroke-dasharray / dashoffset / linecap / linejoin、fill-rule(evenodd 挖洞)

### 复用与结构层
- `<defs>` + `<use>` + `<symbol>`：定义一次，到处引用（图标 sprite 系统的基石）
- `<pattern>`：平铺图案（可嵌套、可内容任意）
- `<marker>`：箭头/端点标记，跟随路径方向自动旋转
- `<g>` 分组 + transform（translate/rotate/scale/skew 矩阵变换）

### 填充进阶层
- 渐变：linearGradient / radialGradient（含 `fr` 焦点控制）/ stop-opacity 透明度渐变
- SVG 2 新增：**meshgradient**（网格渐变，任意形状 2D 渐变）、**hatch**（ hatch 线填充，工程制图风）

### 滤镜系统（最高级的部分）
约 20 个 filter primitive，可自由组合成"矢量版 Photoshop"：
- **feTurbulence**：零素材生成 Perlin 噪声 → 木纹/大理石/云/星空/水面
- **feDisplacementMap**：位移贴图扭曲（毛刺文字 Squiggly text、水波、火焰摇曳）
- feGaussianBlur + feColorMatrix(对比度) → **gooey/metaball 液态融合**效果
- **feComponentTransfer**：色阶/posterize/duotone 双色调
- feColorMatrix：通道级调色（单色图标换色、去色、反色）
- **feDiffuseLighting / feSpecularLighting**：法线贴图打光，出 3D 浮雕质感
- feMorphology：腐蚀/膨胀（描边文字、挤压轮廓）
- feDropShadow、feBlend、feComposite、feOffset、feTile、feImage
- 滤镜可用 CSS `filter: url(#id)` 应用到**任何 HTML 元素**（不只 SVG）

### 裁剪与遮罩层
- clip-path：硬边裁剪（几何形状）
- mask：灰度/亮度遮罩（柔和渐隐、图片填充文字、揭示动画）

### 文字层
- textPath：沿任意路径排文字（环形徽章、波浪文字）
- textLength + lengthAdjust：强制文字对齐宽度（排版利器）
- paint-order：描边在填充下方（描边字不压字重）
- rotate/x/y/dx/dy 逐字符控制

### 交互与动画层
- CSS：transition/keyframes 直接作用 SVG 属性；`:hover` 状态
- **SMIL**（`<animate>`/`<animateTransform>`）：写死在 SVG 文件里的自包含动画，
  无需 JS/CSS，单文件即可动——Agent 产出"会动的图"的重要路径，所有主流浏览器仍支持
- JS：getTotalLength / getPointAtLength（路径采样→描边动画/沿路径排布）、事件监听
- stroke-dasharray + dashoffset 经典组合 = **线稿描边动画**（line drawing）

### 嵌入层
- foreignObject：SVG 里嵌 HTML/CSS（富文本卡片、图文混排图表）
- SVG 2 起部分元素（video/audio/canvas/iframe）可直接嵌入，不用 foreignObject 包裹

### SVG 2 其他新特性（vs 1.1）
- href 取代 xlink:href；lang 取代 xml:lang
- tabindex / role / ARIA 全元素支持（无障碍）
- 几何属性（x/y/cx/r 等）可用 CSS 控制，可过渡动画
- paint-order、vector-effect（non-scaling-stroke 缩放不变形）
- 移除：SVG Fonts、DTD

## 三、高级玩法精选（按"哇"程度）

1. **程序化纹理**：feTurbulence + feColorMatrix + feComposite，几行代码出木纹/星空/噪点，
   零图片依赖（CSS-Tricks《Creating Patterns With SVG Filters》有星空/木纹等整套 gallery）
2. **液态 gooey 效果**：blur→contrast 组合让相邻色块融合成 metaball（X 上 Bikash 的
   文本选中液态跟随效果、jhey 的位移滤镜玩法）
3. **grainy gradient 噪点渐变**：渐变 + turbulence 噪点，消除"AI 味"平涂感（Smashing 收录）
4. **手写体抖动文字**：feTurbulence + feDisplacementMap（Sara Soueidan 系列）
5. **3D 打光质感**：feDiffuseLighting/feSpecularLighting 出浮雕/金属/凹凸
6. **描边动画**：dashoffset 补间，logo/插画"被画出来"
7. **路径采样**：getPointAtLength 沿任意曲线排布粒子/文字/刻度
8. **图进字出**：mask + text，文字镂空显视频/图片
9. **生成艺术**：SVG + JS 随机/噪声/三角函数 → 海报、图案库（X 上 100+ generative SVG
   patterns 库、Study of Space 海报站），且是 pen plotter 绘图机的主流格式
10. **单文件动图**：SMIL 内嵌动画，不依赖任何外部资源
11. **图标系统**：symbol sprite + currentColor + CSS 变量，一套图标任意换色
12. **富文本卡片**：foreignObject 内嵌 HTML，图表里出多行富文本

## 四、Agent × SVG 实践流派（X + Google 情报）

| 流派 | 做法 | 代表 |
|---|---|---|
| 直接手写 | 小图标/单概念图，模型直接输出 SVG | 多数 Agent 默认 |
| DSL 中转 | Mermaid 等语法→引擎渲染；语法脆弱易解析崩溃 | Pretty-Mermaid Skill（15 主题，SVG/ASCII 双输出） |
| 语义 JSON→布局引擎 | 模型出节点/边，ELK/d3 布局，resvg 渲染 | dev.to 文章方案 |
| Skill 化流水线 | 把设计流程写进 SKILL.md，SVG 只是输出格式 | logo-design-skill（★1.8k+，1400 参考库，16px 单色审计，8-12 概念稿）；FigGenie（论文级架构图 SVG→PDF/PNG/PPTX）；svg-diagram（linted house style） |
| 学术增强 | 语义 token 训练让 LLM 理解渲染顺序/遮挡 | LLM4SVG (arXiv 2412.11102) |

关键洞见（dev.to）：LLM 擅长**描述图是什么**，不擅长**决定东西在哪**。
把空间计算交给确定性引擎，把语义交给模型——这正是 ppt-master 类技能画 SVG 而非
"画图"的原因：SVG 既是渲染目标也是可编辑交付物，还能无损转 PPTX/PDF/PNG。

## 五、资料存档（raw/ 全文）

| 文件 | 来源 |
|---|---|
| w3c-svg2-new-features.md | github.com/w3c/svgwg wiki「SVG 2 new features」 |
| joshwcomeau-friendly-intro.md | joshwcomeau.com《A Friendly Introduction to SVG》(2025-07) |
| devto-why-agents-cant-draw-svg.md | dev.to msteja（2026-06） |
| smashing-magical-svg-techniques.md | smashingmagazine.com《Magical SVG Techniques》(2022-05) |
| csstricks-patterns-svg-filters.md | css-tricks.com《Creating Patterns With SVG Filters》(2021-03) |
| codrops-feturbulence-texture.md | tympanus.net/codrops Sara Soueidan 滤镜系列（2019-02） |
| arxiv-llm4svg.md | arxiv.org/abs/2412.11102《Empowering LLMs to Understand and Generate Complex Vector Graphics》 |

规范原文：W3C SVG 2 → https://www.w3.org/TR/SVG2/
MDN SVG 索引 → https://developer.mozilla.org/en-US/docs/Web/SVG
