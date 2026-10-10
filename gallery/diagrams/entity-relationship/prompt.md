# 会话数据实体关系 `静态` `2D`

分类：[流程与架构](../_about.md)

<img src="index.svg" width="720" alt="会话数据实体关系">

```
用 SVG 制作“会话数据实体关系”：用户 / 会话 / 消息 / 附件；显式 PK、FK 与基数。
- 画布1400×900，背景#f3f5f7；标题34px、组件名17–22px、说明15–16px；语义配色：调用蓝、事件橙、数据绿、控制红、关联灰。
- 重点表达：“关系线表示数据关联而非调用；父对象可暂时没有子对象”。
- 四实体，User.id→Conversation.user_id，Conversation.id→Message.conversation_id，Message.id→Attachment.message_id。
- 每个子实体只属于一个父实体，外键非空；每个父实体允许0到多个子实体。连线只表示关联，不是服务调用箭头。
- 表中PK/FK与关系基数对应，不把URI字段宣称为真实文件存储实现。
- 先列节点坐标与端口；端口l/r/t/b分别为矩形左/右/上/下中点，菱形为对应顶点。按下列坐标绘制：
  - users: User；说明["PK id", "email", "created_at"]；(x,y,w,h)=(100,300,290,190)；形状entity。
  - sessions: Conversation；说明["PK id", "FK user_id → User.id", "title / created_at"]；(x,y,w,h)=(700,300,290,190)；形状entity。
  - messages: Message；说明["PK id", "FK conversation_id", "role / content / created_at"]；(x,y,w,h)=(700,590,290,190)；形状entity。
  - attachments: Attachment；说明["PK id", "FK message_id → Message.id", "uri / media_type"]；(x,y,w,h)=(100,590,290,190)；形状entity。
- 连线先画、节点后画，线不穿过无关节点。下列方向、条件与折点必须一致：
  - users → sessions；neutral；标签“1  ——  0..N”；条件“User 1 : Conversation 0..N”；折点[[390, 395.0], [700, 395.0]]；无箭头，仅表示关联或层级。
  - sessions → messages；neutral；标签“1  ——  0..N”；条件“Conversation 1 : Message 0..N”；折点[[845.0, 490], [845.0, 590]]；无箭头，仅表示关联或层级。
  - messages → attachments；neutral；标签“1  ——  0..N”；条件“Message 1 : Attachment 0..N”；折点[[700, 685.0], [390, 685.0]]；无箭头，仅表示关联或层级。
- 页脚注明：“概念结构示意 · 不代表完整生产部署或真实运行状态”。
```
