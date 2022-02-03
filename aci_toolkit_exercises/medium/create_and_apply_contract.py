'''Python ACI Toolkit Excercise - Creating and applying a new contract

SOLUTION FILE

This script, once completed, allows the user to create a contract and apply
it to a consumer and provider EPGs. For the credentials and URL a separate
credentials.py file is used.

- SPICE LEVEL: MEDIUM
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

    resp = <TODO>
    if not resp.ok:
        print('Could not login to APIC')


    tenant = ACI.<TODO>
    app = ACI.<TODO>
    web_epg = ACI.<TODO>
    app_epg = ACI.<TODO>

    # Create the contract and filters to permit only HTTP and HTTPS
    contract = ACI.<TODO>
    http_entry = ACI.FilterEntry(<TODO>)
    https_entry = ACI.FilterEntry(<TODO>)

    # Provide and consume the Contract
    app_epg.<TODO>
    web_epg.<TODO>

    # Push the changes to APIC
    resp = session.<TODO>

    if not resp.ok:
        print("Error: Could not apply the contract")
    else:
        print(f"Contract {contract.name} applied succesfully")

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    create_and_apply_contract()
