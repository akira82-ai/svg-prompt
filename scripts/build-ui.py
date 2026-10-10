#!/usr/bin/env python3
"""Generate sixty distinct UI specimens with shared visual tokens and explicit states."""
from pathlib import Path
from html import escape
import json,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'gallery/ui';BUILT=[]
BLUE='#2467d5';GREEN='#167d65';ORANGE='#9b5b0a';RED='#b83e46';PURPLE='#7251bd'
GROUPS=[
('输入与基础组件', [('buttons','按钮状态'),('toggle','开关状态'),('toggle-animated','开关状态转换'),('checkbox-radio','复选与单选'),('input-states','输入与校验'),('dropdown','下拉选择'),('chips','标签与筛选项'),('avatar-badge','头像与徽章'),('elevation','卡片与层级'),('date-range','日期范围选择'),('file-upload','文件上传过程'),('login-verification','登录与验证')]),
('导航与检索',[('tabs','标签页与分段导航'),('pagination','分页与结果范围'),('tooltip','工具提示'),('breadcrumb','面包屑导航'),('global-search','全局搜索'),('command-palette','命令面板'),('filter-sort','筛选与排序'),('notification-center','通知中心'),('settings-preferences','设置与偏好'),('help-feedback','帮助与反馈')]),
('状态与过程反馈',[('alerts','消息提示条'),('alert-blink','告警强调'),('spinners','加载状态'),('indeterminate-progress','不确定进度'),('skeleton-shimmer','骨架屏加载'),('typing-indicator','正在输入'),('audio-wave','音频输入状态'),('status-patrol','服务状态巡检'),('task-stepper','多步骤任务进度'),('request-retry','请求状态与重试'),('empty-error','空状态与异常'),('modal-confirm','弹窗与确认'),('product-onboarding','产品引导')]),
('数据操作与指标',[('progress-slider','进度与滑块'),('kpi-cards','KPI 指标卡'),('number-roll','指标数值变化'),('data-table','专业数据表格'),('detail-drawer','详情抽屉'),('pricing-usage','套餐与用量')]),
('AI 产品界面',[('ai-chat-workbench','AI 对话工作台'),('model-parameters','模型与参数选择'),('agent-execution','Agent 执行过程'),('knowledge-citations','知识库检索与引用'),('generation-compare','生成结果对比')]),
('协作与业务操作',[('todo-today','待办清单'),('chat-messenger','团队聊天'),('ecommerce-home','电商商品目录'),('kanban-board','看板任务'),('members-permissions','成员与权限'),('checkout-payment','结算与支付状态')]),
('完整工作台与特色场景',[('bi-dashboard','经营分析工作台'),('dashboard','经营分析 · 入场演示'),('dark-ops-dashboard','运维监控工作台'),('live-ops-dashboard','运维监控 · 巡检演示'),('fitness-dashboard','活动与训练'),('music-player','音乐播放工作台'),('hud-interface','HUD 导航概念'),('wave-analyzer','波形解析工作台')])]
ANIMATED={'toggle-animated','file-upload','alert-blink','spinners','indeterminate-progress','skeleton-shimmer','typing-indicator','audio-wave','status-patrol','task-stepper','request-retry','number-roll','agent-execution','dashboard','live-ops-dashboard','music-player','hud-interface','wave-analyzer'}
DARK={'command-palette','ai-chat-workbench','agent-execution','dark-ops-dashboard','live-ops-dashboard','music-player','hud-interface','wave-analyzer'}
REMOVED=['clock','coffee-loader','battery-charger','radar-sweep','donut-sweep','ecg-pulse','gauge-swing','live-stream','glassmorphism']
class UI:
    def __init__(self,slug,title,group):
        self.slug,self.title,self.group=slug,title,group;self.dark=slug in DARK;self.animated=slug in ANIMATED;self.parts=[];self.notes=[];self.labels=[]
        self.bg='#0c1422' if self.dark else '#eef2f7';self.paper='#131f31' if self.dark else '#ffffff';self.ink='#eef4fc' if self.dark else '#1d2e46';self.muted='#acbdd3' if self.dark else '#596b82';self.linecolor='#314159' if self.dark else '#dce4ee';self.tint='#1c3050' if self.dark else '#eaf1fd';self.blue='#79b5ff' if self.dark else BLUE;self.green='#67d7b6' if self.dark else GREEN;self.red='#ff9ca6' if self.dark else RED;self.orange='#ffc16c' if self.dark else ORANGE
        self.rect(0,0,1400,900,self.bg,0);self.text(72,54,'SVG / PRODUCT INTERFACES',14,self.muted,weight=600);self.text(1328,54,'DEMO · 状态示意',14,self.muted,anchor='end');self.line(72,74,1328,74)
        self.text(72,122,title,34,weight=700);self.text(72,160,group+' / '+('过程动画与静态快照' if self.animated else '产品场景与状态设计'),18,self.muted)
        self.line(72,846,1328,846);self.text(72,878,'界面原型 · 模拟内容 · 控件状态不代表实际交互',14,self.muted);self.text(1328,878,'SVG-PROMPT',14,self.muted,anchor='end')
    def add(self,s):self.parts.append(s)
    def req(self,s):self.notes.append(s)
    def text(self,x,y,s,size=17,col=None,anchor='start',weight=400,attrs=''):
        self.labels.append(str(s));self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{col or self.ink}" text-anchor="{anchor}" font-weight="{weight}" {attrs}>{escape(str(s))}</text>')
    def lines(self,x,y,ss,size=17,col=None,step=29):
        for i,s in enumerate(ss):self.text(x,y+i*step,s,size,col)
    def rect(self,x,y,w,h,col=None,rx=10,attrs=''):self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" fill="{col or self.paper}" {attrs}/>')
    def line(self,x,y,xx,yy,col=None,width=1,attrs=''):self.add(f'<line x1="{x:.3f}" y1="{y:.3f}" x2="{xx:.3f}" y2="{yy:.3f}" stroke="{col or self.linecolor}" stroke-width="{width}" {attrs}/>')
    def circle(self,x,y,r,col=None,attrs=''):self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{col or self.blue}" {attrs}/>')
    def path(self,points,col=None,width=2,attrs=''):
        d='M '+' L '.join(f'{x:.3f} {y:.3f}' for x,y in points);self.add(f'<path d="{d}" fill="none" stroke="{col or self.blue}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {attrs}/>')
    def panel(self,x,y,w,h,title=None):
        self.rect(x,y,w,h,attrs=f'stroke="{self.linecolor}"');
        if title:self.text(x+24,y+36,title,19,weight=600)
    def button(self,x,y,label,w=132,kind='primary',state='default',h=42):
        fill=self.blue if kind=='primary' else self.paper;col='#0c1422' if self.dark and kind=='primary' else '#fff' if kind=='primary' else self.ink
        if state=='disabled':fill='#26364c' if self.dark else '#e5eaf0';col=self.muted
        if state=='hover' and kind=='primary':fill='#164faf' if not self.dark else '#a5ceff'
        if state=='pressed' and kind=='primary':fill='#113c89' if not self.dark else '#5699ef'
        if kind=='danger':fill=self.red;col='#0c1422' if self.dark else '#fff'
        if state=='focus':self.rect(x-4,y-4,w+8,h+8,'none',10,attrs=f'stroke="{self.blue}" stroke-width="2"')
        self.rect(x,y,w,h,fill,8,attrs=f'stroke="{self.linecolor if kind=="secondary" else fill}" data-control="button" data-state="{state}"');self.text(x+w/2,y+h/2+5,label,15,col,anchor='middle',weight=600)
    def badge(self,x,y,label,col=None,w=100):
        self.rect(x,y,w,28,self.tint,14);self.text(x+w/2,y+19,label,13,col or self.blue,anchor='middle',weight=600)
    def field(self,x,y,w,label,value,state='default',helper=None):
        self.text(x,y,label,15,weight=600);border=self.red if state=='error' else self.blue if state=='focus' else self.linecolor
        self.rect(x,y+14,w,48,self.tint if state=='disabled' else self.paper,8,attrs=f'stroke="{border}" stroke-width="{2 if state in ("focus","error") else 1}" data-control="input" data-state="{state}"');self.text(x+15,y+44,value,16,self.muted if state in ('disabled','default') else self.ink)
        if helper:self.text(x,y+86,helper,14,self.red if state=='error' else self.muted)
    def check(self,x,y,state='checked',radio=False):
        if radio:
            self.circle(x+10,y+10,10,self.paper,attrs=f'stroke="{self.blue if state=="checked" else self.linecolor}" stroke-width="2"')
            if state=='checked':self.circle(x+10,y+10,5,self.blue)
        else:
            self.rect(x,y,20,20,self.blue if state in ('checked','mixed') else self.paper,4,attrs=f'stroke="{self.blue if state in ("checked","mixed") else self.linecolor}" data-control="checkbox" data-state="{state}"')
            if state=='checked':self.path([(x+4,y+10),(x+8,y+14),(x+16,y+6)],'#fff',2)
            if state=='mixed':self.line(x+5,y+10,x+15,y+10,'#fff',2)
    def toggle(self,x,y,on=True,disabled=False):
        col=self.linecolor if disabled else self.blue if on else self.linecolor;self.rect(x,y,52,28,col,14,attrs=f'data-toggle="{str(on).lower()}" data-disabled="{str(disabled).lower()}"');self.circle(x+(38 if on else 14),y+14,10,self.paper)
    def progress(self,x,y,w,value,total=100,col=None,h=8,label=False):
        self.rect(x,y,w,h,self.linecolor,h/2);self.rect(x,y,w*value/total,h,col or self.blue,h/2,attrs=f'data-progress="{value}" data-total="{total}" data-track="{w}"')
        if label:self.text(x+w,y-12,f'{value}/{total}',14,self.muted,anchor='end')
    def avatar(self,x,y,label,col=None,r=18):
        self.circle(x,y,r,col or self.tint);self.text(x,y+5,label,14,self.blue,anchor='middle',weight=600)
    def animation(self,tag,attrs,tracks,dur='4s',repeat='indefinite',mode='linear'):
        self.add(f'<{tag} {attrs}>')
        for attr,values in tracks.items():self.add(f'<animate attributeName="{attr}" values="'+ ';'.join(map(str,values))+'" keyTimes="'+';'.join(f'{i/(len(values)-1):.6f}' for i in range(len(values)))+f'" dur="{dur}" repeatCount="{repeat}" fill="freeze" calcMode="{mode}"/>')
        self.add(f'</{tag}>')
    def emphasize(self,x,y,w,h,col=None):
        self.animation('rect',f'class="motion" x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="none" stroke="{col or self.blue}" stroke-width="2"',{'opacity':[.25,.85,.25]},'3s')
    def app(self,name,nav,active=0):
        self.panel(80,210,1240,610);self.rect(81,211,208,608,self.tint,10);self.text(110,252,name,20,weight=700);self.text(110,279,'WORKSPACE / DEMO',11,self.muted)
        for i,n in enumerate(nav):
            y=321+i*52
            if i==active:self.rect(97,y-24,176,40,self.paper,8)
            self.text(115,y,n,16,self.blue if i==active else self.muted,weight=600 if i==active else 400)
        self.avatar(116,766,'林');self.text(144,763,'个人工作区',14);self.text(144,785,'演示账号',12,self.muted);self.line(310,279,1290,279)
    def heading(self,title,subtitle=None,action=None):
        self.text(330,252,title,22,weight=700)
        if action:self.button(1140,226,action,150)
        if subtitle:self.text(330,311,subtitle,16,self.muted)
    def finish(self):
        if self.animated:self.add('<style>.fallback{display:none}@media(prefers-reduced-motion:reduce){.motion{display:none}.fallback{display:inline}}</style>')
        finding=self.notes[0] if self.notes else self.title+'的组件状态与产品场景示意'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" font-family="PingFang SC, Microsoft YaHei, sans-serif" role="img" aria-labelledby="title desc"><title id="title">{escape(self.title)}</title><desc id="desc">{escape(finding)}</desc>'+''.join(self.parts)+'</svg>\n'
        p=OUT/self.slug;p.mkdir(exist_ok=True);(p/'index.svg').write_text(svg)
        m=json.loads((p/'meta.json').read_text()) if (p/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
        m.update(slug=self.slug,title=self.title,space='2d',time='smil' if self.animated else 'static',order=len(BUILT)+1,description=finding,tech=['SVG UI','state design','SMIL' if self.animated else 'product layout']);(p/'meta.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
        labels=list(dict.fromkeys(self.labels));lines=[f'用 SVG 制作“{self.title}”，用于{self.group}。',f'- 画布1400×900；{"深色专业工作台" if self.dark else "浅色产品界面"}，背景{self.bg}、卡片{self.paper}、正文{self.ink}、辅助文字{self.muted}、主色{self.blue}；34px标题、15–19px正文、圆角8–12px、8px间距基准。','- 顶部作品标题与分组说明，内容位于x80..1320、y210..820；底部标注界面原型、模拟内容和非真实交互。']+['- '+s for s in self.notes]+['- 文字与示例值包含：'+json.dumps(labels,ensure_ascii=False)+'。','- 控件由SVG图形展示状态，不添加真实网络、登录、支付或权限操作；模拟场景不能宣称实时服务。']
        if self.animated:lines+=['- SMIL过程演示；状态、关键读数与操作从首帧可读，入场可按说明呈现图表，强调不得隐藏关键告警；减少动效时隐藏motion、显示fallback明确静态快照。确定进度/数字必须同步，不确定进度不显示伪百分比；重复演示不代表实际操作。']
        (p/'prompt.md').write_text(f'# {self.title} `{"SMIL 动效" if self.animated else "静态"}` `2D`\n\n分类：[界面与组件](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+'\n'.join(lines)+'\n```\n');BUILT.append(self.slug)

def board(f,cols=3,rows=2):
    boxes=[];gap=24;w=(1240-gap*(cols-1))/cols;h=(570-gap*(rows-1))/rows
    for i in range(cols*rows):
        x=80+i%cols*(w+gap);y=230+i//cols*(h+gap);f.panel(x,y,w,h);boxes.append((x,y,w,h))
    return boxes

def primitives(f):
    slug=f.slug
    if slug=='buttons':
        f.req('主按钮与次按钮均显示默认、悬停、键盘聚焦、按下、禁用；禁用原因明确。')
        f.panel(80,230,1240,570);states=['default','hover','focus','pressed','disabled'];names=['默认','悬停','键盘聚焦','按下','禁用']
        for i,(state,name) in enumerate(zip(states,names)):
            x=120+i*242;f.text(x,310,name,19,weight=600);f.button(x,365,'保存更改',178,state=state);f.button(x,463,'查看详情',178,'secondary',state);f.text(x,565,'提交修改' if i<4 else '请先完成必填项',15,f.muted)
        f.lines(120,675,['聚焦框与按钮边界分离，键盘导航时仍能辨认当前操作。','次按钮保持较低视觉权重；禁用不只依靠颜色表达。'],17,f.muted)
    elif slug in ('toggle','toggle-animated'):
        f.req('开关绑定明确设置语义，开启、关闭与不可用状态同时展示；动画为自动演示。')
        f.panel(210,250,980,510,'通知偏好')
        for i,(label,hint,on) in enumerate([('邮件通知','每周一发送工作摘要',True),('产品更新','收到新功能发布提醒',False),('安全提醒','组织策略要求开启',True)]):
            y=365+i*120;f.text(250,y,label,21,weight=600);f.text(250,y+35,hint,16,f.muted);f.toggle(1070,y-20,on,disabled=i==2);f.text(1010,y,'锁定开启' if i==2 else '自动演示' if f.animated and i==1 else '开启' if on else '关闭',15,f.muted,anchor='end')
        if f.animated:
            f.req('只演示第二行拨动，轨道颜色与滑块位置共享0/1/0参数；文字注明自动演示，避免与静态关闭标签冲突。');f.req('安全提醒由组织策略锁定，保留开启位置并降低控件强调。')
            f.add('<g class="motion">');f.animation('rect',f'x="1070" y="465" width="52" height="28" rx="14" fill="{f.linecolor}"',{'fill':[f.linecolor,f.blue,f.linecolor]},'4s');f.animation('circle',f'cx="1084" cy="479" r="10" fill="{f.paper}"',{'cx':[1084,1108,1084]},'4s');f.add('</g>');f.text(250,725,'自动循环用于演示；静态快照为关闭状态。',15,f.muted,attrs='class="fallback"')
    elif slug=='checkbox-radio':
        for i,(x,y,w,h) in enumerate(board(f,2,1)):
            f.text(x+28,y+48,['复选：可多选','单选：只能选一个'][i],23,weight=600)
            for j,label in enumerate(['未选择','已选择','部分子项已选择'] if i==0 else ['个人工作区','团队工作区','组织工作区']):
                yy=y+130+j*90;f.check(x+30,yy,'unchecked' if j==0 else 'checked' if j==1 else 'mixed' if i==0 else 'unchecked',i==1);f.text(x+70,yy+17,label,19)
            f.text(x+28,y+485,'半选仅用于复选父级' if i==0 else '组织类型只允许一个激活项',16,f.muted)
        f.req('复选未选/选中/半选，单选组仅团队选中；半选不用于单选控件。')
    elif slug=='input-states':
        for (x,y,w,h),(state,label,val,hint) in zip(board(f,2,2),[('default','默认','请输入项目名称','名称将显示在项目列表中'),('focus','键盘聚焦','Atlas 设计库','最多 40 个字符'),('error','校验错误','atlas@','请输入完整的邮箱地址'),('disabled','不可编辑','组织统一配置','此字段由组织管理员维护')]):f.text(x+28,y+44,label,20,weight=600);f.field(x+28,y+95,w-56,'邮箱地址' if state=='error' else '项目名称',val,state,hint)
        f.req('标签不被占位符替代；错误说明如何修正；禁用提供组织策略原因。')
    elif slug=='dropdown':
        f.panel(220,250,960,510,'项目状态');f.field(260,330,390,'选择状态','进行中  ▾','focus');f.panel(260,405,390,290)
        for i,(label,detail) in enumerate([('未开始','已创建，尚未启动'),('进行中  ✓','正在处理任务'),('已完成','全部任务已经完成')]):
            y=448+i*82
            if i==1:f.rect(272,y-28,366,70,f.tint,6)
            f.text(290,y,label,18,f.blue if i==1 else f.ink);f.text(290,y+26,detail,14,f.muted)
        f.lines(735,415,['展开态保留当前值','选中项：勾选与高亮','Esc：关闭菜单','↑ / ↓：切换选项','此图展示键盘操作提示'],17,f.muted,step=43);f.req('触发框与菜单对齐，当前进行中有勾选；普通项和选中项不混淆。')
    elif slug=='chips':
        f.panel(150,250,1100,510,'筛选条件与标签')
        for i,(name,state) in enumerate([('全部项目','选中'),('设计资源','普通'),('状态：进行中 ×','可移除'),('+ 添加条件','添加')]):
            x=195+i*258;f.button(x,365,name,218,'primary' if i==0 else 'secondary');f.text(x+109,448,state,17,f.muted,anchor='middle')
        f.text(195,560,'已应用筛选：状态 = 进行中',20,weight=600);f.text(195,605,'移除筛选后恢复全部结果；标签与筛选条件使用不同文字说明。',17,f.muted);f.req('普通、选中、可移除与添加四类；可移除标签含明确×，显示应用条件。')
    elif slug=='avatar-badge':
        for i,(x,y,w,h) in enumerate(board(f,3,1)):
            f.text(x+28,y+46,['个人头像','协作成员','未读与在线'][i],21,weight=600)
            if i==0:
                for j,r in enumerate([20,30,42]):f.avatar(x+80+j*105,y+200,'林',r=r)
                f.text(x+28,y+330,'小 / 中 / 大尺寸',17,f.muted)
            elif i==1:
                for j,label in enumerate(['林','陈','周','+3']):f.avatar(x+100+j*55,y+200,label,r=30)
                f.text(x+28,y+330,'6 位成员，显示部分头像',17,f.muted)
            else:f.avatar(x+100,y+200,'林',r=42);f.circle(x+132,y+230,9,f.green,attrs=f'stroke="{f.paper}" stroke-width="3"');f.badge(x+205,y+180,'12 条未读',w=130);f.text(x+28,y+330,'在线 · 12 条未读消息',17,f.muted)
        f.req('字母头像三尺寸、成员头像堆叠、文字化在线与未读；数字徽章不是成员数量。')
    elif slug=='elevation':
        for i,(x,y,w,h) in enumerate(board(f,4,1)):
            f.text(x+26,y+46,['页面底层','普通卡片','浮层菜单','模态对话框'][i],21,weight=600)
            if i:f.rect(x+35,y+167, w-56,210,'#e0e6ef',14)
            f.panel(x+26,y+155,w-56,210);f.text(x+50,y+206,f'层级 {i}',20,weight=600);f.lines(x+50,y+248,['边界清晰','适度阴影','内容优先'],16,f.muted)
            f.text(x+26,y+442,['无浮起','内容分组','临时操作','需要明确处理'][i],16,f.muted)
        f.req('四种产品层级用轻量偏移阴影与边界表达，不使用高斯模糊掩盖文本。')
    elif slug=='date-range':
        f.panel(130,230,1140,570,'选择分析时间');f.button(170,295,'最近 7 天',150);f.button(336,295,'最近 30 天',160,'secondary');f.text(170,390,'2026 年 10 月',25,weight=600)
        for j,label in enumerate(['一','二','三','四','五','六','日']):f.text(203+j*72,437,label,15,f.muted,anchor='middle')
        for day in range(1,32):
            index=day+2;col=index%7;row=index//7;x=173+col*72;y=465+row*52
            if 5<=day<=11:f.rect(x,y, 60,40,f.blue if day in (5,11) else f.tint,6,attrs=f'data-day="{day}" data-selected="true"')
            f.text(x+30,y+26,day,16,'#fff' if day in (5,11) else f.ink,anchor='middle',attrs=f'data-date="2026-10-{day:02d}"')
        f.field(810,390,390,'开始日期','2026-10-05');f.field(810,510,390,'结束日期','2026-10-11');f.button(1035,685,'应用范围',165);f.text(810,640,'7 天 · 含开始与结束日期',16,f.muted);f.req('2026-10-01为星期四；预选10月5日至11日，含首尾共7天；日期位置与真实日历匹配。')
    elif slug=='login-verification':
        f.panel(130,235,540,565,'欢迎回来');f.text(170,340,'进入你的工作区',28,weight=700);f.field(170,410,450,'邮箱','lin@example.com');f.field(170,510,450,'密码','••••••••');f.button(170,625,'登录',450);f.text(170,725,'忘记密码？   /   使用组织账号登录',15,f.muted)
        f.panel(710,235,560,565,'验证你的身份');f.lines(750,342,['验证码已发送到','l•••@example.com'],19,step=33)
        for i,n in enumerate(['2','4','8','1','','']):f.rect(750+i*74,470, 60,64,f.paper,8,attrs=f'stroke="{f.blue if i==4 else f.linecolor}"');f.text(780+i*74,510,n,25,anchor='middle')
        f.text(750,595,'请填写 6 位验证码 · 重新发送（28 秒）',16,f.muted);f.button(750,655,'验证并继续',450,state='disabled');f.req('并排展示登录与二次验证；邮箱脱敏，六位验证码未完整时继续按钮禁用；不展示真实凭证。')
    else:return False
    return True

def navigation(f):
    s=f.slug
    if s=='tabs':
        f.panel(140,240,1120,545,'项目详情')
        for i,label in enumerate(['概览','任务','文件','活动']):
            x=185+i*230;f.text(x,350,label,20,f.blue if i==0 else f.muted);f.line(x-10,374,x+150,374,f.blue if i==0 else f.linecolor,3 if i==0 else 1)
        f.text(185,437,'概览内容区域',25,weight=600);f.text(185,478,'标签切换同一对象的不同内容；页面位置保持稳定。',17,f.muted)
        for i,label in enumerate(['周','月','季度']):f.button(185+i*155,580,label,140,'primary' if i==1 else 'secondary')
        f.text(185,680,'分段控件改变当前视图的时间粒度，不跳转到其他页面。',17,f.muted);f.req('下划线标签页激活概览；分段控件激活月，导航与视图切换含义明确。')
    elif s=='pagination':
        f.panel(130,245,1140,540,'项目列表 / 分页')
        for i in range(4):f.line(170,340+i*63,1230,340+i*63);f.text(185,372+i*63,f'项目 {31+i:02d}',18);f.text(650,372+i*63,'进行中',16,f.green);f.text(1130,372+i*63,'查看',16,f.blue)
        f.text(170,660,'显示 31–40 条 / 共 95 条 / 每页 10 条',17,f.muted);f.button(170,710,'上一页',110,'secondary')
        for i,n in enumerate([1,2,3,4,5,'…',10]):f.button(303+i*78,710,str(n),60,'primary' if n==4 else 'secondary')
        f.button(875,710,'下一页',110,'secondary');f.req('分页第4页，共95条，每页10条，范围31–40；列表仅预览其中4条；当前页、前后翻页与省略号明确。')
    elif s=='tooltip':
        for i,(x,y,w,h) in enumerate(board(f,2,1)):
            f.text(x+28,y+48,['文字辅助说明','快捷键辅助说明'][i],22,weight=600);f.button(x+190,y+270,['导出报告','搜索项目'][i],190,'secondary');f.rect(x+115,y+165,w-230, 70,f.ink,8);f.text(x+w/2,y+207,['将当前筛选结果导出为 CSV','按 ⌘ K 打开全局搜索'][i],16,f.paper,anchor='middle');f.add(f'<path d="M{x+w/2-8} {y+235} L{x+w/2} {y+245} L{x+w/2+8} {y+235} Z" fill="{f.ink}"/>');f.text(x+28,y+430,'帮助信息不承载必须完成的操作',17,f.muted)
        f.req('悬浮提示靠近触发按钮，含方向三角；重要操作与错误不只放在提示气泡中。')
    elif s=='breadcrumb':
        f.app('ATLAS', ['首页','项目','团队','设置'],1);f.heading('界面规范',action='编辑文档');f.text(330,320,'首页  /  项目  /  设计系统  /  界面规范',17,f.muted)
        f.panel(330,355,960,395,'文档路径与当前位置');f.text(365,440,'设计系统 / 界面规范',29,weight=700);f.lines(365,505,['父级路径保持可返回，当前项使用普通正文。','面包屑表达层级，不替代浏览历史。','深层路径可以折叠中间项，但保留根级与当前级。'],18,f.muted,step=48);f.req('四级面包屑首页/项目/设计系统/界面规范；当前项不是重复导航按钮。')
    elif s in ('global-search','command-palette'):
        command=s=='command-palette';f.panel(260,230,880,570);f.field(295,285,810,'命令' if command else '搜索所有内容','> 导出' if command else '设计系统','focus');f.text(295,410,'可用命令' if command else '文档与项目',15,f.muted)
        rows=[('导出当前报告','⌘ E'),('导出项目数据','CSV'),('查看导出记录','↵')] if command else [('设计系统 / 组件规范','文档'),('设计系统 / 项目看板','项目'),('设计系统 / 更新日志','文档')]
        for i,(a,b) in enumerate(rows):
            y=450+i*83
            if i==0:f.rect(281,y-26,838,65,f.tint,8)
            f.text(310,y,a,19,f.blue if i==0 else f.ink);f.text(1085,y,b,14,f.muted,anchor='end');f.text(310,y+26,'Enter 执行此命令' if command else '匹配词：设计系统',14,f.muted)
        f.line(295,717,1105,717);f.text(295,755,'↑ ↓ 选择    ↵ '+('执行' if command else '打开')+'    Esc 关闭',15,f.muted);f.req('输入区域、分组结果、键盘选中态与键盘提示清楚；'+('命令含动词和快捷键，不与全文搜索混淆。' if command else '搜索按文档/项目分类，明确匹配关键词。'))
    elif s=='filter-sort':
        f.app('ATLAS', ['项目列表','活动','成员'],0);f.heading('项目筛选',action='清除条件');f.panel(330,320,960,445)
        f.field(365,365,270,'状态','进行中  ▾');f.field(665,365,270,'负责人','林老师  ▾');f.field(965,365,290,'排序','更新时间：降序  ▾');f.badge(365,485,'状态：进行中 ×',w=180);f.badge(565,485,'负责人：林老师 ×',w=200)
        for i,(n,date) in enumerate([('界面规范','10-10 14:30'),('图标资源库','10-09 10:15'),('首页改版','10-08 09:20')]):y=568+i*60;f.line(365,y+24,1255,y+24);f.text(365,y,n,19);f.text(850,y,'林老师',16,f.muted);f.text(1255,y,date,16,f.muted,anchor='end')
        f.req('条件状态=进行中、负责人=林老师；三条示例结果按更新时间降序，条件可移除并提供清除入口。')
    elif s=='notification-center':
        f.app('ATLAS', ['工作台','通知中心','设置'],1);f.heading('通知中心',action='全部标为已读');f.text(330,318,'未读 2    /    全部通知',18,f.blue)
        for i,(title,body,time,unread) in enumerate([('项目需要你的确认','Agent 已完成检索，等待批准下一步','10 分钟前',True),('陈同学提到了你','界面规范：请检查键盘聚焦状态','35 分钟前',True),('报告已导出','经营报告.csv 已准备好','昨天',False)]):
            y=350+i*137;f.panel(330,y,960,116);f.circle(357,y+35,4,f.blue if unread else f.linecolor);f.text(375,y+40,title,20,weight=600);f.text(375,y+76,body,16,f.muted);f.text(1260,y+40,time,14,f.muted,anchor='end')
        f.req('2条未读、1条已读；未读由点、分组计数与文字表达，通知包含来源、时间与行动上下文。')
    elif s=='settings-preferences':
        f.app('ATLAS', ['账户资料','通知偏好','外观','安全'],1);f.heading('通知与外观',action='保存更改')
        for i,(title,hint,on) in enumerate([('邮件摘要','每周接收一次工作摘要',True),('桌面通知','当前浏览器未授予权限',False),('减少动效','关闭非必要的循环强调',True)]):
            y=335+i*135;f.panel(330,y,960,112);f.text(360,y+38,title,21,weight=600);f.text(360,y+74,hint,16,f.muted);f.toggle(1200,y+30,on)
        f.req('设置区分产品偏好与系统权限；桌面通知说明权限未授予，减少动效为独立可读设置。')
    elif s=='help-feedback':
        f.app('ATLAS', ['帮助中心','提交反馈','我的工单'],1);f.heading('帮助与反馈');f.panel(330,320,440,450,'常见问题');f.lines(365,412,['如何邀请团队成员？','如何导出筛选结果？','如何查看使用额度？','如何管理模型引用？'],20,step=70);f.button(365,675,'查看全部帮助',200,'secondary')
        f.panel(795,320,495,450,'告诉我们遇到的问题');f.field(830,410,425,'问题类型','功能建议  ▾');f.field(830,520,425,'问题描述','希望支持批量导出所选项目');f.text(830,632,'可附截图；请勿提交密码或敏感凭证。',14,f.muted);f.button(1070,685,'提交反馈',185);f.req('帮助检索与反馈表单并列；问题类型、描述与提交入口明确，并提示不要包含敏感凭证。')
    else:return False
    return True

def feedback(f):
    s=f.slug
    if s in ('file-upload','task-stepper','request-retry'):
        configs={
        'file-upload':[('等待上传','拖入文件或选择文件',['支持 PDF / CSV / PNG','单个文件不超过 20 MB'],'选择文件'),('正在上传','季度报告.pdf',['4.0 MB / 6.25 MB','64% · 可以取消上传'],'取消上传'),('上传完成','季度报告.pdf',['文件已经准备好','可用于检索与分析'],'查看文件')],
        'task-stepper':[('已完成','1 / 收集资料',['8 份文档已添加','资料完整性检查通过'],'查看资料'),('当前步骤','2 / 分析内容',['正在解析文档结构','下一步：生成报告'],'查看过程'),('等待执行','3 / 生成报告',['分析完成后才会启动','当前没有输出结果'],'等待分析')],
        'request-retry':[('请求超时','首次请求未完成',['未收到服务响应','内容已保留，可以重试'],'重试请求'),('重试中','第 2 次请求',['正在重新建立连接','请等待，避免重复提交'],'取消'),('已恢复','示例恢复结果',['响应已成功接收','原输入内容保持不变'],'查看结果')]}
        for i,((x,y,w,h),(state,title,body,action)) in enumerate(zip(board(f,3,1),configs[s])):
            f.badge(x+28,y+35,state,w=140);f.text(x+28,y+135,title,23,weight=600);f.lines(x+28,y+200,body,17,f.muted,step=38)
            if s=='file-upload' and i==1:f.progress(x+28,y+310,w-56,64)
            if s=='task-stepper':f.circle(x+52,y+310,23,f.tint);f.text(x+52,y+316,str(i+1),20,f.blue,anchor='middle');f.text(x+90,y+316,['✓ 已完成','● 当前步骤','○ 等待'][i],17,f.muted)
            f.button(x+28,y+390,action,w-56,'secondary' if i==1 else 'primary',state='disabled' if s=='task-stepper' and i==2 else 'default')
            if i==1:f.emphasize(x+14,y+14,w-28,h-28)
        f.text(120,824,'三阶段状态对照；循环只强调中间状态，不表示实际任务自动完成。',14,f.muted,attrs='class="fallback"')
        f.req({'file-upload':'上传三阶段：等待/64%上传中/完成；4.0÷6.25=64%，进度与文本一致。','task-stepper':'任务完成/当前/等待三个阶段；等待按钮禁用，不自动跳过当前任务。','request-retry':'请求超时/重试中/恢复三个状态；保留输入，避免重试导致重复提交。'}[s])
    elif s in ('alerts','alert-blink'):
        f.panel(130,235,1140,570,'消息与告警')
        rows=[('✓','保存成功','项目设置已经更新',f.green),('!','连接异常','未收到服务响应，请稍后重试',f.red),('△','额度提醒','本月额度已使用 80%，可查看套餐',ORANGE),('i','报告生成中','完成后将在通知中心提醒你',f.blue)]
        for i,(icon,title,body,col) in enumerate(rows):
            y=320+i*106;f.rect(170,y,1060,88,f.tint,8);f.circle(204,y+35,16,col);f.text(204,y+41,icon,17,f.paper,anchor='middle',weight=700);f.text(240,y+32,title,19,col,weight=600);f.text(240,y+63,body,16,f.muted);f.text(1195,y+40,'×',23,f.muted,anchor='end')
        if f.animated:f.emphasize(164,420,1072,100,f.red);f.text(190,785,'告警内容持续可读；仅边框缓慢强调。',14,f.muted,attrs='class="fallback"')
        f.req('成功/错误/警告/信息同时用符号、标题与说明区分；告警不得随强调消失，不快闪关键内容。')
    elif s=='spinners':
        for i,(x,y,w,h) in enumerate(board(f,3,1)):
            f.text(x+28,y+45,['加载中','正在处理','等待响应'][i],22,weight=600)
            if i==0:
                f.circle(x+w/2,y+220, 40,'none',attrs=f'stroke="{f.linecolor}" stroke-width="7"');f.add(f'<g class="motion"><path d="M{x+w/2} {y+180} A40 40 0 0 1 {x+w/2+40} {y+220}" stroke="{f.blue}" stroke-width="7" fill="none" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="0 {x+w/2} {y+220}" to="360 {x+w/2} {y+220}" dur="2s" repeatCount="indefinite"/></path></g>');f.circle(x+w/2,y+220,40,'none',attrs=f'class="fallback" stroke="{f.blue}" stroke-width="7"')
            elif i==2:
                f.animation('circle',f'class="motion" cx="{x+w/2}" cy="{y+220}" r="20" fill="none" stroke="{f.blue}" stroke-width="3"',{'r':[20,44,20],'opacity':[1,.25,1]},'2.4s');f.circle(x+w/2,y+220,32,'none',attrs=f'class="fallback" stroke="{f.blue}" stroke-width="3"')
            else:
                for j in range(3):
                    xx=x+w/2+(j-1)*38;f.animation('circle',f'class="motion" cx="{xx}" cy="{y+220}" r="8" fill="{f.blue}"',{'opacity':[[.3,1,.3],[1,.3,1],[.3,1,.3]][j]},'2s');f.circle(xx,y+220,8,f.blue,attrs='class="fallback"')
            f.lines(x+28,y+365,['时间未知，不显示百分比','文字说明当前正在处理什么'],16,f.muted,step=40)
        f.req('圆弧旋转与点状等待均为不确定加载；文字固定可读，静态快照保持处理状态。')
    elif s=='indeterminate-progress':
        f.panel(180,260,1040,480,'正在准备导出文件');f.text(220,390,'已提交导出请求，正在整理筛选结果。',22);f.rect(220,455,960,12,f.linecolor,6);f.add('<defs><clipPath id="progress-window"><rect x="220" y="455" width="960" height="12" rx="6"/></clipPath></defs><g clip-path="url(#progress-window)" class="motion">');f.animation('rect',f'x="20" y="455" width="200" height="12" rx="6" fill="{f.blue}"',{'x':[20,1180]},'3s');f.add('</g>');f.rect(600,455,200,12,f.blue,6,attrs='class="fallback"');f.text(220,540,'进度暂不可计算；完成后会发送通知。',17,f.muted);f.button(1040,630,'取消导出',140,'secondary');f.req('未知时长使用循环光条，限定裁切范围，不显示伪百分比或预计完成时间。')
    elif s=='skeleton-shimmer':
        f.app('ATLAS',['项目列表','团队','设置']);f.heading('项目列表');f.text(330,315,'正在加载项目…',17,f.muted)
        f.add('<defs><linearGradient id="shimmer"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".65"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
        for i in range(3):
            y=350+i*140;f.panel(330,y,960,115);f.rect(358,y+25,54,54,f.linecolor,9);f.rect(440,y+25,410,16,f.linecolor,5);f.rect(440,y+60,630,13,f.linecolor,5);f.rect(1170,y+25,90,25,f.linecolor,7);f.add(f'<defs><clipPath id="skeleton-{i}"><rect x="358" y="{y+25}" width="54" height="54" rx="9"/><rect x="440" y="{y+25}" width="410" height="16" rx="5"/><rect x="440" y="{y+60}" width="630" height="13" rx="5"/><rect x="1170" y="{y+25}" width="90" height="25" rx="7"/></clipPath></defs><g class="motion" clip-path="url(#skeleton-{i})">');f.animation('rect',f'x="150" y="{y+10}" width="220" height="95" fill="url(#shimmer)"',{'x':[150,1290]},'3s');f.add('</g>')
        f.text(330,795,'占位结构与内容布局一致；加载失败时转为错误提示。',15,f.muted,attrs='class="fallback"');f.req('三行列表骨架保留图标、标题、副文本与状态位置；微光在占位块内部裁切，不让加载文字闪烁。')
    elif s=='typing-indicator':
        f.panel(220,250,960,500,'团队对话');f.avatar(270,378,'林');f.rect(310,340,470, 80,f.tint,12);f.text(335,388,'我把更新的组件规范发给你。',19);f.avatar(1080,505,'陈');f.rect(820,465,220,80,f.tint,12)
        for j in range(3):f.animation('circle',f'class="motion" cx="{872+j*46}" cy="505" r="7" fill="{f.blue}"',{'opacity':[[1,.3,.3,1],[.3,1,.3,.3],[.3,.3,1,.3]][j]},'2.4s');f.circle(872+j*46,505,7,f.blue,attrs='class="fallback"')
        f.text(820,590,'陈同学正在输入…',17,f.muted);f.field(260,660,880,'消息','输入消息…');f.req('三点依次强调，明确陈同学正在输入；不暗示消息已经发送或内容已经生成。')
    elif s=='audio-wave':
        f.panel(210,250,980,510,'语音输入');f.text(700,365,'正在聆听',28,anchor='middle',weight=700)
        for j in range(19):
            h=20+50*abs(math.sin(j*1.8));x=411+j*30;f.animation('rect',f'class="motion" x="{x}" y="{510-h/2}" width="10" height="{h}" rx="5" fill="{f.blue}"',{'height':[h,h*.4,h],'y':[510-h/2,510-h*.2,510-h/2]},'2s');f.rect(x,510-h/2,10,h,f.blue,5,attrs='class="fallback"')
        f.text(700,640,'模拟声条 · 不代表真实录音或音量测量',16,f.muted,anchor='middle');f.button(535,685,'停止聆听',160,'secondary');f.button(720,685,'确认发送',160);f.req('语音状态包含停止与确认发送；示例声条只演示听取状态，不连接麦克风，不声称实测波形。')
    elif s=='status-patrol':
        f.app('NOVA OPS',['服务状态','告警记录','配置']);f.heading('服务状态巡检');f.text(330,316,'巡检演示 · 服务状态为固定示例',16,f.muted)
        for i,(name,status,col) in enumerate([('API Gateway','正常',f.green),('Search Index','正常',f.green),('Task Worker','降级',ORANGE),('Storage','正常',f.green)]):
            y=350+i*105;f.panel(330,y,960,86);f.circle(365,y+43,6,col);f.text(390,y+50,name,20);f.text(1130,y+50,status,17,col);f.text(1255,y+50,'查看',16,f.blue,anchor='end')
        f.animation('rect',f'class="motion" x="338" y="358" width="944" height="70" rx="8" fill="none" stroke="{f.blue}" stroke-width="2"',{'y':[358,463,568,673,358]},'6s',mode='discrete');f.text(330,790,'正常与降级不随光带变化；减少动效显示完整列表。',15,f.muted,attrs='class="fallback"');f.req('四服务固定3正常/1降级；巡检框离散按行移动，不将扫描位置当作服务健康判定。')
    elif s=='empty-error':
        configs=[('还没有项目','从第一个项目开始','新建项目','○'),('没有匹配结果','试试移除筛选或更换关键词','清除筛选','⌕'),('暂时无法加载','连接失败，已有内容不会丢失','重试加载','!')]
        for (x,y,w,h),(title,body,button,icon) in zip(board(f,3,1),configs):f.circle(x+w/2,y+145,42,f.tint);f.text(x+w/2,y+155,icon, 30,f.blue,anchor='middle');f.text(x+w/2,y+265,title,23,anchor='middle',weight=600);f.text(x+w/2,y+318,body,16,f.muted,anchor='middle');f.button(x+48,y+400,button,w-96)
        f.req('首次使用、搜索无结果、加载失败三个不同原因对应新建、清除条件、重试三种操作。')
    elif s=='modal-confirm':
        f.panel(120,240,1160,550,'项目设置');f.rect(121,241,1158,548,'#dae2ec',9);f.panel(355,320,690,355,'移出团队成员？');f.lines(395,425,['陈同学将无法继续访问此工作区。','已有文档会保留，管理员可重新邀请。'],19,f.muted,step=38);f.button(690,575,'取消',130,'secondary');f.button(845,575,'确认移出',160,'danger');f.text(395,535,'对象：陈同学 / chen@example.com',16);f.req('确认框说明对象、权限影响和可恢复性，危险操作与取消分开；页面原型不执行真实移出。')
    elif s=='product-onboarding':
        f.app('ATLAS',['概览','项目','知识库']);f.heading('欢迎加入工作区',action='新建项目');f.panel(330,330,960,410,'开始使用 / 1 共 3 步')
        for i,(title,body) in enumerate([('建立你的第一个项目','集中管理任务、文件与讨论'),('邀请团队成员','协作之前明确每个人的角色'),('添加知识资料','为搜索与引用准备可追溯来源')]):
            y=410+i*95;f.circle(369,y,18,f.tint);f.text(369,y+6,str(i+1),17,f.blue,anchor='middle');f.text(408,y+6,title,21,weight=600);f.text(408,y+38,body,16,f.muted)
        f.button(1020,665,'继续引导',225);f.text(330,790,'可以跳过引导，稍后从帮助中心继续。',15,f.muted);f.req('新手引导包含建立项目、邀请成员、添加资料三个步骤；当前第一步，允许稍后继续。')
    else:return False
    return True

REVENUE=[12100,13500,14200,16600,17750,16900,18300,19100]
OPS_QPS=[42,43,46,44,49,48,47,46.2]
PROJECTS=[('Atlas 设计系统','林老师','进行中','10-10',48),('知识库索引','陈同学','待审核','10-09',75),('产品首页','周同学','进行中','10-08',32),('组件文档','林老师','已完成','10-07',100),('数据导出','陈同学','未开始','10-06',0)]
def table(f,x,y,w,headers,rows,widths=None,rowh=60):
    f.rect(x,y,w,44,f.tint,6);widths=widths or [w/len(headers)]*len(headers);xs=[x+18];
    for width in widths[:-1]:xs.append(xs[-1]+width)
    for xx,label in zip(xs,headers):f.text(xx,y+28,label,14,f.muted,weight=600)
    for i,row in enumerate(rows):
        yy=y+44+i*rowh;f.line(x,yy+rowh,x+w,yy+rowh)
        for xx,label in zip(xs,row):f.text(xx,yy+rowh/2+5,label,16)

def data_views(f):
    s=f.slug
    if s=='progress-slider':
        f.panel(130,240,1140,550,'确定进度与可调数值')
        for i,value in enumerate([25, 60,100]):
            y=345+i*102;f.text(175,y,f'任务 {i+1}',19,weight=600);f.text(1190,y,f'{value}%',20,f.blue,anchor='end');f.progress(175,y+25,1015,value)
        f.text(175,680,'音量 / 40%',17);f.progress(360,676,700,40);f.circle(640,680,10,f.paper,attrs=f'stroke="{f.blue}" stroke-width="3" data-slider="40"');f.text(175,755,'进度用于反馈完成比例；滑块用于调整可选择的值。',16,f.muted);f.req('进度25/60/100%，滑块40%；圆点坐标与40%轨道比例一致，不把滑块当作进度反馈。')
    elif s=='kpi-cards':
        vals=[('销售额','¥128,450','↑ 12.4% / 较上一周期',BLUE),('订单数','840','↑ 5.0% / 较上一周期',GREEN),('支付转化率','3.86%','↓ 0.40 个百分点',ORANGE),('退款率','2.10%','↓ 0.40 个百分点',GREEN)]
        series=[[sum(REVENUE[:j+1]) for j in range(8)],[60,130,210,310,420,540,680,840],[4.26,4.18,4.12,4.04,3.97,4.01,3.90,3.86],[2.50,2.45,2.40,2.32,2.20,2.25,2.16,2.10]]
        for (x,y,w,h),(title,value,change,col),data in zip(board(f,2,2),vals,series):
            f.text(x+28,y+40,title,18,f.muted);f.text(x+28,y+110,value,40,weight=700);f.text(x+28,y+158,change,16,col);lo,hi=min(data),max(data);f.path([(x+28+j*(w-56)/7,y+225-(v-lo)/(hi-lo)*35) for j,v in enumerate(data)],col,2,attrs='data-kpi-series="'+','.join(map(str,data))+'"');f.text(x+28,y+251,'累计趋势' if title in ('销售额','订单数') else '比率趋势 / 独立尺度',12,f.muted)
        f.req('金额、订单和比率明确单位；累计序列最终值128450/840，比率序列最终值3.86/2.10；上一周期销售114279、订单800，比率4.26/2.50。转化率/退款率变化用百分点，下降是否有利由指标含义决定；迷你趋势各自独立尺度。')
    elif s=='number-roll':
        f.panel(210,250,980,510,'累计完成任务 / 演示阶段')
        for j,value in enumerate([50,100,150]):
            f.add(f'<g class="motion" opacity="{1 if j==0 else 0}" data-count-stage="{value}">');f.add('<animate attributeName="opacity" values="'+';'.join('1' if k==j else '0' for k in [0,1,2,2])+'" keyTimes="0;0.333333;0.666667;1" dur="6s" repeatCount="indefinite" calcMode="discrete"/>');f.text(700,450,value, 70,anchor='middle',weight=700);f.text(700,510,f'{value} / 200 个任务',21,f.muted,anchor='middle');f.progress(290,565,820,value,200);f.add('</g>')
        f.add('<g class="fallback">');f.text(700,450,150,70,anchor='middle',weight=700);f.text(700,510,'150 / 200 个任务',21,f.muted,anchor='middle');f.progress(290,565,820,150,200);f.add('</g>');f.text(700,685,'50 → 100 → 150 · 循环为演示，非真实任务增长',16,f.muted,anchor='middle');f.req('数字与进度共用50/100/150三档，总量200；离散阶段每2秒切换，静态快照150/200。')
    elif s=='data-table':
        f.app('ATLAS',['项目列表','任务','成员']);f.heading('项目管理',action='新建项目');f.field(330,325,340,'搜索项目','输入项目名称');f.button(695,339,'状态：全部 ▾',170,'secondary');f.button(880,339,'负责人：全部 ▾',190,'secondary');f.button(1090,339,'导出所选 2 项',200,'secondary')
        table(f,330,440,960,['选择','项目名称','负责人','状态','更新 ↓'],[['☑' if i<2 else '□',p[0],p[1],p[2],p[3]] for i,p in enumerate(PROJECTS)],widths=[75,355,160,180,190],rowh=52)
        f.text(330,785,'已选 2 项 / 共 5 项 · 示例按更新时间降序',15,f.muted);f.req('5行项目表，前2行选中、批量导出2项；列包含选择/名称/负责人/状态/更新时间，降序日期10-10到10-06。')
    elif s=='detail-drawer':
        f.app('ATLAS',['项目列表','活动','团队']);f.heading('项目详情');table(f,330,335,500,['项目','状态'],[['Atlas 设计系统','进行中'],['知识库索引','待审核'],['组件文档','已完成']],widths=[300,200],rowh=90)
        f.panel(865,295,425,495,'Atlas 设计系统');f.text(1250,330,'×',25,f.muted,anchor='end');f.badge(895,370,'进行中');f.lines(895,450,['负责人：林老师','更新时间：2026-10-10','截止日期：2026-10-18'],17,step=43);f.text(895,600,'完成比例 / 48%',16,f.muted);f.progress(895,625,365,48);f.button(895,710,'打开完整项目',365);f.req('详情抽屉保留列表上下文；同一Atlas项目负责人/状态/进度48%一致，关闭与完整页面入口明确。')
    elif s=='pricing-usage':
        f.app('ATLAS',['账户','套餐与用量','账单'],1);f.heading('套餐与用量',action='升级套餐');f.panel(330,320,960,140,'当前套餐 / Team');f.text(360,410,'¥199 / 月 · 下次续费 2026-11-01',23,weight=600);f.badge(1110,365,'当前套餐',w=140)
        for i,(name,v,total,unit) in enumerate([('任务次数',800,1000,'次'),('知识库空间',6,10,'GB'),('团队席位',4,5,'人')]):
            y=500+i*88;f.text(360,y,name,18);f.text(1250,y,f'{v} / {total} {unit}',18,f.muted,anchor='end');f.progress(360,y+24,890,v,total)
        f.text(360,795,'额度统计为本月快照；升级前先查看权益与续费规则。',14,f.muted);f.req('三项用量800/1000次、6/10GB、4/5席位，进度80/60/80%；额度与套餐价格、周期和续费日期分开表达。')
    else:return False
    return True

def ai_views(f):
    s=f.slug
    if s=='ai-chat-workbench':
        f.app('ATLAS AI',['+ 新建对话','组件规范分析','经营报告摘要','知识库','设置'],1);f.heading('组件规范分析',action='分享对话');f.badge(330,301,'知识库已启用',w=165);f.badge(510,301,'Atlas Pro',w=140)
        f.rect(680,355,570, 80,f.tint);f.lines(710,388,['检查新版按钮规范，列出需要修改的地方。','附件：组件规范.pdf'],16,step=28)
        f.avatar(352,480,'AI');f.lines(390,481,['已检查文档中的 5 类按钮状态。','建议优先补齐键盘聚焦与禁用原因。[1]','输入错误应说明如何修正，而不只标红。[2]'],18,step=38)
        f.badge(390,610,'[1] 第 4 页',w=140);f.badge(550,610,'[2] 第 7 页',w=140);f.text(390,675,'复制    /    重新生成    /    反馈',15,f.muted)
        f.panel(330,710,960, 90);f.text(355,744,'继续追问，或添加文件…',17,f.muted);f.text(355,781,'＋ 附件       模型：Atlas Pro',14,f.muted);f.button(1155,745,'发送',110);f.req('完整AI工作台：会话侧栏、附件、带[1]/[2]来源的回答、页码引用、复制/重新生成/反馈、模型选择与输入栏；这是已完成回答快照。')
    elif s=='model-parameters':
        f.app('ATLAS AI',['模型选择','参数','预设'],0);f.heading('模型与生成参数',action='保存预设')
        for i,(name,detail,selected) in enumerate([('Atlas Lite','快速响应 / 日常整理',False),('Atlas Pro','复杂推理 / 文档分析',True),('Atlas Local','本地部署 / 专用任务',False)]):
            y=320+i*139;f.panel(330,y,450,115);f.check(358,y+30,'checked' if selected else 'unchecked',True);f.text(398,y+47,name,22,weight=600);f.text(358,y+85,detail,16,f.muted)
        f.panel(805,320,485,450,'当前模型 / Atlas Pro');f.field(840,410,415,'温度 / 示例参数','0.7');f.text(840,540,'最大输出长度 / 4,096 tokens',17);f.progress(840,570,415,4096,8192);f.lines(840,635,['较高温度通常提高采样多样性。','实际支持范围由模型决定。','参数不会保证事实正确或输出质量。'],16,f.muted,step=34);f.req('三模型为虚构产品命名；单选Atlas Pro，温度.7与最大输出4096/8192示例；参数含义和模型能力边界明确。')
    elif s=='agent-execution':
        f.app('ATLAS AGENT',['当前任务','历史运行','工具权限'],0);f.heading('分析组件规范',action='停止任务');f.text(330,315,'任务：检查文档并整理可执行建议',17,f.muted)
        states=[('✓','读取文档','已完成 / 8 页',f.green),('✓','检索相关规范','已完成 / 3 条来源',f.green),('●','整理建议','进行中 / 未执行外部修改',f.blue),('○','等待确认','尚未开始 / 确认后才可继续',f.muted)]
        for i,(icon,title,detail,col) in enumerate(states):
            y=350+i*94;f.circle(351,y+20,13,f.tint);f.text(351,y+25,icon,14,col,anchor='middle');f.text(380,y+26,title,20,col,weight=600);f.text(380,y+55,detail,15,f.muted)
            if i<3:f.line(351,y+36,351,y+82)
        f.panel(830,350,460,365,'工具调用 / 只读');f.lines(865,442,['read_document / 已完成','search_knowledge / 已完成','write_project / 尚未授权'],17,f.muted,step=50);f.badge(865,620,'需要用户确认',w=180);f.emphasize(337,531,465,80);f.text(330,790,'快照为整理建议中；强调不意味着自动批准下一步。',14,f.muted,attrs='class="fallback"');f.req('四步骤完成/完成/进行中/未开始，工具只读已执行，写入未授权；确认不能被循环动画自动跳过。')
    elif s=='knowledge-citations':
        f.app('ATLAS KNOWLEDGE',['检索','资料库','引用记录']);f.heading('知识库检索与引用');f.field(330,330,960,'检索问题','按钮应该如何支持键盘聚焦？','focus')
        for i,(title,meta,body) in enumerate([('组件规范.pdf','第 4 页 / 更新 2026-10-08','键盘聚焦使用独立外框，保持操作位置可识别。'),('可访问性检查清单.md','第 2 节 / 更新 2026-10-06','不要仅用颜色表达选中、错误或禁用状态。')]):
            y=440+i*160;f.panel(330,y,960,136);f.badge(355,y+21,f'来源 [{i+1}]',w=100);f.text(475,y+43,title,21,weight=600);f.text(355,y+80,body,17);f.text(355,y+111,meta,14,f.muted);f.text(1255,y+111,'打开原文',15,f.blue,anchor='end')
        f.text(330,790,'引用编号与原文位置对应；示例资料为虚构内容，不编造置信度评分。',14,f.muted);f.req('检索问题与两条出处对应，包含文件名/页码或章节/更新时间；引用明确可追溯，不展示无依据的相关性百分比。')
    elif s=='generation-compare':
        f.panel(130,235,1140,565,'生成结果对比 / 同一请求');f.text(170,315,'请求：用一句话解释键盘聚焦状态。',19)
        for i,(title,body,assessment) in enumerate([('版本 A',['按钮要有明显的聚焦框，','这样用户才能知道当前选中了哪里。'],'清楚说明位置，术语仍可更精确'),('版本 B',['键盘聚焦框标示当前可操作控件，','帮助用户用 Tab 键确认操作位置。'],'明确输入方式与操作对象')]):
            x=170+i*550;f.panel(x,355,510,335,title);f.lines(x+28,453,body,20,step=42);f.text(x+28,570,assessment,15,f.muted);f.button(x+28,615,'采用此版本',454,'primary' if i==1 else 'secondary')
        f.text(170,750,'对比措辞与解释范围；评价为编辑判断，不是自动质量评分。',16,f.muted);f.req('同一请求的两段不同输出并排，版本B明确键盘/Tab/操作对象；支持独立采用，评价不伪装成客观分数。')
    else:return False
    return True

def business_views(f):
    s=f.slug
    if s=='todo-today':
        f.app('ATLAS',['今天','全部任务','项目','已完成']);f.heading('今天的任务',action='新建任务');f.text(330,315,'2026 年 10 月 10 日 · 星期六',17,f.muted)
        for i,(day,date) in enumerate(zip(['一','二','三','四','五','六','日'],range(5,12))):
            x=330+i*139;f.rect(x,345,124, 70,f.tint if date==10 else f.paper,8,attrs=f'stroke="{f.blue if date==10 else f.linecolor}"');f.text(x+62,372,day,14,f.muted,anchor='middle');f.text(x+62,401,date,21,f.blue if date==10 else f.ink,anchor='middle',weight=600)
        for i,(title,detail,done) in enumerate([('检查组件聚焦状态','设计系统 / 今天 10:00',True),('整理知识库引用','知识库 / 今天 14:00',False),('确认首页文案','产品改版 / 今天 16:30',False)]):
            y=450+i*112;f.panel(330,y,960,92);f.check(355,y+30,'checked' if done else 'unchecked');f.text(395,y+42,title,21,f.muted if done else f.ink);f.text(395,y+73,detail,15,f.muted)
        f.text(330,805,'已完成 1 / 共 3 项',15,f.muted);f.req('2026-10-10星期六；周历10月5日至11日，10日选中；3任务1完成，日期、状态和计数一致。')
    elif s=='chat-messenger':
        f.app('ATLAS CHAT',['设计团队 · 2','产品团队','林老师','陈同学'],0);f.heading('设计团队',action='查看成员');f.text(330,315,'6 位成员 · 讨论与文件共享',16,f.muted)
        f.avatar(353,378,'林');f.rect(390,340,600,115,f.tint);f.lines(420,383,['新版规范已经更新。','请重点检查键盘聚焦与错误提示。'],19,step=34);f.text(390,482,'林老师 · 10:32',13,f.muted)
        f.rect(740,520,510,90,f.tint);f.text(770,559,'收到，我会在下午反馈检查结果。',18);f.text(770,589,'附件：检查清单.md',15,f.blue);f.text(1250,643,'你 · 10:35 · 已发送',13,f.muted,anchor='end')
        f.panel(330,690,960,110);f.text(355,730,'发送消息到设计团队…',17,f.muted);f.text(355,775,'＋ 文件    /    @ 提及成员',15,f.muted);f.button(1150,735,'发送',115);f.req('会话列表保留2条未读提示；聊天有作者/时间/发送状态/附件与输入操作，不以气泡位置代替身份。')
    elif s=='ecommerce-home':
        f.app('ATLAS STORE',['全部商品','工作设备','配件','收藏']);f.heading('为工作桌面挑选设备',action='购物车 · 2');f.field(330,330,960,'搜索商品','搜索名称或型号');products=[('轻量耳机','舒适佩戴 / 通话降噪',199),('机械键盘','紧凑布局 / 有线连接',299),('桌面支架','高度可调 / 金属底座',99)]
        for i,(name,detail,price) in enumerate(products):
            x=330+i*328;f.panel(x,440,304,350);f.rect(x+16,456,272,150,f.tint,8)
            if i==0:f.add(f'<path d="M{x+90} 550 A62 62 0 0 1 {x+214} 550" fill="none" stroke="{f.blue}" stroke-width="10"/>');f.rect(x+80,535,30,50,f.blue,8);f.rect(x+194,535,30,50,f.blue,8)
            elif i==1:
                f.rect(x+40,488,224,90,f.paper,8,attrs=f'stroke="{f.blue}" stroke-width="2"')
                for row in range(3):
                    for col in range(8):f.rect(x+54+col*26,502+row*22,18,13,f.tint,3)
            else:f.line(x+90,570,x+210,570,f.blue,10);f.line(x+150,570,x+150,505,f.blue,9);f.line(x+112,500,x+204,478,f.blue,9)
            f.text(x+20,642,name,23,weight=600);f.text(x+20,675,detail,14,f.muted);f.text(x+20,734,f'¥{price}',27,weight=700);f.button(x+160,708,'加入购物车',124)
        f.req('三商品199/299/99元，使用纯矢量产品示意；目录、搜索与购物车操作明确，无虚假折扣或倒计时。')
    elif s=='kanban-board':
        f.app('ATLAS',['项目看板','日历','成员']);f.heading('设计系统 · 任务看板',action='新建任务');cols=[('待开始',[('更新图标资源','周同学 / 10-14'),('补充空状态','林老师 / 10-15')]),('进行中',[('检查键盘聚焦','林老师 / 10-12'),('整理文档引用','陈同学 / 10-13')]),('已完成',[('统一按钮尺寸','周同学 / 10-09')])]
        for i,(label,cards) in enumerate(cols):
            x=330+i*328;f.rect(x,320,304,470,f.tint,10);f.text(x+20,360,f'{label} · {len(cards)}',20,weight=600)
            for j,(title,detail) in enumerate(cards):y=385+j*150;f.panel(x+12,y,280,130);f.text(x+30,y+40,title,20,weight=600);f.text(x+30,y+80,detail,15,f.muted);f.badge(x+30,y+95,'设计规范',w=100)
        f.req('三列待开始2/进行中2/已完成1，共5任务；每卡包含负责人和日期，拖动只是状态示意。')
    elif s=='members-permissions':
        f.app('ATLAS',['成员','角色权限','邀请记录']);f.heading('成员与访问权限',action='邀请成员');f.text(330,315,'4 位成员 · 所有者角色不可直接移除',16,f.muted)
        rows=[('林老师','所有者','全部管理权限','已加入'),('陈同学','管理员','管理内容与成员','已加入'),('周同学','编辑者','编辑项目内容','已加入'),('许同学','查看者','仅查看已授权项目','已加入')];table(f,330,350,960,['成员','角色','权限范围','状态'],rows,[190,170,420,180],rowh=80)
        f.panel(330,735,960,64);f.text(355,775,'权限作用于当前工作区；项目可设置更小范围的访问权限。',16,f.muted);f.req('所有者/管理员/编辑者/查看者四角色，权限范围明确；不能用角色标签暗示全部项目天然可见。')
    elif s=='checkout-payment':
        f.panel(130,240,560,555,'确认订单');f.text(165,350,'Team 套餐 / 月付',26,weight=600);f.lines(165,420,['套餐价格：¥199.00','数量：1','小计：¥199.00','额外费用：¥0.00'],19,step=47);f.line(165,618,655,618);f.text(165,675,'应付金额',20);f.text(655,675,'¥199.00',32,anchor='end',weight=700)
        f.panel(730,240,540,555,'支付状态 / 待支付');f.field(765,365,470,'支付方式','组织支付账号  ▾');f.text(765,480,'确认后才会提交支付请求。',18);f.text(765,523,'支付成功后开通权益，并提供收据。',16,f.muted);f.button(765,610,'确认支付 ¥199.00',470);f.button(765,680,'返回修改订单',470,'secondary');f.req('199×1+0=199元；当前待支付，明确确认后才提交；金额与按钮一致，不能用动画直接跳到支付成功。')
    else:return False
    return True

def dashboard(f,ops=False):
    f.app('NOVA OPS' if ops else 'ATLAS BI',['概览','服务' if ops else '销售分析','告警' if ops else '渠道','设置']);f.heading('服务运行概览' if ops else '经营分析概览',action='查看告警' if ops else '导出报告');f.text(330,315,'模拟快照 / 固定业务数据' if ops else '2026-10-01 至 2026-10-08 / 模拟经营数据',16,f.muted)
    f.add('<g id="dashboard-snapshot">')
    cards=[('当前 QPS','46.2k'),('P99 延迟','182 ms'),('错误率','0.03%'),('服务状态','3 正常 / 1 降级')] if ops else [('销售额','¥128,450'),('订单数','840'),('客单价','¥152.92'),('支付转化率','3.86%')]
    for i,(title,value) in enumerate(cards):
        x=330+i*244;f.panel(x,345,228,115);f.text(x+18,377,title,15,f.muted);f.text(x+18,423,value,24 if ops and i==3 else 27,weight=700)
    f.panel(330,485,610,290,'QPS / 千次每秒' if ops else '每日销售额 / 元');values=OPS_QPS if ops else REVENUE;maximum=60 if ops else 20000;pts=[(370+j*73,716-v/maximum*155) for j,v in enumerate(values)]
    for value in [0,maximum/2,maximum]:y=716-value/maximum*155;f.line(370,y,905,y);f.text(358,y+5,f'{value:g}',12,f.muted,anchor='end')
    f.path(pts,f.blue,2.5,attrs='data-series="'+','.join(map(str,values))+'" data-maximum="'+str(maximum)+'"')
    for j,(x,y) in enumerate(pts):f.circle(x,y,3,f.blue);f.text(x,750,f'10-{j+1:02d}',11,f.muted,anchor='middle')
    f.panel(965,485,325,290,'服务状态' if ops else '渠道销售占比')
    for i,(label,value) in enumerate([('API Gateway','正常'),('Search Index','正常'),('Task Worker','降级'),('Storage','正常')] if ops else [('自然搜索',40),('直接访问',30),('内容推荐',20),('合作渠道',10)]):
        y=555+i*56;f.text(985,y,label,14);f.text(1265,y,str(value)+('' if ops else '%'),14,f.orange if value=='降级' else f.green if ops else f.muted,anchor='end')
        if not ops:f.progress(985,y+12,280,value,h=5)
    f.add('</g>')
    if f.animated:
        if ops:f.emphasize(973,642,309,47);f.text(330,805,'巡检强调固定降级项；读数为快照，不连接实时服务。',14,f.muted,attrs='class="fallback"')
        else:
            f.add('<g class="motion"><animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="1.4s" fill="freeze"/>');f.rect(331,486,608,288,f.paper);f.text(635,640,'正在呈现经营快照…',17,f.muted,anchor='middle');f.add('</g>');f.text(330,805,'入场结束保留完整快照；数据不从零假装实时增长。',14,f.muted,attrs='class="fallback"')
    f.req('四KPI与图表共用显式示例数据；'+('QPS末值46.2k，服务3正常/1降级，动画只强调降级项。' if ops else '每日销售额'+json.dumps(REVENUE)+'，合计128450元；订单840，客单价128450/840≈152.92元；渠道40/30/20/10%合计100%。'))
    f.req('静态与动画的dashboard-snapshot分组完全一致；图表有单位、刻度和日期，固定快照不标注LIVE。')

SIGNAL_N=128
SIGNAL=[math.sin(2*math.pi*3*j/SIGNAL_N)+.5*math.sin(2*math.pi*8*j/SIGNAL_N) for j in range(SIGNAL_N)]
SPECTRUM=[2/SIGNAL_N*abs(sum(v*complex(math.cos(-2*math.pi*k*j/SIGNAL_N),math.sin(-2*math.pi*k*j/SIGNAL_N)) for j,v in enumerate(SIGNAL))) for k in range(17)]
def full_views(f):
    s=f.slug
    if s in ('bi-dashboard','dashboard','dark-ops-dashboard','live-ops-dashboard'):dashboard(f,s in ('dark-ops-dashboard','live-ops-dashboard'))
    elif s=='fitness-dashboard':
        f.app('ATLAS MOVE',['活动概览','训练计划','历史记录']);f.heading('本周活动',action='查看计划');f.text(330,315,'活动快照 / 示例数据，不作为健康诊断',16,f.muted)
        for i,(label,value,total) in enumerate([('今日步数',7200,10000),('活动分钟',28,40),('站立小时',9,12)]):
            x=480+i*330;y=430;r=64;circ=2*math.pi*r;f.circle(x,y,r,'none',attrs=f'stroke="{f.linecolor}" stroke-width="9"');f.circle(x,y,r,'none',attrs=f'stroke="{f.blue}" stroke-width="9" stroke-dasharray="{circ*value/total:.5f} {circ:.5f}" transform="rotate(-90 {x} {y})" data-ring="{value}" data-total="{total}"');f.text(x,y+5,value,27,anchor='middle',weight=700);f.text(x,y+37,f'/ {total}',14,f.muted,anchor='middle');f.text(x,540,label,17,f.muted,anchor='middle')
        f.panel(330,580,960,210,'每日训练分钟 / 本周合计 170 分钟')
        for j,v in enumerate([15,30,0,45,20,35,25]):x=380+j*125;f.rect(x,735-v*2, 50,v*2,f.blue,5,attrs=f'data-minutes="{v}"');f.text(x+25,724-v*2,v,14,f.muted,anchor='middle');f.text(x+25,770,['一','二','三','四','五','六','日'][j],13,f.muted,anchor='middle')
        f.req('三环7200/10000步、28/40分钟、9/12小时；训练分钟15/30/0/45/20/35/25合计170，环弧与数字比例一致。')
    elif s=='music-player':
        f.app('ATLAS SOUND',['正在播放','播放列表','收藏']);f.heading('专注播放',action='查看队列');f.panel(330,320,460,460);f.rect(365,350,390,245,f.tint,12)
        for j in range(12):f.line(405+j*27,555,405+j*27,405+50*math.sin(j),f.blue,4)
        f.text(365,637,'Night Circuit',28,weight=700);f.text(365,676,'Atlas Studio / 示例曲目',16,f.muted);f.button(365,710,'暂停',390)
        f.panel(815,320,475,460,'播放队列');table(f,840,400,425,['曲目','时长'],[['Night Circuit','4:00'],['Quiet Signals','3:20'],['Blue Horizon','5:10']],widths=[320,105],rowh=70);f.progress(840,690,425,80,240);f.text(840,732,'1:20',15,f.muted);f.text(1265,732,'4:00',15,f.muted,anchor='end');f.emphasize(340,698,440,57);f.text(840,766,'播放状态演示 / 时间保持快照',13,f.muted,attrs='class="fallback"');f.req('正在播放Night Circuit，进度80/240秒与1:20/4:00一致；动画只强调播放控件，不让固定时间读数与滚动进度冲突。')
    elif s=='hud-interface':
        f.panel(110,230,1180,570);cx,cy=700,510;r=195
        for rr in [100,160,195]:f.circle(cx,cy,rr,'none',attrs=f'stroke="{f.linecolor}"')
        for d in range(0,360,10):
            t=math.radians(d-90);f.line(cx+(r-12)*math.cos(t),cy+(r-12)*math.sin(t),cx+r*math.cos(t),cy+r*math.sin(t),f.blue,2 if d%30==0 else 1)
        for d,label in [(0,'N'),(90,'E'),(180,'S'),(270,'W')]:t=math.radians(d-90);f.text(cx+230*math.cos(t),cy+230*math.sin(t)+6,label,18,f.muted,anchor='middle')
        angle=math.radians(68-90);tx=cx+145*math.cos(angle);ty=cy+145*math.sin(angle);f.path([(cx,cy),(tx,ty)],f.blue,3,attrs='data-bearing="68"');f.circle(tx,ty,9,f.green);f.emphasize(tx-20,ty-20,40,40,f.green);f.text(cx,cy+60,'航向 068°',27,anchor='middle',weight=600)
        f.lines(150,330,['NAV CONCEPT','速度 12 m/s','高度 120 m','距离 350 m'],18,f.muted,step=60);f.lines(1060,355,['目标点 / DEMO','固定航向刻度','状态强调圈','非导航设备'],17,f.muted,step=60);f.text(160,765,'固定读数与刻度对应；仅目标框缓慢强调，不旋转有数值含义的刻度。',15,f.muted,attrs='class="fallback"');f.req('航向以北为0顺时针，68°指向右上；指示线与读数一致，固定刻度不做装饰旋转；概念界面不用于实际导航。')
    elif s=='wave-analyzer':
        f.app('ATLAS LAB',['信号概览','频谱','采样设置']);f.heading('波形与单边频谱');f.text(330,315,'模拟采样 / N=128 / 一个观察周期 / 频率单位：bin',16,f.muted);f.panel(330,340,960,235,'时域信号 / 幅值')
        for value in [-1,0,1]:y=455-value*55;f.line(375,y,1245,y);f.text(363,y+5,value,12,f.muted,anchor='end')
        f.add('<defs><clipPath id="wave-window"><rect x="375" y="389" width="870" height="146"/></clipPath></defs><g clip-path="url(#wave-window)">')
        pts=[(375+j*870/SIGNAL_N,455-SIGNAL[j%SIGNAL_N]*55) for j in range(2*SIGNAL_N+1)];f.add('<g class="motion">');f.path(pts,f.blue,2);f.add('<animateTransform attributeName="transform" type="translate" from="0 0" to="-870 0" dur="8s" repeatCount="indefinite"/></g>');f.path(pts[:129],f.blue,2,attrs='class="fallback"');f.add('</g>')
        f.panel(330,600,960,195,'DFT 单边幅值 / 频谱与波形共用数据')
        for k,v in enumerate(SPECTRUM):
            x=390+k*51;f.rect(x,748-v*85,24,v*85,f.blue,3,attrs=f'data-bin="{k}" data-amplitude="{v:.10f}"');f.text(x+12,776,k,12,f.muted,anchor='middle')
        f.req('128点信号sin(2π3n/128)+.5sin(2π8n/128)，DFT单边幅值2|Σsₙexp(−i2πkn/N)|/N，k0..16；峰值bin3=1、bin8=.5，其余数值近0。');f.req('时域平移一个完整870px周期，固定频谱不乱跳，因为时移不改变幅值谱；这是模拟界面而非真实测量。')
    else:return False
    return True

def build():
    BUILT.clear()
    for group,entries in GROUPS:
        for slug,title in entries:
            f=UI(slug,title,group)
            if not any(fn(f) for fn in [primitives,navigation,feedback,data_views,ai_views,business_views,full_views]):raise ValueError('Missing renderer: '+slug)
            f.finish()
    assert len(BUILT)==60
    print('Built 60 UI specimens.')
if __name__=='__main__':build()
