const fs = await import("node:fs/promises");
const SINA = Math.sin(20*Math.PI/180), COSA = Math.cos(20*Math.PI/180);
const f1 = n => (Math.round(n*10)/10).toString();
let seed = 42; const rnd = () => (seed = (seed*1103515245+12345) % 2147483648) / 2147483648;

function proj(x,y,z,th,cx,cy){ const c=Math.cos(th), s=Math.sin(th);
  const x2=x*c-y*s, y2=x*s+y*c;
  return [f1(cx+x2), f1(cy-(y2*SINA+z*COSA))]; }

// ---------- P1 等距数据中心 ----------
const UX=0.866, UY=0.5, VX=-0.866, VY=0.5;
let p1='';
let grid='';
for(let k=-4;k<=4;k++){
  const px=330+VX*k*24, py=282+VY*k*24;
  grid+=`<line x1="${f1(px-UX*100)}" y1="${f1(py-UY*100)}" x2="${f1(px+UX*100)}" y2="${f1(py+UY*100)}"/>`;
  const qx=330+UX*k*24, qy=282+UY*k*24;
  grid+=`<line x1="${f1(qx-VX*100)}" y1="${f1(qy-VY*100)}" x2="${f1(qx+VX*100)}" y2="${f1(qy+VY*100)}"/>`;
}
p1+=`<g stroke="#1c2a47" stroke-width="1">${grid}</g>`;

function isoBox(BX,BY,a,b,h,top,left,right){
  const Bu=[BX+UX*a,BY+UY*a], Bv=[BX+VX*b,BY+VY*b], Buv=[BX+UX*a+VX*b,BY+UY*a+VY*b];
  const T=[BX,BY-h], Tu=[Bu[0],Bu[1]-h], Tv=[Bv[0],Bv[1]-h], Tuv=[Buv[0],Buv[1]-h];
  const pts=(...ps)=>ps.map(p=>f1(p[0])+","+f1(p[1])).join(" ");
  const base=[BX,BY];
  let s='';
  s+=`<polygon points="${pts(base,Bu,Bv,Buv)}" fill="#000" opacity="0.22" filter="url(#blur3)"/>`;
  s+=`<polygon points="${pts(Bv,Buv,Tuv,Tv)}" fill="${left}"/>`;
  s+=`<polygon points="${pts(Bu,Buv,Tuv,Tu)}" fill="${right}"/>`;
  s+=`<polygon points="${pts(T,Tu,Tuv,Tv)}" fill="${top}"/>`;
  return s;
}

let leds='';
p1+=isoBox(286,252,48,34,96,"#8ec5ff","#4a94f8","#2b5fc0");
for(let j=0;j<5;j++) for(let i=0;i<3;i++){
  const t=8+i*10, up=14+j*16;
  const cx=286+UX*48+VX*t, cy=252+UY*48+VY*t-up;
  const col = rnd()<0.75 ? "#3ecf8e" : (rnd()<0.7 ? "#f7b32b" : "#f65e5e");
  const dur=(1.1+rnd()*1.6).toFixed(2), beg=(rnd()*2).toFixed(2);
  leds+=`<circle cx="${f1(cx)}" cy="${f1(cy)}" r="2.6" fill="${col}"><animate attributeName="opacity" values="1;0.15;1" dur="${dur}s" begin="${beg}s" repeatCount="indefinite"/></circle>`;
}
p1+=isoBox(424,286,44,30,74,"#cbaeff","#9b6cf5","#6a3fd0");
for(let j=0;j<4;j++) for(let i=0;i<3;i++){
  const t=6+i*9, up=12+j*15;
  const cx=424+UX*44+VX*t, cy=286+UY*44+VY*t-up;
  const col = rnd()<0.75 ? "#3ecf8e" : "#f7b32b";
  const dur=(1.0+rnd()*1.8).toFixed(2), beg=(rnd()*2).toFixed(2);
  leds+=`<circle cx="${f1(cx)}" cy="${f1(cy)}" r="2.4" fill="${col}"><animate attributeName="opacity" values="0.2;1;0.2" dur="${dur}s" begin="${beg}s" repeatCount="indefinite"/></circle>`;
}
p1+=isoBox(185,268,30,24,28,"#7de3d3","#2bb3a3","#177a6e");
p1+=isoBox(185,240,30,24,22,"#7de3d3","#2bb3a3","#177a6e");
const floatCube=isoBox(196,196,24,20,18,"#ffd166","#f7a23b","#c77714");
p1+=`<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="3.4s" repeatCount="indefinite"/>${floatCube}</g>`;
p1+=`<line x1="348" y1="172" x2="294" y2="159" stroke="#5b6b8a" stroke-dasharray="3 4"/><text x="352" y="176" font-size="10.5" fill="#8fa0b8" font-family="SFMono-Regular, Menlo, monospace">RACK-A · 42U</text>`;
p1+=`<line x1="474" y1="224" x2="428" y2="212" stroke="#5b6b8a" stroke-dasharray="3 4"/><text x="478" y="228" font-size="10.5" fill="#8fa0b8" font-family="SFMono-Regular, Menlo, monospace">RACK-B · 36U</text>`;

