# Installation

Install pyATS|Genie and Rest Connector.
```
pip install 'pyats[full]' rest.connector
```

# Running

By pyats run job command
```
pyats run job job.py --testbed-file aci_devnet_sandbox.yaml --html-logs html
```

By pyats run genie command (without `job.py`)
```
pyats run genie --testbed-file aci_devnet_sandbox.yaml --trigger-datafile trigger_datafile.yaml --trigger-groups "And('tenant')" --subsection-datafile subsection_datafile.yaml --html-logs html
```
