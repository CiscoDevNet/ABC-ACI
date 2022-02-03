'''Python Requests Exercise - Getting and creating a bridge domain

SOLUTION FILE

This script, once completed, allows the user to retrieve all the bridge
domains that currently exist on the APIC. This script will also allow the
user to create their own bridge domain under a selected tenant. Note that
authentication token is needed for the API calls, for which the script
imports the get_token function from authentication module (authentication.py).
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

    url = "https://apic/api/class/fvBD.json"

    response = requests.request("GET", url, cookies=cookie, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")

    response_dict = response.json()

    # Print out the Bridge Domains
    for bridge_domain in response_dict["imdata"]:
        print(bridge_domain["fvBD"]["attributes"]["name"])

def create_bridge_domain(cookie, tenant, bd_name, subnet):
    '''Creates a new ACI bridge domain'''

    url = f"https://apic/api/mo/uni/tn-{tenant}.json"

    payload = json.dumps({
        "fvBD": {
            "attributes": {
                "name": bd_name
            },
            "children": [
                {
                    "fvSubnet": {
                        "attributes": {
                            "ip": subnet
                        }
                    }
                }
            ]
        }
    })

    response = requests.request("POST", url, cookies=cookie, data=payload, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for creating {bd_name} at {url}>")

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    TENANT_NAME = "Sales"
    BD_NAME = "DB_BD"
    BD_SUBNET = "10.0.2.254/24"

    token_cookie = get_token()
    get_bridge_domains(token_cookie)
    create_bridge_domain(token_cookie, TENANT_NAME, BD_NAME, BD_SUBNET)
    get_bridge_domains(token_cookie)
