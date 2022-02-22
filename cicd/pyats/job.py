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
    parser = argparse.ArgumentParser()
    parser.add_argument('--after',
                        dest='after',
                        action='store_true')
    parser.set_defaults(after=False)
    args, unknown = parser.parse_known_args()

    test_path = os.path.dirname(__file__)
    if args.after:
        test_sections = And("post_change_snapshot")
    else:
        test_sections = And("pre_change_snapshot")

    gRun(
        trigger_datafile=os.path.join(test_path, 'trigger_snapshot.yaml'),
        subsection_datafile=os.path.join(test_path, 'subsection_datafile.yaml'),
        trigger_groups=And('aci'),
        trigger_uids=test_sections
    )
