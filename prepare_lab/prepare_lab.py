"""
prepare_lab.py

Use the Cobra SDK to initialize the APIC to a base state required for lab tasks
This will only create APIC constructs, any other setup requirements (e.g. for
Jenkins) must be created in a separate script.

NOTE: due to the required packages, a Python interpreter from a venv with the
Cobra SDK must be used.

Usage:
/path/to/venv/bin/python ./prepare_lab.py -c /path/to/lab_setup.yml
"""
import os
import sys
import argparse
import logging
import cobra.mit.access
import cobra.mit.session
import cobra.model.pol
from apic_helpers import (
    load_config_from_file,
    test_apic_connection,
    commit_config,
    create_tenant,
    build_vrfs,
    build_bridge_domains,
    build_contract_filters,
    build_contracts,
    build_applications,
)

# Create the logger
LOGLEVEL = logging.INFO
logger = logging.getLogger(__name__)
logging.basicConfig(level=LOGLEVEL, format="%(levelname)s: %(message)s")

# Determine path of this script
script_basepath = os.path.dirname(__file__)

# Set defaults
DEFAULT_CONFIG_FILE = f"{script_basepath}/lab_setup.yml"

# Set variables for APIC connectivity
APIC_URL = "https://apic"
APIC_USERNAME = "developer"
APIC_PASSWORD = "1234QWer"
APIC_TIMEOUT_MINUTES = 5


if __name__ == "__main__":
    # Grab command-line arguments and set defaults
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", dest="config_file", action="store")
    parser.set_defaults(config_file=DEFAULT_CONFIG_FILE)

    # We don't care about extra / unknown arguments, so only obtain the first
    # element of parse_known_args()
    args = parser.parse_known_args()[0]

    # Load the lab config
    try:
        lab_config = load_config_from_file(args.config_file)
        test_apic_connection(
            url=APIC_URL,
            username=APIC_USERNAME,
            password=APIC_PASSWORD,
            retry_minutes=APIC_TIMEOUT_MINUTES,
        )
    except RuntimeError as err:
        # Any errors in reading the config, parsing the YAML, or connecting to
        # the APIC will raise a RuntimeError - catch it here and exit.
        logger.critical("Error encountered in lab setup script:\n\t%s", err)
        sys.exit(255)

    logger.info("\n%s\nBeginning APIC configuration.\n%s", "*" * 78, "*" * 78)

    # Create the Cobra session
    ls = cobra.mit.session.LoginSession(APIC_URL, APIC_USERNAME, APIC_PASSWORD)
    md = cobra.mit.access.MoDirectory(ls)
    md.login()
    polUni = cobra.model.pol.Uni("")
    # infraInfra = cobra.model.infra.Infra(polUni)
    # infraFuncP = cobra.model.infra.FuncP(infraInfra)

    # For each tenant, call appropriate builders to generate network constructs
    for tenant in lab_config["tenants"]:

        # Tenant must be created before moving forward...
        tenant_mo = create_tenant(policy_universe=polUni, tenant_data=tenant["tenant"])

        try:
            build_vrfs(tenant_mo=tenant_mo, vrfs=tenant["vrfs"])
        except KeyError:
            # Don't fail if no VRFs are defined
            logger.info("No VRFs defined, skipping...")

        try:
            build_bridge_domains(
                tenant_mo=tenant_mo, bridge_domains=tenant["bridge_domains"]
            )
        except KeyError:
            # Don't fail if no bridge domains are defined
            logger.info("No bridge domains defined, skipping...")

        try:
            build_contract_filters(
                tenant_mo=tenant_mo, contract_filters=tenant["contract_filters"]
            )
        except KeyError:
            # Don't fail if no contract filters are defined
            logger.info("No contract filters defined, skipping...")

        try:
            build_contracts(tenant_mo=tenant_mo, contracts=tenant["contracts"])
        except KeyError:
            # Don't fail if no contracts are defined
            logger.info("No contracts defined, skipping...")

        try:
            build_applications(
                tenant_mo=tenant_mo, application_profiles=tenant["application_profiles"]
            )
        except KeyError:
            # Don't fail if no applications are defined
            logger.info("No applications defined, skipping...")

    # Commit all changes to pol:Uni
    commit_config(mo_directory=md, managed_object=polUni)

    logger.info("\n%s\nAPIC configuration complete.\n%s", "*" * 78, "*" * 78)
