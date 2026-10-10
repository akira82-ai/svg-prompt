# 山间日出 / Mountain Sunrise

分类：[插画与场景](../_about.md)

<img src="index.svg" width="720" alt="山间日出">

```
用SVG绘制“山间日出 / Mountain Sunrise”。
- 1400×900画布，背景#edf2f5，正文#19344c，强调色#245ee8；中英文标题，主体裁切在x64..1336、y190..810圆角区域。
- 日出已经成立的静态构图，只有云层作缓慢的轻微漂移。
- 暖色太阳位于远山之后、近山之前，三层山体由浅到深；云层8秒上下6px，不循环昼夜变色。
- 本作品为概念插画，不是科学仿真、地图或可操作界面。
- 动效只改变装饰层，不隐藏主体；CSS失效时静态画面完整；prefers-reduced-motion禁用动画。
- 以下为可复现的完整SVG几何与色彩参考，可直接保存查看，也可据此改写构图：
<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">山间日出 / Mountain Sunrise</title><desc id="desc">日出已经成立的静态构图，只有云层作缓慢的轻微漂移。；暖色太阳位于远山之后、近山之前，三层山体由浅到深；云层8秒上下6px，不循环昼夜变色。</desc><rect x="0" y="0" width="1400" height="900" rx="0" fill="#edf2f5" /><text x="64" y="65" fill="#19344c" font-size="14" text-anchor="start">VECTOR STORIES / 12</text><text x="64" y="117" fill="#19344c" font-size="34" text-anchor="start">山间日出</text><text x="1336" y="117" fill="#19344c" font-size="20" text-anchor="end">Mountain Sunrise</text><defs><radialGradient id="halo"><stop stop-color="#70dddf" stop-opacity=".45"/><stop offset="1" stop-color="#70dddf" stop-opacity="0"/></radialGradient><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#b7d2eb"/><stop offset="1" stop-color="#f4d8b4"/></linearGradient><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="20"/></clipPath></defs><g clip-path="url(#stage)"><rect x="64" y="190" width="1272" height="620" rx="0" fill="url(#sky)" /><circle cx="850" cy="425" r="105" fill="#f6c582" /><path d="M64 635L360 350 530 565 745 370 1040 640 1336 465V810H64Z" fill="#91abb5" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /><path d="M64 760L445 480 670 690 935 540 1336 760V810H64Z" fill="#4d7880" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /><path d="M64 790Q380 710 680 790T1336 755V810H64Z" fill="#244f5b" stroke="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /><g class="drift" opacity=".8"><ellipse cx="320" cy="330" rx="100" ry="15" fill="#fff" /><ellipse cx="1120" cy="280" rx="130" ry="17" fill="#fff" /></g></g><text x="64" y="857" fill="#526778" font-size="16" text-anchor="start">日出已经成立的静态构图，只有云层作缓慢的轻微漂移。</text><style>@keyframes breathe{50%{opacity:.6}}.pulse{animation:breathe 6s ease-in-out infinite}@keyframes drift{50%{transform:translateY(6px)}}.drift{animation:drift 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.pulse,.drift{animation:none}}</style></svg>
```