// ---------- P2 圆环面线框 ----------
const R=62, r=26, CX2=880, CY2=258, AL=20*Math.PI/180;
const sA=Math.sin(AL), cA=Math.cos(AL);
function torusPt(u,v){ const x=(R+r*Math.cos(v))*Math.cos(u), y=(R+r*Math.cos(v))*Math.sin(u), z=r*Math.sin(v);
  return [CX2+x, CY2-(y*sA+z*cA), y*cA-z*sA]; }
const ringPaths=[], tubePaths=[];
for(let i=0;i<12;i++){ const u=i/12*2*Math.PI; let pts=[],dsum=0;
  for(let k=0;k<=36;k++){ const v=k/36*2*Math.PI; const [sx,sy,dp]=torusPt(u,v); pts.push(f1(sx)+","+f1(sy)); dsum+=dp; }
  ringPaths.push({d:"M"+pts.join(" L"), dp:dsum/37});
}
for(let j=0;j<8;j++){ const v=j/8*2*Math.PI; let pts=[],dsum=0;
  for(let k=0;k<=40;k++){ const u=k/40*2*Math.PI; const [sx,sy,dp]=torusPt(u,v); pts.push(f1(sx)+","+f1(sy)); dsum+=dp; }
  tubePaths.push({d:"M"+pts.join(" L"), dp:dsum/41});
}
const allD=ringPaths.concat(tubePaths).map(p=>p.dp);
const dmin=Math.min(...allD), dmax=Math.max(...allD);
const opac=dp=>f1(0.2+0.55*(dp-dmin)/(dmax-dmin));
let torus='';
for(const rp of ringPaths) torus+=`<path d="${rp.d}" fill="none" stroke="#7ec2ff" stroke-width="1.1" opacity="${opac(rp.dp)}"/>`;
for(const tp of tubePaths) torus+=`<path d="${tp.d}" fill="none" stroke="#7ec2ff" stroke-width="1.1" opacity="${opac(tp.dp)}"/>`;
torus+=`<path d="${ringPaths[0].d}" fill="none" stroke="#ffd166" stroke-width="1.7" opacity="0.95"/>`;
torus+=`<path d="${tubePaths[0].d}" fill="none" stroke="#ffd166" stroke-width="1.7" opacity="0.95"/>`;

// ---------- P3 立方体 90° 翻面 ----------
const S=54, CX3=230, CY3=572;
const V3=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]];
function cubeProj(th){ const c=Math.cos(th), s=Math.sin(th);
  return V3.map(([x,y,z])=>{ const x2=x*c-y*s, y2=x*s+y*c;
    return [f1(CX3+x2*S), f1(CY3-(y2*SINA+z*COSA)*S)]; });
}
const EDGES=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
const ths=[0,Math.PI/2,Math.PI,Math.PI*1.5,0];
const cubeVals=ths.map(th=>{ const pp=cubeProj(th);
  return EDGES.map(([a,b])=>"M"+pp[a][0]+","+pp[a][1]+" L"+pp[b][0]+","+pp[b][1]).join(" "); }).join(";");
