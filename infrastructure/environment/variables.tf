variable "IMAGE_TAG" {
  description = "Add aditional permissions to the lambda function"
  type        = string
  default     = "latest"
}

variable "env_suffix" {
  type        = string
  default     = ""
}

variable "stage_name" {
  type        = string
  default     = "prod"
}
