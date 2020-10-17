#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -Ur requirements.txt

echo "All done!"