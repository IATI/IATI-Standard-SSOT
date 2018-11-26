#!/bin/bash
set -o nounset

./scripts/main/gen_rst.sh || exit $?
./scripts/main/gen_html.sh || exit $?
