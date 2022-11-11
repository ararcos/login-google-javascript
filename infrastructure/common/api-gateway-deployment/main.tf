
resource "aws_api_gateway_deployment" "api-gw-deployment" {
  triggers = {
    redeployment = sha1(jsonencode(var.modules))
  }
  rest_api_id = var.aws_api_gateway_rest_api.id
  stage_name  = var.stage_name
}
