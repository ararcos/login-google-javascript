module "base_project_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "office_reservation_base"
}

module "create_book_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "create_booking"
}

module "get_book_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "get_booking"
}

module "find_book_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "find_booking"
}

module "update_book_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "update_booking"
}

module "delete_book_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "delete_booking"
}