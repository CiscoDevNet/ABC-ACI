"""
This file contains definitions for type hinting of ACI objects created by
APIC helper functions.  As some data structures may be used in multiple
files, the goal is to centralize them in this file and import as needed
in the various helper files.
"""
from typing import Union, Optional, TypedDict, List, Literal


class AciCommonAttributes(TypedDict):
    """
    Class representing the common dictionary keys used in ACI objects.
    """

    description: Optional[str]
    name_alias: Optional[str]
    annotation: Optional[str]


class AciTenant(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant objects
    """

    name: str


class AciTenantVrf(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> networking -> VRFs
    """

    name: str


class AciBdSubnet(AciCommonAttributes):
    """
    Lab config file structure for ACI bridge domain subnets.
    """

    ip: str  # IP address/prefix (CIDR notation).  Leave as string for now.
    name: Optional[str]


class AciTenantBridgeDomain(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> networking -> bridge domains
    """

    name: str
    arp_flooding: Optional[bool]
    ip_learning: Optional[bool]
    vrf: Optional[str]
    subnets: List[AciBdSubnet]


class AciApplicationEpg(AciCommonAttributes):
    """
    Lab config file structure for ACI Application Endpoint Group (EPG)
    """

    name: str
    bridge_domain: str
    provider_label_match: Literal[
        "All", "AtleastOne", "AtmostOne", "None", "defaultValue", None
    ]
    shutdown: Optional[bool]
    consumed_contracts: List[str]
    provided_contracts: List[str]


class AciTenantApplicationProfile(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> application profiles
    """

    name: str
    app_epg: List[AciApplicationEpg]


class AciContractFilterEntry(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> contracts -> filters
        -> filter entries
    """

    name: str
    ether_type: Optional[str]
    source_port_from: Union[int, str, None]
    source_port_to: Union[int, str, None]
    dest_port_from: Union[int, str, None]
    dest_port_to: Union[int, str, None]
    proto: Optional[str]
    tcp_rules: Optional[str]
    apply_to_frag: Optional[bool]
    arp_opcodes: Optional[str]
    icmp4_type: Optional[str]
    icmp6_type: Optional[str]
    stateful: Optional[bool]
    dscp: Optional[int]  # Should set the range for DSCP - leave as int for now


class AciContractFilter(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> contracts -> filters
    """

    name: str
    filter_entries: List[AciContractFilterEntry]


class AciContractSubject(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> contracts -> standard
        -> contract_name -> subjects
    """

    name: str
    consumer_match_type: Literal[
        "All", "AtleastOne", "AtmostOne", "None", "defaultValue", None
    ]
    provider_match_type: Literal[
        "All", "AtleastOne", "AtmostOne", "None", "defaultValue", None
    ]
    reverse_filter_ports: Optional[bool]
    filters: List[str]


class AciContract(AciCommonAttributes):
    """
    Lab config file structure for ACI tenant -> contracts
    """

    name: str
    subjects: List[AciContractSubject]


class LabTenantConfig(TypedDict):
    """
    Data structure for each tenant in the config file
    """

    tenant: AciTenant
    vrfs: List[AciTenantVrf]
    bridge_domains: List[AciTenantBridgeDomain]
    application_profiles: List[AciTenantApplicationProfile]
    contract_filters: List[AciContractFilter]
    contracts: List[AciContract]


class LabConfigFile(TypedDict):
    """
    Overall configuration file format, which is a list of the LabTenantConfig
    objects.
    """

    tenants: List[LabTenantConfig]
