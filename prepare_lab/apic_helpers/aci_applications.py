"""
aci_applications.py

ACI Application helper functions for lab preparation script
"""
from typing import List
import logging
import cobra.model.fv
from .ApicTypeHints import AciTenantApplicationProfile, AciApplicationEpg

logger = logging.getLogger(__name__)


def create_application_profile(
    tenant_mo: cobra.model.fv.Tenant, profile_data: AciTenantApplicationProfile
) -> object:
    """
    Create a new application profile in the ACI fabric.  Parameters limited
    at this time to essentials - can expand to include additional items such
    as AP description if desired

    :param tenant_mo: Cobra SDK tenant object reference
    :param profile_data: Dictionary representing possible configurable
        options for an application profile
    :return: Cobra object representing the new application profile
    """
    name = profile_data["name"]
    description = profile_data.get("description", "")
    name_alias = profile_data.get("name_alias", "")
    annotation = profile_data.get("annotation", "")

    logger.info("Creating application profile '%s'...", name)
    new_profile = cobra.model.fv.Ap(
        tenant_mo,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )

    return new_profile


def create_app_epg(
    app_profile_mo: cobra.model.fv.Ap, epg_data: AciApplicationEpg
) -> object:
    """
    Create new Application Endpoint Group (EPG) in the ACI fabric.

    :param app_profile_mo: Cobra SDK application profile object reference
    :param epg_data: Dictionary representing possible configurable
        options for an application EPG
    :return: Cobra object representing the new EPG
    """
    name = epg_data["name"]
    description = epg_data.get("description", "")
    name_alias = epg_data.get("name_alias", "")
    annotation = epg_data.get("annotation", "")

    logger.info(
        "Creating EPG '%s' in application profile '%s'...", name, app_profile_mo.name
    )
    new_epg = cobra.model.fv.AEPg(
        app_profile_mo,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )

    return new_epg


def associate_epg_to_bridge_domain(
    epg_mo: cobra.model.fv.AEPg, bd_name: str
) -> cobra.model.fv.RsBd:
    """
    Associate an Application EPG with a bridge domain

    :param epg_mo: Cobra SDK Application EPG object reference
    :param bd_name: Name of the bridge domain to be associated
    :return: Cobra object representing the new EPG/BD association
    """
    logger.info("Associating EPG '%s' to bridge domain '%s'...", epg_mo.name, bd_name)
    epg_association = cobra.model.fv.RsBd(epg_mo, tnFvBDName=bd_name)
    return epg_association


def create_epg_provided_contract(
    epg_mo: cobra.model.fv.AEPg, contract_name: str
) -> object:
    """
    Build the relationship between an Application EPG and a contract.  The EPG
    will be providing the contract.

    :param epg_mo: Cobra SDA Application EPG object reference
    :param contract_name: Name of the contract the EPG should provide
    :return: Cobra object representing the provided contract relationship
    """
    logger.info("Providing contract '%s' from EPG '%s'...", contract_name, epg_mo.name)
    contract_provider = cobra.model.fv.RsProv(epg_mo, tnVzBrCPName=contract_name)

    return contract_provider


def create_epg_consumed_contract(
    epg_mo: cobra.model.fv.AEPg, contract_name: str
) -> object:
    """
    Build the relationship between an Application EPG and a contract.  The EPG
    will be consuming the contract.

    :param epg_mo: Cobra SDA Application EPG object reference
    :param contract_name: Name of the contract the EPG should consume
    :return: Cobra object representing the consumed contract relationship
    """
    logger.info("Consuming contract '%s' to EPG '%s'...", contract_name, epg_mo.name)
    contract_consumer = cobra.model.fv.RsCons(epg_mo, tnVzBrCPName=contract_name)

    return contract_consumer


def build_applications(
    tenant_mo: cobra.model.fv.Tenant,
    application_profiles: List[AciTenantApplicationProfile],
) -> None:
    """
    Wrapper procedure to build application profiles, EPGs, and contract
    associations given a list of application constructs.  Example expected
    input is a list in the format:

    [
        {
            "name": "Application_profile_name",
            "app_epg": [
                {
                    "name": "EPG_name",
                    "consumed_contracts": [
                        "contract_name",
                        "contract_name"
                    ],
                    "provided_contracts": [
                        "contract_name",
                        "contract_name"
                    ]
                }
            ]
        }
    ]

    Consumed or provided contracts are not required and may be specified
    as consumed, provided, or both.

    :param tenant_mo: Cobra SDK tenant object reference
    :param application_profiles: List of application profiles, EPGs, and
        provided / consumed contract relationships to create
    :return: None (no return value)
    """

    for application_profile in application_profiles:
        new_app = create_application_profile(
            tenant_mo=tenant_mo, profile_data=application_profile
        )

        try:
            # Catch KeyError if no Application EPGs are defined
            for epg in application_profile["app_epg"]:
                new_epg = create_app_epg(app_profile_mo=new_app, epg_data=epg)
                associate_epg_to_bridge_domain(
                    epg_mo=new_epg, bd_name=epg["bridge_domain"]
                )
                try:
                    # Catch KeyError if no consumed contracts are defined
                    for consumed_contract in epg["consumed_contracts"]:
                        create_epg_consumed_contract(
                            epg_mo=new_epg, contract_name=consumed_contract
                        )
                except KeyError:
                    # Don't fail on missing consumed contracts
                    pass

                try:
                    # Catch KeyError if no provided contracts are defined
                    for provided_contract in epg["provided_contracts"]:
                        create_epg_provided_contract(
                            epg_mo=new_epg, contract_name=provided_contract
                        )
                except KeyError:
                    # Don't fail on missing provided contracts
                    pass
        except KeyError:
            # Don't fail on missing EPGs
            pass
