#!/usr/bin/env python3
"""Check geometric invariants independently of the rendering recipes."""
import importlib.util,json,math,re,random
from pathlib import Path
import xml.etree.ElementTree as ET
spec=importlib.util.spec_from_file_location('geo',Path(__file__).with_name('build-geometry.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ns={'s':'http://www.w3.org/2000/svg'}
def area(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2
for i,(slug,title,en) in enumerate(g.ENTRIES,1):
 d=g.OUT/slug;raw=(d/'index.svg').read_text();svg=ET.fromstring(raw);m=json.loads((d/'meta.json').read_text());prompt=(d/'prompt.md').read_text()
 assert m['order']==i and m['title']==title and m['slug']==slug
 assert svg.get('viewBox')=='0 0 1400 900' and svg.get('role')=='img'
 assert raw in prompt and en in prompt
 ids=[e.get('id') for e in svg.iter() if e.get('id')];assert len(ids)==len(set(ids))
 for ref in re.findall(r'url\(#([^)]*)\)',raw):assert ref in ids
 assert not re.search(r'\b(?:nan|inf)\b',raw,re.I)
 assert 'prefers-reduced-motion' in raw
 for e in svg.iter():assert not e.tag.endswith('script') and not any(k.startswith('on') for k in e.attrib)
 if slug in ['shape-morph','blob-morph']:
  a=svg.find('.//s:animate',ns);values=a.get('values').split(';');assert values[0]==values[-1]
  assert len({tuple(re.findall('[A-Za-z]',v)) for v in values})==1
  assert len(re.findall(r'-?\d+\.?\d*',values[0]))==192
  assert svg.find('.//s:path[@class="snapshot"]',ns).get('d')==values[0]
  assert a.get('dur')=='12s'
 if slug=='sunflower':
  cs=svg.findall('.//s:circle',ns);assert len(cs)==800
  for n,c in enumerate(cs):
   x,y=float(c.get('cx'))-700,float(c.get('cy'))-490
   assert abs(math.hypot(x,y)-9.5*math.sqrt(n))<.001
   if n:assert abs(math.atan2(math.sin(math.atan2(y,x)-n*g.GOLDEN),math.cos(math.atan2(y,x)-n*g.GOLDEN)))<.001
assert len(list(g.OUT.glob('*/meta.json')))==18
assert all(not (g.OUT/s).exists() for s in g.RETIRED)
# Every clipped Voronoi vertex is nearer its owner than any competing site.
sites=g.seeds();polys=g.cells(sites)
assert abs(sum(area(p) for p in polys)-1240*570)<1e-5
for i,poly in enumerate(polys):
 assert len(poly)>=3 and area(poly)>0
 for x,y in poly:
  own=(x-sites[i][0])**2+(y-sites[i][1])**2
  assert all(own<=(x-xx)**2+(y-yy)**2+1e-5 for xx,yy in sites)
# Random interior samples belong to exactly one nearest site's polygon.
def contains(poly,x,y):
 signs=[(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0]) for a,b in zip(poly,poly[1:]+poly[:1])]
 return all(t>=-1e-7 for t in signs) or all(t<=1e-7 for t in signs)
rng=random.Random(73)
for _ in range(400):
 x,y=rng.uniform(80,1320),rng.uniform(210,780);owners=[i for i,p in enumerate(polys) if contains(p,x,y)]
 assert len(owners)==1
 assert owners[0]==min(range(len(sites)),key=lambda i:(x-sites[i][0])**2+(y-sites[i][1])**2)
ts=g.triangles();assert len(ts)==100 and all(area(list(t))>0 for t in ts)
assert abs(sum(area(list(t)) for t in ts)-1240*570)<1e-5
edges={}
for t in ts:
 for a,b in zip(t,t[1:]+t[:1]):
  key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
assert set(edges.values())=={1,2} and sum(v==1 for v in edges.values())==30
segments=g.tree_segments();assert len(segments)==511
for depth in range(9):
 ss=[s for s in segments if s[-1]==depth];assert len(ss)==2**depth
 assert all(abs(math.hypot(s[2]-s[0],s[3]-s[1])-155*.72**depth)<1e-8 for s in ss)
lines=g.flow_lines();assert len(lines)==38
for pts in lines:
 for (x,y),(xx,yy) in zip(pts,pts[1:]):
  assert abs(math.hypot(xx-x,yy-y)-4)<1e-9
  a=g.flow_angle(x,y);expected=g.flow_angle(x+2*math.cos(a),y+2*math.sin(a))
  assert abs(math.atan2(yy-y,xx-x)-expected)<1e-10
# Convex combinations of corresponding radial vertices remain ordered and nonzero.
for kind in ['geometric','organic']:
 shapes=g.morph_shapes(kind)
 for a,b in zip(shapes,shapes[1:]+shapes[:1]):
  for t in [0,.25,.5,.75,1]:
   p=[((1-t)*x+t*xx,(1-t)*y+t*yy) for (x,y),(xx,yy) in zip(a,b)]
   assert area(p)>50000
   for x,y in p:assert 64<x<1336 and 190<y<810 and math.hypot(x-700,y-490)>100
print('PASS: 18 specimens; Voronoi nearest-site coverage, 100-face manifold, flow integration, 511 branches, 800 golden-angle points and morph snapshots.')
