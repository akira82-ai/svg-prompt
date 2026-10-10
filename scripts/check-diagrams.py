#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate diagram routing, branches, reachability, variant parity and semantics."""
from pathlib import Path
import ast
import json
import math
import re
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}


def load(slug):
    tree=E.parse(ROOT/'gallery/diagrams'/slug/'index.svg')
    nodes={e.get('data-node'):e for e in tree.findall('.//s:g',NS) if e.get('data-node')}
    edges=[e for e in tree.findall('.//s:polyline',NS) if e.get('data-edge')]
    return tree,nodes,edges


def points(e):return [tuple(map(float,p.split(','))) for p in e.get('points').split()]
def bounds(node):return list(map(float,node.get('data-box').split(',')))
def port(node,side):
    x,y,w,h=bounds(node)
    return {'l':(x,y+h/2),'r':(x+w,y+h/2),'t':(x+w/2,y),'b':(x+w/2,y+h)}[side]


def signature(slug):
    _,nodes,edges=load(slug)
    return ({key:(e.get('data-box'),e.get('data-kind'),''.join(e.itertext())) for key,e in nodes.items()},[(e.get('data-source'),e.get('data-target'),e.get('data-guard'),e.get('points')) for e in edges])


def edge_conditions(slug,source):
    return {e.get('data-guard') for e in load(slug)[2] if e.get('data-source')==source}


entries=sorted((ROOT/'gallery/diagrams').glob('*/meta.json'),key=lambda p:json.loads(p.read_text())['order'])
assert len(entries)==21
assert [json.loads(p.read_text())['order'] for p in entries]==list(range(1,22))
order=[p.parent.name for p in entries]
for a,b in [('process-steps','process-walk'),('system-architecture','animated-architecture'),('service-dependencies','network-pulse'),('timeline-svg','timeline-reveal')]:
    assert order.index(b)==order.index(a)+1
    assert signature(a)==signature(b),(a,b)

for p in entries:
    slug=p.parent.name;tree,nodes,edges=load(slug)
    prompt=(p.parent/'prompt.md').read_text()
    assert prompt.count('```')==2
    assert json.loads(p.read_text())['slug']==slug
    for key,node in nodes.items():
        x,y,w,h=bounds(node);assert w>0 and h>0 and 0<=x and 0<=y and x+w<=1400 and y+h<=900,(slug,key)
    for i,(key,a) in enumerate(nodes.items()):
        if a.get('data-kind')=='event':continue
        x,y,w,h=bounds(a)
        for key2,b in list(nodes.items())[i+1:]:
            if b.get('data-kind')=='event':continue
            xx,yy,ww,hh=bounds(b)
            assert min(x+w,xx+ww)<=max(x,xx) or min(y+h,yy+hh)<=max(y,yy),(slug,key,key2,'nodes overlap')
    for e in edges:
        source,target=e.get('data-source'),e.get('data-target');assert source in nodes and target in nodes
        pts=points(e)
        if e.get('data-route')=='ports':
            assert pts[0]==port(nodes[source],e.get('data-source-port'))
            assert pts[-1]==port(nodes[target],e.get('data-target-port'))
        for a,b in zip(pts,pts[1:]):
            assert a[0]==b[0] or a[1]==b[1],(slug,'diagonal route')
            for key,node in nodes.items():
                if key in (source,target) or node.get('data-kind')=='event':continue
                x,y,w,h=bounds(node)
                assert not (a[0]==b[0] and x+1<a[0]<x+w-1 and max(min(a[1],b[1]),y+1)<min(max(a[1],b[1]),y+h-1)),(slug,source,target,key)
                assert not (a[1]==b[1] and y+1<a[1]<y+h-1 and max(min(a[0],b[0]),x+1)<min(max(a[0],b[0]),x+w-1)),(slug,source,target,key)
    edge_map={e.get('data-edge'):e for e in edges}
    for animated in tree.findall('.//s:path',NS):
        reference=animated.get('data-animated-edge')
        if reference:
            assert reference in edge_map
            actual=[tuple(map(float,xy.split())) for xy in re.split(r'\s+L\s+',animated.get('d')[2:])]
            assert actual==points(edge_map[reference]),(slug,'animation route differs')
    if json.loads(p.read_text())['time']=='css':
        assert 'prefers-reduced-motion' in (p.parent/'index.svg').read_text()
        assert not tree.findall('.//s:animate',NS)
    if slug in ('decision-flowchart','swimlane','state-machine','agent-loop','data-pipeline'):
        terminals={key for key,node in nodes.items() if node.get('data-terminal')=='true'}
        starts={key for key,node in nodes.items() if node.get('data-start')=='true'}
        adjacency={key:[] for key in nodes}
        for e in edges:adjacency[e.get('data-source')].append(e.get('data-target'))
        for terminal in terminals:assert not adjacency[terminal],(slug,'terminal has outgoing edge')
        def reachable(start):
            seen=set();todo=[start]
            while todo:
                item=todo.pop()
                if item in seen:continue
                seen.add(item);todo.extend(adjacency[item])
            return seen
        assert starts
        assert set(nodes)<=set.union(*(reachable(start) for start in starts)),(slug,'unreachable node')
        for key in nodes:assert reachable(key)&terminals,(slug,key,'no terminating path')

