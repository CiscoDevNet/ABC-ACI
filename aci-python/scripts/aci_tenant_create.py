# import login
# import argparse
# import logging
# import requests
# import hvac
# import json
# import os
# import log

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='ACI Create Tenant')
#     parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
#     parser.add_argument('--aci_host', default="https://10.10.20.14", help='the aci simulator')
#     parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
#     parser.add_argument('--tenant', required=True, help='the tenant to create')
#     args = parser.parse_args()

#     # Configure the logger
#     logger =  log.default('aci-tenant-create', level=args.log, patterns=[os.getenv("VAULT_TOKEN")], logfile=None)

#     # Get ACI credentials from our Vault server
#     client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
#     data = client.read("kv-v1/aci/bootcamp")
#     username = data["data"]["ACI_USERNAME"]
#     password = data["data"]["ACI_PASSWORD"]
    
#     # Create a session for our API requests
#     session  = requests.Session()
#     response = login.aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

#     # Create a new Tenant
#     tenant_response = session.post(f'{args.aci_host}/api/mo/uni.json', verify=False, json={
#         "fvTenant" : {
#             "attributes" : {
#             "name" : args.tenant
#             }
#         }
#     })

#     logger.debug("tenant create response code=%s", tenant_response.status_code)