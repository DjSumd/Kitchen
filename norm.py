import re
FR={'½':.5,'¼':.25,'¾':.75,'⅓':1/3,'⅔':2/3,'⅛':.125,'⅜':.375,'⅝':.625,'⅞':.875}
UNITS={
 'g':('g',1),'gram':('g',1),'grams':('g',1),'gm':('g',1),'gms':('g',1),'kg':('g',1000),'kilogram':('g',1000),'kilograms':('g',1000),
 'oz':('g',28.35),'ounce':('g',28.35),'ounces':('g',28.35),'lb':('g',453.6),'lbs':('g',453.6),'pound':('g',453.6),'pounds':('g',453.6),
 'ml':('ml',1),'milliliter':('ml',1),'milliliters':('ml',1),'l':('ml',1000),'liter':('ml',1000),'liters':('ml',1000),'litre':('ml',1000),'litres':('ml',1000),
 'cup':('ml',240),'cups':('ml',240),'c':('ml',240),'tablespoon':('ml',15),'tablespoons':('ml',15),'tbsp':('ml',15),'tbs':('ml',15),'tbsps':('ml',15),'tbl':('ml',15),
 'teaspoon':('ml',5),'teaspoons':('ml',5),'tsp':('ml',5),'tsps':('ml',5),'pint':('ml',473),'pints':('ml',473),'quart':('ml',946),'quarts':('ml',946),'qt':('ml',946),
 'fl oz':('ml',29.6),'fluid ounces':('ml',29.6),'fluid ounce':('ml',29.6),'pinch':('ml',.3),'dash':('ml',.6),'handful':('ml',60),'sprig':('sprig',1),'sprigs':('sprig',1),
 'clove':('clove',1),'cloves':('clove',1),'can':('can',1),'cans':('can',1),'tin':('can',1),'tins':('can',1),'jar':('can',1),'package':('pkg',1),'packages':('pkg',1),'pkg':('pkg',1),'packet':('pkg',1),'box':('pkg',1),'bag':('pkg',1),
 'bunch':('bunch',1),'bunches':('bunch',1),'head':('each',1),'heads':('each',1),'stalk':('stalk',1),'stalks':('stalk',1),'rib':('stalk',1),'ribs':('stalk',1),'slice':('slice',1),'slices':('slice',1),'piece':('each',1),'pieces':('each',1),'inch':('inch',1),'inches':('inch',1),
 'fillet':('each',1),'fillets':('each',1),'breast':('each',1),'breasts':('each',1),'thigh':('each',1),'thighs':('each',1),'link':('each',1),'links':('each',1),'stick':('stick',1),'sticks':('stick',1),'leaves':('leaf',1),'leaf':('leaf',1),'ear':('each',1),'ears':('each',1),
}
SIZE={'small','medium','large','big','extra-large','extra','jumbo','whole','fresh','heaping','level','scant','generous','about','approximately','plus','more','or','to','-','–','a','an','few'}
def num(tok):
    tok=tok.strip()
    for k,v in FR.items():
        if k in tok:
            rest=tok.replace(k,'').strip()
            try: return (float(rest) if rest else 0)+v
            except: return v
    m=re.fullmatch(r'(\d+)/(\d+)',tok)
    if m: return int(m[1])/int(m[2])
    try: return float(tok)
    except: return None
QRE=re.compile(r"^\s*((?:\d+\s+\d+/\d+|\d+/\d+|\d*[½¼¾⅓⅔⅛⅜⅝⅞]|\d+(?:\.\d+)?)(?:\s*(?:-|–|to)\s*(?:\d+\s+\d+/\d+|\d+/\d+|\d*[½¼¾⅓⅔⅛⅜⅝⅞]|\d+(?:\.\d+)?))?)")
def parse(line):
    """returns qty, unit, size_in_paren(qty,unitkind), text"""
    s=line.lower().replace('\u2009',' ').replace('\xa0',' ')
    s=re.sub(r'(\d)([a-z])',r'\1 \2',s)  # 500g -> 500 g
    paren=None
    m=re.search(r'\(([^)]*)\)',s)
    if m:
        pm=QRE.match(m[1].replace('-',' ').strip())
        if pm:
            rest=m[1][pm.end():] if False else re.sub(QRE,'',m[1].strip(),count=1).strip(' -')
            u=rest.split()[0].strip('.,') if rest.split() else ''
            q=pm[1].split('to')[0].split('-')[0].split('–')[0].strip()
            q=sum(num(x) or 0 for x in q.split()) if ' ' in q else num(q)
            if u.replace('-',' ').split()[0:1] and UNITS.get(u.split('-')[0]):
                paren=(q,UNITS[u.split('-')[0]])
    s=re.sub(r'\([^)]*\)',' ',s)
    qty=None
    m=QRE.match(s)
    if m:
        part=re.split(r'\s*(?:-|–|to)\s*',m[1])[0]
        qty=sum(num(x) or 0 for x in part.split())
        s=s[m.end():]
    s=s.strip()
    unit=None
    # multiword unit
    for u in ('fl oz','fluid ounces','fluid ounce'):
        if s.startswith(u+' '): unit=UNITS[u]; s=s[len(u):]; break
    if not unit:
        w=s.split(' ',1)
        w0=w[0].strip('.,/')
        # skip size words before unit e.g. "2 large cloves"
        if w0 in ('small','medium','large','big','heaping','level','scant','generous') and len(w)>1:
            w2=w[1].split(' ',1); 
            if w2[0].strip('.,') in UNITS: w0=w2[0].strip('.,'); w=[w0,w2[1] if len(w2)>1 else '']
        if w0 in UNITS and len(w)>1:
            unit=UNITS[w0]; s=w[1]
    s=re.sub(r'^(of|of the)\s+','',s.strip())
    if unit is None and qty:
        m=re.match(r'^(?:about |approx\.? )?(\d+(?:\.\d+)?(?:\s+\d/\d)?|\d/\d)\s*(?:-?\s*to\s*\d+(?:\s+\d/\d)?)?[- ](pound|lb|ounce|oz|kg|g|gram)s?\b',s)
        if m:
            q2=sum(num(x) or 0 for x in m[1].split()); u2=UNITS.get(m[2])
            if u2: paren=(q2,u2)
    return qty,unit,paren,s.strip()
def head(text):
    t=text.split(',')[0]
    t=re.sub(r'\b(fresh|freshly|chopped|finely|coarsely|roughly|thinly|sliced|diced|minced|grated|shredded|crushed|ground|peeled|deveined|boneless|skinless|large|small|medium|whole|halved|quartered|cubed|trimmed|rinsed|drained|cooked|uncooked|dried|dry|frozen|thawed|packed|lightly|beaten|softened|melted|to taste|optional|for garnish|divided|about|plus more|organic|extra-virgin|extra virgin)\b','',t)
    return re.sub(r'\s+',' ',t).strip(' -.;:')
