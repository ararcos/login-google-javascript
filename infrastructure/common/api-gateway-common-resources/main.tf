resource "aws_api_gateway_rest_api" "rest-api" {
  name = var.api_gw_name
}

resource "aws_api_gateway_resource" "api-gw" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  parent_id   = aws_api_gateway_rest_api.rest-api.root_resource_id
  for_each    = var.path_parts
  path_part   = each.key
}

resource "aws_api_gateway_resource" "api-gw-param" {
  for_each    = var.path_parts
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  parent_id   = aws_api_gateway_resource.api-gw[each.key].id
  path_part   = "{${each.value}+}"
}

resource "aws_api_gateway_method" "api-gw-method-cors" {
  for_each    = var.path_parts
  rest_api_id   = aws_api_gateway_rest_api.rest-api.id
  resource_id   = aws_api_gateway_resource.api-gw[each.key].id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "api-gw-method-param-cors" {
  for_each    = var.path_parts
  rest_api_id   = aws_api_gateway_rest_api.rest-api.id
  resource_id   = aws_api_gateway_resource.api-gw-param[each.key].id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api-gw-integration-cors" {
  for_each    = var.path_parts
  rest_api_id             = aws_api_gateway_rest_api.rest-api.id
  resource_id             = aws_api_gateway_resource.api-gw[each.key].id
  http_method             = aws_api_gateway_method.api-gw-method-cors[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.cors_handler_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "api-gw-integration-param-cors" {
  for_each    = var.path_parts
  rest_api_id             = aws_api_gateway_rest_api.rest-api.id
  resource_id             = aws_api_gateway_resource.api-gw-param[each.key].id
  http_method             = aws_api_gateway_method.api-gw-method-cors[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.cors_handler_lambda.invoke_arn
}

resource "aws_api_gateway_method_response" "response_200-cors" {
  for_each    = var.path_parts
  rest_api_id     = aws_api_gateway_rest_api.rest-api.id
  resource_id     = aws_api_gateway_resource.api-gw[each.key].id
  http_method     = aws_api_gateway_method.api-gw-method-cors[each.key].http_method
  status_code     = "200"
  response_models = { "application/json" = "Empty" }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Methods" = true
  }
}

resource "aws_api_gateway_method_response" "response_200-param-cors" {
  for_each    = var.path_parts
  rest_api_id     = aws_api_gateway_rest_api.rest-api.id
  resource_id     = aws_api_gateway_resource.api-gw-param[each.key].id
  http_method     = aws_api_gateway_method.api-gw-method-cors[each.key].http_method
  status_code     = "200"
  response_models = { "application/json" = "Empty" }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Methods" = true
  }
}

resource "aws_api_gateway_integration_response" "IntegrationResponse-cors" {
  for_each    = var.path_parts
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  resource_id = aws_api_gateway_resource.api-gw[each.key].id
  http_method = aws_api_gateway_method.api-gw-method-cors[each.key].http_method
  status_code = aws_api_gateway_method_response.response_200-cors[each.key].status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "integration.response.body.headers.Access-Control-Allow-Headers"
    "method.response.header.Access-Control-Allow-Origin" = "integration.response.body.headers.Access-Control-Allow-Origin"
    "method.response.header.Access-Control-Allow-Methods" = "integration.response.body.headers.Access-Control-Allow-Methods"
  }
}

resource "aws_api_gateway_integration_response" "IntegrationResponse-param-cors" {
  for_each    = var.path_parts
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  resource_id = aws_api_gateway_resource.api-gw-param[each.key].id
  http_method = aws_api_gateway_method.api-gw-method-param-cors[each.key].http_method
  status_code = aws_api_gateway_method_response.response_200-param-cors[each.key].status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "integration.response.body.headers.Access-Control-Allow-Headers"
    "method.response.header.Access-Control-Allow-Origin" = "integration.response.body.headers.Access-Control-Allow-Origin"
    "method.response.header.Access-Control-Allow-Methods" = "integration.response.body.headers.Access-Control-Allow-Methods"
  }
}
