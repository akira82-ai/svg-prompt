# SMIL 动效面板 `SMIL 动效` `2D`

<img src="index.svg" width="720" alt="SMIL 动效面板">

```
用 SVG 做一块自包含动效面板（零 JS、零 CSS，动画全部用 SMIL <animate>/<animateTransform>/<animateMotion>）：
- 雷达扫描：扇形 <animateTransform type="rotate"> 绕中心匀速旋转，底下三圈同心圆网格 + 扫过余辉
- 引力轨道：小圆 <animateMotion> + <mpath href="#orbit"> 沿椭圆轨道转，中心放行星体
- 状态灯：三个圆 opacity 依次呼吸，begin 依次错开 0.3s
全部 repeatCount="indefinite"，画布 900×600 深色面板底。
```
