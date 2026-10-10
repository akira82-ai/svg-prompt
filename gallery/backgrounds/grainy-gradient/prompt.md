# 颗粒渐变 / Grainy Gradient

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="颗粒渐变">

```
用SVG绘制“颗粒渐变 / Grainy Gradient”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 细颗粒为渐变增加层次，标题区独立保证可读性。
- 渐变224b88→776aad→dc9a92，叠fractalNoise频率0.7、octaves3、seed29，深色颗粒透明度0.14；不声称消除AI味或保证消除色带。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">颗粒渐变 / Grainy Gradient</title><desc id="desc">细颗粒为渐变增加层次，标题区独立保证可读性。；渐变224b88→776aad→dc9a92，叠fractalNoise频率0.7、octaves3、seed29，深色颗粒透明度0.14；不声称消除AI味或保证消除色带。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 01</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">颗粒渐变</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Grainy Gradient</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0.0000" stop-color="#224b88"/><stop offset="0.5000" stop-color="#776aad"/><stop offset="1.0000" stop-color="#dc9a92"/></linearGradient></defs><rect x="64" y="190" width="1272" height="620" fill="url(#g)" /><defs><filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" seed="29" stitchTiles="stitch" result="noise"/><feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.06274509803921569 0 0 0 0 0.12549019607843137 0 0 0 0 0.2235294117647059 1 0 0 0 0"/></filter></defs><rect x="64" y="190" width="1272" height="620" fill="#102039" filter="url(#grain)" opacity="0.14"/></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">细颗粒为渐变增加层次，标题区独立保证可读性。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
