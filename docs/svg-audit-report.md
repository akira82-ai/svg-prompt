# SVG 图鉴全面检查报告

本次结论：图鉴的数量、统一风格和零脚本动效基础已经成立，但还没达到“每条提示词都能可靠复现、每张图都能直接复用”的质量。当前最值得投入的是正确性、提示词与作品对齐、缩略图可读性；不建议先继续扩充数量。

## 修复进度（批准修复后的更新）

以下正文保留初检记录，不能当成修复后的当前状态。本轮已处理 **1项P0、33项P1逐图问题**，并修复了部分P2细节；这不表示134项可选打磨建议全部实施。

- 展示与排版：磨砂玻璃XML、品牌规范重复ID与真实64/24尺寸、字标间距、统计单位、思维导图父子布局、霓虹深底/字距/字形倒影。
- 内容与编码：折线万人单位及日期锚点、气泡面积映射、实用字阶、包装安全线、仪表盘模拟声明及数值、地图统一模拟色阶/省格锚点/三档涟漪、树图无重叠分区、SVG与PNG有条件比较。
- 动画与数学：金额互斥切换、面积共享边界、点线与峰值标签同步、17字符打字与光标同步、雪景主体摇摆/雪花向下复位、同周期双粒子与到达闪光、de Casteljau逐层插值、Fibonacci相切圆弧与方块、傅里叶单一当前档、真实立方体逐帧投影、环面退化与自交边界。
- 时间轴：改为2001/2003/2008/2011/2016/2018六个可核实W3C标准里程碑，点亮时刻由节点在线上的位置计算。2016/2018是候选推荐，未称最终推荐或浏览器全面支持。
- 顺手打磨：五/六瓣花、待办日期与2/5进度、音乐播放/暂停与5首计数、分页可向前状态、维恩图容器边界、黄金板高光裁剪、月牙透明mask、HUD标题笔误、描线画布说明。
- 共性与文档：168张加入title/desc；分类边界和贡献指南与当前schema对齐；README重建仍为168条。

**已验证**：168 SVG XML、同图唯一ID、本地url引用、SMIL values/keyTimes数量与排序；Chromium独立img加载168/168、破图0；元数据按当前schema全部约束逐项检查（未安装标准JSON Schema验证器，未宣称标准验证器通过）；git diff --check通过。重点图使用独立SVG文档截图观察。金额139个边界时刻无重叠，傅里叶169个边界时刻恰有一条当前曲线，打字光标13个时刻与裁剪宽度一致；贝塞尔8个时刻与参数公式误差≤0.03画布单位，折线49次点到线距离≤0.3单位；Fibonacci方块无重叠、面积恰好覆盖34×21矩形。

**仍保留的可选/待验证事项**：全量prompt参数化、缩略图编辑取舍、材质艺术重画、68条减少动态静态状态、各类代表提示词的模型复现及Safari/Firefox/GitHub兼容性。这些没有冒充已经修复或验证；P2原始建议仍在逐图表中供后续打磨。

