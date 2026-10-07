const fs = await import("node:fs/promises");
const SINA = Math.sin(20*Math.PI/180), COSA = Math.cos(20*Math.PI/180);
const f1 = n => (Math.round(n*10)/10).toString();
const f2 = n => (Math.round(n*100)/100).toString();

// 相机：yaw θ（绕竖轴）+ 俯角 20°，正交投影
function proj(x,y,z,th,cx,cy,s){ const c=Math.cos(th), sn=Math.sin(th);
  const x2=x*c-y*sn, y2=x*sn+y*c;
  return [f1(cx+x2*s), f1(cy-(y2*SINA+z*COSA)*s)]; }
const SPL = n => `calcMode="spline" keyTimes="${Array.from({length:n},(_,i)=>f2(i/(n-1))).join(";")}" keySplines="${Array.from({length:n-1},()=>".37 0 .63 1").join(";")}"`;
const vals = arr => arr.join(";");

// ============ P1 球面 ⇄ 圆环面（R: 62→0→62，9 关键帧） ============
const C1=[330,252], S1=1.75, r=26;
const RSEQ=[62,44,26,10,0,10,26,44,62];
function surfPt(u,v,Rr){ const x=(Rr+r*Math.cos(v))*Math.cos(u), y=(Rr+r*Math.cos(v))*Math.sin(u), z=r*Math.sin(v);
  return proj(x,y,z,0,C1[0],C1[1],S1); }
const NU=10, NV=6, NS=20;
let p1Rings='', p1Tubes='';
const ringD=RSEQ.map(Rr=>{
  let d='';
  for(let i=0;i<NU;i++){ const u=i/NU*2*Math.PI;
    const pts=Array.from({length:NS+1},(_,k)=>{ const [sx,sy]=surfPt(u,k/NS*2*Math.PI,Rr); return sx+","+sy; });
    d+="M"+pts.join(" L "); }
  return d; });
const tubeD=RSEQ.map(Rr=>{
  let d='';
  for(let j=0;j<NV;j++){ const v=j/NV*2*Math.PI;
    const pts=Array.from({length:NS+1},(_,k)=>{ const [sx,sy]=surfPt(k/NS*2*Math.PI,v,Rr); return sx+","+sy; });
    d+="M"+pts.join(" L "); }
  return d; });
const p1=`<path fill="none" stroke="#7ec2ff" stroke-width="1.1" opacity="0.55" d="${ringD[0]}"><animate attributeName="d" dur="10s" repeatCount="indefinite" ${SPL(9)} values="${vals(ringD)}"/></path>
    <path fill="none" stroke="#2bb3a3" stroke-width="1.1" opacity="0.55" d="${tubeD[0]}"><animate attributeName="d" dur="10s" repeatCount="indefinite" ${SPL(9)} values="${vals(tubeD)}"/></path>`;

// 金色主线：第一条 u 环随形变走 —— 单独生成
const goldRing=RSEQ.map(Rr=>{
  const u=0; const pts=Array.from({length:NS+1},(_,k)=>{ const [sx,sy]=surfPt(u,k/NS*2*Math.PI,Rr); return sx+","+sy; });
  return "M"+pts.join(" L "); });
const p1Gold=`<path fill="none" stroke="#ffd166" stroke-width="1.7" opacity="0.95" d="${goldRing[0]}"><animate attributeName="d" dur="10s" repeatCount="indefinite" ${SPL(9)} values="${vals(goldRing)}"/></path>`;

// ============ P2 莫比乌斯带（视角摇摆 ±22°，9 关键帧） ============
const C2=[880,252], S2=70;
const TH2=[-22,-11,0,11,22,11,0,-11,-22].map(d=>d*Math.PI/180);
function mobPt(u,v,th){ const c=Math.cos(u/2), s=Math.sin(u/2);
  const x=(1+v/2*c)*Math.cos(u), y=(1+v/2*c)*Math.sin(u), z=v/2*s;
  return proj(x,y,z,th,C2[0],C2[1],S2); }
