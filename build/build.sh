#!/usr/bin/env bash
# Rebuilds ../index.html from the three public recipe datasets.
# Needs Python 3 and curl. Run from this folder: ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
fetch () { [ -d "$2" ] || curl -sfL "https://codeload.github.com/$1/tar.gz/refs/heads/$3" | tar xz; }
fetch josephrmartinez/recipe-dataset recipe-dataset-main main
fetch dpapathanasiou/recipes recipes-master master
fetch nileshiq/Indian-Food Indian-Food-main main
python3 load.py
python3 dinner.py > /dev/null
python3 build.py
python3 export_items.py
python3 inject.py
echo "Done: ../index.html"
