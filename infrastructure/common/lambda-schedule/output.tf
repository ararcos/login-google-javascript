output "function" {
  value = resource.aws_lambda_function.lambda_schedule
}

output "func_role" {
  value = resource.aws_iam_role.func_role
}
