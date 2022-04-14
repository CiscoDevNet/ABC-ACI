'''Python Cobra SDK sample script - MAIN file to call on functions

When this script is run, the specified APIs are called.
'''

import query_class_and_mo
import modify_tenant

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    INTRO = """
    This example application will list out all the current tenants in the
    APIC and create a new tenant with the name specified by the user.
    The tenant will have one VRF, one Bridge Domain and one subnet.
    The target of this example application is to provide an example on how
    Cobra SDK can be used to communicate with ACI APIs.
    """

    print(INTRO)
    username = input("Your APIC username: ")
    password = input("Your APIC password: ")
    apic = input("Your APIC address [with http(s)]: ")

    print("\nCurrent tenants: ")
    tenants = query_class_and_mo.get_class("fvTenant", apic, username, password)
    for tenant in tenants:
        print(tenant.name)

    new_tenant = input("\nName of your new tenant: ")

    print(f"\nCreating a new tenant {new_tenant}")
    pol_uni = modify_tenant.create_tenant(new_tenant,
                                        f"{new_tenant}_VRF",
                                        f"{new_tenant}_BD",
                                        "10.10.10.1/24")
    modify_tenant.commit_changes_to_apic(apic, username, password, pol_uni)

    print("\nTenants after the change: ")
    tenants = query_class_and_mo.get_class("fvTenant", apic, username, password)
    for tenant in tenants:
        print(tenant.name)
