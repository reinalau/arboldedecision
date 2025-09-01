import json
from lambda_service import lambda_handler, prestamo

# Casos de prueba del enunciado
test_cases = [
    {
        'id_prestamo': 'RETOS2_001',
        'casado': 'No',
        'dependientes': 1,
        'educacion': 'Graduado',
        'independiente': 'Si',
        'ingreso_deudor': 4692,
        'ingreso_codeudor': 0,
        'cantidad_prestamo': 106,
        'plazo_prestamo': 360,
        'historia_credito': 1,
        'tipo_propiedad': 'Rural'
    },
    {
        'id_prestamo': 'RETOS2_002',
        'casado': 'No',
        'dependientes': '3+',
        'educacion': 'No Graduado',
        'independiente': 'No',
        'ingreso_deudor': 1830,
        'ingreso_codeudor': 0,
        'cantidad_prestamo': 100,
        'plazo_prestamo': 360,
        'historia_credito': 0,
        'tipo_propiedad': 'Urbano'
    },
    {
        'id_prestamo': 'RETOS2_003',
        'casado': 'No',
        'dependientes': 0,
        'educacion': 'No Graduado',
        'independiente': 'No',
        'ingreso_deudor': 3748,
        'ingreso_codeudor': 1668,
        'cantidad_prestamo': 110,
        'plazo_prestamo': 360,
        'historia_credito': 1,
        'tipo_propiedad': 'Semiurbano'
    }
]

def test_direct_function():
    print("=== Pruebas función directa ===")
    for i, case in enumerate(test_cases, 1):
        result = prestamo(case)
        print(f"Caso {i}: {result}")

def test_lambda_handler():
    print("\n=== Pruebas Lambda handler ===")
    for i, case in enumerate(test_cases, 1):
        # Simular evento Lambda HTTP
        event = {
            'body': json.dumps(case),
            'headers': {'Content-Type': 'application/json'}
        }
        
        response = lambda_handler(event, {})
        body = json.loads(response['body'])
        print(f"Caso {i}: Status {response['statusCode']}, Body: {body}")

if __name__ == "__main__":
    test_direct_function()
    test_lambda_handler()