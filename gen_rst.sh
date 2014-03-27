#!/bin/bash
set -o nounset

# Remove docs (the output directory), and recreate
rm -r docs/*

# Generate csvs etc. from codelists
cd IATI-Codelists || exit 1
./gen.sh || exit 1
cd .. || exit 1
mkdir -p docs/_static/schemas/
cp -r IATI-Schemas/* docs/_static/schemas/
cp -r IATI-Codelists/out/ docs/_static/codelists/

# Generate documentation from the Schema and Codelists etc
python gen.py || exit 1

