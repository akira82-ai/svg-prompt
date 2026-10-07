# 布局测试页（临时文件，验证后删除）

## A. 卡片方案：td 内 HTML pre + details 预览

<table>
<tr>
<td align="center">
<img src="../gallery/basics/basic-shapes/index.svg" width="220" alt="测试1"><br>
<strong>七大基础图形</strong><br>
<details open>
<summary>用 SVG 画一张基础图形教学图：并排展示 rect、circle、ellipse、line、polyline、polygon、path 七种基本形状，每种形状下方标注英文名。</summary>
<pre>用 SVG 画一张基础图形教学图：并排展示 rect、circle、ellipse、line、polyline、polygon、path 七种基本形状，每种形状下方用小字标注英文名。统一风格：深灰描边 2px、半透明蓝色填充、浅米色背景，画布 1200×800，构图整齐留白均匀。</pre>
</details>
</td>
<td align="center">
<img src="../gallery/motion/line-drawing/index.svg" width="220" alt="测试2"><br>
<strong>线稿描边动画</strong><br>
<details>
<summary>用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐"画出来"…</summary>
<pre>用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐"画出来"。
要求：
- 单文件自包含，零 JS，动画用 CSS keyframes 实现
- 所有轮廓只用 stroke 绘制，fill:none
- 每条 path 的 stroke-dasharray 等于自身长度，dashoffset 从满值补间到 0</pre>
</details>
</td>
</tr>
</table>

## B. 对照组：普通 markdown fence

```text
fenced code block 对照组（这里一定有复制按钮）
```

## C. 对照组：裸 HTML pre（不在 table/details 里）

<pre>裸 HTML pre 对照（验证 GitHub 是否给 HTML pre 注入复制按钮）</pre>
