resource "aws_api_gateway_rest_api" "rest-api" {
  name = var.api_gw_name
}

resource "aws_api_gateway_resource" "api-gw" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  parent_id   = aws_api_gateway_rest_api.rest-api.root_resource_id
  path_part   = var.path_part
}

resource "aws_api_gateway_method" "api-gw-method" {
  rest_api_id   = aws_api_gateway_rest_api.rest-api.id
  resource_id   = aws_api_gateway_resource.api-gw.id
  http_method   = var.method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api-gw-integration" {
  content_handling        = "CONVERT_TO_TEXT"
  rest_api_id             = aws_api_gateway_rest_api.rest-api.id
  resource_id             = aws_api_gateway_resource.api-gw.id
  http_method             = aws_api_gateway_method.api-gw-method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.lambda.invoke_arn
}

resource "aws_api_gateway_method_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  resource_id = aws_api_gateway_resource.api-gw.id
  http_method = aws_api_gateway_method.api-gw-method.http_method
  status_code = "200"
  response_models     = {"application/json" = "Empty"}
}

resource "aws_api_gateway_integration_response" "IntegrationResponse" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  resource_id = aws_api_gateway_resource.api-gw.id
  http_method = aws_api_gateway_method.api-gw-method.http_method
  status_code = aws_api_gateway_method_response.response_200.status_code
  depends_on = [
    aws_api_gateway_integration.api-gw-integration
  ]

}


resource "aws_api_gateway_deployment" "api-gw-deployment" {
  depends_on = [
    aws_api_gateway_integration.api-gw-integration,
    aws_api_gateway_integration_response.IntegrationResponse
  ]
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  stage_name  = var.stage_name

  # triggers = {
  #   redeployment = sha1(jsonencode([
  #     aws_api_gateway_resource.api-gw.id,
  #     aws_api_gateway_method.api-gw-method.id,
  #     aws_api_gateway_integration.api-gw-integration.id,
  #   ]))
  # }
  
}