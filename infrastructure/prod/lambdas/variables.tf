variable "create_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "get_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "find_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "update_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "delete_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "image_tag_lambda" {
  description = "Add tag to the lambda function"
  type        = string
  default     = "latest"
}
