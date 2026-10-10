#!/usr/bin/env python3
"""Build the cinematic 7:3 vector atlas cover, using only local SVG geometry."""
from pathlib import Path
from html import escape
import math,random,json
ROOT=Path(__file__).resolve().parents[1]
W,H=2100,900
RNG=random.Random(7301)
PARTS=[]
TEXT=[]
def add(s):PARTS.append(s)
def path(d,fill='none',stroke='none',width=1,extra=''):add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def rect(x,y,w,h,c,extra=''):add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{c}" {extra}/>')
def circle(x,y,r,c,extra=''):add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{c}" {extra}/>')
def ellipse(x,y,rx,ry,c,extra=''):add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{c}" {extra}/>')
def line(x,y,xx,yy,c,width=1,extra=''):path(f'M{x:.2f} {y:.2f}L{xx:.2f} {yy:.2f}',stroke=c,width=width,extra=extra)
def text(x,y,s,size=14,c='#a4bdcb',extra=''):
 TEXT.append(s);add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{c}" {extra}>{escape(s)}</text>')
def poly(points,fill,stroke='none',width=1,extra=''):path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in points)+' Z',fill,stroke,width,extra)
def pos(t,u):
 # A point on the top deck: interpolate rear edge A..B toward the prow C.
 a=(345,535);b=(610,773);c=(1370,356)
 return ((1-t)*((1-u)*a[0]+u*b[0])+t*c[0],(1-t)*((1-u)*a[1]+u*b[1])+t*c[1])
def orbital(t):
 x=350*math.cos(t);y=119*math.sin(t);a=-.36
 return (1655+x*math.cos(a)-y*math.sin(a),285+x*math.sin(a)+y*math.cos(a))
def satellite(x,y,s=1,angle=0):
 add(f'<g transform="translate({x} {y}) rotate({angle}) scale({s})">');rect(-55,-12,40,24,'#264859',extra='stroke="#55798a"');rect(15,-12,40,24,'#264859',extra='stroke="#55798a"')
 for i in range(4):line(-50+i*9,-10,-50+i*9,10,'#7493a1',.7);line(20+i*9,-10,20+i*9,10,'#7493a1',.7)
 rect(-11,-18,22,36,'#a0b2b9',extra='rx="3"');line(0,-18,0,-38,'#adcbd3',2);circle(0,-39,3,'#e8b076');add('</g>')
def shuttle(x,y,s=1,angle=-19):
 add(f'<g transform="translate({x} {y})"><g class="shuttle-flight" style="--sx:{120+s*70:.2f}px;--sy:{-35-s*25:.2f}px;animation-duration:{18+s*12:.2f}s;animation-delay:-{(x+y)%17:.2f}s"><g transform="rotate({angle}) scale({s})">');poly([(-48,-9),(42,0),(-48,9),(-30,0)],'#83a5b4','#c0d0d4');rect(-21,-4,24,8,'#1b3748');ellipse(-50,0,12,4,'#87e5ed');line(-76,0,-56,0,'#79c5d8',2);add('</g></g></g>')
