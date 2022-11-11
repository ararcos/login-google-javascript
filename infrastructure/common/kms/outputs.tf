
output "kms_key" {
  value = resource.aws_kms_key.kms_key
}

output "kms_alias" {
  value = resource.aws_kms_alias.kms_alias
}
