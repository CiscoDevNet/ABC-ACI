import requests
import json
from credentials import *

# Disable warnings for insecure certificates (self-signed)
requests.packages.urllib3.disable_warnings(
    category=requests.packages.urllib3.exceptions.InsecureRequestWarning
)
def post_request(apic, cookies, uri, payload):
    url = apic + uri
    print("\n-----------------------------------------------------------------")
    print("\nExecuting API Call: POST")
    print("\nURL: {}".format(url))
    print("\nBODY: {}".format(payload))

    req = requests.post(url, cookies=cookies, data=payload, verify=False)
    print("\nSTATUS CODE: {}".format(req.status_code))
    return req

def get_cookies(apic):
    uri = "/api/aaaLogin.json"
    credentials = {
        "aaaUser": {"attributes": {"name": APIC_USERNAME, "pwd": APIC_PASSWORD}}
    }
    authenticate = post_request(
        apic=apic, cookies={}, uri=uri, payload=json.dumps(credentials)
    )

    if not authenticate.ok:
        print("\n[ERROR] Authentication failed! APIC responded with:")
        print(json.dumps(json.loads(authenticate.text), indent=4))
        exit()

    print("\n[OK] Authentication successful!")
    return authenticate.cookies

def main():
    cookies = get_cookies(APIC_HOST)

if __name__ == "__main__":
    main()
