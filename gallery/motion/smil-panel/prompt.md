# SMIL 动效面板 `SMIL 动效` `2D`

<img src="index.svg" width="720" alt="SMIL 动效面板">

```
用 SVG 画一块深色动效展示面板（动画全部用 SMIL 实现）：
- 1200×800 深底四宫格，标题"SMIL 动效面板 — 不写一行 JS/CSS"+ Level 5b 副标题
- 雷达扫描：同心圆网格 + 旋转扫描扇形 + 绿/蓝/橙三颗闪烁目标点 + 十字准线
- 引力轨道：中心恒星（radial 渐变、r 26→31 呼吸）+ 两圈椭圆轨道 + 三颗行星（蓝 6s / 紫 11s / 青 11s 相位错开）
- 数据流水线：三条彩色管道（粗底线 + stroke-dashoffset 流动虚线 + animateMotion 光点巡游 + 右端接口框）
- 心电与脉冲：pathLength 归一 dashoffset 扫描心电线 + 同步光点 + 双脉冲环 + 心点变色
- 每卡底部等宽字注释，页脚两行
- 画布 1200×800
```
