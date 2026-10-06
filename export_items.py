"""Write items.json: the priced ingredient table the app uses."""
import json
from mapper import IT
R = json.load(open('final.json'))
used = set(k for r in R for k in r['u'])
items = [dict(id=v['id'], n=v['name'], s=v['sec'], p=v['pan'], l=v['life'], f=v['frz'],
              b=v['base'], k=v['pack'], c=v['price'], y=v['buy'])
         for v in IT.values() if v['id'] in used and v['id'] != 'skip']
json.dump(items, open('items.json', 'w'))
print(len(items), 'ingredients')
