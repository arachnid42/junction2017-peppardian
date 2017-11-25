#!/usr/bin/env bash
#
# No docs yet
source config.sh

python3 -m venv "$(config_get venv_home)"
source ./venv/bin/activate

pip3 install -r "$(config_get python_req)"
# Niiice
