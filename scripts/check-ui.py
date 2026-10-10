#!/usr/bin/env python3
"""Validate product-state semantics and actual SVG data encodings."""
from pathlib import Path
from collections import Counter
import calendar,json,math,re,runpy,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'gallery/ui';NS={'s':'http://www.w3.org/2000/svg'}
SOURCE=runpy.run_path(str(ROOT/'scripts/build-ui.py'))
def svg(slug):return ET.parse(BASE/slug/'index.svg').getroot()
def nodes(slug,attr):return [e for e in svg(slug).iter() if attr in e.attrib]
def texts(slug):return [e.text or '' for e in svg(slug).findall('.//s:text',NS)]
def near(a,b,tol=.001):assert math.isclose(float(a),b,abs_tol=tol),(a,b)
def points(d):
    nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?',d)));return list(zip(nums[::2],nums[1::2]))
entries=sorted(BASE.glob('*/meta.json'),key=lambda p:json.loads(p.read_text())['order'])
expected=[slug for group,items in SOURCE['GROUPS'] for slug,title in items]
assert [p.parent.name for p in entries]==expected and len(entries)==60
assert [json.loads(p.read_text())['order'] for p in entries]==list(range(1,61))
for slug in SOURCE['REMOVED']:assert not (BASE/slug).exists()
for p in entries:
    slug=p.parent.name;m=json.loads(p.read_text());root=svg(slug)
    assert (p.parent/'prompt.md').is_file()
    assert root.get('viewBox')=='0 0 1400 900'
    ids=[e.get('id') for e in root.iter() if e.get('id')];assert len(ids)==len(set(ids))
    assert root.get('aria-labelledby')=='title desc'
    for e in root.iter():
        assert e.tag not in ['{http://www.w3.org/2000/svg}script','{http://www.w3.org/2000/svg}image','{http://www.w3.org/2000/svg}foreignObject']
        for k,v in e.attrib.items():
            assert not k.startswith('on')
            for ref in re.findall(r'url\(#([^)]*)\)',v):assert ref in ids
        if e.tag.endswith('rect'):
            assert float(e.get('width'))>=0 and float(e.get('height'))>=0
        if e.tag.endswith('animate'):
            values=e.get('values').split(';');times=list(map(float,e.get('keyTimes').split(';')))
            assert len(values)==len(times) and times[0]==0 and times[-1]==1
            assert all(a<b for a,b in zip(times,times[1:]))
    if m['time']=='smil':
        assert 'prefers-reduced-motion:reduce' in (p.parent/'index.svg').read_text()
        assert any(e.get('class')=='motion' for e in root.iter()) and any(e.get('class')=='fallback' for e in root.iter())
    else:assert not root.findall('.//s:animate',NS) and not root.findall('.//s:animateTransform',NS)
    for e in nodes(slug,'data-progress'):
        value,total,track=map(float,[e.get('data-progress'),e.get('data-total'),e.get('data-track')]);assert 0<=value<=total
        near(e.get('width'),track*value/total)
