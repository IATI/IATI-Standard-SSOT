#!/bin/bash
set -o nounset

# Remove docs (the output directory), and recreate directory structure
rm -r docs
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

# Append Extra-Documentation to the documentation we've just generated
cd IATI-Extra-Documentation || exit 1
find \( ! -path '*/.*' \) -follow -type f -exec bash -c 'cat {} >> ../docs/{}' \;
cd .. || exit 1

# Build the documentation (generate html etc.) using sphinx
cd docs/en || exit 1
ln -s ../_static .
(echo '.. raw:: html'; echo ''; curl -L "https://raw.github.com/IATI/iati-datastore/master/iati_datastore/iatilib/frontend/docs/index.md" | pandoc -f markdown_github -t html | sed 's/^/   /') > datastore.rst
make dirhtml
cd ../../ || exit 1
cd docs/fr || exit 1
ln -s ../_static .
make dirhtml