const NU2=24, NU2L=12;
const mobLoops=TH2.map(th=>{
  let d='';
  for(const v of [-1,0,1]){
    const pts=Array.from({length:NU2+1},(_,k)=>{ const [sx,sy]=mobPt(k/NU2*2*Math.PI,v,th); return sx+","+sy; });
    d+="M"+pts.join(" L "); }
  return d; });
const mobCross=TH2.map(th=>{
  let d='';
  for(let i=0;i<NU2L;i++){ const u=i/NU2L*2*Math.PI;
    const a=mobPt(u,-1,th), b=mobPt(u,1,th);
    d+="M"+a[0]+","+a[1]+" L"+b[0]+","+b[1]+" "; }
  return d; });
const p2=`<path fill="none" stroke="#7ec2ff" stroke-width="2.2" opacity="0.9" d="${mobLoops[0]}"><animate attributeName="d" dur="7s" repeatCount="indefinite" ${SPL(9)} values="${vals(mobLoops)}"/></path>
    <path fill="none" stroke="#5ad0c0" stroke-width="1.2" opacity="0.6" d="${mobCross[0]}"><animate attributeName="d" dur="7s" repeatCount="indefinite" ${SPL(9)} values="${vals(mobCross)}"/></path>`;

// ============ P3 利萨茹曲线（相位 φ 舞动，12 关键帧） ============
const C3=[230,570], S3=62, TH3=0.4;
const lissPt=(t,ph)=>[Math.sin(3*t+ph), Math.sin(4*t), Math.sin(5*t+ph/2)];
const PH=Array.from({length:12},(_,k)=>k/12*2*Math.PI);
const lissD=PH.map(ph=>{
  const pts=Array.from({length:61},(_,k)=>{ const t=k/60*2*Math.PI; const [x,y,z]=lissPt(t,ph);
    return proj(x,y,z,TH3,C3[0],C3[1],S3).join(","); });
  return "M"+pts.join(" L "); });
const p3=`<path id="liss" fill="none" stroke="#5ad0c0" stroke-width="1.8" d="${lissD[0]}"><animate attributeName="d" dur="8s" repeatCount="indefinite" ${SPL(12)} values="${vals(lissD)}"/></path>
    <use href="#liss" fill="none" stroke="#5ad0c0" stroke-width="7" opacity="0.22" filter="url(#blur3)"/>`;

// ============ P4 涟漪面 z=A·sin(kr−ωt)·e^(−r/70)（14 关键帧） ============
const C4=[590,578], S4=1.4, TH4=0.3;
const G=9, EXT=60;
const rippleZ=(x,y,ph)=>{ const rr=Math.sqrt(x*x+y*y); return 14*Math.sin(0.09*rr-ph)*Math.exp(-rr/70); };
const RIP=Array.from({length:14},(_,k)=>k/14*2*Math.PI);
const ripLines=RIP.map(ph=>{
  let d='';
  for(let i=0;i<G;i++){ const x=-EXT+EXT*2*i/(G-1);
    const pts=Array.from({length:G},(_,j)=>{ const y=-EXT+EXT*2*j/(G-1);
      return proj(x,y,rippleZ(x,y,ph),TH4,C4[0],C4[1],S4).join(","); });
    d+="M"+pts.join(" L "); }
  for(let j=0;j<G;j++){ const y=-EXT+EXT*2*j/(G-1);
    const pts=Array.from({length:G},(_,i)=>{ const x=-EXT+EXT*2*i/(G-1);
      return proj(x,y,rippleZ(x,y,ph),TH4,C4[0],C4[1],S4).join(","); });
    d+="M"+pts.join(" L "); }
  return d; });
const p4=`<path fill="none" stroke="#2bb3a3" stroke-width="1.2" opacity="0.75" d="${ripLines[0]}"><animate attributeName="d" dur="5s" repeatCount="indefinite" ${SPL(14)} values="${vals(ripLines)}"/></path>`;

