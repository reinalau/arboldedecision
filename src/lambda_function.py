import json
from typing import Union, Dict, Any

def convertir_dependientes(valor: Union[int, str]) -> int:
    if isinstance(valor, int):
        return valor
    if isinstance(valor, str) and '+' in valor:
        return int(valor.split('+')[0]) + 1
    return int(valor)

def evaluar_con_historia(info: Dict[str, Any]) -> bool:
    if info['ingreso_codeudor'] > 0 and (info['ingreso_deudor'] / 9) > info['cantidad_prestamo']:
        return True
    
    dependientes = convertir_dependientes(info['dependientes'])
    if dependientes > 2 and info['independiente'].lower() == 'si':
        return info['ingreso_codeudor'] / 12 > info['cantidad_prestamo']
    
    return info['cantidad_prestamo'] < 200

def evaluar_sin_historia(info: Dict[str, Any]) -> bool:
    dependientes = convertir_dependientes(info['dependientes'])
    
    if info['independiente'].lower() == 'si':
        if info['casado'].lower() == 'si' and dependientes > 1:
            return False
        
        ingreso_valido = (info['ingreso_deudor'] / 10 > info['cantidad_prestamo'] or 
                         info['ingreso_codeudor'] / 10 > info['cantidad_prestamo'])
        return ingreso_valido and info['cantidad_prestamo'] < 180
    
    if info['tipo_propiedad'].lower() == 'semiurbano' or dependientes >= 2:
        return False
    
    if info['educacion'].lower() != 'graduado':
        return False
    
    return (info['ingreso_deudor'] / 11 > info['cantidad_prestamo'] and 
            info['ingreso_codeudor'] / 11 > info['cantidad_prestamo'])

def prestamo(informacion: Dict[str, Any]) -> Dict[str, Any]:
    aprobado = (evaluar_con_historia(informacion) if informacion['historia_credito'] == 1 
                else evaluar_sin_historia(informacion))
    
    return {
        'id_prestamo': informacion['id_prestamo'],
        'aprobado': aprobado
    }

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        resultado = prestamo(body)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(resultado)
        }
    
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Error procesando la solicitud de préstamo'
            })
        }