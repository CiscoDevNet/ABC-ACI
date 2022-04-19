"""
Simple script to restore one or more tenants from a local JSON file
to the APIC using pyATS as the connection handler / API wrapper

Testbed is hardcoded - this could be changed to accept an optional
testbed filename using argparse.

For information on the APIC rest.connector and using pyATS to interact
with the APIC using Python, check

https://developer.cisco.com/docs/rest-connector/
"""
import os
import sys
import json
from json.decoder import JSONDecodeError
from pyats.topology import loader
from pyats.utils.yaml import exceptions as pyats_exception

# Read the pyATS Testbed and set 'device' to the APIC.  If the
# testbed can't be loaded, print a message and exit
try:
    testbed = loader.load('testbed.yml')
    device = testbed.devices['apic']
except pyats_exception.LoadError:
    print("Unable to load pyATS Testbed file - terminating.")
    sys.exit(255)


def get_backup_data(filename):
    """
    Load the JSON contents of a backup file.  If the file doesn't exist
    or is not valid JSON, fail somewhat gracefully and raise a RuntimeError

    :param filename: Filename of backup to load
    :return: JSON-formatted string of imported backup data
    """
    try:
        # Open and store the data from the backup file
        with open(filename, "r", encoding="utf-8") as backup_file:
            backup_data = json.loads(backup_file.read())

    except FileNotFoundError:
        # File doesn't exist - print error message and create a RuntimeError
        print(f"Unable to open {filename} - check that the backup file exists and retry")
        raise RuntimeError from FileNotFoundError

    except JSONDecodeError:
        # Invalid JSON!  Raise RuntimeError
        print(f"{filename} does not contain JSON data.  Verify the contents and retry")
        raise RuntimeError from ValueError

    except Exception as _err:
        # Unhandled exception - print a generic error
        print(f"An unhandled exception was caught:\n{_err}")
        raise RuntimeError from Exception

    return backup_data


def restore_configs(filename):
    """
    Given a filename, load the JSON data and restore the tenant data stored in the
    backup

    :param filename: Filename (including path if necessary) to restore
    """
    print(f"\nBeginning restore of {filename}:")
    try:
        restore_data = get_backup_data(filename)
        print(f"\tProcessing tenant '{restore_data['fvTenant']['attributes']['name']}'...")

        # Set the DN to the MO of the tenant being processed then invoke the post method
        tenant_dn = f"/api/node/mo/{restore_data['fvTenant']['attributes']['dn']}.json"
        device.post(dn=tenant_dn, payload=restore_data)

    except RuntimeError:
        # If a RuntimeError was raised in get_backup_data, just print a newline
        # to separate the error message from the prompt to make it easier to see :)
        print()


if __name__ == "__main__":

    # Get the command line arguments.
    # Note: The first element of 'sys.argv' would be the script name,
    # so using the index of [1:] sets restore_file_list to have all arguments
    # beginning at index 1, omitting the name of this script.
    restore_file_list = sys.argv[1:]

    if restore_file_list:
        # If there are any files listed to restore, connect and restore each to the APIC
        device.connect()
        for file in restore_file_list:
            restore_configs(filename=file)
    else:
        # Otherwise, print usage information.
        # Note: os.path.basename(__file__) will print the name of the script without
        # any directory information.
        print("\nRestore tenant(s) from JSON backup files to APIC.\n"
              "\nUsage:\n"
              f"\t{os.path.basename(__file__)} /path/to/file.json </path/to/file2.json> <...>\n"
              )
