variable "ecr_uri" {
  type = string
}

variable "tag" {
  type = string
}

variable "timeout" {
  type = number
}

variable "memory_size" {
  type = number
}

variable "role_name" {
  type = string
}

variable "func_name" {
  type = string
}

variable "permissions" {
  description = "Add aditional permissions to the lambda function"
  default     = []
}

variable "env_variables" {
  default = []
}

variable "schedule" {
  type    = string
  default = "cron(00 13 * * ? *)"
}

variable "schedule_name" {
  type    = string
}
