#!/usr/bin/env python3
"""Check semantic references, actual size examples and stable animation states."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('build_icons',Path(__file__).with_name('build-icons.py'))
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
ns={'s':'http://www.w3.org/2000/svg'}
for order,(slug,title,en) in enumerate(build.ENTRIES,1):
 d=build.OUT/slug;m=json.loads((d/'meta.json').read_text());svg=ET.parse(d/'index.svg').getroot();prompt=(d/'prompt.md').read_text()
 assert m['order']==order and m['title']==title
 assert svg.get('viewBox')=='0 0 1400 900'
 assert title in prompt and en in prompt and '```' in prompt
 ids=[e.get('id') for e in svg.iter() if e.get('id')];assert len(ids)==len(set(ids))
 for use in svg.findall('.//s:use',ns):
  assert use.get('href')[1:] in ids
  assert use.get('fill')=='currentColor' or use.get('stroke')=='currentColor'
 assert not any(e.tag.endswith('script') for e in svg.iter())
 if slug=='small-size-icons':
  for size in [16,20,24,32]:assert any(u.get('width')==str(size) for u in svg.findall('.//s:use',ns))
 if slug=='arrows':
  for deg in [180,-90,90]:assert any(f'rotate({deg} ' in u.get('transform','') for u in svg.findall('.//s:use',ns))
 if slug=='symbol-morph':
  animations=svg.findall('.//s:animate',ns);assert len(animations)==5
  for a in animations:
   assert a.get('fill')=='freeze' and a.get('repeatCount') is None
   start,end=a.get('values').split(';')
   import re
   assert re.findall('[A-Za-z]',start)==re.findall('[A-Za-z]',end)
  assert len(svg.findall('.//s:path[@class="fallback"]',ns))==5
  assert 'prefers-reduced-motion' in (d/'index.svg').read_text()
assert len(list(build.OUT.glob('*/meta.json')))==12
print('PASS: 12 icon specimens; order, bilingual prompts, local symbols, currentColor, sizes, directions and one-shot states.')
