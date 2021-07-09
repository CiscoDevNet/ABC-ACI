#! /usr/bin/env python
"""
Python script to configure baseline the ACI Simulator

Requirements:
  - ACI Cobra 3.0-1k or higher
"""

import requests
from time import sleep
from credentials import *

requests.packages.urllib3.disable_warnings()

# Sandbox Info
username = "admin"
password = "C1sco12345"
retry_minutes = 10

login_url = "https://{host}:{port}/api/aaaLogin.json".format(
    host=HOST,
    port=PORT
    )
login_payload = {
        "aaaUser": {
            "attributes": {
                "name": LOGIN,
                "pwd": PASSWORD
            }
        }
    }

# Make sure APIC is up and accessible
print("Verifying APIC REST API is up and running")
attempt_count = 0
while True:
    # Make sure not stuck waiting on APIC to come up
    if attempt_count > retry_minutes:
        print("ERROR: APIC has not come up after {} minutes.".format(retry_minutes))
        exit("ERROR")
    try:
        response = requests.post(login_url,
                json = login_payload,
                verify = False
               )
        if response.status_code == 200:
            # all good
            break
        else:
            print("APIC REST API not availble, waiting 1 minute.")
            attempt_count += 1
            sleep(60)

    # If unable to connect, fail test
    except Exception as e:
        print("Exception: APIC REST API not availble, waiting 1 minute.")
        attempt_count += 1
        sleep(60)


# Run startup_script.py
try:
    import startup_script
except Exception as e:
    print("Error running startup_script.")
    print(e)

# Run main() from create_snv_apps
import create_snv_apps

try:
    create_snv_apps.main()
except Exception as e:
    print("Error creating apps.")
    print(e)
