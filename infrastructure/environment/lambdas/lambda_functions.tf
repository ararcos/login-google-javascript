module "create_booking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_booking_role${var.env_suffix}"
  func_name   = "create_booking_controller${var.env_suffix}"
}


module "get_booking_lambda" {
  source = "../../common/lambda"
  ecr_uri     = var.get_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "get_booking_role${var.env_suffix}"
  func_name   = "get_booking_controller${var.env_suffix}"
  source_arn  = "${module.get_booking_api.api_arn}/*/GET/booking/*"
}

module "find_booking_lambda" {
  source = "../../common/lambda"
  ecr_uri     = var.find_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_booking_role${var.env_suffix}"
  func_name   = "find_booking_controller${var.env_suffix}"
}

module "update_booking_lambda" {
  source = "../../common/lambda"
  ecr_uri     = var.update_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "update_booking_role${var.env_suffix}"
  func_name   = "update_booking_controller${var.env_suffix}"
}

module "delete_booking_lambda" {
  source = "../../common/lambda"
  ecr_uri     = var.delete_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_booking_role${var.env_suffix}"
  func_name   = "delete_booking_controller${var.env_suffix}"
}