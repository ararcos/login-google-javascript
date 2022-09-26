output "base_ecr_ui" {
  value = module.base_project_ECR.ecr_uri_lambda
}

output "create_book_ecr_ui" {
  value = module.create_book_ECR.ecr_uri_lambda
}
