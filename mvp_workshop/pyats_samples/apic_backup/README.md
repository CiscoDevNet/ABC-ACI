# pyATS Example - APIC Backup and Restore

This contains an example pair of scripts to backup all tenants and their child objects.

The path for the backups is specified in the top of the ```pyats_apic_backup.py``` file (only a directory is specified)
and each tenant will be backed up to a separate file inside ```{backup_dir}/YYYY-MM-DD```.


To restore an entire tenant (and all objects within the tenant), use the ```pyats_apic_restore.py``` script followed by
the path and filename of one or more files to restore.

## Usage:
### Backup tenants:
1. Review the code :)
2. ```python ./pyats_apic_backup.py```

### Restore tenant(s):
1. Review the code...
2. ```python ./pyats_apic_restore.py /path/to/file1.json [/path/to/file2.json /path/to...]```
