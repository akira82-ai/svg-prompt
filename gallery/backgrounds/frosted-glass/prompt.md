# 磨砂玻璃 / Frosted Glass

分类：[背景与材质](../_about.md)

<img src="index.svg" width="720" alt="磨砂玻璃">

```
用SVG绘制“磨砂玻璃 / Frosted Glass”。
- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。
- 同一底图在玻璃外清晰、玻璃内模糊，边缘与白幕共同表达磨砂。
- 复用backdrop两次；内部先铺不透明底色遮住原始清晰层，模糊第二份后再裁切glass，stdDeviation18，内部白幕0.22；滤镜范围150%避免截断。不是backdrop-filter，也不能自动模糊外部网页。
- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。
- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。
- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">磨砂玻璃 / Frosted Glass</title><desc id="desc">同一底图在玻璃外清晰、玻璃内模糊，边缘与白幕共同表达磨砂。；复用backdrop两次；内部先铺不透明底色遮住原始清晰层，模糊第二份后再裁切glass，stdDeviation18，内部白幕0.22；滤镜范围150%避免截断。不是backdrop-filter，也不能自动模糊外部网页。</desc><rect x="0" y="0" width="1400" height="900" fill="#111e2d" /><text x="64" y="64" font-size="14" fill="#b5c7d9" text-anchor="start">SURFACE STUDIES / 09</text><text x="64" y="116" font-size="34" fill="#e9f0fa" text-anchor="start">磨砂玻璃</text><text x="1336" y="116" font-size="20" fill="#b5c7d9" text-anchor="end">Frosted Glass</text><defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)"><rect x="64" y="190" width="1272" height="620" fill="#283b5e" /><defs><g id="backdrop"><circle cx="430" cy="445" r="190" fill="#5eaac1"/><circle cx="990" cy="590" r="205" fill="#ad8cca"/><path d="M685 230L955 720H425Z" fill="#e7b17c"/></g><clipPath id="glass"><rect x="420" y="285" width="580" height="420" rx="28"/></clipPath><filter id="blur" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="18"/></filter></defs><use href="#backdrop"/><g clip-path="url(#glass)"><rect x="420" y="285" width="580" height="420" fill="#283b5e"/><use href="#backdrop" filter="url(#blur)"/><rect x="420" y="285" width="580" height="420" fill="white" fill-opacity=".22"/></g><rect x="420" y="285" width="580" height="420" fill="none" rx="28" stroke="#fff" stroke-opacity=".6" stroke-width="2"/><path d="M452 329H947" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/></g><text x="64" y="856" font-size="16" fill="#b5c7d9" text-anchor="start">同一底图在玻璃外清晰、玻璃内模糊，边缘与白幕共同表达磨砂。</text><style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style></svg>
```
