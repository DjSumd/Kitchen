import json,re
from collections import Counter
U=json.load(open('all.json'))
NOT=r"\b(cake|cakes|cupcake|cookie|cookies|brownie|pie crust|tart|tarts|muffin|muffins|scone|bread|loaf|rolls?|biscuit|biscuits|pancake|pancakes|waffle|waffles|french toast|smoothie|shake|cocktail|martini|margarita|punch|lemonade|tea|coffee|latte|sorbet|ice cream|gelato|pudding|mousse|fudge|candy|candies|truffles?|frosting|icing|glaze|syrup|jam|jelly|preserves|marmalade|chutney|pickle|pickles|pickled|relish|salsa|dip|dressing|vinaigrette|marinade|rub|seasoning|spice mix|sauce|gravy|pesto|aioli|mayonnaise|butter|granola|cereal|oatmeal|porridge|parfait|crumble|cobbler|crisp|pie|cheesecake|dessert|sweet|cocoa|chocolate|caramel|meringue|macaron|bars?|squares|kheer|halwa|ladoo|laddu|barfi|burfi|payasam|raita|lassi|sherbet|sharbat|juice|chaat|pakora|pakoda|bhaji|vada|idli|dosa batter|dhokla|appetizers?|canapes?|crostini|bruschetta|deviled|stuffing|dressing|cranberry|eggnog|wine|sangria|mojito|spritzer|soda|shooter|sangria|popcorn|nuts|trail mix|crackers|chips|croutons|focaccia|pretzels?|bagels?|doughnuts?|donuts?|danish|strudel|eclairs?|souffle|custard|compote|coulis|whipped|frittata|omelet|omelette|breakfast|brunch|benedict|hash browns|quiche|eggs?|side|slaw|coleslaw|salad|chips|fries|wedges|mashed|puree|smash)\b"
YES=r"\b(chicken|beef|pork|lamb|steak|mince|sausages?|meatballs?|meatloaf|salmon|fish|cod|snapper|barramundi|prawns?|shrimp|tuna|mussels|curry|dal|dhal|daal|chana|rajma|paneer|tofu|pasta|spaghetti|penne|linguine|fettuccine|lasagna|lasagne|noodles?|ramen|pho|stir[- ]?fry|fried rice|risotto|pilaf|pulao|biryani|khichdi|soup|stew|chili|chilli|casserole|bake|tacos?|burritos?|enchiladas?|fajitas?|quesadillas?|burgers?|pizza|gnocchi|ravioli|tortellini|macaroni|mac and cheese|pot pie|shepherd|cottage pie|roast|braised?|kebabs?|skewers?|satay|teriyaki|bolognese|ragu|goulash|tagine|korma|tikka|masala|vindaloo|rendang|laksa|jambalaya|gumbo|paella|chops?|cutlets?|thighs?|drumsticks?|wings|ribs|brisket|turkey|duck|veal|ham|chorizo|bacon|lentils?|beans|chickpeas?|kofta|sabzi|subzi|thoran|poriyal|kootu|kurma|rasam|sambar|gravy)\b"
def is_dinner(r):
    t=r['n'].lower()
    if re.search(r'rillettes|\bpaste\b|spice (mix|blend)|\bp[aâ]t[eé]\b|terrine|spread|crostini|canap|tartlets?|mousse|stock\b|broth\b|brine|jerky|baby food|for dogs|dog treats|pet food|starter|sauce for|appetiser',t): return False
    if r['src']=="Archana's Kitchen":
        if r['course'] not in ('Lunch','Dinner','Main Course','One Pot Dish','High Protein Vegetarian','Vegetarian','Non Vegeterian'): return False
        if re.search(r'\b(raita|chutney|pickle|kheer|halwa|salad|papad|roti|paratha|chapati|naan|puri|poori|phulka|bhakri|thepla|kulcha)\b',t): return False
        return True
    tags=set(r['tags'])
    if tags & {'Dessert','Drink','Cocktail','Alcoholic','Breakfast','Brunch','Side','Appetizer','Condiment/Spread','Sauce','Cookie','Cake','Bake'} and 'Dinner' not in tags: return False
    if re.search(NOT,t) and not re.search(r'\b(chicken|beef|pork|lamb|fish|salmon|shrimp|prawn|pasta|curry|tofu|steak)\b',t): return False
    if re.search(r'\b(salad|sauce|dip|marinade|dressing|rub|gravy|pie crust|glaze|soup mix|seasoning|cake|cookies|bars|bread|muffins?|appetizers?|sliders|dessert)\b',t): 
        # allow e.g. "chicken in mushroom sauce", reject "sauce for chicken", salads
        if re.search(r'\b(salad|dip|marinade|dressing|rub|seasoning|glaze|cake|cookies|bars|bread|muffins?|dessert|appetizers?)\b',t): return False
        if t.endswith('sauce') or t.endswith('gravy'): return False
    if 'Dinner' in tags: return True
    return bool(re.search(YES,t))
D=[r for r in U if is_dinner(r)]
print(len(D), Counter(r['src'] for r in D))
import random;random.seed(4)
for r in random.sample(D,40): print(' ',r['n'])
json.dump(D,open('dinner.json','w'))
