module "base_project_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "office_reservation_base${var.env_suffix}"
}

module "create_book_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_booking${var.env_suffix}"
}

module "get_book_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "get_booking${var.env_suffix}"
}

module "find_book_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_booking${var.env_suffix}"
}

module "update_book_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "update_booking${var.env_suffix}"
}

module "delete_book_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "delete_booking${var.env_suffix}"
}

module "create_desk_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_desk${var.env_suffix}"
}

module "find_desk_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_desk${var.env_suffix}"
}

module "create_office_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_office${var.env_suffix}"
}

module "find_office_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_office${var.env_suffix}"
}
module "create_parking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_parking${var.env_suffix}"
}

module "find_parking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_parking${var.env_suffix}"
}

module "create_ride_booking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_ride_booking${var.env_suffix}"
}

module "create_ride_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_ride${var.env_suffix}"
}

module "find_ride_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_ride${var.env_suffix}"
}

module "update_ride_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "update_ride${var.env_suffix}"
}

module "delete_ride_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "delete_ride${var.env_suffix}"
}

module "delete_booking_ride_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "delete_booking_ride${var.env_suffix}"
}

module "create_seat_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_seat${var.env_suffix}"
}

module "find_seat_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_seat${var.env_suffix}"
}

module "update_seat_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "update_seat${var.env_suffix}"
}

module "delete_seat_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "delete_seat${var.env_suffix}"
}

module "create_user_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_user${var.env_suffix}"
}

module "get_user_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "get_user${var.env_suffix}"
}

module "find_user_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_user${var.env_suffix}"
}

module "update_user_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "update_user${var.env_suffix}"
}

module "create_lock_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_lock${var.env_suffix}"
}

module "delete_lock_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "delete_lock${var.env_suffix}"
}

module "find_lock_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_lock${var.env_suffix}"
}

module "create_booking_parking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "create_booking_parking${var.env_suffix}"
}

module "delete_booking_parking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "delete_booking_parking${var.env_suffix}"
}

module "find_booking_parking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "find_booking_parking${var.env_suffix}"
}

module "update_booking_parking_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "update_booking_parking${var.env_suffix}"
}

module "cors_handler_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "cors_handler${var.env_suffix}"
}

module "ride_reminder_ECR" {
  source   = "../../common/ecr_lambda"
  ecr_name = "ride_reminder${var.env_suffix}"
}
