variable "name_webhook" {
  description = "Name of webhook"
  default     = "webhook-test"
}

variable "region" {
  description = "Region"
  default     = "ap-northeast-1"
}

variable "path" {
  description = "Name of resource path"
  default     = "/"
}

variable "api_description" {
  description = "Description of API Method"
  default     = ""
}

variable "stage_name" {
  description = "Name of Stage"
  default     = "test"
}
