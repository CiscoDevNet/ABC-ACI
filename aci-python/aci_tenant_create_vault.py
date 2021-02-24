 #Issue an API Request to the ACI Simulator with missing credentials
    try:
        response = aaa_login(host=args.aci_host, username="", password="", verify=False)
        print ("Valid Credentials")
    
         # Create a session for our API requests
        session  = requests.Session()
        response = aaa_login(session=session, host=args.aci_host, username=username, password=password, verify=False)

             # Create a new Tenant
        tenant_response = session.post(f'{args.aci_host}/api/mo/uni.json', verify=False, json={
                "fvTenant" : {
                    "attributes" : {
                    "name" : args.tenant
                    }
                }
            })

        print("tenant create response code=%s", tenant_response.status_code)
    except requests.exceptions.InvalidURL as e:
        #logger.error("aci login error=%s", e)
        print ("Missing Credentials")