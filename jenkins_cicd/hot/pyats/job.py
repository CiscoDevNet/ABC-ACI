"""
pyATS Quick Trigger (Blitz) job file for Cisco APIC snapshots.

Use this job without additional parameters to take a pre-change snapshot
of the APIC.

Running with the --after parameter will change the environment as needed
to take a post-change snapshot and compare the pre- and post- change
snapshots.

Example usage:

Pre-snapshot run:
    pyats run job job.py --testbed-file testbed.yaml

Post-snapshot run:
    pyats run job job.py --testbed-file testbed.yaml --after
"""
import os
import argparse
from genie.harness.main import gRun

# Needed for logic
from pyats.datastructures.logic import And

# Determine path of this script
test_path = os.path.dirname(__file__)

# Set the pre- and post- snapshot paths.
pre_snapshot_path = os.path.join(test_path, "pre_snapshots")
post_snapshot_path = os.path.join(test_path, "post_snapshots")


def main():
    """
    This function will be executed automatically when using "pyats run job"

    Parse arguments, set default variables and tests, then trigger the pyATS
    job.
    """
    # Grab command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--after", dest="after", action="store_true")
    parser.set_defaults(after=False)

    # We don't care about extra / unknown arguments, so only obtain the first
    # element of parse_known_args()
    args = parser.parse_known_args()[0]

    # Set environment variables to store paths.  These will be used in the
    # trigger_snapshot file to set output and input paths for saved snapshots.
    os.environ["pre_snapshot_path"] = pre_snapshot_path
    os.environ["post_snapshot_path"] = post_snapshot_path

    # Running this script without the --after parameter will default to
    # pre-change mode, so set the default snapshot_path to pre_snapshot_path.
    os.environ["snapshot_path"] = pre_snapshot_path

    # Default test sections - these will run every time
    test_sections = ["tenant_snapshot"]

    if args.after:
        # If the --after flag has been added, include the 'compare_snapshots'
        # test section and set the snapshot_path environment variable to the
        # post_snapshot_path
        test_sections.append("compare_snapshots")
        os.environ["snapshot_path"] = post_snapshot_path

    # Run the tests
    gRun(
        trigger_datafile=os.path.join(test_path, "trigger_snapshot.yaml"),
        subsection_datafile=os.path.join(test_path, "subsection_datafile.yaml"),
        trigger_groups=And("aci"),
        trigger_uids=test_sections,
    )
