'''Python pyATS Excercise - Creating and applying a contract

SOLUTION FILE

This script, once completed, allows the user to create a new filter and contract,
and apply it to EPGs. This is done using pyATS library. The device information
is defined in the testbed yaml file, which is loaded before the functions are
called.
'''

# import the topology module
from pyats import topology

def create_filter(apic, tenant):
    '''Creates a new filter'''

    url = f"api/mo/uni/tn-{tenant}.json"
    payload_file = "json_payload/create_filter_payload.json"
    with open(payload_file, "r", encoding="utf-8") as json_file:
        payload=json_file.read()
    output = apic.rest.post(url, payload)

def create_contract(apic, tenant):
    '''creates a new contract'''

    url = f"api/mo/uni/tn-{tenant}.json"
    payload_file = "json_payload/create_contract_payload.json"
    with open(payload_file, "r", encoding="utf-8") as json_file:
        payload=json_file.read()
    output = apic.rest.post(url, payload)

def apply_provided_contract(apic, tenant, ap, epg):
    '''Applies a contract to the provided EPG'''

    url = f"api/mo/uni/tn-{tenant}/ap-{ap}/epg-{epg}.json"
    payload_file = "json_payload/apply_provided_contract_payload.json"
    with open(payload_file, "r", encoding="utf-8") as json_file:
        payload=json_file.read()
    output = apic.rest.post(url, payload)

def apply_consumed_contract(apic, tenant, ap, epg):
    '''Applies a contract to the consumer EPG'''

    url = f"api/mo/uni/tn-{tenant}/ap-{ap}/epg-{epg}.json"
    payload_file = "json_payload/apply_consumed_contract_payload.json"
    with open(payload_file, "r", encoding="utf-8") as json_file:
        payload=json_file.read()
    output = apic.rest.post(url, payload)

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    TESTBED_FILE = "aci_testbed.yaml"
    TENANT = "Sales"
    AP = "eCommerce"
    EPG1 = "App_EPG"
    EPG2 = "Web_EPG"

    # load the above testbed file containing REST device
    testbed = topology.loader.load(TESTBED_FILE)
    # get apic from the testbed
    my_apic = testbed.devices['APIC']
    # connect to the APIC
    my_apic.connect()

    # Send API calls
    create_filter(my_apic, TENANT)
    create_contract(my_apic, TENANT)
    apply_provided_contract(my_apic, TENANT, AP, EPG1)
    apply_consumed_contract(my_apic, TENANT, AP, EPG2)

    #Disconnect
    my_apic.disconnect()
