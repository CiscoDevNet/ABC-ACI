import requests
import logging
import hvac
import os
import argparse
import json

logger = logging.getLogger('aci-login')
"""Returns a requests.Response resulting from an ACI Login request

Optional plotz says to frobnicate the bizbaz first.
"""
def aaa_login(host='apic', username='', password='', verify=True, timeout=10, session:requests.Session=None):
    if session == None:
        return requests.post(f'{host}/api/aaaLogin.json', verify=verify, timeout=timeout, json={
            "aaaUser" : {
                "attributes" : {
                    "name" : username,
                    "pwd" : password
                }
            }
        })
    else:
        return session.post(f'{host}/api/aaaLogin.json', verify=verify, timeout=timeout, json={
            "aaaUser" : {
                "attributes" : {
                    "name" : username,
                    "pwd" : password
                }
            }
        })

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

    # Issue an API Request to the ACI Simulator with missing credentials
    try:
        response = aaa_login(host=args.aci_host, username="", password="", verify=False)
        logger.debug("aci login status_code=%s", response.status_code)
    except requests.exceptions.InvalidURL as e:
        logger.error("aci login error=%s", e)

    # Issue an API Request to the ACI Simulator with the wrong host
    try:
        response = aaa_login(host="https://10.10.20.144", username="", password="", verify=False, timeout=2)
        logger.debug("aci login status_code=%s", response.status_code)
    except requests.exceptions.ConnectTimeout as e:
        logger.error("aci login error=%s", e)

    # Issue an API Request to the ACI Simulator with the wrong credentials
    response = aaa_login(host=args.aci_host, username="baduser", password="badpassword", verify=False)
    logger.debug("aci login status_code=%s", response.status_code)


    # Issue an API Request to the ACI Simulator with the correct credentials
    response = aaa_login(host=args.aci_host, username=username, password=password, verify=False)
    logger.debug("aci login status_code=%s", response.status_code)

    # Log the headers and body of the API response
    data = response.json()
    logger.debug("aci login headers json=%s", json.dumps(dict(response.headers), indent=4))
    logger.debug("aci login body json=%s",json.dumps(data, indent=4)) 

    # Alternaitvely, instead of extracting out the 
    session  = requests.Session()
    response = aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)
    logger.debug("aci login status_code=%s", response.status_code)

    # Logout
    logout_response = session.get(f'{args.aci_host}/api/aaaLogout.json')
    logger.debug("aci tenant logout status_code=%s", logout_response.status_code)



    # for item in fv_tenant_response.json()["imdata"]:
    #     logger.debug("aci tenant attributes json=%s", json.dumps(item["fvTenant"]["attributes"],indent=4))
    #     # uni/tn-common
    #     mo_tenant_response = session.get(f'{args.aci_host}/api/node/mo/{item["fvTenant"]["attributes"]["dn"]}.json', verify=False)
    #     logger.debug("aci managed object tenant detailed info json=%s", json.dumps(mo_tenant_response.json(), indent=4))


    # Get a list of fault counts for a specific tenant








    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format=formatter)
    # # logging.basicConfig(level=loggging.DEBUG)
    # logger = logging.getLogger("aci-login-example")
