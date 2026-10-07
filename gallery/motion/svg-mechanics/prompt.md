# SVG 黑科技四连 `SMIL 动效` `2D`

<img src="index.svg" width="720" alt="SVG 黑科技四连">

## 提示词

```
用 SVG 做"机制级技法"四联演示：
- 聚光灯：深色底 + 一段隐藏文字，用径向渐变亮斑作为 mask，<animateMotion> 让光斑水平扫过——只有光斑扫到处文字可见
- 路径形变：两条锚点数完全相同的 path，<animate attributeName="d" values="A;B;A"> 平滑变形
- 文字骑路径：一行文字 <textPath href="#curve"> 沿贝塞尔曲线排布
- 等距伪 3D：立方体与台阶用 30° 等距变换拼出一个小场景，三个面三种明度
画布 1200×900，深色底霓虹配色。
```
