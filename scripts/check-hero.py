#!/usr/bin/env python3
"""Check the cinematic cover's projection, dimensions, local assets and motion."""
from pathlib import Path
import xml.etree.ElementTree as ET
import math,re,importlib.util
ROOT=Path(__file__).resolve().parents[1]
ns={'s':'http://www.w3.org/2000/svg'}
raw=(ROOT/'assets/hero.svg').read_text();svg=ET.fromstring(raw)
assert svg.get('viewBox')=='0 0 2100 900'
assert int(svg.get('width'))/int(svg.get('height'))==7/3
assert 'width:100%' in svg.get('style') and 'height:auto' in svg.get('style')
assert svg.get('aria-labelledby')=='hero-title hero-desc'
ids=[e.get('id') for e in svg.iter() if e.get('id')];assert len(ids)==len(set(ids))
for ref in re.findall(r'url\(#([^)]*)\)',raw):assert ref in ids
for e in svg.iter():
 assert not e.tag.endswith('script') and not any(k.startswith('on') for k in e.attrib)
 if e.get('href'):assert e.get('href').startswith('#') and e.get('href')[1:] in ids
assert not svg.findall('.//s:image',ns)
assert len(svg.findall('.//s:path[@data-role="armor-plate"]',ns))==165
assert len(svg.findall('.//s:path[@data-role="hangar"]',ns))==4
assert len(svg.findall('.//s:path[@data-role="hull-window"]',ns))==24
# Collinearity with the actual vanishing point proves streaks are radial.
lines=svg.findall('.//s:path[@class="warp"]',ns);assert len(lines)>40
for e in lines:
 x,y,xx,yy=map(float,re.findall(r'-?\d+\.?\d*',e.get('d')))
 cross=(x-1300)*(yy-y)-(y-340)*(xx-x)
 assert abs(cross)<20
 style=e.get('style');dx,dy=map(float,re.findall(r'--d[xy]:(-?[\d.]+)px',style))
 assert abs(math.hypot(dx,dy)-190)<.002
 assert (x-1300)*dx+(y-340)*dy>0
 assert re.search(r'animation-delay:-',style)
spin=svg.find('.//s:g[@class="planet-spin"]',ns);assert len(spin)==2
assert spin[0].get('href')==spin[1].get('href')=='#map-tile' and spin[1].get('x')=='900'
assert svg.find('.//s:g[@id="map-tile"]',ns).get('clip-path')=='url(#map-bounds)'
cloud=svg.find('.//s:g[@class="cloud-spin"]',ns);assert len(cloud)==2 and cloud[1].get('x')=='900'
assert len(svg.findall('.//s:g[@class="shuttle-flight"]',ns))==5
assert svg.find('.//s:feDiffuseLighting',ns) is not None
for noise in svg.findall('.//s:feTurbulence',ns):assert noise.get('seed') and noise.get('stitchTiles')=='stitch'
for f in svg.findall('.//s:feColorMatrix',ns):assert len(f.get('values').split())==20
assert '78s linear infinite' in raw
assert 'translateX(-900px)' in raw and '60s linear infinite' in raw
assert 'prefers-reduced-motion:reduce' in raw and 'animation:none' in raw
assert 'display:none' not in raw and 'opacity:0' not in raw
# HUD bars and their displayed readings must match.
rects=svg.findall('.//s:rect',ns)
for y,value in [(728,.82),(757,.68),(786,.94)]:
 assert any(float(r.get('x','0'))==1608 and float(r.get('y','0'))==y and abs(float(r.get('width'))-105*value)<.01 for r in rects)
sp=importlib.util.spec_from_file_location('hero',ROOT/'scripts/build-hero.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
for t in [0,.25,.5,.75,1]:
 for u in [0,.25,.5,.75,1]:
  x,y=h.pos(t,u);assert 345<=x<=1370 and 356<=y<=773
prompt=(ROOT/'assets/hero-prompt.md').read_text();assert '2100×900' in prompt and '7301' in prompt and '60秒' in prompt
readme=(ROOT/'README.md').read_text();assert readme.count('src="assets/hero.svg"')==1
assert readme.index('assets/hero.svg')<readme.index('## 目录')
assert 'width="1050"' in readme.split('assets/hero.svg')[1][:120]
assert len(list((ROOT/'gallery').glob('*/*/meta.json')))==233
print(f'PASS: 7:3 hero; 165 plates, 4 hangars, 24 windows, {len(lines)} radial warp streaks, periodic planet texture, HUD ratios and static-safe motion.')

roofs=svg.findall('.//s:path[@data-role="bridge-roof"]',ns)
assert [(int(e.get('data-bottom')),int(e.get('data-top'))) for e in roofs]==[(0,16),(16,30),(30,43)]
for cls in ['radar-sweep','target-orbit','field-spin','target-pulse','charge-flow']:
 assert svg.findall(f'.//*[@class="{cls}"]',ns)
 assert '.'+cls in raw.split('@media(prefers-reduced-motion:reduce)')[1]
for i,v in enumerate([.82,.68,.94]):
 clip=svg.find(f'.//s:clipPath[@id="charge-{i}"]/s:rect',ns)
 assert abs(float(clip.get('width'))-105*v)<.01
