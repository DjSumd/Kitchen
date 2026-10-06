import re, json
from norm import parse
from items import I
IT={}
PATS=[]
for t in I:
    iid,name,sec,pan,life,frz,base,pack,price,buy,dens,ea,d,pats=t
    IT[iid]=dict(id=iid,name=name,sec=sec,pan=pan,life=life,frz=frz,base=base,pack=pack,price=price,buy=buy,dens=dens,ea=ea,d=d)
    for p in pats: PATS.append((re.compile(p),iid))
PRI=[(re.compile(r'\b(broth|stock|bouillon)\b(?! pot)'),'stock'),(re.compile(r'^(?!.*(ground|mince|minced)).*\blamb\b(?! stock)'),'lamb')]
def match(text):
    for rx,iid in PRI:
        if rx.search(text): return iid
    best=None;bl=0
    for rx,iid in PATS:
        m=rx.search(text)
        if m and (m.end()-m.start())>bl: best=iid;bl=m.end()-m.start()
    return best
def clean(s):
    s=s.split(',')[0] if not re.match(r'^(salt|pepper)',s) else s
    if re.search(r'\b(broth|stock)\b',s): return s
    s=re.sub(r'\bor\b.*$','',s) if len(s)>25 else s
    return s
CNT={'springonion':1/7,'coriander':0.05,'parsley':0.05,'basil':0.05,'mint':0.05,'dill':0.05,'thyme':0.05,'curryleaves':0.03,'garlic':0.1,'bokchoy':0.35,'asparagus':1/12,'lemongrass':1}
def amount(it,qty,unit,paren):
    base=it['base'];dens=it['dens'];ea=it['ea'];pack=it['pack']
    if qty is None or qty==0:
        return it['d']
    kind,f=unit if unit else ('count',1)
    g=None;ml=None;cnt=None
    if paren and kind in ('can','pkg','each','count'):
        pk,pf=paren[1]; v=qty*paren[0]*pf
        if pk=='g': g=v
        elif pk=='ml': ml=v
        else: cnt=qty
    elif kind=='g': g=qty*f
    elif kind=='ml': ml=qty*f
    elif kind in ('count','each'):
        cnt=qty
        if base=='ea' and it['id'] in CNT: return qty*CNT[it['id']]
    elif kind=='clove': 
        if it['id']=='garlic': return qty/10
        g=qty*5
    elif kind=='can': g=qty*400
    elif kind=='pkg': g=qty*(pack if base!='ea' else ea*pack)
    elif kind=='bunch':
        if base=='ea': return qty
        g=qty*150
    elif kind in ('stalk',): g=qty*50
    elif kind=='slice': g=qty*25
    elif kind in ('sprig','leaf'):
        if base=='ea': return qty*0.04
        g=qty*1
    elif kind=='inch': g=qty*10
    elif kind=='stick': g=qty*113 if it['id']=='butter' else qty*5
    else: cnt=qty
    if base=='ea':
        if cnt is not None: return cnt/ (pack if it['buy'] in ('dozen','8 pack') and False else 1)
        if g is None: g=ml*dens
        return g/ea
    if base=='g':
        if cnt is not None: return cnt*ea
        if g is None: g=ml*dens
        return g
    if base=='ml':
        if cnt is not None: return cnt*ea
        if ml is None: ml=g
        return ml
def map_recipe(r):
    out={};miss=[]
    for line in r['i']:
        if re.search(r'optional|for garnish|to garnish|for serving|to serve|garnish:',line.lower()): continue
        q,u,p,t=parse(line)
        t2=clean(t)
        iid=match(t2) or match(t)
        if not iid: miss.append(line); continue
        if iid=='skip': continue
        a=amount(IT[iid],q,u,p)
        it=IT[iid]
        a=min(a, it['pack']*3 if it['base']!='ea' else max(3,it['pack']*3)) if a else 0
        out[iid]=out.get(iid,0)+a
    return out,miss
