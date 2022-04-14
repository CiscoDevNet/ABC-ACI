'''Python Cobra SDK sample script - Creating and modifying Tenants

This script allows the user to make a POST request against a specified
ACI Tenant MO to either edit and existing MO or to create a new MO.
'''

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session

from cobra.model import fv, pol

from cobra.internal.codec.jsoncodec import toJSONStr

import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def create_tenant(tenant_name, vrf_name, bd_name, bd_subnet):
    '''Creates tenant with vrf, bridge domain and a subnet'''
    POL_UNI = pol.Uni('')

    tenant = fv.Tenant(POL_UNI, name=tenant_name)
    bridge_domain = fv.BD(tenant, name=bd_name)
    subnet = fv.Subnet(bridge_domain, ip=bd_subnet)
    vrf = fv.Ctx(tenant, name=vrf_name)
    fv.RsCtx(bridge_domain, tnFvCtxName=vrf.name)

    return POL_UNI

def commit_changes_to_apic(apic, username, password, pol_uni):
    '''Take in the changes of Policy Universe (pol_uni) and send to APIC'''

    # log into an APIC and create a directory object
    session = cobra.mit.session.LoginSession(apic, username, password)
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
