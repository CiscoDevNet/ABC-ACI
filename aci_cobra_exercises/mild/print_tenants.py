'''Python Cobra SDK Exercise - Printing out tenant information

This script, once completed, allows the user to print out tenant names.
In the script you get to include both querying a class and an MO with
DN.

- SPICE LEVEL: MILD
- TASK: Replace the <TODO> with correct code based on the lab guide
  instructions

'''

# Import required libraries
from cobra.mit.access import <TODO>
from cobra.mit.session import <TODO>
#import <TODO>

# Disable unverified HTTPS request warnings
# <TODO>

def print_tenants(url, username, password):
    '''Prints out the tenant names'''

    # Login into a session with APIC
    session = <TODO>(url, username, password)
    mo_dir = <TODO>(session)
    mo_dir.<TODO>

    # Query for tenants using class
    tenants_class = mo_dir.lookupByClass(<TODO>)

    print("\nPrinting information from the class request")
    print(<TODO>)
    # for tenant in tenants_class:
        #<todo>

    # Query for specific tenant using DN
    # tenant_dn = mo_dir.<TODO>("uni/tn-Sales")

    print("\nPrinting information from the MO request")
    # print(tenant_dn)

    # Logout
    mo_dir.<TODO>()

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":

    # URL and credentials information:
    URL = "https://<TODO>"
    USERNAME = "<TODO>"
    PASSWORD = "<TODO>"

    print_tenants(URL, USERNAME,PASSWORD)
