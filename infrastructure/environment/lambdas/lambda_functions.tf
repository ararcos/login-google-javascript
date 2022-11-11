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
  source      = "../../common/lambda"
  ecr_uri     = var.get_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "get_booking_role${var.env_suffix}"
  func_name   = "get_booking_controller${var.env_suffix}"
  source_arn  = "${module.get_booking_api.api_arn}/*/GET/bookings/*"
}

module "find_booking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_booking_role${var.env_suffix}"
  func_name   = "find_booking_controller${var.env_suffix}"
}

module "update_booking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.update_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "update_booking_role${var.env_suffix}"
  func_name   = "update_booking_controller${var.env_suffix}"
}

module "delete_booking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.delete_book_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_booking_role${var.env_suffix}"
  func_name   = "delete_booking_controller${var.env_suffix}"
}

module "create_desk_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_desk_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_desk_role${var.env_suffix}"
  func_name   = "create_desk_controller${var.env_suffix}"
}

module "find_desk_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_desk_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_desk_role${var.env_suffix}"
  func_name   = "find_desk_controller${var.env_suffix}"
}

module "create_office_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_office_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_office_role${var.env_suffix}"
  func_name   = "create_office_controller${var.env_suffix}"
}

module "find_office_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_office_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_office_role${var.env_suffix}"
  func_name   = "find_office_controller${var.env_suffix}"
}

module "create_parking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_parking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_parking_role${var.env_suffix}"
  func_name   = "create_parking_controller${var.env_suffix}"
}

module "find_parking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_parking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_parking_role${var.env_suffix}"
  func_name   = "find_parking_controller${var.env_suffix}"
}

module "create_ride_booking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_ride_booking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_ride_booking_role${var.env_suffix}"
  func_name   = "create_ride_booking_controller${var.env_suffix}"
}

module "create_ride_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_ride_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_ride_role${var.env_suffix}"
  func_name   = "create_ride_controller${var.env_suffix}"
}

module "find_ride_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_ride_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_ride_role${var.env_suffix}"
  func_name   = "find_ride_controller${var.env_suffix}"
}

module "update_ride_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.update_ride_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "update_ride_role${var.env_suffix}"
  func_name   = "update_ride_controller${var.env_suffix}"
}

module "delete_ride_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.delete_ride_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_ride_role${var.env_suffix}"
  func_name   = "delete_ride_controller${var.env_suffix}"
}

module "delete_booking_ride_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.delete_booking_ride_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_booking_ride_role${var.env_suffix}"
  func_name   = "delete_booking_ride_controller${var.env_suffix}"
}


module "create_seat_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_seat_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_seat_role${var.env_suffix}"
  func_name   = "create_seat_controller${var.env_suffix}"
}

module "find_seat_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_seat_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_seat_role${var.env_suffix}"
  func_name   = "find_seat_controller${var.env_suffix}"
}

module "update_seat_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.update_seat_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "update_seat_role${var.env_suffix}"
  func_name   = "update_seat_controller${var.env_suffix}"
}

module "delete_seat_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.delete_seat_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_seat_role${var.env_suffix}"
  func_name   = "delete_seat_controller${var.env_suffix}"
}


module "create_user_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_user_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_user_role${var.env_suffix}"
  func_name   = "create_user_controller${var.env_suffix}"
}


module "get_user_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.get_user_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "get_user_role${var.env_suffix}"
  func_name   = "get_user_controller${var.env_suffix}"
  source_arn  = "${module.get_user_api.api_arn}/*/GET/users/*"
}

module "find_user_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_user_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_user_role${var.env_suffix}"
  func_name   = "find_user_controller${var.env_suffix}"
  env_variables = [{
    HEADERS        = "Content-Type,authorization,contenttype,Access-Control-Allow-Origin"
    ALLOWED_ORIGIN = var.origin
    METHODS        = "GET,POST,PATCH,DELETE"
  }]
}

module "update_user_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.update_user_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "update_user_role${var.env_suffix}"
  func_name   = "update_user_controller${var.env_suffix}"
}

module "create_lock_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_lock_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_lock_role${var.env_suffix}"
  func_name   = "create_lock_controller${var.env_suffix}"
}

module "find_lock_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_lock_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_lock_role${var.env_suffix}"
  func_name   = "find_lock_controller${var.env_suffix}"
}

module "delete_lock_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.delete_lock_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_lock_role${var.env_suffix}"
  func_name   = "delete_lock_controller${var.env_suffix}"
}

module "create_booking_parking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.create_booking_parking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "create_booking_parking_role${var.env_suffix}"
  func_name   = "create_booking_parking_controller${var.env_suffix}"
}

module "find_booking_parking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.find_booking_parking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "find_booking_parking_role${var.env_suffix}"
  func_name   = "find_booking_parking_controller${var.env_suffix}"
}

module "delete_booking_parking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.delete_booking_parking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "delete_booking_parking_role${var.env_suffix}"
  func_name   = "delete_booking_parking_controller${var.env_suffix}"
}

module "update_booking_parking_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.update_booking_parking_ecr_ui
  tag         = var.image_tag_lambda
  timeout     = 15
  memory_size = 512
  role_name   = "update_booking_parking_role${var.env_suffix}"
  func_name   = "update_booking_parking_controller${var.env_suffix}"
}

module "cors_handler_lambda" {
  source      = "../../common/lambda"
  ecr_uri     = var.cors_handler_ecr_ui
  tag         = "latest"
  timeout     = 15
  memory_size = 128
  role_name   = "cors_handler_role${var.env_suffix}"
  func_name   = "cors_handler_controller${var.env_suffix}"
  env_variables = [{
    HEADERS        = "Content-Type,authorization,contenttype,Access-Control-Allow-Origin"
    ALLOWED_ORIGIN = var.origin
    METHODS        = "GET,POST,PATCH,DELETE"
  }]
}

module "ride_reminder_lambda" {
  source        = "../../common/lambda-schedule"
  ecr_uri       = var.ride_reminder_ecr_ui
  tag           = var.image_tag_lambda
  timeout       = 15
  memory_size   = 512
  role_name     = "ride_reminder_role${var.env_suffix}"
  func_name     = "ride_reminder_controller${var.env_suffix}"
  schedule      = "cron(0/5 * * * ? *)"
  schedule_name = "ride_reminder_schedule${var.env_suffix}"
}
