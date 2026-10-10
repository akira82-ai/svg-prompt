#!/usr/bin/env python3
"""Deterministic geometric compositions, with explicit generative rules."""
import json,math,random
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'gallery/geometry'
ENTRIES=[('geometric-composition','基础几何构成','Geometric Composition'),('regular-polygons','正多边形构成','Polygon Composition'),('stars-and-flowers','星形与花形','Stars and Petals'),('boolean-shapes','布尔几何构成','Boolean Geometry'),('rotational-patterns','放射与旋转','Radial Symmetry'),('polar-rose','极坐标花园','Polar Garden'),('sunflower','黄金角排列','Golden-angle Phyllotaxis'),('spiral-composition','螺旋构成','Spiral Composition'),('wave-superposition','波形叠构','Wave Superposition'),('lissajous-curves','利萨如曲线','Lissajous Curves'),('flow-field','流场线迹','Flow Field'),('voronoi-tessellation','沃罗诺伊分区','Voronoi Tessellation'),('triangulated-art','三角网格艺术','Triangulated Art'),('moire-patterns','干涉纹构成','Moiré Patterns'),('fractal-tree','递归分形树','Recursive Fractal Tree'),('iso-cubes','等距体块构成','Isometric Blocks'),('shape-morph','几何形变','Geometric Morphing'),('blob-morph','有机形变','Organic Morphing')]
RETIRED=['circle','ellipse','line','path','polygon','polyline','rectangle','fractal-tree-grow','walking-square','spirals-and-waves']
COLORS=['#75ddcf','#e7b875','#819af8','#d18eba','#4e8195']
GOLDEN=math.pi*(3-math.sqrt(5))
def polar(cx,cy,r,t):return (cx+r*math.cos(t),cy+r*math.sin(t))
def path(points,closed=False):return 'M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in points)+(' Z' if closed else '')
def regular(cx,cy,r,n):return [polar(cx,cy,r,-math.pi/2+2*math.pi*i/n) for i in range(n)]
def rose(cx,cy,r,k,n=1080):return [polar(cx,cy,r*math.cos(k*t),t) for t in [2*math.pi*i/n for i in range(n)]]
def clip(poly,nx,ny,c):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  va=nx*a[0]+ny*a[1]-c;vb=nx*b[0]+ny*b[1]-c
  if va<=1e-8:out.append(a)
  if (va<0 and vb>0) or (va>0 and vb<0):
   t=va/(va-vb);out.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
 return out
def seeds():
 rng=random.Random(41);return [(105+col*208+rng.uniform(-38,38),235+row*130+rng.uniform(-28,28)) for row in range(4) for col in range(6)]
def cells(points):
 result=[]
 for i,(x,y) in enumerate(points):
  poly=[(80,210),(1320,210),(1320,780),(80,780)]
  for j,(xx,yy) in enumerate(points):
   if i!=j:poly=clip(poly,xx-x,yy-y,(xx*xx+yy*yy-x*x-y*y)/2)
  result.append(poly)
 return result
def flow_angle(x,y):return .65*math.sin(x/200)*math.cos(y/175)+.12*math.sin(y/110)
def flow_lines():
 lines=[]
 for j in range(38):
  x,y=83,215+j*15;pts=[]
  for _ in range(390):
   if not (80<=x<=1320 and 205<=y<=785):break
   pts.append((x,y));a=flow_angle(x,y);mid=flow_angle(x+2*math.cos(a),y+2*math.sin(a));x+=4*math.cos(mid);y+=4*math.sin(mid)
  if len(pts)>2:lines.append(pts)
 return lines
def triangles():
 rng=random.Random(19);grid=[]
 for row in range(6):
  grid.append([(80+col*124+(rng.uniform(-28,28) if 0<col<10 and 0<row<5 else 0),210+row*114+(rng.uniform(-24,24) if 0<row<5 and 0<col<10 else 0)) for col in range(11)])
 ts=[]
 for row in range(5):
  for col in range(10):
   a,b,c,d=grid[row][col],grid[row][col+1],grid[row+1][col+1],grid[row+1][col]
   ts.extend([(a,b,c),(a,c,d)] if (row+col)%2==0 else [(a,b,d),(b,c,d)])
 return ts
