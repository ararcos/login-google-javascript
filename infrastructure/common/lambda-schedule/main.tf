resource "aws_lambda_function" "lambda_schedule" {
  image_uri     = "${var.ecr_uri}:${var.tag}"
  function_name = var.func_name
  role          = aws_iam_role.func_role.arn
  package_type  = "Image"
  timeout       = var.timeout
  memory_size   = var.memory_size
  dynamic "environment" {
    for_each = var.env_variables
    content {
      variables = environment.value
    }
  }
}

resource "aws_iam_role" "func_role" {
  name = var.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
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
                "logs:PutLogEvents",
                "logs:AssociateKmsKey"
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

resource "aws_cloudwatch_event_rule" "schedule" {
    name = var.schedule_name
    description = "Schedule for Lambda Function"
    schedule_expression = var.schedule
}

resource "aws_cloudwatch_event_target" "schedule_lambda" {
    rule = aws_cloudwatch_event_rule.schedule.name
    target_id = "processing_lambda"
    arn = aws_lambda_function.lambda_schedule.arn
}

resource "aws_lambda_permission" "lambda_permision" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_schedule.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}

