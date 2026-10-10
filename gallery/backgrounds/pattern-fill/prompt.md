# 几何平铺 / Geometric Pattern

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="几何平铺">

```
用SVG绘制“几何平铺 / Geometric Pattern”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 同一复古几何单元无缝重复，适合作包装与编辑底纹。
- 96×96奶油底、中心赭红环、四角藏蓝三角；跨单元四角拼接成菱形，不再与科技网格重复。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">几何平铺 / Geometric Pattern</title><desc id="desc">同一复古几何单元无缝重复，适合作包装与编辑底纹。；96×96奶油底、中心赭红环、四角藏蓝三角；跨单元四角拼接成菱形，不再与科技网格重复。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 06</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">几何平铺</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Geometric Pattern</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><rect x="64" y="190" width="1272" height="620" fill="#e8dfc8" /><defs><pattern id="tile" width="96" height="96" patternUnits="userSpaceOnUse"><rect width="96" height="96" fill="#e8dfc8"/><circle cx="48" cy="48" r="29" fill="none" stroke="#b2674f" stroke-width="8"/><path d="M0 0L12 0 0 12Z M96 0L84 0 96 12Z M0 96L12 96 0 84Z M96 96L84 96 96 84Z" fill="#29455e"/></pattern></defs><rect x="64" y="190" width="1272" height="620" fill="url(#tile)" /></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">同一复古几何单元无缝重复，适合作包装与编辑底纹。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