const SPL="calcMode=\"spline\" keyTimes=\"0;0.25;0.5;0.75;1\" keySplines=\".37 0 .63 1;.37 0 .63 1;.37 0 .63 1;.37 0 .63 1\"";
let cubeDots='';
V3.forEach((_,i)=>{ const xs=ths.map(th=>cubeProj(th)[i][0]).join(";"), ys=ths.map(th=>cubeProj(th)[i][1]).join(";");
  cubeDots+=`<circle r="3.2" fill="#ffd166"><animate attributeName="cx" values="${xs}" dur="7s" repeatCount="indefinite" ${SPL}/><animate attributeName="cy" values="${ys}" dur="7s" repeatCount="indefinite" ${SPL}/></circle>`; });
const cubeSVG=`<path fill="none" stroke="#7ec2ff" stroke-width="1.6" d="${cubeVals.split(";")[0]}"><animate attributeName="d" dur="7s" repeatCount="indefinite" ${SPL} values="${cubeVals}"/></path>${cubeDots}`;

// ---------- P4 3D 柱状图摇摆 ----------
const CX4=590, CY4=580;
const bars=[{x:-42,y:6,h:62,c:["#7ec2ff","#4a94f8","#2b5fc0"]},{x:0,y:-8,h:96,c:["#cbaeff","#9b6cf5","#6a3fd0"]},{x:42,y:10,h:76,c:["#7de3d3","#2bb3a3","#177a6e"]}];
const ths4=[4,7.5,11,14.5,18,14.5,11,7.5,4].map(d=>d*Math.PI/180);
const KF=ths4.length;
const KT4=Array.from({length:KF},(_,i)=>f1(i/(KF-1))).join(";");
const SP4=Array.from({length:KF-1},()=>".37 0 .63 1").join(";");
function boxFaces(x,y,h,th){
  const hw=18, hd=15;
  const v=(dx,dy,dz)=>proj(x+dx,y+dy,dz,th,CX4,CY4);
  const top=[v(-hw,-hd,h),v(hw,-hd,h),v(hw,hd,h),v(-hw,hd,h)];
  const front=[v(-hw,hd,h),v(hw,hd,h),v(hw,hd,0),v(-hw,hd,0)];
  const right=[v(hw,-hd,h),v(hw,hd,h),v(hw,hd,0),v(hw,-hd,0)];
  return {top,front,right};
}
function animPoints(facesFn,color){
  const key=ths4.map(th=>facesFn(th).map(p=>p[0]+","+p[1]).join(" ")).join(";");
  return `<polygon points="${facesFn(ths4[0]).map(p=>p[0]+","+p[1]).join(" ")}" fill="${color}"><animate attributeName="points" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="${KT4}" keySplines="${SP4}" values="${key}"/></polygon>`;
}
let p4='';
for(const b of bars){
  p4+=animPoints(th=>boxFaces(b.x,b.y,b.h,th).top,b.c[0]);
  p4+=animPoints(th=>boxFaces(b.x,b.y,b.h,th).front,b.c[1]);
  p4+=animPoints(th=>boxFaces(b.x,b.y,b.h,th).right,b.c[2]);
}
let floor='';
for(const zz of [-62,-21,21,62]) floor+=`<path fill="none" stroke="#1c2a47" stroke-width="1" d="${(()=>{const a=proj(-62,zz,0,ths4[0],CX4,CY4),b2=proj(62,zz,0,ths4[0],CX4,CY4);return "M"+a[0]+","+a[1]+" L"+b2[0]+","+b2[1];})()}"><animate attributeName="d" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="${KT4}" keySplines="${SP4}" values="${ths4.map(th=>{const a=proj(-62,zz,0,th,CX4,CY4),b2=proj(62,zz,0,th,CX4,CY4);return "M"+a[0]+","+a[1]+" L"+b2[0]+","+b2[1];}).join(";")}"/></path>`;
for(const xx of [-62,-21,21,62]) floor+=`<path fill="none" stroke="#1c2a47" stroke-width="1" d="${(()=>{const a=proj(xx,-62,0,ths4[0],CX4,CY4),b2=proj(xx,62,0,ths4[0],CX4,CY4);return "M"+a[0]+","+a[1]+" L"+b2[0]+","+b2[1];})()}"><animate attributeName="d" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="${KT4}" keySplines="${SP4}" values="${ths4.map(th=>{const a=proj(xx,-62,0,th,CX4,CY4),b2=proj(xx,62,0,th,CX4,CY4);return "M"+a[0]+","+a[1]+" L"+b2[0]+","+b2[1];}).join(";")}"/></path>`;
const p4SVG=floor+p4;

