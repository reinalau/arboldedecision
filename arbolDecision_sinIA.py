
# Nombre           | Abreviación    |     Tipo        |   Descripción
# id_prestamo      |     N/A        |    str          |   código único alfanumérico que identifica el prestamo
# casado           |     N/A        |    str          |   Aplicante es casado (Si / No)
# dependientes     |     N/A        |    int / str    |   Cantidad de personas dependientes del aplicante (0 / 1 / 2 / '3+')
# educacion        |     N/A        |    str          |   Nivel de educación de la persona (Graduado / No Graduado)
# independiente    |     N/A        |    str          |   Aplicante es independiente (Si / No)
# ingreso_deudor   |    i_d         |    float        |   Ingreso del aplicante
# ingreso_codeudor |     i_c        |    float        |   Ingreso del codeudor
# cantidad_prestamo|     c_p        |    float        |   Cantidad de crédito solicitada
# plazo_prestamo   |    p_p         |    int          |   Plazo del crédito
# historia_credito |    N/A         |    int          |   Aplicante cuenta con historia crediticia favorable (1 / 0)
# tipo_propiedad   |    N/A         |    str          |   Urbana / Rural / Semi Urbana

#Falta arreglar variables globales para que se llame varias veces y en lugar de retornar SI/NO
# retorne TRUE/FALSE...te animas arreglarlo????

informacion = {
    'id_prestamo': 'RETOS2_001',
    'casado': 'No',
    'dependientes':1 , #puede contener una expesion '3+'
    'educacion': 'Graduado',
    'independiente': 'Si',
    'ingreso_deudor': 4692,
    'ingreso_codeudor': 0.00,
    'cantidad_prestamo': 106,
    'plazo_prestamo': 360,
    'historia_credito': 1,
    'tipo_propiedad': 'Rural'
}

resultado = {
    'id_prestamo': informacion['id_prestamo'],
    'aprobado': 'false'
}

from typing import Union

def convertirElemento(valor: Union[int, str]) -> int:
    try:
        if isinstance(valor, int):
            return valor
        else:
            if valor.find('+') == -1 : 
                numero = int(valor) #no encontro el signo + intenta castearlo igual
            else:
                numero = int(valor.split('+')[0]) + 1 #si encontro el +, le suma 1 al numero
            return numero
    except:
        raise ValueError("convertirElemento")
    
def historiaDeCred(informacion: dict, resultado: dict) -> dict:
    try:
        if informacion['ingreso_codeudor'] > 0 and ((informacion['ingreso_deudor'] / 9) > informacion['cantidad_prestamo']):
            resultado['aprobado'] = 'true'
        else:
            dependientes = convertirElemento(informacion['dependientes']) #castear tipo de dato
            if dependientes > 2 and informacion['independiente'].lower() == 'si':
                if informacion['ingreso_codeudor'] / 12 > informacion['cantidad_prestamo']:
                    resultado['aprobado'] = 'true'
                else:
                    resultado['aprobado'] = 'false'
            else:
                if informacion['cantidad_prestamo'] < 200:
                    resultado['aprobado']= 'true'
                else:
                    resultado['aprobado'] = 'false'
        
        return resultado
    except  Exception as e:
        raise ValueError(f"Error historiaDeCred: {str(e)}")
    
def sinHistoriaDeCred(informacion: dict, resultado: dict) -> dict:
    try:
        dependientes = convertirElemento(informacion['dependientes']) #castear tipo de dato
        if informacion['independiente'].lower() == 'si':
            if not (informacion['casado'].lower() == 'si' and dependientes > 1):
                if informacion['ingreso_deudor'] / 10 > informacion['cantidad_prestamo'] or informacion['ingreso_codeudor'] / 10 > informacion['cantidad_prestamo']:
                    if informacion['cantidad_prestamo'] < 180:
                        resultado['aprobado'] = 'true'
                    else:
                        resultado['aprobado'] = 'false'
                else:
                    resultado['aprobado'] = 'false'
            else:
                resultado['aprobado'] = 'false'
        else:
            if not (informacion['tipo_propiedad'].lower() == 'semiurbano') and dependientes < 2 :
                if informacion['educacion'].lower() == 'graduado':
                    if informacion['ingreso_deudor'] / 11 > informacion['cantidad_prestamo'] and informacion['ingreso_codeudor'] / 11 > informacion['cantidad_prestamo']:
                        resultado['aprobado'] = 'true'
                    else:
                        resultado['aprobado'] = 'false'
                else:
                    resultado['aprobado'] = 'false'
            else:
                resultado['aprobado'] = 'false'
        return resultado
    except Exception as e:
        raise ValueError(f"Error sinHistoriaDeCred: {str(e)}")
 

def prestamo(informacion: dict) -> dict:
    try:
        if informacion['historia_credito'] == 1:
            return historiaDeCred(informacion, resultado)
        else:
            return sinHistoriaDeCred(informacion, resultado)
    except Exception as e:
        raise ValueError(f"Error en prestamo: {str(e)}")

print(prestamo(informacion))
