module "repositories" {
  source     = "./repositories"
  env_suffix = var.env_suffix
}

module "lambdas" {
  source                        = "./lambdas"
  create_book_ecr_ui            = module.repositories.create_book_ecr_ui
  image_tag_lambda              = var.IMAGE_TAG
  find_book_ecr_ui              = module.repositories.find_book_ecr_ui
  delete_book_ecr_ui            = module.repositories.delete_book_ecr_ui
  update_book_ecr_ui            = module.repositories.update_book_ecr_ui
  get_book_ecr_ui               = module.repositories.get_book_ecr_ui
  create_desk_ecr_ui            = module.repositories.create_desk_ecr_ui
  find_desk_ecr_ui              = module.repositories.find_desk_ecr_ui
  create_office_ecr_ui          = module.repositories.create_office_ecr_ui
  find_office_ecr_ui            = module.repositories.find_office_ecr_ui
  create_parking_ecr_ui         = module.repositories.create_parking_ecr_ui
  find_parking_ecr_ui           = module.repositories.find_parking_ecr_ui
  create_ride_booking_ecr_ui    = module.repositories.create_ride_booking_ecr_ui
  create_ride_ecr_ui            = module.repositories.create_ride_ecr_ui
  find_ride_ecr_ui              = module.repositories.find_ride_ecr_ui
  update_ride_ecr_ui            = module.repositories.update_ride_ecr_ui
  delete_ride_ecr_ui            = module.repositories.delete_ride_ecr_ui
  delete_booking_ride_ecr_ui    = module.repositories.delete_booking_ride_ecr_ui
  create_seat_ecr_ui            = module.repositories.create_seat_ecr_ui
  find_seat_ecr_ui              = module.repositories.find_seat_ecr_ui
  update_seat_ecr_ui            = module.repositories.update_seat_ecr_ui
  delete_seat_ecr_ui            = module.repositories.delete_seat_ecr_ui
  create_user_ecr_ui            = module.repositories.create_user_ecr_ui
  get_user_ecr_ui               = module.repositories.get_user_ecr_ui
  find_user_ecr_ui              = module.repositories.find_user_ecr_ui
  update_user_ecr_ui            = module.repositories.update_user_ecr_ui
  create_lock_ecr_ui            = module.repositories.create_lock_ecr_ui
  find_lock_ecr_ui              = module.repositories.find_lock_ecr_ui
  delete_lock_ecr_ui            = module.repositories.delete_lock_ecr_ui
  create_booking_parking_ecr_ui = module.repositories.create_booking_parking_ecr_ui
  find_booking_parking_ecr_ui   = module.repositories.find_booking_parking_ecr_ui
  delete_booking_parking_ecr_ui = module.repositories.delete_booking_parking_ecr_ui
  update_booking_parking_ecr_ui = module.repositories.update_booking_parking_ecr_ui
  cors_handler_ecr_ui           = module.repositories.cors_handler_ecr_ui
  origin                        = var.origin
  env_suffix                    = var.env_suffix
  stage_name                    = var.stage_name
  ride_reminder_ecr_ui         = module.repositories.ride_reminder_ecr_ui
}

module "kms" {
  source   = "../common/kms"
  key_name = var.stage_name
  key_admins = [
    "arn:aws:iam::808666875322:user/botGithub"
  ]
  key_users = var.key_users
}
