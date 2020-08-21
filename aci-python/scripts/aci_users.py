# import requests
# import logging
# import hvac
# import os
# import argparse
# import json
# import login
# import log



# """
# The APIC provides access according to a user’s role through role-based access control (RBAC). 
# An Cisco Application Centric Infrastructure (ACI) fabric user is associated with the following: 


# - A set of roles
# - For each role, a privilege type: no access, read-only, or read-write
# - One or more security domain tags that identify the portions of the management information tree (MIT) that a user can access


#  Creating a user and assigning a role to that user does not enable access rights. 
#  It is necessary to also assign the user to one or more security domains. By default, the ACI fabric includes two special pre-created domains: 

# - All—allows access to the entire MIT
# - Infra— allows access to fabric infrastructure objects/subtrees, such as fabric access policies

# """

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='ACI Users')
#     parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
#     parser.add_argument('--aci_host', default="https://10.10.20.14", help='the aci simulator')
#     parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
#     parser.add_argument('--new_user', required=True)
#     parser.add_argument('--new_user_password', required=True)
#     args = parser.parse_args()

#     # Configure the logger
#     logger =  log.default('aci-tenant-info', level=args.log, patterns=[os.getenv("VAULT_TOKEN")], logfile=None)

#     # Get ACI credentials from our Vault server
#     client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
#     data = client.read("kv-v1/aci/bootcamp")
#     username = data["data"]["ACI_USERNAME"]
#     password = data["data"]["ACI_PASSWORD"]
    
#     # Create a session for our API requests
#     session  = requests.Session()
#     response = login.aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

#     # Create a local admin user
#     payload = f"""
#         <aaaUser name="{args.new_user}" phone="" pwd="{args.new_user_password}" >
#             <aaaUserDomain childAction="" descr="" name="all" rn="userdomain-all" status="">
#                 <aaaUserRole childAction="" descr="" name="Ops" privType="writePriv"/>
#             </aaaUserDomain>
#       </aaaUser>"""

#     create_user_response = session.post(f'{args.aci_host}/api/policymgr/mo/uni/userext.xml', headers={"Content-Type": "text/xml"}, verify=False, data=payload)
#     logger.debug("aci create user response code=%s",create_user_response.status_code)