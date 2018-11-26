#!/bin/bash

# Create a virtual environment (recommended)
virtualenv pyenv

# Activate the virtual environment if you created one
# This must repeated each time you open a new shell
source pyenv/bin/activate

# Install python requirements
pip install -r requirements.txt

# Clones the initial components
sh clone_components.sh