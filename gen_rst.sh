#!/bin/bash
set -o nounset

# Remove docs (the output directory), and recreate
rm -r outputs/*

# Generate csvs etc. from codelists
cd IATI-Codelists || exit 1
./gen.sh || exit 1
cd .. || exit 1


# Generate documentation from the Schema and Codelists etc
python preprocess_extra.py || exit 1
python gen.py || exit 1

# Copy rulesets SPEC
# cp IATI-Rulesets/SPEC.rst docs/en/rulesets/ruleset-spec.rst
