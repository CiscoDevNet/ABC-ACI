import os
import time
import argparse

# from pyats import aetest

# Needed for logic
from pyats.datastructures.logic import And, Not, Or
from genie.harness.main import gRun

pre_snapshot_path = "./pre_snapshots"
post_snapshot_path = "./post_snapshots"

try:
    os.mkdir(pre_snapshot_path)
    os.mkdir(post_snapshot_path)
except FileExistsError:
    pass


def main():
    test_path = os.path.dirname(__file__)
    gRun(
        trigger_datafile=os.path.join(test_path, 'trigger_snapshot.yaml'),
        subsection_datafile=os.path.join(test_path, 'subsection_datafile.yaml'),
        trigger_groups=And('aci'),
        trigger_uids=And("post_change_snapshot")
    )
