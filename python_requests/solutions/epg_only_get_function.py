'''Python Requests Excercise - Creating a new endpoint group

SOLUTION FILE - ONLY GET FUNCTION

This script, once completed, allows the user to print out all the EPG names.
Note that authentication token is needed for the API calls, for which the script
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


# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    token_cookie = get_token()
    get_epgs(token_cookie)
