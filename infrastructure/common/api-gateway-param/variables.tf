variable "lambda" {
  description = "Lambda Function resource"
}


variable "stage_name" {
  type = string
}

variable "method" {
  type = string
}

variable "param_name" {
  type    = string
  default = ""
}

variable "aws_api_gateway_rest_api" {}

variable "path_part" {
  type = string
}

variable "aws_api_gateway_resource_param" {
  default = ""
}
