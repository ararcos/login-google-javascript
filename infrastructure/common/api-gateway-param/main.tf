resource "aws_api_gateway_method" "api-gw-method" {
  rest_api_id   = var.aws_api_gateway_rest_api.id
  resource_id   = var.aws_api_gateway_resource_param[var.path_part].id
  http_method   = var.method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api-gw-integration" {
  content_handling        = "CONVERT_TO_TEXT"
  rest_api_id             = var.aws_api_gateway_rest_api.id
  resource_id             = var.aws_api_gateway_resource_param[var.path_part].id
  http_method             = aws_api_gateway_method.api-gw-method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.lambda.invoke_arn
  passthrough_behavior    = "WHEN_NO_TEMPLATES"
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
  rest_api_id = var.aws_api_gateway_rest_api.id
  resource_id = var.aws_api_gateway_resource_param[var.path_part].id
  http_method = aws_api_gateway_method.api-gw-method.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Methods" = true
  }
}

resource "aws_api_gateway_integration_response" "IntegrationResponse" {
  rest_api_id = var.aws_api_gateway_rest_api.id
  resource_id = var.aws_api_gateway_resource_param[var.path_part].id
  http_method = aws_api_gateway_method.api-gw-method.http_method
  status_code = aws_api_gateway_method_response.response_200.status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,authorization,contenttype,Access-Control-Allow-Origin'"
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,GET,POST,PATCH,DELETE'"
  }
  depends_on = [
    aws_api_gateway_integration.api-gw-integration
  ]
}
