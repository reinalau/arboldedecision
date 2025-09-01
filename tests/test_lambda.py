import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
from lambda_function import lambda_handler, prestamo

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

def test_lambda():
    print("=== Pruebas Lambda ===")
    for i, case in enumerate(test_cases, 1):
        event = {'body': json.dumps(case)}
        response = lambda_handler(event, {})
        body = json.loads(response['body'])
        print(f"Datos del Caso: {test_cases[i-1]}")
        print(f"Caso {i}: {body}")

if __name__ == "__main__":
    test_lambda()