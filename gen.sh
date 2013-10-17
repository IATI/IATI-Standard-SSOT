#!/bin/bash
rm -r docs
mkdir docs
mkdir docs/codelists
cd docs-extra
find -type d -exec mkdir ../docs/{} \;
cd ..
python2 gen.py
cd docs-extra
find -type f -exec bash -c 'cat {} >> ../docs/{}' \;
cd ..

cd IATI-Codelists
./gen.sh
cd ..
for f in IATI-Codelists/out/csv/*; do
    fname=`basename $f .csv`
    underline=`echo $fname | sed s/./=/g`
    description=`xmllint --xpath "string(/codelist/@description)" IATI-Codelists/xml/$fname.xml`
    echo "$fname
$underline

$description

\`XML <https://github.com/Bjwebb/IATI-Codelists-Output/blob/master/xml/${fname}.xml>\`_
\`CSV <https://github.com/Bjwebb/IATI-Codelists-Output/blob/master/csv/${fname}.csv>\`_
\`JSON <https://github.com/Bjwebb/IATI-Codelists-Output/blob/master/json/${fname}.json>\`_

.. csv-table::
   :file: ../../$f
    
    " > docs/codelists/${fname}.rst;
done

cd docs
make html


