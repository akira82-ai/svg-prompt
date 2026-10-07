# 渐变与玻璃质感

> 难度 L2 · 咒语等级 L2

## 咒语

```
用 SVG 画一张"渐变与玻璃质感"设计展示图，四个区块：
- 极光横幅：linearGradient 蓝→紫→粉多色过渡，叠加两团 radialGradient 光晕，圆角大横条
- 品牌图标：圆角方形渐变底座 + 中心四角星 path + feDropShadow 彩色光晕
- 渐变文字：大标题文字 fill="url(#textGrad)" 直接引用线性渐变
- 毛玻璃卡片：半透明白色圆角矩形叠在彩色背景上，feGaussianBlur 打底 + 1px 白描边（opacity 0.4）
画布 1200×800，深色背景衬托，全部零位图。
```

## 效果

![渐变与玻璃质感](index.svg)

## 复现要点

- 毛玻璃的"磨砂感"靠半透明填充 + 模糊背景两层叠加，只写一层不透明度会像普通半透明块
- 彩色光晕用 feDropShadow 的 flood-color 带 alpha，比手画模糊圆更贴
