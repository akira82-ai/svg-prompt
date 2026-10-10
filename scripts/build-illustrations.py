#!/usr/bin/env python3
"""Curated vector editorial scenes; all geometry is deterministic and standalone."""
from pathlib import Path
from html import escape
import json, math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'gallery/illustrations'
ENTRIES=[('human-ai','人机协作','Human–AI Collaboration'),('knowledge-discovery','知识探索','Knowledge Discovery'),('cloud-computing','云端计算','Cloud Computing'),('data-security','数据安全','Data Security'),('creative-workspace','创意工作室','Creative Workspace'),('robot-assistant','机器人助手','Robot Assistant'),('line-drawing','航天探索','Space Exploration'),('hologram','全息投影','Holographic Projection'),('energy-core','未来能源装置','Future Energy Device'),('cyber-city','未来城市','Future City'),('tech-campus','等距科技园区','Isometric Tech Campus'),('sunrise-scene','山间日出','Mountain Sunrise'),('snow-globe','冬日雪景球','Winter Snow Globe'),('campfire','林间篝火','Forest Campfire'),('sticker-pack','科技主题贴纸','Technology Stickers')]
DARK={'line-drawing','hologram','energy-core','cyber-city','campfire'}
class Scene:
 def __init__(self,slug,title,en,order):
  self.slug,self.title,self.en,self.order=slug,title,en,order;self.a=[];self.notes=[];self.anim=False;self.dark=slug in DARK;self.ink='#e5efff' if self.dark else '#19344c';self.bg='#101e30' if self.dark else '#edf2f5';self.accent='#70dddf' if self.dark else '#245ee8'
  self.rect(0,0,1400,900,self.bg);self.text(64,65,'VECTOR STORIES / '+f'{order:02}',14);self.text(64,117,title,34);self.text(1336,117,en,20,'end');self.add('<defs><radialGradient id="halo"><stop stop-color="#70dddf" stop-opacity=".45"/><stop offset="1" stop-color="#70dddf" stop-opacity="0"/></radialGradient><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#b7d2eb"/><stop offset="1" stop-color="#f4d8b4"/></linearGradient><clipPath id="stage"><rect x="64" y="190" width="1272" height="620" rx="20"/></clipPath></defs><g clip-path="url(#stage)">')
 def add(self,s):self.a.append(s)
 def rect(self,x,y,w,h,c,rx=0,extra=''):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}" {extra}/>')
 def path(self,d,c='none',stroke='none',sw=2,extra=''):self.add(f'<path d="{d}" fill="{c}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
 def circle(self,x,y,r,c,extra=''):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" {extra}/>')
 def ellipse(self,x,y,rx,ry,c,extra=''):self.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" {extra}/>')
 def text(self,x,y,t,size=18,anchor='start',c=None):self.add(f'<text x="{x}" y="{y}" fill="{c or self.ink}" font-size="{size}" text-anchor="{anchor}">{escape(t)}</text>')
 def line(self,x,y,xx,yy,c=None,sw=3):self.path(f'M{x} {y}L{xx} {yy}',stroke=c or self.ink,sw=sw)
 def screen(self,x,y,w,h):
  self.rect(x,y,w,h,'#19344c',16);self.rect(x+12,y+12,w-24,h-30,'#dce8fa',8);self.line(x+w/2,y+h,x+w/2,y+h+30);self.line(x+w*.3,y+h+30,x+w*.7,y+h+30)
 def person(self,x,y,scale=1):
  self.add(f'<g transform="translate({x} {y}) scale({scale})">');self.circle(0,0,28,'#d4a47e');self.path('M-27-6Q-32-42 8-33Q34-32 28-4L11-12-2-17Z','#19344c');self.path('M-30 44Q0 25 30 44L44 146H-50Z','#245ee8');self.path('M-31 60L-66 112 30 125',stroke='#d4a47e',sw=20);self.path('M-30 146L-44 230H-6L8 146M10 146L25 230H60L36 146','#19344c');self.add('</g>')
 def robot(self,x,y,size=1):
  self.add(f'<g transform="translate({x} {y}) scale({size})">');self.line(0,-70,0,-43,'#245ee8',4);self.circle(0,-73,7,'#ef9e58');self.rect(-58,-43,116,87,'#c8d9ea',24);self.rect(-43,-23,86,40,'#19344c',15);self.circle(-20,-3,6,'#70dddf');self.circle(20,-3,6,'#70dddf');self.path('M-22 27h44',stroke='#19344c',sw=3);self.rect(-45,55,90,100,'#fff',20);self.circle(0,99,18,'#245ee8');self.path('M-45 80L-80 125M45 80L83 56',stroke='#8caac4',sw=17);self.line(-24,155,-24,192,'#19344c',14);self.line(24,155,24,192,'#19344c',14);self.add('</g>')
 def book(self,x,y,w=150):
  self.path(f'M{x} {y}q{w/4} -24 {w/2} 0q{w/4} -24 {w/2} 0v100q{-w/4} -24 {-w/2} 0q{-w/4} -24 {-w/2} 0Z','#fff','#19344c',3);self.line(x+w/2,y,x+w/2,y+100,'#19344c',2)
 def tree(self,x,y,h,c):
  self.rect(x-5,y-h*.15,10,h*.15,'#5b676a');self.path(f'M{x} {y-h}L{x-h*.35} {y}H{x+h*.35}Z',c)
 def iso(self,x,y,w,d,h,c):
  dx=d*.866;dy=d*.5;wx=w*.866;wy=w*.5
  self.path(f'M{x} {y}l{wx} {wy} {dx} {-dy} {-wx} {-wy}Z',c)
  self.path(f'M{x} {y}v{h}l{wx} {wy}v{-h}Z','#8da7c3')
  self.path(f'M{x+wx} {y+wy}v{h}l{dx} {-dy}v{-h}Z','#41658a')
 def breathe(self,x,y,r):
  self.anim=True;self.circle(x,y,r,'none',extra='class="pulse" stroke="#70dddf" stroke-width="2" opacity=".3"')
 def finish(self):
  self.add('</g>');self.text(64,857,self.notes[0],16,c='#b3c5da' if self.dark else '#526778');self.add('<style>@keyframes breathe{50%{opacity:.6}}.pulse{animation:breathe 6s ease-in-out infinite}@keyframes drift{50%{transform:translateY(6px)}}.drift{animation:drift 8s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.pulse,.drift{animation:none}}</style>')
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">{self.title} / {self.en}</title><desc id="desc">{escape("；".join(self.notes))}</desc>'+''.join(self.a)+'</svg>\n'
  d=OUT/self.slug;d.mkdir(exist_ok=True);old=json.loads((d/'meta.json').read_text()) if (d/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
  old.update(slug=self.slug,title=self.title,order=self.order,space='2d',time='css' if self.anim else 'static',tech=['path','clipPath','CSS ambient motion' if self.anim else 'vector illustration'],description=self.notes[0]);(d/'meta.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n');(d/'index.svg').write_text(svg)
  # Include the actual scene geometry so the prompt remains reproducible rather than generic.
  (d/'prompt.md').write_text(f'# {self.title} / {self.en}\n\n分类：[插画与场景](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n用SVG绘制“{self.title} / {self.en}”。\n- 1400×900画布，背景{self.bg}，正文{self.ink}，强调色{self.accent}；中英文标题，主体裁切在x64..1336、y190..810圆角区域。\n'+''.join('- '+n+'\n' for n in self.notes)+'- 本作品为概念插画，不是科学仿真、地图或可操作界面。\n- 动效只改变装饰层，不隐藏主体；CSS失效时静态画面完整；prefers-reduced-motion禁用动画。\n- 以下为可复现的完整SVG几何与色彩参考，可直接保存查看，也可据此改写构图：\n'+svg+'```\n')
def render(s):
 k=s.slug
 if k=='human-ai':
  s.ellipse(700,745,430,35,'#d3e0e9');s.circle(735,415,240,'#dce8fa');s.screen(530,355,280,190);s.book(570,375,120);s.rect(430,600,540,20,'#19344c');s.rect(475,620,16,125,'#8da7c3');s.rect(911,620,16,125,'#8da7c3');s.person(375,430,1.15);s.robot(980,473,1.15);s.path('M814 445Q930 340 996 414',stroke='#245ee8',sw=3,extra='stroke-dasharray="7 9"');s.notes=['人负责目标与判断，助手参与整理资料；桌面与共享文档成为画面中心。','左侧人物、右侧机器人、中央资料屏幕与开放书页；蓝色虚线是协作隐喻，不表示系统数据流。']
 elif k=='knowledge-discovery':
  s.circle(700,486,270,'#dce8fa');s.book(400,540,540)
  for x,y,c in [(445,340,'#d6a16e'),(670,270,'#245ee8'),(930,360,'#3d8c79')]:
   s.rect(x,y,125,155,c,10)
   for j in range(3):s.line(x+20,y+45+j*23,x+95,y+45+j*23,'#fff',3)
  s.circle(900,535,85,'#fff',extra='stroke="#19344c" stroke-width="12"');s.line(960,595,1025,660,'#19344c',22);s.notes=['从分散资料到新的理解，用书页、资料卡与放大镜表达探索。','展开的书居下，三个不同色资料卡悬于上方，右前景放大镜；不绘制假装真实的研究数据。']
 elif k=='cloud-computing':
  s.ellipse(700,735,390,32,'#d3e0e9');s.path('M470 440C350 440 340 300 460 295C485 175 690 180 710 290C830 205 985 295 945 385C1070 420 995 495 900 495H490Z','#fff','#8da7c3',4)
  for i in range(3):
   x=400+i*245;s.rect(x,570,190,135,'#19344c',12)
   for j in range(3):s.rect(x+15,585+j*35,160,25,'#41658a',4);s.circle(x+155,598+j*35,4,'#70dddf')
   s.line(x+95,505,x+95,558,'#245ee8',3)
  s.notes=['云端资源与地面计算节点形成稳定的上下层次。','白色云体在上，三组机架在下，以竖直连接线组织构图；并非部署架构。']
 elif k=='data-security':
  s.circle(700,470,270,'#dce8fa');s.path('M700 260L900 340V485Q900 650 700 740Q500 650 500 485V340Z','#245ee8');s.rect(625,445,150,130,'#fff',14);s.path('M654 445V399a46 46 0 0 1 92 0v46',stroke='#fff',sw=17);s.circle(700,490,13,'#19344c');s.line(700,502,700,531,'#19344c',9)
  for x,y in [(330,370),(1035,350),(1010,650)]:s.rect(x,y,95,115,'#fff',8);s.line(x+18,y+33,x+76,y+33,'#8da7c3',4);s.line(x+18,y+57,x+65,y+57,'#8da7c3',4)
  s.notes=['盾牌、锁与资料块表达保护概念，不暗示具体安全认证。','中心蓝盾牌与白锁，外围三份文档，轮廓清晰且不用警报闪烁。']
 elif k=='creative-workspace':
  s.rect(185,240,1030,470,'#e0e8ef',20);s.rect(255,280,240,245,'#fff',8);s.circle(330,355,36,'#efa76e');s.path('M270 500L372 387 464 500Z','#3d8c79');s.screen(545,335,350,230)
  for i,c in enumerate(['#245ee8','#70b5ae','#efa76e']):s.rect(580+i*85,375,65,145,c,8)
  s.rect(210,620,995,24,'#19344c');s.rect(250,644,18,150,'#8da7c3');s.rect(1150,644,18,150,'#8da7c3');s.book(465,590,195);s.rect(1000,535,65,80,'#fff',8);s.line(1070,350,1120,535,'#19344c',8);s.path('M1020 350h110l-30-65h-50Z','#245ee8');s.notes=['创意工作的桌面叙事：图形、色彩与资料共同参与创作。','墙上几何海报、中央设计屏、桌边书页和台灯；以大色块而非细碎界面吸引视线。']
 elif k=='robot-assistant':
  s.circle(660,468,270,'#dce8fa');s.ellipse(660,745,260,32,'#d3e0e9');s.robot(660,435,1.55);s.rect(930,320,215,150,'#fff',24);s.path('M945 470l-20 34 64-34','#fff');s.path('M970 395l30 30 69-70',stroke='#3d8c79',sw=9);s.notes=['机器人助手以温和的姿态和完成反馈表达协助。','主角面部为深色屏和青色眼睛，抬手指向勾选气泡；静态完成画面无拟真能力宣称。']
 elif k=='line-drawing':
  for i in range(35):s.circle(100+(i*137)%1200,220+(i*73)%420,1.5,'#91abc9')
  s.circle(1020,395,140,'#41658a');s.ellipse(1020,395,230,45,'none',extra='stroke="#8da7c3" stroke-width="9" transform="rotate(-18 1020 395)"');s.path('M130 795Q390 560 645 486',stroke='#41658a',sw=3,extra='stroke-dasharray="8 12"')
  s.add('<g transform="translate(600 420) rotate(30)">');s.path('M0-160Q100-50 60 120H-60Q-100-50 0-160Z','#e5efff','#8da7c3',4);s.path('M-60 60L-120 145H-52M60 60L120 145H52','#245ee8');s.circle(0,-25,35,'#245ee8',extra='stroke="#19344c" stroke-width="9"');s.path('M-38 125Q0 280 38 125Z','#efa76e');s.add('</g>');s.notes=['探索主题的完整插画：火箭、轨迹与远方行星形成方向感。','倾斜火箭位于左中，带环行星在右，星点使用确定性位置；删去代码卡，不表现真实轨道。']
 elif k=='hologram':
  s.ellipse(700,710,310,60,'#203950');s.ellipse(700,700,250,40,'none',extra='stroke="#70dddf" stroke-width="3"');s.path('M480 700L540 365H860L920 700Z','#70dddf',extra='opacity=".06"');s.circle(700,442,210,'url(#halo)');s.circle(700,442,155,'none',extra='stroke="#70dddf" stroke-width="3"')
  for rx in [50,105,150]:s.ellipse(700,442,rx,155,'none',extra='stroke="#70dddf" stroke-opacity=".55" stroke-width="2"')
  for ry in [45,100]:s.ellipse(700,442,155,ry,'none',extra='stroke="#70dddf" stroke-opacity=".55" stroke-width="2"')
  s.breathe(700,442,170);s.notes=['投影底座、光束与线框球形成完整设备场景。','球体为抽象线框而非地理地图；仅外圈透明度6秒缓变，主体不闪烁、不扫描遮挡。']
 elif k=='energy-core':
  s.ellipse(700,748,300,36,'#203950');s.rect(460,675,480,60,'#41658a',12);s.path('M485 665L540 290H860L915 665Z','#203950','#8da7c3',4);s.circle(700,465,190,'url(#halo)');s.circle(700,465,90,'#70dddf');s.ellipse(700,465,150,55,'none',extra='stroke="#8da7c3" stroke-width="9" transform="rotate(-30 700 465)"');s.ellipse(700,465,150,55,'none',extra='stroke="#8da7c3" stroke-width="9" transform="rotate(30 700 465)"')
  for x in [510,890]:s.rect(x-15,370,30,190,'#41658a',6)
  s.rect(625,620,150,30,'#101e30',5);s.line(645,635,755,635,'#70dddf',3);s.breathe(700,465,115);s.notes=['未来能源装置有支架、壳体和底座，发光核心只是结构的一部分。','青色核心被交叉固定环包围，外围支柱与仪表条构成设备；非能源工程设计，光环透明度6秒缓变。']
 elif k=='cyber-city':
  s.rect(64,190,1272,620,'#14283f');s.circle(1080,300,58,'#d8e5f6')
  for layer,(base,col) in enumerate([(660,'#25415b'),(770,'#355776')]):
   for i in range(10):
    x=70+i*135+layer*35;h=140+(i*73)%220;s.rect(x,base-h,100,h,col)
    if layer:
     for a in range(3):
      for b in range(int(h/32)-1):s.rect(x+15+a*27,base-h+20+b*32,10,14,'#77b9c0' if (a+b+i)%4 else '#efbb80')
  s.path('M60 755Q650 620 1340 700L1340 810H60Z','#101e30');s.path('M70 785Q650 650 1340 730',stroke='#70dddf',sw=4);s.path('M200 755Q650 660 1250 722',stroke='#efbb80',sw=2);s.rect(480,696,140,24,'#c8d9ea',12);s.notes=['未来城市以远近楼群、交通弧线与月光建立空间层次。','两层错落楼群、稳定窗灯、前景高架与列车；不依赖霓虹文字和随机闪光，精选入口保留原路径。']
 elif k=='tech-campus':
  s.ellipse(700,740,490,45,'#d3e0e9');s.path('M210 535L700 250 1220 545 735 825Z','#dce8fa');s.path('M365 655L855 373M540 760L1030 477',stroke='#fff',sw=28);s.iso(380,410,170,140,190,'#fff');s.iso(720,350,200,140,250,'#c8d9ea');s.iso(750,610,200,100,85,'#3d8c79')
  for i in range(4):s.tree(315+i*70,685-i*40,70,'#3d8c79')
  s.notes=['等距科技园区用建筑、通路和绿化组织空间，不承担地图导航。','建筑投影共用30度轴，竖向保持垂直，三个不同高度体块构成园区；几何等距表现归2D。']
 elif k=='sunrise-scene':
  s.rect(64,190,1272,620,'url(#sky)');s.circle(850,425,105,'#f6c582');s.path('M64 635L360 350 530 565 745 370 1040 640 1336 465V810H64Z','#91abb5');s.path('M64 760L445 480 670 690 935 540 1336 760V810H64Z','#4d7880');s.path('M64 790Q380 710 680 790T1336 755V810H64Z','#244f5b');s.add('<g class="drift" opacity=".8">');s.ellipse(320,330,100,15,'#fff');s.ellipse(1120,280,130,17,'#fff');s.add('</g>');s.anim=True;s.notes=['日出已经成立的静态构图，只有云层作缓慢的轻微漂移。','暖色太阳位于远山之后、近山之前，三层山体由浅到深；云层8秒上下6px，不循环昼夜变色。']
 elif k=='snow-globe':
  s.circle(700,465,270,'#dce8fa',extra='stroke="#8da7c3" stroke-width="5"');s.add('<defs><clipPath id="globe"><circle cx="700" cy="465" r="264"/></clipPath></defs><g clip-path="url(#globe)">');s.path('M420 650Q700 520 980 650V750H420Z','#fff');s.tree(520,635,180,'#3d8c79');s.tree(865,650,220,'#41658a');s.rect(625,520,145,115,'#c58d70');s.path('M605 520L697 425 790 520Z','#fff');s.rect(677,567,37,68,'#19344c');s.rect(636,548,24,25,'#efbb80');s.add('<g class="drift">')
  for i in range(32):s.circle(460+(i*97)%480,225+(i*61)%420,2+i%3,'#fff')
  s.add('</g></g>');s.path('M520 730H880L925 790H475Z','#19344c');s.path('M490 410Q515 285 630 245',stroke='#fff',sw=8);s.anim=True;s.notes=['玻璃球中的冬日小屋，以高光、裁切与前后树木表达材质和深度。','雪粒只在球内8秒轻移6px，球体不摇摆；雪屋、松树、底座在禁用动画时完整。']
 elif k=='campfire':
  s.rect(64,190,1272,620,'#13282d')
  for i in range(9):s.tree(110+i*150,755,280+(i*41)%180,'#1d3b3c')
  s.ellipse(700,738,260,35,'#0d1d25');s.circle(700,650,230,'url(#halo)');s.path('M565 720L815 760M585 765L825 720',stroke='#92694e',sw=30);s.path('M580 720Q550 610 665 500Q655 575 745 430Q840 590 830 690Q760 775 580 720Z','#d97645');s.path('M625 724Q605 650 720 540Q695 635 770 600Q805 760 625 724Z','#f2bb68');s.path('M674 724Q660 685 725 635Q760 735 674 724Z','#fff0c7');s.anim=True;s.circle(755,530,5,'#f2bb68',extra='class="pulse"');s.circle(630,485,4,'#f2bb68',extra='class="pulse"');s.notes=['森林剪影与暖色火焰形成冷暖对照，火光不依赖扰动滤镜。','三层火焰为固定贝塞尔轮廓，交叉木柴与地面阴影支撑主体；仅两颗火星6秒透明度缓变。']
 elif k=='sticker-pack':
  for i,(name,c) in enumerate([('CREATE','#245ee8'),('EXPLORE','#3d8c79'),('BUILD','#d97645'),('CONNECT','#41658a'),('LEARN','#6b4dc4'),('PROTECT','#19344c')]):
   x=170+i%3*435;y=255+i//3*290;s.add(f'<g transform="rotate({[-5,4,-3,3,-4,5][i]} {x+100} {y+95})">');s.rect(x-7,y-7,254,224,'#c8d9ea',40);s.rect(x,y,240,210,c,36,extra='stroke="#fff" stroke-width="10"');s.circle(x+120,y+70,37,'none',extra='stroke="#fff" stroke-width="4"')
   if i==0:s.path(f'M{x+100} {y+70}l20 -22 20 22-20 22Z',stroke='#fff',sw=4)
   elif i==2:s.path(f'M{x+98} {y+54}h44v32h-44Z M{x+110} {y+42}v12 M{x+130} {y+42}v12',stroke='#fff',sw=4)
   elif i==1:s.path(f'M{x+106} {y+83}l14 -34 14 34-14-8Z',stroke='#fff',sw=4)
   elif i==4:s.path(f'M{x+98} {y+54}q11 -8 22 0q11 -8 22 0v31q-11 -8-22 0q-11 -8-22 0Z M{x+120} {y+54}v31',stroke='#fff',sw=4)
   elif i==3:s.path(f'M{x+99} {y+70}h42 M{x+106} {y+56}v28 M{x+134} {y+56}v28',stroke='#fff',sw=4)
   else:s.path(f'M{x+120} {y+46}l20 8v15q0 17-20 27-20-10-20-27V{y+54}Z',stroke='#fff',sw=4)
   s.text(x+120,y+161,name,22,'middle','#fff');s.add('</g>')
  s.notes=['六枚科技主题贴纸组成可复用的小插画，不再重复品牌Logo套件。','统一白色贴纸边缘、偏移底影、轻微旋转；创造/探索/构建/连接/学习/保护六主题为概念符号，非印刷刀模。']
 else:raise ValueError(k)
def build():
 for i,(slug,title,en) in enumerate(ENTRIES,1):
  s=Scene(slug,title,en,i);render(s);s.finish()
 print('Built 15 illustration scenes.')
if __name__=='__main__':build()
