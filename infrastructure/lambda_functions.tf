module "create_booking_lambda" {
  source      = "./common/lambda"
  ecr_uri     = module.create_book_ECR.ecr_uri_lambda
  tag         = var.IMAGE_TAG
  timeout     = 15
  memory_size = 512
  role_name   = "create_booking_role"
  func_name   = "create_booking_controller"
}
