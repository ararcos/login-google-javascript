output "selected" {
  value = var.aws_api_gateway_rest_api.id
}

output "api_method" {
  value = aws_api_gateway_method.api-gw-method.http_method
}

output "api_path" {
  value = var.aws_api_gateway_resource[var.path_part].path
}

output "api_arn" {
  value = var.aws_api_gateway_rest_api.execution_arn
}
