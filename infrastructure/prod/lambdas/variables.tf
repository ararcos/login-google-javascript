variable "create_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "image_tag_lambda" {
  description = "Add aditional permissions to the lambda function"
  type        = string
  default     = "latest"
}
