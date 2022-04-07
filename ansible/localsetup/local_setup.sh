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

# LAB: Ansible
#
# Tasks:
#  - Copy any task, play, or variable files from the solutions into
#    ~student/ansible.  This script will overwrite any existing files
#    of the same name in the destination.  Used if the previous lab
#    was not completed.
#
LAB_WORKING_PATH=~student/ansible

FILES_TO_COPY="inventory.yml \
host_vars/apic/apic_vars.yml \
host_vars/apic/tenant_vars.yml \
host_vars/apic/vault.yml \
ansible.cfg"

for FILE in ${FILES_TO_COPY}; do
  echo "Copying ${FILE}..."
  mkdir -p ${LAB_WORKING_PATH}/$( dirname ${FILE} )
  cp -fp "${LAB_PATH}/solutions/${FILE}" "${LAB_WORKING_PATH}/${FILE}"
done

echo
echo "******************************************************************************"
echo "Local setup tasks complete!"
echo "******************************************************************************"
