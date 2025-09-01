# Project Configuration
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ArbolDeDecision"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# API Gateway Configuration
variable "api_gateway_name" {
  description = "Name of the API Gateway"
  type        = string
  default     = "evaluacion-prestamos"
}

variable "api_gateway_description" {
  description = "Description of the API Gateway"
  type        = string
  default     = "API para evaluar prestamos"
}

variable "api_gateway_stage_name" {
  description = "Stage name for API Gateway deployment"
  type        = string
  default     = "v1"
}

variable "function_name" {
  description = "Lambda function name"
  type        = string
  default     = "evaluacion-prestamos"
}

variable "lambda_runtime" {
  description = "Runtime for Lambda function"
  type        = string
  default     = "python3.9"
}

variable "lambda_timeout" {
  description = "Timeout for Lambda function in seconds"
  type        = number
  default     = 30
}

variable "lambda_memory_size" {
  description = "Memory size for Lambda function in MB"
  type        = number
  default     = 128
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

