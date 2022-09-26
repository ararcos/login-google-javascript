module "create_booking_api" {
  source        = "../../common/api-gateway"
  api_gw_name   = "create_booking"
  method        = "POST"
  path_part     = "booking"
  lambda        = module.create_booking_lambda.function
  stage_name    = "prod"
  #domain_name   = "www.ioet-desk-reservation.com/createbooking"
}

# module "get_booking_api" {
#   source        = "../../common/api-gateway"
#   api_gw_name   = "get_booking"
#   method        = "GET"
#   path_part     = "booking"
#   lambda        = module.get_booking_lambda.function
#   stage_name    = "prod"
#   #domain_name   = "www.ioet-desk-reservation.com/createbooking"
# }

module "find_booking_api" {
  source        = "../../common/api-gateway"
  api_gw_name   = "find_booking"
  method        = "GET"
  path_part     = "booking"
  lambda        = module.find_booking_lambda.function
  stage_name    = "prod"
  #domain_name   = "www.ioet-desk-reservation.com/createbooking"
}

# module "update_booking_api" {
#   source        = "../../common/api-gateway"
#   api_gw_name   = "update_booking"
#   method        = "PATCH"
#   path_part     = "booking"
#   lambda        = module.update_booking_lambda.function
#   stage_name    = "prod"
#   #domain_name   = "www.ioet-desk-reservation.com/createbooking"
# }

# module "delete_booking_api" {
#   source        = "../../common/api-gateway"
#   api_gw_name   = "delete_booking"
#   method        = "DELETE"
#   path_part     = "booking"
#   lambda        = module.delete_booking_lambda.function
#   stage_name    = "prod"
#   #domain_name   = "www.ioet-desk-reservation.com/createbooking"
# }