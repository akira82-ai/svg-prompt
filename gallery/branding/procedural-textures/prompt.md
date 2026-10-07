# 程序化纹理与图案

> 难度 L3 · 咒语等级 L2

## 咒语

```
用 SVG 画"程序化纹理"四联图，全部用滤镜生成、零图片素材：
- 星空：feTurbulence fractalNoise 高频 + feColorMatrix 阈值化 → 深蓝底上稀疏白色星点
- 噪点渐变：线性渐变底 + 半透明 feTurbulence 噪声覆盖，消除"AI 味"平涂感
- 木纹：feTurbulence baseFrequency="0.012 0.09" 横向拉伸噪声 + 棕色系 feColorMatrix 映射
- 平铺图案：<pattern> 定义小单元（圆点/网格）平铺整块
每块纹理下方标注名称，画布 1200×800。
```

## 效果

![程序化纹理与图案](index.svg)

## 复现要点

- 木纹的关键是 baseFrequency 两个值拉开倍率（横向压扁噪声），写成一个值就变成大理石
- 星空的"阈值化"必须点明 feColorMatrix 里 alpha 行拉陡，否则出的是灰雾不是星点