def build():
 PARTS.clear();TEXT.clear();RNG.seed(7301)
 add('''<defs>
 <linearGradient id="space" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#08111f"/><stop offset=".55" stop-color="#102337"/><stop offset="1" stop-color="#060e1a"/></linearGradient>
 <radialGradient id="nebula"><stop stop-color="#527a91" stop-opacity=".28"/><stop offset=".5" stop-color="#284962" stop-opacity=".13"/><stop offset="1" stop-color="#102337" stop-opacity="0"/></radialGradient>
 <radialGradient id="engine"><stop stop-color="#f0fbff"/><stop offset=".2" stop-color="#9be8f4" stop-opacity=".85"/><stop offset=".6" stop-color="#429dd0" stop-opacity=".2"/><stop offset="1" stop-color="#429dd0" stop-opacity="0"/></radialGradient>
 <linearGradient id="hull" x1="0" y1="1" x2=".9" y2="0"><stop stop-color="#345063"/><stop offset=".5" stop-color="#4d6878"/><stop offset="1" stop-color="#a9bdc4"/></linearGradient>
 <linearGradient id="side"><stop stop-color="#0b1c2a"/><stop offset=".55" stop-color="#254050"/><stop offset="1" stop-color="#172c3d"/></linearGradient>
 <radialGradient id="ocean" cx=".3" cy=".22" r=".95"><stop stop-color="#5c8d9c"/><stop offset=".5" stop-color="#1e485e"/><stop offset="1" stop-color="#102337"/></radialGradient>
 <radialGradient id="limb" cx=".27" cy=".26" r=".9"><stop stop-color="#06111b" stop-opacity="0"/><stop offset=".52" stop-color="#06111b" stop-opacity=".1"/><stop offset=".8" stop-color="#06111b" stop-opacity=".7"/><stop offset="1" stop-color="#030b16" stop-opacity=".99"/></radialGradient>
 <radialGradient id="atmosphere"><stop offset=".89" stop-color="#8bc0d2" stop-opacity="0"/><stop offset=".92" stop-color="#98cddd" stop-opacity=".18"/><stop offset=".96" stop-color="#85c6df" stop-opacity=".22"/><stop offset="1" stop-color="#85c6df" stop-opacity="0"/></radialGradient>
 <linearGradient id="glass" x2="1" y2="1"><stop stop-color="#234656" stop-opacity=".34"/><stop offset="1" stop-color="#122735" stop-opacity=".65"/></linearGradient>
 <linearGradient id="title-shade"><stop stop-color="#08111f" stop-opacity=".95"/><stop offset="1" stop-color="#08111f" stop-opacity="0"/></linearGradient>
 <clipPath id="planet-clip"><circle cx="1655" cy="285" r="224"/></clipPath>
 <clipPath id="hull-clip"><path d="M345 535L1370 356 610 773Z"/></clipPath>
 <clipPath id="frame"><rect width="2100" height="900"/></clipPath>
 <pattern id="hull-grain" width="12" height="8" patternUnits="userSpaceOnUse"><path d="M0 2H12M0 6H12" stroke="#c0d2d8" stroke-opacity=".06" stroke-width=".6"/></pattern>
 <filter id="terrain" filterUnits="userSpaceOnUse" x="0" y="0" width="900" height="440" color-interpolation-filters="sRGB">
 <feTurbulence type="fractalNoise" baseFrequency=".008 .012" numOctaves="5" seed="11" stitchTiles="stitch" result="noise"/>
 <feColorMatrix in="noise" type="matrix" values="0 0 0 0 .4 0 0 0 0 .45 0 0 0 0 .34 1 0 0 0 0" result="land"/>
 <feComponentTransfer in="land" result="mask"><feFuncA type="table" tableValues="0 0 0 0 .05 .7 1 1 1"/></feComponentTransfer>
 <feDiffuseLighting in="noise" surfaceScale="4" diffuseConstant="1.1" lighting-color="#9ba48b" result="relief"><feDistantLight azimuth="225" elevation="55"/></feDiffuseLighting>
 <feComposite in="relief" in2="mask" operator="in"/>
 </filter>
 <filter id="cloud-texture" filterUnits="userSpaceOnUse" x="0" y="0" width="900" height="440" color-interpolation-filters="sRGB">
 <feTurbulence type="fractalNoise" baseFrequency=".013 .025" numOctaves="4" seed="23" stitchTiles="stitch" result="noise"/>
 <feColorMatrix in="noise" type="matrix" values="0 0 0 0 .93 0 0 0 0 .98 0 0 0 0 1 4 0 0 0 -2.1"/><feGaussianBlur stdDeviation=".55"/>
 </filter>
 <filter id="bridge-shadow" x="-30%" y="-50%" width="170%" height="230%"><feGaussianBlur stdDeviation="5"/></filter>
 <filter id="metal-grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency=".025 .38" numOctaves="2" seed="19" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 .72 0 0 0 0 .8 0 0 0 0 .84 .12 0 0 0 0"/></filter>
 <linearGradient id="deck-light" x1="0" y1="1" x2=".7" y2="0"><stop stop-color="#071824" stop-opacity=".3"/><stop offset=".55" stop-color="#bbc5c9" stop-opacity=".06"/><stop offset="1" stop-color="#e9e5d8" stop-opacity=".25"/></linearGradient>
 <clipPath id="map-bounds"><rect width="900" height="440"/></clipPath><g id="map-tile" clip-path="url(#map-bounds)">''')
 # Continuous procedural land relief replaces decorative continent blobs.
 rect(0,0,900,440,'#677767',extra='filter="url(#terrain)"')
 for j in range(120):
  x=RNG.uniform(0,900);y=RNG.uniform(30,410)
  circle(x,y,RNG.uniform(.4,1.1),'#e8c28c',extra='opacity=".5"')
 add('</g><g id="cloud-tile" clip-path="url(#map-bounds)">')
 rect(0,0,900,440,'#fff',extra='filter="url(#cloud-texture)" opacity=".72"')
 add('</g></defs><g clip-path="url(#frame)">');rect(0,0,W,H,'url(#space)');ellipse(1390,480,800,430,'url(#nebula)',extra='transform="rotate(-17 1390 480)"');ellipse(820,200,610,240,'url(#nebula)')
 # Sparse stars and outward streaks all use one vanishing point.
 for i in range(250):circle(RNG.uniform(15,2085),RNG.uniform(15,885),RNG.uniform(.4,1.3),'#b8d1e0',extra=f'opacity="{RNG.uniform(.13,.58):.2f}"')
 for i in range(240):
  t=RNG.uniform(0,2*math.pi);r=RNG.uniform(170,1400);length=RNG.uniform(35,165)*(r/550);x=1300+r*math.cos(t);y=340+r*math.sin(t)
  if not (-120<x<2220 and -100<y<1000) or (x<850 and y<285):continue
  xx=x+length*math.cos(t);yy=y+length*math.sin(t);dx=190*math.cos(t);dy=190*math.sin(t)
  line(x,y,xx,yy,'#9cc5dd' if i%5 else '#d8e7eb',RNG.uniform(.55,1.45),extra=f'class="warp" data-vp="1300 340" style="--dx:{dx:.3f}px;--dy:{dy:.3f}px;animation-duration:{RNG.uniform(1.8,3.8):.2f}s;animation-delay:-{RNG.uniform(0,5):.2f}s" opacity=".5"')
 # Celestial navigation halo and orbital infrastructure, behind the planet.
 for r in [92,110,130]:ellipse(1290,350,r,r*.35,'none',extra='stroke="#6ca6b7" stroke-width="1" opacity=".22" transform="rotate(-20 1290 350)"')
 pts=[orbital(i*2*math.pi/240) for i in range(241)];path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts),stroke='#5c7e90',width=2,extra='opacity=".5"')
 for i in range(72):
  x,y=orbital(i*2*math.pi/72);x2,y2=orbital(i*2*math.pi/72+.016);line(x,y,x2,y2,'#a4c5cb',2)
 satellite(1932,200,.55,20);satellite(1440,420,.45,-15)
 circle(1655,285,244,'url(#atmosphere)');circle(1655,285,224,'url(#ocean)')
 add('<g clip-path="url(#planet-clip)"><g transform="translate(1205 65)"><g class="planet-spin"><use href="#map-tile"/><use href="#map-tile" x="900"/></g><g class="cloud-spin"><use href="#cloud-tile"/><use href="#cloud-tile" x="900"/></g></g></g>');circle(1655,285,224,'url(#limb)');circle(1655,285,225,'none',extra='stroke="#a2d3df" stroke-width="1.3" stroke-opacity=".38"');path('M1450 194A225 225 0 0 1 1697 64',stroke='#aedce7',width=2.7,extra='opacity=".45"')
 # A short near arc crosses the limb, with a visible docking hub.
 pts=[orbital(.18+i*.9/60) for i in range(61)];path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts),stroke='#acc5ce',width=3,extra='opacity=".6"');satellite(*orbital(.75),.8,-18)
 shuttle(1780,555,.42);shuttle(1818,573,.25);shuttle(1210,240,.33)
 # Transit wake and aft engines; all underneath the main hull.
 for i,(x,y) in enumerate([(375,571),(453,641),(530,711)]):
  ellipse(x-60,y+40,150,70,'url(#engine)',extra='transform="rotate(-25 '+str(x-60)+' '+str(y+40)+')" class="engine-breathe"');poly([(x-26,y-18),(x+15,y+20),(x-235,y+165),(x-250,y+139)],'#78cae7',extra='opacity=".035"');ellipse(x-25,y+13,48,18,'#213848',extra=f'transform="rotate(42 {x-25} {y+13})" stroke="#6e98ac" stroke-width="3"');ellipse(x-27,y+16,36,10,'#abedf4',extra=f'transform="rotate(42 {x-27} {y+16})"')
 # Hull: distinct dorsal deck, two side faces and armor geometry.
 poly([(345,535),(1370,356),(1377,377),(348,576)],'#334c5b','#54717f',1.5)
 poly([(610,773),(1370,356),(1377,377),(625,818)],'url(#side)','#385464',2)
 poly([(345,535),(348,576),(625,818),(610,773)],'#172c3d','#385464',2)
 poly([(345,535),(1370,356),(610,773)],'url(#hull)','#9ab4be',2)
 add('<g clip-path="url(#hull-clip)">')
 # Armor plates follow the deck projection; texture is integrated into these faces.
 for row in range(15):
  t0=.025+row*.062;t1=t0+.052
  for col in range(11):
   u0=.02+col*.088;u1=u0+.074;corners=[pos(t0,u0),pos(t1,u0),pos(t1,u1),pos(t0,u1)]
   fill=['#354b5b','#405666','#4e6573','#465e6c','#5b727f'][(row*3+col*7)%5];poly(corners,fill,'#213d50',.7,extra='data-role="armor-plate"');line(*corners[0],*corners[1],'#94acb7',.65,extra='opacity=".4"');line(*corners[2],*corners[3],'#142c3e',1.1)
   if (row+col)%9==0:
    a=pos((t0+t1)/2,u0+.01);b=pos((t0+t1)/2,u1-.01);line(*a,*b,'#94aebb',1,extra='opacity=".5"')
 poly([(345,535),(1370,356),(610,773)],'url(#hull-grain)');rect(345,356,1030,420,'#fff',extra='filter="url(#metal-grain)" opacity=".35"');poly([(345,535),(1370,356),(610,773)],'url(#deck-light)')
 # Two mirrored long hull conduits, a visual energy routing network.
 for u in [.23,.77]:
  points=[pos(t,u) for t in [.05,.19,.22,.45,.49,.72,.9]];path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in points),stroke='#142d40',width=7);path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in points),stroke='#75c5cd',width=1.3,extra='opacity=".7"')
 for t in [.19,.45,.72]:
  a=pos(t,.23);b=pos(t,.77);line(*a,*b,'#172f42',5);line(*a,*b,'#789bab',.8)
 # Maintenance hatches and radiator slits, scaled by perspective.
 for j in range(10):
  t=.12+j*.07;a=pos(t,.085);b=pos(t+.028,.14);line(*a,*b,'#162c3e',3*(1-t)+.5)
 add('</g>')
 # Thick starboard hull, with integrated bays, windows and a recovery lane.
 for i in range(24):
  t=.04+i*.037;x,y=pos(t,1);line(x+9,y+12,x+21*(1-t),y+24*(1-t),'#d7b581' if i%6==0 else '#739cab',1.5,extra='data-role="hull-window"')
 for i in range(4):
  t=.12+i*.13;x,y=pos(t,1);poly([(x+5,y+4),(x+54*(1-t),y-25*(1-t)),(x+57*(1-t),y-8*(1-t)),(x+10,y+21*(1-t))],'#091927','#4e7a90',1.3,extra='data-role="hangar"');line(x+12,y+7,x+44*(1-t),y-11*(1-t),'#9ee0e6',2)
 # Compact nested bridge tiers share the hull projection and cumulative elevation.
 decks=[]
 for t0,t1,u0,u1,bottom,top in [(.12,.39,.32,.68,0,16),(.15,.35,.36,.64,16,30),(.18,.31,.4,.6,30,43)]:
  footprint=[pos(t0,u0),pos(t1,u0),pos(t1,u1),pos(t0,u1)]
  decks.append((footprint,bottom,top))
 for points,bottom,top in decks:
  poly([(x+18,y+20) for x,y in points],'#06121c',extra='filter="url(#bridge-shadow)" opacity=".5" clip-path="url(#hull-clip)"')
 for j,(points,bottom,top) in enumerate(decks):
  base=[(x,y-bottom) for x,y in points];roof=[(x,y-top) for x,y in points]
  for k,c in [(1,'#193448'),(2,'#233e50'),(3,'#2e4b5b')]:
   n=(k+1)%4;poly([base[k],base[n],roof[n],roof[k]],c,'#557486',.8)
  poly(roof,['#78929e','#607e8e','#8fa7b1'][j],'#aec2c7',1.2,extra=f'data-role="bridge-roof" data-bottom="{bottom}" data-top="{top}"')
  for i in range(10):
   t=(i+1)/12;a=roof[0];b=roof[1];x=a[0]+t*(b[0]-a[0]);y=a[1]+t*(b[1]-a[1]);line(x,y+3,x+8,y+8,'#243e51',1.4)
  a=roof[2];b=roof[3]
  glass=[(a[0],a[1]+3),(b[0],b[1]+3),(b[0],b[1]+10),(a[0],a[1]+10)]
  poly(glass,'#122f44','#8dc8d6',.7)
  for i in range(1,8):
   t=i/8;x=a[0]+t*(b[0]-a[0]);y=a[1]+t*(b[1]-a[1]);line(x,y+3,x,y+10,'#7baebc',.7)
 # Short sensor masts are mounted on the upper roof rather than floating above it.
 for t,u,h in [(.21,.44,31),(.25,.5,23),(.28,.55,17)]:
  x,y=pos(t,u);y-=43;ellipse(x,y,7,3,'#344f60',extra='stroke="#9cb5bd"');line(x,y,x,y-h,'#91aebb',1.5);line(x-6,y-h+5,x+6,y-h+5,'#91aebb',1);circle(x,y-h,2,'#e3b87b')
 # Branching energy distribution on the lower deck is a physical conduit network.
 for j in range(5):
  t=.32+j*.087;x,y=pos(t,.53)
  circle(x,y,3.2,'#e5bf84')
  for u in [.43,.63]:
   xx,yy=pos(t+.014,u);line(x,y,xx,yy,'#9acdd2',1)
   poly([(xx-3,yy),(xx,yy-3),(xx+3,yy),(xx,yy+3)],'#acdce0')
 # A small docking crane remains on the aft deck.
 poly([(434,570),(474,552),(500,570),(461,594)],'#122c3f','#8aacbb');line(471,559,464,503,'#9cb5bd',3);line(464,503,497,487,'#9cb5bd',3);line(497,487,505,508,'#9cb5bd',2)
 # Engine manifolds and radial hazard marks, subtly integrated with plate faces.
 for j in range(3):
  x,y=pos(.08,.18+j*.3);ellipse(x,y-10,27,13,'#172e41',extra='stroke="#7897a6" stroke-width="2" transform="rotate(-17 '+str(x)+' '+str(y-10)+')"');ellipse(x,y-10,18,7,'#5e9cae',extra='transform="rotate(-17 '+str(x)+' '+str(y-10)+')"')
 text(850,535,'NOVA / ATLAS–07',18,'#c7d6da',extra='transform="rotate(-19 850 535)" letter-spacing="3"');text(834,564,'DEEP FIELD EXPLORATION',8,'#c1d0d6',extra='transform="rotate(-19 834 564)" letter-spacing="2"')
 shuttle(1040,725,.65);shuttle(1080,759,.33)
 # Sparse navigation tracks explain the destination without splitting the scene into cards.
 path('M1100 680Q1370 620 1510 465',stroke='#76b5c7',width=1.5,extra='stroke-dasharray="5 9" opacity=".45"');circle(1510,465,7,'none',extra='stroke="#a8d3d8"');text(1529,476,'ORBITAL CHECKPOINT',12,'#a6c2ce')
 line(1645,535,1645,560,'#76b5c7',1);text(1655,554,'KEPLER / SECTOR 09',11,'#89aebf')
 # Two translucent operational overlays; each is part of the navigation scene.
 rect(80,691,345,154,'url(#glass)',extra='rx="8" stroke="#507487" stroke-opacity=".55"');text(100,717,'NAVIGATION / VECTOR LOCK',12,'#bcd5df',extra='letter-spacing="1.3"')
 add('<g transform="translate(150 775)"><g class="radar-sweep">')
 path('M0 0L-30 -32A44 44 0 0 1 0 -44Z','#78dbe2',extra='opacity=".22"');line(0,0,0,-44,'#b5f2ef',1.8);add('</g></g>')
 for i in range(24):
  a=i*math.pi/12;line(150+46*math.cos(a),775+46*math.sin(a),150+49*math.cos(a),775+49*math.sin(a),'#7cabbc',.8)
 for x,y in [(128,753),(172,791),(140,796)]:
  circle(x,y,2.5,'#a5e2dd');circle(x,y,6,'none',extra='stroke="#8fe2d9" class="target-pulse"')
 add('<g transform="translate(150 775)"><g class="target-orbit">');circle(32,0,3,'#ecc18c');add('</g></g>')
 for r in [24,44]:circle(150,775,r,'none',extra='stroke="#47758b" stroke-dasharray="3 5"')
 path('M120 803L155 755 174 771 199 736',stroke='#92d4dc',width=1.5);circle(199,736,3,'#e9b87d');path('M191 740v-12h12M207 732v12h-12',stroke='#e9b87d',width=1.2,extra='class="target-pulse"');line(105,775,195,775,'#47758b',.6);line(150,730,150,819,'#47758b',.6)
 text(222,755,'DEST  /  K–09',12,'#adcbd7');text(222,778,'VECTOR  032°',12,'#adcbd7');text(222,801,'LINK    STABLE',12,'#8ed3c9');text(100,835,'FICTIONAL NAVIGATION / NOT LIVE TELEMETRY',8,'#7397ac')
 rect(1536,682,478,163,'url(#glass)',extra='rx="8" stroke="#507487" stroke-opacity=".55"');text(1557,708,'JUMP DRIVE / CHARGE DISTRIBUTION',12,'#bcd5df',extra='letter-spacing="1.2"')
 for i,(label,value) in enumerate([('CORE',.82),('FIELD',.68),('SYNC',.94)]):
  y=736+i*29;text(1557,y,label,10,'#9bb7c7');rect(1608,y-8,105,4,'#1b3b4f');rect(1608,y-8,105*value,4,'#8bcacb' if i<2 else '#e8bd82');text(1726,y,str(round(value*100))+'%',10,'#c0d5da')
  add(f'<clipPath id="charge-{i}"><rect x="1608" y="{y-8}" width="{105*value:.2f}" height="4"/></clipPath><g clip-path="url(#charge-{i})">')
  line(1608,y-6,1713,y-6,'#eaf9f6',2,extra=f'class="charge-flow" stroke-dasharray="5 15" style="animation-delay:-{i*.4}s"');add('</g>')
 # Segmented field ring and ticked waveform occupy separate areas of the drive panel.
 circle(1786,749,17,'none',extra='stroke="#426b80" stroke-width="2"')
 add('<g transform="translate(1786 749)"><g class="field-spin">');circle(0,0,17,'none',extra='stroke="#9de4e1" stroke-width="3" stroke-dasharray="18 9"');line(-9,0,9,0,'#b6ece7',1);line(0,-9,0,9,'#b6ece7',1);add('</g></g>')
 for i in range(7):line(1820+i*26,734,1820+i*26,795,'#426b80',.6,extra='opacity=".4"')
 for y in [745,765,785]:line(1820,y,1988,y,'#426b80',.6,extra='opacity=".4"')
 circle(1786,790,3,'#8ed3c9',extra='class="target-pulse"')
 pts=[(1820+i*2.7,777-22*math.sin(i/8)-8*math.sin(i/3)) for i in range(60)];wave='M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts);path(wave,stroke='#98d9df',width=1.4);path(wave,stroke='#e3f5f5',width=2,extra='class="signal-trace" stroke-dasharray="16 180"');line(1794,795,1988,795,'#426b80',.8);text(1800,821,'FIELD OSCILLATION / CONCEPT',9,'#789faf')
 # HUD center reticle remains small; no crosshair covers the narrative subjects.
 path('M1260 329v-12h17M1324 329v-12h-17M1260 371v12h17M1324 371v12h-17',stroke='#8bc9d8',width=1,extra='opacity=".45"');text(1234,299,'EXIT VECTOR',10,'#779fb4')
 # Typography sits in protected negative space, rather than a floating example card.
 text(80,69,'SVG–PROMPT / THE VECTOR ATLAS',14,'#94b5c8',extra='letter-spacing="3"');text(76,142,'BEFORE THE JUMP',63,'#e5edf1',extra='font-weight="600" letter-spacing="3"');text(82,187,'跃迁前夜',27,'#b7ced8',extra='letter-spacing="8"');line(83,215,147,215,'#dfb17e',3);text(163,220,'ONE SCENE. TEN VISUAL LANGUAGES.',12,'#99b8ca',extra='letter-spacing="1.8"');text(82,252,'探索舰抵达未知轨道，下一段航程即将开始。',16,'#91aebf')
 # Edge-scale marks and a mission identification strip add observable details.
 for i in range(26):line(2060,80+i*24,2060+(9 if i%5 else 18),80+i*24,'#4d7b92',.8,extra='opacity=".55"')
 text(80,880,'ATLAS–07  /  ORBITAL TRANSIT  /  BEFORE THE JUMP',10,'#7095aa',extra='letter-spacing="2"');text(2014,880,'几何 · 光影 · 数据 · 场景',12,'#8aa9bb',extra='text-anchor="end" letter-spacing="2"')
 add('</g>')
 style='''<style>
 @keyframes surface-spin{from{transform:translateX(0)}to{transform:translateX(-900px)}}
 .planet-spin{animation:surface-spin 60s linear infinite}
 .cloud-spin{animation:surface-spin 78s linear infinite}
 @keyframes warp-travel{0%{transform:translate(0,0);opacity:.04}20%{opacity:.5}80%{opacity:.5}100%{transform:translate(var(--dx),var(--dy));opacity:.04}}
 .warp{animation:warp-travel 4s linear infinite}
 @keyframes engine-breathe{50%{opacity:.72}}
 .engine-breathe{animation:engine-breathe 4.8s ease-in-out infinite}
 @keyframes shuttle-transit{0%{transform:translate(0,0);opacity:.15}15%{opacity:1}85%{opacity:1}100%{transform:translate(var(--sx),var(--sy));opacity:.15}}
 .shuttle-flight{animation:shuttle-transit 24s linear infinite}
 @keyframes signal-flow{to{stroke-dashoffset:-196}}
 .signal-trace{animation:signal-flow 2s linear infinite}
 @keyframes hud-rotate{to{transform:rotate(360deg)}}
 .radar-sweep{animation:hud-rotate 4s linear infinite}
 .target-orbit{animation:hud-rotate 12s linear infinite}
 .field-spin{animation:hud-rotate 3s linear infinite}
 @keyframes target-glow{50%{opacity:.35}}
 .target-pulse{animation:target-glow 2s ease-in-out infinite}
 @keyframes charge-stream{to{stroke-dashoffset:-20}}
 .charge-flow{animation:charge-stream 1s linear infinite}
 @media(prefers-reduced-motion:reduce){.planet-spin,.cloud-spin,.warp,.engine-breathe,.shuttle-flight,.signal-trace,.radar-sweep,.target-orbit,.field-spin,.target-pulse,.charge-flow{animation:none}}
 </style>'''
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="2100" height="900" viewBox="0 0 2100 900" style="width:100%;height:auto;display:block" role="img" aria-labelledby="hero-title hero-desc" font-family="PingFang SC, Microsoft YaHei, Arial, sans-serif"><title id="hero-title">跃迁前夜 / Before the Jump</title><desc id="hero-desc">探索舰ATLAS–07抵达星球轨道，装甲、机库、运输艇、空间环和导航投影构成一个完整场景。星球地表60秒自转模拟、云层78秒独立移动，星线径向向外运动，运输艇航行，引擎4.8秒波动。所有读数为虚构示意；减少动效时显示完整静态封面。</desc>'+style+''.join(PARTS)+'</svg>\n'
 assets=ROOT/'assets';assets.mkdir(exist_ok=True);(assets/'hero.svg').write_text(svg)
 prompt='''# 跃迁前夜 / Before the Jump

<img src="hero.svg" width="1050" alt="探索舰、星球、空间环与跃迁星线组成的科幻场景">

```text
用独立SVG画一张极其细致、具有叙事的科幻封面，2100×900，7:3。
构图：左上保留标题与暗色留白，中下方巨大楔形探索舰指向右上；右上缓慢自转的星球，空间环、卫星、运输艇建立空间尺度。星线沿同一消失点向外拉长，暗蓝背景中穿插星点与稀薄星云。
风格：深蓝黑、冷白、青色，少量琥珀色引擎与警示。复杂度来自可放大的装甲接缝、机库、窗口、能源走线和维护设备，不是把已有图表拼成九宫格。
融合：导航航线/星图承接地图，能源读数与波形承接图表，舰体线路承接架构，导航投影承接界面，轨道与场线承接科学概念，舰名舷号承接排版，状态/舱段符号承接图标，舰与运输艇承接插画，阵列与几何装甲承接生成艺术，拉丝/玻璃/辉光承接材质。
坐标：舰体顶面A(345,535)、B(610,773)、舰首C(1370,356)。装甲面片使用p(t,u)=(1-t)((1-u)A+uB)+tC，15×11共165面。侧面增厚并加入24窗口、4机库、3层紧凑舰桥（层高0→16→30→43，嵌套轮廓沿甲板投影收缩）、吊机与天线；装甲有迎光斜边和背光接缝、整面低透明度拉丝噪声，舰桥投影偏移(18,20)并模糊5px形成接触与遮挡阴影，不依赖字体画舰体。
星球：中心(1655,285)、半径224；地图宽900高440，在圆形裁切内放两个相隔900px的同图副本；地表60秒、云层78秒各自平移−900px，视觉模拟自转并非真实3D球面投影。地形用feTurbulence频率0.008/0.012、5层、seed11，阈值alpha映射后DiffuseLighting形成微地形；云层频率0.013/0.025、4层、seed23，alpha=4r−2.1，均stitchTiles。城市灯点用固定种子7301，之后覆盖静态球形明暗与大气层。
轨道：rx350/ry119椭圆旋转−0.36弧度，72刻度；三台空间设备和5个不同尺度的运输艇，遮挡关系体现远近；5艘运输艇分别沿局部向量向右上航行，18+s×12秒周期，首尾淡入淡出，减少动效时停在完整基础位置。
跃迁：星点与光线由seed7301确定，所有星线共用消失点(1300,340)，沿径向向外移动190px，周期1.8..3.8秒，起止透明度0.04、主体0.5，负延迟错开，移动区只在背景；静态星线也保持可见。
引擎：3个喷口，径向辉光4.8秒opacity1→0.72→1，不闪烁、不遮挡舰体。
投影：左下导航窗345×154，右下驱动状态窗478×163。CORE82%、FIELD68%、SYNC94%与条长对应；波形为双正弦示意，2秒流光；左雷达4秒扫描、12秒目标环绕、2秒锁定呼吸；右场环3秒旋转，条内能量流1秒循环并裁切于真实百分比宽度。读数、星域名称、舰名均虚构，不是实时遥测或物理仿真。
文字：SVG–PROMPT / THE VECTOR ATLAS、BEFORE THE JUMP、跃迁前夜、ONE SCENE. TEN VISUAL LANGUAGES.；舰身NOVA / ATLAS–07，远景KEPLER / SECTOR 09。
兼容：仅内联矢量、渐变、滤镜、pattern与CSS，没有外部图片/字体/脚本；引用必须都在本文件defs内。prefers-reduced-motion禁用地表、云层、星线、运输艇、引擎、波形和所有HUD动画，保留同一完整静态场景；CSS失效也可完整查看。外部平台是否保留动效需实际页面验证。
```

完整构造可见 [生成脚本](../scripts/build-hero.py)，独立文件可见 [hero.svg](hero.svg)。
'''
 (assets/'hero-prompt.md').write_text(prompt)
 print(f'Built 2100×900 cover: {len(PARTS)} vector elements; 7:3.')
if __name__=='__main__':build()
