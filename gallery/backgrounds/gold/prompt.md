# 金色镜面 / Gold Reflection

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="金色镜面">

```
用SVG绘制“金色镜面 / Gold Reflection”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 多段金色渐变形成镜面反射带，保留干净可用的材质面。
- 横向多段渐变色标：#725328,#e7c37c,#fff1ba,#be8c3e,#f4d89b,#70512d；移除AURUM 24K刻字，不暗示材质纯度和实物性能。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">金色镜面 / Gold Reflection</title><desc id="desc">多段金色渐变形成镜面反射带，保留干净可用的材质面。；横向多段渐变色标：#725328,#e7c37c,#fff1ba,#be8c3e,#f4d89b,#70512d；移除AURUM 24K刻字，不暗示材质纯度和实物性能。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 12</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">金色镜面</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Gold Reflection</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><defs><linearGradient id="metal" x1="0" y1="0" x2="1" y2=".2"><stop offset="0.0000" stop-color="#725328"/><stop offset="0.2000" stop-color="#e7c37c"/><stop offset="0.4000" stop-color="#fff1ba"/><stop offset="0.6000" stop-color="#be8c3e"/><stop offset="0.8000" stop-color="#f4d89b"/><stop offset="1.0000" stop-color="#70512d"/></linearGradient></defs><rect x="64" y="190" width="1272" height="620" fill="url(#metal)" /></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">多段金色渐变形成镜面反射带，保留干净可用的材质面。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
