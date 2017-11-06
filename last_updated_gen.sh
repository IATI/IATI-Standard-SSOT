#!/bin/bash
./gen_rst.sh || exit $?
cd docs || exit 1
git add .
git commit -a -m 'Auto'
cd .. || exit 1
./gen_html.sh || exit $?
