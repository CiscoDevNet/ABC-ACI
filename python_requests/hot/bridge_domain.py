'''Python Requests Exercise - Getting and creating a bridge domain

This script, once completed, allows the user to retrieve all the bridge
domains that currently exist on the APIC. This script will also allow the
user to create their own bridge domain under a selected tenant. Note that
authentication token is needed for the API calls, for which the script
imports the get_token function from authentication module (authentication.py).

- SPICE LEVEL: HOT
- TASK: Replace the # TODO comments with correct code based on the lab guide
  instructions

'''

# Import required libraries
import json
import requests
import urllib3

# Import the function get_token from authentication.py
from authentication import get_token

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def get_bridge_domains(cookie):
    '''Prints out all the ACI bridge domains'''

    # TODO: Code to retrieve and print out all the bridge domains

def create_bridge_domain(cookie, tenant, bd_name, subnet):
    '''Creates a new ACI bridge domain'''

    # TODO: Code to create a new bridge domain

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    token_cookie = get_token()
    get_bridge_domains(token_cookie)