#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

source $SCRIPT_DIR/venv/bin/activate
source $SCRIPT_DIR/.API_KEY

python3 $SCRIPT_DIR/src/main.py