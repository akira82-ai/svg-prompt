# 品牌动效片头 / Brand Intro Animation

分类：[品牌与排版](../_about.md)

<img src="index.svg" width="720" alt="品牌动效片头">

```
用 SVG 制作“品牌动效片头 / Brand Intro Animation”，采用NOVA示例品牌。
- 画布1400×900；背景#eef2f6、纸面#ffffff、正文#14263d、辅助文字#596b80、强调色#245ee8；顶部中英文标题，作品区域x64..1336、y200..820，页脚说明示例与印刷边界。
- 标识0..0.8s出现，字标0.8..2s揭示，完整NOVA组合与口号稳定；motion遮罩只播放一次，减少动效显示相同intro-final组合。
- NOVA共用标准矢量标识：6×6单位视图，路径 M0 0 L2 0 L6 4 L6 6 L4 6 L0 2 Z M4 0 L6 0 L6 2 Z M0 4 L0 6 L2 6 Z；字标N/O/V/A共用固定矢量轮廓，宽高266:60；不依赖字体重建字标。
- 其他标题采用系统无衬线或Georgia衬线回退；中英文字体由环境决定，不声称嵌入商业字体。
- 文字和样例值：["SVG / BRAND & TYPE", "NOVA / CONCEPT BRAND", "品牌动效片头", "Brand Intro Animation", "示例品牌与版式 · 字体依赖系统环境 · 印刷图仅为示意", "SVG-PROMPT", "MAKE WORK TRACEABLE", "标识 → 字标 → 稳定终帧"]。
- SMIL只播放一次，终帧稳定；减少动效隐藏motion并显示完整fallback，不能让品牌名或完整文案永久缺失。
```
