#!/bin/bash

echo "Starting to activate ..."
python3.10 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install -r requirements_dev.txt
