#!/usr/bin/env python3
"""
Patch generated knowledge graph HTML exports so they settle instead of
running an endless unstable force simulation.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPLACEMENT_BLOCK = """const colors={G:"#ef4444",M:"#f97316",E:"#eab308",S:"#22c55e",T:"#06b6d4",K:"#3b82f6",R:"#8b5cf6",Q:"#ec4899",F:"#14b8a6",C:"#d4a853"};
const cv=document.getElementById("c"), ctx=cv.getContext("2d");
const tip=document.getElementById("tip");
const idMap={}; N.forEach((n,i)=>{ idMap[n.id]=i; });
let W=window.innerWidth, H=window.innerHeight;
cv.width=W; cv.height=H;
let ox=0, oy=0, sc=1, drag=null, hover=null;
let simAlpha=1;
let simRunning=true;
let frameCount=0;

const edgeWeight=(et)=>{
  if(et==="shared_layers") return 0.08;
  if(et==="chi_similar") return 0.35;
  if(et==="shared_dominant") return 0.2;
  return 0.15;
};

const visibleLinks = L.filter((l, i) => {
  if(l.et!=="shared_layers") return true;
  if(L.length < 4000) return true;
  const stride=Math.ceil(L.length/2500);
  return i % stride === 0;
});

N.forEach((n,i)=>{
  if(typeof n.x !== "number" || typeof n.y !== "number"){
    const a=2*Math.PI*i/Math.max(1,N.length);
    n.x=W/2+Math.min(W,H)*0.25*Math.cos(a);
    n.y=H/2+Math.min(W,H)*0.25*Math.sin(a);
  }
  n.vx=typeof n.vx==="number"?n.vx:0;
  n.vy=typeof n.vy==="number"?n.vy:0;
});

function tick(){
  if(!simRunning) return;
  frameCount++;
  let totalMotion=0;
  const repulsionBase = N.length > 150 ? 90 : 180;

  for(let i=0;i<N.length;i++){
    for(let j=i+1;j<N.length;j++){
      let dx=N[j].x-N[i].x, dy=N[j].y-N[i].y;
      let d=Math.sqrt(dx*dx+dy*dy)||1;
      let f=(repulsionBase*simAlpha)/(d*d);
      N[i].vx-=dx/d*f; N[i].vy-=dy/d*f;
      N[j].vx+=dx/d*f; N[j].vy+=dy/d*f;
    }
  }

  L.forEach(l=>{
    let si=typeof l.s==="number"?l.s:idMap[l.s];
    let ti=typeof l.t==="number"?l.t:idMap[l.t];
    if(si===undefined||ti===undefined)return;
    let a=N[si], b=N[ti];
    let dx=b.x-a.x, dy=b.y-a.y;
    let d=Math.sqrt(dx*dx+dy*dy)||1;
    let target=l.et==="shared_layers" ? 110 : 75;
    let f=(d-target)*(0.0025*edgeWeight(l.et))*simAlpha;
    a.vx+=dx/d*f; a.vy+=dy/d*f;
    b.vx-=dx/d*f; b.vy-=dy/d*f;
  });

  N.forEach(n=>{
    n.vx+=(W/2-n.x)*0.0007*simAlpha;
    n.vy+=(H/2-n.y)*0.0007*simAlpha;
    n.vx*=0.84;
    n.vy*=0.84;
    if(n!==drag){
      n.x+=n.vx;
      n.y+=n.vy;
    }
    totalMotion += Math.abs(n.vx) + Math.abs(n.vy);
  });

  simAlpha*=0.992;
  if(frameCount>900 || (simAlpha<0.025 && totalMotion < N.length*0.035)){
    simRunning=false;
    N.forEach(n=>{ n.vx=0; n.vy=0; });
  }
}

function draw(){
  ctx.clearRect(0,0,W,H);
  ctx.save();
  ctx.translate(ox,oy);
  ctx.scale(sc,sc);
  visibleLinks.forEach(l=>{
    let si=typeof l.s==="number"?l.s:idMap[l.s];
    let ti=typeof l.t==="number"?l.t:idMap[l.t];
    if(si===undefined||ti===undefined)return;
    ctx.beginPath();
    ctx.moveTo(N[si].x, N[si].y);
    ctx.lineTo(N[ti].x, N[ti].y);
    ctx.strokeStyle=l.et==="chi_similar"?"rgba(45,212,160,0.18)":
                    l.et==="shared_dominant"?"rgba(212,168,83,0.18)":"rgba(42,48,80,0.08)";
    ctx.stroke();
  });
  N.forEach((n,i)=>{
    let r=6+(n.combined||0)*30;
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI*2);
    ctx.fillStyle=colors[n.dominant_var]||"#555";
    if(n===hover){ ctx.fillStyle="#fff"; r+=3; }
    ctx.fill();
    ctx.strokeStyle="#2a3050";
    ctx.stroke();
    if(sc>0.7){
      ctx.fillStyle=n===hover?"#fff":"#6a6d7b";
      ctx.font="8px Segoe UI";
      ctx.fillText(n.text.substring(0,25), n.x+r+3, n.y+3);
    }
  });
  ctx.restore();
  tick();
  requestAnimationFrame(draw);
}
"""


PATTERN = re.compile(
    r'const colors=\{.*?function draw\(\)\{.*?requestAnimationFrame\(draw\);\n\}',
    re.DOTALL,
)


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "let simAlpha=1;" in text:
        return False
    patched, count = PATTERN.subn(REPLACEMENT_BLOCK, text, count=1)
    if count != 1:
        return False
    path.write_text(patched, encoding="utf-8")
    return True


def collect_targets(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(root.rglob("vault_graph.html"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Stabilize generated graph HTML exports")
    parser.add_argument("target", help="HTML file or root folder")
    args = parser.parse_args()

    target = Path(args.target)
    patched = 0
    for path in collect_targets(target):
        if patch_html(path):
            patched += 1
            print(f"patched {path}")

    print(f"patched_files={patched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
