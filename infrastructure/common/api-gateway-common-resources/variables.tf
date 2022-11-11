variable "api_gw_name" {
  type        = string
  description = "API Gateway Name"
}

variable "path_parts" {
  type = map(any)
}

variable "cors_handler_lambda" {
  description = "Lambda Function resource for cors handler"
}
