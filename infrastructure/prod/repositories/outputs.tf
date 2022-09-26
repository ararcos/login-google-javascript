output "base_ecr_ui" {
  value = module.base_project_ECR.ecr_uri_lambda
}

output "create_book_ecr_ui" {
  value = module.create_book_ECR.ecr_uri_lambda
}

# output "get_book_ecr_ui" {
#   value = module.get_book_ECR.ecr_uri_lambda
# }

output "find_book_ecr_ui" {
  value = module.find_book_ECR.ecr_uri_lambda
}

# output "update_book_ecr_ui" {
#   value = module.update_book_ECR.ecr_uri_lambda
# }
output "delete_book_ecr_ui" {
  value = module.delete_book_ECR.ecr_uri_lambda
}
