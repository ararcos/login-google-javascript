variable "api_gw_name" {
  type        = string
  description = "API Gateway Name"
}

variable "path_part" {
  type = string
}

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
  type = string
  default = ""
}
