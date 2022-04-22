import acitoolkit.acitoolkit as aci
from tabulate import tabulate


def main():
    """
    Main Show Endpoints Routine
    :return: None
    """
    username = input("Your APIC username: ")
    password = input("Your APIC password: ")
    apic = input("Your APIC address [with http(s)]: ")

    # Login to APIC
    session = aci.Session(apic, username, password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        return

    # Download all of the interfaces
    # and store the data as tuples in a list
    data = []
    endpoints = aci.Endpoint.get(session)
    for ep in endpoints:
        epg = ep.get_parent()
        app_profile = epg.get_parent()
        tenant = app_profile.get_parent()
        data.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                     tenant.name, app_profile.name, epg.name))

    # Display the data downloaded
    print(tabulate(data, headers=["MACADDRESS", "IPADDRESS", "INTERFACE",
                                  "ENCAP", "TENANT", "APP PROFILE", "EPG"]))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass