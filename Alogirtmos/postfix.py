"""
Este módulo contiene la implementación de la conversión de una expresión regular a una expresión regular en notación postfija.
Se debe de utilizar el algoritmo Shunting Yard para realizar la conversión.
Debe regresar un string con la expresión regular en notación postfija.
"""
import sys
import os

# Añade el directorio base del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Estructuras.Stack import Stack

def regex_to_postfix(regex: str) -> str:
    return shunting_yard(insertar_concatenacion(regex))

def shunting_yard(regex: str) -> str:
    output = []
    pila_operadores = Stack()
    
    # Precedencia de operadores
    precedencia = { "*" : 3, "+" : 2, "?" : 1 }  # La concatenación tiene la menor precedencia
    operadores = list(precedencia.keys())
    
    for token in regex:
        if token not in operadores and token not in "()":  # Si es un operando
            output.append(token)
        elif token in operadores:  # Si es un operador
            while (not pila_operadores.is_empty() and 
                   pila_operadores.peek() in operadores and 
                   precedencia[pila_operadores.peek()] >= precedencia[token]):
                output.append(pila_operadores.pop())
            pila_operadores.push(token)
        elif token == '(':  # Si es un paréntesis izquierdo
            pila_operadores.push(token)
        elif token == ')':  # Si es un paréntesis derecho
            while not pila_operadores.is_empty() and pila_operadores.peek() != '(':
                output.append(pila_operadores.pop())
            pila_operadores.pop()  # Eliminar el paréntesis izquierdo

    # Vaciar la pila de operadores al final
    while not pila_operadores.is_empty():
        output.append(pila_operadores.pop())
    
    # Eliminar los símbolos de concatenación ('?') del output
    output = [token for token in output if token != '?']
    return ''.join(output)

            
        
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


regex = "a(a+b)*b"
print("Expresión en notación postfija:", regex_to_postfix(regex))
