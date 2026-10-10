# 全息投影 / Holographic Projection

分类：[插画与场景](../_about.md)

<img src="index.svg" width="720" alt="全息投影">

```
用SVG绘制“全息投影 / Holographic Projection”。
- 1400×900画布，背景#101e30，正文#e5efff，强调色#70dddf；中英文标题，主体裁切在x64..1336、y190..810圆角区域。
- 投影底座、光束与线框球形成完整设备场景。
- 球体为抽象线框而非地理地图；仅外圈透明度6秒缓变，主体不闪烁、不扫描遮挡。
- 本作品为概念插画，不是科学仿真、地图或可操作界面。
- 动效只改变装饰层，不隐藏主体；CSS失效时静态画面完整；prefers-reduced-motion禁用动画。
- 以下为可复现的完整SVG几何与色彩参考，可直接保存查看，也可据此改写构图：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">全息投影 / Holographic Projection</title><desc id="desc">投影底座、光束与线框球形成完整设备场景。；球体为抽象线框而非地理地图；仅外圈透明度6秒缓变，主体不闪烁、不扫描遮挡。</desc><rect x="0" y="0" width="1400" height="900" rx="0" fill="#101e30" /><text x="64" y="65" fill="#e5efff" font-size="14" text-anchor="start">VECTOR STORIES / 08</text><text x="64" y="117" fill="#e5efff" font-size="34" text-anchor="start">全息投影</text><text x="1336" y="117" fill="#e5efff" font-size="20" text-anchor="end">Holographic Projection</text><defs><radialGradient id="halo"><stop stop-color="#70dddf" stop-opacity=".45"/><stop offset="1" stop-color="#70dddf" stop-opacity="0"/></radialGradient><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#b7d2eb"/><stop offset="1" stop-color="#f4d8b4"/></linearGradient><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="20"/></clipPath></defs><g clip-path="url(#stage)"><ellipse cx="700" cy="710" rx="310" ry="60" fill="#203950" /><ellipse cx="700" cy="700" rx="250" ry="40" fill="none" stroke="#70dddf" stroke-width="3"/><path d="M480 700L540 365H860L920 700Z" fill="#70dddf" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".06"/><circle cx="700" cy="442" r="210" fill="url(#halo)" /><circle cx="700" cy="442" r="155" fill="none" stroke="#70dddf" stroke-width="3"/><ellipse cx="700" cy="442" rx="50" ry="155" fill="none" stroke="#70dddf" stroke-opacity=".55" stroke-width="2"/><ellipse cx="700" cy="442" rx="105" ry="155" fill="none" stroke="#70dddf" stroke-opacity=".55" stroke-width="2"/><ellipse cx="700" cy="442" rx="150" ry="155" fill="none" stroke="#70dddf" stroke-opacity=".55" stroke-width="2"/><ellipse cx="700" cy="442" rx="155" ry="45" fill="none" stroke="#70dddf" stroke-opacity=".55" stroke-width="2"/><ellipse cx="700" cy="442" rx="155" ry="100" fill="none" stroke="#70dddf" stroke-opacity=".55" stroke-width="2"/><circle cx="700" cy="442" r="170" fill="none" class="pulse" stroke="#70dddf" stroke-width="2" opacity=".3"/></g><text x="64" y="857" fill="#b3c5da" font-size="16" text-anchor="start">投影底座、光束与线框球形成完整设备场景。</text><style>@keyframes breathe{50%{opacity:.6}}.pulse{animation:breathe 6s ease-in-out infinite}@keyframes drift{50%{transform:translateY(6px)}}.drift{animation:drift 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.pulse,.drift{animation:none}}</style></svg>
```
