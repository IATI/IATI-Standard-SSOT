#!/bin/bash
set -o nounset

cd docs/en || exit 1
mkdir _static
cd _static || exit 1
ln -s ../../_static/* .
cd .. || exit 1
make dirhtml
cd ../../ || exit 1
cd docs/fr || exit 1
mkdir _static
cd _static || exit 1
ln -s ../../_static/* .
cd .. || exit 1
make dirhtml

cd ../.. || exit 1
mkdir -p docs/en/_build/dirhtml/schema/downloads/
cp -r IATI-Schemas/* docs/en/_build/dirhtml/schema/downloads/
cp -r IATI-Codelists/out/ docs/en/_build/dirhtml/codelists/downloads/
mkdir -p docs/fr/_build/dirhtml/schema/downloads/
cp -r IATI-Schemas/* docs/fr/_build/dirhtml/schema/downloads/
cp -r IATI-Codelists/out/ docs/fr/_build/dirhtml/codelists/downloads/

