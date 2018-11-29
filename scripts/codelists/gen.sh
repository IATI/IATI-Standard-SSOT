#!/bin/bash

rm -rf combined-xml
if [ -d IATI-Codelists-NonEmbedded ]; then
    cd IATI-Codelists-NonEmbedded || exit 1
    git pull
    git checkout master
else
    git clone https://github.com/IATI/IATI-Codelists-NonEmbedded.git
    cd IATI-Codelists-NonEmbedded || exit 1
    git checkout master
fi
cd .. || exit 1

mkdir combined-xml
cp xml/* combined-xml
cp IATI-Codelists-NonEmbedded/xml/* combined-xml

rm -rf out
mkdir -p out/clv2/xml out/clv3
cp -r combined-xml out/clv3/xml
for f in combined-xml/*; do
    python v3tov2.py $f > out/clv2/xml/`basename $f`;
done

python gen.py
python v2tov1.py

cp -r out/clv2/{codelists.json,codelists.xml,csv,json} out/clv3/

python mappings_to_json.py
cp mapping.{xml,json} out/clv1/
cp mapping.{xml,json} out/clv2/
cp mapping.{xml,json} out/clv3/

