'''Python Requests Excercise - Creating a new endpoint group

This script, once completed, allows the user to create their own bridge
endpoint group under a selected application profile and linked to a selected
bridge domain. Note that authentication token is needed for the API calls, for
which the script imports the get_token function from authentication module
(authentication.py).

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

def get_epgs(cookie):
    '''Prints out all the ACI endpoint groups'''

    # TODO: Code to retrieve and print out all the EPGs

def create_epg(cookie, tenant_name, bd_name, ap_name, epg_name):
    '''Creates a new ACI endpoint group'''

    # TODO: Code to create a new EPG

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    token_cookie = get_token()
    get_epgs(token_cookie)
