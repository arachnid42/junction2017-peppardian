#!/usr/bin/env bash
#
# No docs yet
source config.sh

# colors!
readonly COL_RED="$(tput setaf 1)"
readonly COL_GREEN="$(tput setaf 2)"
readonly COL_RESET="$(tput sgr0)"

echo "${COL_GREEN}[i] Bootstrapping server \\(0^0)/${COL_RESET}"

# bootstrap venv if it was not created before
if [[ ! -d "$(config_get venv_home)" ]]; then
    echo "${COL_GREEN}[i] Building venv /-_-/${COL_RESET}"
    bash ./bootstrap.sh
fi

# get into venv
source ./venv/bin/activate

# run ML server
echo "${COL_GREEN}[i] Starting server (*-*)${COL_RESET}"
#./mlserver.py
