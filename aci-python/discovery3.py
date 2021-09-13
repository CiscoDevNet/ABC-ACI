import TODO
import json
from credentials import *

# Disable warnings for insecure certificates (self-signed)
requests.packages.urllib3.disable_warnings(
    category=requests.packages.urllib3.exceptions.InsecureRequestWarning
)


def TODO(apic, cookies, uri):
    url = apic + uri
    print("\n-----------------------------------------------------------------")
    print("\nExecuting API Call: GET")
    print("\nURL: {}".format(url))
tree
    req = requests.get(url, cookies=cookies, verify=False)
    print("\nSTATUS CODE: {}".format(req.status_code))
    print("\nRESPONSE: {}".format(req.text))
    return req


def TODO(apic, cookies, uri, payload):
    url = apic + uri
    print("\n-----------------------------------------------------------------")
    print("\nExecuting API Call: POST")
    print("\nURL: {}".format(url))
    print("\nBODY: {}".format(payload))

    req = requests.post(url, cookies=cookies, data=payload, verify=False)
    print("\nSTATUS CODE: {}".format(req.status_code))
    print("\nRESPONSE: {}".format(req.text))
    return req


def TODO(apic):
    uri = "/api/aaaLogin.json"
    credentials = {
        "aaaUser": {"attributes": {"name": APIC_USERNAME, "pwd": APIC_PASSWORD}}
    }
    authenticate = post_request(
        apic=apic, cookies={}, uri=uri, payload=TODO(credentials)
    )

    if not authenticate.ok:
        print("\n[ERROR] Authentication failed! APIC responded with:")
        print(json.dumps(json.loads(authenticate.text), indent=4))
        exit()

    print("\n[OK] Authentication successful!")
    return authenticate.cookies


def TODO():
    cookies = get_cookies(APIC_HOST)

    # Creating a New Tenant
    tenant = {
        "fvTenant": {
            "attributes": {"name": "Discovery3"}
        }
    }
    path = "/api/mo/uni/TODO.json"
    rsp = post_request(APIC_HOST, cookies, path, json.dumps(tenant))
    
    # Create new VRF
    vrf = {
        "fvCtx": {
            "attributes": {
                "dn": "uni/tn-Discovery3/TODO",
                "name": "Discovery3_VRF",
                "rn": "Discovery3_VRF",
                "status": "created,modified",
            }
        }
    }
    path = "/api/mo/uni/tn-Discovery3/ctx-Discovery3_VRF.json"

    rsp = post_request(APIC_HOST, cookies, path, json.dumps(vrf))

if __name__ == "__main__":
    main()
