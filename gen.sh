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
    echo "$fname
$underline

.. csv-table::
   :file: ../../$f
    
    " > docs/codelists/${fname}.rst;
done

cd docs
make html


