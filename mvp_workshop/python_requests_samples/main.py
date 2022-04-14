'''Python Requests sample script - MAIN file to call on functions

When this script is run, the specified APIs are called.
'''

import get_request
import post_request
import authentication

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    INTRO = """
    This example application will list out all the current tenants in the
    APIC and create a new tenant with the name specified by the user.
    The target of this example application is to provide an example on how
    Python Requests library can be used to communicate with ACI APIs.
    """

    print(INTRO)
    username = input("Your APIC username: ")
    password = input("Your APIC password: ")
    apic = input("Your APIC address [with http(s)]: ")

    print("\nRetrieving the token cookie...")
    token_cookie = authentication.get_token(apic, username, password)

    print("\nCurrent tenants: ")
    tenants = get_request.get_class("fvTenant", apic, token_cookie)
    for tenant in tenants:
        print(tenant["fvTenant"]["attributes"]["name"])

    new_tenant_name = input("\nName of your new tenant: ")

    print(f"\nCreating a new tenant {new_tenant_name}")
    payload = {"fvTenant":{"attributes":{"name":new_tenant_name}}}
    post_request.post_mo("uni", payload, apic, token_cookie)

    print("\nTenants after the change: ")
    tenants = get_request.get_class("fvTenant", apic, token_cookie)
    for tenant in tenants:
        print(tenant["fvTenant"]["attributes"]["name"])
