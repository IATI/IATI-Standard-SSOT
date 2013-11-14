#!/bin/bash
set -o nounset

# Remove docs (the output directory), and recreate directory structure
rm -r docs
mkdir docs
mkdir docs/codelists
cd IATI-Extra-Documentation || exit 1
find -type d -exec mkdir ../docs/{} \;
cd .. || exit 1

# Generate documentation from the Schema etc
python gen.py || exit 1

# Append Extra-Documentation to the documentation we've just generated
cd IATI-Extra-Documentation || exit 1
find -type f -exec bash -c 'cat {} >> ../docs/{}' \;
cd .. || exit 1

# Generate documentation from codelists
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

# Build the documentation (generate html etc.) using sphinx
cd docs || exit 1
make html