def tree_segments():
 out=[]
 def branch(x,y,length,angle,depth):
  xx=x+length*math.cos(angle);yy=y+length*math.sin(angle);out.append((x,y,xx,yy,depth))
  if depth<8:
   for delta in [-.43,.43]:branch(xx,yy,length*.72,angle+delta,depth+1)
 branch(700,760,155,-math.pi/2,0);return out
def morph_shapes(kind):
 n=96
 if kind=='geometric':
  shapes=[]
  for mode in ['square','circle','diamond']:
   pts=[]
   for i in range(n):
    t=-math.pi/2+i*2*math.pi/n;c,s=math.cos(t),math.sin(t)
    r=180 if mode=='circle' else 180/max(abs(c),abs(s)) if mode=='square' else 235/(abs(c)+abs(s))
    pts.append((700+r*c,490+r*s))
   shapes.append(pts)
  return shapes
 return [[polar(700,490,200*(1+.13*math.sin(3*t+phase)+.08*math.cos(5*t-phase)),t) for t in [-math.pi/2+i*2*math.pi/n for i in range(n)]] for phase in [0,2*math.pi/3,4*math.pi/3]]
class Plate:
 def __init__(self,slug,title,en,order):
  self.slug,self.title,self.en,self.order=slug,title,en,order;self.a=[];self.notes=[];self.time='static'
  self.rect(0,0,1400,900,'#101d2d');self.text(64,64,'GENERATIVE STUDIES / '+f'{order:02}',14,'#aabfd5');self.text(64,116,title,34);self.text(1336,116,en,20,'#aabfd5','end')
  self.add('<defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620"/></clipPath><linearGradient id="ink" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#75ddcf"/><stop offset="1" stop-color="#819af8"/></linearGradient></defs><g clip-path="url(#stage)">')
 def add(self,s):self.a.append(s)
 def rect(self,x,y,w,h,c,extra=''):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')
 def text(self,x,y,t,size=18,c='#e7effa',anchor='start'):self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" text-anchor="{anchor}">{escape(t)}</text>')
 def circle(self,x,y,r,c='none',stroke='none',sw=2,extra=''):self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{c}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
 def draw(self,d,c='none',stroke='none',sw=2,extra=''):self.add(f'<path d="{d}" fill="{c}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
 def finish(self):
  self.add('</g>');self.text(64,856,self.notes[0],16,'#aabfd5');self.add('<style>.snapshot{display:none}@media(prefers-reduced-motion:reduce){.motion{display:none}.snapshot{display:inline}.grow{animation:none;stroke-dashoffset:0}}@keyframes grow{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}</style>')
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">{escape(self.title)} / {escape(self.en)}</title><desc id="desc">{escape("；".join(self.notes))}</desc>'+''.join(self.a)+'</svg>\n'
  d=OUT/self.slug;d.mkdir(exist_ok=True);old=json.loads((d/'meta.json').read_text()) if (d/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
  old.update(slug=self.slug,title=self.title,order=self.order,space='2d',time=self.time,description=self.notes[0],tech=['parametric geometry','deterministic generation','SMIL morph' if self.time=='smil' else 'CSS growth' if self.time=='css' else 'path']);(d/'meta.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n');(d/'index.svg').write_text(svg)
  (d/'prompt.md').write_text(f'# {self.title} / {self.en}\n\n分类：[几何与生成艺术](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n用 SVG 制作“{self.title} / {self.en}”。\n- 1400×900画布，深色#101d2d，文字#e7effa、辅助#aabfd5，几何色板#75ddcf/#e7b875/#819af8/#d18eba/#4e8195；标题中英文，主体区域x64..1336、y190..810。\n'+''.join('- '+n+'\n' for n in self.notes)+'- 公式与构造细节只写在提示词，不把主画面做成代码教学卡。仅为几何艺术，不是测量数据或物理仿真。\n- 生成器 scripts/build-geometry.py 包含完整坐标构造；下列SVG是可复现的几何、色彩和参数参考。\n'+svg+'```\n')
def render(p):
 s=p.slug
 if s=='geometric-composition':
  p.circle(510,480,225,'#75ddcf');p.rect(510,310,420,330,'#819af8');p.draw('M335 705L700 220 1050 705Z','none','#e7b875',8);p.circle(850,545,170,'#101d2d');p.circle(850,545,170,'none','#d18eba',3);p.draw('M250 740H1150',stroke='#4e8195',sw=2);p.rect(340,267,120,25,'#e7b875');p.notes=['基础元素合成一个完整构图，以遮挡、对比和留白组织视觉。','圆(510,480,r225)、矩形(510,310,420,330)、大三角、右侧圆形负空间与水平线；元素共享画面，不再拆为7张属性教程。']
 elif s=='regular-polygons':
  for i,n in enumerate([3,4,5,6,8]):
   x=230+i*235;y=490;p.draw(path(regular(x,y,100,n),True),COLORS[i]);p.draw(path(regular(x,y,127,n),True),stroke=COLORS[i],sw=1);p.text(x,715,f'{n} SIDES',14,'#aabfd5','middle')
  p.notes=['正多边形共享中心线与尺度，边数变化形成横向节奏。','n=3/4/5/6/8，外接半径100，轮廓半径127，顶点角−π/2+2πi/n；对比外接尺度，不宣称视觉面积一致。']
 elif s=='stars-and-flowers':
  for j,n in enumerate([5,6,8]):
   x=270+j*430;pts=[polar(x,390,128 if i%2==0 else 55,-math.pi/2+math.pi*i/n) for i in range(n*2)];p.draw(path(pts,True),COLORS[j]);pts=[polar(x,670,103*(.76+.24*math.cos(n*(t+math.pi/2))),t) for t in [2*math.pi*i/480 for i in range(480)]];p.draw(path(pts,True),stroke=COLORS[j],sw=3)
  p.notes=['相同瓣数的锐角星与圆润花形上下呼应。','上排n=5/6/8外半径128内55；下排r=103(0.76+0.24cos(n(θ+π/2)))，480点闭合采样；连续轮廓不是二次曲线冒充。']
 elif s=='boolean-shapes':
  p.add('<defs><mask id="subtract" maskUnits="userSpaceOnUse" x="540" y="300" width="320" height="380"><rect x="540" y="300" width="320" height="380" fill="white"/><circle cx="765" cy="455" r="150" fill="black"/></mask><clipPath id="intersection"><circle cx="1105" cy="490" r="150"/></clipPath></defs>')
  p.draw('M470 490a150 150 0 1 0-300 0a150 150 0 1 0 300 0 M390 490a70 70 0 1 0-140 0a70 70 0 1 0 140 0','#75ddcf',extra='fill-rule="evenodd"');p.circle(700,490,150,'#e7b875',extra='mask="url(#subtract)"');p.circle(1005,490,150,'#819af8',extra='clip-path="url(#intersection)"')
  for x,t in [(320,'DIFFERENCE / RING'),(700,'DIFFERENCE / CRESCENT'),(1055,'INTERSECTION')]:p.text(x,730,t,14,'#aabfd5','middle')
  p.notes=['圆环、月牙与交集由真实负空间和边界构成。','圆环evenodd挖孔半径150/70；月牙从(700,490,r150)减去(765,455,r150)；交集是(1005,490,r150)与(1105,490,r150)共同区域，透明负空间不靠底色覆盖。']
 elif s=='rotational-patterns':
  for j,n in enumerate([8,12,24]):
   x=270+j*430
   for i in range(n):p.rect(x-13,315,26,155,COLORS[j],extra=f'rx="13" transform="rotate({i*360/n} {x} 490)"')
   p.circle(x,490,55,'#101d2d');p.text(x,735,f'{n} × {360/n:g}°',16,'#aabfd5','middle')
  p.notes=['同一径向单元复制出三种密度，轮廓由旋转规则形成。','单元26×155、圆角13，绕共同圆心按360/n复制n=8/12/24，中心负空间半径55。']
 elif s=='polar-rose':
  for j,k in enumerate([3,5,7]):
   x=270+j*430;p.draw(path(rose(x,490,173,k),True),stroke=COLORS[j],sw=3);p.circle(x,490,192,stroke='#294258',sw=1)
  p.notes=['三、五、七瓣玫瑰曲线以共享尺度形成极坐标花园。','r=173cos(kθ)，k=3/5/7；θ采样0..2π共1080点，奇数k的一圈重复追踪不增加花瓣数；不使用重复填充制造假交集。']
 elif s=='sunflower':
  for n in range(800):
   r=9.5*math.sqrt(n);t=n*GOLDEN;x,y=polar(700,490,r,t);p.circle(x,y,2.2+2.2*n/799,COLORS[n%3])
  p.notes=['800 个点以黄金角与平方根半径排列，形成均匀而有节奏的盘面。',f'黄金角π(3−√5)={GOLDEN*180/math.pi:.6f}°；第n点r=9.5√n、θ=nα，n=0..799；点半径2.2+2.2n/799，不标未经计数验证的21/34螺旋。']
 elif s=='spiral-composition':
  for j in range(7):
   pts=[polar(700,490,13*t,t+j*2*math.pi/7) for t in [i*18/1000 for i in range(1001)]];p.draw(path(pts),stroke=COLORS[j%5],sw=2)
  p.notes=['七条阿基米德螺旋围绕共同中心展开，疏密变化成为构图。','r=13θ，θ=0..18，每条1001点，初始相位2πj/7；非对数螺旋，不宣称黄金比例。']
 elif s=='wave-superposition':
  for j in range(31):
   pts=[(100+x,490+(j-15)*13+45*math.sin(x/125+j*.13)+22*math.sin(x/51-j*.09)) for x in range(0,1201,4)];p.draw(path(pts),stroke=COLORS[j%5],sw=1.8)
  p.notes=['两种频率叠加的平行曲线，以相位差形成层叠波纹。','x=0..1200步长4；y=490+(j−15)13+45sin(x/125+j0.13)+22sin(x/51−j0.09)，j=0..30；艺术曲线不是音频实测信号。']
 elif s=='lissajous-curves':
  for j,(a,b) in enumerate([(2,3),(3,4),(5,6)]):
   pts=[(270+j*430+163*math.sin(a*t+math.pi/2),490+205*math.sin(b*t)) for t in [2*math.pi*i/1600 for i in range(1601)]];p.draw(path(pts),stroke=COLORS[j],sw=2.2);p.text(270+j*430,745,f'{a}:{b}',18,'#aabfd5','middle')
  p.notes=['整数频率比让两轴振荡闭合成不同的曲线轮廓。','x=cx+163sin(at+π/2)，y=490+205sin(bt)，t=0..2π共1601点；比值2:3/3:4/5:6。']
 elif s=='flow-field':
  for j,pts in enumerate(flow_lines()):p.draw(path(pts),stroke=COLORS[j%5],sw=1.8)
  p.notes=['确定性的流场线迹，连续方向变化组织画面中的流动感。','方向a(x,y)=0.65sin(x/200)cos(y/175)+0.12sin(y/110)；38起点(83,215+15j)，中点积分步长4，最多390步，越界终止。不是流体力学仿真。']
 elif s=='voronoi-tessellation':
  pts=seeds()
  for j,poly in enumerate(cells(pts)):p.draw(path(poly,True),COLORS[j%5],'#101d2d',3)
  for x,y in pts:p.circle(x,y,3,'#101d2d')
  p.notes=['每块区域归属于最近的种子点，边界由距离关系决定。','24种子，Random(41)，6×4网格加固定随机偏移；每个单元与所有两点垂直平分线半平面相交，裁切边界80..1320/210..780，非随手画的多边形。']
 elif s=='triangulated-art':
  for j,tri in enumerate(triangles()):
   cx=sum(t[0] for t in tri)/3;cy=sum(t[1] for t in tri)/3;idx=int((cx/200+cy/160))%5;p.draw(path(tri,True),COLORS[idx],'#101d2d',1)
  p.notes=['低多边形色面组成完整网格，点位与对角线均可复现。','11×6点格，x=80+124col、y=210+114row，内部Random(19)偏移x±28/y±24；50四边单元按行列奇偶交替对角线生成100三角面；不称Delaunay三角剖分。']
 elif s=='moire-patterns':
  for cx,col in [(650,'#75ddcf'),(750,'#819af8')]:
   for i in range(1,50):p.circle(cx,490,i*8,stroke=col,sw=1.25)
  p.notes=['两组错位同心线叠加产生干涉纹，疏密来自真实线条交叠。','两组中心(650,490)/(750,490)，半径8..392步长8，各49环，线宽1.25；非光学波动模拟，缩略图与设备采样可能改变纹样。']
 elif s=='fractal-tree':
  p.time='css'
  for x,y,xx,yy,depth in tree_segments():
   p.draw(f'M{x:.3f} {y:.3f}L{xx:.3f} {yy:.3f}',stroke=COLORS[0] if depth>4 else '#8ba9bc',sw=max(.7,12*.7**depth),extra=f'class="grow" pathLength="1" stroke-dasharray="1" style="animation:grow .7s ease-out {depth*.35:.2f}s backwards"')
  p.notes=['递归分形树将静态轮廓与一次生长呈现合为一个作品。','9层、511枝，主干(700,760)、长度155、方向−π/2，每层分叉±0.43弧度、长度×0.72；线宽max(0.7,12×0.7^depth)。CSS每层延迟depth×0.35s、.7s描边生长一次，终态完整；CSS失效及减少动效直接显示全部枝干。']
 elif s=='iso-cubes':
  for j,(x,y,size) in enumerate([(250,445,110),(620,350,170),(1030,505,85)]):
   wx=size*math.sqrt(3)/2;wy=size*.5;p.draw(f'M{x} {y}l{wx} {wy} {wx} {-wy} {-wx} {-wy}Z',COLORS[j]);p.draw(f'M{x} {y}v{size}l{wx} {wy}v{-size}Z','#4e8195');p.draw(f'M{x+wx} {y+wy}v{size}l{wx} {-wy}v{-size}Z','#2e546f')
  p.notes=['三种尺度的等距体块，以面明度和错落位置建立空间节奏。','三轴投影使用水平±30°与垂直轴，三个面共用顶点；尺寸110/170/85，真正等距立方体，SVG表现仍归2D。']
 elif s in ['shape-morph','blob-morph']:
  p.time='smil';kind='geometric' if s=='shape-morph' else 'organic';shapes=morph_shapes(kind);ds=[path(pts,True) for pts in shapes];p.add(f'<path class="motion" d="{ds[0]}" fill="url(#ink)"><animate attributeName="d" values="{";".join(ds+[ds[0]])}" dur="12s" repeatCount="indefinite" calcMode="linear"/></path>');p.draw(ds[0],'url(#ink)',extra='class="snapshot"');p.circle(700,490,285,stroke='#294258',sw=1)
  p.notes=['共同顶点骨架保持形变连续；减少动效显示完整的第一状态。','96个等角度顶点，从−π/2起，所有状态共用M+95L+Z；12秒循环3状态并回初态。'+('方形r=180/max(|cosθ|,|sinθ|)，圆r=180，菱形r=235/(|cosθ|+|sinθ|)，闭合折线近似。' if kind=='geometric' else '有机轮廓r=200(1+0.13sin(3θ+φ)+0.08cos(5θ−φ))，φ=0/2π÷3/4π÷3，正半径不自交；无装饰巡游点。')]
 else:raise ValueError(s)
def build():
 for i,(slug,title,en) in enumerate(ENTRIES,1):
  p=Plate(slug,title,en,i);render(p);p.finish()
 print('Built 18 geometric art specimens.')
if __name__=='__main__':build()
