# Installation

Install pyATS|Genie and Rest Connector.
```
pip install 'pyats[full]' rest.connector

git clone https://wwwin-github.cisco.com/DevNet/ABC-ACI.git
cd ABC-ACI/pyats
# uninstall genie.libs.sdk and install wheel in this repository
pip uninstall genie.libs.sdk -y
pip install genie.libs.sdk-20.7.2b2-py3-none-any.whl
```

# Running

By pyats run job command
```
pyats run job job.py --testbed-file aci_devnet_sandbox.yaml --trigger-datafile pre_trigger_datafile.yaml --html-logs pre_snapshots

(configure by Ansible)

pyats run job job.py --testbed-file aci_devnet_sandbox.yaml --trigger-datafile post_trigger_datafile.yaml --html-logs post_snapshots
```

HTML report and JSON files (snapshots) will be generated under `pre|post_snapshots` folders.

