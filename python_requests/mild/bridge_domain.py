'''Python Requests Exercise - Getting and creating a bridge domain

This script, once completed, allows the user to retrieve all the bridge
domains that currently exist on the APIC. This script will also allow the
user to create their own bridge domain under a selected tenant. Note that
authentication token is needed for the API calls, for which the script
imports the get_token function from authentication module (authentication.py).

- SPICE LEVEL: MILD
- TASK: Replace the <TODO> with correct code based on the lab guide
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

    url = "https://apic/api/class/<TODO>.json"

    response = requests.request(<TODO>, url, <TODO>, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {<TODO>} for {url}>")

    #response_dict = response.<TODO>

    # Print out the Bridge Domains
    # <TODO>

def create_bridge_domain(cookie, tenant, bd_name, subnet):
    '''Creates a new ACI bridge domain'''

    #url = f"https://apic/api/mo/uni/tn-{<TODO>}.json"

    #payload = <TODO>

    #response = requests.request(<TODO>, url, cookies=cookie, data=payload, verify=False)

    # Print the status code with the URL for information purpose
    #print(f"<Status code {<TODO>} for creating {bd_name} at {url}>")

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    token_cookie = get_token()
    get_bridge_domains(token_cookie)