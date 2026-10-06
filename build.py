import json,re,gzip,base64
from cuisine import classify as cuisine_of
from collections import Counter
from mapper import *
D=json.load(open('dinner.json'))
D=[r for r in D if not re.search(r'[\u0900-\u097F]',' '.join(r['i'])+r['n'])]
MEAT={'chickthigh','chickbreast','mince','porkmince','beefsteak','beefstew','lamb','pork','sausage','bacon'}
SEA={'whitefish','salmon','prawn','tuna','mussels'}
MAINS=MEAT|SEA|{'tofu','paneer','chickpea','beans','lentils','egg','pasta','asiannoodle','grains'}
PERSERV={'chickthigh':180,'chickbreast':170,'mince':140,'porkmince':140,'beefsteak':170,'beefstew':200,'lamb':200,'pork':180,'sausage':150,'whitefish':160,'salmon':150,'prawn':130,'mussels':300,'tofu':120,'paneer':100,'pasta':100,'asiannoodle':90,'lentils':60,'chickpea':150,'beans':150,'grains':70,'rice':80}
TYPES=[('Curry',r'curry|tikka|masala|vindaloo|korma|rendang|laksa|\bdal\b|dhal|daal|biryani|tagine|madras|jalfrezi|rogan josh|massaman|sambar|rasam|kootu|kurma|sabzi|subzi|chana|rajma|paneer|kadai|makhani|saag|palak|keema|vindaloo|thai .*green|red curry|khichdi|pulao'),
('Pasta & noodles',r'pasta|spaghetti|linguine|penne|lasagn|fettuc|macaroni|rigatoni|gnocchi|carbonara|bolognese|noodle|ravioli|orzo|tagliatelle|bucatini|ziti|farfalle|tortellini|lo mein|chow mein|pad thai|ramen|udon|soba|rotini|fusilli|shells|manicotti|cannelloni|angel hair|alfredo|mac and cheese|mac \'n'),
('Soup & stew',r'soup|chowder|bisque|stew|minestrone|gumbo|chili|chilli|pho\b|goulash|ragout|cassoulet|pozole|posole|congee|jook'),
('Stir-fry & rice',r'stir[- ]?fr|fried rice|teriyaki|kung pao|sesame|szechuan|sichuan|hoisin|orange chicken|sweet and sour|risotto|paella|jambalaya|rice bowl|pilaf|bibimbap|nasi|donburi|bowl'),
('Tacos, wraps & burgers',r'taco|burrito|enchilada|fajita|quesadilla|burger|wrap|sandwich|sloppy|pita|gyro|kebab|kabob|souvlaki|shawarma|tostada|nachos|sub\b|po.? ?boy|slider|banh mi|pizza|calzone|flatbread'),
('Bakes & roasts',r'bake|baked|roast|casserole|pie\b|gratin|lasagn|meatloaf|shepherd|cottage|potpie|pot pie|enchilada|braise|pot roast|slow cooker|crock|stuffed|en papillote'),
('Grills & pan-fries',r'grill|bbq|barbecue|barbeque|steak|chops?|cutlet|schnitzel|seared|pan[- ]fried|pan[- ]seared|skewer|satay|blackened|fillet|burgers?|patties|meatballs|scallopini|piccata|marsala|parmesan|parmigiana|fried')]
def rtype(t):
    t=t.lower()
    for name,rx in TYPES:
        if re.search(rx,t): return name
    return 'Other'
out=[];seen=set()
for r in D:
    o,m=map_recipe(r)
    if m: continue
    mains=[k for k in o if k in MAINS]
    t=r['n']
    if not mains and not re.search(r'soup|stew|curry|chili|casserole|risotto|biryani|pulao|khichdi|pie|dal|sabzi|subzi|frittata|bowl',t.lower()): continue
    # servings
    serv=r['serv']
    if not serv:
        est=[o[k]/PERSERV[k] for k in o if k in PERSERV and k!='rice']
        serv=round(max(est)) if est else 4
    serv=max(2,min(10,serv))
    if r['src']=="Archana's Kitchen" and r['serv']: serv=max(2,min(8,r['serv']))
    # main
    prot=None;pv=0
    for k in o:
        if k in PERSERV and k not in ('rice',):
            v=o[k]/PERSERV[k]
            if v>pv: pv=v;prot=k
    diet='m' if any(k in MEAT for k in o) else ('p' if any(k in SEA for k in o) else 'v')
    fresh=[k for k in o if not IT[k]['pan']]
    if len(fresh)==0 or len(fresh)>14: continue
    if len(r['s'])>25 or len(r['i'])>28: continue
    u={}
    for k,v in o.items():
        it=IT[k]; ps=v/serv
        cap=max(it['pack']*0.6, PERSERV.get(k,0)*1.8)
        if k=='wine': cap=125
        u[k]=round(min(ps,cap),3)
    ml=[]
    for line in r['i']:
        q,uu,p,tt=parse(line); iid=match(clean(tt)) or match(tt)
        ml.append(iid if iid and iid!='skip' else None)
    out.append(dict(n=t,src=r['src'],i=r['i'],s=r['s'],sv=serv,u=u,ty=rtype(t),pr=prot,dt=diet,m=ml,cu=cuisine_of(r) or ''))
print(len(out),Counter(x['ty'] for x in out),Counter(x['dt'] for x in out),Counter(x['src'] for x in out))
json.dump(out,open('final.json','w'))
raw=json.dumps(out,separators=(',',':'),ensure_ascii=False).encode()
z=gzip.compress(raw,9)
print('raw MB',len(raw)/1e6,'gz MB',len(z)/1e6,'b64 MB',len(base64.b64encode(z))/1e6)
