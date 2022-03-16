"""
aci_generic.py

ACI general helper functions for lab preparation.  Includes any tasks
which don't fall into a specific ACI object category (for example, testing
APIC connectivity, loading configs, committing Cobra object to ACI, etc.)
"""
import logging
import time
import requests
import urllib3
import yaml
import cobra.mit.access
import cobra.mit.request
from .ApicTypeHints import LabConfigFile


logger = logging.getLogger(__name__)

# ACI simulator will be using self-signed certificates.  Disable the insecure
# TLS connection warning.
urllib3.disable_warnings()


def test_apic_connection(
    url: str,
    username: str,
    password: str,
    retry_minutes: int = 10,
    tls_verify: bool = False,
) -> None:
    """
    Test that the APIC is reachable and the API is responding as expected by
    attempting to authenticate.  If a 200 is received from a login request,
    we are ready to proceed with configuration.  If no response or a 200 is
    not received, sleep for some interval and try again.  If no successful
    response within the retry_minutes time period, raise a RuntimeError to
    be caught by the calling script.

    :param url: Base URL of the apic without API endpoint.  Include the scheme
        and host - for example, https://apic
    :param username: Username for authentication to the APIC API
    :param password: Password for the username being authenticated
    :param retry_minutes: Maximum minutes to retry before failure.  Default 10
    :param tls_verify: Whether to perform certificate chain validation against
        TLS-secured URL.  Default to False (this SHOULD be True, but the ACI
        simulator uses self-signed certificates by default.
    :return: None (no return value).  Raise RuntimeError if retry_minutes
        reached before successful response.
    """
    login_url = f"{url}/api/aaaLogin.json"
    login_payload = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}

    # Make sure APIC is up and accessible
    logger.info("Verifying APIC REST API is up and running...")
    attempt_count = 0
    while True:
        # Make sure not stuck waiting on APIC to come up
        if attempt_count > retry_minutes:
            raise RuntimeError(
                f"ERROR: APIC has not come up after {retry_minutes} minutes."
            )
        try:
            response = requests.post(login_url, json=login_payload, verify=tls_verify)
            if response.status_code == 200:
                # all good
                break

        # If unable to connect, fail test
        except requests.exceptions.RequestException:
            logger.info("APIC REST API not available, waiting 1 minute.")
            attempt_count += 1
            time.sleep(60)


def load_config_from_file(config_file: str) -> LabConfigFile:
    """
    Loads data from a given YAML-formatted file and returns the resulting
    data structure.  If an exception is encountered, throw a RuntimeError
    to be caught by the calling script.

    :param config_file: Path and name of the YAML file to load
    :return: Python object representing the loaded YAML data on success.  Raise
        a RuntimeError if exception encountered while attempting to load the
        specified config file.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as config:
            loaded_config = yaml.safe_load(config)
    except FileNotFoundError as config_load_err:
        raise RuntimeError(
            f"Missing configuration file '{config_file}' - unable to continue."
        ) from config_load_err
    except yaml.parser.ParserError as config_load_err:
        raise RuntimeError(
            f"Config file '{config_file}' is not valid YAML - unable to continue"
        ) from config_load_err

    return loaded_config


def commit_config(
    mo_directory: cobra.mit.access.MoDirectory, managed_object: object
) -> None:
    """
    Wrapper function to commit a Cobra SDK object to the APIC.  This may be
    used to commit bulk changes - for example, all configuration changed under
    pol:Uni may be submitted here to commit at once.

    :param mo_directory: Cobra SDK object reference to the Managed Object
        Directory handle (cobra.mit.access.MoDirectory object)
    :param managed_object: Cobra SDK object reference to the MO being committed
        to the APIC's configuration
    :return: None (no return value)
    """
    cobra_config_request = cobra.mit.request.ConfigRequest()
    cobra_config_request.addMo(managed_object)
    mo_directory.commit(cobra_config_request)
