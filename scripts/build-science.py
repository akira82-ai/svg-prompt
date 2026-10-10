#!/usr/bin/env python3
"""Build scientific illustrations from explicit equations; stdlib only."""
from pathlib import Path
from html import escape
import json, math
R=Path(__file__).resolve().parents[1];OUT=R/'gallery/science'
B='#51a7ef';G='#37c9a3';O='#efb15b';P='#ac91e8';BG='#0d1724';INK='#edf3fa';MUT='#a8bbce';GRID='#2b4055'
BUILT=[]
def path(points):return 'M '+' L '.join(f'{x:.4f} {y:.4f}' for x,y in points)
def lerp(a,b,t):return tuple(x+(y-x)*t for x,y in zip(a,b))
def bezier(t):
    p=[(150,650),(280,305),(670,310),(820,650)];q=[lerp(a,b,t) for a,b in zip(p,p[1:])];r=[lerp(a,b,t) for a,b in zip(q,q[1:])];return p,q,r,lerp(*r,t)
def fourier(x,n):return 4/math.pi*sum(math.sin(k*x)/k for k in range(1,2*n,2))
def eccentric(M,e):
    E=M
    for _ in range(12):E-=(E-e*math.sin(E)-M)/(1-e*math.cos(E))
    return E
class Fig:
    def __init__(self,slug,title,sub,finding,space='2d',animated=False):
        self.slug,self.title,self.sub,self.finding=slug,title,sub,finding;self.space,self.animated=space,animated;self.s=[]
        self.rect(0,0,1400,900,BG);self.text(72,55,'SVG / SCIENCE ATLAS',14,MUT);self.line((72,73),(1328,73),GRID)
        self.text(72,123,title,34,weight=700);self.text(72,161,sub,18,MUT);self.rect(72,183,1256,51,'#182c40',rx=5);self.text(92,215,finding,18)
        self.line((72,845),(1328,845),GRID);self.text(72,878,'公式驱动 / 理想化教学模型 · 非实验观测或工程认证',14,MUT);self.text(1328,878,'SVG-PROMPT',14,MUT,anchor='end')
    def add(self,s):self.s.append(s)
    def text(self,x,y,text,size=17,color=INK,anchor='start',weight=400):self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(text))}</text>')
    def rect(self,x,y,w,h,col,rx=0,attrs=''):self.add(f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" fill="{col}" rx="{rx}" {attrs}/>')
    def line(self,a,b,col=GRID,width=1,attrs=''):self.add(f'<line x1="{a[0]:.4f}" y1="{a[1]:.4f}" x2="{b[0]:.4f}" y2="{b[1]:.4f}" stroke="{col}" stroke-width="{width}" {attrs}/>')
    def curve(self,pts,col=B,width=2,attrs=''):self.add(f'<path d="{path(pts)}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linejoin="round" {attrs}/>')
    def circle(self,x,y,r,col,attrs=''):self.add(f'<circle cx="{x:.4f}" cy="{y:.4f}" r="{r}" fill="{col}" {attrs}/>')
    def side(self,lines,x=970,y=325,step=42):
        for i,s in enumerate(lines):self.text(x,y+i*step,s,17,MUT)
    def axes(self,x=130,y=300,w=720,h=420,xmin=-math.pi,xmax=math.pi,ymin=-1.6,ymax=1.6,xticks=None,yticks=None):
        sx=lambda v:x+(v-xmin)/(xmax-xmin)*w;sy=lambda v:y+h-(v-ymin)/(ymax-ymin)*h
        for v in xticks or [xmin,0,xmax]:
            self.line((sx(v),y),(sx(v),y+h));self.text(sx(v),y+h+27,f'{v:.2g}',14,MUT,anchor='middle')
        for v in yticks or [ymin,0,ymax]:
            self.line((x,sy(v)),(x+w,sy(v)));self.text(x-14,sy(v)+5,f'{v:.2g}',14,MUT,anchor='end')
        self.text(x+w,y+h+52,'x',16,MUT,anchor='end');self.text(x-12,y-15,'y',16,MUT);return sx,sy
    def motion(self,tag,attrs,tracks,dur='8s',mode='linear'):
        self.add(f'<{tag} {attrs}>')
        for attr,values in tracks.items():self.add(f'<animate attributeName="{attr}" values="'+ ';'.join(values)+f'" keyTimes="'+ ';'.join(f'{i/(len(values)-1):.8f}' for i in range(len(values)))+f'" dur="{dur}" repeatCount="indefinite" calcMode="{mode}"/>')
        self.add(f'</{tag}>')
    def finish(self,requirements,tech):
        if self.animated:self.add('<style>.fallback{display:none}@media(prefers-reduced-motion:reduce){.motion{display:none}.fallback{display:inline}}</style>')
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" font-family="PingFang SC, Microsoft YaHei, sans-serif" role="img" aria-labelledby="title desc"><title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.finding)}</desc>'+''.join(self.s)+'</svg>\n'
        d=OUT/self.slug;d.mkdir(exist_ok=True);(d/'index.svg').write_text(svg)
        meta=json.loads((d/'meta.json').read_text()) if (d/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
        meta.update(slug=self.slug,title=self.title,space=self.space,time='smil' if self.animated else 'static',tech=tech,description=self.finding,order=len(BUILT)+1);(d/'meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
        lines=['用 SVG 制作“'+self.title+'”：'+self.sub+'。','- 画布1400×900，深色底、34px标题、17–18px说明、14px刻度；蓝色主模型、绿色对照、橙色重点。','- 主结论：'+self.finding+'。']+['- '+x for x in requirements]+['- 理想化教学模型；明确参数、坐标范围与近似条件，不伪装成实验观测。']
        if self.animated:lines+=['- 动画使用SMIL预计算取样，不引入脚本；同一构造中的全部动画共同起点、时长和参数序列。减少动效模式隐藏motion组，显示完整fallback静态快照；动效不改变数值编码。']
        (d/'prompt.md').write_text(f'# {self.title} `{"SMIL 动效" if self.animated else "静态"}` `{self.space.upper()}`\n\n分类：[科学与原理](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+'\n'.join(lines)+'\n```\n');BUILT.append(self.slug)

def lissajous():
    f=Fig('lissajous','利萨茹曲线 · 频率与相位','x = sin(at + δ) / y = sin(bt) / t ∈ [0, 2π]','频率比改变闭合结构，相位差改变形状；各面板使用同一坐标尺度')
    for i,(a,b,d) in enumerate([(1,1,0),(1,2,math.pi/2),(2,3,math.pi/2)]):
        cx=265+i*435;cy=510;f.rect(cx-175,320,350,380,'#132538',rx=8)
        f.line((cx-150,cy),(cx+150,cy));f.line((cx,cy-150),(cx,cy+150))
        f.curve([(cx+145*math.sin(a*t+d),cy-145*math.sin(b*t)) for t in [j*2*math.pi/720 for j in range(721)]],B,2.5,attrs=f'data-a="{a}" data-b="{b}" data-phase="{d}"')
        f.text(cx,292,f'a:b = {a}:{b} / δ = {"0" if d==0 else "π/2"}',21,anchor='middle');f.text(cx,745,'x、y ∈ [−1, 1] / 相同比例',16,MUT,anchor='middle')
    f.finish(['三面板参数(1,1,0)、(1,2,π/2)、(2,3,π/2)，各取721点，闭合周期2π。','每面板中心(265+435i,510)，x/y均145px单位；不将曲线当时间序列折线。'],['parametric curves','frequency ratio','phase comparison'])

def spirals():
    f=Fig('golden-spiral','斐波那契螺旋近似','方块圆弧近似 / 严格黄金对数螺旋','相切四分之一圆弧与严格对数螺旋是两种曲线，不能混为一谈')
    # Sequential quarter-circle radii 1,1,2,3,5,8; centers chosen to share endpoint and tangent.
    pts=[];centers=[];start=(0,0);theta=0
    for r in [1,1,2,3,5,8]:
        cx=start[0]-r*math.cos(theta);cy=start[1]-r*math.sin(theta);segment=[(cx+r*math.cos(theta+j*math.pi/2/60),cy+r*math.sin(theta+j*math.pi/2/60)) for j in range(61)]
        centers.append((cx,cy,r,theta));pts+=segment;start=segment[-1];theta+=math.pi/2
    sx=lambda x:470+22*x;sy=lambda y:535-22*y
    for cx,cy,r,t in centers:
        endpoints=[(cx,cy),(cx+r*math.cos(t),cy+r*math.sin(t)),(cx+r*math.cos(t+math.pi/2),cy+r*math.sin(t+math.pi/2))];xs=[p[0] for p in endpoints];ys=[p[1] for p in endpoints]
        f.rect(sx(min(xs)),sy(max(ys)),r*22,r*22,'none',attrs=f'stroke="{GRID}" data-radius="{r}"');f.text(sx((min(xs)+max(xs))/2),sy((min(ys)+max(ys))/2),r,15,MUT,anchor='middle')
    f.curve([(sx(x),sy(y)) for x,y in pts],B,3)
    phi=(1+math.sqrt(5))/2;b=2*math.log(phi)/math.pi
    f.curve([(1035+9*math.exp(b*t)*math.cos(t),520-9*math.exp(b*t)*math.sin(t)) for t in [j*3*math.pi/600 for j in range(601)]],G,3,attrs=f'data-growth="{b}"')
    f.text(320,292,'斐波那契半径：1、1、2、3、5、8',20,anchor='middle');f.text(1040,292,'严格黄金对数螺旋',20,anchor='middle')
    f.text(140,750,'每段曲率恒定；段间半径发生变化',17,MUT);f.text(845,750,'r = r₀ exp(2 ln φ · θ / π)',17,MUT);f.text(845,789,'每转 90°，半径乘 φ ≈ 1.618',17,MUT)
    f.finish(['左侧半径1,1,2,3,5,8的相切四分之一圆弧，显式绘制对应方块；圆弧曲率分段恒定。','右侧r=9exp(bθ)，b=2lnφ/π、φ=(1+√5)/2，θ0..3π；每90°增长φ，不将两图叠合或声称完全相同。'],['Fibonacci approximation','logarithmic spiral','curvature distinction'])

def catenary():
    f=Fig('catenary','悬链线与抛物线','相同跨度、端点高度与最低点 / 无量纲坐标','两曲线共享端点和最低点，但中间形状不同；悬链线对应均匀柔索自重')
    sx,sy=f.axes(xmin=-2,xmax=2,ymin=0,ymax=3,xticks=[-2,-1,0,1,2],yticks=[0,1,2,3]);c=math.cosh(2)-1
    for kind,col,fn in [('catenary',B,lambda x:math.cosh(x)-1),('parabola',G,lambda x:c*x*x/4)]:f.curve([(sx(x),sy(fn(x))) for x in [-2+j*4/400 for j in range(401)]],col,3,attrs=f'data-model="{kind}"')
    for x in [-2,0,2]:f.circle(sx(x),sy(math.cosh(x)-1),5,O)
    f.side(['蓝：y = cosh x − 1','绿：y = (cosh 2 − 1)x²/4','跨度：4 / 最低点：(0,0)','端点高：cosh 2 − 1','柔索均匀、自重、无弯曲刚度','抛物线：水平投影均布荷载'],step=48)
    f.finish(['绘图区x−2..2、y0..3；蓝y=cosh(x)−1，绿y=(cosh2−1)x²/4，两者端点和最低点一致。','悬链线条件：均匀柔索、自重静力平衡、忽略弯曲刚度；抛物线对应按水平投影均布的竖向荷载，不说所有悬索都是抛物线。'],['catenary','boundary matching','load assumptions'])

def bezier_fig():
    f=Fig('bezier-de-casteljau','贝塞尔曲线 · 逐层构造','三次曲线 / 共同参数 t / De Casteljau 算法','每层使用同一个 t 做线性插值；最终点始终位于三次贝塞尔曲线上',animated=True)
    p,_,_,_=bezier(0);f.curve(p,GRID,2);f.curve([bezier(j/400)[3] for j in range(401)],B,3,attrs='id="bezier-curve"')
    for i,(x,y) in enumerate(p):f.circle(x,y,6,INK);f.text(x,y-18,f'P{i}',16,anchor='middle')
    frames=[i/60 for i in range(61)]+[1-i/60 for i in range(1,61)]
    def snapshot(t,cls):
        _,q,r,b=bezier(t);f.add(f'<g class="{cls}">');f.curve(q,G,2);f.curve(r,O,2)
        for pts,col in [(q,G),(r,O),([b],P)]:
            for x,y in pts:f.circle(x,y,6,col)
        f.add('</g>')
    snapshot(.5,'fallback');f.add('<g class="motion">')
    for layer,col in [(1,G),(2,O)]:
        values=[path(bezier(t)[layer]) for t in frames];f.motion('path',f'd="{values[0]}" fill="none" stroke="{col}" stroke-width="2"',{'d':values},'10s')
    for layer,col in [(1,G),(2,O),(3,P)]:
        for k in range({1:3,2:2,3:1}[layer]):
            ps=[bezier(t)[layer][k] if layer!=3 else bezier(t)[3] for t in frames];f.motion('circle',f'cx="{ps[0][0]}" cy="{ps[0][1]}" r="6" fill="{col}"',{'cx':[f'{x:.4f}' for x,y in ps],'cy':[f'{y:.4f}' for x,y in ps]},'10s')
    f.add('</g>');f.side(['P：4 个固定控制点','Qᵢ = (1−t)Pᵢ + tPᵢ₊₁','Rᵢ = (1−t)Qᵢ + tQᵢ₊₁','B = (1−t)R₀ + tR₁','绿色 Q / 橙色 R / 紫色 B','t：0 → 1 → 0 / 10s','静态快照：t = 0.5'],step=47)
    f.finish(['控制点'+json.dumps(p)+'，所有辅助线和点共用121个t样本0→1→0，周期10s；三次曲线取401点。','减少动效显示t=.5的完整Q/R/B构造；SMIL样本间线性插值为近似，样本时刻严格满足递推关系。'],['De Casteljau','shared parameter','SMIL sampling'])

def sierpinski():
    f=Fig('sierpinski','谢尔宾斯基三角形','递归挖空 / 迭代 0、1、2、4 阶','每阶保留 3 倍小三角；边长减半，保留面积乘 3/4')
    def triangles(a,b,c,n):
        if n==0:return [(a,b,c)]
        ab,bc,ca=lerp(a,b,.5),lerp(b,c,.5),lerp(c,a,.5)
        return triangles(a,ab,ca,n-1)+triangles(ab,b,bc,n-1)+triangles(ca,bc,c,n-1)
    for i,n in enumerate([0,1,2,4]):
        x=90+i*325;tri=triangles((x+130,355),(x,580.166604983954),(x+260,580.166604983954),n)
        for a,b,c in tri:f.add(f'<path d="{path([a,b,c])} Z" fill="{B}" data-stage="{n}"/>')
        f.text(x+130,310,f'n = {n}',24,anchor='middle');f.text(x+130,635,f'三角数：{3**n}',18,MUT,anchor='middle');f.text(x+130,675,f'面积占比：{(3/4)**n:.4f}',17,MUT,anchor='middle')
    f.text(110,779,'Nₙ = 3ⁿ / Aₙ = A₀(3/4)ⁿ / 自相似维数 log 3 / log 2 ≈ 1.585',20)
    f.finish(['四面板迭代0/1/2/4阶；每步连接边中点，保留三个角三角；数量3ⁿ，面积比例(3/4)ⁿ，不能将有限渲染称为无限细节。'],['recursive subdivision','area scaling','self similarity'])

def koch():
    f=Fig('koch-snowflake','科赫雪花 · 边长与面积','等边三角形外侧细分 / 迭代 0、1、2、3 阶','每阶边数乘 4、边长除以 3；无限极限周长发散，面积趋于 8A₀/5')
    for i,n in enumerate([0,1,2,3]):
        x=90+i*325;pts=[(x+130,375),(x+20,565.5255888325765),(x+240,565.5255888325765),(x+130,375)]
        for _ in range(n):
            out=[]
            for a,b in zip(pts,pts[1:]):
                c,d=lerp(a,b,1/3),lerp(a,b,2/3);dx,dy=d[0]-c[0],d[1]-c[1];peak=(c[0]+dx*.5-dy*math.sqrt(3)/2,c[1]+dy*.5+dx*math.sqrt(3)/2);out.extend([a,c,peak,d])
            pts=out+[out[0]]
        f.curve(pts,B,2,attrs=f'data-stage="{n}" data-edges="{3*4**n}"');f.text(x+130,305,f'n = {n}',24,anchor='middle');f.text(x+130,675,f'边数 {3*4**n} / Pₙ/P₀ = {(4/3)**n:.3f}',16,MUT,anchor='middle')
    f.text(110,765,'Pₙ = P₀(4/3)ⁿ',22);f.text(650,765,'Aₙ/A₀ = 1 + 3/5 · [1 − (4/9)ⁿ]',22)
    f.finish(['四阶外侧构造0/1/2/3，各边三等分，中间段用向外等边凸起替代；边数3×4ⁿ，周长P₀(4/3)ⁿ。','面积Aₙ=A₀[1+3/5(1−(4/9)ⁿ)]；无穷阶极限周长无限，面积有限8A₀/5；有限图示不能显示无限迭代。'],['Koch recursion','perimeter growth','finite area limit'])

def fourier_fig(animated=False):
    f=Fig('fourier-build' if animated else 'fourier-square','傅里叶级数 · 谐波构建' if animated else '傅里叶级数 · 方波逼近','Sₙ(x) = 4/π Σ sin((2k−1)x)/(2k−1) / 周期 2π','增加奇次谐波使过渡区变窄；跃点附近的吉布斯超调不会消失',animated=animated)
    sx,sy=f.axes(xticks=[-math.pi,-math.pi/2,0,math.pi/2,math.pi],yticks=[-1,0,1]);xs=[-math.pi+j*2*math.pi/600 for j in range(601)]
    for sign in [-1,1]:f.line((sx(-math.pi if sign<0 else 0),sy(sign)),(sx(0 if sign<0 else math.pi),sy(sign)),MUT,1,attrs='stroke-dasharray="6 6"')
    ns=[1,3,9,25]
    if animated:
        values=[path([(sx(x),sy(fourier(x,n))) for x in xs]) for n in ns]
        f.motion('path',f'class="motion" d="{values[0]}" fill="none" stroke="{B}" stroke-width="3"',{'d':values+[values[-1]],},'8s',mode='discrete')
        f.curve([(sx(x),sy(fourier(x,25))) for x in xs],B,3,attrs='class="fallback" data-terms="25"')
        for i,n in enumerate(ns):
            opacity=['1' if j==i else '0' for j in range(4)]+['1' if i==3 else '0'];f.motion('text',f'class="motion" x="970" y="680" fill="{B}" font-size="22" opacity="{opacity[0]}"',{'opacity':opacity},'8s',mode='discrete');f.s[-1]=f.s[-1].replace('</text>',f'N = {n}</text>')
        f.text(970,725,'每档 2 秒 / 快照 N=25',16,MUT)
    else:
        for n,col in zip(ns,[P,O,G,B]):f.curve([(sx(x),sy(fourier(x,n))) for x in xs],col,2,attrs=f'data-terms="{n}"')
    f.side(['N：奇次谐波项数','N = 1 / 3 / 9 / 25' if animated else '紫 1 / 橙 3 / 绿 9 / 蓝 25','最高频率：2N − 1','虚线：理想方波 ±1','跃点收敛到左右均值 0','超调约为跳变量的 9%','更多项 ≠ 消除超调'],step=44)
    f.finish(['方波周期2π，(−π,0)为−1、(0,π)为+1，跃点取0；N1/3/9/25项，每项频率2k−1。','绘图区x−π..π、y−1.6..1.6，601点，静态与动画使用同一公式与尺度；动画每2秒切换项数，离散切换不伪装成连续物理时间。','吉布斯超调极限约跳变量8.95%，发生范围随项数变窄；不可写成增加项数就完全无超调。'],['Fourier series','odd harmonics','Gibbs phenomenon']+(['SMIL discrete stages'] if animated else []))

def waves(standing=False):
    slug='standing-wave' if standing else 'wave-interference';title='驻波 · 节点与腹点' if standing else '波的叠加与干涉'
    f=Fig(slug,title,'两列等幅反向行波 / 无量纲 x ∈ [0, 2π]','等幅反向波叠加形成驻波：节点固定，腹点振幅为单列波的两倍',animated=True)
    sx,sy=f.axes(xmin=0,xmax=2*math.pi,ymin=-2.4,ymax=2.4,xticks=[0,math.pi/2,math.pi,3*math.pi/2,2*math.pi],yticks=[-2,0,2]);xs=[j*2*math.pi/360 for j in range(361)];ts=[j*2*math.pi/48 for j in range(49)]
    funcs=[lambda x,t:math.sin(x-t),lambda x,t:math.sin(x+t),lambda x,t:2*math.sin(x)*math.cos(t)]
    for index in ([2] if standing else [0,1,2]):
        fn=funcs[index];col=[B,G,O][index];values=[path([(sx(x),sy(fn(x,t))) for x in xs]) for t in ts]
        f.motion('path',f'class="motion" d="{values[0]}" fill="none" stroke="{col}" stroke-width="{3 if index==2 else 1.5}" data-wave="{index}"',{'d':values},'6s');f.curve([(sx(x),sy(fn(x,0))) for x in xs],col,3 if index==2 else 1.5,attrs='class="fallback"')
    if standing:
        for x in [0,math.pi,2*math.pi]:f.circle(sx(x),sy(0),6,P,attrs=f'data-node="{x}"')
        for sign in [-1,1]:f.curve([(sx(x),sy(sign*2*abs(math.sin(x)))) for x in xs],MUT,1,attrs='stroke-dasharray="5 5"')
    f.side(['蓝：y₁ = sin(x − t)','绿：y₂ = sin(x + t)','橙：y = 2 sin x · cos t','k = 1 / ω = 1 / A = 1','节点：x = 0、π、2π','腹点：x = π/2、3π/2','6秒代表相位周期 2π','固定快照：t = 0'],step=44)
    f.finish(['y₁=sin(x−t)、y₂=sin(x+t)，共同48段相位周期2π、视觉周期6s；合成y=2sinx cos t，振幅范围±2，X0..2π。','驻波节点x0/π/2π不移动，腹点π/2与3π/2振幅2；虚线包络±2|sinx|；这是理想一维无耗散线性波，不表示介质质点沿波传播。','动画逐帧同参采样，样本间插值近似；减少动效快照t0。'],['linear superposition','opposite traveling waves','standing nodes','SMIL sampling'])

def orbit():
    f=Fig('orbit-gravity','开普勒轨道 · 等时扫等面积','理想二体 / a = 1 / e = 0.6 / M = 2πt/T','中心天体位于焦点；近心点更快，等时间间隔扫过相同面积',animated=True)
    cx,cy=490,525;scale=240;e=.6;b=math.sqrt(1-e*e)
    pos=lambda E:(cx+scale*math.cos(E),cy-scale*b*math.sin(E))
    f.curve([pos(j*2*math.pi/360) for j in range(361)],B,2)
    focus=(cx+scale*e,cy);f.circle(*focus,12,O);f.text(focus[0],focus[1]+38,'焦点 / 中心天体',16,O,anchor='middle')
    for i in [0,4]:
        es=[eccentric(2*math.pi*(i+j/240)/8,e) for j in range(241)];f.add(f'<path d="{path([focus]+[pos(E) for E in es]+[focus])} Z" fill="{G}" fill-opacity=".18" data-sector="{i}"/>')
    ps=[pos(eccentric(j*2*math.pi/96,e)) for j in range(97)];f.motion('circle',f'class="motion" cx="{ps[0][0]}" cy="{ps[0][1]}" r="7" fill="{G}"',{'cx':[f'{x:.4f}' for x,y in ps],'cy':[f'{y:.4f}' for x,y in ps]},'12s');f.circle(*ps[0],7,G,attrs='class="fallback"')
    for x,label in [(cx+scale,'近心点'),(cx-scale,'远心点')]:f.text(x,cy-28,label,16,MUT,anchor='middle')
    f.side(['E − e sin E = M','x = a cos E','y = a√(1−e²) sin E','焦点：x = +ae','绿色扇区：各 Δt = T/8','近/远心距离：0.4a / 1.6a','T：视觉周期 12s','忽略摄动与天体大小比例'],step=44)
    f.finish(['a1/e.6/b.8，椭圆中心(490,525)，240px/a；焦点(634,525)；用牛顿法解E−e sinE=M，均匀M取97点，周期12s。','两绿色扫面积扇区M0..π/4与π..5π/4，各Δt=T/8；精确面积abΔM/2相同，绘制240段近似。','理想二体、忽略摄动；不使用匀速角度绕椭圆冒充开普勒运动；屏幕y方向翻转。'],['Kepler equation','equal areas','eccentric anomaly','SMIL sampling'])

PLANETS=[('水星',.3871),('金星',.7233),('地球',1),('火星',1.5237),('木星',5.2028)]
def solar():
    f=Fig('solar-system','太阳系 · 轨道周期对照','五行星 / 圆轨道简化 / T² ∝ a³','周期由半长轴决定；屏幕轨道半径为压缩示意，不能用于距离比较',animated=True)
    cx,cy=490,525;f.circle(cx,cy,17,O)
    for i,(name,a) in enumerate(PLANETS):
        radius=70+i*43;T=a**1.5;f.circle(cx,cy,radius,'none',attrs=f'stroke="{GRID}"');ps=[(cx+radius*math.cos(j*2*math.pi/96),cy-radius*math.sin(j*2*math.pi/96)) for j in range(97)]
        f.motion('circle',f'class="motion" cx="{ps[0][0]}" cy="{ps[0][1]}" r="5" fill="{[P,G,B,O,INK][i]}" data-planet="{name}" data-a="{a}" data-period="{T:.10f}"',{'cx':[f'{x:.4f}' for x,y in ps],'cy':[f'{y:.4f}' for x,y in ps]},f'{12*T:.8f}s');f.circle(*ps[0],5,[P,G,B,O,INK][i],attrs='class="fallback"')
        f.text(970,360+i*58,f'{name} / {a:.4g} AU / {T:.3f} 年',17,[P,G,B,O,INK][i])
    f.text(970,306,'半长轴 / 模型周期',21);f.side(['T = a^(3/2) / 年','a：半长轴 / AU','地球 1 年映射为 12 秒','只收录五个示例行星','不编码天体尺寸 / 相位','圆轨道，忽略偏心与摄动'],y=690,step=23)
    f.finish(['示例半长轴AU：'+json.dumps(PLANETS,ensure_ascii=False)+'；模型周期T=a^1.5年，地球1年映射12s，全部初始相位0。','半长轴近似参考NASA Planetary Fact Sheet https://nssdc.gsfc.nasa.gov/planetary/factsheet/ ，动画周期是太阳主导二体近似的计算值，不宣称精确星历。','屏幕半径70/113/156/199/242px为压缩示意、不按真实距离；各天体固定5px不按直径；圆轨道简化，不包含全部行星。'],['Kepler third law','period comparison','schematic radii','SMIL sampling'])

def lens():
    f=Fig('thin-lens','薄透镜成像 · 三条主光线','理想会聚薄透镜 / f = 1 / u = 3 / v = 1.5','物距 3f 得到倒立实像：像距 1.5f，放大率 −0.5；光线在像点相交')
    sx=lambda x:650+140*x;sy=lambda y:525-140*y
    f.line((110,525),(1110,525),GRID,2);f.line((650,300),(650,745),B,4);f.text(650,285,'会聚薄透镜',20,B,anchor='middle')
    for x,label in [(-1,'F'),(1,"F′"),(-2,'2F'),(2,"2F′")]:f.circle(sx(x),sy(0),4,INK);f.text(sx(x),sy(0)+30,label,16,MUT,anchor='middle')
    obj=(-3,1);img=(1.5,-.5)
    f.line((sx(-3),sy(0)),(sx(-3),sy(1)),G,4);f.text(sx(-3),sy(1)-18,'物体 / h=1',17,G,anchor='middle');f.line((sx(1.5),sy(0)),(sx(1.5),sy(-.5)),O,4);f.text(sx(1.5),sy(-.5)+30,'实像 / h′=−0.5',17,O,anchor='middle')
    for name,points,col in [('parallel',[obj,(0,1),img],P),('center',[obj,(0,0),img],G),('focus',[obj,(0,-.5),img],O)]:f.curve([(sx(x),sy(y)) for x,y in points],col,2,attrs=f'data-ray="{name}"')
    f.side(['1/f = 1/u + 1/v','u = 3f / v = 1.5f','m = −v/u = −0.5','平行入射 → 后焦点','过光心 → 方向不变','过前焦点 → 平行出射','近轴、薄透镜、理想无像差'],x=1130,y=350,step=46)
    f.finish(['坐标以焦距f为单位，透镜x0，物体(−3,1)，像点(1.5,−.5)，140px/f；三主光线依次经(0,1)、(0,0)、(0,−.5)，均在像点相交。','1/f=1/u+1/v，u3/v1.5/m−.5；理想薄透镜、近轴、无像差模型，教学图纵向高度夸张，不是实际光学追迹；前焦点x−1，后焦点x1。'],['thin lens equation','principal rays','real inverted image'])

def projection():
    f=Fig('three-d','三维投影 · 同物体对照','同一单位立方体 / 正交、透视、等距投影','三个面板使用同一组顶点和边；投影方式改变画面，不改变物体结构',space='3d')
    verts=[(x,y,z) for x in [-1,1] for y in [-1,1] for z in [-1,1]];edges=[(i,j) for i,a in enumerate(verts) for j,b in enumerate(verts) if i<j and sum(x!=y for x,y in zip(a,b))==1]
    def camera(p):
        x,y,z=p;u=math.cos(math.pi/6)*x+math.sin(math.pi/6)*z;depth=-math.sin(math.pi/6)*x+math.cos(math.pi/6)*z;return u,math.cos(math.pi/9)*y-math.sin(math.pi/9)*depth,math.sin(math.pi/9)*y+math.cos(math.pi/9)*depth
    funcs=[lambda p:camera(p)[:2],lambda p:(camera(p)[0]*4/(4+camera(p)[2]),camera(p)[1]*4/(4+camera(p)[2])),lambda p:((p[0]-p[2])/math.sqrt(2),(2*p[1]-p[0]-p[2])/math.sqrt(6))]
    for k,(name,fn) in enumerate(zip(['正交 / 斜视','透视 / 相机距离 4','等距 / 三轴等缩短'],funcs)):
        cx=270+k*430;cy=510;f.text(cx,305,name,21,anchor='middle');coords=[fn(p) for p in verts]
        for i,j in edges:f.line((cx+100*coords[i][0],cy-100*coords[i][1]),(cx+100*coords[j][0],cy-100*coords[j][1]),[B,G,O][k],2,attrs=f'data-panel="{k}" data-edge="{i},{j}"')
        f.text(cx,720,['平行线保持平行','近大远小 / 透视分母','三条坐标轴夹角 120°'][k],17,MUT,anchor='middle')
    f.text(100,798,'顶点 (±1, ±1, ±1) / 12 条边 / 全部边显示，未做隐藏线消除',18,MUT)
    f.finish(['顶点(±1,±1,±1)的12条边；正交相机先绕Y轴30°：u=cos30°x+sin30°z，d=−sin30°x+cos30°z；再俯仰20°：v=cos20°y−sin20°d，depth=sin20°y+cos20°d；透视(U,V)=4(u,v)/(4+depth)，相机距离4。','等距u=(x−z)/√2、v=(2y−x−z)/√6；三坐标轴相同缩短率，不是随意斜画；三个面板100px/投影单位，全部边显示无隐藏线处理。'],['orthographic projection','perspective division','isometric basis'])

def mobius():
    f=Fig('topology-deform','莫比乌斯带 · 半扭转构造','参数曲面 / θ ∈ [0, 2π] / v ∈ [−0.35, 0.35]','绕行一圈，横向坐标反向；边界只有一条闭合曲线，不是环面形变',space='3d')
    def p(t,v):return ((1+v*math.cos(t/2))*math.cos(t),(1+v*math.cos(t/2))*math.sin(t),v*math.sin(t/2))
    def project(p):
        x,y,z=p;return (490+240*(.85*x-.45*y),530-240*(.3*x+.55*y+.8*z))
    for i in range(13):
        v=-.35+i*.7/12;f.curve([project(p(j*2*math.pi/240,v)) for j in range(241)],B,1)
    for j in range(49):
        t=j*2*math.pi/48;f.curve([project(p(t,-.35)),project(p(t,.35))],GRID,1)
    boundary=[project(p(j*4*math.pi/480,.35)) for j in range(481)];f.curve(boundary,O,3,attrs='data-boundary="single"')
    f.side(['x = (1+v cos(θ/2)) cos θ','y = (1+v cos(θ/2)) sin θ','z = v sin(θ/2)','p(2π,v) = p(0,−v)','橙色：单条边界 / θ 0..4π','固定相机线框，无隐藏面','非自交环面 / 非拓扑变形'],x=910,y=345,step=48)
    f.finish(['莫比乌斯嵌入p(θ,v)=((1+v cos(θ/2))cosθ,(1+v cos(θ/2))sinθ,v sin(θ/2))，v±.35；13纵向曲线与49横向线段；固定线性投影。','接缝p(2π,v)=p(0,−v)，橙色边界固定v.35让θ0..4π一圈闭合；该窄带单侧、单边界，不宣称环面可连续变成莫比乌斯带；全部网格显示，不作遮挡。'],['Mobius parameterization','half twist','single boundary'],)


def descent():
    f=Fig('gradient-descent','梯度下降 · 步长与收敛','f(x,y) = x² + 3y² / η = 0.2 / 起点 (2,1.5)','沿负梯度更新，损失逐步下降；步长过大仍可能发散，不能只看箭头方向')
    sx,sy=f.axes(xmin=-2.5,xmax=2.5,ymin=-2,ymax=2,xticks=[-2,-1,0,1,2],yticks=[-2,-1,0,1,2])
    f.add('<defs><clipPath id="contour-window"><rect x="130" y="300" width="720" height="420"/></clipPath></defs><g clip-path="url(#contour-window)">')
    for level in [.25,1,3,6,9]:f.curve([(sx(math.sqrt(level)*math.cos(t)),sy(math.sqrt(level/3)*math.sin(t))) for t in [j*2*math.pi/240 for j in range(241)]],GRID,1,attrs=f'data-level="{level}"')
    f.add('</g>')
    pts=[(2,1.5)]
    for _ in range(10):x,y=pts[-1];pts.append((.6*x,-.2*y))
    f.curve([(sx(x),sy(y)) for x,y in pts],O,2)
    for i,(x,y) in enumerate(pts):f.circle(sx(x),sy(y),5 if i<4 else 3,G,attrs=f'data-step="{i}" data-x="{x:.10f}" data-y="{y:.10f}" data-loss="{x*x+3*y*y:.10f}"')
    f.text(sx(2)+12,sy(1.5)-10,'起点',17);f.circle(sx(0),sy(0),5,P);f.text(sx(0)-15,sy(0)+28,'最优点 (0,0)',16,P)
    f.side(['∇f = (2x, 6y)','pₖ₊₁ = pₖ − η∇f(pₖ)','η = 0.2','xₖ₊₁ = 0.6xₖ','yₖ₊₁ = −0.2yₖ','稳定条件：0 < η < 1/3','示例更新 10 步','凸二次函数，不代表所有模型'],step=45)
    f.finish(['函数x²+3y²，梯度(2x,6y)，起点(2,1.5)，η.2，10步显式迭代(x,y)→(.6x,−.2y)，每步标记损失。','等高线.25/1/3/6/9，椭圆参数(√c cosθ,√(c/3)sinθ)，绘图区x±2.5、y±2；绘图窗口以外等高线须裁切。','Hessian diag(2,6)，收敛条件0<η<2/6；η≥1/3不能保证收敛，此凸二次例不推广到非凸损失。'],['quadratic objective','explicit gradient','learning rate stability'])

def build():
    BUILT.clear();lissajous();spirals();catenary();bezier_fig();sierpinski();koch();fourier_fig();fourier_fig(True);waves();waves(True);lens();orbit();solar();projection();mobius();descent();print(f'Built {len(BUILT)} scientific illustrations.')
if __name__=='__main__':build()
