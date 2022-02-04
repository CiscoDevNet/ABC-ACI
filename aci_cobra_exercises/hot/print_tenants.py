'''Python Cobra SDK Exercise - Printing out tenant information

This script, once completed, allows the user to print out tenant names.
In the script you get to include both querying a class and an MO with
DN.

- SPICE LEVEL: HOT
- TASK: Replace the # <TODO> comments with correct code based on the lab guide
  instructions

'''

# Import required libraries
# <TODO>

# Disable unverified HTTPS request warnings
# <TODO>

def print_tenants(url, username, password):
    '''Prints out the tenant names'''

    # Login into a session with APIC
    # <TODO>: create a LoginSession
    # <TODO>: create a MoDirectory
    # <TODO>: login

    # Query for tenants using class
    # <TODO>

    print("\nPrinting information from the class request")
    # <TODO>

    # Query for specific tenant using DN
    # <TODO>

    print("\nPrinting information from the MO request")
    # <TODO>

    # <TODO> logout

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":

    # URL and credentials information:
    # <TODO>: URL
    # <TODO>: USERNAME
    # <TODO>: PASSWORD

    print_tenants(URL, USERNAME,PASSWORD)
