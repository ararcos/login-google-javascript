module "create_booking_api" {
  source        = "../../common/api-gateway"
  api_gw_name   = "create_booking${var.env_suffix}"
  method        = "POST"
  path_part     = "booking"
  lambda        = module.create_booking_lambda.function
  stage_name    = var.stage_name
}

module "get_booking_api" {
  source        = "../../common/api-gateway-param"
  param_name    = "booking_id"
  api_gw_name   = "get_booking${var.env_suffix}"
  method        = "GET"
  path_part     = "booking"
  lambda        = module.get_booking_lambda.function
  stage_name    = var.stage_name
}

module "find_booking_api" {
  source        = "../../common/api-gateway-query"
  api_gw_name   = "find_booking${var.env_suffix}"
  method        = "GET"
  path_part     = "booking"
  lambda        = module.find_booking_lambda.function
  stage_name    = var.stage_name
}

module "update_booking_api" {
  source        = "../../common/api-gateway"
  api_gw_name   = "update_booking${var.env_suffix}"
  method        = "PATCH"
  path_part     = "booking"
  lambda        = module.update_booking_lambda.function
  stage_name    = var.stage_name
}

module "delete_booking_api" {
  source        = "../../common/api-gateway"
  api_gw_name   = "delete_booking${var.env_suffix}"
  method        = "DELETE"
  path_part     = "booking"
  lambda        = module.delete_booking_lambda.function
  stage_name    = var.stage_name
}