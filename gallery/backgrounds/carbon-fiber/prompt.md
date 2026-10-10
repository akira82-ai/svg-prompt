# 碳纤维编织 / Carbon Fiber Weave

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="碳纤维编织">

```
用SVG绘制“碳纤维编织 / Carbon Fiber Weave”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 深色编织纹通过交替方向与细线高光获得层次。
- 32px单元分四块、水平与垂直纤维交错；这是平纹编织的视觉示意，不宣称2×2斜纹或真实碳纤维结构。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">碳纤维编织 / Carbon Fiber Weave</title><desc id="desc">深色编织纹通过交替方向与细线高光获得层次。；32px单元分四块、水平与垂直纤维交错；这是平纹编织的视觉示意，不宣称2×2斜纹或真实碳纤维结构。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 08</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">碳纤维编织</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Carbon Fiber Weave</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><rect x="64" y="190" width="1272" height="620" fill="#151e2a" /><defs><pattern id="carbon" width="32" height="32" patternUnits="userSpaceOnUse"><rect width="32" height="32" fill="#111923"/><path d="M0 0H16V16H0Z M16 16H32V32H16Z" fill="#2c3e50"/><path d="M2 4H14M2 8H14M2 12H14M18 20H30M18 24H30M18 28H30" stroke="#42596c" stroke-width="1"/><path d="M20 2V14M24 2V14M28 2V14M4 18V30M8 18V30M12 18V30" stroke="#253546" stroke-width="1"/></pattern></defs><rect x="64" y="190" width="1272" height="620" fill="url(#carbon)" /></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">深色编织纹通过交替方向与细线高光获得层次。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
