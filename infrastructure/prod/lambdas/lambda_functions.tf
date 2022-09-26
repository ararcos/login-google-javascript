module "create_booking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_booking_role"
  func_name   = "create_booking_controller"
}

# module "get_booking_lambda" {
#   source = "../../common/lambda"
#   ecr_uri     = module.get_book_ECR.ecr.repository_url
#   tag         = var.IMAGE_TAG
#   timeout     = 15
#   memory_size = 512
#   role_name   = "get_booking_role"
#   func_name   = "get_booking_controller"
# }

module "find_booking_lambda" {
  source = "../../common/lambda"
  ecr_uri     = var.create_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_booking_role"
  func_name   = "find_booking_controller"
}

# module "update_booking_lambda" {
#   source = "../../common/lambda"
#   ecr_uri     = var.create_book_ecr_ui
#   tag         = var.image_tag_lambda
#   timeout     = 15
#   memory_size = 512
#   role_name   = "update_booking_role"
#   func_name   = "update_booking_controller"
# }

module "delete_booking_lambda" {
  source = "../../common/lambda"
  ecr_uri     = var.create_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_booking_role"
  func_name   = "delete_booking_controller"
}