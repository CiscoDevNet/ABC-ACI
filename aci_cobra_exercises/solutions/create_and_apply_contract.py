'''Python Cobra SDK Exercise - Creating and applying a contract

SOLUTION FILE

This script, once completed, allows the user to create a new filter,
subject, and contract, and apply it to a consumer and provider EPG.
'''


# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
from cobra.model import fv, pol, vz
from cobra.internal.codec.jsoncodec import toJSONStr

import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def create_filter(tenant):
    '''Creates filter, contract, and subject and applies to two EPGs'''

    ftp_filter = vz.Filter(tenant, name='FTP_Fltr')
    filter_entry = vz.Entry(ftp_filter, name='TCP21', dFromPort='21',
                            dToPort='21', etherT='ip', prot='tcp')
    return ftp_filter

def create_contract(tenant, vzfilter):
    '''Creates filter, contract, and subject and applies to two EPGs'''

    contract = vz.BrCP(tenant, name='FileServices_Ct')
    subject = vz.Subj(contract, name='FileServices_Subj')
    subject_filter = vz.RsSubjFiltAtt(subject, action='permit', tnVzFilterName=vzfilter.name)

    return contract

def apply_contract(contract, epg_provider, epg_consumer):
    '''Creates filter, contract, and subject and applies to two EPGs'''

    fv.RsProv(epg_provider, tnVzBrCPName=contract.name) #provider
    fv.RsCons(epg_consumer, tnVzBrCPName=contract.name) #consumer

def commit_changes_to_apic(url, username, password, pol_uni):
    '''Take in the changes of Policy Universe (pol_uni) and send to APIC'''

    # log into an APIC and create a directory object
    session = cobra.mit.session.LoginSession(url, username, password)
    mo_dir = cobra.mit.access.MoDirectory(session)
    mo_dir.login()

    # Print the preview of polUni JSON that will be sent to APIC
    print(f'JSON to be sent:\n {toJSONStr(pol_uni)}\n')

    # commit the pol_uni changes to APIC
    c = cobra.mit.request.ConfigRequest()
    c.addMo(pol_uni)
    response = mo_dir.commit(c)

    # Print the status code for information purpose
    print(f'<Status code {response.status_code}>')

    # Logout from the session
    mo_dir.logout()

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":

    # URL and credentials information:
    URL = "https://apic"
    USERNAME = "developer"
    PASSWORD = "1234QWer"

    # the top level object on which operations will be made
    POL_UNI = pol.Uni('')
    TENANT = fv.Tenant(POL_UNI, 'Sales')
    APP_PROFILE = fv.Ap(TENANT, 'eCommerce')
    EPG_PROVIDER = fv.AEPg(APP_PROFILE, 'DB_EPG')
    EPG_CONSUMER = fv.AEPg(APP_PROFILE, 'App_EPG')

    print(toJSONStr(POL_UNI))
    
    # Call the functions to make changes and send the result to APIC
    ftp_filter = create_filter(TENANT)
    contract = create_contract(TENANT, ftp_filter)
    apply_contract(contract, EPG_PROVIDER, EPG_CONSUMER)
    commit_changes_to_apic(URL, USERNAME,PASSWORD, POL_UNI)
