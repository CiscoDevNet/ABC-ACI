'''Python ACI Toolkit Excercise - Creating and applying a new contract

SOLUTION FILE

This script, once completed, allows the user to create a contract and apply
it to a consumer and provider EPGs. For the credentials and URL a separate
credentials.py file is used.

- SPICE LEVEL: HOT
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

    # <TODO> Define the tenant, app, and two epgs

    # <TODO> Create the contract and filters to permit only HTTP and HTTPS

    # <TODO> Apply the contract to the provider and consumer EPGs

    # Push the changes to APIC
    resp = <TODO>

    if not resp.ok:
        print("Error: Could not apply the contract")
    else:
        print(f"Contract {contract.name} applied succesfully")

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    create_and_apply_contract()
