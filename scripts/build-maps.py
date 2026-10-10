#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build geographic and local spatial examples from explicit coordinate data."""
from pathlib import Path
from html import escape
import json
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'gallery/maps'
GEO=json.loads((ROOT/'assets/geography/western-europe.geojson').read_text())
BUILT=[]
BLUE='#3686d9';GREEN='#00a887';ORANGE='#e2a14a';PURPLE='#9774d6'
CITY=[('巴黎',2.3522,48.8566,64),('柏林',13.405,52.52,100),('马德里',-3.7038,40.4168,36),('罗马',12.4964,41.9028,49),('阿姆斯特丹',4.9041,52.3676,25),('里斯本',-9.1393,38.7223,16)]
REGIONS=[('France','法国',2.3,46.5,68),('Germany','德国',10.5,50.4,82),('Spain','西班牙',-3.8,40,55),('Portugal','葡萄牙',-8,39.8,43),('Italy','意大利',12.3,43.1,74),('Belgium','比利时',4.7,50.8,64),('Netherlands','荷兰',5.6,52.2,91),('Switzerland','瑞士',8.2,46.8,78)]
# Longitude, latitude -> fixed equirectangular projection with standard parallel 46 N.
def project(lon,lat):return 140+(lon+12)*23*math.cos(math.radians(46)),285+(56-lat)*23

def linepath(points):return 'M '+' L '.join(f'{x:.3f} {y:.3f}' for x,y in points)

def blend(t,a=(229,239,247),b=(25,117,181)):
    t=max(0,min(1,t));return '#'+''.join(f'{round(x+(y-x)*t):02x}' for x,y in zip(a,b))


