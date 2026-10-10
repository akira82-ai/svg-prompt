#!/usr/bin/env python3
"""Check actual SVG geometry against independent mathematical identities."""
from pathlib import Path
import json,math,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'gallery/science';NS={'s':'http://www.w3.org/2000/svg'}
def svg(slug):return E.parse(BASE/slug/'index.svg').getroot()
def nodes(slug,attr):return [n for n in svg(slug).iter() if attr in n.attrib]
def points(d):
    nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?',d)));return list(zip(nums[::2],nums[1::2]))
def close(a,b,tol=.0002):assert math.isclose(a,b,abs_tol=tol),(a,b)
def area(ps):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ps,ps[1:]+ps[:1])))/2
def tracks(n):return {a.get('attributeName'):a.get('values').split(';') for a in n.findall('s:animate',NS)}
entries=sorted(BASE.glob('*/meta.json'),key=lambda p:json.loads(p.read_text())['order']);assert len(entries)==16
assert [json.loads(p.read_text())['order'] for p in entries]==list(range(1,17))
for p in entries:
    m=json.loads(p.read_text());root=svg(p.parent.name)
    assert (p.parent/'prompt.md').is_file()
    assert root.get('viewBox')=='0 0 1400 900'
    assert not root.findall('.//s:script',NS)
    if m['time']=='smil':
        assert 'prefers-reduced-motion:reduce' in ''.join(root.itertext())
        assert any(n.get('class')=='fallback' for n in root.iter())
        for a in root.findall('.//s:animate',NS):
            values=a.get('values').split(';');times=list(map(float,a.get('keyTimes').split(';')))
            assert len(times)==len(values) and times[0]==0 and times[-1]==1
            assert all(x<y for x,y in zip(times,times[1:]))
for i,n in enumerate(nodes('lissajous','data-a')):
    a,b,d=float(n.get('data-a')),float(n.get('data-b')),float(n.get('data-phase'));ps=points(n.get('d'));assert len(ps)==721
    for j,(x,y) in enumerate(ps):
        t=j*2*math.pi/720;close(x,265+i*435+145*math.sin(a*t+d));close(y,510-145*math.sin(b*t))
spiral=nodes('golden-spiral','data-growth')[0];growth=float(spiral.get('data-growth'));close(math.exp(growth*math.pi/2),(1+math.sqrt(5))/2)
for n in nodes('catenary','data-model'):
    ps=points(n.get('d'))
    for x,y in ps:
        vx=-2+(x-130)/720*4;vy=(720-y)/420*3
        expected=math.cosh(vx)-1 if n.get('data-model')=='catenary' else (math.cosh(2)-1)*vx*vx/4
        close(vy,expected)
# Bernstein form validates the final De Casteljau point independently.
curve=svg('bezier-de-casteljau').find("s:path[@id='bezier-curve']",NS)
control=[(150,650),(280,305),(670,310),(820,650)]
def bernstein(t):return tuple(sum(math.comb(3,i)*(1-t)**(3-i)*t**i*control[i][k] for i in range(4)) for k in range(2))
for j,p in enumerate(points(curve.get('d'))):
    for a,b in zip(p,bernstein(j/400)):close(a,b)
motion=svg('bezier-de-casteljau').find("s:g[@class='motion']",NS);circles=motion.findall('s:circle',NS);tr=tracks(circles[-1])
for j,(x,y) in enumerate(zip(tr['cx'],tr['cy'])):
    t=j/60 if j<=60 else 2-j/60
    for a,b in zip((float(x),float(y)),bernstein(t)):close(a,b)
for stage in [0,1,2,4]:
    tri=[points(n.get('d')) for n in nodes('sierpinski','data-stage') if int(n.get('data-stage'))==stage]
    assert len(tri)==3**stage
    close(sum(area(p) for p in tri)/(260*225.166604983954/2),(3/4)**stage,tol=.00001)
for n in nodes('koch-snowflake','data-stage'):
    stage=int(n.get('data-stage'));ps=points(n.get('d'));assert len(ps)-1==3*4**stage
    perimeter=sum(math.dist(a,b) for a,b in zip(ps,ps[1:]));close(perimeter/(3*220),(4/3)**stage,tol=.00001)
    close(area(ps)/(math.sqrt(3)*220**2/4),1+.6*(1-(4/9)**stage),tol=.00001)
for n in nodes('fourier-square','data-terms'):
    N=int(n.get('data-terms'));ps=points(n.get('d'));assert len(ps)==601
    for j,(x,y) in enumerate(ps):
        t=-math.pi+j*2*math.pi/600;expected=sum(math.sin(k*t)/k for k in range(1,2*N,2))*4/math.pi
        close((720-y)/420*3.2-1.6,expected)
