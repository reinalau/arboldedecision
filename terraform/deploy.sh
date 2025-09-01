#!/bin/bash

echo "Desplegando servicio de evaluación de préstamos..."

# Cambiar al directorio de terraform
cd terraform

# Inicializar Terraform
echo "Inicializando Terraform..."
terraform init

echo "Verficando Terraform..."
terraform validate

# Planificar el despliegue
echo "Planificando despliegue..."
terraform plan -var-file="terraform.tfvars"

# Aplicar cambios
echo "Aplicando cambios..."
terraform apply -var-file="terraform.tfvars"


# Mostrar outputs
echo "Despliegue completado. URLs:"
terraform output