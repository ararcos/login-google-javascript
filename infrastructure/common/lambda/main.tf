resource "aws_lambda_function" "func" {
  image_uri     = "${var.ecr_uri}:${var.tag}"
  function_name = var.func_name
  role          = aws_iam_role.func_role.arn
  package_type  = "Image"
  timeout       = var.timeout
  memory_size   = var.memory_size
  dynamic environment {
    for_each = var.env_variables
    content {
      variables = environment.value
    }
  }
}

resource "aws_iam_role" "func_role" {
  name = var.role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  inline_policy {
    name = "perms"
    policy = jsonencode(
      {
        "Version" : "2012-10-17",
        "Statement" : concat(
          [
            {
              "Effect" : "Allow",
              "Action" : [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
              ],
              "Resource" : "*"
            }
          ],
          var.permissions
        )
      }
    )
  }
}

resource "aws_lambda_permission" "lambda_permision" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.func.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = var.source_arn
}
