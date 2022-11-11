module "api-base" {
  source      = "../../common/api-gateway-common-resources"
  api_gw_name = "backend${var.env_suffix}"
  path_parts = {
    bookings         = "booking_id"
    desks            = "desk_id"
    offices           = "office_id"
    parkings         = "parking_id"
    rides-booking    = "rides-booking_id"
    rides            = "ride_id"
    seats            = "seat_id"
    users            = "user_id"
    lock-bookings    = "lock-booking_id"
    parking-bookings = "parking-bookings"
  }
  cors_handler_lambda      = module.cors_handler_lambda.function
}

module "create_booking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_booking_lambda.function
  stage_name               = var.stage_name
  path_part                = "bookings"
}

module "get_booking_api" {
  source                         = "../../common/api-gateway-param"
  param_name                     = "booking_id"
  aws_api_gateway_rest_api       = module.api-base.aws_api_gateway_rest_api
  method                         = "GET"
  aws_api_gateway_resource_param = module.api-base.aws_api_gateway_resource_param
  lambda                         = module.get_booking_lambda.function
  stage_name                     = var.stage_name
  path_part                      = "bookings"
}

module "find_booking_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_booking_lambda.function
  stage_name               = var.stage_name
  path_part                = "bookings"
}

module "update_booking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "PATCH"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.update_booking_lambda.function
  stage_name               = var.stage_name
  path_part                = "bookings"
}

module "delete_booking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "DELETE"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.delete_booking_lambda.function
  stage_name               = var.stage_name
  path_part                = "bookings"
}

module "create_desk_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_desk_lambda.function
  stage_name               = var.stage_name
  path_part                = "desks"
}

module "find_desk_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_desk_lambda.function
  stage_name               = var.stage_name
  path_part                = "desks"
}

module "create_office_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_office_lambda.function
  stage_name               = var.stage_name
  path_part                = "offices"
}

module "find_office_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_office_lambda.function
  stage_name               = var.stage_name
  path_part                = "offices"
}

module "create_parking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_parking_lambda.function
  stage_name               = var.stage_name
  path_part                = "parkings"
}

module "find_parking_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_parking_lambda.function
  stage_name               = var.stage_name
  path_part                = "parkings"
}

module "create_ride_booking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_ride_booking_lambda.function
  stage_name               = var.stage_name
  path_part                = "rides-booking"
}

module "create_ride_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_ride_lambda.function
  stage_name               = var.stage_name
  path_part                = "rides"
}

module "find_ride_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_ride_lambda.function
  stage_name               = var.stage_name
  path_part                = "rides"
}

module "update_ride_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "PATCH"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.update_ride_lambda.function
  stage_name               = var.stage_name
  path_part                = "rides"
}

module "delete_ride_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "DELETE"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.delete_ride_lambda.function
  stage_name               = var.stage_name
  path_part                = "rides"
}

module "delete_booking_ride_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "DELETE"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.delete_booking_ride_lambda.function
  stage_name               = var.stage_name
  path_part                = "rides-booking"
}

module "create_seat_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_seat_lambda.function
  stage_name               = var.stage_name
  path_part                = "seats"
}

module "find_seat_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_seat_lambda.function
  stage_name               = var.stage_name
  path_part                = "seats"
}

module "update_seat_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "PATCH"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.update_seat_lambda.function
  stage_name               = var.stage_name
  path_part                = "seats"
}

module "delete_seat_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "DELETE"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.delete_seat_lambda.function
  stage_name               = var.stage_name
  path_part                = "seats"
}

module "create_user_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_user_lambda.function
  stage_name               = var.stage_name
  path_part                = "users"
}

module "get_user_api" {
  source                         = "../../common/api-gateway-param"
  param_name                     = "user_id"
  aws_api_gateway_rest_api       = module.api-base.aws_api_gateway_rest_api
  method                         = "GET"
  aws_api_gateway_resource_param = module.api-base.aws_api_gateway_resource_param
  lambda                         = module.get_user_lambda.function
  stage_name                     = var.stage_name
  path_part                      = "users"
}

