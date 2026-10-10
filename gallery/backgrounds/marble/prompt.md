# 大理石 `静态` `2D`

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="大理石">

```
用 SVG 画"大理石"满版材质：
- 底色冷白渐变（#f4f4f0 → #dfe3e8）
- 蓝灰纹理层：feTurbulence baseFrequency="0.008 0.028" octaves 4 映射蓝灰（opacity 0.6）
- 静脉纹：第二条低频噪声阈值化细深纹（opacity 0.5）
- 一条金色细纹点缀（stroke 金 0.8）
- 右下参数卡：底色 / 纹理频率 / 静脉纹 / 金纹
- 画布 1200×800
```
