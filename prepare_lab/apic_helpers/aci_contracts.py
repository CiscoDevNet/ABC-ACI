"""
aci_contracts.py

ACI Contract helper functions for lab preparation
"""
from typing import List
import logging
import cobra.model.fv
import cobra.model.vz
from .ApicTypeHints import (
    AciContractFilterEntry,
    AciContract,
    AciContractSubject,
    AciContractFilter,
)

logger = logging.getLogger(__name__)


def create_contract(
    tenant_mo: cobra.model.fv.Tenant, contract_data: AciContract
) -> cobra.model.vz.BrCP:
    """
    Create a new contract in the ACI fabric.  Parameters limited at this time
    to essentials - can expand to include additional items such as contract
    description if desired

    :param tenant_mo: Cobra SDK tenant object reference
    :param contract_data: Dictionary representing possible configurable
        options for a contract
    :return: Cobra object representing the new contract
    """
    name = contract_data["name"]
    description = contract_data.get("description", "")
    name_alias = contract_data.get("name_alias", "")
    annotation = contract_data.get("annotation", "")
    logger.info("Building contract '%s'...", name)
    new_contract = cobra.model.vz.BrCP(
        tenant_mo,
        name=name,
        descr=description,
        annotation=annotation,
        name_alias=name_alias,
    )

    return new_contract


def create_contract_subject(
    contract_mo: cobra.model.vz.BrCP, subject_data: AciContractSubject
) -> cobra.model.vz.Subj:
    """
    Create a new subject within an ACI contract

    :param contract_mo: Cobra SDK contract object reference
    :param subject_data: Dictionary representing possible configurable
        options for a contract subject
    :return: Cobra object representing the new contract subject
    """
    name = subject_data["name"]
    description = subject_data.get("description", "")
    name_alias = subject_data.get("name_alias", "")
    annotation = subject_data.get("annotation", "")

    logger.info("Building contract subject '%s'...", name)
    new_subject = cobra.model.vz.Subj(
        contract_mo,
        name=name,
        descr=description,
        annotation=annotation,
        name_alias=name_alias,
    )

    return new_subject


def create_contract_filter(
    tenant_mo: cobra.model.fv.Tenant, filter_data: AciContractFilter
) -> cobra.model.vz.Filter:
    """
    Create a new contract filter inside an ACI tenant.  Contract filters
    are containers for filter entries.

    :param tenant_mo: Cobra SDK tenant object reference
    :param filter_data: Dictionary representing possible configurable
        options for a contract filter
    :return: Cobra object representing the new contract filter
    """
    name = filter_data["name"]
    description = filter_data.get("description", "")
    name_alias = filter_data.get("name_alias", "")
    annotation = filter_data.get("annotation", "")

    logger.info("Building contract filter '%s' in tenant '%s'...", name, tenant_mo.name)
    new_filter = cobra.model.vz.Filter(
        tenant_mo,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )

    return new_filter


def create_contract_filter_entry(
    filter_mo: cobra.model.vz.Filter,
    filter_entry: AciContractFilterEntry,
) -> cobra.model.vz.Entry:
    """
    Create a new contract filter entry inside a contract filter.  Due to the
    number of possible options, arguments are received as **kwargs and defaults
    matching the ACI object model reference defaults will be set for any
    missing key.

    :param filter_mo: Cobra SDK filter object reference
    :param filter_entry: Dictionary representing possible configurable
        options for a filter entry
    :return: Cobra object representing the new contrat filter entry
    """
    # Set defaults for all possible filter entry options based on the ACI
    # API reference for values used when not explicitly set.
    name = filter_entry["name"]
    description = filter_entry.get("description", "")
    name_alias = filter_entry.get("name_alias", "")
    annotation = filter_entry.get("annotation", "")
    ether_type = filter_entry.get("ether_type", "unspecified")
    source_port_from = filter_entry.get("source_port_from", "unspecified")
    source_port_to = filter_entry.get("source_port_to", "unspecified")
    dest_port_from = filter_entry.get("dest_port_from", "unspecified")
    dest_port_to = filter_entry.get("dest_port_to", "unspecified")
    proto = filter_entry.get("proto", "unspecified")
    tcp_rules = filter_entry.get("tcp_rules", "unspecified")
    apply_to_frag = str(filter_entry.get("apply_to_frag", "false")).lower()
    arp_opcodes = filter_entry.get("arp_opcodes", "unspecified")
    icmp4_type = filter_entry.get("icmp4_type", "unspecified")
    icmp6_type = filter_entry.get("icmp6_type", "unspecified")
    stateful = str(filter_entry.get("stateful", "false")).lower()
    dscp = filter_entry.get("dscp", "unspecified")

    logger.info("Building filter entry '%s'...", name)

    new_entry = cobra.model.vz.Entry(
        filter_mo,
        annotation=annotation,
        tcpRules=tcp_rules,
        arpOpc=arp_opcodes,
        applyToFrag=apply_to_frag,
        dFromPort=dest_port_from,
        dToPort=dest_port_to,
        descr=description,
        prot=proto,
        icmpv4T=icmp4_type,
        icmpv6T=icmp6_type,
        sFromPort=source_port_from,
        sToPort=source_port_to,
        stateful=stateful,
        name=name,
        name_alias=name_alias,
        etherT=ether_type,
        matchDscp=dscp,
    )

    return new_entry


