'''Python Cobra SDK Exercise - Printing out tenant information

SOLUTION FILE

This script, once completed, allows the user to print out tenant names.
In the script you get to include both querying a class and an MO with
DN.
'''

# Import required libraries
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def print_tenants(url, username, password):
    '''Prints out the tenant names'''

    # Login into a session with APIC
    session = LoginSession(url, username, password)
    mo_dir = MoDirectory(session)
    mo_dir.login()

    # Query for tenants using class
    tenants_class = mo_dir.lookupByClass("fvTenant")

    print("\nPrinting information from the class request")
    # print(tenants_class)
    for tenant in tenants_class:
        # print(tenant)
        # print(dir(tenant))
        print(tenant.name)

    # Query for specific tenant using DN
    tenant_dn = mo_dir.lookupByDn("uni/tn-Sales")

    print("\nPrinting information from the MO request")
    # print(tenant_dn)
    print(tenant_dn.name)

    # Logout
    mo_dir.logout()

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    
    # URL and credentials information:
    URL = "https://apic"
    USERNAME = "developer"
    PASSWORD = "1234QWer"

    print_tenants(URL, USERNAME,PASSWORD)
