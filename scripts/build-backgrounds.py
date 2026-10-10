#!/usr/bin/env python3
"""Build reusable background studies with complete static base layers."""
from pathlib import Path
from html import escape
import math,json,random
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'gallery/backgrounds'
ENTRIES=[('grainy-gradient','颗粒渐变','Grainy Gradient'),('transparency-blend','透明色层','Translucent Layers'),('gradient-spheres','柔光球体背景','Soft Sphere Background'),('spotlight-scan','环境聚光','Ambient Spotlight'),('pattern-tile','科技网格','Technical Grid'),('pattern-fill','几何平铺','Geometric Pattern'),('fabric','织物纹理','Woven Fabric'),('carbon-fiber','碳纤维编织','Carbon Fiber Weave'),('frosted-glass','磨砂玻璃','Frosted Glass'),('filter-materials','液态金属','Liquid Metal'),('brushed-metal','拉丝金属','Brushed Metal'),('gold','金色镜面','Gold Reflection'),('rusted-iron','锈蚀金属','Weathered Metal'),('marble','大理石纹理','Marble Veins'),('concrete','混凝土纹理','Concrete Texture'),('kraft-paper','牛皮纸纤维','Kraft Paper'),('wood-grain','木纹层理','Wood Grain'),('water-drop','叶面水滴','Leaf Droplets'),('starry-sky','程序化星空','Procedural Starfield'),('water-shimmer','水面波光','Water Shimmer'),('rain-ripples','雨滴涟漪','Rain Ripples'),('lava','熔岩裂隙','Lava Fissures'),('digital-rain','数据字符流','Digital Streams'),('confetti','庆祝粒子背景','Celebration Confetti')]
PALETTE=['#6ed4ca','#869cee','#d995b8','#e9b57e']
class Sample:
 def __init__(self,slug,title,en,order):
  self.slug,self.title,self.en,self.order=slug,title,en,order;self.a=[];self.notes=[];self.animated=False;self.rng=random.Random(29)
  self.rect(0,0,1400,900,'#111e2d');self.text(64,64,'SURFACE STUDIES / '+f'{order:02}',14,'#b5c7d9');self.text(64,116,title,34);self.text(1336,116,en,20,'#b5c7d9','end');self.add('<defs><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="18"/></clipPath></defs><g clip-path="url(#stage)">')
 def add(self,s):self.a.append(s)
 def rect(self,x,y,w,h,c,extra=''):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')
 def text(self,x,y,t,size=18,c='#e9f0fa',anchor='start'):self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" text-anchor="{anchor}">{escape(t)}</text>')
 def circle(self,x,y,r,c,extra=''):self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{c}" {extra}/>')
 def ellipse(self,x,y,rx,ry,c,extra=''):self.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" {extra}/>')
 def path(self,d,c='none',stroke='none',sw=2,extra=''):self.add(f'<path d="{d}" fill="{c}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
 def base(self,c):self.rect(64,190,1272,620,c)
 def gradient(self,id,colors,radial=False,coords=''):
  kind='radialGradient' if radial else 'linearGradient';coords=coords or ('cx=".35" cy=".3" r=".75" fx=".28" fy=".22"' if radial else 'x1="0" y1="0" x2="1" y2="1"');self.add(f'<defs><{kind} id="{id}" {coords}>'+''.join(f'<stop offset="{i/(len(colors)-1):.4f}" stop-color="{c}"/>' for i,c in enumerate(colors))+f'</{kind}></defs>')
 def noise(self,id,freq,color,alpha,octaves=3):
  h=color.lstrip('#');r,g,b=[int(h[i:i+2],16)/255 for i in [0,2,4]];matrix=f'0 0 0 0 {r} 0 0 0 0 {g} 0 0 0 0 {b} 1 0 0 0 0'
  self.add(f'<defs><filter id="{id}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}" seed="29" stitchTiles="stitch" result="noise"/><feColorMatrix in="noise" type="matrix" values="{matrix}"/></filter></defs>');self.rect(64,190,1272,620,color,extra=f'filter="url(#{id})" opacity="{alpha}"')
 def motion(self):self.animated=True
 def finish(self):
  self.add('</g>');self.text(64,856,self.notes[0],16,'#b5c7d9');self.add('<style>@keyframes drift{50%{transform:translate(0,12px)}}@keyframes shine{50%{opacity:.75}}.drift{animation:drift 10s ease-in-out infinite}.shine{animation:shine 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.drift,.shine{animation:none}}</style>')
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">{self.title} / {self.en}</title><desc id="desc">{escape("；".join(self.notes))}</desc>'+''.join(self.a)+'</svg>\n'
  d=OUT/self.slug;d.mkdir(exist_ok=True);old=json.loads((d/'meta.json').read_text());old.update(title=self.title,slug=self.slug,order=self.order,space='2d',time='css' if self.animated else 'static',description=self.notes[0],tech=['surface composition','SVG gradient','CSS ambient motion' if self.animated else 'standalone texture']);(d/'meta.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n');(d/'index.svg').write_text(svg)
  (d/'prompt.md').write_text(f'# {self.title} / {self.en}\n\n分类：[背景与材质](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n用SVG绘制“{self.title} / {self.en}”。\n- 展示画幅1400×900，外框#111e2d，文字#e9f0fa/辅助#b5c7d9；中英文名称与页脚在纹理区外，样张x64..1336、y190..810。\n'+''.join('- '+n+'\n' for n in self.notes)+'- 材质为矢量视觉模拟，不宣称物理渲染、材料性能或真实测量。背景使用时提取样张组并同步保留其defs，移除外框标题；只有pattern作品可以按单元无缝平铺，其余为固定构图。\n- 动效只用于装饰，8–10秒缓变，无闪烁和主体遮挡；减少动效禁用CSS动画，静态基底完整；滤镜不支持时质感会简化。\n- 生成器scripts/build-backgrounds.py记录构造，完整SVG参考：\n'+svg+'```\n')
def render(p):
 s=p.slug
 if s=='grainy-gradient':
  p.gradient('g',['#224b88','#776aad','#dc9a92']);p.base('url(#g)');p.noise('grain','.7','#102039',.14,3);p.notes=['细颗粒为渐变增加层次，标题区独立保证可读性。','渐变224b88→776aad→dc9a92，叠fractalNoise频率0.7、octaves3、seed29，深色颗粒透明度0.14；不声称消除AI味或保证消除色带。']
 elif s=='transparency-blend':
  p.base('#e8edf2')
  for x,y,c in [(540,450,'#da7996'),(810,450,'#5d9ec6'),(670,640,'#71bfa3')]:p.circle(x,y,235,c,extra='fill-opacity=".55"')
  p.notes=['透明色层在浅底叠出有顺序的混色，不把透明度当特殊混合模式。','三圆半径235，粉/蓝/绿按此顺序source-over叠加opacity0.55；颜色结果依赖图层顺序与底色。']
 elif s=='gradient-spheres':
  p.base('#172b43')
  for j,(x,y,r,cols) in enumerate([(390,480,190,['#c1e6ed','#5faac0','#234764']),(850,390,125,['#eadffc','#899bea','#37467c']),(1030,670,100,['#ffe9cb','#dbab7b','#775344'])]):
   p.gradient('ball'+str(j),cols,True);p.ellipse(x,y+r+20,r*.85,r*.15,'#102039');p.circle(x,y,r,'url(#ball'+str(j)+')')
  p.notes=['偏移焦点与明暗层次构成柔光球体，留白可承接封面内容。','三球r190/125/100，径向渐变焦点(.28,.22)、中心(.35,.3)，每球有扁椭圆地面阴影；没有代码卡和焦点标注。']
 elif s=='spotlight-scan':
  p.gradient('spot',['#5c8194','#213c55','#122238'],True);p.base('#122238');p.rect(64,190,1272,620,'url(#spot)',extra='class="drift"');p.motion();p.notes=['大面积环境光为深色背景提供柔和的视觉中心。','偏移径向渐变以10秒上下12px缓移；没有隐藏内容和扫描交互，不声称聚光灯揭示文字。']
 elif s=='pattern-tile':
  p.base('#162b40');p.add('<defs><pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#355570" stroke-width="1"/><circle cx="0" cy="0" r="2" fill="#70b4c0"/><circle cx="80" cy="0" r="2" fill="#70b4c0"/><circle cx="0" cy="80" r="2" fill="#70b4c0"/><circle cx="80" cy="80" r="2" fill="#70b4c0"/></pattern></defs>');p.base('url(#grid)');p.notes=['克制的坐标网格适合技术封面与页面底图。','80×80单元，边线1px、交点半径2，四角复制避免切断；patternUnits=userSpaceOnUse，不承担数据坐标含义。']
 elif s=='pattern-fill':
  p.base('#e8dfc8');p.add('<defs><pattern id="tile" width="96" height="96" patternUnits="userSpaceOnUse"><rect width="96" height="96" fill="#e8dfc8"/><circle cx="48" cy="48" r="29" fill="none" stroke="#b2674f" stroke-width="8"/><path d="M0 0L12 0 0 12Z M96 0L84 0 96 12Z M0 96L12 96 0 84Z M96 96L84 96 96 84Z" fill="#29455e"/></pattern></defs>');p.base('url(#tile)');p.notes=['同一复古几何单元无缝重复，适合作包装与编辑底纹。','96×96奶油底、中心赭红环、四角藏蓝三角；跨单元四角拼接成菱形，不再与科技网格重复。']
 elif s=='fabric':
  p.base('#e9e3d7');p.add('<defs><pattern id="weave" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#e9e3d7"/><path d="M0 4H16M0 12H16" stroke="#cec6b7" stroke-width="3"/><path d="M4 0V16M12 0V16" stroke="#f8f4eb" stroke-width="3"/><path d="M0 4H8M8 12H16" stroke="#bfb6a5" stroke-width="2"/></pattern></defs>');p.base('url(#weave)');p.notes=['平纹织物用经纬交错的明暗表达柔软纤维。','16×16单元，经纬线宽3、局部覆盖宽2；明确为风格化平纹，不把斜线图案称作针织。']
 elif s=='carbon-fiber':
  p.base('#151e2a');p.add('<defs><pattern id="carbon" width="32" height="32" patternUnits="userSpaceOnUse"><rect width="32" height="32" fill="#111923"/><path d="M0 0H16V16H0Z M16 16H32V32H16Z" fill="#2c3e50"/><path d="M2 4H14M2 8H14M2 12H14M18 20H30M18 24H30M18 28H30" stroke="#42596c" stroke-width="1"/><path d="M20 2V14M24 2V14M28 2V14M4 18V30M8 18V30M12 18V30" stroke="#253546" stroke-width="1"/></pattern></defs>');p.base('url(#carbon)');p.notes=['深色编织纹通过交替方向与细线高光获得层次。','32px单元分四块、水平与垂直纤维交错；这是平纹编织的视觉示意，不宣称2×2斜纹或真实碳纤维结构。']
 elif s=='frosted-glass':
  p.base('#283b5e');p.add('<defs><g id="backdrop"><circle cx="430" cy="445" r="190" fill="#5eaac1"/><circle cx="990" cy="590" r="205" fill="#ad8cca"/><path d="M685 230L955 720H425Z" fill="#e7b17c"/></g><clipPath id="glass"><rect x="420" y="285" width="580" height="420" rx="28"/></clipPath><filter id="blur" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="18"/></filter></defs>');p.add('<use href="#backdrop"/><g clip-path="url(#glass)"><rect x="420" y="285" width="580" height="420" fill="#283b5e"/><use href="#backdrop" filter="url(#blur)"/><rect x="420" y="285" width="580" height="420" fill="white" fill-opacity=".22"/></g>');p.rect(420,285,580,420,'none',extra='rx="28" stroke="#fff" stroke-opacity=".6" stroke-width="2"');p.path('M452 329H947',stroke='#fff',sw=2,extra='opacity=".35"');p.notes=['同一底图在玻璃外清晰、玻璃内模糊，边缘与白幕共同表达磨砂。','复用backdrop两次；内部先铺不透明底色遮住原始清晰层，模糊第二份后再裁切glass，stdDeviation18，内部白幕0.22；滤镜范围150%避免截断。不是backdrop-filter，也不能自动模糊外部网页。']
 elif s=='filter-materials':
  p.base('#182536');p.gradient('chrome',['#20354b','#c9dce5','#4c6c86','#edf5f7','#28435a'],False,coords='x1="0" y1="0" x2=".8" y2="1"');p.path('M345 325C470 205 560 390 715 295C1005 135 1220 510 970 600C790 670 810 815 550 730C370 670 155 500 345 325Z','url(#chrome)');p.path('M390 330C525 280 530 445 735 330',stroke='#edf5f7',sw=7,extra='opacity=".75"');p.path('M900 600Q780 680 595 672',stroke='#91acbe',sw=5);p.notes=['液态轮廓与交替亮暗反射带表达金属质感。','单个闭合贝塞尔轮廓，多段线性渐变与两道高光，固定构图；不宣称metaball物理融合和真实光照。']
 elif s in ['brushed-metal','gold']:
  cols=['#647685','#dce4e8','#8c9fae','#f1f5f6','#697c8b'] if s=='brushed-metal' else ['#725328','#e7c37c','#fff1ba','#be8c3e','#f4d89b','#70512d'];p.gradient('metal',cols,coords='x1="0" y1="0" x2="1" y2=".2"');p.base('url(#metal)')
  if s=='brushed-metal':
   for i in range(230):
    y=192+i*2.7;p.path(f'M64 {y:.2f}H1336',stroke='#293f52' if i%3 else '#fff',sw=.5,extra=f'opacity="{.025+(i%7)*.005}"')
  p.notes=['定向高光与细纹形成拉丝金属的视觉质感。' if s=='brushed-metal' else '多段金色渐变形成镜面反射带，保留干净可用的材质面。','横向多段渐变色标：'+','.join(cols)+'；'+('230条水平细纹、.5px笔画、透明度0.025..0.055，未加铆钉道具。' if s=='brushed-metal' else '移除AURUM 24K刻字，不暗示材质纯度和实物性能。')]
 elif s=='rusted-iron':
  p.base('#454a4c');p.noise('iron','.025','#b06b3e',.8,4);p.noise('spots','.12','#29292b',.35,3)
  for i in range(40):
   x=p.rng.uniform(80,1320);y=p.rng.uniform(210,790);p.ellipse(x,y,p.rng.uniform(8,75),p.rng.uniform(5,35),'#ab643f',extra='opacity=".22"')
  p.path('M320 690L970 345',stroke='#aab5bc',sw=2);p.notes=['铁灰基底与暖色斑驳表达风化，而非整面橙色噪声。','底色454a4c，两层固定seed29的噪声，40个低透明度锈斑与一道浅刮痕；噪声是视觉模拟。']
 elif s=='marble':
  p.gradient('stone',['#eff1ed','#cfd9de','#f6f4ee']);p.base('url(#stone)')
  for i in range(14):
   pts=[(80+x,270+i*38+27*math.sin(x/150+i)+10*math.sin(x/41+i*.5)) for x in range(0,1241,8)];p.path('M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts),stroke='#67818e' if i%4 else '#b59b70',sw=1+(i%3)*.8,extra='opacity=".28"')
  p.noise('stonegrain','.04','#748b97',.08);p.notes=['冷白石面与连续细脉纹形成大理石的风格化层理。','14条双正弦采样脉纹，主色67818e、每四条点缀b59b70，透明度0.28；不是从普通云噪声直接声称静脉纹。']
 elif s=='concrete':
  p.base('#b2b5b0');p.noise('cloud','.014','#5f6968',.2,3);p.noise('fine','.5','#434e4c',.15,2)
  for i in range(100):p.circle(p.rng.uniform(80,1320),p.rng.uniform(210,790),p.rng.uniform(.6,3),'#5b6765',extra='opacity=".25"')
  p.notes=['混凝土由低频斑驳、细颗粒和小气孔构成，避免装饰裂纹喧宾夺主。','底色b2b5b0，噪声频率0.014/0.5、透明度0.2/0.15；100个固定种子气孔，半径0.6..3。']
 elif s=='kraft-paper':
  p.base('#c5ab7c');p.noise('paper','.65','#806442',.15,3);p.noise('stain','.02','#f2dfb3',.12,3)
  for i in range(140):
   x=p.rng.uniform(80,1320);y=p.rng.uniform(210,790);p.path(f'M{x:.2f} {y:.2f}l{p.rng.uniform(2,8):.2f} 1',stroke='#7e6849',sw=.6,extra='opacity=".16"')
  p.notes=['纸纤维与暖色斑点构成可用底纹，不附咖啡渍和道具。','底色c5ab7c，两层seed29噪声，140条稀疏短纤维；固定画幅不是毛边纸实物。']
 elif s=='wood-grain':
  p.gradient('wood',['#886447','#c19a6d','#846047']);p.base('url(#wood)')
  for i in range(90):
   pts=[(64+x,200+i*7+9*math.sin(x/175+i*.25)+4*math.sin(x/44)) for x in range(0,1273,8)];p.path('M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts),stroke='#513b2a',sw=.6+(i%4)*.2,extra='opacity=".23"')
  for y in [345,500,655]:p.path(f'M64 {y}H1336',stroke='#5b4533',sw=2,extra='opacity=".35"')
  p.notes=['连续纹线与板缝表达木材方向性，避免把噪声拉伸直接等同年轮。','90条横向双正弦纹线，3条板缝y345/500/655；暖棕渐变，明确为风格化木纹。']
 elif s=='water-drop':
  p.gradient('leaf',['#345f50','#67916b','#294e47']);p.base('url(#leaf)');p.path('M110 800L1220 220',stroke='#90af84',sw=4,extra='opacity=".4"')
  for i in range(9):p.path(f'M{160+i*125} {780-i*65}l-120 -165',stroke='#90af84',sw=2,extra='opacity=".25"')
  p.add('<defs><radialGradient id="drop"><stop offset="0" stop-color="#bce7d8" stop-opacity=".08"/><stop offset=".7" stop-color="#a3d4bc" stop-opacity=".12"/><stop offset="1" stop-color="#e3f5ef" stop-opacity=".5"/></radialGradient></defs>')
  for x,y,r in [(565,495,132),(915,400,55),(990,660,40)]:
   p.ellipse(x+10,y+r*.7,r,r*.4,'#193f36',extra='opacity=".35"');p.circle(x,y,r,'url(#drop)',extra='stroke="#cee7dc" stroke-width="1"');p.ellipse(x,y+r*.5,r*.5,r*.15,'#e3f5ef',extra='opacity=".55"');p.ellipse(x-r*.3,y-r*.4,r*.2,r*.12,'#fff',extra='opacity=".8"')
  p.notes=['叶脉、投影与局部高光表现水滴的透明体积。','三滴r132/55/40，各有渐变边缘、下部亮斑、左上高光与偏移投影；视觉模拟，不是光线追踪折射。']
 elif s=='starry-sky':
  p.gradient('night',['#14253e','#1c3f55','#111e2d']);p.base('url(#night)')
  for i in range(220):p.circle(p.rng.uniform(80,1320),p.rng.uniform(210,790),p.rng.uniform(.5,1.7),'#dcecf2',extra=f'opacity="{p.rng.uniform(.25,.9):.3f}"')
  for x,y in [(355,365),(970,430),(765,660)]:p.path(f'M{x-8} {y}h16M{x} {y-8}v16',stroke='#e9f0fa',sw=1.5)
  p.notes=['固定随机种子生成疏密有别的星点，保持整幅背景用途。','Random(29)生成220个星点，3颗十字亮星；显式几何点保证不支持滤镜时星空仍可见，没有天文方位含义。']
 elif s=='water-shimmer':
  p.gradient('water',['#173e54','#112c45','#172938']);p.base('url(#water)')
  for i in range(75):
   x=p.rng.uniform(95,1260);y=220+i*7.5;w=p.rng.uniform(15,95);p.path(f'M{x:.1f} {y:.1f}h{w:.1f}',stroke='#a8d7d7',sw=1.5,extra=f'opacity="{p.rng.uniform(.15,.5):.3f}" class="shine" style="animation-delay:-{i%8}s"')
  p.motion();p.notes=['深色水面上的稀疏短线形成波光，变化只作用于高光。','75条固定随机线段，长15..95；8秒opacity缓变至0.75，错开延迟，基底和高光始终存在，不作真实水面模拟。']
 elif s=='rain-ripples':
  p.base('#183347')
  for i in range(12):
   x=150+i%4*320+p.rng.uniform(-38,38);y=305+i//4*195+p.rng.uniform(-30,30)
   for j in range(3):p.ellipse(x,y,30+j*26,8+j*7,'none',extra=f'stroke="#70aebd" stroke-width="1.5" opacity="{.6-j*.15}" class="shine" style="animation-delay:-{i%8}s"')
  p.motion();p.notes=['椭圆涟漪形成静谧雨面，保留完整且低干扰的背景。','12组固定seed29、分层错位的三层椭圆，高光透明度8秒缓变；没有不同步的下落雨滴，不声称碰撞或真实扩散。']
 elif s=='lava':
  p.base('#29272b');p.noise('rock','.08','#111b24',.25)
  for i in range(11):
   x=120+i*116;pts=[]
   for j in range(11):
    x+=p.rng.uniform(-30,30);pts.append((x,210+j*57+p.rng.uniform(-7,7)))
   d='M'+' L'.join(f'{xx:.1f} {yy:.1f}' for xx,yy in pts);p.path(d,stroke='#a7513b',sw=9,extra='opacity=".35"');p.path(d,stroke='#e5a16a',sw=2.5,extra='class="shine"')
   for j in [3,7]:
    xx,yy=pts[j];dx=50 if i%2 else -50;p.path(f'M{xx:.1f} {yy:.1f}l{dx*.45:.1f} 19 {dx*.55:.1f} -9',stroke='#cf845b',sw=1.5,extra='class="shine"')
  p.motion();p.notes=['固定岩壳与暖色裂隙构成熔岩纹理，亮度缓变避免纹理跳变。','11条seed29随机游走裂隙，每条带2个分叉，宽外辉光9/内芯2.5；8秒透明度缓变，噪声seed固定29，删去seed步进闪动。']
 elif s=='digital-rain':
  p.base('#102b30');p.add('<g class="drift" font-family="Menlo, Consolas, monospace">')
  for i in range(22):
   for j in range(19):
    ch='0123456789ABCDEF'[(i*7+j*11)%16];p.text(95+i*57,215+j*32,ch,16,'#b4e5c8' if j==(i*3)%19 else ['#376a68','#4a8c82','#70b5a9'][(j+i)%3])
  p.add('</g>');p.motion();p.notes=['低对比字符流提供科技气氛，字符与速度不冒充实时数据。','22列19行十六进制字符，内容固定由索引生成，列首亮字符位置(i×3)%19，尾部三档明度，10秒垂直12px轻移；不依赖片假名字体，不采用闪烁随机字符。']
 elif s=='confetti':
  p.base('#edf1f4');p.add('<g class="drift">')
  for i in range(65):
   x=p.rng.uniform(90,1310);y=p.rng.uniform(210,790);col=PALETTE[i%4]
   while 510<x<890 and 340<y<650:x=p.rng.uniform(90,1310);y=p.rng.uniform(210,790)
   if i%3:p.rect(x,y,5,15,col,extra=f'rx="2" transform="rotate({i*37%180} {x} {y})"')
   else:p.circle(x,y,4,col)
  p.add('</g>');p.motion();p.notes=['疏朗的彩色粒子可作庆祝背景，中央留白不被爆炸效果占据。','Random(29)生成65个短条或圆点，固定静态分布，10秒上下12px轻移；没有重力仿真和无限爆发闪烁。']
 else:raise ValueError(s)
def build():
 for i,(slug,title,en) in enumerate(ENTRIES,1):
  p=Sample(slug,title,en,i);render(p);p.finish()
 print('Built 24 background and material studies.')
if __name__=='__main__':build()
