'''Python Requests sample script - Making an ACI GET request

This script allows the user to query the selected ACI class or
MO and returns the response as Python Dictionary.
'''

# Import required libraries
import requests
import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def get_class(classname, apic, cookie):
    '''GET the objects belonging to the specified ACI class'''

    url = f"{apic}/api/class/{classname}.json"
    response = requests.request("GET", url, cookies=cookie, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")

    return response.json()["imdata"]

def get_mo(mo_dn, apic, cookie):
    '''GET a specified ACI Managed Object (MO)'''

    url = f"{apic}/api/mo/{mo_dn}.json"
    response = requests.request("GET", url, cookies=cookie, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")

    return response.json()["imdata"]
