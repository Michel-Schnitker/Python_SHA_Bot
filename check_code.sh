#!/bin/bash

# Copied from https://stackoverflow.com/a/26759734/18680554
if ! [ -x "$(command -v mypy)" ]; then
  echo 'Error: mypy is not installed. Get it by installing requirements.txt' >&2
  exit 1
fi

if ! [ -x "$(command -v flake8)" ]; then
  echo 'Error: flake8 is not installed. Get it by installing requirements.txt' >&2
  exit 1
fi

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
source $SCRIPT_DIR/venv/bin/activate

dmypy run src
flake8 src --max-line-length=200
