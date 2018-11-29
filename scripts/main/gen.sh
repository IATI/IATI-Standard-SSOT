#!/bin/bash
set -o nounset

bash scripts/main/gen_rst.sh || exit $?
bash scripts/main/gen_html.sh || exit $?
