output "url" {
  description = "apigateway invoke url"
  value       = aws_api_gateway_deployment.this.invoke_url
}

output "execution_arn" {
  value       = aws_api_gateway_deployment.this.execution_arn
}
