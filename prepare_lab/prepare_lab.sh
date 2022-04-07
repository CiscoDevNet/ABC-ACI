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
LAB_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Python interpreter
PYTHON_VENV=~student/py3venv
PYTHON_BIN=${PYTHON_VENV}/bin/python
PYTHON_PIP_BIN=${PYTHON_VENV}/bin/pip

# Full path and name of the script to run
PYTHON_SCRIPT="${SCRIPT_BASEPATH}/prepare_lab.py"

# Expected config file (called script path and filename)
LAB_CONFIG="${LAB_PATH}/lab_setup.yml"

# Expected lab requirements.txt file
REPO_PIP_REQUIREMENTS=${SCRIPT_BASEPATH}/lab-requirements.txt
LAB_PIP_REQUIREMENTS=${LAB_PATH}/requirements.txt

# Generate the commandline
CMD="${PYTHON_BIN} ${PYTHON_SCRIPT} -c ${LAB_CONFIG}"

LOCAL_SETUP_SCRIPT="${LAB_PATH}/localsetup/local_setup.sh"

# And execute the script...
echo
echo "******************************************************************************"
echo "Beginning lab preparation tasks..."
echo "******************************************************************************"
echo


echo
echo "******************************************************************************"
echo "Installing additional Python packages..."
echo "******************************************************************************"
echo

[ -e ${REPO_PIP_REQUIREMENTS} ] && ${PYTHON_PIP_BIN} install -r ${REPO_PIP_REQUIREMENTS} 2>&1 > /dev/null

[ -e ${LAB_PIP_REQUIREMENTS} ] && ${PYTHON_PIP_BIN} install -r ${LAB_PIP_REQUIREMENTS} 2>&1 > /dev/null

${CMD}


# If there's a lab-local setup script, source it
if [ -f ${LOCAL_SETUP_SCRIPT} ]; then
  . ${LOCAL_SETUP_SCRIPT}
fi

echo
echo "******************************************************************************"
echo "Lab preparation tasks complete!"
echo "******************************************************************************"
echo