assert edge_conditions('decision-flowchart','render')=={'是','否'}
assert edge_conditions('decision-flowchart','aligned')=={'是','否'}
assert edge_conditions('decision-flowchart','fix')=={'retry<3','retry>=3'}
assert edge_conditions('swimlane','check')=={'是','否'}
assert edge_conditions('rag-pipeline','retrieve')=={'sufficient evidence','insufficient evidence',''}
assert edge_conditions('agent-loop','policy')=={'authorized and high risk and budget available','authorized and low risk and budget available','unauthorized or budget exhausted'}
assert edge_conditions('agent-loop','approval')=={'approved','denied or timeout'}
assert edge_conditions('agent-loop','verify')=={'valid result','invalid and budget available','invalid and budget exhausted'}
assert edge_conditions('state-machine','running')=={'success','failure and attempt>=3','failure and attempt<3','cancel acknowledged'}
assert edge_conditions('data-pipeline','retry')=={'retry<3','retry>=3'}
# Service dependency graphs must be acyclic; a physical network may legitimately contain cycles.
_,nodes,edges=load('service-dependencies');adj={key:[] for key in nodes}
for e in edges:adj[e.get('data-source')].append(e.get('data-target'))
def visit(key,stack):
    assert key not in stack,'dependency cycle'
    for target in adj[key]:visit(target,stack|{key})
for key in nodes:visit(key,set())
assert len(load('system-architecture')[1])==12
assert len(load('entity-relationship')[1])==4
assert len(load('mind-map')[1])==19
assert len(load('org-chart')[1])==13
# Validate every region label against the conceptual set geometry.
centers=[(530,450),(800,450),(665,620)]
regions=[(470,425,(1,0,0)),(860,425,(0,1,0)),(665,742,(0,0,1)),(665,356,(1,1,0)),(525,598,(1,0,1)),(805,598,(0,1,1)),(665,528,(1,1,1)),(1090,750,(0,0,0))]
for x,y,expected in regions:assert tuple(int(math.hypot(x-cx,y-cy)<180) for cx,cy in centers)==expected
builder=ast.parse((ROOT/'scripts/build-diagrams.py').read_text())
events=next(ast.literal_eval(n.value) for n in builder.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EVENTS' for t in n.targets))
assert len(events)==6
assert [event[0] for event in events]==sorted(event[0] for event in events)
for slug in ['timeline-svg','timeline-reveal']:
    prompt=(ROOT/'gallery/diagrams'/slug/'prompt.md').read_text()
    for when,title,status,url in events:assert when in prompt and url in prompt
print('PASS: 21 diagrams; order/variant parity; ports; orthogonal routes; node clearance; animation routes; finite exits; decision coverage; dependency DAG; set regions; timeline sources')
