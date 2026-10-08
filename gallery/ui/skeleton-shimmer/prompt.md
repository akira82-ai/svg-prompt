# 骨架屏微光 `SMIL 动效` `2D`

<img src="index.svg" width="720" alt="骨架屏微光">

```
用 SVG 做一张"骨架屏动效规格图"（SMIL、零 JS）：
- 骨架屏布局：圆形头像占位 + 三行宽度递减的文字条占位 + 下方大图占位，全部浅灰圆角块
- 一道白色斜向高光从左到右循环扫过所有占位块（用 linearGradient 高亮矩形 + clipPath 裁剪在骨架区域内，animate 平移循环）
- 标注 骨架屏 skeleton · 扫光 1.8s 循环
- 画布 1200×800，浅蓝灰背景 #f6f8fb，白色圆角卡片，占位块 #e9edf3
```
