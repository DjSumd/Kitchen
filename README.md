# The Kitchen

A dinner planner that turns one shop into several nights of dinners.

Choose how many nights the shop covers (1 to 7), a rough spend per dinner, and who's eating. The Kitchen picks recipes that share their fresh ingredients, so a bunch of coriander or a tray of chicken thighs gets used across several nights instead of going in the bin. It then writes a shopping list grouped by section, priced in whole packs.

**Live app:** `https://<your-username>.github.io/the-kitchen/`

## What it does

- Plans 1 to 7 nights from about 21,000 dinner recipes.
- Prices the shop the way you actually buy it: whole bunches, packs and cans.
- Counts what each fresh ingredient leaves over, and what keeps for later (pasta, frozen meat, jars).
- Orders dinners so fish and soft herbs are cooked first and beans and stews later, and suggests freezing meat for later nights.
- Lets you mark nights you're out. Later dinners are planned knowing the food has waited longer in the fridge.
- Sets a cuisine for any night, and how many people are eating on each night.
- Includes ingredients you already have (free, off the list) or want to use up.
- Leaves out ingredients you don't want, and follows vegetarian, pescatarian or no-pork diets.
- **Similar** switches a dinner to a close match. **Swap** lets you choose any recipe, showing how the whole shop changes. **Keep** holds a dinner in place when you re-plan.
- Assumes a standard pantry of 32 staples (salt, oils, soy sauce, rice, stock, spices and so on), shown on screen and editable.
- Saves everything in your browser: settings, plan, ticked items, your own prices and aisle numbers.

## Run it

Open `index.html` in any current browser. It is a single self-contained file of about 11 MB with no server or install. Fonts load from Google Fonts when online.

## Publish with GitHub Pages

1. Create a new repository called `the-kitchen` on GitHub.
2. Upload the contents of this folder (`index.html`, `README.md`, `.gitignore` and the `build` folder). At about 11 MB, `index.html` is under GitHub's 25 MB web-upload limit, so drag and drop works.
3. In the repository, go to **Settings > Pages**, set **Source** to *Deploy from a branch*, choose `main` and `/ (root)`, and save.
4. After a minute or two the app is live at `https://<your-username>.github.io/the-kitchen/`.

## Rebuild the data

The `build` folder regenerates `index.html` from the source recipe datasets. You only need this if you change the ingredient table, prices or matching rules.

```bash
cd build
./build.sh
```

It needs Python 3 and `curl`. It downloads about 50 MB of source data (ignored by git), then writes `../index.html`. The build is reproducible: the same inputs give an identical file.

| File | Job |
| --- | --- |
| `load.py` | Reads the three datasets and removes duplicate titles |
| `dinner.py` | Keeps dinner dishes; drops desserts, sides, drinks and sauces |
| `norm.py` | Parses quantities and units from ingredient lines |
| `items.py` | The priced ingredient table: sections, pack sizes, prices, fridge life, pantry defaults |
| `mapper.py` | Matches each ingredient line to an item and converts amounts |
| `cuisine.py` | Labels cuisines from titles and telling ingredients |
| `build.py` | Keeps recipes where every ingredient is priced, then estimates servings |
| `export_items.py` | Writes the ingredient table for the app |
| `inject.py` | Compresses the data into `template.html` to produce `index.html` |
| `template.html` | The app itself: layout, styles and planner |

To change prices or pack sizes permanently, edit `items.py` and rebuild. For quick changes, tap any price in the app's shopping list instead.

## Limits

- Prices are rough Woolworths (Perth) estimates from October 2026.
- Quantities are parsed from mostly American recipes, and servings are often estimated, so amounts are close rather than exact.
- Cuisine labels come from the source data for Archana's Kitchen recipes and are inferred for the rest. About 30% of recipes have no cuisine label and appear only on nights set to "Any".

## Recipe sources

- Epicurious, via [josephrmartinez/recipe-dataset](https://github.com/josephrmartinez/recipe-dataset)
- Allrecipes, Epicurious, Food Network and Williams-Sonoma, via [dpapathanasiou/recipes](https://github.com/dpapathanasiou/recipes)
- Archana's Kitchen, via [nileshiq/Indian-Food](https://github.com/nileshiq/Indian-Food)

Recipes remain the property of their original publishers. This is a personal, non-commercial project.
