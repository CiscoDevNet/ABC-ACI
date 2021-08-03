
# Define an ACI Tenant Resource.
resource "aci_tenant" "terraform_tenant" {
    name        = "abc-tenant"
    #description = "This tenant is imported by terraform"
}
# Define an ACI Tenant VRF Resource.
resource "aci_vrf" "terraform_vrf" {
    tenant_dn   = aci_tenant.terraform_tenant.id
    description = "VRF Created Using Terraform"
    name        = "prod_vrf"
}

# Define an ACI Tenant BD Resource.
resource "aci_bridge_domain" "terraform_bd" {
    tenant_dn          = aci_tenant.terraform_tenant.id
    relation_fv_rs_ctx = aci_vrf.terraform_vrf.id
    description        = "BD Created Using Terraform"
    name               = "prod_bd"
}

# Define an ACI Tenant BD Subnet Resource.
resource "aci_subnet" "terraform_bd_subnet" {
    parent_dn   = aci_bridge_domain.terraform_bd.id
    description = "Subnet Created Using Terraform"
    ip          = "10.10.101.1/24"
}


