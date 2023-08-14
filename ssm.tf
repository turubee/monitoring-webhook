resource "aws_ssm_parameter" "backlog_api_key" {
  name        = "/backlog/api_key"
  description = "API_KEY of backlog"
  type        = "SecureString"
  value       = "dummy"
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "backlog_project_id" {
  name        = "/backlog/project_id"
  description = "API_KEY of backlog"
  type        = "SecureString"
  value       = "dummy"
  lifecycle {
    ignore_changes = [value]
  }
}
