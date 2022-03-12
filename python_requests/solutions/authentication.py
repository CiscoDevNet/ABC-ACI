'''Python Requests Excercise - Getting APIC Authentication Token

SOLUTION FILE

This script, once completed, allows the user to retrieve an Authentication
Token to be used when sending API calls against Cisco APIC.
'''

# Import required libraries
import json
import requests
import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def get_token():
    '''Return a Cisco APIC authentication token'''

    url = "https://apic/api/aaaLogin.json"

    payload = json.dumps({
        "aaaUser": {
            "attributes": {
            "name": "developer",
            "pwd": "1234QWer"
            }
        }
    })

    response = requests.request("POST", url, data=payload, verify=False)

    # Print the status code with the URL for information purpose
    print(f"<Status code {response.status_code} for {url}>")

    # Return the Authentication cookie so it can be used in API calls
    return response.cookies

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    token_cookie = get_token()
    print(token_cookie)
