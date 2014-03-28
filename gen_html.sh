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

