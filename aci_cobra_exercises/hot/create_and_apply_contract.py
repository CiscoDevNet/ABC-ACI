'''Python Cobra SDK Exercise - Creating and applying a contract

This script, once completed, allows the user to create a new filter,
subject, and contract, and apply it to a consumer and provider EPG.

- SPICE LEVEL: HOT
- TASK: Replace the # <TODO> comments with correct code based on the lab guide
  instructions

'''


# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
from cobra.model import <TODO>, <TODO>, <TODO>
from cobra.internal.codec.jsoncodec import toJSONStr

import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def create_filter(tenant):
    '''Creates filter, contract, and subject and applies to two EPGs'''
"""
    <TODO>: Create and return an ftp_filter with one entry

    return ftp_filter
"""

def create_contract(tenant, vzfilter):
    '''Creates filter, contract, and subject and applies to two EPGs'''
"""
    <TODO>: Create and return contract with one subject linked to the vzfilter

    return contract
"""

def apply_contract(contract, epg_provider, epg_consumer):
    '''Creates filter, contract, and subject and applies to two EPGs'''
"""
    <TODO>: apply the provided and consumed contract
"""

def commit_changes_to_apic(url, username, password, pol_uni):
    '''Take in the changes of Policy Universe (pol_uni) and send to APIC'''
"""
    # log into an APIC and create a directory object
    session = # <TODO>: LoginSession object
    mo_dir = # <TODO>: MoDirectory object
    # <TODO>: Login to the session

    # Print the preview of polUni JSON that will be sent to APIC
    # <TODO>

    # commit the pol_uni changes to APIC
    c = # <TODO>: ConfigRequest object
    # <TODO>: Add managed object to ConfigRequest
    response = # <TODO> Commit the changes to APIC

    # Print the status code for information purpose
    # <TODO>

    # Logout from the session
    mo_dir.logout()
"""
# The following if statement is True when this file is executed directly.
if __name__ == "__main__":

    # URL and credentials information:
    # <TODO>: URL, USERNAME, and PASSWORD

    # the top level object on which operations will be made
    POL_UNI = pol.Uni('')
    TENANT = # <TODO>
    APP_PROFILE = # <TODO>
    EPG_PROVIDER = # <TODO>
    EPG_CONSUMER = # <TODO>
    
    # Call the functions to make changes and send the result to APIC
    # ftp_filter = create_filter(TENANT)
    # contract = create_contract(TENANT, ftp_filter)
    # apply_contract(contract, EPG_PROVIDER, EPG_CONSUMER)
    # commit_changes_to_apic(URL, USERNAME,PASSWORD, POL_UNI)
