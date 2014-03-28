#!/bin/bash
set -o nounset

cd docs/en || exit 1
mkdir _static
ln -s ../_static/* _static/
make dirhtml
cd ../../ || exit 1
cd docs/fr || exit 1
mkdir _static
ln -s ../_static/* _static/
make dirhtml

