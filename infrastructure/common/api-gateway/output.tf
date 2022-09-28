output "selected" {
  value = aws_api_gateway_rest_api.rest-api.id
}

output "api_method" {
  value = aws_api_gateway_method.api-gw-method.http_method
}

output "api_path" {
  value = aws_api_gateway_resource.api-gw.path
}

output "api_arn" {
  value = aws_api_gateway_rest_api.rest-api.execution_arn
}