# 环境聚光 / Ambient Spotlight

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="环境聚光">

```
用SVG绘制“环境聚光 / Ambient Spotlight”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 大面积环境光为深色背景提供柔和的视觉中心。
- 偏移径向渐变以10秒上下12px缓移；没有隐藏内容和扫描交互，不声称聚光灯揭示文字。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">环境聚光 / Ambient Spotlight</title><desc id="desc">大面积环境光为深色背景提供柔和的视觉中心。；偏移径向渐变以10秒上下12px缓移；没有隐藏内容和扫描交互，不声称聚光灯揭示文字。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 04</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">环境聚光</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Ambient Spotlight</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><defs><radialGradient id="spot" cx=".35" cy=".3" r=".75" fx=".28" fy=".22"><stop offset="0.0000" stop-color="#5c8194"/><stop offset="0.5000" stop-color="#213c55"/><stop offset="1.0000" stop-color="#122238"/></radialGradient></defs><rect x="64" y="190" width="1272" height="620" fill="#122238" /><rect x="64" y="190" width="1272" height="620" fill="url(#spot)" class="drift"/></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">大面积环境光为深色背景提供柔和的视觉中心。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
