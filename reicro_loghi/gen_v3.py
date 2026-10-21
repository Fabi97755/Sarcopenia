import math, sys
DEEP,TEAL,CORAL,INK='#0E4F5C','#1C9C8C','#E8664A','#12303A'
def P(r,a): a=math.radians(a); return (round(r*math.cos(a),2), round(r*math.sin(a),2))
def arc(r,a0,a1,col,w,op=1):
    s,e=P(r,a0),P(r,a1); large=1 if (a1-a0)%360>180 else 0
    return f'<path d="M{s[0]},{s[1]} A{r},{r} 0 {large} 1 {e[0]},{e[1]}" stroke="{col}" stroke-width="{w}" opacity="{op}" fill="none" stroke-linecap="round"/>'
def dot(p,r,col,extra=''): return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{col}" {extra}/>'
def line(p,q,col=DEEP,w=3,op=.5): return f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{col}" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>'

def wrap(id_,mark,word,sub,comment):
    return f'''<!-- {comment} -->
<div class="logo" id="{id_}"><svg width="780" height="220" viewBox="0 0 780 220">
 <g transform="translate(112,110)">
  {chr(10).join('  '+m for m in mark)}
 </g>
 <text class="word" x="252" y="118">{word}</text>
 <text class="sub" x="256" y="160">{sub}</text>
</svg></div>'''


O=(0,0)
def ring_segments(r,angles,gap,col,w,op=1):
    # anello spezzato: un arco tra un nodo e il successivo, con uno stacco attorno a ogni nodo
    out=[]
    for i,a in enumerate(angles):
        b=angles[(i+1)%len(angles)]+(360 if i==len(angles)-1 else 0)
        out.append(arc(r,a+gap,b-gap,col,w,op))
    return out

RI,RO=36,74
inner=[-90,30,150]
outer=[-90+30+60*k for k in range(6)]          # -60,0,60,120,180,240
IN=[P(RI,a) for a in inner]; OUT=[P(RO,a) for a in outer]
# ogni nodo interno è collegato alla persona e ai due nodi esterni più vicini
links=[line(O,p,DEEP,3,.45) for p in IN]
for a,p in zip(inner,IN):
    for b,q in zip(outer,OUT):
        if abs(((b-a+180)%360)-180)==30: links.append(line(p,q,DEEP,3,.45))
hosp=1  # nodo esterno a 0 gradi: l'ospedale, in corallo
nodesO=[dot(q,10,CORAL if i==hosp else DEEP) for i,q in enumerate(OUT)]
nodesI=[dot(p,8,TEAL) for p in IN]
base=links+ring_segments(RI,inner,22,TEAL,6)+ring_segments(RO,outer,13,DEEP,7)+nodesI+nodesO+[dot(O,15,CORAL)]

# 7. RETE A ORBITE
m7=base
# 8. RETE + CICLO: un'orbita esterna con freccia, il ciclo di cura che continua nel tempo
RC=96
a0,a1=-80,215
tip=P(RC,a1+4); t1=P(RC-8,a1-8); t2=P(RC+8,a1-8)
m8=base+[arc(RC,a0,a1,TEAL,5,.9),
    f'<path d="M{t1[0]},{t1[1]} L{tip[0]},{tip[1]} L{t2[0]},{t2[1]}" fill="none" stroke="{TEAL}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>']
# 9. SPIRALE IN RETE: il percorso di cura si allarga nel tempo, tre raggi lo collegano alla persona
th1=2.25*360; r0,r1=20,96
def sp(t): return P(r0+(r1-r0)*t/th1,t-90)
pts=[sp(t) for t in range(0,int(th1)+1,3)]
d='M'+' L'.join(f'{x},{y}' for x,y in pts)
spokes=[]; nodes9=[]
for k,base_a in enumerate((0,120,240)):
    ts=[t for t in range(base_a+120*0, int(th1)+1, 360) if t>=base_a]
    ts=[base_a+360*j for j in range(3) if base_a+360*j<=th1]
    far=sp(ts[-1]); spokes.append(line(O,far,DEEP,3,.45))
    for j,t in enumerate(ts):
        last = (t==max(ts))
        nodes9.append(dot(sp(t),7+2*j, CORAL if (last and k==0) else (TEAL if j==0 else DEEP)))
m9=spokes+[f'<defs><linearGradient id="g9" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{DEEP}"/></linearGradient></defs>',
    f'<path d="{d}" fill="none" stroke="url(#g9)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>']+nodes9+[dot(O,14,CORAL)]
head='''<!doctype html><html><head><meta charset="utf-8"><title>Loghi REICRO v3</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;500;600;800&display=swap">
<style>
body{margin:0;background:#fff;font-family:Manrope,sans-serif}
.logo{display:inline-block;padding:40px;background:transparent}
.word{font:800 92px Manrope;letter-spacing:2px;fill:#12303A}
.sub{font:600 19px Manrope;letter-spacing:3.4px;fill:#5D7A80}
</style></head><body>
<!-- Sviluppo della proposta 6 "Orbite". Generato da gen_v3.py -->
'''
out=head+'\n\n'.join([
 wrap('logo7',m7,'REICRO','RETE INTEGRATA CRONICITÀ','7. RETE A ORBITE: servizi del territorio (interno) e della rete (esterno) collegati alla persona'),
 wrap('logo8',m8,'REICRO','RETE INTEGRATA CRONICITÀ','8. RETE + CICLO: la freccia esterna è la presa in carico che continua nel tempo'),
 wrap('logo9',m9,'REICRO','RETE INTEGRATA CRONICITÀ','9. SPIRALE IN RETE: il percorso si allarga nel tempo, i raggi lo tengono legato alla persona'),
])+'\n</body></html>\n'
open(sys.argv[1],'w').write(out)
