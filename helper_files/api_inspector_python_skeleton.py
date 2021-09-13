'''
Skeleton to help you create Python script with
REST API calls towards Cisco APIC.
'''

# DEFINE YOUR IMPORT STATEMENTS HERE
import requests
import urllib3
urllib3.disable_warnings()

# DEFINE YOUR GLOBAL VARIABLES HERE
APIC_USER = "admin"
APIC_PW = "C1sco12345"
APIC_IP = "10.10.20.14"

# DEFINE YOUR FUNCTIONS HERE
def get_token():
    '''
    This is a function to authenticate with the
    Sandbox APIC.
    '''

    url = f"https://{APIC_IP}/api/aaaLogin.json"

    payload = {
        "aaaUser" : {
            "attributes" : {
                "name" :APIC_USER,
                "pwd" :APIC_PW
                }
            }
        }

    response = requests.request("POST", url, json = payload, verify=False)

    return response.cookies

def configure_tenant(my_cookies, tenant_name, vrf_name):
    '''
    Function to create a new tenant with a vrf.
    '''
    pass

def configure_bridge_domain(my_cookies, tenant, bd_name, subnet, vrf):
    '''
    Function to create a new bridgedomain under a tenant.
    '''
    pass

def configure_filter(my_cookies, tenant, filter_name):
    '''
    Function to create a new filter under a tenant.
    '''
    pass

def configure_contract(my_cookies, tenant, contract_name, subject_name, filter_name):
    '''
    Function to create a new contract under a tenant.
    '''
    pass

def configure_ap(my_cookies, tenant, ap_name, epg_name, bd_name, contract_name):
    '''
    Function to create a new application profile under a tenant.
    '''
    pass

# DEFINE YOUR MAIN FUNCTION HERE

def main():
    '''
    Main function. Call the other functions from here.
    '''
    cookies = get_token()
    print(cookies)

# RUN YOUR MAIN SCRIPT
if __name__ == "__main__":
    main()
