#!/usr/bin/env python3
"""Verify standalone scene assets, reference parity and safe ambient motion."""
from pathlib import Path
import importlib.util,json,xml.etree.ElementTree as ET
spec=importlib.util.spec_from_file_location('build',Path(__file__).with_name('build-illustrations.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
ns={'s':'http://www.w3.org/2000/svg'}
animated={'hologram','energy-core','sunrise-scene','snow-globe','campfire'}
assert not (b.OUT/'particle-collider').exists()
assert len(list(b.OUT.glob('*/meta.json')))==15
for i,(slug,title,en) in enumerate(b.ENTRIES,1):
 d=b.OUT/slug;raw=(d/'index.svg').read_text();svg=ET.fromstring(raw);meta=json.loads((d/'meta.json').read_text());prompt=(d/'prompt.md').read_text()
 assert meta['order']==i and meta['title']==title and meta['slug']==slug
 assert meta['time']==('css' if slug in animated else 'static')
 assert svg.get('viewBox')=='0 0 1400 900' and svg.get('aria-labelledby')=='title desc'
 assert raw in prompt and title in prompt and en in prompt
 ids=[e.get('id') for e in svg.iter() if e.get('id')];assert len(ids)==len(set(ids))
 import re
 for ref in re.findall(r'url\(#([^)]*)\)',raw):assert ref in ids
 for e in svg.iter():
  assert not e.tag.endswith('script') and not any(k.startswith('on') for k in e.attrib)
  if e.tag.endswith('text'):
   assert 0<=float(e.get('x'))<=1400 and 0<=float(e.get('y'))<=900
 assert 'prefers-reduced-motion:reduce' in raw and 'animation:none' in raw
 assert 'opacity:0' not in raw and 'display:none' not in raw
 assert 'clip-path="url(#stage)"' in raw
 if slug=='snow-globe':assert 'clip-path="url(#globe)"' in raw
 if slug=='tech-campus':assert meta['space']=='2d' and '.866' not in raw
print('PASS: 15 standalone scenes; bilingual titles, order, prompt parity, local references, clipping and visible reduced-motion states.')
