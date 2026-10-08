# 线稿描边动画 `CSS 动效` `2D`

<img src="index.svg" width="720" alt="线稿描边动画">

```
用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐"画出来"。
要求：
- 单文件自包含，零 JS，动画用 CSS keyframes 实现
- 所有轮廓只用 stroke 绘制，fill:none，统一 stroke-width:{2}、stroke-linecap:round
- 每条 path 的 stroke-dasharray 等于自身长度，dashoffset 从满值补间到 0
- 各条 path 依次延迟 {0.3s} 开始描边，总时长 {6s}，动画结束后停留在线稿完成状态（forwards）
- 画布 {1000×700}，{深蓝夜色} 背景衬托 {浅金色} 线条
```
