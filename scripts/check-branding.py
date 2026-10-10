#!/usr/bin/env python3
"""Validate shared brand geometry, print proportions and library statistics."""
from pathlib import Path
import json,math,re,runpy,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'gallery/branding';NS={'s':'http://www.w3.org/2000/svg'}
SOURCE=runpy.run_path(str(ROOT/'scripts/build-branding.py'))
def svg(slug):return E.parse(BASE/slug/'index.svg').getroot()
def nodes(slug,attr):return [e for e in svg(slug).iter() if attr in e.attrib]
def near(a,b,tol=.001):assert math.isclose(float(a),b,abs_tol=tol),(a,b)
def texts(slug):return [e.text or '' for e in svg(slug).findall('.//s:text',NS)]
entries=sorted(BASE.glob('*/meta.json'),key=lambda p:json.loads(p.read_text())['order']);assert len(entries)==24
assert [p.parent.name for p in entries]==[e[0] for e in SOURCE['ENTRIES']]
assert [json.loads(p.read_text())['order'] for p in entries]==list(range(1,25))
for removed in SOURCE['REMOVED']:assert not (BASE/removed).exists()
canonical_mark=None;canonical_word=None
for p in entries:
    slug=p.parent.name;m=json.loads(p.read_text());root=svg(slug);assert root.get('viewBox')=='0 0 1400 900'
    assert root.find('s:title',NS).text==m['title']
    assert (p.parent/'prompt.md').read_text().splitlines()[0].startswith('# '+m['title']+' / ')
    ids={e.get('id') for e in root.iter() if e.get('id')};assert len(ids)==sum(bool(e.get('id')) for e in root.iter())
    for e in root.iter():
        assert e.tag not in ['{http://www.w3.org/2000/svg}script','{http://www.w3.org/2000/svg}image','{http://www.w3.org/2000/svg}foreignObject']
        if e.get('href'):assert e.get('href').startswith('#') and e.get('href')[1:] in ids
        for v in e.attrib.values():
            for ref in re.findall(r'url\(#([^)]*)\)',v):assert ref in ids
    mark=root.find("s:defs/s:symbol[@id='nova-mark']",NS);word=root.find("s:defs/s:symbol[@id='nova-wordmark']",NS)
    if canonical_mark is None:canonical_mark=E.tostring(mark);canonical_word=E.tostring(word)
    assert E.tostring(mark)==canonical_mark and E.tostring(word)==canonical_word
    assert mark.get('viewBox')=='0 0 6 6' and word.get('viewBox')=='0 0 266 60'
    assert len(word.findall('s:path',NS))==4
    for e in nodes(slug,'data-mark-size'):near(e.get('width'),float(e.get('height')));near(e.get('width'),float(e.get('data-mark-size')))
    for e in nodes(slug,'data-word-height'):near(float(e.get('width'))/float(e.get('height')),266/60)
    if m['time']=='smil':
        assert 'prefers-reduced-motion:reduce' in (p.parent/'index.svg').read_text()
        assert any(e.get('class')=='motion' for e in root.iter()) and any(e.get('class')=='fallback' for e in root.iter())
        for e in root.findall('.//s:animate',NS):
            assert e.get('repeatCount') in (None,'1') and e.get('fill')=='freeze'
            values=e.get('values').split(';');times=list(map(float,e.get('keyTimes').split(';')))
            assert len(values)==len(times) and times[0]==0 and times[-1]==1
    else:assert not root.findall('.//s:animate',NS)
for slug in ['logo-grid','brand-guidelines']:
    box=nodes(slug,'data-clearance')[0];mark=nodes(slug,'data-mark-size')[0];u=float(box.get('data-clearance'));size=float(mark.get('width'));near(size/6,u)
    for side in ['x','y']:near(float(mark.get(side))-float(box.get(side)),u)
    near(box.get('width'),size+2*u);near(box.get('height'),size+2*u)
# Independent lockup relations: size ratios, gap and common vertical center.
marks=nodes('brand-lockup','data-mark-size');words=nodes('brand-lockup','data-word-height')
near(float(marks[0].get('height'))/float(words[0].get('height')),1.5)
near(float(words[0].get('x'))-float(marks[0].get('x'))-float(marks[0].get('width')),float(words[0].get('height'))/2)
near(float(marks[1].get('x'))+float(marks[1].get('width'))/2,float(words[1].get('x'))+float(words[1].get('width'))/2)
for color in ['#245EE8','#14263D','#FFFFFF','#DCE7FC']:assert color in texts('brand-palette')
assert [e.get('data-type-size') for e in nodes('type-scale','data-type-size')]==['56','36','24','18','14']
for e in nodes('type-scale','data-type-size'):assert float(e.get('data-leading'))>float(e.get('font-size'))
for e in nodes('business-card','data-print-width'):
    near(float(e.get('width'))/float(e.get('data-print-width')),6);near(float(e.get('height'))/float(e.get('data-print-height')),6)
for e in nodes('social-kit','data-design-width'):
    near(float(e.get('width'))/float(e.get('height')),float(e.get('data-design-width'))/float(e.get('data-design-height')))
# Packaging: actual physical panel proportions and distinct cut/fold/safety roles.
assert [int(e.get('data-panel-width')) for e in nodes('packaging-dieline','data-panel-width')]==[24,60,180,60,180]
for e in nodes('packaging-dieline','data-fold'):assert e.get('stroke-dasharray')
bleed=nodes('packaging-dieline','data-bleed')[0]
near(bleed.get('x'),150-8);near(bleed.get('y'),330-8);near(bleed.get('width'),504+16);near(bleed.get('height'),340+16)
safety=nodes('packaging-dieline','data-safety')[0]
near(safety.get('x'),234+12);near(safety.get('y'),390+12);near(safety.get('width'),180-24);near(safety.get('height'),220-24)
front=nodes('packaging-dieline','data-front-aspect')[0];near(float(front.get('width'))/float(front.get('height')),180/220)
assert 'PNG通常静态，APNG支持动画' in texts('comparison-vs')
assert '不添加虚构认证或质量背书。' in texts('circular-badge')
records=[json.loads(p.read_text()) for p in (ROOT/'gallery').glob('*/*/meta.json')];static=sum(m['time']=='static' for m in records)
stats={e.get('data-stat'):int(e.text) for e in nodes('stat-numbers','data-stat')}
assert stats=={'works':len(records),'categories':10,'static':static,'animated':len(records)-static}
assert stats['static']+stats['animated']==stats['works']
# Cross-category links should no longer refer to retired branding specimens.
for p in [ROOT/'README.md',ROOT/'scripts/build-readme.mjs']+list((ROOT/'gallery').glob('*/*/prompt.md')):
    for removed in SOURCE['REMOVED']:assert 'branding/'+removed+'/' not in p.read_text(),p
print('PASS: 24 branding specimens; shared vector assets, clear space, lockup ratios, typography, media proportions, packaging roles, one-shot animations and library statistics.')
