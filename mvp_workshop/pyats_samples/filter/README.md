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
pyats run genie --testbed-file testbed.yaml --trigger-datafile trigger_datafile.yaml --trigger-groups "And('filter') --subsection-datafile subsection_datafile.yaml
```

# Customize
You an uncomment out the delete_filter_entry step in the job to create / verify filter via pyATS and then confirm it was deleted in the APIC GUI

```yaml
# - delete_filter_entry:
#     - api:
#         device: uut
#         function: apic_rest_post
#         arguments:
#           dn: "/api/node/mo/uni/tn-%{vars.tenant}/flt-%{vars.filter}/e-%{vars.filter_entry}.json"
#           payload: |
#             {
#               "vzEntry": {
#                 "attributes": {
#                   "dn": "uni/tn-%{vars.tenant}/flt-%{vars.filter}/e-%{vars.filter_entry}",
#                   "status": "deleted"
#                 },
#                 "children": []
#               }
#             }
#         include:
#           - contains_key_value("totalCount", '0'
```

The check_tenant_was_deleted step is expected to fail if you comment out the above