#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build semantic technical diagrams from explicit nodes, ports and relationships."""
from pathlib import Path
from html import escape
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'gallery' / 'diagrams'
BUILT = []
COLOR = {'call':'#3686d9', 'event':'#d99431', 'data':'#00a887', 'control':'#bc637d', 'neutral':'#8093a6'}


def attrs(values):
    return ' '.join(f'{key}="{escape(str(value), quote=True)}"' for key, value in values.items())


def path(points):
    return 'M ' + ' L '.join(f'{x:g} {y:g}' for x,y in points)


class Diagram:
    def __init__(self, slug, title, subtitle, takeaway, dark=False, animated=False, footer='概念结构示意 · 不代表完整生产部署或真实运行状态'):
        self.slug, self.title, self.subtitle = slug, title, subtitle
        self.takeaway, self.animated, self.footer = takeaway, animated, footer
        self.bg = '#0d1724' if dark else '#f3f5f7'
        self.box = '#182b3f' if dark else '#ffffff'
        self.ink = '#edf3fa' if dark else '#172a3a'
        self.muted = '#a5b6c9' if dark else '#596e81'
        self.grid = '#2d4155' if dark else '#d7e0e9'
        self.layers, self.nodes, self.edges, self.notes = [], {}, [], []
        self.dark = dark

    def text(self,x,y,text,size=18,fill=None,anchor='start',weight=400):
        return f'<text {attrs(dict(x=x,y=y,fill=fill or self.ink,**{"font-size":size,"text-anchor":anchor,"font-weight":weight}))}>{escape(str(text))}</text>'

    def boundary(self,x,y,w,h,title,color='neutral'):
        self.layers.append(f'<rect {attrs(dict(x=x,y=y,width=w,height=h,rx=12,fill="none",stroke=COLOR[color],**{"stroke-dasharray":"6 5","stroke-opacity":.65}))}/>'+self.text(x+18,y+28,title,17,COLOR[color],weight=600))

    def note(self,x,y,text,size=16,fill=None,anchor='start'):
        self.notes.append(self.text(x,y,text,size,fill,anchor))

    def node(self,identity,x,y,w,h,title,sub=(),kind='box',color='call',terminal=False,start=False):
        if identity in self.nodes: raise ValueError(f'duplicate node: {identity}')
        if isinstance(sub,str): sub=[sub]
        self.nodes[identity]=dict(id=identity,x=x,y=y,w=w,h=h,title=title,sub=list(sub),kind=kind,color=color,terminal=terminal,start=start)
        return identity

    def port(self,identity,side):
        n=self.nodes[identity];x,y,w,h=[n[k] for k in ['x','y','w','h']]
        return {'l':(x,y+h/2),'r':(x+w,y+h/2),'t':(x+w/2,y),'b':(x+w/2,y+h)}[side]

    def edge(self,source,target,sp='r',tp='l',via=(),label='',at=None,kind='call',animate=False,guard='',arrow=True,points=None):
        if source not in self.nodes or target not in self.nodes: raise ValueError((source,target))
        pts=list(points) if points is not None else [self.port(source,sp),*via,self.port(target,tp)]
        if any(x1!=x2 and y1!=y2 for (x1,y1),(x2,y2) in zip(pts,pts[1:])): raise ValueError(f'non-orthogonal edge: {self.slug} {source}->{target}')
        self.edges.append(dict(id=f'edge-{len(self.edges)+1}',source=source,target=target,sp=sp,tp=tp,points=pts,label=label,at=at,kind=kind,animate=animate,guard=guard,arrow=arrow,custom=points is not None))

    def render_node(self,n):
        x,y,w,h=[n[k] for k in ['x','y','w','h']];color=COLOR[n['color']]
        outer=attrs({'id':'node-'+n['id'],'data-node':n['id'],'data-kind':n['kind'],'data-terminal':str(n['terminal']).lower(),'data-start':str(n['start']).lower(),'data-box':f'{x},{y},{w},{h}'})
        if n['kind']=='event':
            shape=f'<circle cx="{x+w/2}" cy="{y+h/2}" r="{w/2}" fill="{self.box}" stroke="{color}" stroke-width="3"/>'
            return f'<g {outer}>{shape}</g>'
        if n['kind']=='diamond':
            shape=f'<path d="{path([(x+w/2,y),(x+w,y+h/2),(x+w/2,y+h),(x,y+h/2)])} Z" fill="{self.box}" stroke="{color}" stroke-width="2"/>'
        else:
            shape=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if n["kind"]=="pill" else 8}" fill="{self.box}" stroke="{color}" stroke-width="1.6"/>'
        if n['kind']=='entity':
            shape+=f'<line x1="{x}" y1="{y+52}" x2="{x+w}" y2="{y+52}" stroke="{color}"/>'
            text=self.text(x+18,y+33,n['title'],22,weight=600)
            text+=''.join(self.text(x+18,y+81+i*28,line,16,self.muted) for i,line in enumerate(n['sub']))
        else:
            size=17 if w<=145 else 19 if w<=200 else 22
            baseline=y+h/2+7 if not n['sub'] else y+31 if h<=85 else y+38
            if n['kind']=='diamond': baseline=y+h/2-4 if n['sub'] else y+h/2+6
            text=self.text(x+w/2,baseline,n['title'],size,anchor='middle',weight=600)
            text+=''.join(self.text(x+w/2,baseline+27+i*24,line,15 if w<180 else 16,self.muted,'middle') for i,line in enumerate(n['sub']))
        return f'<g {outer}>{shape}{text}</g>'

    def finish(self,requirements,tech=('orthogonal routing','ports','semantic edges')):
        edge_svg=[];edge_labels=[]
        for e in self.edges:
            color=COLOR[e['kind']];points=' '.join(f'{x:g},{y:g}' for x,y in e['points'])
            values={'id':e['id'],'data-edge':e['id'],'data-source':e['source'],'data-target':e['target'],'data-source-port':e['sp'],'data-target-port':e['tp'],'data-guard':e['guard'],'data-route':'custom' if e['custom'] else 'ports','points':points,'fill':'none','stroke':color,'stroke-width':2,'stroke-linejoin':'round'}
            if e['arrow']:values['marker-end']='url(#arrow-'+e['kind']+')'
            if e['kind'] in ('event','control','neutral'):values['stroke-dasharray']='6 5'
            edge_svg.append('<polyline '+attrs(values)+'/>')
            if self.animated and e['animate']:
                edge_svg.append(f'<path class="flow" data-animated-edge="{e["id"]}" d="{path(e["points"])}" fill="none" stroke="{color}" stroke-width="4"/>')
            if e['label']:
                x,y=e['at'] if e['at'] else ((e['points'][0][0]+e['points'][-1][0])/2,(e['points'][0][1]+e['points'][-1][1])/2-12)
                edge_labels.append(self.text(x,y,e['label'],15,color,'middle'))
        markers=''.join(f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="{color}"/></marker>' for name,color in COLOR.items())
        style='<style>.flow{stroke-dasharray:7 17;animation:flow 2.8s linear infinite}@keyframes flow{to{stroke-dashoffset:-48}}.event-focus{animation:focus 6s infinite}@keyframes focus{0%,100%{stroke-width:2}35%,55%{stroke-width:7}}@media(prefers-reduced-motion:reduce){.flow{animation:none;display:none}.event-focus{animation:none;stroke-width:2}}</style>' if self.animated else ''
        header=f'<rect width="1400" height="900" fill="{self.bg}"/>'+self.text(72,55,'SVG / SYSTEM ATLAS',14,self.muted)+f'<line x1="72" y1="73" x2="1328" y2="73" stroke="{self.grid}"/>'+self.text(72,122,self.title,34,weight=700)+self.text(72,160,self.subtitle,18,self.muted)+f'<rect x="72" y="183" width="1256" height="51" rx="5" fill="{"#172c40" if self.dark else "#e6edf3"}"/>'+self.text(92,215,self.takeaway,18,weight=600)
        footer=f'<line x1="72" y1="845" x2="1328" y2="845" stroke="{self.grid}"/>'+self.text(72,877,self.footer,15,self.muted)+self.text(1328,877,'SVG-PROMPT',14,self.muted,'end')
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" font-family="PingFang SC, Microsoft YaHei, sans-serif" role="img" aria-labelledby="title desc"><title id="title">'+escape(self.title)+'</title><desc id="desc">'+escape(self.takeaway+'。'+self.footer)+'</desc><defs>'+markers+'</defs>'+style+header+''.join(self.layers)+''.join(edge_svg)+''.join(self.render_node(n) for n in self.nodes.values())+''.join(edge_labels)+''.join(self.notes)+footer+'</svg>\n'
        p=OUT/self.slug;p.mkdir(exist_ok=True)
        (p/'index.svg').write_text(svg,encoding='utf-8')
        old=json.loads((p/'meta.json').read_text()) if (p/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
        old.update(slug=self.slug,title=self.title,space='2d',time='css' if self.animated else 'static',description=self.takeaway,tech=list(tech)+(['CSS semantic flow','reduced motion'] if self.animated else []))
        (p/'meta.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        steps=[f'用 SVG 制作“{self.title}”：{self.subtitle}。','- 画布1400×900，背景'+self.bg+'；标题34px、组件名17–22px、说明15–16px；语义配色：调用蓝、事件橙、数据绿、控制红、关联灰。', '- 重点表达：“'+self.takeaway+'”。']+['- '+s for s in requirements]
        if self.nodes:
            steps.append('- 先列节点坐标与端口；端口l/r/t/b分别为矩形左/右/上/下中点，菱形为对应顶点。按下列坐标绘制：')
            steps += [f'  - {n["id"]}: {n["title"]}；说明{json.dumps(n["sub"],ensure_ascii=False)}；(x,y,w,h)=({n["x"]},{n["y"]},{n["w"]},{n["h"]})；形状{n["kind"]}。' for n in self.nodes.values()]
        if self.edges:
            steps.append('- 连线先画、节点后画，线不穿过无关节点。下列方向、条件与折点必须一致：')
            steps += [f'  - {e["source"]} → {e["target"]}；{e["kind"]}；标签“{e["label"]}”；条件“{e["guard"]}”；折点{json.dumps(e["points"])}；'+('有箭头。' if e['arrow'] else '无箭头，仅表示关联或层级。') for e in self.edges]
        if self.animated:steps.append('- 完整文字和节点从首帧起可见；CSS只改变路径叠加层的stroke-dashoffset或事件圈stroke-width，不改变节点、端点、条件或顺序。动效是演示、不编码吞吐量或真实在线状态。prefers-reduced-motion: reduce时去掉动态叠加层，保留完整静态结构。')
        steps.append('- 页脚注明：“'+self.footer+'”。')
        label='CSS 动效' if self.animated else '静态'
        (p/'prompt.md').write_text(f'# {self.title} `{label}` `2D`\n\n分类：[流程与架构](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+'\n'.join(steps)+'\n```\n',encoding='utf-8')
        BUILT.append(self.slug)


def process(animated=False):
    d=Diagram('process-walk' if animated else 'process-steps','交付流程 · 动态路径' if animated else '输入与输出流程','需求 → 生成 → 验证 → 归档','每一步有明确输入与输出；验证不通过时返回生成',animated=animated)
    stages=[('request','01 需求定义',['输入：目标与约束','输出：验收清单']),('generate','02 生成作品',['输入：清单与提示词','输出：SVG 初稿']),('validate','03 验证结果',['输入：初稿与清单','输出：差异或通过']),('archive','04 归档交付',['输入：已通过作品','输出：三件套与版本'])]
    for i,(identity,title,sub) in enumerate(stages):d.node(identity,100+300*i,365,230,170,title,sub,start=i==0,terminal=i==3)
    for a,b in zip(stages,stages[1:]):d.edge(a[0],b[0],animate=True,label='通过' if a[0]=='validate' else '',at=(965,438) if a[0]=='validate' else None,guard='验收通过' if a[0]=='validate' else '')
    d.edge('validate','generate','b','b',via=[(815,675),(515,675)],label='未通过：携带差异清单返回',at=(665,654),kind='control',guard='验收不通过')
    d.note(700,787,'步骤编号是执行顺序；返回路径表达修正，不代表无限自动重试。',anchor='middle')
    d.finish(['按四个阶段展示输入与输出，不把“生成”当成已经验证成功。','验证→归档条件为通过，验证→生成条件为未通过；重试策略由具体实施流程决定。'])


def decision():
    d=Diagram('decision-flowchart','质量决策与有限重试','渲染检查、提示词对齐、修复与退出','两次判断都有是／否分支；达到重试上限必须停止')
    d.node('start',100,350,150,70,'开始',kind='pill',start=True)
    d.node('generate',370,350,190,70,'生成 SVG')
    d.node('render',750,335,190,100,'渲染通过？',kind='diamond')
    d.node('review',1100,350,190,70,'视觉终审')
    d.node('aligned',750,580,190,100,'提示词对齐？',kind='diamond')
    d.node('publish',1100,595,190,70,'归档交付',kind='pill',terminal=True,color='data')
    d.node('fix',385,715,200,70,'定位与修复',color='control')
    d.node('stop',100,715,160,70,'停止并报告',kind='pill',terminal=True,color='control')
    d.edge('start','generate');d.edge('generate','render');d.edge('render','review',label='是',at=(1020,367),guard='是')
    d.edge('render','fix','b','r',via=[(845,505),(650,505),(650,750)],label='否',at=(800,488),kind='control',guard='否')
    d.edge('review','aligned','b','t',via=[(1195,535),(845,535)],label='检查一致性',at=(1045,518))
    d.edge('aligned','publish',label='是',at=(1020,612),guard='是')
    d.edge('aligned','fix','b','r',via=[(845,750)],label='否',at=(865,721),kind='control',guard='否')
    d.edge('fix','generate','l','l',via=[(310,750),(310,385)],label='重试次数 < 3',at=(310,620),kind='control',guard='retry<3')
    d.edge('fix','stop','l','r',label='≥ 3 次',at=(320,781),kind='control',guard='retry>=3')
    d.note(700,817,'首次生成不计重试；每次进入修复后检查预算，失败原因保留在报告中。',anchor='middle')
    d.finish(['渲染与提示词对齐两判断必须完整覆盖是/否，失败进入定位修复，不直接交付。','最多3次重试，retry<3返回生成且次数加1，retry>=3停止报告；不要吞掉渲染或校验失败。'])


def swimlane():
    d=Diagram('swimlane','跨角色泳道流程','需求方 / 生成系统 / 审核方','泳道表达职责，箭头表达交接；审核失败必须返回修正')
    for x,w,name in [(80,350,'需求方'),(460,400,'生成系统'),(890,430,'审核方')]:d.boundary(x,270,w,535,name)
    d.node('request',160,325,220,70,'提交需求',['目标与验收条件'],start=True)
    d.node('generate',570,325,220,70,'生成初稿',['依据验收清单'])
    d.node('preview',570,500,220,80,'提交预览',['作品与检查结果'])
    d.node('check',980,490,220,100,'审核通过？',kind='diamond')
    d.node('revise',570,680,220,70,'修正差异',['保留审核意见'],color='control')
    d.node('deliver',160,680,220,70,'接收交付',['作品与提示词'],terminal=True,color='data')
    d.edge('request','generate',label='需求交接',at=(475,345));d.edge('generate','preview','b','t',label='渲染与自检',at=(730,453))
    d.edge('preview','check',label='送审',at=(880,520))
    d.edge('check','revise','l','r',via=[(925,540),(925,715)],label='否：差异反馈',at=(917,644),kind='control',guard='否')
    d.edge('revise','generate','l','l',via=[(515,715),(515,360)],label='修正后重送',at=(510,626),kind='control')
    d.edge('check','deliver','b','b',via=[(1090,785),(270,785)],label='是：交付归档',at=(1080,633),kind='data',guard='是')
    d.finish(['三条纵向泳道，节点只能放在其负责角色的泳道里；需求方提交并接收，生成系统生成/自检/修正，审核方判断。','审核是/否分别交付与反馈，修正后回到生成；箭头跨泳道处明确交接内容。'])


def sequence():
    d=Diagram('sequence-diagram','流式请求时序图','客户端 / API / 检索 / 模型；时间从上往下','请求、返回与超时分支分别表示；关闭连接不等于取消后台计算')
    centers=[]
    for i,(identity,title) in enumerate([('client','客户端'),('api','API 服务'),('retrieval','检索服务'),('model','模型服务')]):
        x=105+i*330;d.node(identity,x,280,190,70,title);cx=x+95;centers.append(cx);d.layers.append(f'<line x1="{cx}" y1="350" x2="{cx}" y2="784" stroke="{d.grid}" stroke-dasharray="5 5"/>')
    d.boundary(80,510,1240,269,'alt · 生成成功 / 超时失败')
    messages=[('client','api',388,'1 发起请求','call'),('api','retrieval',435,'2 检索证据','call'),('retrieval','api',482,'3 返回证据','neutral'),('api','model',565,'4 生成请求','call'),('model','api',616,'5 token 流','event'),('api','client',663,'6 SSE 回传','event'),('api','client',747,'超时：错误事件 + 关闭连接','control')]
    for a,b,y,label,kind in messages:
        x1=d.port(a,'t')[0];x2=d.port(b,'t')[0];d.edge(a,b,points=[(x1,y),(x2,y)],label=label,at=((x1+x2)/2,y-13),kind=kind,guard='超时' if y==747 else '成功' if y>=565 else '')
    d.layers.append(f'<line x1="80" y1="697" x2="1320" y2="697" stroke="{d.grid}" stroke-dasharray="5 5"/>')
    d.note(120,730,'[超时]',15,COLOR['control']);d.note(700,819,'纵向间隔为排版，不表示实际耗时；取消模型计算需额外取消协议。',anchor='middle')
    d.finish(['四个参与者的生命线垂直；消息方向遵循请求/返回的实际发送者，按编号由上向下。','生成阶段使用alt分支：成功时token流转发为SSE；超时发送错误事件并关闭客户端连接，两分支不在同一次请求中同时执行。','时间间隔不编码耗时，服务端计算取消与连接关闭分别处理。'],['sequence messages','lifelines','alt branches'])


def state_machine():
    d=Diagram('state-machine','异步任务状态机','排队、执行、退避与终态；最多 3 次尝试','成功、失败、取消都是终态；重试有明确预算与条件')
    for args in [('pending',100,335,'排队中','等待调度'),('running',490,335,'执行中','失败包含校验失败'),('success',960,290,'成功','结果通过校验'),('failed',960,490,'失败','保留最后错误'),('retry',490,620,'退避等待','准备下一次尝试'),('cancelled',100,620,'已取消','任务已停止')]:
        identity,x,y,title,sub=args;d.node(identity,x,y,220,80,title,[sub],terminal=identity in ('success','failed','cancelled'),start=identity=='pending',color='data' if identity=='success' else 'control' if identity in ('failed','cancelled') else 'call')
    d.edge('pending','running',label='调度成功',at=(405,360))
    d.edge('running','success',via=[(840,375),(840,330)],label='输出有效',at=(875,313),guard='success')
    d.edge('running','failed',via=[(840,375),(840,530)],label='失败且 attempt ≥ 3',at=(914,590),kind='control',guard='failure and attempt>=3')
    d.edge('running','retry','b','t',label='失败且 attempt < 3',at=(710,535),kind='control',guard='failure and attempt<3')
    d.edge('retry','running','r','r',via=[(775,660),(775,375)],label='退避结束 · attempt + 1',at=(952,725),kind='control',guard='backoff complete')
    d.edge('pending','cancelled','b','t',label='取消请求',at=(270,540),kind='control',guard='cancel')
    d.edge('running','cancelled','l','r',via=[(380,375),(380,660)],label='收到取消且任务已停止',at=(320,596),kind='control',guard='cancel acknowledged')
    d.edge('retry','cancelled','l','r',label='取消',at=(405,642),kind='control',guard='cancel')
    d.note(700,817,'attempt 从 1 开始；终态不再接受执行转换；取消完成须由执行方确认。',anchor='middle')
    d.finish(['六个状态，attempt从1开始且最多3次；失败包含工具/执行错误和结果校验失败。','排队与退避可取消；执行中的取消只有在执行方停止并确认后才能进入已取消，不能只因客户端断开连接就宣称已取消。','成功/失败/已取消均为终态，无出边。失败可重试与不可重试条件不重叠。'],['state transitions','bounded retry','terminal states'])


def context():
    d=Diagram('system-context','系统上下文图','人与外部系统 / 被设计系统的边界','只解释谁使用系统、系统依赖谁；不混入内部部署细节',dark=True)
    d.boundary(490,370,430,235,'被设计系统 · AI 应用','call')
    d.node('user',100,450,220,90,'终端用户',['提交问题 / 阅读答案'],start=True)
    d.node('app',560,435,280,120,'AI 应用系统',['权限、编排、结果交付'],color='data')
    d.node('model',1040,410,230,100,'外部模型服务',['生成接口'],color='event')
    d.node('search',1040,600,230,90,'企业知识源',['授权文档接口'],color='event')
    d.node('identity',560,680,280,70,'身份提供方',['令牌与身份校验'],color='control')
    d.node('admin',100,650,220,90,'管理员',['配置与审计'])
    d.edge('user','app',label='提交问题 / 获取结果',at=(430,473))
    d.edge('app','model',via=[(950,495),(950,460)],label='生成请求',at=(930,445))
    d.edge('app','search',via=[(965,495),(965,645)],label='读取授权内容',at=(1120,760),kind='data')
    d.edge('app','identity','b','t',label='校验身份',at=(763,643),kind='control')
    d.edge('admin','app',via=[(430,695),(430,495)],label='管理配置',at=(430,650),kind='control')
    d.finish(['系统边界仅包围AI应用；用户、管理员、模型服务、知识源和身份提供方均在外部。','节点表示人与系统，不出现Pod、数据库表或内部微服务；箭头表示主要交互，响应可在接口语义中说明。'],['system boundary','C4 context','external systems'])


def architecture(animated=False):
    d=Diagram('animated-architecture' if animated else 'system-architecture','逻辑架构 · 请求路径' if animated else '应用逻辑架构','接入、业务、存储与横切能力 / 12 个组件','节点表示逻辑职责；同步调用、异步事件和数据读写分别编码',dark=True,animated=animated)
    d.boundary(60,260,270,295,'客户端')
    d.boundary(370,260,630,515,'应用职责边界','call')
    d.boundary(1040,260,290,420,'存储与消息','data')
    specs=[('web',80,310,'Web 客户端','发起请求'),('mobile',80,440,'移动客户端','发起请求'),('gateway',410,310,'接入网关','路由 / 限流'),('identity',410,440,'身份校验','令牌 / scope'),('order',740,310,'订单职责','校验 / 编排'),('catalog',740,440,'商品职责','查询 / 缓存'),('payment',740,570,'支付职责','授权 / 幂等'),('database',1070,310,'业务数据库','持久化订单'),('cache',1070,440,'缓存','商品热点'),('events',1070,570,'事件队列','订单事件'),('worker',740,695,'通知消费者','消费 / 去重'),('metrics',410,695,'可观测采集','日志 / 指标')]
    for identity,x,y,title,sub in specs:d.node(identity,x,y,210,70,title,[sub],color='data' if identity in ('database','cache') else 'event' if identity in ('events','worker') else 'control' if identity in ('identity','metrics') else 'call')
    d.edge('web','gateway',label='HTTPS',at=(365,332),animate=True)
    d.edge('mobile','gateway',via=[(350,475),(350,345)],animate=True)
    d.edge('gateway','order',label='同步调用',at=(675,332),animate=True)
    d.edge('gateway','identity','b','t',label='鉴权',at=(560,412),kind='control')
    d.edge('order','database',label='写入',at=(1005,330),kind='data',animate=True)
    d.edge('order','catalog','b','t',label='商品查询',at=(890,412))
    d.edge('catalog','cache',label='读缓存',at=(1005,460),kind='data')
    d.edge('order','payment','l','l',via=[(700,345),(700,605)],label='支付请求',at=(681,548))
    d.edge('order','events',via=[(1010,345),(1010,605)],label='异步发布',at=(1020,535),kind='event',animate=True)
    d.edge('events','worker','b','r',via=[(1175,730)],label='消费事件',at=(1070,754),kind='event',animate=True)
    d.edge('metrics','gateway','r','r',via=[(650,730),(650,345)],label='指标拉取',at=(648,648),kind='control')
    d.note(700,815,'示例只展示主要关系；请求返回、事务边界与其他观测连接未全部展开。',anchor='middle')
    d.finish(['共12个逻辑组件，三块边界：客户端、应用职责、存储与消息。不是六层上下排列，也不是部署图。','同步调用蓝色实线；异步发布/消费橙色虚线；读写绿色实线；鉴权/观测红色虚线。','主示例路径Web→网关→订单→数据库及订单事件→消费者；不以循环光点宣称服务实时在线，不把箭头当真实流量计。'])


def deployment():
    d=Diagram('deployment','运行位置与部署边界','公网 / 应用集群 / 托管数据服务','部署图解释运行位置、实例与网络边界，不替代逻辑架构图',dark=True)
    d.boundary(70,270,300,480,'公网访问','event');d.boundary(410,270,580,480,'私有应用集群','call');d.boundary(1030,270,300,480,'托管数据服务','data')
    specs=[('client',115,330,'访问终端','公网客户端'),('edge',110,530,'边缘入口','TLS / WAF'),('ingress',450,330,'Ingress','TLS / 路由'),('worker',740,330,'Worker Pod × 2','队列消费者'),('app',450,530,'应用 Pod × 2','业务请求'),('queue',740,530,'持久化队列','消息 / offset'),('db',1070,340,'托管数据库','私网端点'),('objects',1070,550,'对象存储','授权读写')]
    for identity,x,y,title,sub in specs:d.node(identity,x,y,210 if identity!='edge' else 220,80,title,[sub],color='data' if identity in ('db','objects') else 'event' if identity=='queue' else 'call')
    d.edge('client','edge','b','t',via=[(220,485)],label='HTTPS',at=(265,480))
    d.edge('edge','ingress',via=[(390,570),(390,370)],label='受控入口',at=(405,456))
    d.edge('ingress','app','b','t',label='路由',at=(590,484))
    d.edge('app','queue',label='发布',at=(700,550),kind='event')
    d.edge('worker','queue','b','t',label='拉取消费',at=(900,484),kind='event')
    d.edge('app','db',via=[(695,570),(695,460),(1020,460),(1020,380)],label='数据读写',at=(863,443),kind='data')
    d.edge('worker','objects',via=[(1005,370),(1005,590)],label='归档',at=(1010,684),kind='data')
    d.finish(['边界明确公网访问区、私有应用集群、托管数据服务；实例数仅标注应用/Worker各2，不暗示高可用已得到验证。','流向依次客户端→边缘→Ingress→应用；应用发布队列，Worker拉取消费并归档；应用读写数据库。','网络边界与TLS是示意，不代替完整防火墙、密钥管理或实际生产配置。'],['deployment boundary','replica annotations','private endpoints'])


def pipeline():
    d=Diagram('data-pipeline','有校验与失败出口的数据管线','输入 → Schema 校验 → 转换 → 存储 → 消费','无效输入进入隔离区；消费失败有限重试，耗尽后进入死信队列',dark=True,animated=True)
    stages=[('ingest','采集输入','来源 / 事件 ID'),('schema','Schema 校验','字段与类型'),('transform','转换规范','格式 / 单位'),('store','幂等存储','事件 ID 去重'),('consumer','下游消费','确认 / checkpoint')]
    for i,(identity,title,sub) in enumerate(stages):d.node(identity,80+i*250,400,200,100,title,[sub],start=i==0)
    d.node('quarantine',330,650,200,80,'隔离区',['原始输入与原因'],color='control',terminal=True)
    d.node('retry',820,650,200,80,'退避重试',['最多 3 次'],color='control')
    d.node('dead',1080,650,200,80,'死信队列',['保留最后错误'],color='control',terminal=True)
    for (a,_,_),(b,_,_) in zip(stages,stages[1:]):d.edge(a,b,animate=True,guard='通过' if a in ('schema','transform') else '')
    d.edge('schema','quarantine','b','t',label='校验失败',at=(486,585),kind='control',guard='schema invalid')
    d.edge('transform','quarantine','b','r',via=[(680,690)],label='转换失败',at=(705,595),kind='control',guard='transform failed')
    d.edge('consumer','retry','b','t',via=[(1180,580),(920,580)],label='消费失败',at=(1060,564),kind='control',guard='consumer failed')
    d.edge('retry','consumer','r','l',via=[(1050,690),(1050,450)],label='重试 < 3',at=(998,620),kind='control',guard='retry<3')
    d.edge('retry','dead',label='≥ 3',at=(1050,719),kind='control',guard='retry>=3')
    d.note(700,803,'幂等写入不自动等于端到端“恰好一次”；隔离与死信都需要可追溯的错误信息。',anchor='middle')
    d.finish(['五个有名称的处理节点，加隔离/退避/死信三个失败节点；每个节点有输入输出职责。','校验或转换失败进入隔离区；消费失败退避，retry<3返回消费并加1，retry>=3进入死信队列。','正常路径的虚线叠加动画只表达方向，不编码吞吐量；不要掩盖失败或承诺恰好一次。'])


def rag():
    d=Diagram('rag-pipeline','RAG：索引与查询两条路径','离线知识处理 / 在线授权检索与生成','权限过滤先于重排；证据不足应拒答，引用需要可追溯',dark=True)
    d.boundary(60,270,1280,190,'离线索引 · 保留来源与 ACL','data');d.boundary(40,525,1300,240,'在线查询 · scope 贯穿各阶段','call')
    offline=[('documents','授权文档',['source_id / ACL']),('chunks','文档切分',['chunk_id / source_id']),('embedding','文档嵌入',['同一编码器']),('vectors','向量与元数据',['vector / ID / ACL'])]
    for i,(identity,title,sub) in enumerate(offline):d.node(identity,90+i*340,330,220,90,title,sub,color='data')
    for i,(a,b) in enumerate(zip(offline,offline[1:])):d.edge(a[0],b[0],label=['保留 ACL','文本与 ID','向量与 ACL'][i],at=(370+i*340,360),kind='data')
    online=[('query','查询与权限','query + scope'),('qembed','查询嵌入','保留授权 scope'),('retrieve','过滤检索','先 ACL 后 top-k'),('rerank','证据重排','证据排序'),('generate','生成与拒答','不凭空补证据'),('answer','答案与引用','source_id 可追溯')]
    for i,(identity,title,sub) in enumerate(online):d.node(identity,60+i*220,605,175,95,title,[sub],start=i==0,terminal=i==5)
    for a,b in zip(online,online[1:]):d.edge(a[0],b[0],guard='sufficient evidence' if a[0]=='retrieve' else '')
    d.edge('retrieve','vectors','t','b',via=[(587.5,490),(1220,490)],label='带 scope 检索 / 返回已过滤候选',at=(865,480),kind='data')
    d.edge('retrieve','generate','b','b',via=[(587.5,790),(1027.5,790)],label='证据不足 → 拒答',at=(806,817),kind='control',guard='insufficient evidence')
    d.finish(['离线文档→切分→嵌入→向量元数据保留source_id、chunk_id和ACL；文档/查询使用兼容的同一编码器。','在线query与scope→查询嵌入→ACL过滤检索→重排→生成/拒答→答案与来源；授权scope不能在嵌入后丢失，不能只在生成之后做权限过滤。','证据不足走拒答分支；来源ID供引用核查，引用存在不自动保证答案正确。'])


def agent():
    d=Diagram('agent-loop','Agent 的受控执行闭环','规划、授权、人工审批、工具执行与验证','工具调用前检查权限和预算；高风险操作先审批，失败有退出路径',dark=True)
    specs=[('request',100,320,220,80,'输入目标',['目标与验收条件'],'box'),('plan',500,320,220,80,'规划下一步',['仅使用允许工具'],'box'),('policy',900,300,220,120,'可执行？',['权限 / 风险 / 预算'],'diamond'),('approval',900,510,220,80,'人工审批',['拒绝或超时即退出'],'box'),('tool',500,510,220,80,'执行工具',['step + 1 / 单次 10s'],'box'),('verify',100,490,220,120,'结果通过？',['核对验收条件'],'diamond'),('output',100,700,220,70,'交付结果',[],'pill'),('stop',900,700,220,70,'停止并报告',[],'pill')]
    for identity,x,y,w,h,title,sub,kind in specs:d.node(identity,x,y,w,h,title,sub,kind=kind,terminal=identity in ('output','stop'),start=identity=='request',color='control' if identity in ('policy','approval','stop') else 'data' if identity=='output' else 'call')
    d.edge('request','plan',label='需求与约束',at=(410,343));d.edge('plan','policy',label='拟执行动作',at=(810,343))
    d.edge('policy','approval','b','t',label='已授权但需审批',at=(1142,465),kind='control',guard='authorized and high risk and budget available')
    d.edge('policy','tool','l','r',via=[(830,360),(830,550)],label='已授权低风险',at=(792,453),guard='authorized and low risk and budget available')
    d.edge('policy','stop','r','r',via=[(1250,360),(1250,735)],label='无权或预算耗尽',at=(1197,651),kind='control',guard='unauthorized or budget exhausted')
    d.edge('approval','tool','l','r',label='批准',at=(810,531),kind='control',guard='approved')
    d.edge('approval','stop','r','t',via=[(1190,550),(1190,650),(1010,650)],label='拒绝 / 超时',at=(1100,634),kind='control',guard='denied or timeout')
    d.edge('tool','verify','l','r',label='结果或异常',at=(410,532))
    d.edge('verify','output','b','t',label='通过',at=(258,664),kind='data',guard='valid result')
    d.edge('verify','plan','t','b',via=[(210,445),(610,445)],label='未通过且还有预算',at=(420,433),kind='control',guard='invalid and budget available')
    d.edge('verify','stop','l','b',via=[(60,550),(60,803),(1010,803)],label='未通过且预算耗尽',at=(690,789),kind='control',guard='invalid and budget exhausted')
    d.note(700,280,'执行预算：最多 5 次工具调用 / 总计 60 秒；每次调用前重新检查。',anchor='middle')
    d.finish(['每次工具调用前重新检查授权、风险与预算；最多5次调用、单次10秒、总计60秒。无权或预算耗尽优先停止；已授权高风险须人工审批；已授权低风险直接调用。','审批批准进入工具，拒绝或超时退出；工具调用记录step+1，异常也要进入验证/失败处理。','验证通过交付；未通过且还有预算回规划，预算耗尽停止报告；不把无限循环当Agent能力，不在图中省略人工审批。'])


def er():
    d=Diagram('entity-relationship','会话数据实体关系','用户 / 会话 / 消息 / 附件；显式 PK、FK 与基数','关系线表示数据关联而非调用；父对象可暂时没有子对象')
    d.node('users',100,300,290,190,'User',['PK id','email','created_at'],kind='entity',start=True)
    d.node('sessions',700,300,290,190,'Conversation',['PK id','FK user_id → User.id','title / created_at'],kind='entity')
    d.node('messages',700,590,290,190,'Message',['PK id','FK conversation_id','role / content / created_at'],kind='entity')
    d.node('attachments',100,590,290,190,'Attachment',['PK id','FK message_id → Message.id','uri / media_type'],kind='entity')
    d.edge('users','sessions',label='1  ——  0..N',at=(545,382),kind='neutral',arrow=False,guard='User 1 : Conversation 0..N')
    d.edge('sessions','messages','b','t',label='1  ——  0..N',at=(962,547),kind='neutral',arrow=False,guard='Conversation 1 : Message 0..N')
    d.edge('messages','attachments','l','r',label='1  ——  0..N',at=(545,669),kind='neutral',arrow=False,guard='Message 1 : Attachment 0..N')
    d.note(1150,365,'PK · 主键',18);d.note(1150,410,'FK · 外键',18);d.note(1150,455,'0..N · 零或多个',18)
    d.finish(['四实体，User.id→Conversation.user_id，Conversation.id→Message.conversation_id，Message.id→Attachment.message_id。','每个子实体只属于一个父实体，外键非空；每个父实体允许0到多个子实体。连线只表示关联，不是服务调用箭头。','表中PK/FK与关系基数对应，不把URI字段宣称为真实文件存储实现。'],['PK/FK','cardinality','entity tables'])


def dependency(animated=False):
    d=Diagram('network-pulse' if animated else 'service-dependencies','服务依赖 · 动态路径' if animated else '有方向的服务依赖','箭头从调用方指向依赖方；依赖方向与故障传播方向相反','检索和生成各有下游依赖；故障影响沿依赖关系反向分析',dark=True,animated=animated)
    specs=[('web',100,430,'Web','入口'),('api',400,430,'API','编排'),('retrieve',730,300,'检索服务','授权候选'),('generate',730,590,'生成服务','模型请求'),('vector',1100,300,'向量存储','索引与元数据'),('model',1100,590,'模型接口','生成输出'),('cache',730,450,'缓存','热点结果')]
    for identity,x,y,title,sub in specs:d.node(identity,x,y,190,80,title,[sub],start=identity=='web',color='data' if identity in ('vector','cache') else 'call')
    d.edge('web','api',animate=True,label='调用',at=(345,451))
    d.edge('api','retrieve',via=[(660,470),(660,340)],animate=True,label='检索',at=(692,324))
    d.edge('api','generate',via=[(640,470),(640,630)],animate=True,label='生成',at=(690,613))
    d.edge('api','cache',via=[(690,470),(690,490)],label='读缓存',at=(685,524),kind='data')
    d.edge('retrieve','vector',label='查询',at=(1005,322),kind='data',animate=True)
    d.edge('generate','model',label='生成调用',at=(1007,612),animate=True)
    d.note(700,789,'节点尺寸相同，不编码重要性；动态图只高亮示例路径，不宣称实时健康状态。',anchor='middle')
    d.finish(['七个有名称的节点；Web依赖API，API依赖检索/生成/缓存，检索依赖向量存储，生成依赖模型接口。','箭头从调用者指向被调用者，图是有向无环依赖；模型故障的影响需反向沿生成→API→Web分析。','节点等大、连线等宽，不暗示未定义的中心性、流量或力导向算法。'])


def org():
    d=Diagram('org-chart','组织与汇报层级','负责人 → 四个部门 → 成员；虚构组织','实线表示正式汇报层级；跨部门协作不应伪装成第二条汇报线')
    d.node('lead',570,290,220,80,'组织负责人',['职责与决策'],start=True)
    depts=[('product','产品'),('design','设计'),('engineering','研发'),('growth','增长')]
    for i,(identity,title) in enumerate(depts):
        x=100+i*300;d.node(identity,x,470,220,70,title+'部门',['部门负责人'])
        d.edge('lead',identity,'b','t',via=[(680,420),(x+110,420)],arrow=False)
        for j in range(2):
            member=identity+f'-{j+1}';xx=x+j*125;d.node(member,xx,650,95,70,'成员 '+str(j+1),['岗位'],color='neutral',terminal=True)
            d.edge(identity,member,'b','t',via=[(x+110,590),(xx+47.5,590)],arrow=False)
    d.edge('product','engineering','b','b',via=[(210,565),(810,565)],label='跨部门协作 · 非汇报关系',at=(510,555),kind='neutral',arrow=False,guard='collaboration')
    d.finish(['虚构组织，负责人、产品/设计/研发/增长四部门、每部门两成员，共13节点。','正式层级连线用实线无箭头，成员只设一个正式父节点；协作用灰色虚线单独标出，不能误读为双重汇报。'],['hierarchy','collaboration relation'])


def mindmap():
    d=Diagram('mind-map','SVG 知识层级图','中心主题 → 六个分支 → 十二个叶子','分支表示知识归类而非执行顺序；主干与叶子清晰分层')
    d.node('svg',600,490,200,90,'SVG',['文本描述图形'],start=True)
    branches=[('shapes','图形',['形状','路径'],True,320),('animation','动画',['CSS','SMIL'],True,500),('interaction','交互',['事件','悬停'],True,680),('data','数据',['图表','地图'],False,320),('ecosystem','生态',['工具','规范'],False,500),('ai','AI 工作流',['生成','验证'],False,680)]
    for identity,title,leaves,left,y in branches:
        x=290 if left else 930;d.node(identity,x,y,200,70,title)
        lane=540 if left else 860;side='l' if left else 'r';target='r' if left else 'l';d.edge('svg',identity,side,target,via=[(lane,535),(lane,y+35)],arrow=False)
        for j,label in enumerate(leaves):
            leaf=identity+f'-{j}';lx=40 if left else 1210;ly=y-20 if j==0 else y+55;d.node(leaf,lx,ly,140,40,label,color='neutral',terminal=True)
            route=240 if left else 1170;d.edge(identity,leaf,'l' if left else 'r','r' if left else 'l',via=[(route,y+35),(route,ly+20)],arrow=False)
    d.finish(['中心SVG；图形/动画/交互/数据/生态/AI工作流六分支，每分支两叶子，共19节点。','连线无箭头，粗细不编码统计量；四列支撑左右展开，父子层级明确，不把知识层级画成时间顺序。'],['hierarchy','orthogonal mind map'])


def venn():
    d=Diagram('venn-diagram','权限、相关性与安全的交集','概念集合 / 不表示人数或占比','可交付候选 = 已授权 ∩ 相关 ∩ 满足安全条件')
    d.boundary(120,255,1150,550,'候选结果全集')
    circles=[(530,450,'#3686d9'),(800,450,'#9268cf'),(665,620,'#00a887')]
    for cx,cy,col in circles:d.layers.append(f'<circle cx="{cx}" cy="{cy}" r="180" fill="{col}" fill-opacity="0.23" stroke="{col}" stroke-width="2"/>')
    labels=[(470,425,'仅已授权'),(860,425,'仅相关'),(665,742,'仅满足安全条件'),(665,356,'授权且相关'),(525,598,'授权且安全'),(805,598,'相关且安全'),(665,528,'三者交集'),(1090,750,'三条件均不满足')]
    for x,y,label in labels:d.note(x,y,label,18,anchor='middle')
    d.finish(['三个集合P=有权限、R=与查询相关、S=满足安全条件；七个内部区域与外部区域分别标注，中央P∩R∩S为可交付候选。','三个等半径圆只是概念集合示意，不以面积编码数值；不能把三交集定义为“全能T型人”。','圆心(530,450)、(800,450)、(665,620)，半径180；区域标签必须位于对应布尔集合中。'],['set intersection','Boolean regions'])


EVENTS=[('2001-09-04','SVG 1.0 推荐','Recommendation','https://www.w3.org/TR/2001/REC-SVG-20010904/'),('2003-01-14','SVG 1.1 推荐','Recommendation','https://www.w3.org/TR/2003/REC-SVG11-20030114/'),('2008-12-22','SVG Tiny 1.2 推荐','Recommendation','https://www.w3.org/TR/2008/REC-SVGTiny12-20081222/'),('2011-08-16','SVG 1.1 第二版','Recommendation','https://www.w3.org/TR/2011/REC-SVG11-20110816/'),('2016-09-15','SVG 2 候选推荐','Candidate Recommendation','https://www.w3.org/TR/2016/CR-SVG2-20160915/'),('2018-10-04','SVG 2 候选推荐更新','Candidate Recommendation','https://www.w3.org/TR/2018/CR-SVG2-20181004/')]


def timeline(animated=False):
    d=Diagram('timeline-reveal' if animated else 'timeline-svg','标准里程碑 · 动态强调' if animated else 'SVG 标准里程碑','W3C 文档 / 2001–2018；候选推荐不等于正式推荐','按事件顺序等距排列，不编码实际时间间隔；首帧信息完整',animated=animated,footer='来源：W3C 对应版本文档 · 推荐状态不代表浏览器全面支持')
    for i,(when,title,status,url) in enumerate(EVENTS):
        y=310+i*80;identity='event-'+str(i);d.node(identity,691,y-9,18,18,'',kind='event',color='call',start=i==0,terminal=i==5)
        x=160 if i%2==0 else 815
        d.note(x,y-9,when[:4],27,COLOR['call']);d.note(x,y+22,title,20);d.note(x,y+49,when+' · '+status,15,d.muted)
        d.layers.append(f'<line x1="700" y1="{y}" x2="{630 if i%2==0 else 770}" y2="{y}" stroke="{d.grid}"/>')
        if animated:d.notes.append(f'<circle class="event-focus" cx="700" cy="{y}" r="12" fill="none" stroke="{COLOR["call"]}" style="animation-delay:{i}s"/>')
        if i:d.edge('event-'+str(i-1),identity,'b','t',arrow=False,kind='neutral')
    d.finish(['六事件以对应W3C版本文档为来源：']+[when+' '+title+'；'+url for when,title,status,url in EVENTS]+['只展示2001–2018的选定里程碑，不能写成1996–2026完整历史；Candidate Recommendation不等于Recommendation。','节点顺序等距排版；首帧所有日期和事件可见，动态版仅逐个强调外圈。'],['chronological events','W3C document status'])


def build():
    BUILT.clear()
    process();process(True);decision();swimlane();sequence();state_machine();context();architecture();architecture(True);deployment();pipeline();rag();agent();er();dependency();dependency(True);org();mindmap();venn();timeline();timeline(True)
    for index,slug in enumerate(BUILT,1):
        p=OUT/slug/'meta.json';m=json.loads(p.read_text());m['order']=index;p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(BUILT)} diagrams with explicit relationship semantics.')


if __name__=='__main__':build()
