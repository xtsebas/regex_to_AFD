"""
Este modulo contiene la implementación de la conversión de una expresión regular en notación postfix a un autómata finito no determinista.
Se debe utilizar el algoritmo de Thompson o Glushkov para realizar la conversión.
Debe retornar un objeto json con la representación del autómata finito no determinista.
La estructura del objeto json esta en el README.md
"""

def postfix_to_AFND(postfix: str) -> dict:
    return