# 科技网格 / Technical Grid

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="科技网格">

```
用SVG绘制“科技网格 / Technical Grid”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 克制的坐标网格适合技术封面与页面底图。
- 80×80单元，边线1px、交点半径2，四角复制避免切断；patternUnits=userSpaceOnUse，不承担数据坐标含义。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">科技网格 / Technical Grid</title><desc id="desc">克制的坐标网格适合技术封面与页面底图。；80×80单元，边线1px、交点半径2，四角复制避免切断；patternUnits=userSpaceOnUse，不承担数据坐标含义。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 05</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">科技网格</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Technical Grid</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><rect x="64" y="190" width="1272" height="620" fill="#162b40" /><defs><pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#355570" stroke-width="1"/><circle cx="0" cy="0" r="2" fill="#70b4c0"/><circle cx="80" cy="0" r="2" fill="#70b4c0"/><circle cx="0" cy="80" r="2" fill="#70b4c0"/><circle cx="80" cy="80" r="2" fill="#70b4c0"/></pattern></defs><rect x="64" y="190" width="1272" height="620" fill="url(#grid)" /></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">克制的坐标网格适合技术封面与页面底图。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
