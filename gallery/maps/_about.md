# 地图与空间 · maps

表达位置、地理分布、流向、覆盖与空间关系，共 12 张，按区域概览 → 点位与密度 → 事件 → 流向与拓扑 → 距离覆盖与楼层 → 多时刻对照排序。

**收录标准**：位置必须承担信息编码；区分真实地理、抽象布局和虚构米制空间。模拟业务数值明确标注；圆面积、线宽、色档与图例一致，动效不改变数据含义。

**底图来源**：`assets/geography/western-europe.geojson` 摘自 [Natural Earth 1:110m](https://github.com/nvkelso/natural-earth-vector)，[公共领域许可](https://www.naturalearthdata.com/about/terms-of-use/)。只含部分欧洲国家，采用标准纬线 46°N 的等距圆柱投影与固定窗口裁切，不能用于精确边界、面积或距离测量。

**空间约束**：区域格网不是行政地图；城市弧线不是实际路由；站间距不编码距离。园区图 X/Y 同米制比例；覆盖仅计算欧氏距离圆的并集，密度为显式点位的高斯核估计，均不代表现实风险、通行时间或服务容量。多时刻图共用空间分区和色域。

**维护**：修改 `scripts/build-maps.py` 后生成三件套，运行 `scripts/check-maps.py` 并检查浏览器显示；首页由 `scripts/build-readme.mjs` 更新。静态事件图与动效图保留同一快照，减少动效模式关闭强调圈。

**标签**：时间、空间形式与技术分别使用 `time`、`space`、`tech`；每张图只有一个主分类。
