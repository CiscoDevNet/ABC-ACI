# Installation
Make sure rest.connector is installed

```console
pip install 'pyats[full] rest.connector
```

# Run the code
Via pyATS run job command

```console
pyats run job aci_abc.job --testbed-file testbed.yaml
```

Via pyATS run Genie command (without the job.py file)

```console
pyats run genie --testbed-file testbed.yaml --trigger-datafile trigger_datafile.yaml --trigger-groups "And('tenant') --subsection-datafile subsection_datafile.yaml
```

# Customize
You can change the tenant name under vars at the top of the tigger_datafile.yaml

```yaml
vars:
  tenant: new_tenant
```

You an comment out the delete_tenant step in the job to create / verify tenant via pyATS and then confirm it was created in the APIC GUI

```yaml
#    - delete_tenant:
#        - api:
#            device: uut
#            function: apic_rest_post
#            arguments:
#              dn: "/api/node/mo/uni/tn-%{vars.tenant}.json"
#              payload: |
#                {
#                  "fvTenant": {
#                      "attributes": {
#                        "dn": "uni/tn-%{vars.tenant}",
#                        "status": "deleted"
#                      },
#                      "children": []
#                  }
#                }
#            include:
#              - contains_key_value("totalCount", '0')
```

The check_tenant_was_deleted step is expected to fail if you comment out the above