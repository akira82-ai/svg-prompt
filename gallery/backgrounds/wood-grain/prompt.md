# 木纹 `静态` `2D`

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="木纹">

```
用 SVG 画一张满版木纹材质：
- 底色暖棕，feTurbulence baseFrequency="0.012 0.09"（横向低频、纵向高频 = 横向拉伸的年轮条纹），numOctaves 4
- 用 feColorMatrix 把噪声映射成棕色系明暗
- 上面 3 条深色横向木板缝（分成四条木板）增强真实感
- 左下角白底参数卡四行：baseFrequency 两个值 / numOctaves / 色彩映射·棕金三通道 / 木板缝·3 条深色分隔
- 标题米白字在左上，画布 1200×800 满版
```
