#!/bin/sh

# Generic shell script to call the prepare_lab.py setup script from any
# path inside the local repo.  Each path may have a lab_setup.yml file
# present - need to use that file to bring the lab environment up-to-date
# with the expected configuration for the current lab step.
# This allows this script to be placed in one directory and be symlinked from
# any subdirectory which contains a lab_setup.yml file.

# Obtain the true location of this script
SCRIPT_TRUEPATH="$( readlink -f $0 )"
# Extract the path of this script from the true path
SCRIPT_BASEPATH="$( dirname ${SCRIPT_TRUEPATH} )"
# Get the path for the called script (not the true script path)
CALLED_SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# Python interpreter
PYTHON_BIN=~student/py3venv/bin/python
# Name of the script to run
PYTHON_SCRIPTNAME=prepare_lab.py
# Expected config file (called script path and filename)
LAB_CONFIG="${CALLED_SCRIPT_PATH}/lab_setup.yml"
# Full path and name of the Python script to execute
PYTHON_SCRIPT="${SCRIPT_BASEPATH}/${PYTHON_SCRIPTNAME}"
# Generate the commandline
CMD="${PYTHON_BIN} ${PYTHON_SCRIPT} -c ${LAB_CONFIG}"

# And execute the script...
echo "Running lab setup script..."
${CMD}