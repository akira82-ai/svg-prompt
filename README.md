# svg-prompt

> **AI 生成 SVG 的图形图鉴** —— 每个作品都带可复制的提示词咒语。
> GitHub 上"看得见作品、拿不到提示词"的 SVG 画廊千千万，把两者耦合在一起的图鉴，此前不存在。

**用法**：看中哪张图 → 点卡片跳到它的咒语 → 点代码块右上角的复制按钮 → 粘贴给任意模型复现。

**咒语等级**：`L1` 一句话直出 · `L2` 结构化模板 · `L3` 系统化流水线（语义 JSON → 布局引擎 → 渲染）

## 目录

<!-- GALLERY:START -->
- **[教学基础](#%E6%95%99%E5%AD%A6%E5%9F%BA%E7%A1%80)** <sub>basics · 1 条</sub>
  - [七大基础图形](#%E4%B8%83%E5%A4%A7%E5%9F%BA%E7%A1%80%E5%9B%BE%E5%BD%A2)
- **[UI 组件](#ui-%E7%BB%84%E4%BB%B6)** <sub>ui · 1 条</sub>
  - [渐变与玻璃质感](#%E6%B8%90%E5%8F%98%E4%B8%8E%E7%8E%BB%E7%92%83%E8%B4%A8%E6%84%9F)
- **[品牌排版](#%E5%93%81%E7%89%8C%E6%8E%92%E7%89%88)** <sub>branding · 1 条</sub>
  - [程序化纹理与图案](#%E7%A8%8B%E5%BA%8F%E5%8C%96%E7%BA%B9%E7%90%86%E4%B8%8E%E5%9B%BE%E6%A1%88)
- **[图表报表](#%E5%9B%BE%E8%A1%A8%E6%8A%A5%E8%A1%A8)** <sub>charts · 3 条</sub>
  - [动态架构图](#%E5%8A%A8%E6%80%81%E6%9E%B6%E6%9E%84%E5%9B%BE)
  - [数据可视化仪表盘](#%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96%E4%BB%AA%E8%A1%A8%E7%9B%98)
  - [复杂系统架构图](#%E5%A4%8D%E6%9D%82%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84%E5%9B%BE)
- **[信息可视化](#%E4%BF%A1%E6%81%AF%E5%8F%AF%E8%A7%86%E5%8C%96)** <sub>infographics · 0 条</sub>
- **[实物模拟](#%E5%AE%9E%E7%89%A9%E6%A8%A1%E6%8B%9F)** <sub>materials · 1 条</sub>
  - [滤镜材质特效](#%E6%BB%A4%E9%95%9C%E6%9D%90%E8%B4%A8%E7%89%B9%E6%95%88)
- **[动效艺术](#%E5%8A%A8%E6%95%88%E8%89%BA%E6%9C%AF)** <sub>motion · 5 条</sub>
  - [线稿描边动画](#%E7%BA%BF%E7%A8%BF%E6%8F%8F%E8%BE%B9%E5%8A%A8%E7%94%BB)
  - [变形记 II](#%E5%8F%98%E5%BD%A2%E8%AE%B0-ii)
  - [变形记 Morph](#%E5%8F%98%E5%BD%A2%E8%AE%B0-morph)
  - [SMIL 动效面板](#smil-%E5%8A%A8%E6%95%88%E9%9D%A2%E6%9D%BF)
  - [SVG 黑科技四连](#svg-%E9%BB%91%E7%A7%91%E6%8A%80%E5%9B%9B%E8%BF%9E)
- **[高级数学](#%E9%AB%98%E7%BA%A7%E6%95%B0%E5%AD%A6)** <sub>math · 2 条</sub>
  - [三维投影](#%E4%B8%89%E7%BB%B4%E6%8A%95%E5%BD%B1)
  - [拓扑形变](#%E6%8B%93%E6%89%91%E5%BD%A2%E5%8F%98)

## 教学基础

<table>
<tr><td width="260" valign="top"><a href="#%E4%B8%83%E5%A4%A7%E5%9F%BA%E7%A1%80%E5%9B%BE%E5%BD%A2"><img src="gallery/basics/basic-shapes/index.svg" width="220" alt="七大基础图形"></a><br><strong><a href="#%E4%B8%83%E5%A4%A7%E5%9F%BA%E7%A1%80%E5%9B%BE%E5%BD%A2">七大基础图形</a></strong><br><sub>用 SVG 画一张基础图形教学图：并排展示 rect、circle、ellipse、line、polyline、poly…</sub></td></tr>
</table>

### 七大基础图形

<img src="gallery/basics/basic-shapes/index.svg" width="400" alt="七大基础图形">

```text
用 SVG 画一张基础图形教学图：并排展示 rect、circle、ellipse、line、polyline、polygon、path 七种基本形状，每种形状下方用小字标注英文名。统一风格：深灰描边 2px、半透明蓝色填充、浅米色背景，画布 1200×800，构图整齐留白均匀。
```


## UI 组件

<table>
<tr><td width="260" valign="top"><a href="#%E6%B8%90%E5%8F%98%E4%B8%8E%E7%8E%BB%E7%92%83%E8%B4%A8%E6%84%9F"><img src="gallery/ui/glassmorphism/index.svg" width="220" alt="渐变与玻璃质感"></a><br><strong><a href="#%E6%B8%90%E5%8F%98%E4%B8%8E%E7%8E%BB%E7%92%83%E8%B4%A8%E6%84%9F">渐变与玻璃质感</a></strong><br><sub>用 SVG 画一张&quot;渐变与玻璃质感&quot;设计展示图，四个区块： - 极光横幅：linearGradient 蓝→紫→粉多色过…</sub></td></tr>
</table>

### 渐变与玻璃质感

<img src="gallery/ui/glassmorphism/index.svg" width="400" alt="渐变与玻璃质感">

```text
用 SVG 画一张"渐变与玻璃质感"设计展示图，四个区块：
- 极光横幅：linearGradient 蓝→紫→粉多色过渡，叠加两团 radialGradient 光晕，圆角大横条
- 品牌图标：圆角方形渐变底座 + 中心四角星 path + feDropShadow 彩色光晕
- 渐变文字：大标题文字 fill="url(#textGrad)" 直接引用线性渐变
- 毛玻璃卡片：半透明白色圆角矩形叠在彩色背景上，feGaussianBlur 打底 + 1px 白描边（opacity 0.4）
画布 1200×800，深色背景衬托，全部零位图。
```


## 品牌排版

<table>
<tr><td width="260" valign="top"><a href="#%E7%A8%8B%E5%BA%8F%E5%8C%96%E7%BA%B9%E7%90%86%E4%B8%8E%E5%9B%BE%E6%A1%88"><img src="gallery/branding/procedural-textures/index.svg" width="220" alt="程序化纹理与图案"></a><br><strong><a href="#%E7%A8%8B%E5%BA%8F%E5%8C%96%E7%BA%B9%E7%90%86%E4%B8%8E%E5%9B%BE%E6%A1%88">程序化纹理与图案</a></strong><br><sub>用 SVG 画&quot;程序化纹理&quot;四联图，全部用滤镜生成、零图片素材： - 星空：feTurbulence fractalNo…</sub></td></tr>
</table>

### 程序化纹理与图案

<img src="gallery/branding/procedural-textures/index.svg" width="400" alt="程序化纹理与图案">

```text
用 SVG 画"程序化纹理"四联图，全部用滤镜生成、零图片素材：
- 星空：feTurbulence fractalNoise 高频 + feColorMatrix 阈值化 → 深蓝底上稀疏白色星点
- 噪点渐变：线性渐变底 + 半透明 feTurbulence 噪声覆盖，消除"AI 味"平涂感
- 木纹：feTurbulence baseFrequency="0.012 0.09" 横向拉伸噪声 + 棕色系 feColorMatrix 映射
- 平铺图案：<pattern> 定义小单元（圆点/网格）平铺整块
每块纹理下方标注名称，画布 1200×800。
```


## 图表报表

<table>
<tr><td width="260" valign="top"><a href="#%E5%8A%A8%E6%80%81%E6%9E%B6%E6%9E%84%E5%9B%BE"><img src="gallery/charts/animated-architecture/index.svg" width="220" alt="动态架构图"></a><br><strong><a href="#%E5%8A%A8%E6%80%81%E6%9E%B6%E6%9E%84%E5%9B%BE">动态架构图</a></strong><br><sub>用 SVG 画一张&quot;会呼吸&quot;的系统架构图（单文件、零 JS，动效全部 SMIL）： - 四层结构：Web 前端/小程序（…</sub></td><td width="260" valign="top"><a href="#%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96%E4%BB%AA%E8%A1%A8%E7%9B%98"><img src="gallery/charts/dashboard/index.svg" width="220" alt="数据可视化仪表盘"></a><br><strong><a href="#%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96%E4%BB%AA%E8%A1%A8%E7%9B%98">数据可视化仪表盘</a></strong><br><sub>用 SVG 画一张数据可视化仪表盘： - KPI 卡片行：4 张圆角卡片（指标名 + 大数字 + 涨跌幅箭头），如&quot;销售…</sub></td><td width="260" valign="top"><a href="#%E5%A4%8D%E6%9D%82%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84%E5%9B%BE"><img src="gallery/charts/system-architecture/index.svg" width="220" alt="复杂系统架构图"></a><br><strong><a href="#%E5%A4%8D%E6%9D%82%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84%E5%9B%BE">复杂系统架构图</a></strong><br><sub>用 SVG 画一张六层系统架构图（约 20 个节点）： - 分区自上而下：客户端层 / 接入层 / 服务层 / 中间件层…</sub></td></tr>
</table>

### 动态架构图

<img src="gallery/charts/animated-architecture/index.svg" width="400" alt="动态架构图">

```text
用 SVG 画一张"会呼吸"的系统架构图（单文件、零 JS，动效全部 SMIL）：
- 四层结构：Web 前端/小程序（客户端）→ API 网关 → 微服务 ×4 → 数据库主从，圆角矩形节点 + 正交折线布线
- 数据包流动：每条连接线上放小圆 <animateMotion> 沿真实布线 path 移动，各链路 begin 错开
- 心跳灯：每个服务节点角落小圆 opacity 0.3↔1 循环，dur 2s、begin 各不相同
- 标题流光：渐变 x1/x2 循环平移制造扫光
画布 1400×1000 深色底。
```


### 数据可视化仪表盘

<img src="gallery/charts/dashboard/index.svg" width="400" alt="数据可视化仪表盘">

```text
用 SVG 画一张数据可视化仪表盘：
- KPI 卡片行：4 张圆角卡片（指标名 + 大数字 + 涨跌幅箭头），如"销售额 GMV ¥1,284,590 +12.4%↑"
- 主区左侧：面积折线图（网格线 + 坐标轴刻度 + 渐变面积填充）
- 主区右侧：两枚环形进度图（stroke-dasharray 控制弧长，中心百分比数字）
- 底部：横向条形图 5 条，右端数值标签
- SMIL 入场动画：条形从 0 生长、环形描一圈、KPI 数字渐显，打开文件自动播放一次
画布 1200×900，蓝色系配色，留白均匀。
```


### 复杂系统架构图

<img src="gallery/charts/system-architecture/index.svg" width="400" alt="复杂系统架构图">

```text
用 SVG 画一张六层系统架构图（约 20 个节点）：
- 分区自上而下：客户端层 / 接入层 / 服务层 / 中间件层 / 数据层 / 观测层，每层一块浅色圆角底板 + 层名
- 每层 2–5 个节点（140×44 圆角矩形，写服务名），同层水平等距
- 连线全部正交折线（只走水平/垂直段），marker 箭头指向目标；从源节点底边中点出、目标节点顶边中点入
- 画布 1400×1000，分区留白均匀
动笔前先输出完整的节点坐标清单，再按清单绘制。
```


## 信息可视化

*暂无条目，欢迎按 `templates/entry/` 投稿。*

## 实物模拟

<table>
<tr><td width="260" valign="top"><a href="#%E6%BB%A4%E9%95%9C%E6%9D%90%E8%B4%A8%E7%89%B9%E6%95%88"><img src="gallery/materials/filter-materials/index.svg" width="220" alt="滤镜材质特效"></a><br><strong><a href="#%E6%BB%A4%E9%95%9C%E6%9D%90%E8%B4%A8%E7%89%B9%E6%95%88">滤镜材质特效</a></strong><br><sub>用 SVG 展示三种滤镜材质特效，全部零位图实时计算： - 液态融合：两个相邻色块 + feGaussianBlur(s…</sub></td></tr>
</table>

### 滤镜材质特效

<img src="gallery/materials/filter-materials/index.svg" width="400" alt="滤镜材质特效">

```text
用 SVG 展示三种滤镜材质特效，全部零位图实时计算：
- 液态融合：两个相邻色块 + feGaussianBlur(stdDeviation 10) + feColorMatrix 把 alpha 通道对比度拉陡
  （"20 0 0 0 0 / 0 0 0 20 -7" 型矩阵）→ 色块相互吸附成 metaball
- 金属打光：灰色凸起文字 + feSpecularLighting + fePointLight，光源 z 坐标加 <animate> 让高光游走
- 水波扭曲：一行文字 + feTurbulence + feDisplacementMap，baseFrequency 加缓慢 <animate> 像在水中晃动
画布 1200×800 深色底，每块标注名称。
```


## 动效艺术

<table>
<tr><td width="260" valign="top"><a href="#%E7%BA%BF%E7%A8%BF%E6%8F%8F%E8%BE%B9%E5%8A%A8%E7%94%BB"><img src="gallery/motion/line-drawing/index.svg" width="220" alt="线稿描边动画"></a><br><strong><a href="#%E7%BA%BF%E7%A8%BF%E6%8F%8F%E8%BE%B9%E5%8A%A8%E7%94%BB">线稿描边动画</a></strong><br><sub>用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐&quot;画出来&quot;。 要求： - 单文件自包含，零 JS，动画用 …</sub></td><td width="260" valign="top"><a href="#%E5%8F%98%E5%BD%A2%E8%AE%B0-ii"><img src="gallery/motion/morph-ii/index.svg" width="220" alt="变形记 II"></a><br><strong><a href="#%E5%8F%98%E5%BD%A2%E8%AE%B0-ii">变形记 II</a></strong><br><sub>用 SVG 做进阶路径形变： - 单词变形 CAT ⇄ DOG：C/A/T 与 D/O/G 六个字母各设计一副 6 段贝…</sub></td><td width="260" valign="top"><a href="#%E5%8F%98%E5%BD%A2%E8%AE%B0-morph"><img src="gallery/motion/path-morph/index.svg" width="220" alt="变形记 Morph"></a><br><strong><a href="#%E5%8F%98%E5%BD%A2%E8%AE%B0-morph">变形记 Morph</a></strong><br><sub>用 SVG 做路径形变动画，两组： - 几何三态：圆角方形 ⇄ 圆 ⇄ 菱形，同一副 8 锚点骨架（直线态 = 控制点全…</sub></td><td width="260" valign="top"><a href="#smil-%E5%8A%A8%E6%95%88%E9%9D%A2%E6%9D%BF"><img src="gallery/motion/smil-panel/index.svg" width="220" alt="SMIL 动效面板"></a><br><strong><a href="#smil-%E5%8A%A8%E6%95%88%E9%9D%A2%E6%9D%BF">SMIL 动效面板</a></strong><br><sub>用 SVG 做一块自包含动效面板（零 JS、零 CSS，动画全部用 SMIL &lt;animate&gt;/&lt;animateTra…</sub></td></tr>
<tr><td width="260" valign="top"><a href="#svg-%E9%BB%91%E7%A7%91%E6%8A%80%E5%9B%9B%E8%BF%9E"><img src="gallery/motion/svg-mechanics/index.svg" width="220" alt="SVG 黑科技四连"></a><br><strong><a href="#svg-%E9%BB%91%E7%A7%91%E6%8A%80%E5%9B%9B%E8%BF%9E">SVG 黑科技四连</a></strong><br><sub>用 SVG 做&quot;机制级技法&quot;四联演示： - 聚光灯：深色底 + 一段隐藏文字，用径向渐变亮斑作为 mask，&lt;anima…</sub></td></tr>
</table>

### 线稿描边动画

<img src="gallery/motion/line-drawing/index.svg" width="400" alt="线稿描边动画">

```text
用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐"画出来"。
要求：
- 单文件自包含，零 JS，动画用 CSS keyframes 实现
- 所有轮廓只用 stroke 绘制，fill:none，统一 stroke-width:{2}、stroke-linecap:round
- 每条 path 的 stroke-dasharray 等于自身长度，dashoffset 从满值补间到 0
- 各条 path 依次延迟 {0.3s} 开始描边，总时长 {6s}，动画结束后停留在线稿完成状态（forwards）
- 画布 {1000×700}，{深蓝夜色} 背景衬托 {浅金色} 线条
```


### 变形记 II

<img src="gallery/motion/morph-ii/index.svg" width="400" alt="变形记 II">

```text
用 SVG 做进阶路径形变：
- 单词变形 CAT ⇄ DOG：C/A/T 与 D/O/G 六个字母各设计一副 6 段贝塞尔骨架，
  两词都是 3 子路径 × 6 段 = 18 段，逐字母插值成"液态书法"
- 字母 B ⇄ X：B = 竖笔 + 双碗，X = 回描四臂，锚点结构对齐
- 图标互变：播放 ▶ ⇄ 暂停 ⏸ 两个"画出来"的图标平滑过渡
铁律写进要求：任何两条 path 的命令数与锚点数完全相同。
画布 1200×800 深色底。
```


### 变形记 Morph

<img src="gallery/motion/path-morph/index.svg" width="400" alt="变形记 Morph">

```text
用 SVG 做路径形变动画，两组：
- 几何三态：圆角方形 ⇄ 圆 ⇄ 菱形，同一副 8 锚点骨架（直线态 = 控制点全部落在边上的共线退化贝塞尔）
- 图形开花：圆 → 五角星 → 爱心，同一副 10 锚点骨架（星 = 内锚点收到 r=38，心 = 锚点按心形重排）
全部用 <animate attributeName="d" values="…"> 循环，dur 6s，画布 1000×700 居中。
```


### SMIL 动效面板

<img src="gallery/motion/smil-panel/index.svg" width="400" alt="SMIL 动效面板">

```text
用 SVG 做一块自包含动效面板（零 JS、零 CSS，动画全部用 SMIL <animate>/<animateTransform>/<animateMotion>）：
- 雷达扫描：扇形 <animateTransform type="rotate"> 绕中心匀速旋转，底下三圈同心圆网格 + 扫过余辉
- 引力轨道：小圆 <animateMotion> + <mpath href="#orbit"> 沿椭圆轨道转，中心放行星体
- 状态灯：三个圆 opacity 依次呼吸，begin 依次错开 0.3s
全部 repeatCount="indefinite"，画布 900×600 深色面板底。
```


### SVG 黑科技四连

<img src="gallery/motion/svg-mechanics/index.svg" width="400" alt="SVG 黑科技四连">

```text
用 SVG 做"机制级技法"四联演示：
- 聚光灯：深色底 + 一段隐藏文字，用径向渐变亮斑作为 mask，<animateMotion> 让光斑水平扫过——只有光斑扫到处文字可见
- 路径形变：两条锚点数完全相同的 path，<animate attributeName="d" values="A;B;A"> 平滑变形
- 文字骑路径：一行文字 <textPath href="#curve"> 沿贝塞尔曲线排布
- 等距伪 3D：立方体与台阶用 30° 等距变换拼出一个小场景，三个面三种明度
画布 1200×900，深色底霓虹配色。
```


## 高级数学

<table>
<tr><td width="260" valign="top"><a href="#%E4%B8%89%E7%BB%B4%E6%8A%95%E5%BD%B1"><img src="gallery/math/three-d/index.svg" width="220" alt="三维投影"></a><br><strong><a href="#%E4%B8%89%E7%BB%B4%E6%8A%95%E5%BD%B1">三维投影</a></strong><br><sub>用 SVG 表现 3D（零 JS、零 WebGL），三块： - 等距插画：数据中心机柜，30° 等距轴，顶/左/右三个面…</sub></td><td width="260" valign="top"><a href="#%E6%8B%93%E6%89%91%E5%BD%A2%E5%8F%98"><img src="gallery/math/topology-deform/index.svg" width="220" alt="拓扑形变"></a><br><strong><a href="#%E6%8B%93%E6%89%91%E5%BD%A2%E5%8F%98">拓扑形变</a></strong><br><sub>用 SVG 展示 3D 参数之舞（每一帧都是真实 3D：参数方程 + 旋转矩阵 + 投影，SMIL 关键帧由脚本预计算）…</sub></td></tr>
</table>

### 三维投影

<img src="gallery/math/three-d/index.svg" width="400" alt="三维投影">

```text
用 SVG 表现 3D（零 JS、零 WebGL），三块：
- 等距插画：数据中心机柜，30° 等距轴，顶/左/右三个面不同明度 + LED 心跳 SMIL
- 参数投影：线框球与环面，顶点经旋转矩阵 + 透视投影落到 2D，近棱亮、远棱暗
- 动态 3D：一个旋转立方体，把预计算的若干关键帧 pose 写成 <animateTransform> 的 values 序列
复杂坐标必须用脚本生成后填入 SVG。画布 1200×900 深色底。
```


### 拓扑形变

<img src="gallery/math/topology-deform/index.svg" width="400" alt="拓扑形变">

```text
用 SVG 展示 3D 参数之舞（每一帧都是真实 3D：参数方程 + 旋转矩阵 + 投影，SMIL 关键帧由脚本预计算）：
- 球面 ⇄ 圆环面：同一副 (u,v) 网格，环面主半径 R 从 62 收到 0，圆环面连续退化成球面
- 莫比乌斯带：M(u,v) 参数方程生成单侧曲面，点阵渲染，标注"只有一条边"
- 利萨茹曲线与水面涟漪各一块，同样参数方程驱动
点阵量大必须用脚本（Node/Python）生成坐标再固化进 SVG。画布 1200×800 深底彩点。
```
<!-- GALLERY:END -->

## 贡献

复制 `templates/entry/` 到对应分类目录，填好三件套（`index.svg` 作品 / `prompt.md` 咒语 / `meta.json` 标签），跑 `node scripts/build-readme.mjs` 重新生成本页。收录标准见各分类目录的 `_about.md`，完整指南见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

代码 [MIT](LICENSE) · 图鉴内容 CC BY 4.0（注明出处即可自由使用）
