#!/bin/sh
#####
# Perform lab-specific setup tasks
# This file should be invoked from the top-level prepare_lab.sh file and will
# copy any necessary "fast forward" configuration or exercise files into the
# default working directory
#####

echo
echo "******************************************************************************"
echo "Beginning local setup tasks..."
echo "******************************************************************************"
echo

# LAB: Python requests
#
# Tasks:
#  - Copy postman environment and collections from previous
#  lab(s) to a postman/ directory in the student working path
#  for this lab.  Used if the previous lab was not completed.
#
LAB_WORKING_PATH=~student/python_requests/postman

POSTMAN_ENV_PATH=${LAB_PATH}/../visore_postman/solutions
POSTMAN_COLLECTION_PATH=${LAB_PATH}/../api_inspector/solutions


FILES_TO_COPY="${POSTMAN_ENV_PATH}/APIC.postman_environment.json,\
${POSTMAN_COLLECTION_PATH}/ABC ACI.postman_collection.json"

# Ensure the working path exists
mkdir -p ${LAB_WORKING_PATH}

# Filename(s) contain spaces.  Change delimiter to comma for the
# copy loop
IFS=","

for FILE in ${FILES_TO_COPY}; do
  echo "Copying $(basename ${FILE})..."
  cp -fp ${FILE} ${LAB_WORKING_PATH}
done

echo
echo "******************************************************************************"
echo "Local setup tasks complete!"
echo "******************************************************************************"
