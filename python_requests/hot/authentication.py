'''Python Requests Excercise - Getting APIC Authentication Token

This script, once completed, allows the user to retrieve an Authentication
Token to be used when sending API calls against Cisco APIC.
- SPICE LEVEL: HOT
- TASK: Replace the # TODO comments with correct code based on the lab guide
  instructions
'''

# Import required libraries
# TODO: Add imports

# Disable unverified HTTPS request warnings
#<TODO>

def get_token():
    '''Return a Cisco APIC authentication token'''
    
    # TODO: Code to retrieve authentication token

if __name__ == "__main__":
    token_cookie = get_token()
    print(token_cookie)
