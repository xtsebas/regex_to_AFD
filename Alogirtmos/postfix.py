"""
Este módulo contiene la implementación de la conversión de una expresión regular a una expresión regular en notación postfija.
Se debe de utilizar el algoritmo Shunting Yard para realizar la conversión.
Debe regresar un string con la expresión regular en notación postfija.
"""

def regex_to_postfix(regex: str) -> str:
    return 

def shunting_yard(regex: str) -> str:
    
    output = []
    
    for token in regex:
        print(token)
        
def insertar_concatenacion(regex):
    """
    Dado que el algoritmo de shunting_yard no esta explicitamente creado para
    expresiones regulares, si no para operaciones aritmeticas infix y las regex
    no tienen explicitamente el operador de concatenacion, es necesario agregar el operador
    para que el algoritmo sepa de la operacion a realizar.
    
    Esta funcion tiene como objectivo agregar la concatenacion explicitamentre a la regex
    por ejemplo
    
    input -> (b|b)*abb(a|b)*
    output -> (b|b)*?a?b?b?(a|b)*
    """
    
    nueva_expresion = ""
    length = len(regex)
    
    for i in range(length):
        char = regex[i]
        nueva_expresion += char
        
        # No hacer nada si es el último carácter
        if i < length - 1:
            next_char = regex[i + 1]
            
            # Verificar si hay que agregar un símbolo de concatenación
            if (char.isalnum() or char == ')' or char == '*') and \
               (next_char.isalnum() or next_char == '('):
                nueva_expresion += '?'
    
    return nueva_expresion


