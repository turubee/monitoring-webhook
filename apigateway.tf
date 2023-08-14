resource "aws_api_gateway_rest_api" "this" {
  name        = var.name_webhook
  description = var.api_description

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_method" "root_post" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_rest_api.this.root_resource_id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_rest_api.this.root_resource_id
  http_method = aws_api_gateway_method.root_post.http_method

  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.this.invoke_arn
}

resource "aws_api_gateway_deployment" "this" {
  rest_api_id       = aws_api_gateway_rest_api.this.id
  stage_name        = var.stage_name
  stage_description = "setting file hash = ${md5(file("apigateway.tf"))}"

  depends_on = [
    aws_api_gateway_method.root_post,
    aws_api_gateway_integration.this,
    aws_api_gateway_rest_api_policy.this,
  ]
}

resource "aws_api_gateway_rest_api_policy" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  policy      = data.aws_iam_policy_document.api_policy.json
}

data "aws_iam_policy_document" "api_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    actions = ["execute-api:Invoke"]
    #resources = ["execute-api:/*"]
    resources = ["arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.this.id}/*"]
  }
  statement {
    effect = "Deny"
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    actions = ["execute-api:Invoke"]
    #resources = ["execute-api:/*"]
    resources = ["arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.this.id}/*"]
    condition {
      test     = "NotIpAddress"
      variable = "aws:SourceIp"
      values = [
        # NewRelic us region
        "162.247.240.0/22",
        "18.246.82.0/25",
        "3.145.244.128/25",
      ]
    }
  }
}

resource "aws_api_gateway_method_settings" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  stage_name  = var.stage_name
  method_path = "*/*"
  depends_on = [
    aws_api_gateway_deployment.this,
  ]

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}

## Accout global setting
resource "aws_api_gateway_account" "global" {
  cloudwatch_role_arn = aws_iam_role.apigateway_cloudwatch_global.arn
}
