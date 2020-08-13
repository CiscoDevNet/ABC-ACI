import login
import argparse
import logging
import requests
import hvac
import json
import os
logger = logging.getLogger('vault-verify')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vault Init')
    parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
    parser.add_argument('--log', default="DEBUG")
    args = parser.parse_args()

    logger.setLevel(args.log)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
    data = client.read("kv-v1/aci/bootcamp")
    username = data["data"]["ACI_USERNAME"]
    password = data["data"]["ACI_PASSWORD"]

    response = login.aaa_login(host="10.10.20.14", username="admin", password="badusername", verify=False)
    print(response.status_code)
    data = response.json()

    print(json.dumps(data, indent=4, sort_keys=True)) 

# All for the ACI workflow we want each of us to go over and automate, I was thinking to have the following:
# Create Tenant
# Create 3 Subnets
# Create 3 bridge domains and associate a subnet to each of them
# Create a VRF and associate the BDs with it
# Create 3 Endpoint Groups: web, app, db
# Create 2 contracts: app to web and db to app
# Create 2 filters for the contracts: one allowing http/https between app and web and the second one allowing sql between db and app
# Any thoughts? Quinn, John, anyone else

# {
#     "imdata": [
#         {
#             "aaaLogin": {
#                 "attributes": {
#                     "buildTime": "Fri Mar 27 00:33:56 PDT 2020",
#                     "changePassword": "no",
#                     "creationTime": "1597092375",
#                     "firstLoginTime": "1597092375",
#                     "firstName": "",
#                     "guiIdleTimeoutSeconds": "1200",
#                     "lastName": "",
#                     "maximumLifetimeSeconds": "86400",
#                     "node": "topology/pod-1/node-1",
#                     "refreshTimeoutSeconds": "600",
#                     "remoteUser": "false",
#                     "restTimeoutSeconds": "90",
#                     "sessionId": "GpRG8wIrSGKKHl1ux/7UHA==",
#                     "siteFingerprint": "Se0AKUO6ieRoJ8qq",
#                     "token": "QAEAAAAAAAAAAAAAAAAAABP6akBaRWfR3m1zzMPFnGDZs2/Ecw6i/HPkmdnM9DwaJAl3ITyAxUAd7OEUVdDPM8sH6Rbx1a8j9hPGbRsf0Mt4WVcOW2muYpPHJaC78TIbl6gGlCfcppy1yMjuHeJ3+oxXeGF1jh5pKVu2oCHeo4kwNP8tdKgEeVwcr4tgzeq3/Ef/sOd5RfWveucUMBKh2Q==",
#                     "unixUserId": "15374",
#                     "userName": "admin",
#                     "version": "4.2(3q)"
#                 },
#                 "children": [
#                     {
#                         "aaaUserDomain": {
#                             "attributes": {
#                                 "name": "all",
#                                 "rolesR": "admin",
#                                 "rolesW": "admin"
#                             },
#                             "children": [
#                                 {
#                                     "aaaReadRoles": {
#                                         "attributes": {}
#                                     }
#                                 },
#                                 {
#                                     "aaaWriteRoles": {
#                                         "attributes": {},
#                                         "children": [
#                                             {
#                                                 "role": {
#                                                     "attributes": {
#                                                         "name": "admin"
#                                                     }
#                                                 }
#                                             }
#                                         ]
#                                     }
#                                 }
#                             ]
#                         }
#                     },
#                     {
#                         "DnDomainMapEntry": {
#                             "attributes": {
#                                 "dn": "uni/tn-infra",
#                                 "readPrivileges": "admin",
#                                 "writePrivileges": "admin"
#                             }
#                         }
#                     },
#                     {
#                         "DnDomainMapEntry": {
#                             "attributes": {
#                                 "dn": "uni/tn-mgmt",
#                                 "readPrivileges": "admin",
#                                 "writePrivileges": "admin"
#                             }
#                         }
#                     },
#                     {
#                         "DnDomainMapEntry": {
#                             "attributes": {
#                                 "dn": "uni/tn-common",
#                                 "readPrivileges": "admin",
#                                 "writePrivileges": "admin"
#                             }
#                         }
#                     }
#                 ]
#             }
#         }
#     ],
#     "totalCount": "1"
# }
