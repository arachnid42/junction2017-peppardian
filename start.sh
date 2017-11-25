#!/usr/bin/env bash
#
# No docs yet

readonly PWD="$(pwd)"
readonly PYNAOQI_PYTHONPATH_PREFIX="${PWD}/pynaoqi/lib/python2.7/site-packages"

if [[ ! "X${PYTHONPATH}/${PYNAOQI_PYTHONPATH_PREFIX}" = "X${PYTHONPATH}" ]]
then
    export PYTHONPATH="${PYTHONPATH}:${PYNAOQI_PYTHONPATH_PREFIX}"
fi

# start shit here
