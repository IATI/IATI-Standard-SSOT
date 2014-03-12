#!/bin/bash
set -o nounset

./gen_rst.sh || exit $?
./gen_html.sh || exit $?
