#!/usr/bin/env python3
"""Verify spatial encodings against explicit source coordinates and measurements."""
import json
import math
import runpy
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DATA=runpy.run_path(str(ROOT/'scripts/build-maps.py'))
BASE=ROOT/'gallery/maps'
NS={'s':'http://www.w3.org/2000/svg'}
def svg(slug):return ET.parse(BASE/slug/'index.svg').getroot()
def nodes(slug,attribute):return [n for n in svg(slug).iter() if attribute in n.attrib]
def near(a,b):assert math.isclose(float(a),b,abs_tol=.001), (a,b)
entries=sorted(BASE.glob('*/meta.json'),key=lambda p:json.loads(p.read_text())['order'])
assert len(entries)==12
assert [json.loads(p.read_text())['order'] for p in entries]==list(range(1,13))
for p in entries:
    for f in ['index.svg','prompt.md']:assert (p.parent/f).is_file()
assert DATA['GEO']['features']
assert 'naturalearth' in json.dumps(DATA['GEO']).lower()
tiles=nodes('china-grid-map','data-province')
assert any(n.get('data-province')=='豫' and n.get('data-value')=='61' for n in tiles)
for n in tiles:
    v=int(n.get('data-value'));assert int(n.get('data-band'))==(3 if v>=80 else 2 if v>=40 else 1 if v>=20 else 0)
for n in nodes('choropleth','data-band'):
    v=int(n.get('data-value'));assert int(n.get('data-band'))==(0 if v<60 else 1 if v<75 else 2 if v<90 else 3)
for n in nodes('proportional-symbols','data-city'):
    x,y=DATA['project'](float(n.get('data-lon')),float(n.get('data-lat')))
    near(n.get('cx'),x);near(n.get('cy'),y);near(float(n.get('r'))**2,9*float(n.get('data-value')))
points=nodes('point-distribution','data-point');assert len(points)==20
for n in points:
    near(n.get('cx'),140+1.2*float(n.get('data-x')));near(n.get('cy'),785-1.2*float(n.get('data-y')))
cells=nodes('spatial-density','data-cell');assert len(cells)==600
for n in cells:
    x,y=map(float,n.get('data-cell').split(','))
    expected=sum(math.exp(-((x-px)**2+(y-py)**2)/4050) for px,py in DATA['POINTS'])/ (4050*math.pi)*10000
    near(n.get('data-density'),expected);assert n.get('fill')==DATA['blend'](expected/3)
assert max(float(n.get('data-density')) for n in cells)<3
snap=lambda slug:ET.tostring(svg(slug).find("s:g[@id='event-snapshot']",NS))
assert snap('regional-events')==snap('map-ripple')
assert 'prefers-reduced-motion:reduce' in (BASE/'map-ripple/index.svg').read_text()
for n in nodes('map-ripple','data-event'):near(float(n.get('r'))**2,36*float(n.get('data-value')))
flows=nodes('origin-destination','data-flow');assert len(flows)==4
for n in flows:
    near(n.get('stroke-width'),.7*float(n.get('data-flow')));assert n.get('marker-end')=='url(#flow-arrow)'
stations=nodes('route-stations','data-station');assert len(stations)==7
assert sum(n.get('data-station')=='X' for n in stations)==1
services=nodes('service-coverage','data-service')
for n in services:near(n.get('r'),1.2*float(n.get('data-radius-m')))
for n in nodes('service-coverage','data-target'):
    x,y=float(n.get('data-x')),float(n.get('data-y'))
    covered=any((x-float(s.get('data-x')))**2+(y-float(s.get('data-y')))**2<=float(s.get('data-radius-m'))**2 for s in services)
    assert n.get('data-covered')==str(covered).lower()
rooms=nodes('campus-floorplan','data-room');assert len(rooms)==6
for n in rooms:
    x,y,w,h=map(float,n.get('data-box-m').split(','));near(n.get('width'),12*w);near(n.get('height'),12*h)
for n in nodes('campus-floorplan','data-device'):
    x,y=float(n.get('data-x')),float(n.get('data-y'))
    assert any(rx<x<rx+w and ry<y<ry+h for rx,ry,w,h in [map(float,r.get('data-box-m').split(',')) for r in rooms])
comparison=nodes('spatial-comparison','data-time');assert len(comparison)==36
for n in comparison:
    v=DATA['TIME_DATA'][int(n.get('data-time'))][int(n.get('data-zone'))]
    assert int(n.get('data-value'))==v and n.get('fill')==DATA['blend'](v/50)
    near(n.get('width'),90);near(n.get('height'),90)
print('OK: 12 maps; projections, area, bins, 600 KDE cells, snapshot parity, flows, coverage and shared scales verified.')
