"""
aci_tenants.py

ACI Tenant helper functions for lab preparation
"""
from typing import List
import logging
import cobra.model.pol
import cobra.model.fv
from .ApicTypeHints import AciTenantVrf, AciTenantBridgeDomain, AciTenant, AciBdSubnet


logger = logging.getLogger(__name__)


def create_tenant(
    policy_universe: cobra.model.pol.Uni, tenant_data: AciTenant
) -> cobra.model.fv.Tenant:
    """
    Create a new tenant in the ACI fabric

    :param policy_universe: Cobra SDK pol:Uni object reference
    :param tenant_data: Dictionary representing possible configurable
        options for a tenant
    :return: Cobra object representing the created tenant
    """
    name = tenant_data["name"]
    description = tenant_data.get("description", "")
    name_alias = tenant_data.get("name_alias", "")
    annotation = tenant_data.get("annotation", "")

    logger.info("Creating tenant '%s'...", name)
    new_tenant = cobra.model.fv.Tenant(
        policy_universe,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )
    return new_tenant


def create_bd(
    tenant_mo: cobra.model.fv.Tenant, bd_data: AciTenantBridgeDomain
) -> cobra.model.fv.BD:
    """
    Create a new bridge domain inside a tenant

    :param tenant_mo: Cobra SDK tenant object reference
    :param bd_data: Dictionary representing possible configurable
        options for a bridge domain
    :return: Cobra object representing the created bridge domain
    """
    name = bd_data["name"]
    description = bd_data.get("description", "")
    name_alias = bd_data.get("name_alias", "")
    annotation = bd_data.get("annotation", "")

    logger.info("Building bridge domain '%s'...", name)
    new_bd = cobra.model.fv.BD(
        tenant_mo,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )
    return new_bd


def create_vrf(
    tenant_mo: cobra.model.fv.Tenant, vrf_data: AciTenantVrf
) -> cobra.model.fv.Ctx:
    """
    Create a new VRF inside a tenant

    :param tenant_mo: Cobra SDK tenant object reference
    :param vrf_data: Dictionary representing possible configurable
        options for a VRF
    :return: Cobra object representing the created VRF
    """
    name = vrf_data["name"]
    description = vrf_data.get("description", "")
    name_alias = vrf_data.get("name_alias", "")
    annotation = vrf_data.get("annotation", "")

    logger.info("Creating VRF '%s'...", name)
    new_vrf = cobra.model.fv.Ctx(
        tenant_mo,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )
    return new_vrf


def associate_vrf_to_bd(
    bd_mo: cobra.model.fv.BD, vrf_name: str
) -> cobra.model.fv.RsCtx:
    """
    Associate a VRF with a bridge domain

    :param bd_mo: Cobra SDK bridge domain object reference
    :param vrf_name: Name of the VRF to associate with the BD
    :return: Cobra object representing the VRF to bridge domain association
    """
    logger.info("Associating VRF '%s' with bridge domain '%s'...", vrf_name, bd_mo.name)
    vrf_bd_association = cobra.model.fv.RsCtx(bd_mo, tnFvCtxName=vrf_name)
    return vrf_bd_association


def create_bd_subnet(
    bd_mo: cobra.model.fv.BD, subnet_data: AciBdSubnet
) -> cobra.model.fv.Subnet:
    """
    Create a new subnet inside a bridge domain

    :param bd_mo: Cobra SDK bridge domain object reference
    :param subnet_data: Dictionary representing possible configurable
        options for a subnet
    :return: Cobra object representing the created subnet
    """
    subnet_ip = subnet_data["ip"]
    name = subnet_data.get("name", "")
    description = subnet_data.get("description", "")
    name_alias = subnet_data.get("name_alias", "")
    annotation = subnet_data.get("annotation", "")

    logger.info("Creating subnet '%s' in BD '%s'...", subnet_ip, bd_mo.name)
    new_subnet = cobra.model.fv.Subnet(
        bd_mo,
        ip=subnet_ip,
        name=name,
        descr=description,
        name_alias=name_alias,
        annotation=annotation,
    )
    return new_subnet


def build_vrfs(tenant_mo: cobra.model.fv.Tenant, vrfs: List[AciTenantVrf]) -> None:
    """
    Wrapper procedure to create VRFs.  Example expected input from config
    file is a list in the format:

    [
        {
            "name": "VRF_name"
        }
    ]

    :param tenant_mo: Cobra SDK tenant object reference
    :param vrfs: List of VRFs to create
    :return: None (no return value)
    """
    for vrf in vrfs:
        create_vrf(tenant_mo=tenant_mo, vrf_data=vrf)


def build_bridge_domains(
    tenant_mo: cobra.model.fv.Tenant, bridge_domains: List[AciTenantBridgeDomain]
) -> None:
    """
    Wrapper procedure to create bridge domains, VRFs, subnets, and associate
    VRFs to bridge domains if defined. Example expected input is a list in the format:

    [
        {
            "name": "Bridge_domain_name",
            "vrf": "VRF_to_create_and_associate",
            "subnets": [
              "ip_and_prefix_in_cidr_notation",
              "ip_and_prefix_in_cidr_notation"
            ]
        }
    ]

    :param tenant_mo: Cobra SDK tenant object reference
    :param bridge_domains: List of bridge domains and associated VRFs and
        subnets to create
    :return: None (no return value)
    """
    try:
        for bridge_domain in bridge_domains:
            new_bd = create_bd(tenant_mo=tenant_mo, bd_data=bridge_domain)
            if bridge_domain["vrf"] is not None:
                associate_vrf_to_bd(bd_mo=new_bd, vrf_name=bridge_domain["vrf"])

            for subnet in bridge_domain["subnets"]:
                create_bd_subnet(bd_mo=new_bd, subnet_data=subnet)
    except KeyError:
        # Don't fail if no VRF or subnets defined
        pass
