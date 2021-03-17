# Installation

Install pyATS|Genie and Rest Connector.
```
pip install 'pyats[full]' rest.connector
pip install genie.libs.sdk --upgrade --pre

git clone https://wwwin-github.cisco.com/DevNet/ABC-ACI.git
cd ABC-ACI/pyats
```

# Running

By pyats run job command
```
pyats run job job.py --testbed-file aci_devnet_sandbox.yaml --trigger-datafile pre_trigger_datafile.yaml --html-logs pre_snapshots

(configure by Ansible)

pyats run job job.py --testbed-file aci_devnet_sandbox.yaml --trigger-datafile post_trigger_datafile.yaml --html-logs post_snapshots
```

HTML report and JSON files (snapshots) will be generated under `pre|post_snapshots` folders.

