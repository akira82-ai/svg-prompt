#!/usr/bin/env python3
"""Build coherent icon specimens using local, reusable SVG symbols."""
import json
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'gallery/icons'
ENTRIES=[('icon-construction','图标构形与光学校正','Icon Construction'),('icon-set','线性图标系统','Outline Icons'),('solid-icons','实心图标系统','Solid Icons'),('duotone-icons','双色图标系统','Duotone Icons'),('small-size-icons','小尺寸图标','Small-size Icons'),('arrows','方向与箭头','Directional Symbols'),('status-symbols','状态与反馈符号','Status Symbols'),('file-type-icons','文件与格式图标','File Type Icons'),('technology-icons','科技产品图标','Technology Icons'),('app-icon','App 图标家族','App Icon Family'),('wayfinding-symbols','场所与导视符号','Wayfinding Symbols'),('symbol-morph','状态切换动效','Animated State Transitions')]
PATHS={
'home':'M3 10 12 3 21 10 M5 9v12h5v-7h4v7h5V9',
'search':'M16 16l5 5 M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
'heart':'M12 21C-2 12 2 1 9 5l3 3 3-3c7-4 11 7-3 16Z',
'bell':'M5 17h14l-2-3V9a5 5 0 0 0-10 0v5Z M10 21h4 M12 2v2',
'user':'M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0 M4 21v-2a8 8 0 0 1 16 0v2',
'mail':'M3 5h18v14H3Z M3 6l9 7 9-7',
'camera':'M3 7h5l2-3h4l2 3h5v14H3Z M16 14a4 4 0 1 1-8 0 4 4 0 0 1 8 0',
'settings':'M3 7h18 M3 17h18 M8 4v6 M16 14v6',
'check':'M5 12l5 5L20 6', 'close':'M5 5l14 14 M19 5 5 19',
'warning':'M12 3 22 21H2Z M12 9v5 M12 17v.2',
'info':'M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0 M12 11v6 M12 7v.2',
'clock':'M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0 M12 6v6l4 3',
'cloud':'M7 19h11a4 4 0 0 0 1-8 7 7 0 0 0-13-3 5.5 5.5 0 0 0 1 11Z',
'chip':'M6 6h12v12H6Z M9 9h6v6H9Z M9 2v4 M15 2v4 M9 18v4 M15 18v4 M2 9h4 M2 15h4 M18 9h4 M18 15h4',
'database':'M3 6C3 1 21 1 21 6S3 11 3 6v12c0 5 18 5 18 0V6 M3 12c0 5 18 5 18 0',
'shield':'M12 2 21 6v6c0 5-5 8-9 10-4-2-9-5-9-10V6Z M8 12l3 3 5-6',
'model':'M12 2 22 8v9l-10 5-10-5V8Z M2 8l10 6 10-6 M12 14v8',
'network':'M10 2h4v4h-4Z M2 18h4v4H2Z M18 18h4v4h-4Z M12 6v6 M4 18v-6h16v6',
'arrow':'M3 12h18 M14 5l7 7-7 7',
'upload':'M12 17V3 M5 10l7-7 7 7 M3 16v5h18v-5',
'download':'M12 3v14 M5 10l7 7 7-7 M3 16v5h18v-5',
'external':'M14 3h7v7 M21 3 11 13 M10 4H3v17h17v-7',
'file':'M5 2h9l5 5v15H5Z M14 2v6h5',
'coffee':'M3 8h13v8a5 5 0 0 1-10 0V8 M16 8h2a3 3 0 0 1 0 6h-2 M6 3v2 M10 2v3 M14 3v2 M3 22h15',
'lift':'M3 2h18v20H3Z M8 8l4-4 4 4 M8 16l4 4 4-4',
'exit':'M11 3H3v18h8 M9 12h13 M17 7l5 5-5 5',
'accessible':'M10 5a2 2 0 1 1 0-4 2 2 0 0 1 0 4 M10 7v7h7l4 7 M10 10h7 M7 10a6 6 0 1 0 8 8',
'parking':'M7 22V2h7a6 6 0 0 1 0 12H7',
'restroom':'M6 5a2 2 0 1 1 0-4 2 2 0 0 1 0 4 M3 8h6v7H3Z M4 15v7 M8 15v7 M18 5a2 2 0 1 1 0-4 2 2 0 0 1 0 4 M18 8l-4 9h8Z M16 17v5 M20 17v5'}
SOLIDS={
'home':'M2 10 12 2 22 10h-3v12h-5v-8h-4v8H5V10Z',
'search':'M10 2a8 8 0 1 0 5.6 13.7L21 21l2-2-5.3-5.4A8 8 0 0 0 10 2Z M10 5a5 5 0 1 1 0 10 5 5 0 0 1 0-10Z',
'heart':PATHS['heart'], 'bell':'M12 3a6 6 0 0 0-6 6v5l-3 4h18l-3-4V9a6 6 0 0 0-6-6Z M9 20a3 3 0 0 0 6 0Z',
'user':'M12 2a5 5 0 1 0 0 10 5 5 0 0 0 0-10 M3 22v-2a9 7 0 0 1 18 0v2Z',
'mail':'M2 5h20v15H2Z M4 7l8 6 8-6v3l-8 6-8-6Z',
'camera':'M2 7h5l2-4h6l2 4h5v15H2Z M12 10a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z',
'settings':'M2 5H6V2h4v3h12v3H10v3H6V8H2Z M2 16h12v-3h4v3h4v3h-4v3h-4v-3H2Z'}
BASE=list(SOLIDS)
LABELS=dict(zip(BASE,['首页','搜索','收藏','通知','账户','邮件','相机','设置']))
class Plate:
 def __init__(self,slug,title,en,order):
  self.slug,self.title,self.en,self.order=slug,title,en,order;self.a=[];self.labels=[];self.notes=[]
  self.add('<rect width="1400" height="900" fill="#f2f5f9"/><path d="M64 166h1272" stroke="#c8d2df"/>')
  self.text(64,65,'VECTOR SYSTEMS / '+f'{order:02}',14,'#516478');self.text(64,116,title,34);self.text(1336,116,en,20,'#516478','end')
  defs=''.join(f'<symbol id="{k}" viewBox="0 0 24 24"><path d="{d}"/></symbol>' for k,d in PATHS.items())+''.join(f'<symbol id="solid-{k}" viewBox="0 0 24 24"><path fill-rule="evenodd" d="{d}"/></symbol>' for k,d in SOLIDS.items())
  self.add('<defs>'+defs+'</defs>')
 def add(self,s):self.a.append(s)
 def text(self,x,y,s,size=18,color='#172b42',anchor='start'):
  self.labels.append(s);self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')
 def rect(self,x,y,w,h,fill='#fff',rx=0):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>')
 def icon(self,k,x,y,size=96,color='#172b42',solid=False,weight=1.6):
  self.add(f'<use href="#{"solid-" if solid else ""}{k}" x="{x}" y="{y}" width="{size}" height="{size}" color="{color}" fill="{"currentColor" if solid else "none"}" stroke="{"none" if solid else "currentColor"}" stroke-width="{weight}" stroke-linecap="round" stroke-linejoin="round"/>')
 def grid(self,items,mode='outline'):
  for i,item in enumerate(items):
   k,cn=item[:2];en=item[2] if len(item)>2 else k.upper()
   x=64+(i%4)*324;y=206+(i//4)*290;self.rect(x,y,300,266)
   if mode=='duotone':self.rect(x+98,y+38,104,104,'#dbe7ff',24)
   self.icon(k,x+102,y+42,96,'#245ee8' if mode=='duotone' else '#172b42',mode=='solid')
   self.text(x+24,y+196,cn,22);self.text(x+24,y+230,en,13,'#516478')
 def finish(self):
  self.text(64,858,self.notes[0],16,'#516478')
  anim=self.slug=='symbol-morph'
  if anim:self.add('<style>.fallback{display:none}@media(prefers-reduced-motion:reduce){.motion{display:none}.fallback{display:inline}}</style>')
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc" font-family="PingFang SC, Microsoft YaHei, sans-serif"><title id="title">{self.title} / {self.en}</title><desc id="desc">{escape("；".join(self.notes))}</desc>'+''.join(self.a)+'</svg>\n'
  d=OUT/self.slug;d.mkdir(exist_ok=True);(d/'index.svg').write_text(svg)
  old=json.loads((d/'meta.json').read_text()) if (d/'meta.json').exists() else {'author':'airay1015','date':'2026-10-10'}
  old.update(slug=self.slug,title=self.title,space='2d',time='smil' if anim else 'static',order=self.order,description=self.notes[0],tech=['symbol','use','currentColor','SMIL' if anim else '24px grid'])
  (d/'meta.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
  prompt=['用 SVG 制作“'+self.title+' / '+self.en+'”。','- 画布1400×900，背景#f2f5f9，正文#172b42，辅助文字#516478，强调色#245ee8；顶部中英文名称，主体y206..786，页脚y858。','- 图标使用24×24局部坐标，默认1.6单位描边、圆端点与圆拐角；symbol/use复用轮廓，颜色由currentColor继承。']+['- '+n for n in self.notes]+['- 可见文字：'+json.dumps(self.labels,ensure_ascii=False),'逐一复现以下本页使用的符号路径（24×24 viewBox）：']
  used=[k for k in PATHS if f'href="#{k}"' in svg or f'href="#solid-{k}"' in svg]
  prompt += [f'- {k}: {PATHS[k]}' for k in used]
  if self.slug=='solid-icons':prompt += [f'- 实心{k}: {SOLIDS[k]}（evenodd填充）' for k in BASE]
  (d/'prompt.md').write_text(f'# {self.title} / {self.en}\n\n分类：[图标与符号](../_about.md)\n\n<img src="index.svg" width="720" alt="{self.title}">\n\n```\n'+'\n'.join(prompt)+'\n```\n')
def render(p):
 s=p.slug
 if s in ['icon-set','solid-icons','duotone-icons']:
  p.grid([(k,LABELS[k]) for k in BASE],{'icon-set':'outline','solid-icons':'solid','duotone-icons':'duotone'}[s]);p.notes=['同一组八种功能语义，保持一致网格、视觉重量与中英文名称。','线性版1.6单位描边；实心版使用独立闭合轮廓与evenodd内孔；双色版淡蓝底形加蓝色前景，不依赖颜色区分功能。']
 elif s=='icon-construction':
  p.rect(64,206,700,580);x,y,u=145,260,18
  for i in range(25):p.add(f'<path d="M{x+i*u} {y}v432 M{x} {y+i*u}h432" stroke="#d5deea" stroke-width="1"/>')
  p.icon('camera',x,y,432);p.add(f'<rect x="{x+2*u}" y="{y+2*u}" width="360" height="360" fill="none" stroke="#245ee8" stroke-dasharray="7 7"/>')
  p.text(100,753,'24 × 24 / 2u 基础留白',20)
  p.text(815,245,'OPTICAL BALANCE',18,'#245ee8')
  p.add('<path d="M805 360h460" stroke="#c8d2df" stroke-dasharray="4 4"/>');p.icon('search',825,300,120);p.icon('heart',1095,310,120)
  p.text(815,465,'斜向延伸与尖端需要独立校正',22)
  p.text(815,523,'圆形、方形、斜线不能只比边界框。',18)
  p.text(815,574,'以实际尺寸复核重心、留白和线宽。',18)
  p.text(815,645,'收藏相对基线下移 10px（示例校正）',18,'#245ee8');p.text(815,707,'构形参考，不宣称自动获得视觉等重。',17,'#516478')
  p.notes=['构形网格是共同起点，最终视觉重量仍需实际尺寸判断。','左侧相机24单位网格放大18倍；2..22为基础安全区，底边可按轮廓校正。右侧搜索y300、收藏y310，120px显示尺寸，收藏相对几何位置下移10px；虚线y360为共同几何中线，示例校正仍需用户测试。']
 elif s=='small-size-icons':
  p.rect(64,206,1272,580)
  for i,size in enumerate([16,20,24,32]):
   x=145+i*310;p.text(x,260,str(size)+'px / 1:1',22)
   p.icon('search',x,305,size,weight=2 if size<=20 else 1.6);p.icon('mail',x+70,305,size,weight=2 if size<=20 else 1.6)
   p.text(x,407,'8× 细节放大',16,'#516478');p.icon('search',x,440,size*8,weight=2 if size<=20 else 1.6)
   p.text(x,750,'2u 描边' if size<=20 else '1.6u 描边',18)
  p.notes=['上排按SVG原始像素展示；缩略图会缩放，1:1需原图100%查看。','16/20px使用2单位笔画；24/32px使用1.6单位；同一搜索与信封形状比较，底部8倍放大。']
 elif s=='arrows':
  p.grid([('arrow','前进','FORWARD'),('upload','上传','UPLOAD'),('download','下载','DOWNLOAD'),('external','外部打开','OPEN EXTERNAL'),('arrow','返回','BACK'),('arrow','向上','UP'),('arrow','向下','DOWN'),('exit','离开','EXIT')])
  # Rotate the last three ordinary arrows around their own centers.
  for i,deg in [(4,180),(5,-90),(6,90)]:
   x=64+i%4*324+102;y=206+i//4*290+42
   old=f'<use href="#arrow" x="{x}" y="{y}"';p.a=[a.replace(old,f'<use transform="rotate({deg} {x+48} {y+48})" href="#arrow" x="{x}" y="{y}"') for a in p.a]
  p.notes=['统一箭头端点、斜边和笔触；方向与操作语义分开命名。','前进、返回、向上、向下共用同一轮廓，以各自中心旋转0/180/-90/90度；上传/下载保留托盘，外部打开保留容器边界。']
 elif s=='status-symbols':
  items=[('check','成功','#16734b'),('warning','警告','#925600'),('close','错误','#bd3442'),('info','提示','#245ee8'),('clock','等待','#516478'),('shield','已保护','#16734b')]
  for i,(k,cn,c) in enumerate(items):
   x=64+i%3*432;y=206+i//3*290;p.rect(x,y,408,266);p.add(f'<circle cx="{x+80}" cy="{y+86}" r="48" fill="none" stroke="{c}" stroke-width="2"/>') if k in ['check','close'] else None;p.icon(k,x+44,y+50,72,c);p.text(x+145,y+85,cn,25);p.text(x+145,y+121,k.upper(),14,'#516478');p.text(x+24,y+222,'形状 + 文案 + 语义色',17,'#516478')
  p.notes=['状态不只靠红绿区分：轮廓、文字与颜色共同表达。','成功/错误圆形容器，警告三角、提示圆圈、等待钟表、防护盾牌；等待为静态符号，不假装实时进度。']
 elif s=='file-type-icons':
  for i,(tag,cn,c) in enumerate([('DOC','文档','#245ee8'),('PDF','阅读','#bd3442'),('CSV','表格','#16734b'),('SVG','矢量','#6b4dc4'),('PNG','图像','#925600'),('MP4','视频','#245ee8'),('ZIP','归档','#516478'),('JSON','数据','#16734b')]):
   x=64+i%4*324;y=206+i//4*290;p.rect(x,y,300,266);p.icon('file',x+95,y+28,110);p.rect(x+75,y+110,150,42,c,4);p.text(x+150,y+138,tag,21,'#fff','middle');p.text(x+24,y+209,cn,22)
  p.notes=['共同文件轮廓与明确格式缩写，缩写承担区分功能。','八种格式DOC/PDF/CSV/SVG/PNG/MP4/ZIP/JSON；折角与文字牌共享位置，色彩只作辅助。']
 elif s=='technology-icons':
  p.grid([('model','模型'),('chip','算力'),('cloud','云端'),('database','数据'),('shield','安全'),('network','网络'),('search','检索'),('settings','配置')]);p.notes=['科技产品的常见能力符号，不把抽象图标当架构说明。','立方体表示模型、芯片表示算力、圆柱表示数据；八项使用共同笔触与留白。']
 elif s=='app-icon':
  for i,(k,name,c) in enumerate([('model','MODEL','#245ee8'),('database','DATA','#16734b'),('shield','SECURE','#6b4dc4'),('network','CONNECT','#172b42')]):
   x=96+i*320;p.rect(x,250,240,240,c,54);p.icon(k,x+56,306,128,'#fff');p.text(x+120,543,name,20,'#172b42','middle')
   for j,size in enumerate([24,40,64]):p.rect(x+j*78,600,size,size,c,size*.225);p.icon(k,x+j*78+size*.22,600+size*.22,size*.56,'#fff');p.text(x+j*78,709,str(size)+'px',15,'#516478')
  p.notes=['四枚科技App图标共享圆角、构形与单色反白，下面展示实际尺寸。','240px主体圆角54px，为普通圆角矩形，不冒称平台专用超椭圆；小样24/40/64px，图形占容器56%。']
 elif s=='wayfinding-symbols':
  p.grid([('exit','出口'),('lift','电梯'),('accessible','无障碍'),('parking','停车'),('coffee','茶歇'),('info','咨询'),('arrow','前往'),('restroom','卫生间')]);p.notes=['导视概念样例：附文字辅助识别，不声称符合标准认证。','出口、电梯、无障碍、停车、茶歇、咨询、方向、卫生间，统一笔触；公共场所应用需另核验当地规范和可读距离。']
 elif s=='symbol-morph':
  for i,(name,en) in enumerate([('播放 → 暂停','PLAY / PAUSE'),('菜单 → 关闭','MENU / CLOSE')]):
   x=64+i*648;p.rect(x,206,624,580,'#172b42');p.text(x+40,260,en,18,'#b9cdf6');p.text(x+40,735,name,26,'#fff')
   p.add(f'<g transform="translate({x+232} 386) scale(6.6667)" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">')
   pairs=[('M6 3L6 21','M8 4L8 20'),('M6 3L21 12L6 21','M16 4L16 12L16 20')] if i==0 else [('M3 5L21 5','M5 5L19 19'),('M3 12L21 12','M12 12L12 12'),('M3 19L21 19','M5 19L19 5')]
   for start,end in pairs:p.add(f'<path class="motion" d="{start}"><animate attributeName="d" values="{start};{end}" begin=".6s" dur=".8s" fill="freeze"/></path><path class="fallback" d="{end}"/>')
   p.add('</g>')
  p.notes=['两组有明确操作含义的状态过渡，一次播放后保持终态。','播放→暂停由三角形两条分段轮廓转换为双竖线；菜单→关闭保留两条对角线、中线收缩；对应路径指令一致，.6秒等待、.8秒过渡，fill=freeze；减少动效隐藏motion显示终态fallback。']
 else:raise ValueError(s)
def build():
 for i,(slug,title,en) in enumerate(ENTRIES,1):
  p=Plate(slug,title,en,i);render(p);p.finish()
 print('Built 12 icon specimens.')
if __name__=='__main__':build()
