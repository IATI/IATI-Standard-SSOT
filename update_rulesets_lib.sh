#!/bin/bash

## This script updates IATI-Rulesets repo with codelists and schemas

# make sure we have all submodules loaded and create a branch in IATI-Rulesets
git submodule update --init --recursive || exit 1
cd IATI-Rulesets
git checkout master
git checkout codelist-schema-update || git checkout -b codelist-schema-update 
cd ../

# Update codelists in IATI-Rulesets from IATI-Codelists
for VER in 1.04 1.05 2.01 2.02 2.03 ; do
    echo "Updating codelist for version-$VER"
    cd IATI-Codelists
    git checkout version-$VER
    cp -R xml/ ../IATI-Rulesets/lib/schemata/$VER/codelist/
    cd ../
done

# Update schemas in IATI-Rulesets from IATI-Schemas
for VER in 1.01 1.02 1.03 1.04 1.05 2.01 2.02 2.03 ; do
    echo "Updating schemas for version-$VER"
    cd IATI-Schemas
    git checkout version-$VER
    cp iati-activities-schema.xsd ../IATI-Rulesets/lib/schemata/$VER/
    cp iati-common.xsd ../IATI-Rulesets/lib/schemata/$VER/
    cp iati-organisations-schema.xsd ../IATI-Rulesets/lib/schemata/$VER/
    cp xml.xsd ../IATI-Rulesets/lib/schemata/$VER/
    cd ../
done

# Copy non-embedded codelists
git clone git@github.com:IATI/IATI-Codelists-NonEmbedded.git || exit 1
cd IATI-Codelists-NonEmbedded
git checkout master || exit 1
cp -R xml/ ../IATI-Rulesets/lib/schemata/non-embedded-codelist/ || exit 1
cd ../
rm -rf IATI-Codelists-NonEmbedded || exit 1 # clean up 
