#!/bin/bash

venv_name="asiayo-pretest-env"

# Check if Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed."
    exit 1
fi

# Activate the virtual environment
source $venv_name/bin/activate

# run unit test
pytest