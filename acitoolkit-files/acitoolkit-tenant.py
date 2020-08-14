#! /usr/bin/env python
"""
The goal here is to define a minimum viable product while still remaining true
to form with how an actual ACI tenant is defined within the fabric.

Everything will be built from the name of the tenant (BD, CTX, etc) and 
will assume that a two-tier app is created (web, db).

We'll need to feed inputs into the command line for IP and credentials.
Also, there are additional switches for tenant delete and print JSON
"""

import acitoolkit.acitoolkit as ACI
import json

def main():

    # We're going to prompt the user for a desired tenant name to build from
    # and then return the name to ensure that its correct
    tenant = ACI.Tenant(input("Enter desired tenant name: "))
    print("Tenant name is: " + tenant.name)

    # Application profile name is built from the tenant name
    # and printed to validate
    ap = ACI.AppProfile(tenant.name + "-AP", tenant)
    print("AppProfile name is: " + ap.name)

    # Two EGPs are created and tied to the previously created AP
    web_epg = ACI.EPG('web', ap)
    db_epg = ACI.EPG('db', ap)

    # A VRF is built from the tenant name and printed
    vrf = ACI.Context(tenant.name + "-CTX", tenant)
    print("VRF name is: " + vrf.name)

    # Build a bridge domain from tenant name, print
    tenant_bd = ACI.BridgeDomain(tenant.name + "-BD", tenant)
    print("BD name is: " + tenant_bd.name)

    # Finally, build the subnet from tenant name, print
    tenant_bd_subnet = ACI.Subnet(tenant.name + "-Subnet", tenant_bd)
    print("Subnet name is: " + tenant_bd_subnet.name)

    # For sake of exercise, we'll just statically assign the subnet for
    # the BD
    tenant_bd_subnet.addr = "10.1.1.1/24"

    # The BD is attached to the VRF, and options are set for flooding
    tenant_bd.add_context(vrf)
    tenant_bd.set_arp_flood('no')
    tenant_bd.set_unicast_route('yes')

    # Each of the EPGs is added to the previously created BD
    web_epg.add_bd(tenant_bd)
    db_epg.add_bd(tenant_bd)

    # The first contract, defining SQL and tied to our tenant.
    # The entry is tied to the contract and includes port and other info
    sql_contract = ACI.Contract('mssql-contract', tenant)
    sql_entry_1 = ACI.FilterEntry('ms-sql',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='1433',
                         dToPort='1433',
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=sql_contract)

    # The second contract will be for web services.  Include 80 and 443
    web_contract = ACI.Contract('web-contract', tenant)
    web_entry_1 = ACI.FilterEntry('http',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='80',
                         dToPort='80',
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=web_contract)
    web_entry_2 = ACI.FilterEntry('https',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='443',
                         dToPort='443',
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=web_contract)

    # The contracts are attached to the EPGs are providers, consumers
    db_epg.provide(sql_contract)
    web_epg.consume(sql_contract)
    web_epg.provide(web_contract)

    # Physical interfaces for attachment
    intf1 = ACI.Interface('eth', '1', '101', '1', '1')
    intf2 = ACI.Interface('eth', '1', '102', '1', '1')

    # Create a single VLAN for these interfaces.  Remember, EPGs do the allow-list
    vl10_intf1_web = ACI.L2Interface('vl10_intf1_web', 'vlan', '10')
    vl10_intf2_db = ACI.L2Interface('vl10_intf2_db', 'vlan', '10')

    # Attach the logical to physical interface config
    vl10_intf1_web.attach(intf1)
    vl10_intf2_db.attach(intf2)

    # Finally attach the EPGs to the layer-2 interface configs
    web_epg.attach(vl10_intf1_web)
    db_epg.attach(vl10_intf2_db) 

    # Now the actual "configuration push" is setup
    description = 'ACIToolkit mock full tenant configuration script'
    creds = ACI.Credentials('apic', description)
    # Adding in pieces for JSON only or delete the tenant
    creds.add_argument('--delete', action='store_true',
                    help='Delete the configuration from the APIC')
    creds.add_argument('--json', const='false', nargs='?', help='JSON output only')
    args = creds.get()
    session = ACI.Session(args.url, args.login, args.password)
    session.login()

    # Several if/else to delete the tenant or print the JSON payload
    if args.delete:
        tenant.mark_as_deleted()

    if args.json:
        print("The following JSON payload was created")
        print("URL: ", tenant.get_url())
        print(json.dumps(tenant.get_json(), indent=2))

    else:
        resp = session.push_to_apic(tenant.get_url(),tenant.get_json())

        # Some error handling along the way
        if not resp.ok:
            print("%% Error: Could not push configuration to APIC")
            print(resp.text)

        else:
            print("Success")

# Run it!
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass