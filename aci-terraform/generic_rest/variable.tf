variable "user" {
  description = "Login information"
  type        = map
  default     = {
    username = "admin"
    password = "C1sco12345"
    url      = "https://10.10.20.14"
  }
}
variable "tenant" {
    type    = string
    default = "abc-tenant"
}
variable "l3out" {
    type    = object({
        name    = string
        description = string
    })
    default = {
        name    = "corp_l3"
        description = "Created Using Terraform"
    }
}
