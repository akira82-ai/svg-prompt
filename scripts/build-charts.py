#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the curated data charts from explicit synthetic data; no dependencies."""
from pathlib import Path
from html import escape
from datetime import date, timedelta
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'gallery' / 'charts'
COLORS = ['#2678d9', '#00a887', '#ed9c35', '#9268cf', '#df647a', '#5896a0']
CHARTS = []

class Chart:
    def __init__(self, slug, title, subtitle, finding, dark=False, animated=False):
        self.slug, self.title, self.subtitle, self.finding = slug, title, subtitle, finding
        self.dark, self.animated = dark, animated
        self.bg = '#0d1724' if dark else '#f3f5f7'
        self.ink = '#edf3fa' if dark else '#172a3a'
        self.muted = '#a2b4c8' if dark else '#596e81'
        self.grid = '#293b4d' if dark else '#dce4eb'
        self.parts = []
        self.requirements = []
        self.rect(0, 0, 1200, 800, self.bg)
        self.text(72, 56, 'SVG / DATA ATLAS', 14, self.muted, mono=True)
        self.line(72, 72, 1128, 72, self.grid)
        self.text(72, 119, title, 32, weight=700)
        self.text(72, 155, subtitle, 18, self.muted)
        self.rect(72, 178, 1056, 49, '#172c40' if dark else '#e7edf3', rx=5)
        self.text(91, 210, finding, 18, weight=600)
        self.line(72, 714, 1128, 714, self.grid)
        self.text(72, 746, '模拟数据 · 用于图型演示，不代表真实产品或行业结论', 15, self.muted)
        self.text(1128, 746, 'SVG-PROMPT', 14, self.muted, anchor='end', mono=True)

    def add(self, s): self.parts.append(s)
    def text(self, x, y, text, size=17, fill=None, anchor='start', weight=400, mono=False):
        font = 'SFMono-Regular, Consolas, monospace' if mono else 'PingFang SC, Microsoft YaHei, sans-serif'
        self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{fill or self.ink}" text-anchor="{anchor}" font-weight="{weight}" font-family="{font}">{escape(str(text))}</text>')
    def rect(self, x, y, w, h, fill, rx=0, attrs=''):
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" fill="{fill}" {attrs}/>')
    def line(self, x1, y1, x2, y2, fill=None, width=1, attrs=''):
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{fill or self.grid}" stroke-width="{width}" {attrs}/>')
    def circle(self, x, y, r, fill, attrs=''):
        self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" {attrs}/>')
    def path(self, d, fill='none', stroke=None, width=2, attrs=''):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{width}" {attrs}/>')
    def legend(self, items, x=140, y=257, gap=190):
        for i,(label,color) in enumerate(items):
            self.rect(x+i*gap,y-12,13,13,color,rx=2)
            self.text(x+i*gap+23,y,label,15,self.muted)
    def axes(self, xmin, xmax, ymin, ymax, xticks, yticks, xlabel, ylabel, bounds=(145,300,925,350)):
        x,y,w,h=bounds
        sx=lambda v:x+(v-xmin)/(xmax-xmin)*w
        sy=lambda v:y+h-(v-ymin)/(ymax-ymin)*h
        for v in yticks:
            self.line(x,sy(v),x+w,sy(v));self.text(x-16,sy(v)+5,f'{v:g}',15,self.muted,anchor='end',mono=True)
        self.line(x,y+h,x+w,y+h,self.muted)
        for v,label in xticks:
            self.text(sx(v),y+h+28,label,15,self.muted,anchor='middle')
        self.text(x,y-17,ylabel,15,self.muted)
        self.text(x+w,y+h+53,xlabel,15,self.muted,anchor='end')
        return sx,sy
    def reveal(self):
        # CSS clipping reveals fixed geometry; reduced motion keeps the final chart visible.
        self.add(f'<style>.reveal{{clip-path:inset(0 0 0 0);animation:reveal 8s infinite}}@keyframes reveal{{0%,5%{{clip-path:inset(0 100% 0 0)}}35%,92%{{clip-path:inset(0 0 0 0)}}100%{{clip-path:inset(0 100% 0 0)}}}}@media(prefers-reduced-motion:reduce){{.reveal{{animation:none;clip-path:none}}}}</style><g class="reveal">')
    def end_reveal(self):self.add('</g>')
    def finish(self, requirements, tech):
        self.requirements=requirements
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc"><title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.finding)}。模拟数据，{escape(self.subtitle)}。</desc>'+''.join(self.parts)+'</svg>\n'
        p=OUT/self.slug;p.mkdir(exist_ok=True)
        (p/'index.svg').write_text(svg,encoding='utf-8')
        old=json.loads((p/'meta.json').read_text()) if (p/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
        old.update(slug=self.slug,title=self.title,space='2d',time='css' if self.animated else 'static',tech=tech,description=self.finding)
        (p/'meta.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        steps=[f'用 SVG 制作“{self.title}”，主题为{self.subtitle}。',f'- 画布 1200×800，背景 {self.bg}；标题 32px、正文 17–18px、轴标签不小于 15px；主图区留白，不使用装饰性发光。',f'- 图中重点结论：“{self.finding}”。']+['- '+s for s in requirements]+['- 底部注明“模拟数据 · 用于图型演示，不代表真实产品或行业结论”；所有量纲、刻度、图例与数据对应。']
        if self.animated:steps+=['- 固定数据几何，只用 CSS clip-path 做 8 秒循环揭示：0–5%隐藏、35–92%显示完整终态、末段重置；不修改数据坐标、数值或任务日期。prefers-reduced-motion: reduce 时显示完整静态图；不支持动画时也显示终态。']
        label='CSS 动效' if self.animated else '静态'
        (p/'prompt.md').write_text(f'# {self.title} `{label}` `2D`\n\n分类：[数据图表](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+ '\n'.join(steps)+'\n```\n',encoding='utf-8')
        CHARTS.append(self.slug)


def poly(points, close=False):
    return 'M '+' L '.join(f'{x:.3f} {y:.3f}' for x,y in points)+(' Z' if close else '')

def bar(animated=False):
    a=[42,55,61,70,84,92];b=[36,44,50,58,66,72]
    c=Chart('bar-growth' if animated else 'bar','柱状图 · 动态揭示' if animated else '分组柱状图','月度推理请求 / 百万次','六月请求量：本期 92，基期 72；同月增长 27.8%',animated=animated)
    c.legend([('本期',COLORS[0]),('基期',COLORS[5])])
    sx,sy=c.axes(-0.5,5.5,0,100,[(i,f'{i+1}月') for i in range(6)],[0,20,40,60,80,100],'月份','请求 / 百万次',bounds=(170,300,870,350))
    if animated:c.reveal()
    for i,(v,u) in enumerate(zip(a,b)):
        for dx,value,color in [(-32,v,COLORS[0]),(4,u,COLORS[5])]:
            c.rect(sx(i)+dx,sy(value),28,sy(0)-sy(value),color,attrs=f'data-value="{value}" data-scale="3.5"')
            c.text(sx(i)+dx+14,sy(value)-10,value,15,anchor='middle',mono=True)
    if animated:c.end_reveal()
    c.finish(['本期数据42/55/61/70/84/92，基期36/44/50/58/66/72，X轴1–6月，Y轴0–100百万次，柱高=数值×3.5px，零基线固定。','分组而非重叠；本期蓝色、基期灰青；标签与柱同步揭示。'],['rect','分组比较','零基线']+(['CSS clip-path'] if animated else []))


def ranking():
    names=['Vector-A','Vector-B','Vector-C','Vector-D','Vector-E'];vals=[182,156,129,104,86]
    c=Chart('ranking-lollipop','排名棒棒糖图','固定负载下的模拟吞吐量 / tokens·s⁻¹','Vector-A 吞吐量最高；比 Vector-B 高 16.7%',dark=True)
    x0,x1=340,1050;scale=(x1-x0)/200
    for t in range(0,201,50):c.line(x0+t*scale,290,x0+t*scale,640);c.text(x0+t*scale,676,t,15,c.muted,anchor='middle',mono=True)
    for i,(name,v) in enumerate(zip(names,vals)):
        y=325+i*68;c.text(110,y+6,name,19,mono=True);c.line(x0,y,x0+v*scale,y,COLORS[1] if i==0 else '#526e8c',4);c.circle(x0+v*scale,y,9,COLORS[1] if i==0 else '#87a2bf',attrs=f'data-value="{v}"');c.text(x0+v*scale+20,y+5,v,17,mono=True)
    c.finish(['模型名称均为虚构，数据182/156/129/104/86，按降序排列。','X轴0–200 tokens/s，从零开始，x=340+3.55v；每行连接线与圆点，第一名绿色突出，不使用真实模型排名。'],['circle','排序','position'])


def bullet():
    c=Chart('bullet-chart','子弹图','服务指标 / 实际、目标与评价区间','吞吐量超过目标；成功率与延迟目标仍需改善',dark=True)
    rows=[('吞吐量 / req·s⁻¹',820,750,1000,[400,700,1000],False),('成功率 / %',96,98,100,[85,95,100],False),('P95 延迟 / ms',210,180,400,[180,250,400],True)]
    c.legend([('实际值',COLORS[0]),('目标线',COLORS[2])],x=280)
    for i,(name,actual,target,maxv,bands,inverse) in enumerate(rows):
        y=320+i*125;x=330;scale=620/maxv;c.text(96,y+25,name,17)
        start=0
        fills=['#425870','#34485e','#263a50'] if not inverse else ['#263a50','#34485e','#425870']
        for end,fill in zip(bands,fills):c.rect(x+start*scale,y,(end-start)*scale,40,fill);start=end
        c.rect(x,y+12,actual*scale,16,COLORS[0],attrs=f'data-value="{actual}" data-scale="{scale}"')
        c.line(x+target*scale,y-5,x+target*scale,y+45,COLORS[2],3)
        for t in [0,maxv/2,maxv]:c.text(x+t*scale,y+64,f'{t:g}',14,c.muted,anchor='middle',mono=True)
        c.text(980,y+20,f'{actual} / {target}',17,mono=True);c.text(980,y+47,'越低越好' if inverse else '越高越好',14,c.muted)
    c.finish(['三指标分别：吞吐量实际820/目标750/轴上限1000；成功率96/98/100；P95延迟210/180/400。','区间阈值分别400/700/1000、85/95/100、180/250/400；各行独立量纲，不比较条长。延迟越低越好，明确标出方向。','绘图区x=330至950，实际条宽=实际值/轴上限×620，橙色目标竖线。'],['rect','target marker','独立量纲'])


def dumbbell():
    names=['检索','重排','生成','后处理'];before=[120,90,260,60];after=[72,54,182,42]
    c=Chart('dumbbell','哑铃图','管线优化前后 / 延迟 ms','四个阶段均缩短；生成阶段减少 78 ms，绝对改善最大')
    c.legend([('优化前',COLORS[5]),('优化后',COLORS[0])],x=310)
    for t in range(0,301,50):c.line(310+t*2.4,295,310+t*2.4,635);c.text(310+t*2.4,672,t,15,c.muted,anchor='middle',mono=True)
    for i,(n,a,b) in enumerate(zip(names,before,after)):
        y=330+i*83;c.text(120,y+6,n,19);c.line(310+b*2.4,y,310+a*2.4,y,c.muted,3)
        c.circle(310+a*2.4,y,8,COLORS[5]);c.circle(310+b*2.4,y,8,COLORS[0]);c.text(310+b*2.4,y-18,b,15,COLORS[0],anchor='middle',mono=True);c.text(310+a*2.4,y+31,a,15,c.muted,anchor='middle',mono=True)
    c.finish(['四阶段优化前120/90/260/60ms，优化后72/54/182/42ms；X轴0–300ms，x=310+2.4v。','每行用线连接同一阶段前后两点，优化前灰青、优化后蓝色；标注实际值。'],['circle','paired comparison'])


def line_chart(animated=False):
    actual=[42,55,61,70,84,92];forecast=[40,52,64,73,82,96];low=[35,46,56,64,72,82];high=[45,58,72,82,93,110]
    c=Chart('line-draw' if animated else 'line','折线图 · 动态揭示' if animated else '趋势与预测区间','推理请求 / 百万次；预测区间为演示范围','实际请求持续增长；六月 92 落在演示预测区间 82–110 内',animated=animated)
    c.legend([('实际',COLORS[0]),('预测虚线',COLORS[5]),('演示区间','#c7dae9')],gap=220)
    sx,sy=c.axes(0,5,0,120,[(i,f'{i+1}月') for i in range(6)],[0,30,60,90,120],'月份','请求 / 百万次')
    if animated:c.reveal()
    c.path(poly([(sx(i),sy(v)) for i,v in enumerate(high)]+[(sx(i),sy(low[i])) for i in reversed(range(6))],True),'#dce8f3')
    c.path(poly([(sx(i),sy(v)) for i,v in enumerate(forecast)]),stroke=COLORS[5],attrs='stroke-dasharray="7 6"')
    c.path(poly([(sx(i),sy(v)) for i,v in enumerate(actual)]),stroke=COLORS[0],width=3)
    for i,v in enumerate(actual):c.circle(sx(i),sy(v),5,COLORS[0])
    c.text(sx(5)-12,sy(92)+28,'92',17,COLORS[0],anchor='end',mono=True)
    if animated:c.end_reveal()
    c.finish(['实际42/55/61/70/84/92；预测40/52/64/73/82/96；下界35/46/56/64/72/82，上界45/58/72/82/93/110。','X轴1–6月，Y轴0–120；蓝色实际实线、灰青预测虚线、浅蓝区间。区间仅为演示范围，不称统计置信区间。'],['path','预测区间','stroke-dasharray']+(['CSS clip-path'] if animated else []))


def area(animated=False):
    edge=[24,30,35,42,48,56];cloud=[18,21,25,28,31,36];total=[a+b for a,b in zip(edge,cloud)]
    c=Chart('area-expand' if animated else 'area','面积图 · 动态揭示' if animated else '堆叠面积图','推理请求构成 / 百万次','六月总量 92；边缘端贡献 56，占总量 60.9%',animated=animated)
    c.legend([('边缘端',COLORS[0]),('云端',COLORS[1])])
    sx,sy=c.axes(0,5,0,100,[(i,f'{i+1}月') for i in range(6)],[0,20,40,60,80,100],'月份','累计请求 / 百万次')
    if animated:c.reveal()
    c.path(poly([(sx(i),sy(v)) for i,v in enumerate(edge)]+[(sx(5),sy(0)),(sx(0),sy(0))],True),COLORS[0],attrs='fill-opacity="0.75"')
    c.path(poly([(sx(i),sy(v)) for i,v in enumerate(total)]+[(sx(i),sy(edge[i])) for i in reversed(range(6))],True),COLORS[1],attrs='fill-opacity="0.65"')
    c.path(poly([(sx(i),sy(v)) for i,v in enumerate(total)]),stroke=COLORS[1],width=3)
    c.text(sx(5)-10,sy(92)-12,'总量 92',17,COLORS[1],anchor='end')
    if animated:c.end_reveal()
    c.finish(['边缘端24/30/35/42/48/56，云端18/21/25/28/31/36；上边界逐项相加为42/51/60/70/79/92。','X轴1–6月，Y轴0–100百万次；下层从零到边缘端，上层从边缘端到累计总量，不采用相互遮盖的独立面积。'],['path','累计边界']+(['CSS clip-path'] if animated else []))


def waterfall():
    vals=[120,-24,-18,-12,8,74];names=['基准成本','缓存','量化','批处理','观测开销','最终成本']
    c=Chart('waterfall','成本瀑布图','每百万次推理成本 / 模拟货币单位','120 − 24 − 18 − 12 + 8 = 74；净成本下降 38.3%',dark=True)
    c.legend([('总量',COLORS[0]),('减少',COLORS[1]),('增加',COLORS[2])],gap=175)
    sx,sy=c.axes(-0.5,5.5,0,140,[(i,n) for i,n in enumerate(names)],[0,35,70,105,140],'成本项','成本 / 模拟单位',bounds=(180,300,840,350))
    current=0
    for i,v in enumerate(vals):
        if i in (0,5):start,end=0,v
        else:start,end=current,current+v
        color=COLORS[0] if i in (0,5) else COLORS[1] if v<0 else COLORS[2]
        c.rect(sx(i)-36,sy(max(start,end)),72,abs(sy(start)-sy(end)),color,attrs=f'data-start="{start}" data-end="{end}" data-scale="2.5"')
        c.text(sx(i),sy(max(start,end))-13,str(v) if i in (0,5) else f'{v:+}',17,color,anchor='middle',mono=True)
        current=end
        if i<5:c.line(sx(i)+36,sy(current),sx(i+1)-36,sy(current),c.muted,attrs='stroke-dasharray="4 4"')
    c.finish(['起点120，缓存-24、量化-18、批处理-12、观测开销+8，终点74；逐项累加，连接线对应累计值。','Y轴0–140，绘图高度350px；减少绿色、增加橙色、总量蓝色。每个浮动柱跨越调整前后的真实累计值。'],['rect','累计增减','waterfall'])


def small_multiples():
    data=[[20,24,32,40,49,60],[35,36,40,45,51,58],[12,18,26,38,52,70],[60,58,55,52,50,48]]
    names=['北部节点','东部节点','南部节点','西部节点']
    c=Chart('small-multiples','小多图','四个区域的请求趋势 / 百万次','南部节点增长最快：12 → 70；西部节点持续回落')
    for i,(name,vals) in enumerate(zip(names,data)):
        col,row=i%2,i//2;x=160+col*530;y=320+row*200;w=360;h=120
        c.text(x,y-20,name,19,weight=600)
        for v in [0,40,80]:c.line(x,y+h-v/80*h,x+w,y+h-v/80*h);c.text(x-12,y+h-v/80*h+5,v,14,c.muted,anchor='end',mono=True)
        pts=[(x+j*w/5,y+h-v/80*h) for j,v in enumerate(vals)]
        c.path(poly(pts),stroke=COLORS[i],width=3)
        for px,py in pts:c.circle(px,py,4,COLORS[i])
        for j in [0,2,5]:c.text(x+j*w/5,y+h+25,f'{j+1}月',14,c.muted,anchor='middle')
        c.text(x+w+10,pts[-1][1]+5,vals[-1],16,COLORS[i],mono=True)
    c.finish(['四组数据：北部20/24/32/40/49/60、东部35/36/40/45/51/58、南部12/18/26/38/52/70、西部60/58/55/52/50/48。','2×2布局；所有子图共用Y轴0–80百万次、X轴1–6月与同样绘图区尺寸，不独立缩放制造差异。'],['small multiples','共用尺度','path'])


SAMPLES=[88,92,95,98,102,106,108,110,112,114,115,116,118,120,122,124,126,128,130,132,135,138,142,146,150,156,164,178,215,260]
def quantile(data,p):
    s=sorted(data);idx=(len(s)-1)*p;lo=math.floor(idx);hi=math.ceil(idx)
    return s[lo]+(s[hi]-s[lo])*(idx-lo)


def histogram():
    edges=list(range(80,281,20));counts=[sum(a<=v<b or (i==9 and v==b) for v in SAMPLES) for i,(a,b) in enumerate(zip(edges,edges[1:]))]
    c=Chart('histogram-boxplot','延迟直方图','30 次模拟请求 / 延迟分布','多数请求落在 100–140 ms；右侧存在长尾')
    sx,sy=c.axes(80,280,0,10,[(i,str(i)) for i in range(80,281,40)],[0,2,4,6,8,10],'延迟 / ms','请求数 / 次')
    for i,count in enumerate(counts):
        c.rect(sx(edges[i])+1,sy(count),sx(edges[i+1])-sx(edges[i])-2,sy(0)-sy(count),COLORS[0],attrs=f'data-count="{count}" data-scale="35"')
        if count:c.text((sx(edges[i])+sx(edges[i+1]))/2,sy(count)-10,count,16,anchor='middle',mono=True)
    c.finish(['数据集 '+json.dumps(SAMPLES)+'；每箱20ms，区间[80,100)、[100,120)…，最后一箱[260,280]含右端点。','10箱频数'+json.dumps(counts)+'，总计30；Y轴人数0–10，柱高=频数×35px，等宽箱紧密排列。'],['binning','rect','frequency'])


def boxplot():
    q1,q2,q3=[quantile(SAMPLES,p) for p in [.25,.5,.75]];iqr=q3-q1;low=q1-1.5*iqr;high=q3+1.5*iqr;inside=[v for v in SAMPLES if low<=v<=high];out=[v for v in SAMPLES if not low<=v<=high]
    c=Chart('boxplot','延迟箱线图','与直方图共用 30 次请求 / Tukey 须线','中位数 123 ms；215 与 260 ms 被识别为离群值',dark=True)
    sx=lambda v:170+(v-80)/200*880
    for v in range(80,281,40):c.line(sx(v),300,sx(v),575);c.text(sx(v),620,v,16,c.muted,anchor='middle',mono=True)
    y=420;c.line(sx(min(inside)),y,sx(max(inside)),y,COLORS[0],3)
    for v in [min(inside),max(inside)]:c.line(sx(v),y-22,sx(v),y+22,COLORS[0],3)
    c.rect(sx(q1),y-45,sx(q3)-sx(q1),90,'#1e4161',attrs=f'stroke="{COLORS[0]}" stroke-width="2" data-q1="{q1}" data-q3="{q3}"')
    c.line(sx(q2),y-45,sx(q2),y+45,COLORS[1],4)
    for v in out:c.circle(sx(v),y,7,COLORS[2]);c.text(sx(v),y-25,v,16,COLORS[2],anchor='middle',mono=True)
    for v,label,yy in [(min(inside),'下须 88',y+85),(q1,f'Q1 {q1:g}',y-75),(q2,f'中位 {q2:g}',y+85),(q3,f'Q3 {q3:g}',y-75),(max(inside),'上须 178',y+85)]:c.text(sx(v),yy,label,16,c.muted,anchor='middle')
    c.text(170,671,f'IQR = {iqr:g} ms   ·   离群阈值 {low:g}–{high:g} ms',16,c.muted,mono=True)
    c.finish(['数据集与延迟直方图一致：'+json.dumps(SAMPLES)+'。','分位数使用线性插值索引(n−1)p；Q1='+str(q1)+'，中位数='+str(q2)+'，Q3='+str(q3)+'，IQR='+str(iqr)+'。','Tukey阈值Q1−1.5IQR和Q3+1.5IQR；须端为阈值内实际最小/最大值88/178，不把须端写成全样本min/max；离群点215/260。'],['quantile','Tukey fences','outliers'])


def violin():
    groups=[[84,90,94,98,103,107,112,116,121,126,132,140],[110,117,126,136,148,159,171,182,194,206,224,244],[76,79,83,86,90,92,95,99,104,112,126,158]]
    c=Chart('violin','请求延迟小提琴图','三个模拟服务 / 高斯 KDE，带宽 15 ms','服务 B 分布偏高且更分散；每组仅 12 个样本')
    sx,sy=c.axes(0,2,40,280,[(0,'服务 A'),(1,'服务 B'),(2,'服务 C')],[40,100,160,220,280],'服务组','延迟 / ms',bounds=(300,300,600,350))
    ys=[40+i*2 for i in range(121)];densities=[[sum(math.exp(-.5*((y-v)/15)**2) for v in data)/(len(data)*15*math.sqrt(2*math.pi)) for y in ys] for data in groups];maxd=max(max(d) for d in densities)
    for i,(data,dens) in enumerate(zip(groups,densities)):
        widths=[70*d/maxd for d in dens];points=[(sx(i)-w,sy(y)) for y,w in zip(ys,widths)]+[(sx(i)+widths[j],sy(ys[j])) for j in reversed(range(len(ys)))]
        c.path(poly(points,True),COLORS[i],COLORS[i],attrs='fill-opacity="0.25"')
        for j,v in enumerate(data):c.circle(sx(i)+(j%3-1)*8,sy(v),3,COLORS[i])
        median=statistics.median(data);c.line(sx(i)-20,sy(median),sx(i)+20,sy(median),COLORS[i],4)
    c.finish(['三组各12个样本：'+json.dumps(groups)+'；高斯KDE带宽h=15ms，y从40到280按2ms采样。','密度为sum(exp(−0.5((y−v)/h)²))/(n·h·sqrt(2π))；三组共用密度最大值归一化，最大半宽70px，不能分别放大。','叠加原始样本点及中位数横线；Y轴共用40–280ms，不将小样本密度外观当总体结论。'],['KDE','shared density scale','raw samples'])


def interval():
    groups=[[72,75,78,74,76],[81,83,80,84,82],[76,79,77,80,78],[84,87,85,86,88]];names=['方案 A','方案 B','方案 C','方案 D'];critical=2.776445105
    c=Chart('interval','均值与置信区间','每方案 5 次独立模拟重复 / 得分','展示均值及 95% t 区间；区间重叠本身不等于显著性检验')
    for v in range(65,96,5):x=320+(v-65)/30*720;c.line(x,290,x,640);c.text(x,673,v,15,c.muted,anchor='middle',mono=True)
    for i,(name,data) in enumerate(zip(names,groups)):
        y=330+i*88;mean=statistics.mean(data);margin=critical*statistics.stdev(data)/math.sqrt(len(data));lo,hi=mean-margin,mean+margin;sx=lambda v:320+(v-65)/30*720
        c.text(115,y+6,name,19);c.line(sx(lo),y,sx(hi),y,COLORS[i],4)
        for v in [lo,hi]:c.line(sx(v),y-12,sx(v),y+12,COLORS[i],2)
        c.circle(sx(mean),y,7,COLORS[i]);c.text(sx(mean),y-25,f'{mean:.1f} [{lo:.1f}, {hi:.1f}]',15,COLORS[i],anchor='middle',mono=True)
    c.finish(['四组模拟重复：'+json.dumps(groups)+'；每组n=5，以独立重复与近似正态为演示前提。','95%双侧均值t区间：mean±t(0.975,df=4)·s/√5，t=2.776445105，s为样本标准差(ddof=1)。','X轴65–95分，点表示均值、横线表示区间、端点短竖线；不凭区间是否重叠直接作显著性结论。'],['Student t','sample standard deviation','error bars'])


def scatter():
    xs=[10+3*i for i in range(24)];ys=[12+.72*x+[2,-4,3,-2,5,-1][i%6] for i,x in enumerate(xs)];ys[-1]=35
    mx,my=statistics.mean(xs),statistics.mean(ys);slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs);intercept=my-slope*mx
    c=Chart('scatter','散点与回归','模拟广告投入 / 万元；销量 / 千件',f'全样本 OLS：销量 ≈ {intercept:.2f} + {slope:.2f} × 投入；相关不代表因果')
    sx,sy=c.axes(0,90,0,80,[(v,str(v)) for v in [0,30,60,90]],[0,20,40,60,80],'投入 / 万元','销量 / 千件')
    c.path(poly([(sx(x),sy(intercept+slope*x)) for x in [0,90]]),stroke=c.muted,attrs='stroke-dasharray="7 6"')
    for i,(x,y) in enumerate(zip(xs,ys)):c.circle(sx(x),sy(y),6,COLORS[2] if i==23 else COLORS[0],attrs=f'fill-opacity="0.8" data-x="{x}" data-y="{y}"')
    c.circle(sx(xs[-1]),sy(ys[-1]),14,'none',attrs=f'stroke="{COLORS[2]}" stroke-width="2"');c.text(sx(xs[-1])-20,sy(ys[-1])+35,'高投入、低销量',16,COLORS[2],anchor='end')
    c.finish(['x='+json.dumps(xs)+'；y='+json.dumps(ys)+'；最后一点作为低销量异常示例。','使用全部24点计算OLS：b=sum((x−meanX)(y−meanY))/sum((x−meanX)²)，a=meanY−b·meanX；a='+str(intercept)+'，b='+str(slope)+'。','X轴0–90万元，Y轴0–80千件，虚线是数据计算的回归线，不是手绘趋势；注明相关不代表因果。'],['OLS','circle','outlier'])


def bubble():
    data=[('A1',10,72,20),('A2',25,65,40),('A3',45,54,80),('B1',20,42,30),('B2',40,34,60),('B3',62,26,100),('C1',68,74,25),('C2',82,58,50),('C3',92,40,15)]
    c=Chart('bubble','三变量气泡图','增长率 × 毛利率 × 市场规模','位置编码两个比例；气泡面积编码模拟市场规模')
    c.legend([('产品线 A',COLORS[0]),('产品线 B',COLORS[1]),('产品线 C',COLORS[2])])
    sx,sy=c.axes(0,100,0,100,[(v,str(v)) for v in [0,25,50,75,100]],[0,25,50,75,100],'增长率 / %','毛利率 / %',bounds=(145,315,680,330))
    for name,x,y,v in data:
        color=COLORS[ord(name[0])-65];c.circle(sx(x),sy(y),4*math.sqrt(v),color,attrs=f'fill-opacity="0.45" stroke="{color}" data-size="{v}"');c.text(sx(x),sy(y)+5,name,15,anchor='middle',weight=600)
    c.text(910,323,'规模 / 模拟单位',16,c.muted)
    for i,v in enumerate([20,50,100]):
        yy=400+i*100;c.circle(954,yy,4*math.sqrt(v),'none',attrs=f'stroke="{c.muted}" data-size="{v}"');c.text(1020,yy+5,v,16,c.muted,mono=True)
    c.finish(['数据(产品,增长%,毛利%,规模)：'+json.dumps(data)+'。','所有气泡含尺寸图例使用r=4√规模，因此面积=16π×规模；X、Y轴均0–100%，不使用半径直接编码规模。','绘图区680×330px，图例右置，不掩盖数据；产品线按色分组。'],['area encoding','circle','size legend'])


def matrix():
    names=['Vector-A','Vector-B','Vector-C','Vector-D','Vector-E'];tasks=['检索','推理','代码','摘要','多语'];data=[[84,72,68,88,76],[78,86,82,80,74],[75,78,91,79,70],[89,74,72,85,87],[80,81,79,83,82]]
    c=Chart('matrix-heatmap','任务表现矩阵','虚构模型 × 任务 / 模拟得分 0–100','各模型有不同优势；不以单项最高分代替总体排名',dark=True)
    x0,y0,cw,ch=320,316,125,62
    for j,name in enumerate(tasks):c.text(x0+j*cw+cw/2,y0-20,name,17,anchor='middle')
    def color(v):
        t=v/100;return '#'+''.join(f'{round(a+(b-a)*t):02x}' for a,b in zip((22,43,65),(60,205,174)))
    for i,(name,row) in enumerate(zip(names,data)):
        c.text(112,y0+i*ch+38,name,18,mono=True)
        for j,v in enumerate(row):c.rect(x0+j*cw,y0+i*ch,cw-4,ch-4,color(v),rx=3,attrs=f'data-value="{v}"');c.text(x0+j*cw+(cw-4)/2,y0+i*ch+37,v,19,'#081f2b',anchor='middle',weight=700,mono=True)
    c.text(965,330,'得分',15,c.muted)
    for k in range(101):c.rect(980,355+(100-k)*2,25,2,color(k))
    for v in [0,50,100]:c.text(1020,360+(100-v)*2,v,15,c.muted,mono=True)
    c.finish(['虚构模型A–E，任务检索/推理/代码/摘要/多语，5×5矩阵：'+json.dumps(data)+'。','共用0–100顺序色阶，从RGB(22,43,65)线性插值到(60,205,174)；不得按每行各自归一化。','格内显示数值，右侧完整色标，颜色之外保留文本编码，不宣称真实模型性能。'],['matrix','sequential color scale','text labels'])


def calendar():
    start=date(2026,1,5);vals=[(i*7+i//7*3)%25 for i in range(140)];colors=['#e3e9ef','#bcdccb','#76bf9e','#369c78','#12734f']
    c=Chart('heatmap','日历热力图','2026-01-05 至 2026-05-24 / 140 天模拟活动','日期按真实日历排列；颜色表示每日请求批次数')
    x0,y0,step,size=210,320,41,34
    for j,name in enumerate(['一','二','三','四','五','六','日']):c.text(x0-22,y0+j*step+23,name,16,c.muted,anchor='end')
    lastmonth=None
    for i,v in enumerate(vals):
        d=start+timedelta(days=i);col,row=i//7,i%7;band=0 if v==0 else 1 if v<=5 else 2 if v<=10 else 3 if v<=15 else 4
        if row==0 and d.month!=lastmonth:c.text(x0+col*step,y0-22,f'{d.month}月',17,c.muted);lastmonth=d.month
        c.rect(x0+col*step,y0+row*step,size,size,colors[band],rx=3,attrs=f'data-date="{d.isoformat()}" data-value="{v}"')
    for i,label in enumerate(['0','1–5','6–10','11–15','16–24']):
        xx=310+i*150;c.rect(xx,650,22,22,colors[i],rx=3);c.text(xx+31,667,label,15,c.muted)
    c.finish(['从周一2026-01-05开始，连续140天，结束2026-05-24；列=周、行=星期一到日。','第i天的模拟批次数v=(7i+3⌊i/7⌋) mod 25；色阶明确为0、1–5、6–10、11–15、16–24；月标签依据该周周一的真实月份。'],['date arithmetic','discrete scale','rect'])


def radial_point(cx,cy,r,a):return cx+r*math.cos(a),cy+r*math.sin(a)
def sector(cx,cy,r0,r1,a,b):
    p1=radial_point(cx,cy,r1,a);p2=radial_point(cx,cy,r1,b);p3=radial_point(cx,cy,r0,b);p4=radial_point(cx,cy,r0,a);large=int(b-a>math.pi)
    if r0==0:return f'M {cx} {cy} L {p1[0]} {p1[1]} A {r1} {r1} 0 {large} 1 {p2[0]} {p2[1]} Z'
    return f'M {p1[0]} {p1[1]} A {r1} {r1} 0 {large} 1 {p2[0]} {p2[1]} L {p3[0]} {p3[1]} A {r0} {r0} 0 {large} 0 {p4[0]} {p4[1]} Z'


def pie():
    vals=[35,25,20,12,8];names=['计算','存储','网络','观测','其他']
    c=Chart('pie-donut','饼图与环形图','模拟基础设施成本构成 / 总额 100 单位','计算与存储合计占 60%；两种图型使用同一组数据')
    for cx,r0,label in [(340,0,'饼图'),(850,90,'环形图')]:
        c.text(cx,274,label,19,anchor='middle');angle=-math.pi/2
        for v,color in zip(vals,COLORS):
            end=angle+v/100*2*math.pi;c.path(sector(cx,460,r0,150,angle,end),color,c.bg,2,attrs=f'data-value="{v}" data-angle="{end-angle}"');px,py=radial_point(cx,460,177,(angle+end)/2);c.text(px,py+5,f'{v}%',16,anchor='middle',mono=True);angle=end
        if r0:c.text(cx,460,'100',30,anchor='middle',weight=700,mono=True);c.text(cx,488,'总成本',15,c.muted,anchor='middle')
    c.legend(list(zip(names,COLORS)),x=180,y=679,gap=170)
    c.finish(['五项成本计算35、存储25、网络20、观测12、其他8，共100；两图使用同一数据。','每扇区角度=份额×2π；饼图和环形图分列，不混入目标完成度仪表；百分比外标、图例底置。'],['arc','part-to-whole'])


def treemap():
    vals=[34,22,18,14,12];names=['计算','存储','网络','观测','其他'];c=Chart('treemap','矩形树图','基础设施预算 / 父类份额与子项','矩形面积对应预算份额；子项面积在各自父类内比较')
    x,y,w,h=160,310,880,340
    # Slice-and-dice layout preserves exact areas with no title band subtraction.
    placements=[(x,y,w*.56,h*34/56),(x,y+h*34/56,w*.56,h*22/56),(x+w*.56,y,w*.44,h*18/44),(x+w*.56,y+h*18/44,w*.44,h*14/44),(x+w*.56,y+h*32/44,w*.44,h*12/44)]
    for i,(v,name,(xx,yy,ww,hh)) in enumerate(zip(vals,names,placements)):
        c.rect(xx,yy,ww,hh,COLORS[i],attrs=f'data-share="{v}" stroke="{c.bg}" stroke-width="2"')
        parts=3 if i==0 else 2
        for j in range(1,parts):c.line(xx+ww*j/parts,yy,xx+ww*j/parts,yy+hh,c.bg,1)
        c.text(xx+14,yy+30,f'{name} {v}%',18,c.ink if i in (1,2) else '#ffffff',weight=600)
        for j in range(parts):c.text(xx+ww*(j+.5)/parts,yy+hh-18,f'{name[0]}-{j+1} · {100/parts:.1f}%',14,c.ink if i in (1,2) else '#ffffff',anchor='middle')
    c.finish(['五父类份额34/22/18/14/12%，总量100；整体绘图区880×340px。','左列宽56%，上下高度34/56与22/56；右列宽44%，三块高度18/44、14/44、12/44，父面积严格对应份额。','计算父类内等分3子项，其余父类内等分2子项；不扣除标题区而改变子项比例，子项百分比为父类内部占比，细描边分隔。'],['slice-and-dice','area encoding','hierarchy'])


def sunburst():
    parents=[('计算',[('推理',25),('训练',15)]),('存储',[('对象',15),('向量',10)]),('网络',[('出口',12),('内网',8)]),('其他',[('观测',9),('支持',6)])]
    c=Chart('sunburst','层级旭日图','预算总量 100 / 两层结构','父类等于子类之和；角度编码份额，环面积不直接比较')
    cx,cy=425,475;a=-math.pi/2
    for i,(parent,children) in enumerate(parents):
        total=sum(v for _,v in children);b=a+total/100*2*math.pi;c.path(sector(cx,cy,65,125,a,b),COLORS[i],c.bg,2)
        px,py=radial_point(cx,cy,94,(a+b)/2);c.text(px,py+5,str(total),17,'#ffffff' if i in (0,3) else c.ink,anchor='middle',weight=700)
        ca=a
        for child,v in children:
            cb=ca+v/100*2*math.pi;c.path(sector(cx,cy,129,190,ca,cb),COLORS[i],c.bg,2,attrs='fill-opacity="0.7"');px,py=radial_point(cx,cy,159,(ca+cb)/2);c.text(px,py+5,str(v),16,c.ink,anchor='middle');ca=cb
        c.rect(740,315+i*85,14,14,COLORS[i],rx=2);c.text(766,331+i*85,f'{parent} · {total}%',19,weight=600);c.text(766,360+i*85,' / '.join(f'{n} {v}%' for n,v in children),16,c.muted)
        a=b
    c.text(cx,cy+5,'100',27,anchor='middle',weight=700,mono=True)
    c.finish(['父类计算40=推理25+训练15、存储25=对象15+向量10、网络20=出口12+内网8、其他15=观测9+支持6。','父子沿相同全局100单位角尺度，子弧角度合计严格覆盖对应父弧；内环65–125px、外环129–190px。','图例完整列出父子名称与份额，说明角度编码，不拿不同半径环的扇区面积作直接比较。'],['arc','hierarchical sums'])


def radar():
    a=[82,76,90,68,84];b=[72,88,78,86,74];names=['检索','推理','代码','摘要','多语']
    c=Chart('radar','雷达图','五项模拟任务得分 / 共用 0–100 刻度','方案 A 与 B 各有优势；多边形面积不代表综合评分')
    c.legend([('方案 A',COLORS[0]),('方案 B',COLORS[2])],x=180)
    cx,cy,r=530,480,155;angles=[-math.pi/2+i*2*math.pi/5 for i in range(5)]
    for v in [20,40,60,80,100]:c.path(poly([radial_point(cx,cy,r*v/100,t) for t in angles],True),stroke=c.grid,width=1);c.text(cx+9,cy-r*v/100+5,v,13,c.muted,mono=True)
    for name,t in zip(names,angles):
        px,py=radial_point(cx,cy,r,t);c.line(cx,cy,px,py);px,py=radial_point(cx,cy,r+35,t);c.text(px,py+5,name,18,anchor='middle')
    for vals,color in [(a,COLORS[0]),(b,COLORS[2])]:
        pts=[radial_point(cx,cy,r*v/100,t) for v,t in zip(vals,angles)];c.path(poly(pts,True),color,color,2,attrs='fill-opacity="0.13"')
        for x,y in pts:c.circle(x,y,4,color)
    for i,name in enumerate(names):c.text(860,340+i*57,name,16,c.muted);c.text(985,340+i*57,f'{a[i]} / {b[i]}',16,anchor='end',mono=True)
    c.finish(['任务检索/推理/代码/摘要/多语；A=82/76/90/68/84，B=72/88/78/86/74。','所有轴0–100，五层20分刻度，半径155px；顶点半径=r·score/100；旁列数值，避免只读形状。','固定维度顺序，明确不得以多边形面积判断综合能力，不假设不同任务得分可直接加总。'],['polygon','shared scale','explicit values'])


def combo():
    sales=[120,132,145,150,168,180];growth=[10,10,9.8484848485,3.4482758621,12,7.1428571429]
    c=Chart('combo-dual-axis','双轴组合图','营收 / 模拟单位；环比 / %；首月前期基数约 109.09','柱与线使用不同单位；高度相似不代表两个指标相关')
    c.legend([('营收 · 左轴',COLORS[0]),('环比 · 右轴',COLORS[2])],gap=240)
    sx,sy=c.axes(-0.5,5.5,0,200,[(i,f'{i+1}月') for i in range(6)],[0,50,100,150,200],'月份','营收 / 模拟单位',bounds=(170,320,840,330))
    for i,v in enumerate(sales):c.rect(sx(i)-25,sy(v),50,sy(0)-sy(v),COLORS[0]);c.text(sx(i),sy(v)-12,v,15,COLORS[0],anchor='middle',mono=True)
    sy2=lambda v:650-v/20*330
    for t in [0,5,10,15,20]:c.text(1030,sy2(t)+5,f'{t}%',15,COLORS[2],mono=True)
    c.text(1000,299,'环比 / %',15,COLORS[2],anchor='end');c.path(poly([(sx(i),sy2(v)) for i,v in enumerate(growth)]),stroke=COLORS[2],width=3)
    for i,v in enumerate(growth):c.circle(sx(i),sy2(v),5,COLORS[2])
    c.finish(['营收120/132/145/150/168/180；首月环比10%，首月前期基数120/1.1；其余环比严格由(本月/前月−1)×100计算。','左轴0–200营收单位，右轴0–20%；轴、图例与数据按颜色对应；不通过裁剪轴范围制造趋势一致。','显式写出双轴不同量纲，不能依据视觉高度或形状推断相关性。'],['dual axes','derived growth'])


def funnel(animated=False):
    vals=[10000,4200,1800,1200,400];names=['访问','加购','下单','支付','复购']
    c=Chart('funnel-steps' if animated else 'funnel','漏斗图 · 动态揭示' if animated else '转化漏斗图','同一批访客的模拟转化 / 人数','累计复购率 4%；人数按等高矩形宽度编码',animated=animated)
    c.text(90,275,'阶段',16,c.muted);c.text(820,275,'人数 / 累计占比',16,c.muted);c.text(1120,275,'相邻转化率',16,c.muted,anchor='end')
    if animated:c.reveal()
    for i,(name,v) in enumerate(zip(names,vals)):
        y=307+i*71;w=520*v/10000;c.text(90,y+32,name,19);c.rect(490-w/2,y,w,47,COLORS[0],attrs=f'data-value="{v}" data-scale="0.052"');c.text(820,y+29,f'{v:,} / {v/100:.0f}%',17,mono=True)
        if i>0:c.text(1120,y+29,f'{v/vals[i-1]*100:.1f}%',17,COLORS[1],anchor='end',mono=True)
        else:c.text(1120,y+29,'—',17,c.muted,anchor='end')
    if animated:c.end_reveal()
    c.finish(['同一批访客依次访问10000、加购4200、下单1800、支付1200、复购400。','用居中等高矩形而非装饰梯形，最大宽520px，其余宽=人数/10000×520；因此宽度与面积都正比人数。','累计占比100/42/18/12/4%；相邻转化率42.0/42.9/66.7/33.3%，两种分母明确区分。'],['rect','conversion denominators']+(['CSS clip-path'] if animated else []))


def sankey(animated=False):
    c=Chart('sankey-flow' if animated else 'sankey','桑基图 · 动态揭示' if animated else '预算流量桑基图','算力预算 / 模拟单位；带宽与金额成正比','总预算 100 = 三个来源之和 = 四个去向之和',dark=True,animated=animated)
    inputs=[('核心预算',60),('项目预算',25),('弹性预算',15)];outputs=[('推理',45),('训练',25),('存储',18),('网络',12)];scale=2.5
    ys_in=[330,500,580];ys_out=[315,443,523,583];center_y=355
    c.text(155,274,'来源',16,c.muted);c.text(565,274,'汇总',16,c.muted);c.text(960,274,'去向',16,c.muted)
    if animated:c.reveal()
    offset=0
    for i,((name,v),y) in enumerate(zip(inputs,ys_in)):
        h=v*scale;mid=center_y+offset;d=f'M 260 {y} C 380 {y}, 430 {mid}, 550 {mid} L 550 {mid+h} C 430 {mid+h}, 380 {y+h}, 260 {y+h} Z';c.path(d,COLORS[i],attrs=f'fill-opacity="0.5" data-flow="{v}" data-thickness="{h}"');c.rect(245,y,15,h,COLORS[i]);c.text(230,y+h/2+5,f'{name} {v}',16,anchor='end');offset+=h
    c.rect(550,center_y,20,250,'#b3c6d9');c.text(560,center_y-16,'100',19,anchor='middle',mono=True)
    offset=0
    for i,((name,v),y) in enumerate(zip(outputs,ys_out)):
        h=v*scale;mid=center_y+offset;d=f'M 570 {mid} C 710 {mid}, 785 {y}, 930 {y} L 930 {y+h} C 785 {y+h}, 710 {mid+h}, 570 {mid+h} Z';c.path(d,COLORS[i],attrs=f'fill-opacity="0.5" data-flow="{v}" data-thickness="{h}"');c.rect(930,y,15,h,COLORS[i]);c.text(965,y+h/2+5,f'{name} {v}',17);offset+=h
    if animated:c.end_reveal()
    c.finish(['来源核心60、项目25、弹性15；去向推理45、训练25、存储18、网络12；两侧均合计100。','每单位2.5px，汇总节点高250px；来源与去向沿汇总节点连续分配对应端口，贝塞尔闭合飘带两端厚度均为v×2.5。','仅表达汇总流量，不推断某一来源与某一去向的对应分配；动画只揭示，不增加未经定义的流速或粒子密度编码。'],['closed ribbons','flow conservation']+(['CSS clip-path'] if animated else []))


def chord():
    names=['北区','东区','南区','西区'];matrix=[[0,18,12,8],[18,0,15,9],[12,15,0,10],[8,9,10,0]];sums=[sum(row) for row in matrix];total=sum(sums);gap=.08;scale=(2*math.pi-4*gap)/total
    c=Chart('chord-diagram','跨区域流量弦图','对称往来矩阵 / 模拟数据量 TB','每条弦的两端占用真实子弧；外环角度对应区域总往来量',dark=True)
    cx,cy,r=430,475,172;angle=-math.pi/2;arcs=[];segments={}
    for i,sm in enumerate(sums):
        end=angle+sm*scale;arcs.append((angle,end));sub=angle
        for j,v in enumerate(matrix[i]):
            if v:segments[(i,j)]=(sub,sub+v*scale);sub+=v*scale
        angle=end+gap
    for i in range(4):
        for j in range(i+1,4):
            a,b=segments[(i,j)];d,e=segments[(j,i)];p1,p2,p3,p4=[radial_point(cx,cy,r,t) for t in [a,b,d,e]];dpath=f'M {p1[0]} {p1[1]} A {r} {r} 0 0 1 {p2[0]} {p2[1]} Q {cx} {cy} {p3[0]} {p3[1]} A {r} {r} 0 0 1 {p4[0]} {p4[1]} Q {cx} {cy} {p1[0]} {p1[1]} Z';c.path(dpath,COLORS[i],attrs=f'fill-opacity="0.4" data-flow="{matrix[i][j]}" data-angle="{b-a}"')
    for i,(a,b) in enumerate(arcs):
        c.path(sector(cx,cy,177,194,a,b),COLORS[i]);x,y=radial_point(cx,cy,222,(a+b)/2);c.text(x,y+5,f'{names[i]} {sums[i]}',17,anchor='middle')
    c.text(755,301,'对称往来矩阵 / TB',18,weight=600)
    for j,n in enumerate(names):c.text(840+j*72,345,n,15,c.muted,anchor='middle')
    for i,row in enumerate(matrix):
        c.text(755,396+i*52,names[i],16,c.muted)
        for j,v in enumerate(row):c.text(840+j*72,396+i*52,v,17,anchor='middle',mono=True)
    c.text(755,643,'不表示迁移方向；对称总和含双计',15,c.muted)
    c.finish(['四区对称矩阵'+json.dumps(matrix)+'，单位TB，行和38/42/37/27，总和144（双向对称重复计数）。','外环四个间隙各0.08rad，角比例(2π−0.32)/144；每区域按行内数值顺序分配子弧。','每对i<j绘制一条闭合弦带，两端圆弧跨度均=matrix[i][j]×角比例，使用二次曲线连接；不是粗描边关系线。','矩阵和总量同步展示，数据对称不表示方向，双计口径明确。'],['chord ribbons','matrix layout','angular encoding'])


def gantt(animated=False):
    tasks=[('需求',1,5,1.0),('原型',6,10,1.0),('开发',11,19,.25),('集成',20,24,0),('测试',25,28,0),('上线',29,30,0)]
    c=Chart('gantt-progress' if animated else 'gantt','甘特图 · 动态揭示' if animated else '项目甘特图','30 天交付计划 / 第 12 日进度快照','条长编码排期，深色段编码完成比例；依赖从上一任务结束后开始',animated=animated)
    c.legend([('计划', '#c5d9ed'),('已完成',COLORS[0]),('今日线',COLORS[2])],gap=190)
    sx=lambda day:290+(day-1)/30*750
    for day in [1,5,10,15,20,25,30]:c.line(sx(day),295,sx(day),649);c.text(sx(day),680,day,15,c.muted,anchor='middle',mono=True)
    if animated:c.reveal()
    for i,(name,start,end,progress) in enumerate(tasks):
        y=308+i*56;w=(end-start+1)*25;c.text(110,y+25,name,18);c.rect(sx(start),y,w,32,'#c5d9ed',rx=3,attrs=f'data-start="{start}" data-end="{end}"');c.rect(sx(start),y,w*progress,32,COLORS[0],rx=3);c.text(1085,y+23,f'{progress:.0%}',16,c.muted,anchor='end',mono=True)
        if i<5:
            xx=sx(end+1);nx=sx(tasks[i+1][1]);c.path(f'M {xx} {y+16} L {xx+8} {y+16} L {xx+8} {y+48} L {nx} {y+48}',stroke=c.muted,width=1.5)
    c.line(sx(12),295,sx(12),649,COLORS[2],2,attrs='stroke-dasharray="5 4"');c.text(sx(12)+8,290,'今日 D12',15,COLORS[2]);c.circle(sx(31),608,6,COLORS[1]);c.text(sx(31)-8,658,'完成里程碑',15,COLORS[1],anchor='end')
    if animated:c.end_reveal()
    c.finish(['任务(名称,起日,止日,完成比例)：'+json.dumps(tasks,ensure_ascii=False)+'。','30个日区间，边界x=290+(day−1)×25；条长=(止日−起日+1)×25px，D30完整覆盖到D31边界。','第12日今日线固定；完成段=计划宽×完成比例，不用条长动画改变起止日期；连接依赖与D30结束里程碑。'],['date intervals','dependencies','progress overlay']+(['CSS clip-path'] if animated else []))


def build():
    CHARTS.clear()
    bar();bar(True);ranking();bullet();dumbbell();line_chart();line_chart(True);area();area(True);waterfall();small_multiples();histogram();boxplot();violin();interval();scatter();bubble();matrix();calendar();radar();combo();pie();treemap();sunburst();funnel();funnel(True);sankey();sankey(True);chord();gantt();gantt(True)
    for i,slug in enumerate(CHARTS,1):
        p=OUT/slug/'meta.json';m=json.loads(p.read_text());m['order']=i;p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(CHARTS)} charts from explicit synthetic datasets.')

if __name__ == '__main__':build()
