

# Define an ACI Application Profile Resource.
resource "aci_application_profile" "terraform_ap" {
    tenant_dn  = aci_tenant.terraform_tenant.id
    name       = var.ap
    description = "App Profile Created Using Terraform"
}

# Define an ACI Application EPG Resource with iterator.
resource "aci_application_epg" "terraform_epg" {
    for_each                = var.epgs
    application_profile_dn  = aci_application_profile.terraform_ap.id
    name                    = each.value.epg
    relation_fv_rs_bd       = aci_bridge_domain.terraform_bd.id
    description             = "EPG Created Using Terraform"
}
# Define an ACI Application EPG Resource with static value.
resource "ToDo" "db_epg" {
    for_each                = var.epgs
    application_profile_dn  = aci_application_profile.terraform_ap.id
    name                    = epg-db    
    relation_fv_rs_bd       = aci_bridge_domain.terraform_bd.id
    description             = "EPG Created Using Terraform"
}


