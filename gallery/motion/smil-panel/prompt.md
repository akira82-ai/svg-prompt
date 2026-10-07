# SMIL 动效面板

> 难度 L3 · 咒语等级 L2

## 咒语

```
用 SVG 做一块自包含动效面板（零 JS、零 CSS，动画全部用 SMIL <animate>/<animateTransform>/<animateMotion>）：
- 雷达扫描：扇形 <animateTransform type="rotate"> 绕中心匀速旋转，底下三圈同心圆网格 + 扫过余辉
- 引力轨道：小圆 <animateMotion> + <mpath href="#orbit"> 沿椭圆轨道转，中心放行星体
- 状态灯：三个圆 opacity 依次呼吸，begin 依次错开 0.3s
全部 repeatCount="indefinite"，画布 900×600 深色面板底。
```

## 效果

![SMIL 动效面板](index.svg)

## 复现要点

- 沿任意曲线运动用 animateMotion + mpath 引用现成 path，比重写坐标序列优雅得多
- SMIL 动画在 GitHub README 的 `<img>` 里照样播放——这是"单文件会动"的核心价值
