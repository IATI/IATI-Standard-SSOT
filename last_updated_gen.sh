#!/bin/bash
./gen_rst.sh
cd docs || exit 1
git add .
git commit -a -m 'Auto'
git ls-tree -r --name-only HEAD | grep 'rst$' | while read filename; do
    echo $'\n\n\n'"*Last updated on $(git log -1 --format="%ad" --date=short -- $filename)*" >> $filename
done
cd .. || exit 1
./gen_html.sh
