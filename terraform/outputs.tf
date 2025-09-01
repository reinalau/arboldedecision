output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.prestamos_lambda.function_name
}

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "${aws_api_gateway_deployment.prestamos_deployment.invoke_url}/evaluar"
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.prestamos_lambda.arn
}