def associate_contract_subject_to_filter(
    contract_subject_mo: cobra.model.vz.Subj, filter_name: str
) -> cobra.model.vz.RsSubjFiltAtt:
    """
    Create the association between a contract filter and a contract subject

    :param contract_subject_mo: Cobra SDK contract subject object reference
    :param filter_name: Name of the contract filter to associate with the subject
    :return: Cobra object representing the new subject/filter association
    """
    logger.info(
        "Associating contract filter '%s' to contract subject " "'%s'...",
        filter_name,
        contract_subject_mo.name,
    )
    new_association = cobra.model.vz.RsSubjFiltAtt(
        contract_subject_mo, tnVzFilterName=filter_name
    )

    return new_association


def build_contract_filters(
    tenant_mo: cobra.model.fv.Tenant, contract_filters: List[AciContractFilter]
) -> None:
    """
    Wrapper procedure to build contract filters and associated filter entries.
    Example expected input is a list in the format:

    [
        {
            "name": "Contract_filter_name",
            "filter_entries": [
                {
                    "name": "Filter_entry_namne",
                    "ether_type": "ip",
                    "proto": "L4_protocol",
                    "dest_port_from": "destination_starting_port",
                    "dest_port_to": "destination_ending_port",
                    ... any other filter options
                }
            ]
        }
    ]

    :param tenant_mo: Cobra SDK tenant object reference
    :param contract_filters: List of contract filters and associated filter
        entries to create
    :return: None (no return value)
    """
    for contract_filter in contract_filters:
        new_filter = create_contract_filter(
            tenant_mo=tenant_mo, filter_data=contract_filter
        )

        try:
            # Catch KeyError if no filter entries are defined
            for filter_entry in contract_filter["filter_entries"]:
                create_contract_filter_entry(
                    filter_mo=new_filter, filter_entry=filter_entry
                )
        except KeyError:
            # Don't fail on missing filter entries
            pass


def build_contracts(
    tenant_mo: cobra.model.fv.Tenant, contracts: List[AciContract]
) -> None:
    """
    Wrapper procedure to build contracts, contract subjects, and associate
    contract filters with contract subjects.  Example input is a list of
    contract data in the format:

    [
        {
            "name": "Contract_name",
            "subjects": [
                {
                    "name": "Contract_subject_name",
                    "filters": [
                        "filter_to_associate_with_subject",
                        "filter_to_associate_with_subject"
                    ]
                }
            ]
        }
    ]

    :param tenant_mo: Cobra SDK tenant object reference
    :param contracts: List of contracts, contract subjects, and filters to
        associate with the subjects
    :return: None (no return value)
    """
    for contract in contracts:
        new_contract = create_contract(tenant_mo=tenant_mo, contract_data=contract)

        try:
            # Catch KeyError if no contract subjects are defined
            for contract_subject in contract["subjects"]:
                new_subject = create_contract_subject(
                    contract_mo=new_contract, subject_data=contract_subject
                )

                try:
                    # Catch KeyError if no filter associations are defined
                    for subject_filter in contract_subject["filters"]:
                        associate_contract_subject_to_filter(
                            contract_subject_mo=new_subject, filter_name=subject_filter
                        )
                except KeyError:
                    # Don't fail on missing filter associations
                    pass
        except KeyError:
            # Don't fail on missing contract subjects
            pass
