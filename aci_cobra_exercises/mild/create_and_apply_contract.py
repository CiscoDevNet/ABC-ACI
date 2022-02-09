'''Python Cobra SDK Exercise - Creating and applying a contract

This script, once completed, allows the user to create a new filter,
subject, and contract, and apply it to a consumer and provider EPG.

- SPICE LEVEL: MILD
- TASK: Replace the <TODO> with correct code based on the lab guide
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
    ftp_filter = vz.<TODO>(tenant, name='FTP_Fltr')
    filter_entry = vz.<TODO>(ftp_filter, name='TCP21', dFromPort='21',
                            dToPort=<TODO>, etherT=<TODO>, prot=<TODO>)
    return ftp_filter
"""

def create_contract(tenant, vzfilter):
    '''Creates filter, contract, and subject and applies to two EPGs'''
"""
    contract = vz.<TODO>(tenant, name=<TODO>)
    subject = vz.<TODO>(contract, name=<TODO>)
    subject_filter = vz.<TODO>(subject, action='permit', tnVzFilterName=vzfilter.<TODO>)

    return contract
"""

def apply_contract(contract, epg_provider, epg_consumer):
    '''Creates filter, contract, and subject and applies to two EPGs'''
"""
    fv.<TODO>(epg_provider, tnVzBrCPName=<TODO>) #provider
    fv.<TODO>(epg_consumer, tnVzBrCPName=<TODO>) #consumer
"""

def commit_changes_to_apic(url, username, password, pol_uni):
    '''Take in the changes of Policy Universe (pol_uni) and send to APIC'''
"""
    # log into an APIC and create a directory object
    session = cobra.mit.session.<TODO>(url, username, password)
    mo_dir = cobra.mit.access.<TODO>(session)
    mo_dir.<TODO>() #add the method to login

    # Print the preview of polUni JSON that will be sent to APIC
    print(f'JSON to be sent:\n {<TODO>(pol_uni)}\n')

    # commit the pol_uni changes to APIC
    c = cobra.mit.request.<TODO>() # Create a ConfigRequest
    c.<TODO>(pol_uni)
    response = mo_dir.<TODO>(c) # Commit the changes to APIC

    # Print the status code for information purpose
    print(f'<Status code {response.<TODO>}>')

    # Logout from the session
    mo_dir.logout()
"""
# The following if statement is True when this file is executed directly.
if __name__ == "__main__":

    # URL and credentials information:
    URL = "https://<TODO>"
    USERNAME = "<TODO>"
    PASSWORD = "<TODO>"

    # the top level object on which operations will be made
    POL_UNI = pol.Uni('')
    TENANT = fv.Tenant(<TODO>, 'Sales')
    APP_PROFILE = fv.Ap(TENANT, <TODO>)
    EPG_PROVIDER = fv.AEPg(<TODO>, <TODO>)
    EPG_CONSUMER = fv.AEPg(<TODO>, <TODO>)
    
    # Call the functions to make changes and send the result to APIC
    # ftp_filter = create_filter(TENANT)
    # contract = create_contract(TENANT, ftp_filter)
    # apply_contract(contract, EPG_PROVIDER, EPG_CONSUMER)
    # commit_changes_to_apic(URL, USERNAME,PASSWORD, POL_UNI)