新增历史一手来源：[SVG Tiny 1.2](https://www.w3.org/TR/2008/REC-SVGTiny12-20081222/)、[SVG 1.1第二版](https://www.w3.org/TR/2011/REC-SVG11-20110816/)、[SVG 2 2016候选推荐](https://www.w3.org/TR/2016/CR-SVG2-20160915/)、[SVG 2 2018候选推荐](https://www.w3.org/TR/2018/CR-SVG2-20181004/)。

## 初检范围与证据边界

- 全量覆盖 `gallery/` 的 **8 类、168 条**：基础15、UI25、品牌15、图表26、信息可视化23、材质17、动效33、数学14。存档 `archive/demos/` 和模板不是图鉴条目，不计入。
- 每条读取 `meta.json`、`prompt.md`、`index.svg`；检查三件套、基本schema字段、目录slug、README收录、XML解析、同图ID和属性引用。
- 168张均在 Chromium 浏览器以独立 `<img>` 渲染检查；68条动态作品额外生成 **3.5秒、7秒** 的时间定位帧，重点核对中间态及循环差异。重点排版问题另按1200×800放大确认。全量图册以480px宽观察，README实际336px更小。
- 动画定位帧通过独立iframe里的SVG `setCurrentTime()`检查，不是逐帧录像；本报告不宣称验证了所有瞬间、全部循环接缝、性能或Safari/Firefox/GitHub代理兼容性。
- 未调用模型重新生成168份提示词，故“可复现同款”未被实证。数学类做模型/标注与明显几何检查，未逐一复算全部固化坐标。
- **事实**来自源文件、浏览器渲染或明确数值计算；**建议**是视觉/产品判断；**待核查**代表证据不足。逐图表的P级是处理先后，不是给作品打分，也不代表每张都有缺陷。
- 本次只交付此报告，不改图、不改提示词、不提交、不推送。

## 全量检查结果

| 项目 | 结果 | 含义 |
|---|---|---|
| 三件套、slug、README收录 | 168条齐全，未发现漏收或slug不一致 | 内容组织基础正常 |
| 基本schema字段/枚举检查 | 未发现字段缺漏或额外字段 | 尚未接入标准JSON Schema验证器，不等同完整schema测试 |
| XML合法性 | 167通过，1失败 | 磨砂玻璃确定破图 |
| 同图ID | 品牌规范页的lg5重复 | 当前可显示，不代表重复ID合法 |
| 属性中的本地引用 | 可解析167张未发现悬空引用 | 源码注释/图中文字里的示意url不算真实引用 |
| 时间标签 | 100静态、67 SMIL、1 CSS，与动画标记基本一致 | 没有发现static作品含明显动画标记 |
| SVG容量 | 总计1,416,402字节，约1.42MB；最大110,176字节 | 体积不算大，但不能宣称SVG普遍2–10KB；滤镜耗时不能只看字节 |
| SVG内可访问说明 | 168张均无title/desc | Markdown有alt，但单独复用SVG缺少内部文字说明 |
| 减少动态支持 | 68动态作品均未发现prefers-reduced-motion | 停止SMIL需专门策略，不能只加CSS就算完成 |
| 提示词变量位 | 168份均未使用贡献指南推荐的花括号占位 | 更像定稿展示咒语，换内容时需用户手改许多位置 |

## 优先处理的确定问题

P0表示不能正常展示；P1表示内容、数据、排版或承诺不一致；P2表示进一步打磨。这里优先列最有证据、收益最高的问题，其他在逐图表。

| 优先级 | 作品/范围 | 已确认事实与根因 | 建议及验收 |
|---|---|---|---|
| P0 | materials/frosted-glass | 三个circle把颜色写成裸属性，如`r="170" #4f8ef7`，XML在第1行第619列失败；img实际破图 | 改成合法fill属性；重新解析和独立img展示，两项都通过 |
| P1 | charts/number-roll | 不同金额文本淡出/淡入时间重叠，3.5秒及7秒出现叠字 | 同一时刻只允许一档数字可见，或做互斥离散切换；再检查每个切换边界 |
| P1 | charts/area-expand、line-draw | 面积、轮廓、点使用分别写死的关键帧；3.5秒面积线离开填充边界，折线点不随曲线移动 | 由同一帧数据生成全部几何，逐帧共享边界/点线距离为零 |
| P1 | branding/wordmark、infographics/stat-numbers、mind-map | N覆盖O；168覆盖单位；父节点覆盖叶节点 | 用字形边界/节点尺寸算间距，1200、720、336px逐级检查 |
| P1 | motion/neon-sign | 提示词深底，作品实际浅底，标题近白；倒影仅一个渐变矩形 | 恢复深底，校正文字光学居中及间距，倒影按灯牌轮廓翻转渐隐 |
| P1 | motion/typewriter、snow-globe、particle-collider | 光标无x动画；摇摆动画挂空g；对撞闪光是静态path | 分别把光标和字符进度共用时间、摇摆包住实际主体、闪光与粒子到达同步 |
| P1 | math/bezier-de-casteljau | 没有de Casteljau所需的逐级插值点/连线，只是控制线呼吸与沿曲线走点 | 用同一t计算Q0/Q1/Q2→R0/R1→B，或如实改名 |
| P1 | math/golden-spiral | 四分之一圆弧在连接处反向尖折；1×1方块落入13×13方块区域 | 先生成正确Fibonacci方块拓扑再生成切向连续圆弧，明确只是黄金螺旋近似 |
| P1 | charts/line、line-draw、bubble | 万人轴峰值32却标3.2w；气泡图例面积比不匹配10/50/100 | 单位统一；气泡半径由平方根映射数据；同时补轴名 |
| P1 | branding/packaging-dieline、type-scale | 内缩红线被叫出血；五级字号并非1.333的等比字阶 | 区分外出血/内安全线；改成真实字阶描述或按倍率重算 |
| P1 | charts/dashboard、infographics/live-ops-dashboard | KPI内容与提示词不同；动态大屏承诺的数字滚涨/跑马灯实际不存在 | 对齐提示词与作品，保留模拟声明；不为迎合标题增加不必要的动效 |
| P1 | infographics/timeline-svg、timeline-reveal、china-grid-map | SVG1.1年份错误；GDP最浅色块与高值榜单冲突且无年份来源 | 改时间轴并引用一手来源；GDP示例给统一阈值、年份/来源或标虚构 |

SVG历史一手核对：W3C [SVG 1.0推荐规范，2001-09-04](https://www.w3.org/TR/2001/REC-SVG-20010904/)与[SVG 1.1推荐规范，2003-01-14](https://www.w3.org/TR/2003/REC-SVG11-20030114/)。PGML1996本轮未获取到有效一手页面，保留为待核查，不编造替代年份。

## 分类层面的建议

| 分类 | 现状判断 | 建议边界与打磨重点 |
|---|---|---|
| 基础图形 · 15 | 风格最统一，但多数带语法和教学说明；与“非教程图”收录方向有张力 | 明确允许几何本体教学图；基础几何优先，对circle/line等保留简洁对照，减少长段代码说明 |
| UI组件 · 25 | 组件规格图＋整机原型＋加载动效三种层次；整体可看，但不能把img当交互控件 | 收录标准改为“界面视觉/状态参考”；原型仍留UI分类，标签区分组件/状态规格/原型，复杂度递进 |
| 品牌排版 · 15 | NOVA星芒贯穿，有一致品牌系统 | 保留统一品牌案例，修字标/字阶/印刷错误；提示词开放品牌名、配色、文案，避免所有示例只能产NOVA |
| 图表报表 · 26 | 标准统计图与告警灯/加载式动效混在一起 | 以数值比较、趋势、分布为主；dashboard留此类，alert/status偏监控展示可标用途；先确保数据编码 |
| 信息可视化 · 23 | 关系/流向/层级作品符合方向，但混入两张经营/运维仪表盘 | 架构/流程/地图/桑基留此类；BI/运维仪表盘建议归charts，现有分类简介同时修正 |
| 实物模拟 · 17 | 纯SVG材质方向明确，部分更像抽象纹理 | 先修破图；木、锈、石、水滴加强可辨识特征；光源只要求适用的拟真作品，不强迫图案纹理虚构光源 |
| 动效艺术 · 33 | 覆盖丰富，有可保留代表作；部分教学底注和小主体稀释效果 | 装饰动画强调完成态、节奏、接缝；UI加载器仍归UI；用途与技巧做标签，减少新分类 |
| 高级数学 · 14 | 参数曲线/分形丰富，但“数学正确”与“技术演示”混用 | 收录标准落实模型、参数、采样、投影、误差；修黄金螺旋与构造动画，拓扑退化明确边界 |

分类根因：`charts/_about.md`写“架构图、流程图”，`infographics/_about.md`又说“系统架构图归此类”，互相争范围。建议只改定义和少量归属，不新建更多目录。`CONTRIBUTING.md`宣称五维标签含difficulty/spellLevel，但schema没有这两字段且additionalProperties=false；先决定是否真要这两维，不用则同步删文档承诺，要用才改schema/展示流程。

## 共性打磨策略

1. **先把看图和读说明分开。** 1200宽原图在README压到336宽，14px说明变成3.92px、28px标题变成7.84px；1600宽架构图更吃亏。主页图旁已有标题，SVG里不必再堆教学长句。缩略图负责辨认主题，720px详情负责读标注，提示词承载参数。不是把所有字粗暴放大，而是减少缩略图必须阅读的文字。
2. **同一份数据生成所有位置。** 图表的path、点、填充、标签、计数器，数学动画的t参数、光点和辅助线不能各自手写。可离线生成后固化，继续保留零JS成品。树图与架构图采用成熟布局算法/现有工具生成坐标，再做必要的视觉调整。
3. **提示词从“风格要求”补到“可验收规格”。** 给`{标题}`、`{数据}`、`{配色}`，写画布、结构、关键参数、动画时序、输出独立SVG、禁止外部资源、验收条件。数学例补完整公式；图表例给数据表，避免让模型凭视觉猜数。
4. **模拟信息如实标注。** LIVE、实时、GDP、全球出货、12种动效/5轮终审等，当前有些无数据源或口径。示意图写模拟，事实数据给年份与来源。“此前不存在”“任意模型复现”等仓库主张也需要证据或收窄。
5. **减少动态要有可读静态状态。** 动态初始为空可作为入场设计，不是自动判坏；但停止动画/截封面时要有代表性图形。CSS与SMIL分别处理，验收减少动态模式时仍可见、可理解。
6. **保持“一图三件套”，别先重构站点。** 当前源目录结构很好。先把XML解析、meta标准schema、唯一ID、真实属性引用、图表比例、prompt对齐加入现有校验流程；报告没有建议为此马上改CI或搭网站。
7. **SVG复用先明确方式。** 作为img可保留alt；单独素材可加title/desc；多SVG内联时ID需命名空间。带展示背景/大段说明的图应叫展示图，不能暗示下载即产品组件。

## 168条逐图检查与建议

每行的作品链接指向原SVG；同目录的prompt.md/meta.json是该行文案核对依据。P2多数是可选优化，已有优点建议保留，不要求全部重画。所有行同时适用上面的缩略可读性与提示词参数化建议，以下只写各自最值得处理的点。

### 基础图形（15张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [箭头家族 · arrows](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/arrows/index.svg) | P2 | 箭头方向表现清楚；减少底部小字，把 marker 与手绘箭头的区别写进提示词验收条件。 |
| [相减与挖洞 · boolean-shapes](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/boolean-shapes/index.svg) | P2 | 月牙目前是背景色覆盖，不是真正透明相减；明确示意版与可复用透明素材的区别，复用版用 mask。 |
| [圆 circle · circle](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/circle/index.svg) | P2 | 半径、同心圆层次清楚；放大属性说明，三种状态统一对齐。 |
| [椭圆 ellipse · ellipse](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/ellipse/index.svg) | P2 | 比例递进清楚；保持同一 rx 或同一面积再改 ry，能更直观比较扁率。 |
| [渐变球体 · gradient-spheres](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/gradient-spheres/index.svg) | P2 | 球体高光成立；添加光源箭头，提示词明确各球共用光源方向，减少公式说明占位。 |
| [直线 line · line](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/line/index.svg) | P2 | 线帽对比成立；三种 linecap 加共用端点参考线，才能看出 square/round 超出端点的区别。 |
| [路径 path · path](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/path/index.svg) | P2 | 六命令结构清楚；A 卡补 large-arc-flag/sweep-flag 的具体值，别只给省略语法。 |
| [多边形 polygon · polygon](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/polygon/index.svg) | P2 | 开放/闭合区别清楚；最后一条边与起点说明统一位置，明确闭合的是末点→首点。 |
| [折线 polyline · polyline](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/polyline/index.svg) | P2 | 主图可保留；右卡的趋势曲线与基础分类边界略混，改成无数据语义的折线变体更一致。 |
| [矩形 rect · rectangle](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/rectangle/index.svg) | P1 | 胶囊提示词“rx≥宽高一半”表述不严谨，130×110 又接近椭圆；明确 rx/ry 的半宽半高限制，做宽度明显大于高度的胶囊。 |
| [正多边形家族 · regular-polygons](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/regular-polygons/index.svg) | P2 | 家族排列清楚；补顶点公式 x=cx+Rcosθ、y=cy+Rsinθ 及起始角，方便复现。 |
| [旋转复制组合 · rotational-patterns](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/rotational-patterns/index.svg) | P2 | 三例辨识度好；把孔做成透明挖洞，说明 use/rotate 复用单元的方式。 |
| [螺旋与波浪 · spirals-and-waves](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/spirals-and-waves/index.svg) | P2 | 曲线可保留；补 a、A、ω、采样区间和步长，当前数学公式不能唯一确定图形。 |
| [星形与花形 · stars-and-flowers](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/stars-and-flowers/index.svg) | P1 | 提示词要求五瓣圆角花和下方六瓣花，实际圆角形更像四尖星；核对路径瓣数并让名称、提示词与作品一致。 |
| [透明叠色 · transparency-blend](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/basics/transparency-blend/index.svg) | P2 | 透明度对比成立；说明普通 alpha 叠色受绘制顺序影响，别让它看起来像加法 RGB 混色。 |

### UI组件（25张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [消息提示条 · alerts](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/alerts/index.svg) | P2 | 四语义态清楚；增加紧凑组件尺寸要求和可替换消息占位，说明展示图不等于可交互组件。 |
| [音频波形 · audio-wave](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/audio-wave/index.svg) | P2 | 中心线伸缩成立；主体过小、留白过大，可提高条高；装饰音频动画与真实输入音量需区别。 |
| [头像与徽章 · avatar-badge](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/avatar-badge/index.svg) | P2 | 徽章贴边方式不错；数字变化给99+方案，在线/离线文字保持同等可读性。 |
| [按钮四态 · buttons](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/buttons/index.svg) | P2 | 八状态完整；四态是并列展示而非真实hover，提示词明确；给focus-visible视觉与最小尺寸建议。 |
| [聊天 IM · chat-messenger](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/chat-messenger/index.svg) | P2 | 双屏流程完整；缩略图文字过密，放大手机或突出一屏，消息用占位内容，统一列表行高。 |
| [复选与单选 · checkbox-radio](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/checkbox-radio/index.svg) | P2 | 状态逻辑清楚；加禁用态与焦点态的提示词约束，实际产品仍需要HTML语义控件。 |
| [标签 Chips · chips](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/chips/index.svg) | P2 | 变体丰富；删除/添加的说明字偏小，统一胶囊高、内边距与图标尺寸，内容替换给占位符。 |
| [下拉菜单 · dropdown](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/dropdown/index.svg) | P2 | 展开与状态对照好；层级间距和禁用文本对比再调，说明它是示意图，不具有键盘导航。 |
| [电商首页 · ecommerce-home](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/ecommerce-home/index.svg) | P2 | 首页布局完整；商品图是占位几何，应如实称界面原型，缩略图用更大的商品与价格焦点。 |
| [卡片与阴影层级 · elevation](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/elevation/index.svg) | P2 | 四阴影递进合理；固定同一物体/背景及光源，阴影参数加入提示词，避免仅写小/中/大。 |
| [健身数据 · fitness-dashboard](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/fitness-dashboard/index.svg) | P2 | 三环和本周柱图层级不错；补每环目标/实际数，今天柱与日期口径统一，图表缩略尺度偏小。 |
| [渐变与玻璃质感 · glassmorphism](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/glassmorphism/index.svg) | P2 | 品牌感较强，可保留；玻璃卡是半透明叠加并非通用backdrop-filter，说明blur背景层的实现边界。 |
| [不确定进度条 · indeterminate-progress](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/indeterminate-progress/index.svg) | P2 | 轨道内裁剪成立；光条与加载说明可放大，设置代表性首帧，停止动画时仍有可见状态。 |
| [输入框状态 · input-states](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/input-states/index.svg) | P2 | 四状态基本完整；聚焦与错误提示层级可读，提示词补标签/帮助文案占位和长文本裁剪要求。 |
| [音乐播放器 · music-player](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/music-player/index.svg) | P2 | 深浅双屏风格统一；第一首播放中却播放页主控为播放三角，统一播放/暂停语义；5首歌曲与底部迷你播放条拉开层级。 |
| [分页器 · pagination](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/pagination/index.svg) | P2 | 当前页3辨识明确；下方“上一页”置灰但当前非第一页，若代表禁用案例需单独说明，别与上方页码逻辑冲突。 |
| [进度条与滑块 · progress-slider](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/progress-slider/index.svg) | P2 | 25/60/90%基本匹配条长；滑块固定40%属静态示意，补可替换数值/轨道宽度的计算关系。 |
| [骨架屏微光 · skeleton-shimmer](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/skeleton-shimmer/index.svg) | P2 | 扫光成立；范围覆盖到整个骨架外框而非只占位块，若要求“所有占位块”，用联合clip严格裁剪。 |
| [加载器三连 · spinners](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/spinners/index.svg) | P2 | 三加载动效可保留；提示词时长与实际各条标注统一，增加静态/减少动态时仍可识别的默认图形。 |
| [标签页与分段控件 · tabs](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/tabs/index.svg) | P2 | 下划线与分段控件清楚；上方说明文字占比偏高，改为更紧凑组件示意，补激活状态切换约束。 |
| [待办清单 · todo-today](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/todo-today/index.svg) | P1 | 完成5/8但只展示2条完成、3条进行中且未说明隐藏；标“仅展示部分任务”或补齐，周三10月8日若指2026则不对，需明确年份。 |
| [开关 Toggle · toggle](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/toggle/index.svg) | P2 | 大小开关清楚；统一手柄与轨道端部安全间距，提示词给尺寸和缩放公式。 |
| [开关拨动动画 · toggle-animated](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/toggle-animated/index.svg) | P2 | 同步位移与颜色成立；线性来回更像摆动，改成端态停留＋快速切换，更符合开关操作节奏。 |
| [工具提示 Tooltip · tooltip](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/tooltip/index.svg) | P2 | 两方向示意完整；箭头与按钮中心精确对齐，浅色变体边框略弱，长文案设最大宽度和换行。 |
| [打字指示器 · typing-indicator](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/ui/typing-indicator/index.svg) | P2 | 呼吸点有节奏；主体偏小，建议紧凑viewBox/更大展示倍率，明确三点亮暗相位与循环。 |

### 品牌排版（15张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [App 图标 · app-icon](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/app-icon/index.svg) | P2 | 四图标辨识度好；网格示意不能替代平台规范，明确“示意网格”，可复用部分去掉展示卡和说明。 |
| [品牌规范页 · brand-guidelines](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/brand-guidelines/index.svg) | P1 | 同一 SVG 重复定义 lg5；去重并核对 64/24px 标签与真实几何尺寸，安全区 x 要与最小尺寸用同一尺度。 |
| [品牌色板 · brand-palette](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/brand-palette/index.svg) | P2 | 色板系统可保留；补文字/背景组合的对比度验证，百分比写明是推荐使用占比。 |
| [名片正反面 · business-card](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/business-card/index.svg) | P2 | 正反面组织清楚；示例联系方式用占位符，明确 90×54mm 是本案例尺寸，补出血和安全边距。 |
| [圆形徽章 · circular-badge](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/circular-badge/index.svg) | P2 | 三版本识别清楚；检查字体替换后的环形文字接缝，提示词给 startOffset、字距和文字长度。 |
| [单色图标系统 · icon-set](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/icon-set/index.svg) | P2 | 整体笔触统一；currentColor 优点已有，提示词再明确图标单体导出时保留 24×24 viewBox。 |
| [Logo 网格构图 · logo-grid](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/logo-grid/index.svg) | P2 | 网格、成品与安全距离组合好；明确网格是构形约束还是展示辅助，避免事后套圆就叫精确构图。 |
| [包装展开图 · packaging-dieline](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/packaging-dieline/index.svg) | P1 | 红虚线位于刀线内侧却标“出血3mm”；应区分外侧出血与内侧安全线，当前图无尺寸验证，改掉“印刷厂看左边”的可生产暗示。 |
| [图案平铺 · pattern-tile](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/pattern-tile/index.svg) | P2 | 平铺与反白展示清楚；增加接缝验收条件，明确 patternUnits、单元尺寸和可替换配色。 |
| [品牌海报 · poster](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/poster/index.svg) | P2 | 主体海报视觉不错；右侧缩略尺寸太小，增加 A 系列比例说明，展示缩略图不当作实际印刷尺寸。 |
| [社媒套件 · social-kit](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/social-kit/index.svg) | P2 | 底部左侧确有150×150方形帖子缩略图，符合提示词；但1080×1080标签远在通栏右侧，移到方形旁，避免把整个横条误认成帖子。 |
| [贴纸包 · sticker-pack](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/sticker-pack/index.svg) | P2 | 八枚造型够丰富；统一白色切边粗细、光源方向和安全间距，让最底两枚不显得拥挤。 |
| [文字特效四连 · type-effects](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/type-effects/index.svg) | P1 | mask 镂空实现是字内透出白底，提示词却写“字内透出渐变”；统一意图并移除未使用 cutout 定义。 |
| [字阶系统 · type-scale](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/type-scale/index.svg) | P1 | 48→32→24→15→12 的倍率分别1.5/1.333/1.6/1.25，不能笼统标相邻级差≈1.333；改成实际字阶或重算字号。 |
| [字标 Wordmark · wordmark](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/branding/wordmark/index.svg) | P1 | 放大确认 N 压住 O 圆环，O→VA 间距又偏大；按字形边界重新定位并校准视觉居中。 |

### 图表报表（26张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [告警闪烁 · alert-blink](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/alert-blink/index.svg) | P2 | 告警识别明确；保留常亮可读底层，闪烁只用于强调层，别让文字随整体透明度变淡。 |
| [面积图 · area](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/area/index.svg) | P2 | 堆叠关系清楚；提示词补两系列原始数组和 y 上限，图区加示例数据说明。 |
| [面积展开动画 · area-expand](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/area-expand/index.svg) | P1 | 3.5秒帧描边与面积边界明显分离，两个面积共享边界也未同步；由同一组帧数据同时生成填充和描边。 |
| [柱状图 · bar](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/bar/index.svg) | P2 | 分组与堆叠都有；左右系列配色、年份顺序统一，提示词给完整数据表和轴上限。 |
| [柱状生长动画 · bar-growth](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/bar-growth/index.svg) | P2 | 播放后柱与数值可见；循环开始为空属于设计选择，建议底层留淡柱轮廓，并让标签显示与柱顶位置共用数据。 |
| [气泡图 · bubble](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/bubble/index.svg) | P1 | X/Y轴无指标名导致不可解释；10/50/100图例半径8/13/18，面积比约1:2.64:5.06而非1:5:10；使用 r=k√value。 |
| [子弹图 · bullet-chart](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/bullet-chart/index.svg) | P2 | 实际/目标结构成立；三个指标单位不同，明确各自量程和定性区间含义，避免仅凭条长跨指标比较。 |
| [双轴组合图 · combo-dual-axis](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/combo-dual-axis/index.svg) | P2 | 两轴颜色对应清楚；给左轴、右轴固定域和原始数据，提示双轴只能看各自趋势，避免制造相关性。 |
| [数据可视化仪表盘 · dashboard](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/dashboard/index.svg) | P1 | 提示词订单8432/客单价152，作品却为38209/支付转化率3.86%；“近7日”图有8日期，LIVE每60s刷新无数据接入，统一内容并标模拟。 |
| [环形扫描动画 · donut-sweep](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/donut-sweep/index.svg) | P2 | 完成态68%与440/648四舍五入吻合；quarterly与年度目标口径冲突，统一周期，初始保留淡数字或说明。 |
| [漏斗图 · funnel](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/funnel/index.svg) | P2 | 各层底宽约按10000/4200/1800/1200/400编码，但梯形上宽沿用前一层下宽；明确“底宽代表本阶段”，否则读者会比较梯形面积或上宽。 |
| [漏斗逐层动画 · funnel-steps](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/funnel-steps/index.svg) | P2 | 分层入场成立；与静态漏斗统一编码方式，数值和转化率用同一数据计算，保持完成态足够久。 |
| [甘特图 · gantt](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/gantt/index.svg) | P2 | 任务、负责人、今日线清楚；日期使用真实起止日期或明确“项目第N天”，避免0日让人误解。 |
| [甘特推进动画 · gantt-progress](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/gantt-progress/index.svg) | P2 | 任务生长成立；增长的是计划时间长度，不等于完成进度；若叫推进，另画已完成比例与计划底条。 |
| [仪表指针动画 · gauge-swing](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/gauge-swing/index.svg) | P2 | 完成指针约对应68%，未确认读数错误；初始指针在表盘外侧，建议从0刻度入场，把数字移出扫针范围。 |
| [日历热力图 · heatmap](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/heatmap/index.svg) | P2 | 140格结构完整；补强度阈值、日期起点和缺失值说明，别只写少/多。 |
| [直方图与箱线图 · histogram-boxplot](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/histogram-boxplot/index.svg) | P2 | 双图对照能保留；提示词补同一批样本数据与分箱规则，明确 min/max 是样本极值还是箱线图须端。 |
| [KPI 指标卡 · kpi-cards](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/kpi-cards/index.svg) | P2 | 卡片层级好；收益/退款/投诉的好坏方向由业务语义控制，补时间窗口和同比/环比口径。 |
| [折线图 · line](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/line/index.svg) | P1 | Y轴单位万人、峰值落在32附近，提示气泡却写3.2w（3.2万人）；修正10倍单位差，勿只修改配色。 |
| [折线描线动画 · line-draw](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/line-draw/index.svg) | P1 | 同样有峰值3.2w与32万人不一致；曲线d在动、数据点cy固定，播放后会偏离，点、线、气泡需同步。 |
| [实时数据流 · live-stream](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/live-stream/index.svg) | P2 | 流动示意能看出；“实时监控”实际是预置循环路径，标模拟数据，并给时间/数值轴或明确仅为装饰波形。 |
| [数字滚动动画 · number-roll](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/number-roll/index.svg) | P1 | 3.5/7秒帧出现前后数字重叠；各档淡出与下一档淡入交叉造成，改成互斥切换；84257与增量8914对应约11.83%，不是12.4%。 |
| [饼图与环形图 · pie-donut](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/pie-donut/index.svg) | P2 | 三种占比图可保留；补类别名称和数值映射，提示词说明弧段比例与合计100%的验收方法。 |
| [雷达图 · radar](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/radar/index.svg) | P2 | 两系列区分明确；补刻度范围、量纲标准化方法，避免不同指标直接用同一半径比较。 |
| [散点图 · scatter](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/scatter/index.svg) | P2 | 散点、回归线、离群点结构完整；补原始点集和拟合方法，当前虚线不能证明统计回归成立。 |
| [状态灯巡检 · status-patrol](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/charts/status-patrol/index.svg) | P2 | 服务异常不只依赖颜色，已有文字/延时；减弱正常灯呼吸，突出异常并标模拟巡检。 |

### 信息可视化（23张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [动态架构图 · animated-architecture](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/animated-architecture/index.svg) | P2 | 内容丰富、数据包可见；先保留静态路由可读性，再减少同时运动的链路，补节点坐标/链路表到提示词。 |
| [浅色 BI 经营盘 · bi-dashboard](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/bi-dashboard/index.svg) | P2 | 布局是本类较成熟的一张；筛选栏是静态示意，注明无真实查询；KPI、订单、客单价用同一示例数据口径。 |
| [地理填色图 · china-grid-map](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/china-grid-map/index.svg) | P1 | GDP榜中粤/苏最高，色块却是最浅档；图例高→待发展也由浅到深，与提示词相反；统一阈值，并给年份/来源或标虚构示例。 |
| [弦图 · chord-diagram](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/chord-diagram/index.svg) | P2 | 弧带关系直观；“迁徒”改“迁徙”，提示词给城市流量矩阵并让弧段/带宽都由流量计算。 |
| [对比信息图 · comparison-vs](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/comparison-vs/index.svg) | P1 | SVG体积2–10KB、PNG数百KB、SVG可索引/PNG不可都过度绝对；本库SVG已到110KB，改为有条件比较，说明滤镜导出也会栅格化。 |
| [深色监控大屏 · dark-ops-dashboard](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/dark-ops-dashboard/index.svg) | P2 | 一屏九区层次好；虽列深色监控大屏，meta标SMIL且有动画，应在标题/说明里明确微动效；区域点阵补地域图例。 |
| [决策流程图 · decision-flowchart](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/decision-flowchart/index.svg) | P2 | 正交主流程能读懂；两个“否”回路补明确箭头、汇入点和标签，避免靠位置猜回哪一步。 |
| [动态大屏 · live-ops-dashboard](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/live-ops-dashboard/index.svg) | P1 | 提示词承诺KPI逐级滚涨和告警跑马灯，源码KPI和告警文本均静态；补动效或如实收窄提示词，纠正左右面板位置描述。 |
| [地图涟漪 · map-ripple](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/map-ripple/index.svg) | P1 | 提示词六城市、实图五城市；城市光点与对应省份块脱离，大小图例只有一句话；建立省块→城市锚点，再补三档具体值。 |
| [思维导图 · mind-map](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/mind-map/index.svg) | P1 | 生态/AI分支的叶节点被父节点遮住，左侧节点越出白卡边缘；重算父子间距，保留六主分支但统一安全边距。 |
| [网络脉冲 · network-pulse](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/network-pulse/index.svg) | P2 | 十节点网络成立；补边表和布局约束，静态底边对比度略低，脉冲不应替代关系本身。 |
| [组织架构图 · org-chart](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/org-chart/index.svg) | P2 | 三层层级好理解；成员小字与下层连线偏弱，放大职位文字、缩小多余留白。 |
| [过程图解 · process-steps](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/process-steps/index.svg) | P2 | 四步逻辑清楚；卡片之间几乎无间距，箭头偏小，拉开卡片间隙并放大步骤连接。 |
| [流程行进 · process-walk](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/process-walk/index.svg) | P1 | 提示词写带分支决策图，实际只有串行节点，且主线无方向箭头；补分支/失败回环或改成直线流程演示。 |
| [桑基图 · sankey](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/sankey/index.svg) | P2 | 收入25000+8000+4000与支出8000+5000+12000+12000都合计37000；可保留，中央标签加留白，提示词明确统一宽度比例。 |
| [桑基流动 · sankey-flow](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/sankey-flow/index.svg) | P2 | 流动中线可见；来源汇聚后多色飘带容易被读成直接来源→去向，明确混合规则，保持数值守恒。 |
| [数字统计图 · stat-numbers](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/stat-numbers/index.svg) | P1 | “168”和“条提示词”实际重叠；12种动效/5轮终审没有可核对定义或记录，“每条都能复现”未验证；改动态计数或标统计口径。 |
| [旭日图 · sunburst](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/sunburst/index.svg) | P2 | 主类合计100%，子类加总匹配主类；“其他”只一子类与提示词每类2–3段不符，说明例外并标虚构数据。 |
| [复杂系统架构图 · system-architecture](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/system-architecture/index.svg) | P2 | 主层次完整；提示词要求浅色分区，实际是深色系统图；节点名、OPS侧栏布局需要更具体才能复现同结构。 |
| [时间轴点亮 · timeline-reveal](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/timeline-reveal/index.svg) | P1 | 复用静态历史时间轴的年份问题；先纠正文案，再把线到达时刻与事件亮起同步，别在动画中传播错误年份。 |
| [SVG 简史时间轴 · timeline-svg](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/timeline-svg/index.svg) | P1 | 2001标SVG1.1有误：W3C的SVG1.0推荐为2001-09-04，SVG1.1为2003-01-14；PGML1996和“2023全面支持”需另核来源。 |
| [树状图 Treemap · treemap](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/treemap/index.svg) | P1 | 一级面积占比基本匹配标签，但子型号块互相重叠且未铺满父块（首两块重叠17单位）；按层级分区生成，补虚构数据说明。 |
| [维恩图 · venn-diagram](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/infographics/venn-diagram/index.svg) | P2 | 七区域文案齐全；下方商业圆越出白色卡片，缩小三圆或扩大容器，使留白一致。 |

### 实物模拟（17张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [金属拉丝 · brushed-metal](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/brushed-metal/index.svg) | P2 | 横向拉丝辨识清楚；高光与铆钉的光源统一，参数卡缩略图不可读，减少文字并把参数放入提示词。 |
| [碳纤维 · carbon-fiber](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/carbon-fiber/index.svg) | P2 | 当前更像小棋盘而非连续斜纹束；增加同向纤维线和跨单元斜向连续性，降低格子感。 |
| [混凝土 · concrete](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/concrete/index.svg) | P2 | 墙面颗粒不错；裂纹对比度过弱且缺少提示词要求的明显分叉，给裂纹粗细与分叉位置。 |
| [织物 · fabric](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/fabric/index.svg) | P2 | 针织/亚麻双区可保留；补真实比例尺度与接缝细节，当前浅线在缩略图上几乎消失。 |
| [滤镜材质特效 · filter-materials](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/filter-materials/index.svg) | P2 | 四滤镜演示有价值；水波文字位移偏强导致难读，降低 displacement 幅度；液态融合验收看两球实际接触的帧。 |
| [磨砂玻璃 · frosted-glass](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/frosted-glass/index.svg) | P0 | 三颗circle写成 r="170" #4f8ef7 这类非法属性，缺 fill=；独立XML解析失败且img破图，先修语法再谈质感。 |
| [黄金质感 · gold](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/gold/index.svg) | P2 | 金色梯度效果成立；斜高光未被金板裁剪、露出板外，文字更像印刷而非刻入，补高光clip与微弱刻字阴影。 |
| [噪点渐变 · grainy-gradient](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/grainy-gradient/index.svg) | P2 | 噪点层次明显；颗粒稍强，可降低叠加透明度并让对比小卡使用完全一致底色与尺寸。 |
| [牛皮纸 · kraft-paper](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/kraft-paper/index.svg) | P2 | 色温合适；纤维不够明显、咖啡渍太规整，加入非均匀边缘和细纤维，避免只是棕色渐变。 |
| [熔岩 · lava](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/lava/index.svg) | P2 | 裂缝辨识强，但橙色面积很大；增加暗岩壳比例、收细熔光，seed步进的跳变需在真实播放中确认。 |
| [大理石 · marble](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/marble/index.svg) | P2 | 目前主要像模糊云纹，深色静脉纹太弱；加强低频长纹的连续走向，金纹局部自然分叉。 |
| [平铺图案 · pattern-fill](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/pattern-fill/index.svg) | P2 | 三尺度比对不错；比例标签被繁密底纹干扰，补纯色小底牌并说明这是图案材质，与品牌平铺的用途边界。 |
| [铁锈 · rusted-iron](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/rusted-iron/index.svg) | P2 | 锈斑过于均匀，像砂土；加入大尺度裸铁区和局部锈斑聚集，刮痕要有高光/暗边。 |
| [程序化星空 · starry-sky](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/starry-sky/index.svg) | P2 | 满版氛围较成熟，可保留；提示词给seed与亮星坐标，保证随机纹理可复现。 |
| [水滴特写 · water-drop](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/water-drop/index.svg) | P2 | 主水滴更像悬浮球，椭圆投影与滴体分离；压低滴形、贴合叶面，强调接触边缘和背景折射。 |
| [水面波光 · water-shimmer](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/water-shimmer/index.svg) | P2 | 动效可见但短线像散落星点；按透视让近处线更宽更密，把月亮反光组织成纵向光路。 |
| [木纹 · wood-grain](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/materials/wood-grain/index.svg) | P2 | 横向纹理清楚；略像噪声条纹，加入木节与局部纹理弯折，提示词补可平铺及seed约束。 |

### 动效艺术（33张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [电池充电 · battery-charger](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/battery-charger/index.svg) | P2 | 充电三段成立；首帧留低亮度电量轮廓，补充满→复位节奏，中心闪电不遮挡电量。 |
| [液态形变 · blob-morph](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/blob-morph/index.svg) | P2 | 形变平滑感可以保留；补每个关键帧的控制点、停留/过渡比例，扩大造型差异以免只像轻微呼吸。 |
| [篝火 · campfire](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/campfire/index.svg) | P2 | 火焰气氛不错；火星、火舌、辉光使用不同相位，避免同频摆动，降低边缘高频噪点。 |
| [钟表 · clock](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/clock/index.svg) | P2 | 针有运动但比例是演示时钟；明确加速倍率，60刻度与秒针30°步进不符合真实秒针6°，如要拟真用真实齿比。 |
| [咖啡杯 loading · coffee-loader](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/coffee-loader/index.svg) | P2 | 当前造型像饮料杯且液面橙黄；咖啡改棕色、补杯柄或明确纸杯，蒸汽与液面都给柔和错相。 |
| [粒子礼花 · confetti](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/confetti/index.svg) | P2 | 粒子礼花动态可见，但主体占画幅偏小；增大散射范围和尺寸层次，提示词给随机seed及粒子数。 |
| [赛博城市 · cyber-city](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/cyber-city/index.svg) | P2 | 城市气氛成熟；NEO CITY与光线位置分散，减少上方空区，让飞行轨迹服务于城市主体。 |
| [数据流水线 · data-pipeline](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/data-pipeline/index.svg) | P2 | 三通道可见；加起点/终点语义与方向，流速、粒子相位给明确值，便于复现。 |
| [数据雨 · digital-rain](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/digital-rain/index.svg) | P2 | 中间帧可见数据雨，首帧空白并非损坏；用负begin铺开初始相位，提高暗尾文字的可见性。 |
| [心电脉冲 · ecg-pulse](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/ecg-pulse/index.svg) | P2 | 当前更像光点与描线展示；写明装饰心电示意，突出扫描头并让拖尾强度可读。 |
| [能量核心 · energy-core](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/energy-core/index.svg) | P2 | 视觉焦点明确，可保留；收回伸出圆环的细线或赋予扫描语义，多个环的方向/速度形成节奏差。 |
| [故障文字 Glitch · glitch-text](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/glitch-text/index.svg) | P2 | RGB错位有辨识度；限定故障时间窗，中间保留完整可读文字，给减少动态时的静态样式。 |
| [全息投影 · hologram](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/hologram/index.svg) | P2 | 球体扫描层次好；球下小文字与投影轮廓拥挤，放大主体说明并减少装饰线。 |
| [HUD 瞬准界面 · hud-interface](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/hud-interface/index.svg) | P2 | 整体风格一致；meta标题“瞬准”疑为“瞄准”笔误，核对；扫描线经过底部读数，给数据区独立裁剪。 |
| [等距立方 · iso-cubes](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/iso-cubes/index.svg) | P2 | 等距三面关系成立；立方体主体略小，把有效图形放大、说明缩短，投影随浮动高度同步。 |
| [字母变换 · letter-morph](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/letter-morph/index.svg) | P2 | 端态B/W/X可识别，中间态抽象；补骨架映射与端态停留，至少在稳定帧保证字母清楚。 |
| [线稿描边动画 · line-drawing](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/line-drawing/index.svg) | P2 | CSS描线与上色可见；唯一1000×700画幅却提示词1200×800，统一尺寸；右侧代码挤在卡边，增左边距并精简。 |
| [霓虹灯牌 · neon-sign](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/neon-sign/index.svg) | P1 | 提示词深底、实际浅底却用近白标题，造成低对比；OPEN/24H整体偏左、间隔点压在H附近，倒影只是渐变矩形，重做底色与排版/倒影。 |
| [引力轨道 · orbit-gravity](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/orbit-gravity/index.svg) | P2 | 两轨道三行星运动成立；若是物理模拟，补椭圆焦点与速度规则；若装饰，明确不代表真实引力轨道。 |
| [粒子对撞机 · particle-collider](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/particle-collider/index.svg) | P1 | 对撞星芒是静态path，无周期爆发动画；补与粒子到达共同触发的闪光，或去掉提示词中的周期爆发承诺。 |
| [雷达扫描 · radar-sweep](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/radar-sweep/index.svg) | P2 | 扇形与目标点成立；目标亮起最好与扫线经过同步，减少无关联的随机闪烁。 |
| [雨滴涟漪 · rain-ripples](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/rain-ripples/index.svg) | P2 | 下雨与涟漪都可见；补每滴到水面时刻表并逐一对齐，雨滴返程隐藏避免向上飞。 |
| [形状变换 · shape-morph](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/shape-morph/index.svg) | P2 | 方/圆/菱与星/心形范围够丰富；中间圆偏多边形感，优化控制点与端态停留，别只保证命令数一致。 |
| [雪景球 · snow-globe](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/snow-globe/index.svg) | P1 | 摇摆animateTransform在空g内，实际没有摇球；cy为起点→640→起点导致雪花往返上升；把动画包住主体、雪花在裁剪区外复位。 |
| [太阳系轨道 · solar-system](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/solar-system/index.svg) | P2 | 行星轨道展示清楚；五行星与逆行是装饰而非真实太阳系，标示意；当前提示词尾迹需补明确形状与随动规则。 |
| [聚光灯 · spotlight-scan](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/spotlight-scan/index.svg) | P2 | mask显露成立；主体字与图表布局可保留，提升光斑边缘柔度并明确轨迹/速度。 |
| [日出场景 · sunrise-scene](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/sunrise-scene/index.svg) | P2 | 天空与太阳变化成立；渐变背景时标题对比度也要检查，补太阳升起后停留和夜昼回环处理。 |
| [符号变换 · symbol-morph](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/symbol-morph/index.svg) | P2 | 心/电端态明确，气泡→信封更像开口折纸轮廓；补封口和矩形外框，使稳定端态一眼能认。 |
| [文字骑路径 · text-on-path](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/text-on-path/index.svg) | P2 | 环形文字可保留；旋转中仍要保留中心静态标题，补文本长度、startOffset和字体回退验收。 |
| [打字机文字 · typewriter](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/typewriter/index.svg) | P1 | 光标只有opacity动画，没有x动画，始终停在起点；按每个字符宽度同步移动，裁剪步数与实际字符串长度对齐。 |
| [步行方块 · walking-square](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/walking-square/index.svg) | P2 | 身体、脚和位移成立；后段靠近卡片右缘，眼睛没有随身体y颠簸，统一局部坐标并在边界外复位。 |
| [波形解析器 · wave-analyzer](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/wave-analyzer/index.svg) | P2 | 示波波形与频谱视觉好；下方柱子是独立预置动画而非FFT，标装饰频谱或补数据到频谱的计算模型。 |
| [单词变换 · word-morph](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/motion/word-morph/index.svg) | P2 | CAT/DOG端态清楚，是值得保留的代表作；中间态不可读可接受，但补锚点映射、端态停留比例与路径骨架约束。 |

### 高级数学（14张）

| 作品 | 优先级 | 检查结论与建议 |
|---|---|---|
| [贝塞尔构造动画 · bezier-de-casteljau](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/bezier-de-casteljau/index.svg) | P1 | 只有控制多边形呼吸与曲线上光点，没有Q/R分级插值线和点；实现de Casteljau的逐层lerp，并共用t参数，或改名“贝塞尔轨迹”。 |
| [悬链线 · catenary](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/catenary/index.svg) | P2 | 两曲线对比有价值；补a、跨度、垂度与坐标变换，提示词说放大楔形标注但作品没有明确差值放大区。 |
| [傅里叶构建动画 · fourier-build](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/fourier-build/index.svg) | P1 | 历史各档曲线/项数持续叠留，不是单一当前逼近；档位1/3/5/7/9/13/21也非每次+2，补完整级数、目标方波与互斥当前计数。 |
| [傅里叶逼近 · fourier-square](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/fourier-square/index.svg) | P2 | 四联趋势清楚；提示词补 fN(x)=4/π∑sin((2k−1)x)/(2k−1)、周期、相位、幅度和采样数。 |
| [分形树 · fractal-tree](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/fractal-tree/index.svg) | P2 | 树形完成度不错；提示词深绿底而作品深蓝，统一背景；扰动给固定seed、角度范围和层数计数定义。 |
| [分形树生长动画 · fractal-tree-grow](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/fractal-tree-grow/index.svg) | P2 | 按层出现成立；淡入更像显现而非枝条生长，可改名称或沿枝条描线；补生长与复位时序表。 |
| [黄金螺旋 · golden-spiral](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/golden-spiral/index.svg) | P1 | 圆弧连接处出现尖折回头，不是平滑螺旋；两个1方块还落在13方块内；重算方块和弧的朝向，注明Fibonacci圆弧近似而非严格黄金螺旋。 |
| [科赫雪花 · koch-snowflake](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/koch-snowflake/index.svg) | P2 | 轮廓与4层768边说明可保留；补初始三角形尺寸、方向与面积极限，迷你对照与提示词“中央”位置不一致。 |
| [利萨茹曲线 · lissajous](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/lissajous/index.svg) | P2 | 三联形态鲜明；提示词补每卡精确a/b/δ、参数范围和采样，当前只说标相位但未给相位值。 |
| [极坐标玫瑰 · polar-rose](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/polar-rose/index.svg) | P2 | 3/5/7瓣正确可保留；补R、采样区间，奇数k用[0,π]已遍历一次，避免[0,2π]重复描线。 |
| [谢尔宾斯基三角形 · sierpinski](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/sierpinski/index.svg) | P2 | 自相似图案成立；明确729为保留的最小三角数量、不同色阶含义，别把挖孔层数与保留块数混用。 |
| [向日葵种子图 · sunflower](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/sunflower/index.svg) | P2 | 800粒与黄金角说明清楚；补c、半径增长函数、n起始值和色彩映射，螺旋计数应说明随半径观察而变。 |
| [三维投影 · three-d](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/three-d/index.svg) | P1 | 【待核查】“90°翻面”面板在采样帧看起来像矩形网格，未验证全时段是否形成完整立方体；查投影坐标/遮挡，并补数学模型而非只列path插值。 |
| [拓扑形变 · topology-deform](/Users/agiray/Desktop/github/1-my-repo/svg-prompt/gallery/math/topology-deform/index.svg) | P1 | 球面与环面不可能不经退化保持拓扑等价；明确这是参数退化/自交的视觉演示，补参数方程、R/r范围和投影，莫比乌斯带给半扭转公式。 |

## 建议执行顺序与验收

| 批次 | 做什么 | 验收标准 |
|---|---|---|
| 1：可展示 | 修磨砂玻璃XML、重复ID；数字叠字、遮挡、霓虹底色 | 168个独立SVG均可解析/作为img展示；336/720/原尺寸重点图不重叠 |
| 2：内容正确 | 单位、气泡面积、字阶、出血、时间轴、地图色阶；黄金螺旋与贝塞尔构造 | 每项有计算或一手来源；示例数据明确；数学参数可复算 |
| 3：动效完整 | 点线面同步、光标跟随、雪景摇摆/雪花复位、对撞闪光、傅里叶当前档 | 每种动画按各自dur检查起点、中间、完成、dur前后；稳定态可读、跨循环无错误重影 |
| 4：更好复用 | prompt与SVG/meta对齐、占位参数、分类简介统一、减少动态与可访问说明 | 选每类代表作进行一次模型复现，记录模型/版本/偏差；通过后再扩大，不直接承诺任意模型同款 |

暂不建议：给168张统一加更多辉光、为了丰富感增加更多子分类、只压缩SVG文件而不修数据或布局、把原型图直接包装成生产组件。真正能提升品质的是让每张图说对话、画对数、动对地方，然后再统一视觉细节。
