# 织物纹理 / Woven Fabric

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="织物纹理">

```
用SVG绘制“织物纹理 / Woven Fabric”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 平纹织物用经纬交错的明暗表达柔软纤维。
- 16×16单元，经纬线宽3、局部覆盖宽2；明确为风格化平纹，不把斜线图案称作针织。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">织物纹理 / Woven Fabric</title><desc id="desc">平纹织物用经纬交错的明暗表达柔软纤维。；16×16单元，经纬线宽3、局部覆盖宽2；明确为风格化平纹，不把斜线图案称作针织。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 07</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">织物纹理</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Woven Fabric</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><rect x="64" y="190" width="1272" height="620" fill="#e9e3d7" /><defs><pattern id="weave" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#e9e3d7"/><path d="M0 4H16M0 12H16" stroke="#cec6b7" stroke-width="3"/><path d="M4 0V16M12 0V16" stroke="#f8f4eb" stroke-width="3"/><path d="M0 4H8M8 12H16" stroke="#bfb6a5" stroke-width="2"/></pattern></defs><rect x="64" y="190" width="1272" height="620" fill="url(#weave)" /></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">平纹织物用经纬交错的明暗表达柔软纤维。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
