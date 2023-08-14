data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/source"
  excludes    = [
    "tests/*",
  ]
  output_path = "${path.module}/out/lambda_function.zip"
}

resource "aws_lambda_function" "this" {
  function_name    = var.name_webhook
  role             = aws_iam_role.iam_for_lambda.arn
  filename         = "out/lambda_function.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.10"
  timeout          = 300
}

resource "aws_lambda_permission" "this" {
  action        = "lambda:InvokeFunction"
  function_name = var.name_webhook
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_deployment.this.execution_arn}/${aws_api_gateway_method.root_post.http_method}/"
  depends_on = [
    aws_lambda_function.this
  ]
}
