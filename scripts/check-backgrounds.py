#!/usr/bin/env python3
"""Verify surface references, opacity semantics and complete fallback layers."""
from pathlib import Path
import importlib.util,json,re,xml.etree.ElementTree as ET
sp=importlib.util.spec_from_file_location('build',Path(__file__).with_name('build-backgrounds.py'));b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
ns={'s':'http://www.w3.org/2000/svg'}
animated={'spotlight-scan','water-shimmer','rain-ripples','lava','digital-rain','confetti'}
assert len(list(b.OUT.glob('*/meta.json')))==24
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
print('PASS: 24 materials; order, prompt parity, reference integrity, 4 patterns, opaque glass backing, fixed noise seeds and 6 static-safe ambient animations.')
