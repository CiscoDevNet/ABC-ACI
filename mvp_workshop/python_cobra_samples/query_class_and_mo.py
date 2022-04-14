'''Python Cobra SDK sample script - querying information

This script allows the user to query the selected ACI class or
MO and returns the response as Python Dictionary.
'''

# Import required libraries
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
import urllib3

# Disable unverified HTTPS request warnings
urllib3.disable_warnings()

def get_class(classname, apic, username, password):
    '''GET the objects belonging to the specified ACI class'''

    # Login into a session with APIC
    session = LoginSession(apic, username, password)
    mo_dir = MoDirectory(session)
    mo_dir.login()

    # Query for tenants using class
    response = mo_dir.lookupByClass(classname)
    # Logout
    mo_dir.logout()

    return response

def get_mo(mo_dn, apic, username, password):
    '''GET a specified ACI Managed Object (MO)'''

    # Login into a session with APIC
    session = LoginSession(apic, username, password)
    mo_dir = MoDirectory(session)
    mo_dir.login()

    # Query for specific tenant using DN
    response = mo_dir.lookupByDn(mo_dn)
    # Logout
    mo_dir.logout()

    return response
