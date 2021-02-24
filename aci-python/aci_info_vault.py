import requests
import logging
import hvac
import os
import argparse
from argparse import ArgumentParser
import json
import log 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
    parser.add_argument('--aci_host', default="https://10.10.20.14", help='the aci simulator')
    parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
    args = parser.parse_args()

    client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
    data = client.read("kv-v1/aci/bootcamp")
    username = data["data"]["ACI_USERNAME"]
    password = data["data"]["ACI_PASSWORD"]

#Issue an API Request to the ACI Simulator with missing credentials
    try:
        response = aaa_login(host=args.aci_host, username="", password="", verify=False)
        print ("Valid Credentials")
    

        # Create a session for our operational API requests
        session  = requests.Session()
        response = aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

        fv_tenant_response = session.get(f'{args.aci_host}/api/node/class/fvTenant.json?', verify=False)
        print("aci tenant response json=%s", json.dumps(fv_tenant_response.json(), indent=4))

        proc_response = session.get(f'{args.aci_host}/api/node/class/procEntity.json?', verify=False)
        print("aci cpu and memory response json=%s", json.dumps(proc_response.json(), indent=4))

        disk_utilization_response = session.get(f'{args.aci_host}/api/node/class/eqptStorage.json?', verify=False)
        print("aci disk utilization response json=%s", json.dumps(disk_utilization_response.json(), indent=4))

    except requests.exceptions.InvalidURL as e:
        print ("Missing Credentials")