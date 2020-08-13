import requests
import logging
import hvac
import os
import argparse
import json
import login

logger = logging.getLogger('aci-tenant-info')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ACI Login')
    parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
    parser.add_argument('--aci_host', default="https://10.10.20.14", help='the vault server')
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

    logger.debug(args.aci_host)

    # Alternaitvely, instead of extracting out the 
    session  = requests.Session()

    response = login.aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

    # Using the fvTenant class to get a list of all Tenants

    fv_tenant_response = session.get(f'{args.aci_host}/api/node/class/fvTenant.json?', verify=False)
    logger.debug("aci tenant response json=%s", json.dumps(fv_tenant_response.json(), indent=4))

