import csv, json, glob, re, ast
csv.field_size_limit(10**9)
def plist(s):
    try:
        v=ast.literal_eval(s); return [str(x).strip() for x in v if str(x).strip()]
    except Exception: return []
def split_steps(t):
    t=re.sub(r'\s+',' ',t).strip()
    p=re.split(r'(?<=[.!?])\s+(?=[A-Z])',t)
    out=[];cur=''
    for s in p:
        cur=(cur+' '+s).strip()
        if len(cur)>90: out.append(cur);cur=''
    if cur: out.append(cur)
    return out
R=[]
for row in csv.DictReader(open('recipe-dataset-main/13k-recipes.csv',encoding='utf-8')):
    ins=[s.strip() for s in (row['Instructions'] or '').split('\n') if s.strip()]
    R.append(dict(n=row['Title'].strip(),i=plist(row['Ingredients']),s=ins,src='Epicurious',tags=[],serv=None,course=None,cuisine=None,diet=None))
for f in glob.glob('recipes-master/index/**/*.json',recursive=True):
    d=json.load(open(f))
    src={'allrecipes.com':'Allrecipes','www.epicurious.com':'Epicurious','www.foodnetwork.com':'Food Network','www.williams-sonoma.com':'Williams-Sonoma'}.get(d.get('source'),d.get('source'))
    R.append(dict(n=(d.get('title') or '').strip(),i=[x.strip() for x in d.get('ingredients') or [] if x.strip()],s=[x.strip() for x in d.get('directions') or [] if x.strip()],src=src,tags=d.get('tags') or [],serv=None,course=None,cuisine=None,diet=None))
for row in csv.DictReader(open('Indian-Food-main/IndianFoodDataset.csv',encoding='utf-8',errors='replace')):
    ings=[x.strip() for x in (row.get('TranslatedIngredients') or '').split(',') if x.strip()]
    try: sv=int(float(row['Servings']))
    except: sv=None
    R.append(dict(n=row['TranslatedRecipeName'].replace(' Recipe','').strip(),i=ings,s=split_steps(row.get('TranslatedInstructions') or ''),src="Archana's Kitchen",tags=[],serv=sv,course=row['Course'],cuisine=row['Cuisine'],diet=row['Diet']))
seen=set();U=[]
for r in R:
    k=re.sub(r'[^a-z]','',r['n'].lower())
    if not k or k in seen or len(r['i'])<2 or not r['s']: continue
    seen.add(k);U.append(r)
print(len(R),len(U))
json.dump(U,open('all.json','w'))
