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
    TENANT_PAYLOAD = {"fvTenant":{"attributes":{"dn":"uni/tn-Aardvark-1","name":"Aardvark-1","rn":"tn-Aardvark-1","status":"created"},"children":[{"fvCtx":{"attributes":{"dn":"uni/tn-Aardvark-1/ctx-Aardvark-1","name":"Aardvark-1","rn":"ctx-Aardvark-1","status":"created"},"children":[]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(TENANT_PAYLOAD), verify=False)

    print("Configuring Tenant...")
    if RESPONSE.status_code == requests.codes.ok:
        print("Tenant configured.  200 OK Received")
    else:
        print("Tenant not configured. Something went wrong")

def configure_bd(header):
    BD_PAYLOAD = {"fvBD":{"attributes":{"dn":"uni/tn-Aardvark-1/BD-Aardvark-BD","mac":"00:22:BD:F8:19:FF","arpFlood":"true","name":"Aardvark-BD","rn":"BD-Aardvark-BD","status":"created"},"children":[{"fvSubnet":{"attributes":{"dn":"uni/tn-Aardvark-1/BD-Aardvark-BD/subnet-[10.10.10.1/24]","ctrl":"","ip":"10.10.10.1/24","rn":"subnet-[10.10.10.1/24]","status":"created"},"children":[]}},{"fvRsCtx":{"attributes":{"tnFvCtxName":"Aardvark-1","status":"created,modified"},"children":[]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1/BD-Aardvark-BD.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(BD_PAYLOAD), verify=False)
    
    print("Configuring Bridge Domain (BD)...")
    if RESPONSE.status_code == requests.codes.ok:
        print("BD configured.  200 OK Received")
    else:
        print("BD not configured. Something went wrong")

def configure_web_filter(header):
    WEB_FILTER_PAYLOAD = {"vzFilter":{"attributes":{"dn":"uni/tn-Aardvark-1/flt-web-filter","name":"web-filter","rn":"flt-web-filter","status":"created,modified"},"children":[{"vzEntry":{"attributes":{"dn":"uni/tn-Aardvark-1/flt-web-filter/e-http","name":"http","etherT":"ip","prot":"tcp","dFromPort":"http","dToPort":"http","rn":"e-http","status":"created,modified"},"children":[]}},{"vzEntry":{"attributes":{"dn":"uni/tn-Aardvark-1/flt-web-filter/e-https","name":"https","etherT":"ip","prot":"tcp","dFromPort":"https","dToPort":"https","rn":"e-https","status":"created,modified"},"children":[]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1/flt-web-filter.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(WEB_FILTER_PAYLOAD), verify=False)

    print("Configuring web filter...")
    if RESPONSE.status_code == requests.codes.ok:
        print("Filter configured.  200 OK Received")
    else:
        print("Filter not configured. Something went wrong")

def configure_db_filter(header):
    DB_FILTER_PAYLOAD = {"vzFilter":{"attributes":{"dn":"uni/tn-Aardvark-1/flt-db-filter","name":"db-filter","rn":"flt-db-filter","status":"created,modified"},"children":[{"vzEntry":{"attributes":{"dn":"uni/tn-Aardvark-1/flt-db-filter/e-sql","name":"sql","etherT":"ip","prot":"tcp","dFromPort":"1433","dToPort":"1433","rn":"e-sql","status":"created,modified"},"children":[]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1/flt-db-filter.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(DB_FILTER_PAYLOAD), verify=False)
    
    print("Configuring database filter...")
    if RESPONSE.status_code == requests.codes.ok:
        print("Filter configured.  200 OK Received")
    else:
        print("Filter not configured. Something went wrong")

def configure_web_contract(header):
    WEB_CONTRACT_PAYLOAD = {"vzBrCP":{"attributes":{"dn":"uni/tn-Aardvark-1/brc-web-contract","name":"web-contract","rn":"brc-web-contract","status":"created"},"children":[{"vzSubj":{"attributes":{"dn":"uni/tn-Aardvark-1/brc-web-contract/subj-web","name":"web","rn":"subj-web","status":"created"},"children":[{"vzRsSubjFiltAtt":{"attributes":{"status":"created,modified","tnVzFilterName":"web-filter","directives":"none"},"children":[]}}]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1/brc-web-contract.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(WEB_CONTRACT_PAYLOAD), verify=False)
    
    print("Configuring web contract...")
    if RESPONSE.status_code == requests.codes.ok:
        print("Contract configured.  200 OK Received")
    else:
        print("Contract not configured. Something went wrong")

def configure_db_contract(header):
    DB_CONTRACT_PAYLOAD = {"vzBrCP":{"attributes":{"dn":"uni/tn-Aardvark-1/brc-db-contract","name":"db-contract","rn":"brc-db-contract","status":"created"},"children":[{"vzSubj":{"attributes":{"dn":"uni/tn-Aardvark-1/brc-db-contract/subj-db","name":"db","rn":"subj-db","status":"created"},"children":[{"vzRsSubjFiltAtt":{"attributes":{"status":"created,modified","tnVzFilterName":"db-filter","directives":"none"},"children":[]}}]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1/brc-db-contract.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(DB_CONTRACT_PAYLOAD), verify=False)
    
    print("Configuring database contract...")
    if RESPONSE.status_code == requests.codes.ok:
        print("Contract configured.  200 OK Received")
    else:
        print("Contract not configured. Something went wrong")

def configure_ap(header):
    AP_PAYLOAD = {"fvAp":{"attributes":{"dn":"uni/tn-Aardvark-1/ap-Aardvark-1-AP","name":"Aardvark-1-AP","rn":"ap-Aardvark-1-AP","status":"created"},"children":[{"fvAEPg":{"attributes":{"dn":"uni/tn-Aardvark-1/ap-Aardvark-1-AP/epg-db","name":"db","rn":"epg-db","status":"created"},"children":[{"fvRsPathAtt":{"attributes":{"tDn":"topology/pod-1/paths-102/pathep-[eth1/5]","encap":"vlan-100","status":"created"},"children":[]}},{"fvRsBd":{"attributes":{"tnFvBDName":"Aardvark-BD","status":"created,modified"},"children":[]}},{"fvRsProv":{"attributes":{"tnVzBrCPName":"db-contract","status":"created,modified"},"children":[]}}]}},{"fvAEPg":{"attributes":{"dn":"uni/tn-Aardvark-1/ap-Aardvark-1-AP/epg-web","name":"web","rn":"epg-web","status":"created"},"children":[{"fvRsPathAtt":{"attributes":{"tDn":"topology/pod-1/paths-101/pathep-[eth1/5]","encap":"vlan-100","status":"created"},"children":[]}},{"fvRsBd":{"attributes":{"tnFvBDName":"Aardvark-BD","status":"created,modified"},"children":[]}},{"fvRsProv":{"attributes":{"tnVzBrCPName":"web-contract","status":"created,modified"},"children":[]}},{"fvRsCons":{"attributes":{"tnVzBrCPName":"db-contract","status":"created,modified"},"children":[]}}]}}]}}

    URI = "node/mo/uni/tn-Aardvark-1/ap-Aardvark-1-AP.json"

    RESPONSE = requests.post(BASE_URL + URI, headers=header, data=json.dumps(AP_PAYLOAD), verify=False)
    
    print("Configuring application profile (AP)...")
    if RESPONSE.status_code == requests.codes.ok:
        print("AP configured.  200 OK Received")
    else:
        print("AP not configured. Something went wrong")

def main():
    HEADER = fabric_login()

    configure_tenant(HEADER)
    configure_bd(HEADER)
    configure_web_filter(HEADER)
    configure_db_filter(HEADER)
    configure_web_contract(HEADER)
    configure_db_contract(HEADER)
    configure_ap(HEADER)

    TENANT = requests.get(BASE_URL + "node/mo/uni/tn-Aardvark-1.json?rsp-subtree=full", headers=HEADER, verify=False)

    print("The resulting generated tenant configuration:")
    print(json.dumps(TENANT.json(), indent=2))

# Run it!
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
