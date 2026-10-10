#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify chart encodings, data semantics, ordering and library links (stdlib only)."""
from pathlib import Path
import json,math,re,xml.etree.ElementTree as E
from collections import Counter
from datetime import date
r=Path(__file__).resolve().parents[1];ns={'s':'http://www.w3.org/2000/svg'}
files=list((r/'gallery').glob('*/*/meta.json'));assert len(files)>0
schema=json.loads((r/'schema/entry.schema.json').read_text())
for p in files:
 m=json.loads(p.read_text());assert set(schema['required'])<=m.keys();assert m.keys()<=schema['properties'].keys();assert m['slug']==p.parent.name
 for k,v in m.items():
  rule=schema['properties'][k]
  if 'enum' in rule:assert v in rule['enum']
  if rule.get('type')=='string':assert isinstance(v,str)
  if rule.get('type')=='integer':assert type(v)==int and v>=rule.get('minimum',0)
  if rule.get('type')=='array':assert isinstance(v,list) and all(isinstance(x,str) for x in v)
  if 'pattern' in rule:assert re.fullmatch(rule['pattern'],v)
  if rule.get('format')=='date':date.fromisoformat(v)
 text=(p.parent/'prompt.md').read_text();assert text.count('```')==2
 for groups in re.findall(r'\]\(([^)]+)\)|src="([^"]+)"',text):
  link=next(g for g in groups if g)
  if not link.startswith(('http:','https:','#')):assert (p.parent/link).exists(),(p,link)
 svg=E.parse(p.parent/'index.svg');ids=[e.get('id') for e in svg.iter() if e.get('id')];assert len(ids)==len(set(ids)),p
 for e in svg.iter():
  for attr,value in e.attrib.items():
   for id in re.findall(r'url\(#([^)]*)\)',value):assert id in ids,(p,id)
entries=sorted((r/'gallery/charts').glob('*/meta.json'),key=lambda p:json.loads(p.read_text())['order']);assert len(entries)==31;assert [json.loads(p.read_text())['order'] for p in entries]==list(range(1,32))
order=[p.parent.name for p in entries]
for a,b in [('bar','bar-growth'),('line','line-draw'),('area','area-expand'),('funnel','funnel-steps'),('sankey','sankey-flow'),('gantt','gantt-progress')]:assert order.index(b)==order.index(a)+1

def svg(slug):return E.parse(r/'gallery/charts'/slug/'index.svg')
def tagged(slug,tag,attr):return [e for e in svg(slug).findall('.//s:'+tag,ns) if attr in e.attrib]
for slug in ['bar','bar-growth','bullet-chart','funnel','funnel-steps']:
 for e in tagged(slug,'rect','data-value'):
  dimension='height' if slug.startswith('bar') else 'width'
  assert math.isclose(float(e.get(dimension)),float(e.get('data-value'))*float(e.get('data-scale')),abs_tol=.001)
for e in tagged('bubble','circle','data-size'):assert math.isclose(float(e.get('r'))**2,16*float(e.get('data-size')),abs_tol=.09)
for e in tagged('treemap','rect','data-share'):assert math.isclose(float(e.get('width'))*float(e.get('height'))/(880*340)*100,float(e.get('data-share')),abs_tol=.001)
for e in tagged('pie-donut','path','data-angle'):assert math.isclose(float(e.get('data-angle')),float(e.get('data-value'))/100*2*math.pi)
for slug in ['sankey','sankey-flow']:
 ribbons=tagged(slug,'path','data-flow');assert sum(float(e.get('data-flow')) for e in ribbons[:3])==100;assert sum(float(e.get('data-flow')) for e in ribbons[3:])==100
 for e in ribbons:assert float(e.get('data-thickness'))==float(e.get('data-flow'))*2.5
flows=tagged('chord-diagram','path','data-flow');assert len(flows)==6
for e in flows:assert math.isclose(float(e.get('data-angle'))/float(e.get('data-flow')),(2*math.pi-.32)/144)
expected={38,42,37,27};assert {int(e.text.split()[-1]) for e in svg('chord-diagram').findall('.//s:text',ns) if e.text and re.match(r'^[北东南西]区 \d+$',e.text)}==expected
for e in tagged('waterfall','rect','data-start'):assert math.isclose(float(e.get('height')),abs(float(e.get('data-end'))-float(e.get('data-start')))*2.5,abs_tol=.001)
counts=[int(e.get('data-count')) for e in tagged('histogram-boxplot','rect','data-count')];assert counts==[4,9,9,4,2,0,1,0,0,1] and sum(counts)==30
box=tagged('boxplot','rect','data-q1')[0];assert float(box.get('data-q1'))==110.5 and float(box.get('data-q3'))==141
for slug in ['line-draw','area-expand','bar-growth','funnel-steps','sankey-flow','gantt-progress']:
 text=(r/'gallery/charts'/slug/'index.svg').read_text();assert 'prefers-reduced-motion' in text;assert not svg(slug).findall('.//s:animate',ns);assert not svg(slug).findall('.//s:animateTransform',ns)
calendar=tagged('heatmap','rect','data-date');assert len(calendar)==140;assert calendar[0].get('data-date')=='2026-01-05' and calendar[-1].get('data-date')=='2026-05-24'
readme=(r/'README.md').read_text()
for link in re.findall(r'(?:src|href)="([^"]+)"',readme):assert (r/link).exists(),link
print('PASS: Entry metadata and links; 31 chart order; schema constraints; XML/IDs; encoding ratios; conservation; histogram/quantiles; calendar; reduced motion')
print(Counter(json.loads(p.read_text())['time'] for p in files))
