module "create_ECR" {
  source   = "./common/ecr_lambda"
  ecr_name = "office_reservation_base_with_terraform2"
}
