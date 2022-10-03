resource "aws_api_gateway_rest_api" "rest-api" {
  name = var.api_gw_name
}

resource "aws_api_gateway_resource" "api-gw-root" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  parent_id   = aws_api_gateway_rest_api.rest-api.root_resource_id
  path_part   = var.path_part
}

resource "aws_api_gateway_resource" "api-gw" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  parent_id   = aws_api_gateway_resource.api-gw-root.id
  path_part   = "{${var.param_name}+}"
}

resource "aws_api_gateway_method" "api-gw-method" {
  rest_api_id   = aws_api_gateway_rest_api.rest-api.id
  resource_id   = aws_api_gateway_resource.api-gw.id
  http_method   = var.method
  authorization = "NONE"
}
#booking/
resource "aws_api_gateway_integration" "api-gw-integration" {
  content_handling        = "CONVERT_TO_TEXT"
  rest_api_id             = aws_api_gateway_rest_api.rest-api.id
  resource_id             = aws_api_gateway_resource.api-gw.id
  http_method             = aws_api_gateway_method.api-gw-method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.lambda.invoke_arn
  passthrough_behavior = "WHEN_NO_TEMPLATES"
  request_templates = {
    "application/json" = <<EOF
    #set($allParams = $input.params())
    {
      "pathParameters": {
              "${var.param_name}":"$input.params('${var.param_name}')"
      },
    "queryStringParameters": {
        #foreach($paramName in $allParams.querystring.keySet())
        "$paramName" : "$util.escapeJavaScript($allParams.querystring.get($paramName))"
        #if($foreach.hasNext),#end
        #end
        }
    }
    EOF
}
}

resource "aws_api_gateway_method_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.rest-api.id
  resource_id = aws_api_gateway_resource.api-gw.id
  http_method = aws_api_gateway_method.api-gw-method.http_method
  status_code = "200"
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