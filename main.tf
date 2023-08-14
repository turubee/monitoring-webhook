terraform {
  required_version = "~> 1.5.5"

  backend "s3" {
    bucket = ""
    region = "ap-northeast-1"
    key    = "monitoring-webhook.tfstate"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}
