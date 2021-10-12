import requests
import json
from credentials import *

# Disable warnings for insecure certificates (self-signed)
requests.packages.urllib3.disable_warnings(
    category=requests.packages.urllib3.exceptions.InsecureRequestWarning
)


def get_request(apic, cookies, uri):
    url = apic + uri
    print("\n-----------------------------------------------------------------")
    print("\nExecuting API Call: GET")
    print("\nURL: {}".format(url))

    req = requests.get(url, cookies=cookies, verify=False)
    print("\nSTATUS CODE: {}".format(req.status_code))
    print("\nRESPONSE: {}".format(req.text))
    return req


def post_request(apic, cookies, uri, payload):
    url = apic + uri
    print("\n-----------------------------------------------------------------")
    print("\nExecuting API Call: POST")
    print("\nURL: {}".format(url))
    print("\nBODY: {}".format(payload))

    req = requests.post(url, cookies=cookies, data=payload, verify=False)
    print("\nSTATUS CODE: {}".format(req.status_code))
    print("\nRESPONSE: {}".format(req.text))
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

    # Create new VRF
    vrf = {
        "fvCtx": {
            "attributes": {
                "dn": "uni/tn-ACI-Python/ctx-ACI-Python_VRF",
                "name": "ACI-Python_VRF",
                "rn": "ctx-ACI-Python_VRF",
                "status": "created",
            }
        }
    }
    path = "/api/mo/uni/tn-ACI-Python/ctx-ACI-Python_VRF.json"

    rsp = post_request(APIC_HOST, cookies, path, json.dumps(vrf))

if __name__ == "__main__":
    main()