class Map:
    def __init__(self,slug,title,subtitle,finding,dark=False,animated=False,footer='模拟业务数据 · 空间示意不代表实际服务或运营结果'):
        self.slug,self.title,self.subtitle,self.finding=slug,title,subtitle,finding
        self.dark,self.animated,self.footer=dark,animated,footer
        self.bg='#0d1724' if dark else '#f3f5f7';self.ink='#edf3fa' if dark else '#172a3a';self.muted='#a5b6c9' if dark else '#596e81';self.grid='#30455b' if dark else '#d9e2ea'
        self.parts=[]
        self.rect(0,0,1400,900,self.bg)
        self.text(72,55,'SVG / SPATIAL ATLAS',14,self.muted)
        self.line(72,73,1328,73,self.grid)
        self.text(72,122,title,34,weight=700);self.text(72,160,subtitle,18,self.muted)
        self.rect(72,183,1256,51,'#172c40' if dark else '#e6edf3',rx=5);self.text(92,215,finding,18,weight=600)
        self.line(72,845,1328,845,self.grid);self.text(72,877,footer,14,self.muted)
        self.text(1328,877,'SVG-PROMPT',14,self.muted,anchor='end')
    def add(self,s):self.parts.append(s)
    def text(self,x,y,text,size=18,color=None,anchor='start',weight=400):self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color or self.ink}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(text))}</text>')
    def rect(self,x,y,w,h,fill,rx=0,attrs=''):self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" fill="{fill}" {attrs}/>')
    def line(self,x,y,xx,yy,color,width=1,attrs=''):self.add(f'<line x1="{x:.3f}" y1="{y:.3f}" x2="{xx:.3f}" y2="{yy:.3f}" stroke="{color}" stroke-width="{width}" {attrs}/>')
    def circle(self,x,y,r,fill,attrs=''):self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" {attrs}/>')
    def path(self,d,fill='none',stroke=None,width=1,attrs=''):self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{width}" {attrs}/>')
    def sidebar(self,items,x=920,y=320,step=48):
        for i,text in enumerate(items):self.text(x,y+i*step,text,17,self.muted)
    def geographic(self,values=None):
        self.add('<defs><clipPath id="map-window"><rect x="140" y="285" width="511.27" height="483"/></clipPath></defs>')
        for lat in [35,40,45,50,55]:
            x,y=project(-12,lat);xx,_=project(20,lat);self.line(x,y,xx,y,self.grid);self.text(124,y+5,f'{lat}°N',14,self.muted,anchor='end')
        for lon in [-10,0,10,20]:
            x,y=project(lon,35);_,yy=project(lon,56);self.line(x,y,x,yy,self.grid);self.text(x,794,f'{lon}°',14,self.muted,anchor='middle')
        self.add('<g clip-path="url(#map-window)">')
        for f in GEO['features']:
            name=f['properties']['name'];v=values.get(name) if values else None
            fill=blend((v-40)/60) if v is not None else '#23394e' if self.dark else '#e1e7ed'
            d=' '.join(linepath([project(x,y) for x,y in ring])+' Z' for poly in f['geometry']['coordinates'] for ring in poly)
            self.path(d,fill,self.bg,1.2,attrs=f'fill-rule="evenodd" data-country="{name}"'+(f' data-value="{v}"' if v is not None else ''))
        self.add('</g>')
        self.text(140,821,'等距圆柱 · 标准纬线 46°N · 低精度裁切底图',15,self.muted)
    def local(self,x=140,y=305,w=720,h=480,maxx=600,maxy=400):
        sx=lambda v:x+v/maxx*w;sy=lambda v:y+h-v/maxy*h
        self.rect(x,y,w,h,'#14283b' if self.dark else '#edf2f6',attrs=f'stroke="{self.grid}"')
        for v in range(0,maxx+1,10 if maxx<=60 else 100):self.line(sx(v),y,sx(v),y+h,self.grid);self.text(sx(v),y+h+25,v,14,self.muted,anchor='middle')
        for v in range(0,maxy+1,10 if maxy<=40 else 100):self.line(x,sy(v),x+w,sy(v),self.grid);self.text(x-13,sy(v)+5,v,14,self.muted,anchor='end')
        self.text(x+w,y+h+48,'X / m',15,self.muted,anchor='end');self.text(x-10,y-15,'Y / m',15,self.muted)
        return sx,sy
    def finish(self,requirements,tech):
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" font-family="PingFang SC, Microsoft YaHei, sans-serif" role="img" aria-labelledby="title desc"><title id="title">'+escape(self.title)+'</title><desc id="desc">'+escape(self.finding+'。'+self.footer)+'</desc>'+''.join(self.parts)+'</svg>\n'
        p=OUT/self.slug;p.mkdir(exist_ok=True)
        (p/'index.svg').write_text(svg,encoding='utf-8')
        meta=json.loads((p/'meta.json').read_text()) if (p/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
        meta.update(slug=self.slug,title=self.title,space='2d',time='css' if self.animated else 'static',description=self.finding,tech=tech)
        (p/'meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        steps=[f'用 SVG 制作“{self.title}”：{self.subtitle}。',f'- 画布1400×900，背景{self.bg}；标题34px、正文17–18px、刻度14–15px。重点结论：“{self.finding}”。']+['- '+s for s in requirements]+['- 页脚明确：“'+self.footer+'”。']
        if self.animated:steps+=['- 事件标记与所有标签从首帧可见；CSS涟漪只是事件强调，不编码数值、时间或业务速度；减少动效模式关闭涟漪但保留完整静态图。']
        (p/'prompt.md').write_text(f'# {self.title} `{"CSS 动效" if self.animated else "静态"}` `2D`\n\n分类：[地图与空间](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+'\n'.join(steps)+'\n```\n',encoding='utf-8')
        BUILT.append(self.slug)

GEO_REQUIREMENTS=['底图使用 assets/geography/western-europe.geojson，来源Natural Earth 1:110m Admin 0 countries，公共领域；不可手绘行政轮廓。来源：https://github.com/nvkelso/natural-earth-vector；许可：https://www.naturalearthdata.com/about/terms-of-use/。','示例只截取经度−12至20、纬度35至56的部分国家；等距圆柱投影标准纬线46°N，x=140+(lon+12)×23×cos46°，y=285+(56−lat)×23；使用SVG clipPath裁切，不作精确边界、面积或距离测量。']
GEO_FOOTER='底图：Natural Earth 1:110m · 公共领域 · 部分国家裁切 · 业务数据为模拟'


def grid():
    m=Map('china-grid-map','区域格网图','抽象区域与部分省份 / 不编码距离或面积','排行榜与格网使用同一组省份；抽象位置不等于真实行政区划')
    groups=[('西北',[('新',18),('甘',12),('青',4),('陕',33)]),('华北',[('京',44),('津',17),('冀',44),('晋',26),('蒙',24)]),('东北',[('黑',16),('吉',14),('辽',30)]),('西南',[('川',58),('渝',30),('云',30),('贵',21)]),('华中',[('豫',61),('鄂',39),('湘',35)]),('华东',[('鲁',92),('苏',128),('浙',83),('沪',45),('皖',48),('闽',51)]),('华南',[('粤',136),('桂',27),('琼',8)])]
    slots=[(120,290),(380,290),(640,290),(120,490),(380,490),(640,490),(380,680)]
    colors=['#e2eaf1','#accce3','#609ecb','#2875ae']
    for (name,data),(x,y) in zip(groups,slots):
        m.text(x,y,name,19,weight=600)
        for i,(province,v) in enumerate(data):
            xx=x+i%3*68;yy=y+20+i//3*62;b=3 if v>=80 else 2 if v>=40 else 1 if v>=20 else 0
            m.rect(xx,yy,60,54,colors[b],rx=5,attrs=f'data-province="{province}" data-value="{v}" data-band="{b}"');m.text(xx+30,yy+22,province,18,'#ffffff' if b>=2 else m.ink,anchor='middle');m.text(xx+30,yy+43,v,14,'#ffffff' if b>=2 else m.ink,anchor='middle')
    ranked=sorted([p for _,ps in groups for p in ps],key=lambda p:p[1],reverse=True)[:5]
    m.text(960,305,'TOP 5 / 模拟单位',19,weight=600)
    for i,(n,v) in enumerate(ranked):
        y=350+i*58;m.text(960,y,n,18);m.rect(1000,y-16,v*1.5,20,BLUE);m.text(1230,y,v,17)
    for i,label in enumerate(['<20','20–39','40–79','≥80']):m.rect(920+i*100,700,16,16,colors[i],rx=2);m.text(920+i*100,744,label,15,m.muted)
    m.finish(['七组抽象区域：'+json.dumps(groups,ensure_ascii=False)+'。示例区域划分用于布局，不宣称唯一地理分区。','统一色档v<20、20≤v<40、40≤v<80、v≥80；显示部分省份，不是完整中国行政区划。','TOP5由同一格网数值排序得到，河南格必须存在；每格面积相同不编码数值。'],['tile grid','shared data','discrete color scale'])


def choropleth():
    m=Map('choropleth','区域指标分级设色','部分欧洲国家 / 模拟服务可用率 %','颜色表达比率而非业务总量；灰色区域表示无示例数据',footer=GEO_FOOTER)
    vals={n:v for n,_,_,_,v in REGIONS}
    # Discrete thresholds are used for fill, not a hidden continuous scale.
    representative={n:45 if v<60 else 65 if v<75 else 82 if v<90 else 95 for n,v in vals.items()}
    m.geographic(representative)
    # Preserve actual values in the SVG metadata rather than only class midpoint values.
    for i,(name,zh,lon,lat,v) in enumerate(REGIONS):
        x,y=project(lon,lat)
        if name in ('Belgium','Netherlands','Switzerland'):continue
        m.text(x,y-40 if name=='Portugal' else y,f'{zh} {v}%',16,anchor='middle')
    m.text(910,315,'模拟服务可用率',20,weight=600)
    for i,(label,value) in enumerate([('<60%',45),('60–74%',65),('75–89%',82),('≥90%',95)]):
        m.rect(910,350+i*54,24,24,blend((value-40)/60),rx=3);m.text(952,369+i*54,label,18)
    m.sidebar(['比利时 64%','荷兰 91%','瑞士 78%','未着色国家：无数据','不是实际可用率报告'],y=625,step=34)
    m.finish(GEO_REQUIREMENTS+['模拟比率：'+json.dumps(vals,ensure_ascii=False)+'；分档<60、60–74、75–89、≥90；其他国家灰色无数据。','分类色依次用映射值45/65/82/95生成，原始比率需在文本与data-value中保留；不得用总量填色比较不同面积国家。'],['equirectangular projection','choropleth','ratio bins'])
    p=OUT/'choropleth/index.svg';s=p.read_text()
    for n,v in vals.items():s=s.replace(f'data-country="{n}" data-value="{representative[n]}"',f'data-country="{n}" data-value="{v}" data-band="{0 if v<60 else 1 if v<75 else 2 if v<90 else 3}"')
    p.write_text(s,encoding='utf-8')


def symbols():
    m=Map('proportional-symbols','城市比例符号地图','六个真实城市坐标 / 模拟请求量','圆面积正比业务量；坐标真实、数值模拟',footer=GEO_FOOTER)
    m.geographic()
    m.add('<g id="city-symbols">')
    for name,lon,lat,v in CITY:
        x,y=project(lon,lat);m.circle(x,y,3*math.sqrt(v),BLUE,attrs=f'fill-opacity="0.5" stroke="{BLUE}" data-city="{name}" data-lon="{lon}" data-lat="{lat}" data-value="{v}"');m.text(x,y+4,name,14,anchor='middle')
    m.add('</g>');m.text(910,320,'请求量 / 模拟单位',20,weight=600)
    for i,v in enumerate([25,64,100]):
        y=405+i*100;m.circle(950,y,3*math.sqrt(v),'none',attrs=f'stroke="{m.muted}" data-value="{v}"');m.text(1020,y+6,v,18)
    m.sidebar(['半径 r = 3√v','面积 = 9πv','城市位置与底图同投影'],y=730,step=30)
    m.finish(GEO_REQUIREMENTS+['城市经纬度与模拟数值：'+json.dumps(CITY,ensure_ascii=False)+'。','所有数据圆与尺寸图例均r=3√v，面积正比业务量；城市中心来自上述明确经纬度，不靠手工摆放。'],['area encoding','longitude latitude','size legend'])


POINTS=[(80,70),(115,85),(150,110),(175,80),(205,125),(230,155),(300,250),(325,285),(345,245),(365,310),(390,280),(420,330),(455,190),(480,215),(500,180),(530,250),(90,310),(140,330),(250,70),(560,65)]
LOCAL_REQ=['虚构园区平面笛卡尔坐标，X轴0–600m、Y轴0–400m，北向上；绘图区x=140..860、y=305..785，比例1.2px/m，X/Y必须同尺度。','点位数据：'+json.dumps(POINTS)+'；只表达示例传感器位置，不是现实园区测量。']


def dots():
    m=Map('point-distribution','园区点位分布','虚构园区 / 20 个传感器 / 米制坐标','同尺寸标记只编码位置；颜色表示设备类型而非数量')
    sx,sy=m.local()
    for i,(x,y) in enumerate(POINTS):m.circle(sx(x),sy(y),6,BLUE if i%2==0 else GREEN,attrs=f'data-point="{i}" data-x="{x}" data-y="{y}"')
    m.text(950,320,'图例 / 设备类型',20,weight=600)
    for i,(n,col) in enumerate([('环境传感器',BLUE),('设备监测器',GREEN)]):m.circle(962,370+i*60,6,col);m.text(987,376+i*60,n,18)
    m.sidebar(['每种类型 10 个','标记半径固定 6px','坐标单位：米','比例：100m = 120px'],y=555)
    m.line(950,768,1070,768,m.ink,3);m.text(1010,797,'100 m',15,anchor='middle')
    m.finish(LOCAL_REQ+['偶数索引为环境传感器，奇数为设备监测器，均10个；固定半径6px，不能将点大小解释成强度。'],['Cartesian coordinates','point symbols','metric scale'])


def kde_values():
    # 20m square cells, fixed 45m Gaussian bandwidth; no per-panel rescaling.
    return [(x,y,sum(math.exp(-((x-px)**2+(y-py)**2)/(2*45**2)) for px,py in POINTS)/(2*math.pi*45**2)*10000) for x in range(10,600,20) for y in range(10,400,20)]


def density():
    m=Map('spatial-density','点位空间密度','同一组 20 个传感器 / 高斯核带宽 45m','密度来自显式点位计算；颜色不是手绘光斑，也不是风险概率')
    sx,sy=m.local();cells=kde_values();maxv=3
    for x,y,v in cells:m.rect(sx(x-10),sy(y+10),24,24,blend(v/maxv),attrs=f'data-cell="{x},{y}" data-density="{v:.8f}"')
    for x,y in POINTS:m.circle(sx(x),sy(y),3,'#ffffff',attrs=f'stroke="{BLUE}"')
    m.text(950,315,'点 / 公顷',20,weight=600)
    for i in range(80):m.rect(960,355+(79-i)*4,30,4,blend(i/79))
    for v in [0,1.5,3]:m.text(1010,677-v/3*316,f'{v:.1f}',17,m.muted)
    m.sidebar(['带宽 h = 45m','网格 20 × 20m','固定色域：0–3.0','未做边缘校正','非概率 / 非真实风险'],y=720,step=23)
    m.finish(LOCAL_REQ+['每20m方格中心计算sum(exp(−((x−xi)²+(y−yi)²)/(2h²)))/(2πh²)×10000，h=45m；单位点/公顷，不除以样本数。','色域固定0–3.0点/公顷，超过上限才饱和；显示原始点位白色小圆；有限窗口未边缘校正，边缘估计偏低。'],['Gaussian KDE','fixed bandwidth','shared color scale'])


EVENTS=[('E1',110,100,9),('E2',330,270,16),('E3',480,205,4)]

def events(animated=False):
    m=Map('map-ripple' if animated else 'regional-events','区域事件 · 动态强调' if animated else '区域事件分布','虚构园区 / 同一事件快照','固定圆面积编码事件次数；涟漪仅吸引注意，不编码业务量',dark=True,animated=animated)
    sx,sy=m.local()
    if animated:m.add('<style>.ripple{transform-box:fill-box;transform-origin:center;animation:ripple 3s ease-out infinite}@keyframes ripple{0%{transform:scale(.5);opacity:.8}100%{transform:scale(2);opacity:0}}@media(prefers-reduced-motion:reduce){.ripple{animation:none;display:none}}</style>')
    m.add('<g id="event-snapshot">')
    for i,(name,x,y,v) in enumerate(EVENTS):
        xx,yy=sx(x),sy(y);m.circle(xx,yy,6*math.sqrt(v),ORANGE,attrs=f'fill-opacity="0.4" stroke="{ORANGE}" data-event="{name}" data-x="{x}" data-y="{y}" data-value="{v}"');m.text(xx,yy+5,name,16,anchor='middle');m.text(xx,yy+6*math.sqrt(v)+27,f'{v} 次',16,ORANGE,anchor='middle')
    m.add('</g>')
    if animated:
        for i,(name,x,y,v) in enumerate(EVENTS):m.circle(sx(x),sy(y),20,'none',attrs=f'class="ripple" stroke="{ORANGE}" stroke-width="2" style="animation-delay:-{i}s"')
    m.sidebar(['事件计数 / 同一快照','E1：9 次','E2：16 次','E3：4 次','固定半径 r = 6√次数','涟漪相同，不编码数值'],y=335)
    m.finish(LOCAL_REQ[:1]+['事件(ID,x米,y米,次数)：'+json.dumps(EVENTS)+'；固定圆面积=36π×次数。','静态/动态使用完全相同事件标记、坐标、数值与标签；动态版每个强调圈初始半径相同20px。'],['event snapshot','area encoding']+(['CSS ripple','reduced motion'] if animated else []))


def flow():
    m=Map('origin-destination','城市起终点流向图','四条有向链路 / 模拟传输量 TB','箭头编码方向，线宽编码流量；曲线不代表实际网络路由',dark=True,footer=GEO_FOOTER)
    m.geographic();m.add(f'<defs><marker id="flow-arrow" markerWidth="9" markerHeight="9" refX="9" refY="4.5" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="{ORANGE}"/></marker></defs>')
    links=[(0,1,8,-45),(0,2,5,45),(2,5,3,-30),(1,3,6,-35)]
    for source,target,v,offset in links:
        a=CITY[source];b=CITY[target];x,y=project(a[1],a[2]);xx,yy=project(b[1],b[2]);cx=(x+xx)/2+offset;cy=(y+yy)/2-50
        # Stop 8px short of the target node so the fixed-size arrowhead stays visible.
        length=math.hypot(xx-cx,yy-cy);tx=xx-8*(xx-cx)/length;ty=yy-8*(yy-cy)/length
        m.path(f'M{x} {y} Q{cx} {cy} {tx} {ty}',stroke=ORANGE,width=v*.7,attrs=f'marker-end="url(#flow-arrow)" data-source="{a[0]}" data-target="{b[0]}" data-flow="{v}"')
    for name,lon,lat,_ in CITY:
        x,y=project(lon,lat);m.circle(x,y,6,GREEN);m.text(x+11,y+6,name,16)
    m.sidebar(['巴黎 → 柏林：8 TB','巴黎 → 马德里：5 TB','马德里 → 里斯本：3 TB','柏林 → 罗马：6 TB','线宽 = 0.7 × TB','弧线为视觉避让'],y=330)
    m.finish(GEO_REQUIREMENTS+['城市同上述真实经纬度；有向链路'+json.dumps(links)+'，索引参照城市顺序'+json.dumps(CITY,ensure_ascii=False)+'。','蓝图只展示起终点，不沿真实线路或道路，二次曲线仅为避让；线宽0.7v，箭头固定屏幕尺寸，不随线宽夸大。'],['directed flows','stroke width encoding','fixed arrowheads'])


def transit():
    m=Map('route-stations','路线与换乘拓扑图','虚构园区交通 / 站序与换乘，不编码距离','站间距为排版；交叉线路只有标记站点才表示换乘')
    line_a=[('A1',150,520),('A2',340,520),('X',550,520),('A4',760,520),('A5',1020,520)]
    line_b=[('B1',550,300),('X',550,520),('B3',550,740)]
    m.path(linepath([(x,y) for _,x,y in line_a]),stroke=BLUE,width=8,attrs='data-route="A"');m.path(linepath([(x,y) for _,x,y in line_b]),stroke=GREEN,width=8,attrs='data-route="B"')
    coords={name:(x,y) for name,x,y in line_a+line_b}
    for name,(x,y) in coords.items():
        m.circle(x,y,12 if name=='X' else 7,m.bg,attrs=f'stroke="{m.ink if name=="X" else BLUE if name.startswith("A") else GREEN}" stroke-width="3" data-station="{name}"')
        m.text(x,y-28 if name!='B1' else y+40,'中央换乘 X' if name=='X' else name,17,anchor='middle')
    m.sidebar(['A 线：A1 → A2 → X → A4 → A5','B 线：B1 → X → B3','仅 X 为换乘站','非真实园区 / 无比例尺'],x=810,y=680,step=35)
    m.finish(['A线站序A1/A2/X/A4/A5，B线B1/X/B3；X只有一个坐标(550,520)，两条线共享该站。','A线蓝、B线绿；等距或不等距站间排版不编码距离、耗时或真实地理方向，不加误导比例尺。'],['network topology','station sequence','transfer node'])


SERVICES=[('S1',170,180,140),('S2',410,220,130)]
TARGETS=[('P1',60,80),('P2',220,260),('P3',300,200),('P4',490,300),('P5',560,70),('P6',100,340)]

def is_covered(x,y):return any(math.hypot(x-cx,y-cy)<=r for _,cx,cy,r in SERVICES)


def coverage():
    covered=sum(is_covered(x,y) for _,x,y in TARGETS)
    m=Map('service-coverage','直线距离服务覆盖','虚构园区 / 半径 140m 与 130m','6 个测试点中 '+str(covered)+' 个在覆盖内；不是通行时间、无线信号或容量预测',dark=True)
    sx,sy=m.local();m.add('<defs><clipPath id="local-window"><rect x="140" y="305" width="720" height="480"/></clipPath></defs><g clip-path="url(#local-window)">')
    for name,x,y,r in SERVICES:m.circle(sx(x),sy(y),r*1.2,GREEN,attrs=f'fill-opacity="0.12" stroke="{GREEN}" data-service="{name}" data-x="{x}" data-y="{y}" data-radius-m="{r}"')
    m.add('</g>')
    for name,x,y,r in SERVICES:m.circle(sx(x),sy(y),7,GREEN);m.text(sx(x),sy(y)-16,f'{name} / {r}m',16,GREEN,anchor='middle')
    for name,x,y in TARGETS:
        ok=is_covered(x,y);col=GREEN if ok else ORANGE;m.circle(sx(x),sy(y),6,col,attrs=f'data-target="{name}" data-x="{x}" data-y="{y}" data-covered="{str(ok).lower()}"');m.text(sx(x)+12,sy(y)+5,name,16)
    m.sidebar(['服务半径：欧氏距离','绿色点：至少一个圆内','橙色点：覆盖外','边界距离 ≤ 半径视为覆盖','不含道路 / 障碍 / 衰减','重叠区域不重复计数'],y=330)
    m.finish(LOCAL_REQ[:1]+['服务点(ID,x,y,半径m)：'+json.dumps(SERVICES)+'；测试点：'+json.dumps(TARGETS)+'。','判定min距离：任一sqrt((x−cx)²+(y−cy)²)≤r即覆盖，两个圆交集只计一次。','X/Y都1.2px/m，屏幕圆半径=物理半径×1.2；直线距离覆盖不表示15分钟可达、无线信号可靠性或可服务容量。'],['Euclidean distance','union coverage','metric circles'])


def floorplan():
    m=Map('campus-floorplan','楼层空间与设备分区','虚构 60m × 40m 楼层 / 等比例，不是施工或疏散图','房间、走廊与设备使用同一米制坐标；标出入口与门洞')
    sx,sy=m.local(w=720,h=480,maxx=60,maxy=40)
    rooms=[('R1','机房',0,0,20,16,BLUE),('R2','实验室',20,0,20,16,GREEN),('R3','仓储',40,0,20,16,ORANGE),('R4','控制室',0,24,20,16,PURPLE),('R5','会议室',20,24,20,16,BLUE),('R6','办公区',40,24,20,16,GREEN)]
    for name,label,x,y,w,h,col in rooms:
        m.rect(sx(x),sy(y+h),w*12,h*12,col,attrs=f'fill-opacity="0.16" stroke="{col}" stroke-width="2" data-room="{name}" data-box-m="{x},{y},{w},{h}"');m.text(sx(x+w/2),sy(y+h/2),label,20,anchor='middle')
        # Door apertures on the corridor-facing wall, 2m wide.
        door_y=16 if y==0 else 24;m.line(sx(x+9),sy(door_y),sx(x+11),sy(door_y),m.bg,5);m.line(sx(x+9),sy(door_y),sx(x+9),sy(door_y)+(24 if y==0 else -24),col,2)
    m.text(sx(30),sy(20)+6,'8m 中央走廊',18,anchor='middle');m.text(sx(0)+10,sy(20)-25,'入口',16)
    for name,x,y in [('D1',5,5),('D2',25,5),('D3',45,29)]:m.circle(sx(x),sy(y),6,ORANGE,attrs=f'data-device="{name}" data-x="{x}" data-y="{y}"');m.text(sx(x)+12,sy(y)+5,name,15)
    m.sidebar(['1m = 12px','房间 20m × 16m','走廊 y=16..24m','门洞宽 2m','D1 / D2 / D3：设备','非消防或疏散合规图'],y=340)
    m.finish(['虚构楼层X=0–60m、Y=0–40m，绘图区720×480px，X/Y同为12px/m；北向上；走廊y=16–24m贯穿。','六房间数据(ID,功能,x,y,w,h,color)：'+json.dumps(rooms,ensure_ascii=False)+'；各房间门洞在走廊侧，宽2m；西侧走廊为入口。','设备D1(5,5)、D2(25,5)、D3(45,29)须在房间内部；平面仅为空间信息示意，不是测绘、施工或安全认证图。'],['metric floorplan','room partitions','door openings'])


TIME_DATA=[[12,18,24,32,18,12,8,15,23,30,16,10],[8,14,22,28,30,18,12,20,35,42,27,16],[6,10,18,22,34,28,18,25,40,50,36,24]]

def time_comparison():
    m=Map('spatial-comparison','多时刻空间对照','同一虚构园区 / 08:00、12:00、18:00 / 4×3 分区','三时刻共用空间范围与 0–50 色域；不能各自自动归一化')
    for index,values in enumerate(TIME_DATA):
        x=95+index*440;y=350;w=360;h=270;m.text(x+w/2,305,['08:00','12:00','18:00'][index],23,anchor='middle',weight=600)
        for i,v in enumerate(values):
            col=i%4;row=i//4;m.rect(x+col*90,y+row*90,90,90,blend(v/50),attrs=f'stroke="{m.bg}" stroke-width="2" data-time="{index}" data-zone="{i}" data-value="{v}"');m.text(x+col*90+45,y+row*90+53,v,20,'#ffffff' if v>=30 else m.ink,anchor='middle')
        m.text(x,y+h+30,'同一分区：西→东 / 北→南',15,m.muted)
    for i in range(100):m.rect(425+i*4,727,4,22,blend(i/99))
    m.text(415,744,'0',16,m.muted,anchor='end');m.text(835,744,'50',16,m.muted);m.text(625,792,'模拟任务数 / 分区；等面积格网为虚构空间分区',17,m.muted,anchor='middle')
    m.finish(['三个时刻4列×3行矩阵：'+json.dumps(TIME_DATA)+'；所有格子对应同一空间分区ID，行从北到南、列从西到东。','三图共用0–50模拟任务数色域与同样格子面积；色值blend(v/50)，不得分别按各面板最大值缩放。','这是同一空间分区的快照，不是连续时间轨迹；不以插值动画暗示未观测的数据。'],['small multiples','fixed spatial extent','shared color scale'])


def build():
    BUILT.clear();grid();choropleth();symbols();dots();density();events();events(True);flow();transit();coverage();floorplan();time_comparison()
    for i,slug in enumerate(BUILT,1):
        p=OUT/slug/'meta.json';m=json.loads(p.read_text());m['order']=i;p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(BUILT)} maps and spatial examples.')

if __name__=='__main__':build()
