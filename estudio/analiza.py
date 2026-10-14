import re, glob, os, json
from PIL import Image
def palabras(vtt):
    t=open(vtt).read(); out=[]
    for bloque in t.split('\n\n'):
        m=re.search(r'(\d+):(\d+):([\d.]+) -->',bloque)
        if not m or '<c>' not in bloque: continue
        t0=int(m[1])*3600+int(m[2])*60+float(m[3])
        linea=[l for l in bloque.split('\n') if '<c>' in l][0]
        primera=linea.split('<')[0].strip()
        if primera: out.append((t0,primera))
        for ts,w in re.findall(r'<(\d+:\d+:[\d.]+)><c>\s*([^<]+)</c>',linea):
            h,mi,s=ts.split(':'); out.append((int(h)*3600+int(mi)*60+float(s),w.strip()))
    return out
for d in sorted(glob.glob('v/*')):
    id_=os.path.basename(d)
    info=open(f'{d}/info.txt').read().strip() if os.path.exists(f'{d}/info.txt') else ''
    vtts=sorted(glob.glob(f'{d}/x.*-orig.vtt')) or sorted(glob.glob(f'{d}/x.*.vtt'))
    print('=====',id_, info)
    if vtts:
        w=palabras(vtts[0])
        if w:
            dur=w[-1][0]-w[0][0]
            print(f'  palabras {len(w)} · {len(w)/max(dur,1):.1f} pal/s · empieza a hablar en {w[0][0]:.1f}s')
            print('  0-3s:', ' '.join(x for t,x in w if t<3))
            print('  3-8s:', ' '.join(x for t,x in w if 3<=t<8))
            print('  final:', ' '.join(x for t,x in w[-25:]))
    sbs=sorted(glob.glob(f'{d}/sb/sb_*.jpg'))
    if sbs:
        ims=[Image.open(s) for s in sbs]; W=max(i.width for i in ims); H=sum(i.height for i in ims)
        c=Image.new('RGB',(W,H)); y=0
        for i in ims: c.paste(i,(0,y)); y+=i.height
        c=c.resize((W*3,H*3),Image.LANCZOS); c.save(f'{d}/hoja.jpg',quality=85)
