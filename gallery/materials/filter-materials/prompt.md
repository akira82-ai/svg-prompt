# 滤镜材质特效 `SMIL 动效` `2D`

<img src="index.svg" width="720" alt="滤镜材质特效">

```
用 SVG 展示三种滤镜材质特效，全部零位图实时计算：
- 液态融合：两个相邻色块 + feGaussianBlur(stdDeviation 10) + feColorMatrix 把 alpha 通道对比度拉陡
  （"20 0 0 0 0 / 0 0 0 20 -7" 型矩阵）→ 色块相互吸附成 metaball
- 金属打光：灰色凸起文字 + feSpecularLighting + fePointLight，光源 z 坐标加 <animate> 让高光游走
- 水波扭曲：一行文字 + feTurbulence + feDisplacementMap，baseFrequency 加缓慢 <animate> 像在水中晃动
画布 1200×800 深色底，每块标注名称。
```
