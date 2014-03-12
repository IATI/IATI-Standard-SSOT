#!/bin/bash
set -o nounset

cd docs/en || exit 1
ln -s ../_static .
make dirhtml
cd ../../ || exit 1
cd docs/fr || exit 1
ln -s ../_static .
make dirhtml

