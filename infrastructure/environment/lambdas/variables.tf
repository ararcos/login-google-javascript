variable "create_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking"
}
variable "get_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for get_booking"
}
variable "find_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_booking"
}
variable "update_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for update_booking"
}
variable "delete_book_ecr_ui" {
  type        = string
  description = "ECR Repository URI for delete_booking"
}
variable "image_tag_lambda" {
  description = "Add tag to the lambda function"
  type        = string
  default     = "latest"
}

variable "myregion" {
  type    = string
  default = "latest"
}

variable "accountId" {
  type    = string
  default = "latest"
}

variable "env_suffix" {
  type    = string
  default = ""
}

variable "stage_name" {
  type    = string
  default = "prod"
}

variable "create_desk_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_desk"
}

variable "find_desk_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_desk"
}

variable "create_office_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_office"
}

variable "find_office_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_office"
}

variable "create_parking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_parking"
}

variable "find_parking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_parking"
}

variable "create_ride_booking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_ride_booking"
}

variable "create_ride_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_ride"
}

variable "find_ride_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_ride"
}
variable "update_ride_ecr_ui" {
  type        = string
  description = "ECR Repository URI for update_ride"
}
variable "delete_ride_ecr_ui" {
  type        = string
  description = "ECR Repository URI for delete_ride"
}

variable "delete_booking_ride_ecr_ui" {
  type        = string
  description = "ECR Repository URI for delete_booking_ride"
}

variable "create_seat_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_seat"
}

variable "find_seat_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_seat"
}

variable "update_seat_ecr_ui" {
  type        = string
  description = "ECR Repository URI for update_seat"
}

variable "delete_seat_ecr_ui" {
  type        = string
  description = "ECR Repository URI for delete_seat"
}

variable "create_user_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_user"
}
variable "get_user_ecr_ui" {
  type        = string
  description = "ECR Repository URI for get_user"
}
variable "find_user_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_user"
}
variable "update_user_ecr_ui" {
  type        = string
  description = "ECR Repository URI for update_user"
}

variable "create_lock_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_lock"
}

variable "find_lock_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_lock"
}

variable "delete_lock_ecr_ui" {
  type        = string
  description = "ECR Repository URI for delete_lock"
}

variable "create_booking_parking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for create_booking_parking"
}

variable "find_booking_parking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for find_booking_parking"
}

variable "delete_booking_parking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for delete_booking_parking"
}

variable "update_booking_parking_ecr_ui" {
  type        = string
  description = "ECR Repository URI for update_booking_parking"
}

variable "cors_handler_ecr_ui" {
  type        = string
  description = "ECR Repository URI for cors_handler"
}

variable "origin" {
  type        = string
  description = "origin URL"
}

variable "ride_reminder_ecr_ui" {
  type        = string
  description = "ECR Repository URI for ride_reminder"
}