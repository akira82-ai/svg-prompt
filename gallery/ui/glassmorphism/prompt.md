# 渐变与玻璃质感 `静态` `2D`

<img src="index.svg" width="720" alt="渐变与玻璃质感">

## 提示词

```
用 SVG 画一张"渐变与玻璃质感"设计展示图，四个区块：
- 极光横幅：linearGradient 蓝→紫→粉多色过渡，叠加两团 radialGradient 光晕，圆角大横条
- 品牌图标：圆角方形渐变底座 + 中心四角星 path + feDropShadow 彩色光晕
- 渐变文字：大标题文字 fill="url(#textGrad)" 直接引用线性渐变
- 毛玻璃卡片：半透明白色圆角矩形叠在彩色背景上，feGaussianBlur 打底 + 1px 白描边（opacity 0.4）
画布 1200×800，深色背景衬托，全部零位图。
```
