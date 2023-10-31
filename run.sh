#!/bin/bash

venv_name="asiayo-pretest-env"

# Check if Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed."
    exit 1
fi

# Create a virtual environment
python3 -m venv $venv_name

# Activate the virtual environment
source $venv_name/bin/activate

# Install packages
pip install --upgrade pip
pip3 install -r requirement.txt

echo "$venv_name has been set up."

# run the server
python3 api.py