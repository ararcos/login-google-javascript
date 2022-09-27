terraform {
  backend "s3" {
    bucket         = "terraform-test-2-app-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}