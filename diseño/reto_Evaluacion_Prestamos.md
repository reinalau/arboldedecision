# Enunciado Reto 2 - Evaluación de Créditos

## Descripción

Usted trabaja en una entidad financiera que cuenta con la siguiente información en base a la que realizan la evaluación de nuevas solicitudes de crédito:

| Nombre | Abreviación | Tipo | Descripción |
|--------|-------------|------|-------------|
| id_prestamo | N/A | str | código único alfanumérico que identifica el prestamo |
| casado | N/A | str | Aplicante es casado (Si / No) |
| dependientes | N/A | int / str | Cantidad de personas dependientes del aplicante (0 / 1 / 2 / '3+') |
| educacion | N/A | str | Nivel de educación de la persona (Graduado / No Graduado) |
| independiente | N/A | str | Aplicante es independiente (Si / No) |
| ingreso_deudor | i_d | float | Ingreso del aplicante |
| ingreso_codeudor | i_c | float | Ingreso del codeudor |
| cantidad_prestamo | c_p | float | Cantidad de crédito solicitada |
| plazo_prestamo | p_p | int | Plazo del crédito |
| historia_credito | N/A | int | Aplicante cuenta con historia crediticia favorable (1 / 0) |
| tipo_propiedad | N/A | str | Urbana / Rural / Semi Urbana |

## Tarea

Recientemente, su empleador adquirió un modelo basado en árboles de decisión para poder realizar más fácilmente una primera revisión de estas solicitudes. Este se muestra a continuación:

Utilizando python, escriba una función que reciba como parámetro un diccionario en el cuál las llaves son los nombres de las variables mencionadas anteriormente. Retorne un nuevo diccionario con las llaves "id_prestamo" y "aprobado" dónde esta última tenga como valor una variable booleana representando la salida del árbol de decisión. Es decir, informando si el préstamo debe ser aprobado o no.

## Esqueleto

```python
def prestamo(informacion: dict) -> dict:
    pass
```

## Ejemplos

| id_prestamo | casado | dependientes | educacion | independiente | ingreso_deudor | ingreso_codeudor | cantidad_prestamo | plazo_prestamo | historia_credito | tipo_propiedad | return |
|-------------|--------|--------------|-----------|---------------|----------------|------------------|-------------------|----------------|------------------|----------------|--------|
| RETOS2_001 | No | 1 | Graduado | Si | 4692 | 0 | 106 | 360 | 1 | Rural | {'id_prestamo': 'RETOS2_001', 'aprobado': True} |
| RETOS2_002 | No | 3+ | No Graduado | No | 1830 | 0 | 100 | 360 | 0 | Urbano | {'id_prestamo': 'RETOS2_002', 'aprobado': False} |
| RETOS2_003 | No | 0 | No Graduado | No | 3748 | 1668 | 110 | 360 | 1 | Semiurbano | {'id_prestamo': 'RETOS2_003', 'aprobado': True} |