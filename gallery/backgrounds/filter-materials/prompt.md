# 滤镜材质特效 `SMIL 动效` `2D`

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="滤镜材质特效">

```
用 SVG 展示四种滤镜材质特效：
- 液态融合：三个彩圆相互吸附 + feGaussianBlur(stdDeviation 10) + feColorMatrix 把 alpha 通道对比度拉陡（阈值约 20/-9）→ metaball 效果
- 金属打光：灰色凸起文字 + feSpecularLighting + fePointLight，光源 z 坐标加 <animate> 让高光游走
- 水波扭曲：一行文字 + feTurbulence + feDisplacementMap，baseFrequency 加缓慢 <animate> 像在水中晃动
  - 霓虹辉光：描边文字 + feGaussianBlur 双层叠加辉光，opacity 闪烁
画布 1200×800 深色底，标题与副标题在左上，四块面板各配等宽字注释。
```