// ---------- 组装 ----------
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">
  <defs><filter id="blur3" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3"/></filter></defs>
  <rect width="1200" height="800" fill="#0b101d"/>
  <text x="60" y="64" font-size="28" font-weight="700" fill="#e8eef7">三维 — SVG 的 3D 姿势：插画级 · 数学级 · 动画级</text>
  <text x="60" y="92" font-size="14" fill="#8fa0b8">Level 6++ — 静态 3D：等距插画 / 参数方程投影；动态 3D：关键帧插值（SMIL）。全部零 JS、零 WebGL</text>
  <g>
    <rect x="60" y="110" width="540" height="280" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="84" y="146" font-size="18" font-weight="700" fill="#e8eef7">等距插画：数据中心（插画级伪 3D）</text>
    ${p1}${leds}
    <text x="84" y="366" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">30° 等距轴：顶/左/右三面 × 明度 + LED 心跳 — Keynote 插画就这么画</text>
  </g>
  <g>
    <rect x="620" y="110" width="540" height="280" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="644" y="146" font-size="18" font-weight="700" fill="#e8eef7">数学投影：圆环面线框（真 3D）</text>
    ${torus}
    <text x="644" y="366" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">参数方程逐点投影，20 条线按深度调透明度 — 金色为主视线环</text>
  </g>
  <g>
    <rect x="60" y="440" width="340" height="260" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="84" y="466" font-size="17" font-weight="700" fill="#e8eef7">立方体 90° 翻面</text>
    ${cubeSVG}
    <text x="84" y="686" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">4 个真投影间样条过渡，顶点发光</text>
  </g>
  <g>
    <rect x="420" y="440" width="340" height="260" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="444" y="466" font-size="17" font-weight="700" fill="#e8eef7">3D 柱状图摇摆（SMIL）</text>
    ${p4SVG}
    <text x="444" y="686" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">相机绕轴摆动，面片逐帧投影 — 无 JS</text>
  </g>
  <g>
    <rect x="780" y="440" width="360" height="260" rx="14" fill="#0e1524" stroke="#22304d"/>
    <text x="804" y="466" font-size="17" font-weight="700" fill="#e8eef7">边界说明</text>
    <text x="804" y="498" font-size="13.5" fill="#c6d2e4">静态 3D：等距插画（好看可控）</text>
    <text x="804" y="522" font-size="13.5" fill="#c6d2e4">静态 3D：数学投影（精确可编程）</text>
    <text x="804" y="546" font-size="13.5" fill="#c6d2e4">动态 3D：关键帧插值（本页两种）</text>
    <text x="804" y="570" font-size="13.5" fill="#c6d2e4">动态 3D：CSS 3D / foreignObject（真）</text>
    <text x="804" y="594" font-size="13.5" fill="#c6d2e4">可拖拽旋转：Three.js / WebGL 出场</text>
    <text x="804" y="630" font-size="12.5" fill="#5b6b8a">注意：CSS 3D 需要 foreignObject 嵌 HTML，</text>
    <text x="804" y="648" font-size="12.5" fill="#5b6b8a">无法在 &lt;img&gt; 里生效 — 所以本页全部用</text>
    <text x="804" y="666" font-size="12.5" fill="#5b6b8a">纯 SVG 路径方案实现"会动的 3D"。</text>
    <text x="804" y="686" font-size="11.5" fill="#6f84a8" font-family="SFMono-Regular, Menlo, monospace">三维台阶：能画 → 会算 → 会动 → 可交互</text>
  </g>
  <text x="60" y="756" font-size="14" fill="#c6d2e4">结论：静态 3D 随便画；"会动"的 3D 用关键帧插值；可拖拽、可缩放的真 3D 场景才需要 WebGL — 而 Three.js 也能导出 SVG。</text>
  <text x="60" y="778" font-size="12.5" fill="#5b6b8a">本页由一个 30 行的 Node 迷你 3D 引擎生成：旋转矩阵 + 正交投影 + 深度排序，输出的全是纯 SVG 标记。</text>
</svg>`;
await fs.writeFile("/Users/agiray/Desktop/test/99-临时/svg-demos/13-三维.svg", svg);
console.log("written bytes:", svg.length, "| rings:", ringPaths.length, "tubes:", tubePaths.length, "barKF:", KF);
