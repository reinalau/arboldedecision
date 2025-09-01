# Servicio de Evaluación de Préstamos desplegado en AWS
(este reto fue propuesto por la genia de @roxsross 💗 )

## Descripción
Servicio Python para AWS Lambda que implementa un árbol de decisión para evaluar solicitudes de préstamos bancarios de acuerdo a una logica determinada.
TOTALMENTE PERFECTIBLE!! 🤓 


## Árbol de Decisión

```
                    Historia Crediticia?
                           /        \
                        SI /          \ NO
                          /            \
                         /              \
              Ingreso Codeudor > 0       Independiente?
              Y (Ingreso Deudor/9)         /        \
              > Cantidad Préstamo?      SI /          \ NO
                     /    \               /            \
                  SI /      \ NO         /              \
                    /        \          /                \
               APROBADO   Dependientes > 2  Tipo Propiedad != Semiurbano
                          Y Independiente?   Y Dependientes < 2?
                               /    \              /        \
                            SI /      \ NO       SI /          \ NO
                              /        \          /            \
                             /          \        /              \
                  Ingreso Codeudor/12  Cantidad  Educación    RECHAZADO
                  > Cantidad Préstamo? < 200?   Graduado?
                         /    \         /  \       /    \
                      SI /      \ NO  SI /    \ NO SI /      \ NO
                        /        \      /      \    /        \
                   APROBADO  RECHAZADO APROBADO RECHAZADO    RECHAZADO
                                                    |
                                              (Ingreso Deudor/11 > Cantidad
                                               Y Ingreso Codeudor/11 > Cantidad)
                                                     /        \
                                                  SI /          \ NO
                                                    /            \
                                               APROBADO      RECHAZADO
```


## Estructura del Proyecto
```
ArbolDeDecision/
├── src/
│   └── lambda_function.py    # Código Lambda
├── terraform/
│   ├── main.tf              # Configuración principal
│   ├── variables.tf         # Variables
│   ├── outputs.tf           # Outputs
│   ├── terraform.tfvars.example
|   └── deploy.sh            # Script de despliegue
├── tests/
│   └── test_lambda.py       # Pruebas

```

## Despliegue con Terraform

### Prerrequisitos
- AWS CLI configurado
- Terraform instalado
- Credenciales AWS válidas

### Despliegue
```bash
# Opción 1: Script automático
./deploy.sh

# Opción 2: Manual
cd terraform
terraform init
terraform plan
terraform apply
```

### Configuración
Copiar `terraform.tfvars.example` a `terraform.tfvars` y ajustar valores:
```hcl
aws_region    = "us-east-1"
function_name = "evaluacion-prestamos"
environment   = "dev"
```

## Uso del API

### Endpoint
```
POST https://{api-id}.execute-api.{region}.amazonaws.com/dev/evaluar
```

### Payload
```json
{
  "id_prestamo": "RETOS2_001",
  "casado": "No",
  "dependientes": 1,
  "educacion": "Graduado",
  "independiente": "Si",
  "ingreso_deudor": 4692,
  "ingreso_codeudor": 0,
  "cantidad_prestamo": 106,
  "plazo_prestamo": 360,
  "historia_credito": 1,
  "tipo_propiedad": "Rural"
}
```

### Respuesta
```json
{
  "statusCode": 200,
  "body": "{\"id_prestamo\": \"RETOS2_001\", \"aprobado\": true}"
}
```

## Pruebas
```bash
cd tests
python test_lambda.py
```