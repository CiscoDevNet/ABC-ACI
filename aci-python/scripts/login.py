# import requests
# import logging
# import hvac
# import os
# import argparse
# import json
# import log 

# def aaa_login(host='apic', username='', password='', verify=True, timeout=10, session:requests.Session=None):
#     if session == None:
#         return requests.post(f'{host}/api/aaaLogin.json', verify=verify, timeout=timeout, json={
#             "aaaUser" : {
#                 "attributes" : {
#                     "name" : username,
#                     "pwd" : password
#                 }
#             }
#         })
#     else:
#         return session.post(f'{host}/api/aaaLogin.json', verify=verify, timeout=timeout, json={
#             "aaaUser" : {
#                 "attributes" : {
#                     "name" : username,
#                     "pwd" : password
#                 }
#             }
#         })

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='ACI Login')
#     parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
#     parser.add_argument('--aci_host', default="https://10.10.20.14", help='the aci simulator')
#     parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
#     args = parser.parse_args()

#     logger = log.default("aci-login", level=args.log, patterns=[os.getenv("VAULT_TOKEN")])
#     client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
#     data = client.read("kv-v1/aci/bootcamp")
#     username = data["data"]["ACI_USERNAME"]
#     password = data["data"]["ACI_PASSWORD"]

#     # Issue an API Request to the ACI Simulator with missing credentials
#     try:
#         response = aaa_login(host=args.aci_host, username="", password="", verify=False)
#         logger.debug("aci login status_code=%s", response.status_code)
#     except requests.exceptions.InvalidURL as e:
#         logger.error("aci login error=%s", e)

#     # Issue an API Request to the ACI Simulator with the wrong host
#     try:
#         response = aaa_login(host="https://10.10.20.144", username="", password="", verify=False, timeout=2)
#         logger.debug("aci login status_code=%s", response.status_code)
#     except requests.exceptions.ConnectTimeout as e:
#         logger.error("aci login error=%s", e)

#     # Issue an API Request to the ACI Simulator with the wrong credentials
#     response = aaa_login(host=args.aci_host, username="baduser", password="badpassword", verify=False)
#     logger.debug("aci login status_code=%s", response.status_code)


#     # Issue an API Request to the ACI Simulator with the correct credentials
#     response = aaa_login(host=args.aci_host, username=username, password=password, verify=False)
#     logger.debug("aci login status_code=%s", response.status_code)

#     # Log the headers and body of the API response
#     data = response.json()
#     logger.debug("aci login headers json=%s", json.dumps(dict(response.headers), indent=4))
#     logger.debug("aci login body json=%s",json.dumps(data, indent=4)) 

#     # Alternaitvely, instead of extracting out the 
#     session  = requests.Session()
#     response = aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)
#     logger.debug("aci login status_code=%s", response.status_code)

#     # Logout
#     logout_response = session.get(f'{args.aci_host}/api/aaaLogout.json')
#     logger.debug("aci tenant logout status_code=%s", logout_response.status_code)

