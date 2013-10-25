#!/bin/bash
set -o nounset

rm -r docs
mkdir docs
mkdir docs/codelists
cd IATI-Extra-Documentation || exit 1
find -type d -exec mkdir ../docs/{} \;
cd .. || exit 1
python gen.py || exit 1
cd IATI-Extra-Documentation || exit 1
find -type f -exec bash -c 'cat {} >> ../docs/{}' \;
cd .. || exit 1

cd IATI-Codelists || exit 1
./gen.sh || exit 1
cd .. || exit 1
mkdir docs/_static
cp -r IATI-Codelists/out/ docs/_static/codelists/
for f in IATI-Codelists/out/csv/*; do
    fname=`basename $f .csv`
    underline=`echo $fname | sed s/./=/g`
    description=`xmllint --xpath "string(/codelist/@description)" IATI-Codelists/xml/$fname.xml`
    echo "$fname
$underline


$description

Download this codelist:
\`XML <../_static/codelists/xml/${fname}.xml>\`_
\`CSV <../_static/codelists/csv/${fname}.csv>\`_
\`JSON <../_static/codelists/json/${fname}.json>\`_
View on github:
\`XML <https://github.com/Bjwebb/IATI-Codelists-Output/blob/master/xml/${fname}.xml>\`_
\`CSV <https://github.com/Bjwebb/IATI-Codelists-Output/blob/master/csv/${fname}.csv>\`_
\`JSON <https://github.com/Bjwebb/IATI-Codelists-Output/blob/master/json/${fname}.json>\`_

.. csv-table::
   :file: ../../$f
    
    " > docs/codelists/${fname}.rst;
done

cd docs || exit 1
make html


