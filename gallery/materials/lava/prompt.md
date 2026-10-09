# 熔岩 `静态·smil` `2D`

<img src="index.svg" width="720" alt="熔岩">

```
用 SVG 做"熔岩"动态材质：
- 深色岩壳满版，裂缝网络透出橙红熔光（feTurbulence bf 0.025 octaves 3 + feColorMatrix 阈值映射橙红）
- 岩壳纹理 seed 步进循环（discrete，纹理持续演化）
- 裂缝辉光：同纹理高斯模糊橙色层叠加
- 右下参数卡：阈值矩阵 / seed 步进 / 辉光层
- 画布 1200×800
```
