'''Python Requests Excercise - Creating a new endpoint group

SOLUTION FILE

This script, once completed, allows the user to create their own bridge
endpoint group under a selected application profile and linked to a selected
bridge domain. Note that authentication token is needed for the API calls, for
which the script imports the get_token function from authentication module
(authentication.py).
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

    url = "https://apic/api/class/fvAEPg.json"

    response = requests.request("GET", url, cookies=cookie, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")

    response_dict = response.json()

    # Print out the EPGs
    for epg in response_dict["imdata"]:
        print(epg["fvAEPg"]["attributes"]["name"])

def create_epg(cookie, tenant_name, bd_name, ap_name, epg_name):
    '''Creates a new ACI endpoint group'''

    url = f"https://apic/api/mo/uni/tn-{tenant_name}/ap-{ap_name}.json"

    payload = json.dumps({
        "fvAEPg": {
            "attributes": {
                "name": epg_name,
                "status": "created"
            },
            "children": [
                {
                    "fvRsBd": {
                        "attributes": {
                            "tnFvBDName":bd_name,
                            "status":"created,modified"
                        }
                    }
                }
            ]
        }
    })

    response = requests.request("POST", url, cookies=cookie, data=payload, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for creating {epg_name} at {url}>")

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    TENANT_NAME = "Sales"
    BD_NAME = "DB_BD"
    AP_NAME = "eCommerce"
    EPG_NAME = "DB_EPG"

    token_cookie = get_token()
    get_epgs(token_cookie)
    create_epg(token_cookie, TENANT_NAME, BD_NAME, AP_NAME, EPG_NAME)
    get_epgs(token_cookie)
