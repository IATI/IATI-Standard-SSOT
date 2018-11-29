#!/bin/bash
# This script pulls in the Developer Documetnation and Guidance to build the full iatistandard.org website
# See the README for more information
echo "Setting up live templates symlinks IATI-Websites -> IATI-Extra-Documentation"
cd IATI-Extra-Documentation/en
ln -s ../../IATI-Websites/iatistandard/_templates/ ./
ln -s ../../IATI-Websites/iatistandard/_static/ ./
cd _templates
ln -s ../../../IATI-Websites/iatistandard/_templates/layout_live.html layout.html
cd ../../..


echo "Generating RST copy"
bash scripts/main/gen_rst.sh || exit $?

cd docs || exit 1

mkdir en/developer
cp -n ../IATI-Developer-Documentation/*.rst en/developer
cp -rn ../IATI-Developer-Documentation/*/ en/developer
mkdir en/guidance
cp -n ../IATI-Guidance/en/*.rst en/guidance
cp -rn ../IATI-Guidance/en/*/ en/guidance
mv en/guidance/404.rst en/
mv en/guidance/upgrades* en/
mv en/guidance/introduction* en/
mv en/guidance/key-considerations* en/
mv en/guidance/license* en/
cp ../combined_sitemap.rst en/sitemap.rst

git add .
git commit -a -m 'Auto'
git ls-tree -r --name-only HEAD | grep 'rst$' | while read filename; do
    echo $'\n\n\n'"*Last updated on $(git log -1 --format="%ad" --date=short -- $filename)*" >> $filename
done

cd .. || exit 1


echo "Generating HTML copy"
bash scripts/main/gen_html.sh || exit $?

echo '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' > docs/en/_build/dirhtml/sitemap.xml
find docs/en/_build/dirhtml | grep -v _static | grep index.html$ | sed 's|index.html$|</loc></url>|' | sed "s|docs/en/_build/dirhtml|<url><loc>http://`cat URL`|" >> docs/en/_build/dirhtml/sitemap.xml
echo '</urlset>' >> docs/en/_build/dirhtml/sitemap.xml

cp -r docs docs-copy.new
mv docs-copy docs-copy.old
mv docs-copy.new docs-copy
rm -rf docs-copy.old
sed -i 's/\.\.\//\//g' docs-copy/en/_build/dirhtml/404/index.html

echo "Generation complete"

