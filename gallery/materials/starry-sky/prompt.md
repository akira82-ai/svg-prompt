# 程序化星空 `静态` `2D`

<img src="index.svg" width="720" alt="程序化星空">

```
用 SVG 画一张满版程序化星空：
- 背景：深蓝夜空纵向渐变（#0b1026 → #1b2a4a），叠一层低频蓝青星云薄雾，顶部 180px 深色压暗渐变，底部深色山影剪影
- 星星全部由 feTurbulence fractalNoise（baseFrequency=0.9）生成，再用 feColorMatrix 把 alpha 通道阈值化拉陡，筛出稀疏白色星点
- 手工点缀 3 颗亮星（十字光芒），与噪声星点形成大小层次
- 右下角深色半透明参数卡，标注四行参数：type / baseFrequency / 阈值矩阵 alpha 34/-27 / 亮星手工点缀 3 颗
- 画布 1200×800 满版纹理，标题白字在左上
```