static25=next(n.get('d') for n in nodes('fourier-square','data-terms') if n.get('data-terms')=='25')
animated=svg('fourier-build').find("s:path[@class='motion']",NS)
assert tracks(animated)['d'][-1]==static25
# Each sampled waveform must obey exact superposition at the same phase.
wave_paths=nodes('wave-interference','data-wave');assert len(wave_paths)==3
waveframes=[tracks(n)['d'] for n in wave_paths]
for j in range(49):
    ps=[points(frames[j]) for frames in waveframes]
    for k in range(361):
        t=j*2*math.pi/48;x=k*2*math.pi/360
        for index,expected in enumerate([math.sin(x-t),math.sin(x+t),2*math.sin(x)*math.cos(t)]):close((720-ps[index][k][1])/420*4.8-2.4,expected)
        close(ps[0][k][1]+ps[1][k][1]-510,ps[2][k][1])
standing=nodes('standing-wave','data-wave')[0]
assert tracks(standing)['d']==waveframes[2]
for d in tracks(standing)['d']:
    ps=points(d)
    for index in [0,180,360]:close(ps[index][1],510)
# Principal rays share object/image endpoints and satisfy the focal construction.
rays=nodes('thin-lens','data-ray');assert len(rays)==3
for n in rays:
    ps=points(n.get('d'));assert ps[0]==(230,385) and ps[-1]==(860,595)
close(1/3+1/1.5,1);close(-1.5/3,-.5)
# Recover eccentric anomaly from rendered planet positions; check uniform mean anomaly.
planet=svg('orbit-gravity').find("s:circle[@class='motion']",NS);tr=tracks(planet);positions=list(zip(map(float,tr['cx']),map(float,tr['cy'])))
for j,(x,y) in enumerate(positions):
    c=(x-490)/240;s=(525-y)/192;close(c*c+s*s,1,tol=.000002)
    anomaly=math.atan2(s,c)%(2*math.pi)
    if j==96:anomaly=2*math.pi
    close(anomaly-.6*math.sin(anomaly),j*2*math.pi/96,tol=.000002)
focus=(634,525);assert math.dist(focus,positions[0])<math.dist(focus,positions[48])
assert math.dist(positions[0],positions[1])>math.dist(positions[48],positions[49])
sectors=[points(n.get('d')) for n in nodes('orbit-gravity','data-sector')]
close(area(sectors[0]),area(sectors[1]),tol=.3)
for sector in sectors:close(area(sector),240*192*math.pi/8,tol=.3)
for n in nodes('solar-system','data-planet'):
    a,T=float(n.get('data-a')),float(n.get('data-period'));close(T*T,a**3,tol=.000001)
    for anim in n.findall('s:animate',NS):close(float(anim.get('dur')[:-1]),12*T,tol=.000001)
for panel in range(3):
    edges=[n for n in nodes('three-d','data-panel') if int(n.get('data-panel'))==panel];assert len(edges)==12
    pairs=[tuple(map(int,n.get('data-edge').split(','))) for n in edges];assert len(set(pairs))==12
    assert all(sum(i in edge for edge in pairs)==3 for i in range(8))
# Validate projection coordinates, not only the cube connectivity.
verts=[(x,y,z) for x in [-1,1] for y in [-1,1] for z in [-1,1]]
def projected(p,panel):
    x,y,z=p
    u=math.cos(math.pi/6)*x+math.sin(math.pi/6)*z;d=-math.sin(math.pi/6)*x+math.cos(math.pi/6)*z
    v=math.cos(math.pi/9)*y-math.sin(math.pi/9)*d;depth=math.sin(math.pi/9)*y+math.cos(math.pi/9)*d
    if panel==1:u,v=4*u/(4+depth),4*v/(4+depth)
    if panel==2:u,v=(x-z)/math.sqrt(2),(2*y-x-z)/math.sqrt(6)
    return 270+430*panel+100*u,510-100*v
for n in nodes('three-d','data-panel'):
    panel=int(n.get('data-panel'));i,j=map(int,n.get('data-edge').split(','))
    for key,expected in [('x1',projected(verts[i],panel)[0]),('y1',projected(verts[i],panel)[1]),('x2',projected(verts[j],panel)[0]),('y2',projected(verts[j],panel)[1])]:close(float(n.get(key)),expected)
boundary=points(nodes('topology-deform','data-boundary')[0].get('d'));assert len(boundary)==481
assert math.dist(boundary[0],boundary[-1])<.001 and math.dist(boundary[0],boundary[240])>100
for j,(X,Y) in enumerate(boundary):
    theta=j*4*math.pi/480;v=.35
    x=(1+v*math.cos(theta/2))*math.cos(theta);y=(1+v*math.cos(theta/2))*math.sin(theta);z=v*math.sin(theta/2)
    close(X,490+240*(.85*x-.45*y));close(Y,530-240*(.3*x+.55*y+.8*z))
steps=nodes('gradient-descent','data-step');assert len(steps)==11
for i,n in enumerate(steps):
    x,y=float(n.get('data-x')),float(n.get('data-y'));close(x,2*.6**i);close(y,1.5*(-.2)**i);close(float(n.get('data-loss')),x*x+3*y*y)
    if i:assert float(n.get('data-loss'))<float(steps[i-1].get('data-loss'))
print('PASS: 16 science entries; curves, fractal areas/perimeters, Fourier parity, synchronized waves, Kepler timing, optics, projection topology and gradient losses.')
