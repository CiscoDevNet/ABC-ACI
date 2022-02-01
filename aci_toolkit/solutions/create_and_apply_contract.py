'''Python ACI Toolkit Excercise - Creating and applying a new contract

SOLUTION FILE

This script, once completed, allows the user to create a contract and apply
it to a consumer and provider EPGs. For the credentials and URL a separate
credentials.py file is used.
'''
import acitoolkit.acitoolkit as ACI

def create_and_apply_contract():
    '''Creates and applies a contract'''
    description = 'ACI Toolkit Bootcamp app'
    creds = ACI.Credentials('apic', description)
    args = creds.get()
    session = ACI.Session(args.url, args.login, args.password)

    tenant = ACI.Tenant('Sales')
    app = ACI.AppProfile('eCommerce', tenant)
    web_epg = ACI.EPG('Web_EPG', app)
    app_epg = ACI.EPG('App_EPG', app)

    # Create the Contract to permit only HTTP and HTTPS
    contract = ACI.Contract('WebServices', tenant)
    http_entry = ACI.FilterEntry('TCP80',
                            applyToFrag='no',
                            arpOpc='unspecified',
                            dFromPort='80',
                            dToPort='80',
                            etherT='ip',
                            prot='tcp',
                            sFromPort='unspecified',
                            sToPort='unspecified',
                            tcpRules='unspecified',
                            parent=contract)
    https_entry = ACI.FilterEntry('TCP443',
                            applyToFrag='no',
                            arpOpc='unspecified',
                            dFromPort='443',
                            dToPort='443',
                            etherT='ip',
                            prot='tcp',
                            sFromPort='unspecified',
                            sToPort='unspecified',
                            tcpRules='unspecified',
                            parent=contract)

    # Provide and consume the Contract
    app_epg.provide(contract)
    web_epg.consume(contract)

    resp = session.push_to_apic(tenant.get_url(),
                                tenant.get_json())

    if not resp.ok:
        print("Error: Could not apply the contract")
    else:
        print(f"Contract {contract.name} applied succesfully")

if __name__ == "__main__":
    create_and_apply_contract()
