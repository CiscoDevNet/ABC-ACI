# import requests
# import logging
# import hvac
# import os
# import argparse
# import json
# import login
# import log

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='ACI Info')
#     parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
#     parser.add_argument('--aci_host', default="https://10.10.20.14", help='the aci simulator')
#     parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
#     args = parser.parse_args()

#     # Configure the logger
#     logger =  log.default('aci-info', level=args.log, patterns=[os.getenv("VAULT_TOKEN")], logfile=None)

#     # Get ACI credentials from our Vault server
#     client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
#     data = client.read("kv-v1/aci/bootcamp")
#     username = data["data"]["ACI_USERNAME"]
#     password = data["data"]["ACI_PASSWORD"]

#     # Create a session for our API requests
#     session  = requests.Session()
#     response = login.aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

#     fv_tenant_response = session.get(f'{args.aci_host}/api/node/class/fvTenant.json?', verify=False)
#     logger.debug("aci tenant response json=%s", json.dumps(fv_tenant_response.json(), indent=4))

#     proc_response = session.get(f'{args.aci_host}/api/node/class/procEntity.json?', verify=False)
#     logger.debug("aci cpu and memory response json=%s", json.dumps(proc_response.json(), indent=4))

#     disk_utilization_response = session.get(f'{args.aci_host}/api/node/class/eqptStorage.json?', verify=False)
#     logger.debug("aci disk utilization response json=%s", json.dumps(disk_utilization_response.json(), indent=4))
    

