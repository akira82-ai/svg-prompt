#!/usr/bin/env python3
"""Verify surface references, opacity semantics and complete fallback layers."""
from pathlib import Path
import importlib.util,json,math,re,xml.etree.ElementTree as ET
sp=importlib.util.spec_from_file_location('build',Path(__file__).with_name('build-backgrounds.py'));b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
ns={'s':'http://www.w3.org/2000/svg'}
animated={'spotlight-scan','water-shimmer','rain-ripples','lava','digital-rain','confetti','glass-lens'}
assert len(list(b.OUT.glob('*/meta.json')))==26
for i,(slug,title,en) in enumerate(b.ENTRIES,1):
 d=b.OUT/slug;raw=(d/'index.svg').read_text();svg=ET.fromstring(raw);m=json.loads((d/'meta.json').read_text())
 assert m['order']==i and m['title']==title and m['slug']==slug
 assert m['time']==('css' if slug in animated else 'static')
 assert raw in (d/'prompt.md').read_text()
 assert svg.get('viewBox')=='0 0 1400 900' and svg.get('aria-labelledby')=='title desc'
 ids=[e.get('id') for e in svg.iter() if e.get('id')];assert len(ids)==len(set(ids))
 for ref in re.findall(r'url\(#([^)]*)\)',raw):assert ref in ids
 for use in svg.findall('.//s:use',ns):assert use.get('href')[1:] in ids
 for e in svg.iter():
  assert not e.tag.endswith('script') and not any(k.startswith('on') for k in e.attrib)
  if e.tag.endswith('feTurbulence'):assert e.get('seed')=='29' and not list(e)
  if e.tag.endswith('feColorMatrix'):assert len(e.get('values').split())==20
 assert 'prefers-reduced-motion:reduce' in raw and 'animation:none' in raw
 assert 'display:none' not in raw and 'opacity:0' not in raw
 for text in svg.findall('.//s:text',ns):
  y=float(text.get('y'));assert slug=='digital-rain' or y<190 or y>810
 if slug=='focal-circle-gradient':
  captions=[e for e in svg.findall('s:text',ns) if float(e.get('y'))==166];assert len(captions)==3
  gradients=svg.findall('.//s:radialGradient',ns);assert len(gradients)==4
  base=svg.find('.//s:radialGradient[@id="lens-colors"]',ns)
  assert len(base.findall('s:stop',ns))==6 and base.get('color-interpolation')=='sRGB'
  circles=svg.findall('.//s:circle[@data-lens]',ns);assert len(circles)==3
  for name,fr,fx,fy in [('point',0,.5,.5),('circle',.2,.5,.5),('offset',.2,.38,.42)]:
   g=svg.find(f'.//s:radialGradient[@id="lens-{name}"]',ns)
   assert g.get('href')=='#lens-colors' and g.get('gradientUnits')=='objectBoundingBox'
   assert not list(g)
   assert tuple(float(g.get(k)) for k in ('fr','fx','fy'))==(fr,fx,fy)
   assert all(float(g.get(k))==.5 for k in ('cx','cy','r'))
   assert math.hypot(fx-.5,fy-.5)+fr<=.5
  assert all(float(c.get('r'))==188 and float(c.get('cy'))==500 for c in circles)
  assert not svg.findall('.//s:filter',ns) and m['time']=='static'
 if slug=='frosted-glass':
  assert len(svg.findall('.//s:use[@href="#backdrop"]',ns))==2
  clip=svg.find('.//s:g[@clip-path="url(#glass)"]',ns)
  assert clip[0].tag.endswith('rect') and clip[0].get('fill')=='#283b5e'
  assert clip[1].get('filter')=='url(#blur)'
  assert svg.find('.//s:feGaussianBlur',ns).get('stdDeviation')=='18'
 if slug in ['pattern-tile','pattern-fill','fabric','carbon-fiber']:
  pattern=svg.find('.//s:pattern',ns);assert pattern is not None and pattern.get('patternUnits')=='userSpaceOnUse'
 if slug=='starry-sky':assert len(svg.findall('.//s:circle',ns))==220
 if slug=='confetti':
  group=svg.find('.//s:g[@class="drift"]',ns);assert len(group)==65
  for e in group:
   x=float(e.get('x',e.get('cx')));y=float(e.get('y',e.get('cy')));assert not (510<x<890 and 340<y<650)

lens=ET.parse(b.OUT/'glass-lens/index.svg').getroot()
assert len(lens.findall('.//s:use[@href="#stripe-scene"]',ns))==2
interior=lens.find('.//s:g[@data-lens-interior]',ns)
assert interior[0].tag.endswith('rect') and interior[0].get('fill')=='#ece8df'
assert interior[1].get('transform')=='translate(-126 -90) scale(1.18)'
assert lens.find('.//s:feDisplacementMap',ns).get('scale')=='32'
print('PASS: 26 materials; prompt/reference integrity, patterns, glass, noise, ambient motion and shared-stop focal-circle gradients.')