module "find_user_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_user_lambda.function
  stage_name               = var.stage_name
  path_part                = "users"
}

module "update_user_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "PATCH"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.update_user_lambda.function
  stage_name               = var.stage_name
  path_part                = "users"
}

module "create_lock_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_lock_lambda.function
  stage_name               = var.stage_name
  path_part                = "lock-bookings"
}

module "find_lock_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_lock_lambda.function
  stage_name               = var.stage_name
  path_part                = "lock-bookings"
}

module "delete_lock_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "DELETE"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.delete_lock_lambda.function
  stage_name               = var.stage_name
  path_part                = "lock-bookings"
}

module "create_booking_parking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "POST"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.create_booking_parking_lambda.function
  stage_name               = var.stage_name
  path_part                = "parking-bookings"
}

module "find_booking_parking_api" {
  source                   = "../../common/api-gateway-query"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "GET"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.find_booking_parking_lambda.function
  stage_name               = var.stage_name
  path_part                = "parking-bookings"
}

module "delete_booking_parking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "DELETE"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.delete_booking_parking_lambda.function
  stage_name               = var.stage_name
  path_part                = "parking-bookings"
}

module "update_booking_parking_api" {
  source                   = "../../common/api-gateway"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  method                   = "PATCH"
  aws_api_gateway_resource = module.api-base.aws_api_gateway_resource
  lambda                   = module.update_booking_parking_lambda.function
  stage_name               = var.stage_name
  path_part                = "parking-bookings"
}

module "api-gw-deployment" {
  source                   = "../../common/api-gateway-deployment"
  aws_api_gateway_rest_api = module.api-base.aws_api_gateway_rest_api
  stage_name               = var.stage_name
  modules = [
    module.api-base,
    module.create_booking_api,
    module.get_booking_api,
    module.find_booking_api,
    module.update_booking_api,
    module.delete_booking_api,
    module.create_desk_api,
    module.find_desk_api,
    module.create_office_api,
    module.find_office_api,
    module.create_parking_api,
    module.find_parking_api,
    module.create_ride_booking_api,
    module.create_ride_api,
    module.find_ride_api,
    module.update_ride_api,
    module.delete_ride_api,
    module.delete_booking_ride_api,
    module.create_seat_api,
    module.find_seat_api,
    module.update_seat_api,
    module.delete_seat_api,
    module.create_user_api,
    module.get_user_api,
    module.find_user_api,
    module.update_user_api,
    module.create_lock_api,
    module.find_lock_api,
    module.delete_lock_api,
    module.create_booking_parking_api,
    module.find_booking_parking_api,
    module.delete_booking_parking_api,
    module.update_booking_parking_api,
    module.create_booking_lambda,
    module.get_booking_lambda,
    module.find_booking_lambda,
    module.update_booking_lambda,
    module.delete_booking_lambda,
    module.create_desk_lambda,
    module.find_desk_lambda,
    module.create_office_lambda,
    module.find_office_lambda,
    module.create_parking_lambda,
    module.find_parking_lambda,
    module.create_ride_booking_lambda,
    module.create_ride_lambda,
    module.find_ride_lambda,
    module.update_ride_lambda,
    module.delete_ride_lambda,
    module.delete_booking_ride_lambda,
    module.create_seat_lambda,
    module.find_seat_lambda,
    module.update_seat_lambda,
    module.delete_seat_lambda,
    module.create_user_lambda,
    module.get_user_lambda,
    module.find_user_lambda,
    module.update_user_lambda,
    module.create_lock_lambda,
    module.find_lock_lambda,
    module.delete_lock_lambda,
    module.create_booking_parking_lambda,
    module.find_booking_parking_lambda,
    module.delete_booking_parking_lambda,
    module.update_booking_parking_lambda,
    module.cors_handler_lambda.function
  ]
}
