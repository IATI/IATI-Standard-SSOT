#!/bin/bash
set -o nounset

sh scripts/main/gen_rst.sh || exit $?
sh scripts/main/gen_html.sh || exit $?