// ============ 组装 ============
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">
  <defs><filter id="blur3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3"/></filter></defs>
  <rect width="1200" height="800" fill="#0b101d"/>
  <text x="60" y="64" font-size="28" font-weight="700" fill="#e8eef7">数学变换 — 3D 参数之舞：球化环 · 莫比乌斯 · 利萨茹 · 涟漪</text>
  <text x="60" y="92" font-size="14" fill="#8fa0b8">Level 6++ — 每一帧都是真实 3D：参数方程 + 旋转矩阵 + 投影，由引擎预计算成 SMIL 关键帧 —— 零 JS</text>
  <g>
    <rect x="60" y="110" width="540" height="280" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="84" y="146" font-size="18" font-weight="700" fill="#e8eef7">球面 ⇄ 圆环面（拓扑变形）</text>
    ${p1}${p1Gold}
    <text x="84" y="366" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">同一副 (u,v) 网格：R 从 62 收到 0，圆环面退化成球面 — 拓扑教材经典案例</text>
  </g>
  <g>
    <rect x="620" y="110" width="540" height="280" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="644" y="146" font-size="18" font-weight="700" fill="#e8eef7">莫比乌斯带（单侧曲面）</text>
    ${p2}
    <text x="644" y="366" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">M(u,v)=((1+v/2·cos u/2)cosu, …) — 只有一条边，蚂蚁走一圈回到"背面"</text>
  </g>
  <g>
    <rect x="60" y="440" width="340" height="260" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="84" y="466" font-size="17" font-weight="700" fill="#e8eef7">利萨茹曲线（相位之舞）</text>
    ${p3}
    <text x="84" y="686" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">x=sin(3t+φ) y=sin(4t) z=sin(5t)</text>
  </g>
  <g>
    <rect x="420" y="440" width="340" height="260" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="444" y="466" font-size="17" font-weight="700" fill="#e8eef7">涟漪面（波的传播）</text>
    ${p4}
    <text x="444" y="686" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">z=A·sin(k·r−ωt)·e^(−r/70) — 相位推进，波荡开</text>
  </g>
  <g>
    <rect x="780" y="440" width="360" height="260" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="804" y="466" font-size="17" font-weight="700" fill="#e8eef7">变换的通用配方</text>
    <text x="804" y="498" font-size="13.5" fill="#c6d2e4">① 写下参数方程 P(u,v,t)</text>
    <text x="804" y="522" font-size="13.5" fill="#c6d2e4">② 每个关键帧算一遍 3D 坐标</text>
    <text x="804" y="546" font-size="13.5" fill="#c6d2e4">③ 旋转矩阵 + 投影到 2D</text>
    <text x="804" y="570" font-size="13.5" fill="#c6d2e4">④ 帧序列填进 SMIL values</text>
    <text x="804" y="594" font-size="13.5" fill="#c6d2e4">⑤ 样条缓动 = 丝滑的数学动画</text>
    <text x="804" y="630" font-size="12.5" fill="#5b6b8a">球化环：R 62→44→26→10→0→…</text>
    <text x="804" y="648" font-size="12.5" fill="#5b6b8a">26 是"角圆环"（内孔消失），</text>
    <text x="804" y="666" font-size="12.5" fill="#5b6b8a">0 就是球面 — 全程同一副网格。</text>
    <text x="804" y="686" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">换一个方程 = 换一种宇宙</text>
  </g>
  <text x="60" y="756" font-size="14" fill="#c6d2e4">到这里，"3D 数学变换"的答案：任何参数方程都能变成会动的 SVG —— 帧是真 3D，输出是纯标记，生成器只有 60 行。</text>
  <text x="60" y="778" font-size="12.5" fill="#5b6b8a">想亲手转：给本页任一面板接上拖拽事件改 yaw 角，就是可交互 3D 的起点。</text>
</svg>`;
await fs.writeFile("/Users/agiray/Desktop/test/99-临时/svg-demos/14-数学变换.svg", svg);
console.log("written bytes:", svg.length);
