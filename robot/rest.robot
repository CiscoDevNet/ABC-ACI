** Settings ***
Library         REST     https://10.10.20.14    ssl_verify=false

*** Test Cases ***
Basic Auth Example
    POST            /api/aaaLogin.json    body={"aaaUser" : { "attributes" : { "name" : "admin","pwd" : "C1sco12345" } }}
    Output          response
    Integer         response status                 200

Get Tenants 
    GET            /api/class/fvTenant.json
    Output          response
    Integer         response status                 200