assert Counter(e.get('data-state') for e in nodes('buttons','data-state'))=={'default':2,'hover':2,'focus':2,'pressed':2,'disabled':2}
assert {'default','focus','error','disabled'}=={e.get('data-state') for e in nodes('input-states','data-state')}
for label in ['请输入完整的邮箱地址','此字段由组织管理员维护']:assert label in texts('input-states')
assert {e.get('data-state') for e in nodes('checkbox-radio','data-state')}=={'unchecked','checked','mixed'}
assert sum(e.get('data-disabled')=='true' for e in nodes('toggle','data-toggle'))==1
assert '锁定开启' in texts('toggle')
# Correct weekday, calendar cells, and inclusive range selection.
dates=nodes('date-range','data-date');assert len(dates)==31
for e in dates:
    day=int(e.get('data-date')[-2:]);weekday=calendar.weekday(2026,10,day);index=day+2
    near(e.get('x'),203+72*weekday);near(e.get('y'),491+52*(index//7))
assert [int(e.get('data-day')) for e in nodes('date-range','data-day')]==list(range(5,12))
assert calendar.weekday(2026,10,10)==5 and '2026 年 10 月 10 日 · 星期六' in texts('todo-today')
assert '已完成 1 / 共 3 项' in texts('todo-today')
assert '显示 31–40 条 / 共 95 条 / 每页 10 条' in texts('pagination')
assert math.ceil(95/10)==10 and (4-1)*10+1==31
assert '已选 2 项 / 共 5 项 · 示例按更新时间降序' in texts('data-table')
assert texts('data-table').count('☑')==2 and texts('data-table').count('□')==3
assert texts('notification-center').count('未读 2    /    全部通知')==1
assert '7 天 · 含开始与结束日期' in texts('date-range')
assert [float(e.get('data-progress'))/float(e.get('data-total')) for e in nodes('pricing-usage','data-progress')]==[.8,.6,.8]
assert [float(e.get('data-progress')) for e in nodes('file-upload','data-progress')]==[64]
near(4/6.25*100,64)
assert '¥199.00' in texts('checkout-payment') and '确认支付 ¥199.00' in texts('checkout-payment')
# Animated numeric stages keep text and bar in the same visibility group.
for e in nodes('number-roll','data-count-stage'):
    value=int(e.get('data-count-stage'));bar=next(n for n in e.iter() if n.get('data-progress'))
    assert int(bar.get('data-progress'))==value
    assert str(value) in [n.text for n in e.findall('s:text',NS)]
assert '50 → 100 → 150 · 循环为演示，非真实任务增长' in texts('number-roll')
assert not any('%' in t for t in texts('indeterminate-progress'))
# Alert text is never inside an animated opacity group.
alert=svg('alert-blink')
for g in alert.findall('.//s:g',NS):
    if g.find('s:animate',NS) is not None:assert not g.findall('.//s:text',NS)
assert '连接异常' in texts('alert-blink')
for label in ['等待确认','尚未开始 / 确认后才可继续','write_project / 尚未授权']:assert label in texts('agent-execution')
for label in ['[1] 第 4 页','[2] 第 7 页']:assert label in texts('ai-chat-workbench')
assert len([t for t in texts('members-permissions') if t in ('所有者','管理员','编辑者','查看者')])==4
assert {'待开始 · 2','进行中 · 2','已完成 · 1'}<=set(texts('kanban-board'))
def snapshot(slug):return ET.tostring(svg(slug).find("s:g[@id='dashboard-snapshot']",NS))
assert snapshot('bi-dashboard')==snapshot('dashboard')
assert snapshot('dark-ops-dashboard')==snapshot('live-ops-dashboard')
series=list(map(float,nodes('bi-dashboard','data-series')[0].get('data-series').split(',')))
assert sum(series)==128450
near(128450/840,152.92,tol=.005)
assert '3.86%' in texts('bi-dashboard')
assert [float(e.get('data-progress')) for e in nodes('bi-dashboard','data-progress')]==[40,30,20,10]
ops=list(map(float,nodes('dark-ops-dashboard','data-series')[0].get('data-series').split(',')));assert ops[-1]==46.2
assert texts('dark-ops-dashboard').count('正常')==3 and texts('dark-ops-dashboard').count('降级')==1
for slug in ['bi-dashboard','dark-ops-dashboard']:
    e=nodes(slug,'data-series')[0];values=list(map(float,e.get('data-series').split(',')));maximum=float(e.get('data-maximum'))
    for j,((x,y),v) in enumerate(zip(points(e.get('d')),values)):
        near(x,370+j*73);near(y,716-v/maximum*155)
kpi=[list(map(float,e.get('data-kpi-series').split(','))) for e in nodes('kpi-cards','data-kpi-series')]
assert [s[-1] for s in kpi]==[128450,840,3.86,2.1]
near((128450/114279-1)*100,12.4,tol=.001);near((840/800-1)*100,5)
near(kpi[2][-1]-kpi[2][0],-.4);near(kpi[3][-1]-kpi[3][0],-.4)
for e in nodes('fitness-dashboard','data-ring'):
    r=float(e.get('r'));value,total=float(e.get('data-ring')),float(e.get('data-total'));dash=float(e.get('stroke-dasharray').split()[0]);near(dash,2*math.pi*r*value/total)
assert sum(float(e.get('data-minutes')) for e in nodes('fitness-dashboard','data-minutes'))==170
assert '1:20' in texts('music-player') and '4:00' in texts('music-player')
assert [float(e.get('data-progress'))/float(e.get('data-total')) for e in nodes('music-player','data-progress')]==[1/3]
bearing=points(nodes('hud-interface','data-bearing')[0].get('d'));dx,dy=bearing[1][0]-bearing[0][0],bearing[1][1]-bearing[0][1];near(math.degrees(math.atan2(dx,-dy)),68)
# Frequency peaks must be the DFT of the displayed signal, not decorative random bars.
N=128;signal=[math.sin(2*math.pi*3*n/N)+.5*math.sin(2*math.pi*8*n/N) for n in range(N)]
for e in nodes('wave-analyzer','data-bin'):
    k=int(e.get('data-bin'));real=sum(v*math.cos(2*math.pi*k*n/N) for n,v in enumerate(signal));imag=sum(v*math.sin(2*math.pi*k*n/N) for n,v in enumerate(signal));amplitude=2*math.hypot(real,imag)/N
    near(e.get('data-amplitude'),amplitude,tol=.00000001);near(e.get('height'),85*amplitude)
    if k not in (3,8):assert amplitude<1e-12
# Deleted works must not survive in generated navigation or live prompts.
for p in [ROOT/'README.md',ROOT/'scripts/build-readme.mjs']+list((ROOT/'gallery').glob('*/*/prompt.md')):
    for slug in SOURCE['REMOVED']:assert 'ui/'+slug+'/' not in p.read_text(),p
print('PASS: 60 UI specimens; states, dates, selection counts, progress ratios, finance, dashboard parity, agent confirmation, HUD bearing and signal spectrum.')
