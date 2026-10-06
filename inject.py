import json,gzip,base64
R=json.load(open('final.json'))
IX={it['id']:k for k,it in enumerate(json.load(open('items.json')))}
for r in R: r['m']=[IX.get(x,-1) if x else -1 for x in r['m']]
raw=json.dumps(R,separators=(',',':'),ensure_ascii=False).encode()
b=base64.b64encode(gzip.compress(raw,9,mtime=0)).decode()
t=open('template.html').read().replace('__ITEMS__',open('items.json').read().replace('</','<\\/')).replace('__DATA__',b)
open('../index.html','w').write(t)
import os;print(os.path.getsize('../index.html')/1e6,'MB')
