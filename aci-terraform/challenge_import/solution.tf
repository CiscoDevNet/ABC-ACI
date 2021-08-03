# Define an ACI Filter-HTTPS Resource.
resource "aci_filter" "terraform_filter_flt-https" {
    tenant_dn   = aci_tenant.terraform_tenant.id
    description = "This is filter filter-https created by terraform"  
    name = "https" 
}
# Define an ACI Filter Entry Resource Filter HTTPS.
resource "aci_filter_entry" "terraform_filter_entry_filter_https" {
    filter_dn     = aci_filter.terraform_filter_flt-https.id
    name          = "https"
    ether_t       = "ipv4"
    prot          = "tcp"
    d_from_port   = 443
    d_to_port     = 443
}
# Define an ACI Filter-SQL Resource.
resource "aci_filter" "terraform_filter_flt-sql" {
    tenant_dn   = aci_tenant.terraform_tenant.id
    description = "This is filter filter-sql created by terraform"  
    name = "sql"
}
# Define an ACI Filter Entry Resource Filter SQL.
resource "aci_filter_entry" "terraform_filter_entry_filter_sql" {
    filter_dn     = aci_filter.terraform_filter_flt-sql.id
    name          = "sql"
    ether_t       = "ipv4"
    prot          = "tcp"
    d_from_port   = 1433
    d_to_port     = 1433
}

# Define an ACI Contract Resource SQL.
resource "aci_contract" "terraform_contract_sql" {
    tenant_dn     = aci_tenant.terraform_tenant.id
    description   = "Contract created using Terraform"
    name = "sql"
}
# Define an ACI Contract Resource Web.
resource "aci_contract" "terraform_contract_web" {
    tenant_dn     = aci_tenant.terraform_tenant.id
    description   = "Contract created using Terraform"
    name = "web"
}
# Define an ACI Contract Subject Resource SQL.
resource "aci_contract_subject" "terraform_contract_subject_sql" {
    contract_dn                   = aci_contract.terraform_contract_sql.id
    relation_vz_rs_subj_filt_att  = [aci_filter.terraform_filter_flt-sql.id]
    name                          = "sql"
}
# Define an ACI Contract Subject Resource Web.
resource "aci_contract_subject" "terraform_contract_subject_https" {
    contract_dn                   = aci_contract.terraform_contract_web.id
    relation_vz_rs_subj_filt_att  = [aci_filter.terraform_filter_flt-https.id]
    name                          = "https"
}


# Associate the EPG-WEB with the contracts
resource "aci_epg_to_contract" "terraform_one" {
    application_epg_dn = aci_application_epg.web_epg.id
    contract_dn        = aci_contract.terraform_contract_web.id
    contract_type      = "provider"
}

# Associate the EPG-WEB with the contracts
resource "aci_epg_to_contract" "terraform_two" {
    application_epg_dn = aci_application_epg.web_epg.id
    contract_dn        = aci_contract.terraform_contract_sql.id
    contract_type      = "consumer"
}

# Associate the EPG-SQL with the contracts
resource "aci_epg_to_contract" "terraform_three" {
    application_epg_dn = aci_application_epg.db_epg.id
    contract_dn        = aci_contract.terraform_contract_sql.id
    contract_type      = "provider"
}

# Ensure Tenant has L3 external network.
resource "aci_rest" "terraform_l3out" {
    path   = "api/mo/${aci_tenant.terraform_tenant.id}/out-corp_l3.json"
    payload = <<EOF
    {"l3extOut": {"attributes": {"descr":"Created Using Terraform", "name":"corp_l3"}}}
    EOF
}

