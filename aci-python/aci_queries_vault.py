import requests
import logging
import hvac
import os
import argparse
from argparse import ArgumentParser
import json
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
    parser.add_argument('--tenant', required=True, help='the tenant to query for faults')
    args = parser.parse_args()

    client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
    data = client.read("kv-v1/aci/bootcamp")
    username = data["data"]["ACI_USERNAME"]
    password = data["data"]["ACI_PASSWORD"]

#Issue an API Request to the ACI Simulator with missing credentials
    try:
        response = aaa_login(host=args.aci_host, username="", password="", verify=False)
        print ("Valid Credentials")
    
         # Create a session for our API requests
        session  = requests.Session()
        response = aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

        """    

     You can filter the response to an API query by applying an expression of logical operators and values. 
     A basic equality or inequality test is expressed as follows:
     query-target-filter=[eq|ne](attribute,value)

     Available Logical Operators 
     =========================================
         eq              equal to
         ne              not equal to
         lt              less than
         gt              greater than
         le              less than or equal to
         ge              greater than or equal to
         bw              between
         not             logical inverse
         and             logical AND
         or              logical OR
         xor             logical exclusive OR
         true            Boolean
         false           Boolean
         anybit          true if at least one bit is set
         allbits         true if all bits are set
         wcard           wildcard
         pholder         property holder
         passive         passive holder
     =========================================
     """

        #  all tenant objects with a current health score of less than 50: 
        tenant_health_payload = {
            "rsp-subtree-include": "health,required",
            "rsp-subtree-filter": 'lt(healthInst.cur,"50")'
        }


        tenant_health_response = session.get(f'{args.aci_host}/api/class/fvTenant.json?', params=tenant_health_payload, verify=False)
        print("aci tenant health response json=%s", json.dumps(tenant_health_response.json(), indent=4))
        
        """    
        The REST API supports a wide range of flexible filters, useful for narrowing the scope of your search 
        to allow information to be located more quickly. The filters themselves are appended as query URI options,
        starting with a question mark (?) and concatenated with an ampersand (&). 
        Multiple conditions can be joined together to form complex filters. 

        Query Filters
        ====================================================================================================================================================================
            Filter Type                 Syntax                              Cobra Query Property                Description
            ------------------------------------------------------------------------------------------------------------------------------------------------------------
            query-target                {self | children | subtree}         AbstractQuery.queryTarget           Define the scope of a query
            target-subtree-class        class name                          AbstractQuery.classFilter           Respond-only elements including the specified class
            query-target-filter         filter expressions                  AbstractQuery.propFilter            Respond-only elements matching conditions
            rsp-subtree                 {no | children | full}              AbstractQuery.subtree               Specifies child object level included in the response
            rsp-subtree-class           class name                          AbstractQuery.subtreeClassFilter    Respond only specified classes
            rsp-subtree-filter          filter expressions                  AbstractQuery.subtreePropFilter     Respond only classes matching conditions
            rsp-subtree-include         {faults | health :stats :…}         AbstractQuery.subtreeInclude        Request additional objects
            order-by                    classname.property | {asc | desc}   Not Implemented                     Sort the response based on the property values
            ------------------------------------------------------------------------------------------------------------------------------------------------------------
        ====================================================================================================================================================================
        """ 
        tenant_epg_faults_payload = {
            'query-target': 'subtree',
            'target-subtree-class': 'fvAEPg',
            'rsp-subtree-include': 'fault-count'
        }

        tenant_epg_faults_response = session.get(f'{args.aci_host}/api/mo/uni/tn-{args.tenant}.json?', params=tenant_epg_faults_payload, verify=False)
        print("aci tenant epg faults response json=%s", json.dumps(tenant_epg_faults_response.json(), indent=4))\

        # query filtering
        user_query_response = session.get(f'{args.aci_host}/api/node/class/aaaUser.json?order-by=aaaUser.lastName|asc,aaaUser.firstName|asc', verify=False)
        print("aci user query response json=%s", json.dumps(user_query_response.json(), indent=4))

    except requests.exceptions.InvalidURL as e:
        print ("Missing Credentials")
