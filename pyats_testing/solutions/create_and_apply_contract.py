'''Python pyATS Excercise - Creating and applying a contract

SOLUTION FILE

This script, once completed, allows the user to create a new filter and contract,
and apply it to EPGs. This is done using pyATS library. The device information
is defined in the testbed yaml file, which is loaded before the functions are
called.
'''

# import the topology module
import json
from pyats import topology

def create_filter(apic, tenant):
    '''Creates a new filter'''

    url = f'api/mo/uni/tn-{tenant}.json'
    with open("json_payload/create_filter_payload.json", "r", encoding="utf-8") as json_file:
        payload=json_file.read()
    output = apic.rest.post(url, payload)
    print(output)

def create_contract(apic, tenant, filter_name):
    '''creates a new contract'''

    url = f'api/mo/uni/tn-{tenant}.json'
    with open("json_payload/create_contract_payload.json", "r", encoding="utf-8") as json_file:
        payload=json.loads(json_file.read())
        payload["vzBrCP"]["children"][0]["vzSubj"]["children"][0]["vzRsSubjFiltAtt"]["attributes"]["tnVzFilterName"] = filter_name
    output = apic.rest.post(url, json.dumps(payload))
    print(output)

def apply_provided_contract(apic, tenant, ap, epg, contract):
    '''Applies a contract to the provided EPG'''

    url = f'api/mo/uni/tn-{tenant}/ap-{ap}/epg-{epg}.json'
    with open("json_payload/apply_provided_contract_payload.json", "r", encoding="utf-8") as json_file:
        payload=json.loads(json_file.read())
        payload["fvRsProv"]["attributes"]["tnVzBrCPName"] = contract
    output = apic.rest.post(url, json.dumps(payload))
    print(output)

def apply_consumed_contract(apic, tenant, ap, epg, contract):
    '''Applies a contract to the consumer EPG'''

    url = f'api/mo/uni/tn-{tenant}/ap-{ap}/epg-{epg}.json'
    with open("json_payload/apply_consumed_contract_payload.json", "r", encoding="utf-8") as json_file:
        payload=json.loads(json_file.read())
        payload["fvRsCons"]["attributes"]["tnVzBrCPName"] = contract
    output = apic.rest.post(url, json.dumps(payload))
    print(output)

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    TESTBED_FILE = "aci_testbed.yaml"
    TENANT = "Sales"
    AP = "eCommerce"
    EPG1 = "App_EPG"
    EPG2 = "Web_EPG"
    CONTRACT = "BasicServices_Ct"
    FILTER = "Basic_Fltr"

    # load the above testbed file containing REST device
    testbed = topology.loader.load(TESTBED_FILE)
    # get apic from the testbed
    my_apic = testbed.devices['APIC']
    # connect to the APIC
    my_apic.connect()

    # Send API calls
    create_filter(my_apic, TENANT)
    create_contract(my_apic, TENANT, FILTER)
    apply_provided_contract(my_apic, TENANT, AP, EPG1, CONTRACT)
    apply_consumed_contract(my_apic, TENANT, AP, EPG2, CONTRACT)

    #Disconnect
    my_apic.disconnect()
