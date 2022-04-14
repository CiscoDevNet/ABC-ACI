'''Python Requests sample script - Making an ACI POST request

This script allows the user to make a POST request against a specified
ACI MO to either edit and existing MO or to create a new MO.
'''

# Import required libraries
import json
import requests
import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def post_mo(mo_dn, payload, apic, cookie):
    '''Make a POST request against an ACI managed object.'''

    if not isinstance(payload, str): # check if the payload is JSON
        payload = json.dumps(payload)

    url = f"{apic}/api/mo/{mo_dn}.json"
    response = requests.request("POST", url, cookies=cookie, data=payload, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")
