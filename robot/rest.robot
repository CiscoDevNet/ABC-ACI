** Settings ***
Library         REST     https://10.10.20.14    ssl_verify=false
Suite Setup        Get APIC Token
*** Variables ***
${auth_json}            {"aaaUser": {"attributes": { "name": "admin", "pwd" : "C1sco12345"}}}

*** Keywords ***
Get APIC Token
    ${res}=  POST  /api/aaaLogin.json  ${auth_json}
    Integer  response status  200
    ${cookie}=  Catenate  APIC-cookie\=${res['body']['imdata'][0]['aaaLogin']['attributes']['token']}
    Set Suite Variable  ${cookie}  ${cookie}
    [Teardown]  Set Suite Variable  ${cookie}  ${cookie}

*** Test Cases ***
Test Check NGINX Rest API Status
    Set Headers  {"Cookie": "${cookie}"}
    ${res}=  GET  /api/node/mo/topology/pod-1/node-1/sys/proc/proc-nginx.json?query-target=self
    Integer         response status                 200
    Output  response body imdata 0 procEntry attributes
    [Teardown]



