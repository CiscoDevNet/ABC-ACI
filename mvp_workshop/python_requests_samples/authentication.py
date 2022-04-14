'''Python Requests sample script - Getting APIC Authentication Token

This script allows the user to retrieve an Authentication
Token to be used when sending API calls against Cisco APIC.
'''

# Import required libraries
import json
import requests
import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def get_token(apic, username, password):
    '''Return a Cisco APIC authentication token'''

    url = f"{apic}/api/aaaLogin.json"

    payload = json.dumps({
        "aaaUser": {
            "attributes": {
            "name": username,
            "pwd": password
            }
        }
    })

    response = requests.request("POST", url, data=payload, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")

    # Return the Authentication cookie so it can be used in API calls
    return response.cookies
