#!/bin/bash
set -o nounset

# deletes all components folders
rm -rf IATI-*

# deletes virtualenv
rm -rf pyenv

# deletes docs and docs-copy folders
rm -rf docs docs-copy