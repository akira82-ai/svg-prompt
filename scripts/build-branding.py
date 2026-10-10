#!/usr/bin/env python3
"""Generate brand systems and editorial layouts from shared geometric assets."""
from pathlib import Path
from html import escape
import json,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'gallery/branding';BUILT=[]
TECH={'name':'NOVA','bg':'#eef2f6','paper':'#ffffff','ink':'#14263d','muted':'#596b80','accent':'#245ee8','soft':'#dce7fc'}
EDIT={'name':'FIELD','bg':'#ece9e2','paper':'#faf8f1','ink':'#272b29','muted':'#656862','accent':'#b23c32','soft':'#e9d9ce'}
LIFE={'name':'LOAM','bg':'#ebe5da','paper':'#faf5e9','ink':'#343b2d','muted':'#626852','accent':'#94583b','soft':'#e4d6bd'}
ENTRIES=[
('logo-grid','Logo 构形与网格','Logo Construction Grid','tech'),('wordmark','几何字标','Geometric Wordmark','tech'),('brand-lockup','品牌组合标识','Brand Lockups','tech'),('brand-palette','品牌色彩系统','Brand Color System','tech'),('brand-guidelines','品牌使用规范','Brand Guidelines','tech'),
('type-scale','字阶与阅读层级','Type Scale and Hierarchy','edit'),('bilingual-type','中英文字体搭配','Bilingual Typography','edit'),('editorial-grid','编辑网格与版式','Editorial Grid Systems','edit'),('type-effects','品牌文字表达','Expressive Typography','tech'),('text-on-path','文字沿路径排布','Type on a Path','life'),
('magazine-cover','杂志式封面','Magazine Cover','edit'),('report-cover','技术报告封面','Technical Report Cover','tech'),('product-launch','产品发布海报','Product Launch Poster','tech'),('article-header','文章头图与裁切','Article Header and Cropping','edit'),('presentation-title','演讲标题页','Presentation Title Slide','tech'),('poster','编辑式品牌海报','Editorial Brand Poster','edit'),('comparison-vs','对比信息版式','Comparison Layout','edit'),('stat-numbers','图鉴统计卡','Gallery Statistics','tech'),
('business-card','名片正反面','Business Card Front and Back','tech'),('social-kit','社媒品牌套件','Social Brand Kit','tech'),('packaging-dieline','包装结构与品牌应用','Packaging Structure and Branding','life'),('circular-badge','品牌圆形徽章','Circular Brand Badge','life'),
('typewriter','品牌文案揭示','Brand Copy Reveal','tech'),('brand-intro','品牌动效片头','Brand Intro Animation','tech')]
REMOVED=['letter-morph','word-morph','neon-sign','glitch-text'];ANIMATED={'typewriter','brand-intro'}
MARK='M0 0 L2 0 L6 4 L6 6 L4 6 L0 2 Z M4 0 L6 0 L6 2 Z M0 4 L0 6 L2 6 Z'
GLYPHS={
'N':'M0 0 H12 L42 38 V0 H54 V60 H42 L12 22 V60 H0 Z',
'O':'M12 0 H44 L56 12 V48 L44 60 H12 L0 48 V12 Z M17 12 L12 17 V43 L17 48 H39 L44 43 V17 L39 12 Z',
'V':'M0 0 H14 L30 43 L46 0 H60 L38 60 H22 Z',
'A':'M0 60 L22 0 H38 L60 60 H45 L40 45 H20 L15 60 Z M26 30 H34 L30 17 Z'}
class Brand:
    def __init__(self,slug,title,en,theme):
        self.slug,self.title,self.en=slug,title,en;self.theme=theme;self.t={'tech':TECH,'edit':EDIT,'life':LIFE}[theme];self.parts=[];self.labels=[];self.notes=[];self.animated=slug in ANIMATED
        self.rect(0,0,1400,900,self.t['bg']);self.text(64,48,'SVG / BRAND & TYPE',14,self.t['muted']);self.text(1336,48,self.t['name']+' / CONCEPT BRAND',14,self.t['muted'],anchor='end');self.line(64, 70,1336,70)
        self.text(64,118,title,32,weight=700);self.text(64,153,en,18,self.t['muted']);self.line(64,846,1336,846);self.text(64,878,'示例品牌与版式 · 字体依赖系统环境 · 印刷图仅为示意',14,self.t['muted']);self.text(1336,878,'SVG-PROMPT',14,self.t['muted'],anchor='end')
        glyphs='';offset=0
        for letter,width in [('N',54),('O',56),('V',60),('A',60)]:glyphs+=f'<path d="{GLYPHS[letter]}" transform="translate({offset} 0)" fill-rule="evenodd"/>';offset+=width+12
        self.add(f'<defs><symbol id="nova-mark" viewBox="0 0 6 6"><path d="{MARK}"/></symbol><symbol id="nova-wordmark" viewBox="0 0 266 60">{glyphs}</symbol></defs>')
    def add(self,s):self.parts.append(s)
    def req(self,s):self.notes.append(s)
    def text(self,x,y,s,size=18,col=None,anchor='start',weight=400,font=None,attrs=''):
        self.labels.append(str(s));self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{col or self.t["ink"]}" text-anchor="{anchor}" font-weight="{weight}" '+(f'font-family="{font}" ' if font else '')+f'{attrs}>{escape(str(s))}</text>')
    def lines(self,x,y,ss,size=18,col=None,step=34,**kw):
        for i,s in enumerate(ss):self.text(x,y+i*step,s,size,col,**kw)
    def rect(self,x,y,w,h,col=None,rx=0,attrs=''):self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{col or self.t["paper"]}" rx="{rx}" {attrs}/>')
    def line(self,x,y,xx,yy,col=None,width=1,attrs=''):self.add(f'<line x1="{x:.3f}" y1="{y:.3f}" x2="{xx:.3f}" y2="{yy:.3f}" stroke="{col or self.t["muted"]}" stroke-width="{width}" {attrs}/>')
    def circle(self,x,y,r,col=None,attrs=''):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col or self.t["accent"]}" {attrs}/>')
    def path(self,d,col=None,stroke=None,width=1,attrs=''):self.add(f'<path d="{d}" fill="{col or "none"}" stroke="{stroke or "none"}" stroke-width="{width}" {attrs}/>')
    def mark(self,x,y,size,col=None,attrs=''):self.add(f'<use href="#nova-mark" x="{x}" y="{y}" width="{size}" height="{size}" fill="{col or self.t["accent"]}" data-mark-size="{size}" {attrs}/>')
    def word(self,x,y,h,col=None,attrs=''):self.add(f'<use href="#nova-wordmark" x="{x}" y="{y}" width="{h*266/60:.4f}" height="{h}" fill="{col or self.t["ink"]}" data-word-height="{h}" {attrs}/>')
    def life(self,x,y,size,col=None):
        col=col or self.t['accent'];self.circle(x+size/2,y+size/2,size/2,'none',attrs=f'stroke="{col}" stroke-width="2"');self.line(x+size*.18,y+size*.62,x+size*.82,y+size*.62,col,2);self.circle(x+size*.5,y+size*.38,size*.12,col)
    def finish(self):
        if self.animated:self.add('<style>.fallback{display:none}@media(prefers-reduced-motion:reduce){.motion{display:none}.fallback{display:inline}}</style>')
        finding=self.notes[0];svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" font-family="PingFang SC, Microsoft YaHei, sans-serif" role="img" aria-labelledby="title desc"><title id="title">{escape(self.title)}</title><desc id="desc">{escape(finding)}</desc>'+''.join(self.parts)+'</svg>\n'
        p=OUT/self.slug;p.mkdir(exist_ok=True);(p/'index.svg').write_text(svg);m=json.loads((p/'meta.json').read_text()) if (p/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
        m.update(slug=self.slug,title=self.title,space='2d',time='smil' if self.animated else 'static',order=len(BUILT)+1,description=finding,tech=['brand system','SVG typography','SMIL reveal' if self.animated else 'editorial layout']);(p/'meta.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
        lines=[f'用 SVG 制作“{self.title} / {self.en}”，采用{self.t["name"]}示例品牌。',f'- 画布1400×900；背景{self.t["bg"]}、纸面{self.t["paper"]}、正文{self.t["ink"]}、辅助文字{self.t["muted"]}、强调色{self.t["accent"]}；顶部中英文标题，作品区域x64..1336、y200..820，页脚说明示例与印刷边界。']+['- '+s for s in self.notes]+['- NOVA共用标准矢量标识：6×6单位视图，路径 '+MARK+'；字标N/O/V/A共用固定矢量轮廓，宽高266:60；不依赖字体重建字标。','- 其他标题采用系统无衬线或Georgia衬线回退；中英文字体由环境决定，不声称嵌入商业字体。','- 文字和样例值：'+json.dumps(list(dict.fromkeys(self.labels)),ensure_ascii=False)+'。']
        if self.animated:lines+=['- SMIL只播放一次，终帧稳定；减少动效隐藏motion并显示完整fallback，不能让品牌名或完整文案永久缺失。']
        (p/'prompt.md').write_text(f'# {self.title} / {self.en}\n\n分类：[品牌与排版](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+'\n'.join(lines)+'\n```\n');BUILT.append(self.slug)

def identity(f):
    s=f.slug
    if s=='logo-grid':
        f.rect(90,220,740,580);u= 60;x,y=275,330
        for i in range(-1,8):f.line(x+i*u,y-u,x+i*u,y+7*u,'#cbd6e7');f.line(x-u,y+i*u,x+7*u,y+i*u,'#cbd6e7')
        f.mark(x,y,6*u);f.rect(x-u,y-u,8*u,8*u,'none',attrs=f'stroke="{f.t["accent"]}" stroke-dasharray="6 6" data-clearance="{u}"');f.text(x+3*u,787,'6u × 6u 标识 / 四边留白 1u',17,anchor='middle')
        f.text(900,270,'CONSTRUCTION / 01',16,f.t['muted']);f.lines(900,355,['整数网格上的共同轮廓','斜边斜率为 1','三块形状共享网格边界','辅助线由几何关系产生'],23,step=60);f.lines(900,670,['u = 标识高度 / 6','网格用于构形，不代表审美证明。'],17,f.t['muted'],step= 40);f.req('标识6u×6u，所有顶点在整数网格上；四周安全留白1u，虚线框8u×8u，几何辅助线与真实轮廓对应。')
    elif s=='wordmark':
        for y,dark in [(235,False),(530,True)]:
            f.rect(90,y,1220,260,f.t['ink'] if dark else f.t['paper']);f.word(260,y+90,80,'#fff' if dark else f.t['ink']);f.text(1110,y+60,'REVERSED' if dark else 'PRIMARY',14,'#d5dfed' if dark else f.t['muted'],anchor='end')
        f.req('NOVA字标N/O/V/A采用固定矢量轮廓，深色与反白轮廓完全一致，宽高266:60；内孔使用evenodd。')
    elif s=='brand-lockup':
        f.rect(90,235,1220,555);f.mark(150,330, 90);f.word(270,345,60);f.text(150,490,'横版 / 图标高 1.5h / 间隔 0.5h',17,f.t['muted']);f.mark(905,310,90);f.word(817,430,60);f.text(855,560,'竖版 / 居中组合',17,f.t['muted']);f.mark(150,625, 60,f.t['ink']);f.word(235,640,30,f.t['ink']);f.rect(750,610,490,125,f.t['ink']);f.mark(780,640, 60,'#fff');f.word(865,655,30,'#fff');f.req('横版图标90px、字标60px、间隔30px；竖版图标与字标共同中心；小尺寸单色和反白版本保留共同轮廓。')
    elif s=='brand-palette':
        colors=[('PRIMARY','#245ee8','品牌主色'),('INK','#14263d','正文与深底'),('PAPER','#ffffff','纸面'),('MIST','#dce7fc','浅色层级')]
        for i,(name,col,role) in enumerate(colors):
            x=90+i*310;f.rect(x,235,290,310,col,attrs='stroke="#cbd6e7"');f.text(x,595,name,21,weight=700);f.text(x,638,col.upper(),19);f.text(x,685,role,17,f.t['muted'])
        f.text(90,775,'颜色承担品牌与层级；功能性成功、错误、告警另按产品语义定义。',18,f.t['muted']);f.req('4品牌色主色245ee8/正文14263d/纸面ffffff/浅层dce7fc，HEX文本与色块一致；不把品牌色板当完整功能语义色。')
    elif s=='brand-guidelines':
        f.rect(90,225,1220,580);f.text(130,270,'01 / CLEAR SPACE',16,f.t['muted']);f.mark(210,355,180);f.rect(180,325,240,240,'none',attrs=f'stroke="{f.t["accent"]}" stroke-dasharray="6 6" data-clearance="30"');f.text(180,615,'1u 留白 / u = H÷6',18)
        f.text(530,270,'02 / SMALL SIZE',16,f.t['muted']);f.mark(570,380,72);f.mark(720,425,24);f.text(570,535,'72px',17);f.text(700,535,'24px',17);f.lines(530,615,['24px 为此示例的预设值。','实际最小尺寸需载体测试。'],16,f.t['muted'])
        f.text(925,270,'03 / MISUSE',16,f.t['muted']);f.add('<g transform="translate(940 335) scale(1.5 1)">');f.mark(0,0,90);f.add('</g>');f.line(930,325,1085,440,'#b23c32',3);f.text(925,485,'不要单向拉伸',18);f.mark(950,555,90,'#a06a3e');f.line(930,540,1065,660,'#b23c32',3);f.text(925,710,'不要任意换色',18);f.req('安全距离与构形同规则H/6，标准与错误轮廓可对照；24px仅为示例预设，不声称经可读性实测认证。')
    else:return False
    return True

def typography(f):
    s=f.slug
    if s=='type-scale':
        f.rect(90,225,1220,580);levels=[('DISPLAY',56,64,'把重要的事，放在第一眼。'),('HEADING',36,46,'排版决定阅读顺序'),('SUBHEADING',24,34,'层级来自字号、字重与留白'),('BODY',18,29,'正文保持适度行长，让读者顺着内容向下阅读。'),('CAPTION',14,22,'辅助信息服务理解，不与主标题争夺注意力。')]
        for y,(role,size,leading,text) in zip([325,450,560,655,735],levels):f.text(130,y,role,14,f.t['muted']);f.text(400,y,text,size,weight=700 if role in ('DISPLAY','HEADING') else 400,attrs=f'data-type-size="{size}" data-leading="{leading}"');f.text(1280,y,f'{size}/{leading}',14,f.t['muted'],anchor='end')
        f.req('五阶字号/行高56/64、36/46、24/34、18/29、14/22；行高明确为版式规范，单行SVG文本不声称自动布局。')
    elif s=='bilingual-type':
        f.rect(90,225,1220,580);f.text(130,275,'FIELD / 见地',19,weight=700);f.lines(130,405,['设计的秩序','与阅读的节奏'],58,weight=700,step=85);f.lines(770,415,['The order of design.','The rhythm of reading.'],36,font='Georgia, serif',step=58)
        f.line(130,610,1270,610);f.lines(130,665,['中文正文重视字面密度与行距。','英文衬线标题提供编辑感，正文仍保持清楚。'],19,step=36);f.text(770,665,'2026 / Issue 08 / 128 pages',24,font='Georgia, serif');f.text(770,725,'中英不强求字号相同，而应比较实际字面。',16,f.t['muted']);f.req('中文58px粗体搭配英文Georgia36px；数字独立示例。采用系统字体回退，混排字面和基线需实测，不将字号相等当视觉等大。')
    elif s=='editorial-grid':
        widths=[340,400,400];starts=[90,470,910]
        for i,(x,w) in enumerate(zip(starts,widths)):
            f.rect(x,225,w,575);f.text(x+24,268,['单栏 / ONE','双栏 / TWO','非对称 / ASYMMETRIC'][i],16,f.t['muted']);f.text(x+24,350,'阅读的顺序',30,weight=700)
            if i==0:
                f.lines(x+24,425,['先明确一个主信息。','再安排解释与证据。','最后给出下一步。'],21,step=53);f.rect(x+24,610,w-48,100,f.t['soft'])
            elif i==1:
                for j in range(2):
                    xx=x+24+j*184;f.rect(xx,405,160,130,f.t['soft']);f.lines(xx,585,['主信息' if j==0 else '解释内容','统一边界','独立留白'],19,step=45)
            else:
                f.rect(x+24,405,220,200,f.t['soft']);f.lines(x+266,440,['侧注','来源','日期'],18,step=52);f.lines(x+24,665,['主栏承载叙述。','窄栏承载补充。'],19)
            f.rect(x+24,295,w-48,440,'none',attrs=f'stroke="{f.t["accent"]}" stroke-dasharray="4 6" data-layout="{i}"');f.text(x+24,765,'相同主题 / 不同阅读路径',14,f.t['muted'])
        f.req('相同主题主信息/解释/下一步以单栏、双栏、非对称主侧栏组织；虚线显示内容边界，列间留白不小于24px。')
    elif s=='type-effects':
        for i,(x,y) in enumerate([(90,230),(730,230),(90,525),(730,525)]):
            dark=i==3;f.rect(x,y,580,255,f.t['ink'] if dark else f.t['paper']);f.text(x+28,y+40,['实心 / SOLID','描边 / OUTLINE','反白 / REVERSED','轻度光晕 / GLOW'][i],15,'#d5dfed' if dark else f.t['muted'])
            if i==0:f.word(x+70,y+95,95)
            elif i==1:f.word(x+70,y+95,95,'none',attrs=f'stroke="{f.t["ink"]}" stroke-width=".7"')
            elif i==2:f.rect(x+30,y+65,520,145,f.t['accent']);f.word(x+70,y+95,95,'#fff')
            else:
                f.add('<defs><filter id="type-glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="5"/></filter></defs>');f.word(x+70,y+95,95,'#87b7ff',attrs='filter="url(#type-glow)" opacity=".6"');f.word(x+70,y+95,95,'#fff')
        f.req('四种处理共用NOVA矢量轮廓；描边不填色，反白是真实白色字标，光晕叠加清晰前景，不让模糊成为文字主体。')
    elif s=='text-on-path':
        f.rect(90,225,1220,580);f.add('<defs><path id="loam-arc" d="M220 520 A220 220 0 0 1 660 520"/><path id="loam-wave" d="M790 490 C920 360 1070 620 1240 490"/></defs>')
        f.add(f'<text font-size="28" fill="{f.t["ink"]}" letter-spacing="2"><textPath href="#loam-arc" startOffset="50%" text-anchor="middle">LOAM / EARTH &amp; EVERYDAY</textPath></text>');f.life(365,450,150);f.text(440,710,'弧线建立标识外缘',20,anchor='middle')
        f.add(f'<text font-size="25" fill="{f.t["accent"]}"><textPath href="#loam-wave" startOffset="50%" text-anchor="middle">Find your everyday rhythm.</textPath></text>');f.text(1010,710,'曲线改变节奏，正文保持直排',20,anchor='middle');f.req('圆弧与缓曲线两种textPath，使用href本地路径、50%居中；不旋转品牌文字，保证静态阅读。')
    else:return False
    return True

def editorial(f):
    s=f.slug
    if s=='magazine-cover':
        x,y,w,h=150,230,440,550;f.rect(x,y,w,h);f.text(x+28,y+65,'FIELD',60,font='Georgia, serif',weight=700);f.text(x+28,y+101,'见地 / DESIGN & CULTURE',14);f.line(x+28,y+125,x+w-28,y+125);f.text(x+28,y+159,'08 / OCTOBER 2026',14,f.t['accent'])
        f.circle(x+280,y+315,125,f.t['soft']);f.rect(x+270,y+230,110,210,f.t['accent']);f.lines(x+28,y+265,['秩序，','也有温度。'],44,weight=700,step=65);f.lines(x+28,y+465,['设计系统如何形成自己的性格','字体 · 材料 · 阅读'],16,step=33)
        f.lines(720,300,['EDITORIAL / 08','一个主标题','一个主视觉','三层信息'],25,step=70);f.lines(720,665,['期号与日期放在稳定位置。','导读辅助封面，而不争夺主视觉。','图形与文字是独立、可调整的层。'],18,f.t['muted'],step=40);f.req('4:5杂志封面440×550，FIELD刊头、08期/2026年10月、主标题秩序也有温度和两条导读；图形背景与主标题阅读层级分离。')
    elif s=='report-cover':
        x,y,w,h=170,230,390,552;f.rect(x,y,w,h);f.mark(x+28,y+28,36);f.text(x+80,y+54,'NOVA RESEARCH',15,weight=700);f.text(x+28,y+140,'TECHNICAL REPORT',14,f.t['accent']);f.lines(x+28,y+215,['系统的边界','与协作效率'],36,weight=700,step=58)
        for i in range(7):f.line(x+28,y+390+i*14,x+w-28,y+330+i*14,'#afc4ee',1)
        f.lines(x+28,y+468,['研究报告 / 示例内容','Version 1.0 · 2026-10-10'],14,step=28);f.lines(720,315,['TECHNICAL / REPORT','题名 → 类型 → 版本','机构 → 日期 → 状态'],26,step=75);f.lines(720,665,['A 系列纸张比例近似 1:√2。','技术图形服务主题，不代替研究结论。','此示例不暗示真实机构发布。'],18,f.t['muted'],step=40);f.req('报告封面390×552近似A4比例，题名系统的边界与协作效率；机构NOVA RESEARCH为虚构，版本1.0与日期明确。')
    elif s=='product-launch':
        f.rect(90,225,1220,580,f.t['ink']);f.text(140,290,'NOVA / RELEASE 02',16,'#b8cff6');f.lines(140,420,['复杂工作，','清楚推进。'],64,'#fff',weight=700,step=90);f.text(140,650,'从资料到结果，保留每一步的来由。',23,'#d5dfed');f.rect(140,710,250,52,'#fff',4);f.text(265,744,'了解 NOVA 2.0',17,f.t['ink'],anchor='middle',weight=600)
        f.mark(920,355,250,'#80aaff');f.line(880,650,1240,650,'#91b4ed');f.text(1240,732,'MAKE WORK TRACEABLE',14,'#d5dfed',anchor='end');f.req('横向发布海报突出一个主信息复杂工作清楚推进、NOVA2.0版本和了解入口；虚构产品，不编造发布日期或性能指标。')
    elif s=='article-header':
        f.text(90,225,'16:9 / 原始横向画面',16,f.t['muted']);f.rect(90,250,780,438.75);f.text(125,305,'FIELD / 见地',18,weight=700);f.lines(125,425,['让信息，','有自己的顺序。'],48,weight=700,step=74);f.text(125,640,'编辑设计 / 2026 年 10 月',16,f.t['muted']);f.circle(740,440,105,f.t['soft']);f.rect(640,420,90,160,f.t['accent']);f.rect(120,330,500,280,'none',attrs=f'stroke="{f.t["accent"]}" stroke-dasharray="5 5"')
        f.text(950,280,'裁切安全区',24,weight=600);f.lines(950,355,['文字放在稳定区域。','右侧图形允许裁切。','缩略图重新检查字重。'],20,f.t['muted'],step=50);f.rect(940,570,330,186);f.text(960,625,'让信息，',32,weight=700);f.text(960,675,'有自己的顺序。',27,weight=700);f.text(940,796,'缩略图重排示意 / 不声称自动裁切',14,f.t['muted']);f.req('原画780×438.75为16:9；标题安全区x120..620/y330..610，副图在右可裁切；右下为缩略重排而非同画面自动裁切。')
    elif s=='presentation-title':
        f.rect(90,235,1220,548,f.t['ink']);f.mark(140,285,50,'#fff');f.text(215,317,'NOVA / DESIGN SESSION',17,'#d5dfed');f.lines(140,455,['让复杂系统','被清楚理解'],64,'#fff',weight=700,step=90);f.line(140,625,600,625,'#718aa8');f.text(140,690,'林老师 / 示例讲者',22,'#fff');f.text(140,737,'设计方法分享 · 2026-10-10',17,'#d5dfed')
        for i in range(8):f.line(1000+i*26,380,810+i*26,660,'#638ed6',2)
        f.req('演讲标题页采用横向屏幕布局，主题、讲者、活动日期三个层级；右侧线性图形不干扰标题，不冒充真实活动。')
    elif s=='poster':
        f.rect(130,220,400,566);f.text(160,273,'FIELD / 08',15,f.t['accent']);f.lines(160,395,['看见','秩序'],90,weight=700,step=130);f.line(160,585,500,585,f.t['accent'],5);f.text(160,655,'ORDER / IN VIEW',20,font='Georgia, serif');f.lines(160,714,['字体、留白与阅读路径','编辑设计系列 / 示例海报'],15,step=30)
        f.lines(710,320,['EDITORIAL POSTER','主标题支配画面','说明退居第二层','信息锚点稳定'],26,step=70);f.lines(710,650,['400×566 近似 A 系列比例。','大字、细线、小字形成节奏。','不用装饰图形填满所有空白。'],19,f.t['muted'],step=44);f.req('竖版400×566近似A3比例，主标题看见秩序、英文副标题ORDER IN VIEW、编辑设计系列说明；排版用留白与字重建立层级。')
    elif s=='comparison-vs':
        f.rect(90,230,1220,560);f.text(350,290,'SVG / 矢量',28,anchor='middle',weight=700);f.text(1060,290,'PNG / 位图',28,anchor='middle',weight=700)
        rows=[('缩放','矢量形状可重新绘制','受原始像素尺寸限制'),('体积','取决于结构与复杂度','取决于像素、内容与压缩'),('编辑','可修改图形、文字与属性','主要修改像素内容'),('动效','可用SMIL或CSS，支持依环境','PNG通常静态，APNG支持动画'),('文字','提取能力取决于嵌入方式','可使用alt，或依赖OCR')]
        for i,(label,a,b) in enumerate(rows):y=365+i*79;f.line(125,y+40,1275,y+40,'#d1cfc7');f.text(700,y,label,15,f.t['accent'],anchor='middle',weight=600);f.text(140,y,a,17);f.text(805,y,b,17)
        f.req('五维比较保留条件，不绝对宣称矢量文件更小或图片无法动画；PNG/APNG与文字提取方式区别清楚。')
    elif s=='stat-numbers':
        records={str(p.parent.relative_to(ROOT/'gallery')):json.loads(p.read_text()) for p in (ROOT/'gallery').glob('*/*/meta.json')}
        for slug in REMOVED:records.pop('branding/'+slug,None)
        for slug,_,_,_ in ENTRIES:records['branding/'+slug]={'time':'smil' if slug in ANIMATED else 'static'}
        count=len(records);static=sum(m['time']=='static' for m in records.values());values=[('WORKS',count,'个作品'),('CATEGORIES',10,'个分类'),('STATIC',static,'个静态作品'),('ANIMATED',count-static,'个动效作品')]
        for i,(label,value,unit) in enumerate(values):
            x=90+(i%2)*640;y=235+(i//2)*285;f.rect(x,y,580,250);f.text(x+28,y+45,label,14,f.t['muted']);f.text(x+28,y+150,value,70,f.t['accent'],weight=700,attrs=f'data-stat="{label.lower()}"');f.text(x+265,y+150,unit,21);f.text(x+28,y+212,'图鉴快照 / 2026-10-10',14,f.t['muted'])
        f.req(f'截至2026-10-10的全库快照：{count}个作品、10类、{static}个静态和{count-static}个动效；由条目元数据计算，统计布局随数值更新。')
    else:return False
    return True

def applications(f):
    s=f.slug
    if s=='business-card':
        for x,dark in [(90,False),(750,True)]:f.rect(x,290,540,324,f.t['ink'] if dark else f.t['paper'],attrs='data-print-width="90" data-print-height="54"')
        f.mark(130,330,48);f.word(200,338,32);f.text(130,470,'林老师',28,weight=700);f.text(130,508,'Brand Designer / 示例名片',16,f.t['muted']);f.text(130,559,'designer@example.com',16);f.word(830,402,90,'#fff');f.text(1020,540,'MAKE WORK TRACEABLE',14,'#d5dfed',anchor='middle');f.text(90,695,'正面 / 信息优先',20);f.text(750,695,'背面 / 标识优先',20);f.text(90,770,'逻辑规格 90×54 mm / 展示比例 6 px/mm / 未生成印刷生产文件',17,f.t['muted']);f.req('名片正反面各540×324px，逻辑规格90×54mm，比例一致；姓名、职位与示例邮箱建立层级，不提供真实联系方式。')
    elif s=='social-kit':
        f.rect(100,230,240,240,f.t['ink'],attrs='data-design-width="240" data-design-height="240"');f.mark(175,305,90,'#fff');f.circle(220,350,95,'none',attrs='stroke="#8ea2bf" stroke-dasharray="4 4"');f.text(100,510,'头像 / 240×240',17)
        f.rect(390,230,900,300,f.t['ink'],attrs='data-design-width="1200" data-design-height="400"');f.word(430,300,70,'#fff');f.text(430,445,'MAKE WORK TRACEABLE',21,'#d5dfed');f.mark(1060,290,170,'#80aaff');f.text(390,575,'横幅 / 1200×400 / 等比缩放展示',17)
        f.rect(100,560,240,240,f.t['paper'],attrs='data-design-width="1080" data-design-height="1080"');f.word(120,590,40);f.lines(120,700,['复杂工作，','清楚推进。'],25,weight=700,step=40);f.text(390,670,'同一标识 / 三种画幅',30,weight=600);f.lines(390,733,['方帖逻辑规格1080×1080，缩略展示。','头像保留中心安全区；横幅文字避开右侧视觉。'],17,f.t['muted']);f.req('头像240×240、横幅1200×400、方帖1080×1080逻辑规格，分别以240×240/900×300/240×240展示，保持比例；共同NOVA标识。')
    elif s=='packaging-dieline':
        f.text(90,235,'折叠纸盒结构示意 / 展示单位 px',17,f.t['muted']);x,y=150,390;panels=[('粘口',24),('侧面',60),('正面',180),('侧面',60),('背面',180)];cursor=x
        total=sum(w for _,w in panels);height=220
        f.rect(x-8,y-68,total+16,height+136,'none',attrs='stroke="#ba6c43" stroke-dasharray="7 5" data-bleed="8"')
        for i,(name,w) in enumerate(panels):
            f.rect(cursor,y,w,height,f.t['soft'],attrs='data-panel-width="'+str(w)+'"');f.text(cursor+w/2,y+height+90,name,14,anchor='middle')
            if i>0:
                f.rect(cursor,y-60,w,60,f.t['paper']);f.rect(cursor,y+height,w,60,f.t['paper']);f.line(cursor,y,cursor+w,y,f.t['accent'],1.5,attrs='stroke-dasharray="5 4"');f.line(cursor,y+height,cursor+w,y+height,f.t['accent'],1.5,attrs='stroke-dasharray="5 4"')
            if name=='正面':
                f.rect(cursor+12,y+12,w-24,height-24,'none',attrs='stroke="#69734f" stroke-dasharray="3 4" data-safety="12"');f.life(cursor+50,y+30,80);f.text(cursor+w/2,y+145,'LOAM',27,anchor='middle',font='Georgia, serif',weight=700);f.text(cursor+w/2,y+181,'日常手作 / 示例包装',12,anchor='middle')
            cursor+=w
        f.path('M150 390 H174 V330 H654 V670 H174 V610 H150 Z',stroke=f.t['ink'],width=1.5,attrs='data-cut-outline="true"')
        for seam in [174,234,414,474]:
            f.line(seam,390,seam,610,f.t['accent'],1.5,attrs='stroke-dasharray="5 4" data-fold="vertical"')
            if seam>174:f.line(seam,330,seam,390,f.t['ink'],1.5);f.line(seam,610,seam,670,f.t['ink'],1.5)
        f.rect(900,315,240,293.333333,f.t['soft'],attrs='data-front-aspect="180/220"');f.path('M1140 315 L1210 275 L1210 568.333333 L1140 608.333333 Z',f.t['accent']);f.path('M900 315 L970 275 L1210 275 L1140 315 Z',f.t['paper']);f.life(970,380,100);f.text(1020,555,'LOAM',40,anchor='middle',font='Georgia, serif',weight=700);f.text(1020,586,'EARTH & EVERYDAY',13,anchor='middle')
        f.lines(90,755,['实线：外缘 / 虚线：折线 / 外扩橙线：出血示意 / 内缩绿线：安全区','未做锁底、插舌、纸厚与工艺验证，不可直接作为生产刀版。'],16,f.t['muted'],step=30);f.req('纸盒24/60/180/60/180px面板宽，粘口/侧/正/侧/背对应；顶底折片60px，橙色外扩8px示意出血，正面安全区内缩12px；只作展开结构示意，未经生产验证。')
    elif s=='circular-badge':
        cx,cy=440,505;r=215;f.circle(cx,cy,r,f.t['paper'],attrs=f'stroke="{f.t["accent"]}" stroke-width="2"');f.circle(cx,cy,165,'none',attrs=f'stroke="{f.t["accent"]}"')
        f.add('<defs><path id="badge-upper" d="M255 505 A185 185 0 0 1 625 505"/><path id="badge-lower" d="M255 505 A185 185 0 0 0 625 505"/></defs>');f.add(f'<text font-size="26" fill="{f.t["ink"]}" letter-spacing="3"><textPath href="#badge-upper" startOffset="50%" text-anchor="middle">LOAM / EVERYDAY GOODS</textPath></text><text font-size="20" fill="{f.t["ink"]}" letter-spacing="2"><textPath href="#badge-lower" startOffset="50%" text-anchor="middle">A CONCEPT BRAND</textPath></text>');f.life(390,420,100);f.text(cx,580,'LOAM',34,anchor='middle',font='Georgia, serif',weight=700)
        f.lines(820,345,['CIRCULAR / BADGE','外圈建立边界','内圈承载标识','文字沿弧线居中'],23,step=65);f.lines(820,660,['徽章用于品牌识别。','不添加虚构认证或质量背书。'],18,f.t['muted'],step=40);f.req('LOAM单色徽章，外半径215/内半径165/文字路径185；上弧品牌名称、下弧A CONCEPT BRAND，不伪造认证标志。')
    else:return False
    return True

def motion(f):
    s=f.slug
    if s=='typewriter':
        f.rect(90,235,1220,550,f.t['ink']);f.word(140,290,45,'#fff');f.text(140,430,'MAKE WORK',60,'#fff',weight=700)
        f.add('<defs><clipPath id="copy-reveal"><rect x="140" y="475" width="0" height="90"><animate attributeName="width" values="0;760" keyTimes="0;1" dur="2s" begin=".4s" fill="freeze"/></rect></clipPath></defs>')
        f.add('<g class="motion" clip-path="url(#copy-reveal)">');f.text(140,545,'TRACEABLE.',70,'#fff',weight=700);f.add('</g>');f.text(140,545,'TRACEABLE.',70,'#fff',weight=700,attrs='class="fallback"');f.text(140,675,'从资料到结果，保留每一步的来由。',22,'#d5dfed');f.text(140,735,'一次揭示 / 完整终帧',15,'#b8cff6');f.req('两行品牌文案MAKE WORK / TRACEABLE，第一行常显，第二行2秒线性遮罩揭示，延迟.4秒；不声称逐字打字，结束完整保留，不循环闪烁。')
    elif s=='brand-intro':
        f.rect(90,235,1220,550,f.t['ink']);f.add('<g id="intro-final">');f.mark(290,415,120,'#fff');f.word(470,425,100,'#fff');f.text(700,650,'MAKE WORK TRACEABLE',20,'#d5dfed',anchor='middle');f.add('</g>')
        f.add('<g class="motion"><rect x="270" y="390" width="150" height="170" fill="#14263d"><animate attributeName="opacity" values="1;0" keyTimes="0;1" dur=".8s" fill="freeze"/></rect><rect x="455" y="390" width="500" height="170" fill="#14263d"><animate attributeName="width" values="500;0" keyTimes="0;1" begin=".8s" dur="1.2s" fill="freeze"/><animate attributeName="x" values="455;955" keyTimes="0;1" begin=".8s" dur="1.2s" fill="freeze"/></rect></g>');f.text(130,752,'标识 → 字标 → 稳定终帧',16,'#b8cff6',attrs='class="fallback"');f.req('标识0..0.8s出现，字标0.8..2s揭示，完整NOVA组合与口号稳定；motion遮罩只播放一次，减少动效显示相同intro-final组合。')
    else:return False
    return True

def build():
    BUILT.clear()
    for slug,title,en,theme in ENTRIES:
        f=Brand(slug,title,en,theme)
        if not any(fn(f) for fn in [identity,typography,editorial,applications,motion]):raise ValueError('Missing renderer: '+slug)
        f.finish()
    assert len(BUILT)==24
    print('Built 24 brand and typography specimens.')
if __name__=='__main__':build()
