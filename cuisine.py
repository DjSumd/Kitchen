import re
CU=['indian','chinese','japanese','korean','thai','vietnamese','seasian','italian','french','med','latin','american','british']
AK={'Italian Recipes':'italian','Mexican':'latin','Thai':'thai','Chinese':'chinese','Indo Chinese':'chinese','Cantonese':'chinese','Sichuan':'chinese','Hunan':'chinese',
 'Middle Eastern':'med','Mediterranean':'med','Greek':'med','African':'med','Afghan':'med','Jewish':'med','French':'french','European':None,'Continental':None,'Fusion':None,'Asian':None,
 'Japanese':'japanese','Korean':'korean','Vietnamese':'vietnamese','Indonesian':'seasian','Malaysian':'seasian','Burmese':'seasian','Caribbean':'latin','British':'british'}
T=[ # title rules, order matters
('med',r"persian|iranian|greek|turkish|lebanese|moroccan|israeli|egyptian|syrian|afghan|armenian|tunisian|spanish|portuguese"),
('thai',r"\bthai\b|pad thai|pad see|tom yum|tom kha|massaman|panang|penang curry|green curry|red curry|yellow curry|larb|laab|khao|siam|bangkok|pad kra"),
('vietnamese',r"vietnam|hanoi|\bpho\b|banh mi|\bbun\b|saigon|nuoc|caramel(ized)? (pork|fish)|lemongrass (beef|chicken|pork)"),
('korean',r"korea|bulgogi|bibimbap|kimchi|gochujang|galbi|gal-bi|kalbi|japchae|bossam|dak "),
('japanese',r"japan|teriyaki|\bmiso\b|katsu|ramen|udon|soba|sukiyaki|yakitori|tonkatsu|donburi|tempura|gyoza|yakisoba|okonomiyaki|oyakodon|shabu|nabe|furikake|tokyo"),
('seasian',r"laksa|rendang|satay|sate\b|nasi|mee goreng|mie goreng|\badobo\b|filipin|philippin|indonesia|malay|singapore|sambal|kecap|sinigang|pancit|lumpia|balinese|bali\b|burmese|penang|kare-kare|caldereta|afritada|tinola|guinataan"),
('indian',r"masala|tikka|tandoor|korma|kurma|vindaloo|biryani|biriyani|\bdal\b|\bdhal\b|\bdaal\b|paneer|\bsaag\b|palak|\baloo\b|\bgobi\b|\bchana\b|chole|rajma|keema|kheema|makhani|jalfrezi|madras|rogan josh|roghan|pulao|pullao|khichdi|sambar|rasam|kadai|kadhai|karahi|bhuna|balti|dhansak|\bdesi\b|punjabi|goan|kerala|chettinad|hyderabad|indian|bombay|mumbai|delhi|kashmiri|bengali|patia|xacuti|sabzi|subzi|subji|kofta curry|mughlai|lucknow|awadhi|malabar|kootu|poriyal|thoran|avial|moilee|molee|nihari|haleem|korma|butter chicken|murgh|gosht|josh|\bmutter\b|\bmatar\b|bhindi|baingan|bharta|tarka|tadka|sri lanka|ceylon|nepal|mysore|madrasi|curd rice|lemon rice|tamarind rice|upma|uttapam|dosa"),
('chinese',r"chinese|kung pao|gung bao|szechuan|sichuan|schezwan|hoisin|chow mein|lo mein|chop suey|fried rice|sweet and sour|sweet & sour|general tso|orange chicken|lemon chicken|mapo|char siu|moo shu|mu shu|cantonese|hunan|wonton|dim sum|potsticker|egg foo|foo young|cashew chicken|mongolian|sesame chicken|peking|shanghai|beijing|hong kong|chow fun|dan dan|black bean sauce|five[- ]spice|congee|jook|manchurian|chilli chicken|chili chicken|hakka|cumin lamb|red[- ]braised|kung po|bok choy|oyster sauce|stir[- ]?fr"),
('latin',r"mexic|taco|burrito|enchilada|fajita|quesadilla|salsa|\bmole\b|carnitas|chile verde|chili verde|pozole|posole|tamale|tostada|chipotle|chimichanga|carne asada|al pastor|barbacoa|cuban|\bmojo\b|brazil|peru|churrasco|chimichurri|empanada|arepa|tex[- ]mex|southwest|jerk|caribbean|jamaica|puerto ric|picadillo|ropa vieja|arroz con|cilantro[- ]lime|cilantro lime|latin|argentin|colombia|venezuel|salvador|guatemal|yucatan|oaxaca|baja|ancho|poblano|tomatillo|nacho|huevos|chilaquiles|sofrito|feijoada|moqueca|chicharr"),
('italian',r"ital|pasta|spaghetti|linguine|penne|lasagn|fettuc|rigatoni|gnocchi|carbonara|bolognese|ragu|ravioli|tortellini|orecchiette|risotto|parmigiana|parmesan chicken|chicken parm|eggplant parm|marsala|piccata|cacciatore|alfredo|pesto|osso buco|saltimbocca|tuscan|tuscany|sicil|tuscan|roman|milan|venet|calabr|neapol|napoli|florentine|pizza|calzone|stromboli|minestrone|polenta|arrabbiata|puttanesca|scampi|prosciutto|primavera|ziti|manicotti|cannelloni|orzo|farfalle|fusilli|bucatini|tagliatelle|pappardelle|cioppino|frittata|braciole|porchetta|scaloppin|piccante|vodka sauce|amatriciana|aglio|arrabiata|caprese|bruschetta chicken|genovese|ribollita|pasta e fagioli|panzanella|gremolata|agrodolce|limone|al forno|italiano|macaroni"),
('french',r"french|proven[cç]|bourguignon|bourguignonne|coq au vin|cassoulet|au vin|ratatouille|bouillabaisse|gratin|confit|ni[cç]oise|b[eé]arnaise|fricass[eé]e|croque|quiche|papillote|normand|lyonn|dijon|paris|bistro|daube|blanquette|pot-au-feu|pot au feu|choucroute|tarte|vichyssoise|soubise|meuni[eè]re|au poivre|steak frites|frites|provence|brittany|breton|alsac|basquaise|parisienne|bonne femme|chasseur|veronique|cordon bleu|beurre|bordelaise|duxelles"),
('med',r"greek|greece|souvlaki|moussaka|gyro|tzatziki|kleftiko|stifado|spanakopita|pastitsio|lebanes|leban|turkish|turkey kebab|persian|iran|kofta|kofte|kebab|kabob|shawarma|falafel|hummus|tagine|tajine|moroccan|morocc|harissa|za.?atar|sumac|israel|shakshuka|couscous|middle east|egypt|syria|tunisia|algeri|north african|ethiopia|levant|mediterran|spanish|spain|paella|romesco|gazpacho|catalan|basque|portugu|piri|peri peri|andalu|valencia|cypr|armenia|georgian|afghan|pilaf|plov|dolma|kibbeh|fattoush|tabbouleh|baba|lamb shank|aegean|crete|cretan|sicilian"),
('british',r"shepherd|cottage pie|irish|guinness|bangers|toad in the hole|fish and chips|fish & chips|wellington|cornish|pasty|bubble and squeak|kedgeree|scotch|scottish|english|british|yorkshire|lancashire|hotpot|hot pot|steak and kidney|steak & kidney|ploughman|welsh|london|cumberland|coddle|colcannon|boxty|bangers|beef and ale|chicken and leek pie|pie and mash|sunday roast|roast dinner|corned beef and cabbage|aussie|australian|anzac|kiwi|new zealand"),
('american',r"bbq|barbe?cue|pulled pork|sloppy joe|meatloaf|burger|mac and cheese|mac 'n|macaroni and cheese|casserole|pot roast|\bchili\b|chilli con|gumbo|jambalaya|cajun|creole|southern|buffalo|ranch|tater tot|chicken fried|country fried|cornbread|hot dog|philly|texas|kansas|carolina|memphis|louisiana|new england|chowder|pot pie|potpie|hawaiian|smothered|dumplings|brunswick|tennessee|kentucky|nashville|california|cheesesteak|sliders|hash|baked beans|biscuits|apple cider|maple|crock|slow cooker|grilled cheese|stroganoff|goulash|swedish|hungarian|german|schnitzel|bratwurst|polish|pierog|kielbasa|russian|ukrain|beef stew|chicken and rice|tuna noodle|tetrazzini|sloppy|campbell|velveeta|ritz|tater|po.? ?boy|sheet pan|one pot|skillet"),
]
TR=[(c,re.compile(p)) for c,p in T]
def classify(r):
    t=r['n'].lower()
    if r['src']=="Archana's Kitchen":
        c=r.get('cuisine') or ''
        if c in AK:
            v=AK[c]
            if v: return v
        else:
            return 'indian'
    for c,rx in TR:
        if rx.search(t):
            # title "stir fry"/"bok choy" -> generic asian; keep chinese
            return c
    txt=' '.join(r['i']).lower()
    def has(*ws): return sum(1 for w in ws if w in txt)
    if has('garam masala','curry leaves','asafoetida','cumin seeds','kasuri','ghee','mustard seeds','turmeric')>=2: return 'indian'
    if 'fish sauce' in txt and has('lemongrass','lemon grass','coconut milk','thai','kaffir','galangal','basil')>=1: return 'thai'
    if has('gochujang','kimchi','gochugaru'): return 'korean'
    if has('mirin','miso','dashi','nori','sake','furikake','wasabi'): return 'japanese'
    if has('hoisin','oyster sauce','shaoxing','five-spice','five spice','chinese','bok choy','rice wine'): return 'chinese'
    if 'soy sauce' in txt and has('ginger','sesame oil','rice vinegar','scallion','green onion')>=2: return 'chinese'
    if has('tortilla','salsa','chipotle','taco seasoning','enchilada','jalape','cilantro','tomatillo','queso')>=2: return 'latin'
    if has('curry powder','curry paste')>=1 and 'coconut milk' in txt: return 'seasian'
    if has('feta','kalamata','tahini','sumac',"za'atar",'harissa','pomegranate molasses','chickpeas','couscous','preserved lemon')>=2: return 'med'
    if has('parmesan','parmigiano','mozzarella','basil','oregano','italian seasoning','marinara','pancetta','balsamic')>=2: return 'italian'
    if has('condensed','cream of mushroom','cream of chicken','cheddar','barbecue sauce','bbq sauce','ketchup','ranch','velveeta','processed cheese','worcestershire')>=1: return 'american'
    return None
