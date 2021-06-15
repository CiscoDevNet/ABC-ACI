#! /usr/bin/env python
"""
The goal is to take the requests stripped from the API inspector,
pass them through the requests module, and configure a tenant that
is the same tenant that we configured using the GUI to get the 
API calls and paylod.
We will need to ensure that our previously configured tenant
is deleted from the fabric prior to running this Python code
"""

import requests
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://10.10.20.14/api/"

def fabric_login():
    URI = "aaaLogin.json"
    PAYLOAD = {"aaaUser":{"attributes":{"name":"admin","pwd":"C1sco12345"}}}

    RESPONSE = requests.post(BASE_URL + URI, data=json.dumps(PAYLOAD), verify=False)

    APIC_COOKIE = RESPONSE.cookies["APIC-cookie"]

    HEADER = {"Cookie": "APIC-cookie=" + APIC_COOKIE}
    
    return HEADER

def configure_tenant(header):
    TENANT_PAYLOAD = {"fvTenant":{"attributes":{"dn":"uni/tn-Aardvark-1","name":"Aardvark-1","rn":"tn-Aardvark-1","status":"created,modified"},"children":[{"fvCtx":{"attributes":{"dn":"uni/tn-Aardvark-1/ctx-api_inspector","name":"api_inspector","rn":"ctx-api_inspector","status":"created,modified"},"children":[]}}]}}
    URI = "node/mo/uni/tn-Aardvark-1.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(TENANT_PAYLOAD), verify=False)

    print("Configuring Tenant...")
    if RESPONSE.status_code == requests.codes.ok:
        print("Tenant configured.  200 OK Received")
    else:
        print("Tenant not configured. Something went wrong")

def configure_bd(header):
    BD_PAYLOAD =  #TO DO add modified JSON Payload from the API Inspector

    URI = "node/mo/uni/tn-Aardvark-1/BD-api_inspector.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(BD_PAYLOAD), verify=False)
    
    print("Configuring Bridge Domain (BD)...")
    if RESPONSE.status_code == requests.codes.ok:
        print("BD configured.  200 OK Received")
    else:
        print("BD not configured. Something went wrong")







def main():
    HEADER = fabric_login()

    configure_tenant(HEADER)
    configure_bd(HEADER)
    

    TENANT = requests.get(BASE_URL + "node/mo/uni/tn-Aardvark-1.json?rsp-subtree=full", headers=HEADER, verify=False)

    #print("The resulting generated tenant configuration:")
    #print(json.dumps(TENANT.json(), indent=2))

# Run it!
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
