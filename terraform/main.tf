# Terraform configuration ArbolDeDecision
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Data source for current AWS region
data "aws_region" "current" {}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

resource "aws_lambda_function" "prestamos_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = var.function_name
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = var.lambda_runtime
  memory_size     = var.lambda_memory_size
  timeout         = var.lambda_timeout

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_api_gateway_rest_api" "prestamos_api" {
  name        = var.api_gateway_name
  description = var.api_gateway_description
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_api_gateway_resource" "prestamos_resource" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  parent_id   = aws_api_gateway_rest_api.prestamos_api.root_resource_id
  path_part   = "evaluar"
}

resource "aws_api_gateway_method" "prestamos_method" {
  rest_api_id   = aws_api_gateway_rest_api.prestamos_api.id
  resource_id   = aws_api_gateway_resource.prestamos_resource.id
  http_method   = "POST"
  authorization = "NONE"
  
  request_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration" "prestamos_integration" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.prestamos_lambda.invoke_arn
  
  request_templates = {
    "application/json" = "$input.json('$')"
  }
}

resource "aws_api_gateway_method_response" "prestamos_200" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method
  status_code = "200"
  
  response_models = {
    "application/json" = "Empty"
  }
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_method_response" "prestamos_400" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method
  status_code = "400"
  
  response_models = {
    "application/json" = "Empty"
  }
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_method_response" "prestamos_500" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method
  status_code = "500"
  
  response_models = {
    "application/json" = "Empty"
  }
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_integration_response" "prestamos_200" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method
  status_code = aws_api_gateway_method_response.prestamos_200.status_code
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
  
  depends_on = [aws_api_gateway_integration.prestamos_integration]
}

resource "aws_api_gateway_integration_response" "prestamos_400" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method
  status_code = aws_api_gateway_method_response.prestamos_400.status_code
  
  selection_pattern = "4\\d{2}"
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
  
  depends_on = [aws_api_gateway_integration.prestamos_integration]
}

resource "aws_api_gateway_integration_response" "prestamos_500" {
  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  resource_id = aws_api_gateway_resource.prestamos_resource.id
  http_method = aws_api_gateway_method.prestamos_method.http_method
  status_code = aws_api_gateway_method_response.prestamos_500.status_code
  
  selection_pattern = "5\\d{2}"
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
  
  depends_on = [aws_api_gateway_integration.prestamos_integration]
}

resource "aws_api_gateway_deployment" "prestamos_deployment" {
  depends_on = [
    aws_api_gateway_integration.prestamos_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.prestamos_api.id
  stage_name  = var.environment
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.prestamos_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.prestamos_api.execution_arn}/*/*"
}