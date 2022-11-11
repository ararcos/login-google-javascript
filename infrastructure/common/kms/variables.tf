
variable "key_name" {
  type        = string
  description = "KMS Key Name (Alias)"
}

variable "key_description" {
  type        = string
  description = "KMS Key Description"
  default     = "KMS Key created by Terraform"
}

variable "key_admins" {
  type        = list(string)
  description = "KMS Key Admins"
  default = [
    # These commented values are here to give an example of how KMS keys should be placed, but terraform does not allow us to put a data here.
    #"arn:aws:iam::${data.aws_caller_identity.current_user.account_id}:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AWSAdministratorAccess_*"
    "arn:aws:iam::*:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AWSAdministratorAccess_*"
  ]
}

variable "key_users" {
  type        = list(string)
  description = "KMS Key Users"
  default = [
    # These commented values are here to give an example of how KMS keys should be placed, but terraform does not allow us to put a data here.
    #"arn:aws:iam::${data.aws_caller_identity.current_user.account_id}:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_KMSUsers_*"
    "arn:aws:iam::*:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_KMSUsers_*"
  ]
}
