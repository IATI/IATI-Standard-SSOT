#!/bin/bash
rm -r docs
mkdir docs
cd docs-extra
find -type d -exec mkdir ../docs/{} \;
cd ..
python2 gen.py
cd docs-extra
find -type f -exec bash -c 'cat {} >> ../docs/{}' \;
cd ../docs
make html


