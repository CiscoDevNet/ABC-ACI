'''Python Requests Excercise - Getting APIC Authentication Token

This script, once completed, allows the user to retrieve an Authentication
Token to be used when sending API calls against Cisco APIC.
- SPICE LEVEL: MILD
- TASK: Replace the <TODO> with correct code based on the lab guide
  instructions
'''

# Import required libraries
import <TODO>
import <TODO>
#import <TODO>

# Disable unverified HTTPS request warnings
#<TODO>

def get_token():
    '''Return a Cisco APIC authentication token'''

    url = <TODO>

    payload = <TODO>

    response = requests.request(<TODO>, url, data=payload)

    # Print the status code with the URL for information purpose
    print(f"<Status code {<TODO>} for {url}>")

    # Return the Authentication cookie so it can be used in API calls
    return response.<TODO>

# The following if statement is True when this file is executed directly.
if __name__ == "__main__":
    token_cookie = get_token()
    print(token_cookie)
