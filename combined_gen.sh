#!/bin/bash
# This script pulls in the Developer Documetnation and Guidance to build the full iatistandard.org website
./gen_rst.sh || exit $?

cd docs || exit 1
git add .
git commit -a -m 'Auto'
git ls-tree -r --name-only HEAD | grep 'rst$' | while read filename; do
    echo $'\n\n\n'"*Last updated on $(git log -1 --format="%ad" --date=short -- $filename)*" >> $filename
done

ln -s /home/ssot/IATI-Developer-Documentation en/developer
ln -s /home/ssot/IATI-Guidance/en/*.rst en/
ln -s /home/ssot/IATI-Guidance/en/*/ en/
cp ../special_sitemap.rst en/sitemap.rst

cd .. || exit 1
./gen_html.sh || exit $?

rm -rf docs-copy
cp -r docs docs-copy

