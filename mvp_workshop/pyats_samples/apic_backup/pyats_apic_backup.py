"""
Simple script to backup all tenants from APIC using pyATS as the
connection handler / API wrapper

Testbed is hardcoded - this could be changed to accept an optional
testbed filename using argparse.

For information on the APIC rest.connector and using pyATS to interact
with the APIC using Python, check

https://developer.cisco.com/docs/rest-connector/
"""
import sys
import json

from datetime import datetime
from pathlib import Path
from pyats.topology import loader
from pyats.utils.yaml import exceptions as pyats_exception

# Set the time and datestamp for backup directory and filenames
DATESTAMP = datetime.now().strftime('%Y-%m-%d')
TIMESTAMP = datetime.now().strftime('%H%M%S')

# Location to store the backups
BACKUP_PATH = f"./backups/{DATESTAMP}"

try:
    testbed = loader.load('testbed.yml')
    device = testbed.devices['apic']
except pyats_exception.LoadError:
    print("Unable to load pyATS Testbed file - terminating.")
    sys.exit(255)


def save_output(filename, backup_data):
    """
    Write the backup data as JSON to a file

    :param filename: Output filename for saved JSON
    :param backup_data: Backup data to write to file
    """
    try:
        with open(filename, "w", encoding="utf-8") as backup_file:
            json.dump(backup_data, backup_file)
            print(f"saved to file '{filename}'")
    except Exception as _err:
        print(f"Caught unhandled exception writing to backup file:\n{_err}")


def get_all_tenants():
    """
    Get all configurable attributes for all fvTenant objects

    :return: Dictionary output from the fvTenant class in APIC
    """
    tenant_dn = "/api/node/class/fvTenant.json"
    return device.get(dn=tenant_dn, rsp_prop_include='config-only', rsp_subtree='full')


def backup_tenants():
    """
    Get all tenants from the APIC.  Iterate over the result dictionary to
    create individual backup files for each tenant.  Backup files will have
    the TIMESTAMP appended to prevent overwrite on subsequent invocations.
    """

    # Get all tenant data
    apic_data = get_all_tenants()

    # Iterate over the returned dict from APIC to create separate files
    for tenant in apic_data['imdata']:
        tenant_name = tenant['fvTenant']['attributes']['name']
        print(f"Backing up tenant '{tenant_name}'... ", end='')

        # Set the backup filename and write the data to the filesystem
        backup_file = f"{BACKUP_PATH}/{tenant_name}_{TIMESTAMP}.json"
        save_output(filename=backup_file, backup_data=tenant)


if __name__ == "__main__":
    try:
        # Create the backup path - do not error if it already exists
        Path(BACKUP_PATH).mkdir(parents=True, exist_ok=True)

        # Connect to the APIC and backup all tenants
        device.connect()
        backup_tenants()
    except PermissionError:
        # Can't create the directory - error gracefully
        print(f"Unable to create backup directory '{BACKUP_PATH}' - "
              f"verify you have permission to write to this location")
    except Exception as err:
        # Some error has occurred which we didn't explicitly catch...
        print(f"Unhandled exception caught: {err}")
