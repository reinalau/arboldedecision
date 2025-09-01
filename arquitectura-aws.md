# Diagrama de Arquitectura AWS - Servicio de Evaluación de Préstamos

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AWS CLOUD                                      │
│                                                                             │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐ │
│  │   API Gateway   │    │   Lambda Function │    │      IAM Role          │ │
│  │                 │    │                  │    │                        │ │
│  │ REST API        │◄──►│ evaluacion-      │◄───│ Lambda Execution       │ │
│  │ Regional        │    │ prestamos        │    │ Role                   │ │
│  │                 │    │                  │    │                        │ │
│  │ POST /evaluar   │    │ Python 3.9       │    │ AWSLambdaBasicExecution│ │
│  │                 │    │ Memory: 125MB    │    │ Role                   │ │
│  │                 │    │ Timeout: 30s     │    │                        │ │
│  └─────────────────┘    └──────────────────┘    └─────────────────────────┘ │
│           ▲                       ▲                                        │
│           │                       │                                        │
│           │              ┌────────────────┐                                │
│           │              │  Source Code   │                                │
│           │              │  ZIP Package   │                                │
│           │              │  (../src)      │                                │
│           │              └────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────┘
           ▲
           │
    ┌─────────────┐
    │   Cliente   │
    │    HTTP     │
    └─────────────┘
```

## Componentes de la Infraestructura

### 1. **API Gateway REST API**
- **Tipo**: Regional
- **Nombre**: `{function_name}-api`
- **Endpoint**: `/evaluar`
- **Método**: POST
- **Integración**: AWS_PROXY con Lambda

### 2. **Lambda Function**
- **Nombre**: `evaluacion-prestamos`
- **Runtime**: Python 3.9
- **Handler**: `lambda_function.lambda_handler`
- **Memoria**: 125 MB
- **Timeout**: 30 segundos
- **Función**: Implementa árbol de decisión para evaluación de préstamos

### 3. **IAM Role**
- **Nombre**: `{function_name}-role`
- **Política**: `AWSLambdaBasicExecutionRole`
- **Propósito**: Permite a Lambda escribir logs en CloudWatch

### 4. **Deployment**
- **Stage**: `dev` (configurable)
- **Source**: Código empaquetado desde `../src`

## Flujo de Datos

```
1. Cliente HTTP → POST /evaluar → API Gateway
2. API Gateway → AWS_PROXY Integration → Lambda Function
3. Lambda Function → Ejecuta árbol de decisión → Respuesta JSON
4. Lambda Function → Respuesta → API Gateway
5. API Gateway → HTTP Response → Cliente
```

## Configuración de Variables

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `aws_region` | `us-east-1` | Región AWS |
| `function_name` | `evaluacion-prestamos` | Nombre de la función |
| `lambda_runtime` | `python3.9` | Runtime de Lambda |
| `lambda_memory_size` | `128` | Memoria en MB |
| `lambda_timeout` | `30` | Timeout en segundos |
| `environment` | `dev` | Entorno de despliegue |

## Endpoints Generados

```
POST https://{api-id}.execute-api.{region}.amazonaws.com/prod/evaluar

```
### Probar en el body:
{
        "id_prestamo": "RETOS2_002",
        "casado": "No",
        "dependientes": "3+",
        "educacion": "No Graduado",
        "independiente": "No",
        "ingreso_deudor": 1830,
        "ingreso_codeudor": 0,
        "cantidad_prestamo": 100,
        "plazo_prestamo": 360,
        "historia_credito": 0,
        "tipo_propiedad": "Urbano"

}


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

{
        "id_prestamo": "RETOS2_003",
        "casado": "No",
        "dependientes": 0,
        "educacion": "No Graduado",
        "independiente": "No",
        "ingreso_deudor": 3748,
        "ingreso_codeudor": 1668,
        "cantidad_prestamo": 110,
        "plazo_prestamo": 360,
        "historia_credito": 1,
        "tipo_propiedad": "Semiurbano"
}


## Permisos y Seguridad

- Lambda tiene permisos básicos de ejecución
- API Gateway tiene permiso para invocar Lambda
- No hay autenticación configurada (authorization = "NONE")


