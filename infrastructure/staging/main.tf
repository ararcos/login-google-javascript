terraform {
  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.9.0"
    }
  
  }
  backend "s3" {
    bucket         = "terraform-test-2-app-state"
    key            = "global/s3/terraform-stg.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}

module "environment" {
  source = "../environment"
  env_suffix = "_stg"
  stage_name = "stage"
}
