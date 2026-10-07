# 线稿描边动画

> 难度 L2 · 咒语等级 L2

## 咒语

```
用 SVG 做一个描边动画：一个 {城市天际线} 的线稿被逐渐"画出来"。
要求：
- 单文件自包含，零 JS，动画用 CSS keyframes 实现
- 所有轮廓只用 stroke 绘制，fill:none，统一 stroke-width:{2}、stroke-linecap:round
- 每条 path 的 stroke-dasharray 等于自身长度，dashoffset 从满值补间到 0
- 各条 path 依次延迟 {0.3s} 开始描边，总时长 {6s}，动画结束后停留在线稿完成状态（forwards）
- 画布 {1000×700}，{深蓝夜色} 背景衬托 {浅金色} 线条
```

## 效果

![线稿描边动画](index.svg)

## 复现要点

- 关键约束是"dasharray 等于自身长度"——不强调这句，模型经常写死一个数字导致断线或出不了笔迹
- 需要手写复杂线稿时升级为 L3：先用脚本生成 path，再让模型套用本模板
- 在 GitHub README 的 `<img>` 中本条目的 CSS 动画可以正常播放；下载到本地双击打开效果相同
