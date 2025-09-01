#!/usr/bin/env python3
"""
AWS Architecture Diagram for Loan Evaluation Service
Based on Terraform configuration analysis
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.security import IAM
from diagrams.aws.general import Client
from diagrams.aws.storage import S3

with Diagram("Servicio de Evaluación de Préstamos - AWS Architecture", show=False, direction="TB"):
    
    # Client
    client = Client("Cliente HTTP")
    
    with Cluster("AWS Cloud"):
        
        # API Gateway
        api_gw = APIGateway("API Gateway\n(REST API)")
        
        with Cluster("Lambda Function"):
            # IAM Role
            iam_role = IAM("Lambda Execution Role\n(AWSLambdaBasicExecutionRole)")
            
            # Lambda Function
            lambda_func = Lambda("evaluacion-prestamos\n(Python 3.9)\nÁrbol de Decisión")
        
        # Source Code (implied from terraform)
        source = S3("Source Code\n(ZIP Package)")
    
    # Connections
    client >> Edge(label="POST /evaluar") >> api_gw
    api_gw >> Edge(label="AWS_PROXY Integration") >> lambda_func
    iam_role >> Edge(label="Execution Role") >> lambda_func
    source >> Edge(label="Code Deployment") >> lambda_func
    
    # Response flow
    lambda_func >> Edge(label="JSON Response", style="dashed") >> api_gw
    api_gw >> Edge(label="HTTP Response", style="dashed") >> client
