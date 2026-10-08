# 木纹 `静态` `2D`

<img src="index.svg" width="720" alt="木纹">

```
用 SVG 画一张满版木纹材质：
- 底色暖棕，feTurbulence baseFrequency="0.012 0.09"（横向低频、纵向高频 = 横向拉伸的年轮条纹），numOctaves 4
- 用 feColorMatrix 把噪声映射成棕色系明暗
- 上面叠加三块木板分隔线（深色细缝）增强真实感
- 左下角白底参数卡：baseFrequency 两个值、numOctaves、色彩映射
- 标题深字在左上，画布 1200×800 满版
```
