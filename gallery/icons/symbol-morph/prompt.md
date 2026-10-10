# 状态切换动效 / Animated State Transitions

分类：[图标与符号](../_about.md)

<img src="index.svg" width="720" alt="状态切换动效">

```
用 SVG 制作“状态切换动效 / Animated State Transitions”。
- 画布1400×900，背景#f2f5f9，正文#172b42，辅助文字#516478，强调色#245ee8；顶部中英文名称，主体y206..786，页脚y858。
- 图标使用24×24局部坐标，默认1.6单位描边、圆端点与圆拐角；symbol/use复用轮廓，颜色由currentColor继承。
- 两组有明确操作含义的状态过渡，一次播放后保持终态。
- 播放→暂停由三角形两条分段轮廓转换为双竖线；菜单→关闭保留两条对角线、中线收缩；对应路径指令一致，.6秒等待、.8秒过渡，fill=freeze；减少动效隐藏motion显示终态fallback。
- 可见文字：["VECTOR SYSTEMS / 12", "状态切换动效", "Animated State Transitions", "PLAY / PAUSE", "播放 → 暂停", "MENU / CLOSE", "菜单 → 关闭", "两组有明确操作含义的状态过渡，一次播放后保持终态。"]
逐一复现以下本页使用的符号路径（24×24 viewBox）：
```
