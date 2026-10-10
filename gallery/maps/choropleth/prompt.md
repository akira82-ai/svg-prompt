# 区域指标分级设色 `静态` `2D`

分类：[地图与空间](../_about.md)

<img src="index.svg" width="720" alt="区域指标分级设色">

```
用 SVG 制作“区域指标分级设色”：部分欧洲国家 / 模拟服务可用率 %。
- 画布1400×900，背景#f3f5f7；标题34px、正文17–18px、刻度14–15px。重点结论：“颜色表达比率而非业务总量；灰色区域表示无示例数据”。
- 底图使用 assets/geography/western-europe.geojson，来源Natural Earth 1:110m Admin 0 countries，公共领域；不可手绘行政轮廓。来源：https://github.com/nvkelso/natural-earth-vector；许可：https://www.naturalearthdata.com/about/terms-of-use/。
- 示例只截取经度−12至20、纬度35至56的部分国家；等距圆柱投影标准纬线46°N，x=140+(lon+12)×23×cos46°，y=285+(56−lat)×23；使用SVG clipPath裁切，不作精确边界、面积或距离测量。
- 模拟比率：{"France": 68, "Germany": 82, "Spain": 55, "Portugal": 43, "Italy": 74, "Belgium": 64, "Netherlands": 91, "Switzerland": 78}；分档<60、60–74、75–89、≥90；其他国家灰色无数据。
- 分类色依次用映射值45/65/82/95生成，原始比率需在文本与data-value中保留；不得用总量填色比较不同面积国家。
- 页脚明确：“底图：Natural Earth 1:110m · 公共领域 · 部分国家裁切 · 业务数据为模拟”。
```
