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