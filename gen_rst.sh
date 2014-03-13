#!/bin/bash
set -o nounset

# Remove docs (the output directory), and recreate directory structure
rm -r docs/*
mkdir docs
cd IATI-Extra-Documentation/ || exit 1
find -type d -exec mkdir ../docs/{} \;
cd .. || exit 1

# Generate csvs etc. from codelists
cd IATI-Codelists || exit 1
./gen.sh || exit 1
cd .. || exit 1
mkdir docs/_static
cp -r IATI-Codelists/out/ docs/_static/codelists/

# Generate documentation from the Schema and Codelists etc
python gen.py || exit 1

