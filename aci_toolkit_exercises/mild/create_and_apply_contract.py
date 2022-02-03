'''Python ACI Toolkit Excercise - Creating and applying a new contract

SOLUTION FILE

This script, once completed, allows the user to create a contract and apply
it to a consumer and provider EPGs. For the credentials and URL a separate
credentials.py file is used.

- SPICE LEVEL: MILD
- TASK: Replace the <TODO> with correct code based on the lab guide
  instructions

'''
import acitoolkit.acitoolkit as ACI

def create_and_apply_contract():
    '''Creates and applies a contract'''
    description = 'ACI Toolkit Bootcamp app'
    creds = ACI.Credentials('apic', description)
    args = creds.get()
    session = ACI.Session(args.url, args.login, args.password)

    resp = session.<TODO>
    if not resp.ok:
        print('Could not login to APIC')


    tenant = ACI.<TODO>('Sales')
    app = ACI.<TODO>('eCommerce', tenant)
    web_epg = ACI.<TODO>('Web_EPG', app)
    app_epg = ACI.<TODO>('App_EPG', app)

    # Create the contract and filters to permit only HTTP and HTTPS
    contract = ACI.<TODO>(<TODO>, tenant)
    http_entry = ACI.FilterEntry('TCP80',
                            dFromPort=<TODO>,
                            dToPort=<TODO>,
                            etherT=<TODO>,
                            prot=<TODO>,
                            sFromPort='unspecified',
                            sToPort='unspecified',
                            parent=contract)
    https_entry = ACI.FilterEntry('TCP443',
                            dFromPort=<TODO>,
                            dToPort=<TODO>,
                            etherT=<TODO>,
                            prot=<TODO>,
                            sFromPort='unspecified',
                            sToPort='unspecified',
                            parent=contract)

    # Provide and consume the Contract
    app_epg.<TODO>(contract)
    web_epg.<TODO>(contract)

    # Push the changes to APIC
    resp = session.<TODO>(tenant.get_url(),
                                tenant.get_json())

    if not resp.ok:
        print("Error: Could not apply the contract")
    else:
        print(f"Contract {contract.name} applied succesfully")

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    create_and_apply_contract()
