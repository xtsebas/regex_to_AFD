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
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

def regex_to_postfix(regex: str) -> str:
    """
    Recibe una regex y lo
    Operadores aceptados

    "|" -> Union
    "*" -> Estrella de 
    
    """
    return shunting_yard(insertar_concatenacion(regex))

def shunting_yard(regex: str) -> str:
    output = []
    pila_operadores = Stack()
    
    # Precedencia de operadores
    precedencia = { 
                   "+" : 4,  # Cerradura positiva (uno o más)
                   "*" : 4,  # Cerradura de Kleene (cero o más)
                   "?" : 3,  # Concatenación
                   "|" : 2   # Unión (alternancia)
                   }
    
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
    
    # Eliminar los símbolos de concatenación ('?') del output si no es necesario
    output = [token for token in output]
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


regex_postfix_test = {
    "a(a+b)|b": "aab+b|",
    "abc": "abc",
    "ab|c": "abc|",
    "a(bb)+c": "abbc+",
    "abc(a|v)": "abcav|",
    "(b|b)*abb(a|b)*" : "bb|*abbab|*"
    }


def test(regex_hash):
    passed = 0
    for regex in regex_hash:
        
        postfix_output = regex_to_postfix(regex=regex)
        
        if postfix_output == regex_hash[regex]:
            
            passed += 1
            debug = f"infix regex --> {BLUE}{regex}{RESET} postfix regex -> {MAGENTA}{postfix_output}{RESET}"            
            print(f"{YELLOW}{"="*len(debug)}{RESET}")
            print(f"REGEX: {CYAN}{regex}{RESET}")
            print(f"expresion formateada: {CYAN}{insertar_concatenacion(regex)}{RESET}")
            print(debug)
            print(f"{GREEN}PASSED{RESET}")
            
        else:
            debug = f"infix regex --> {BLUE}{regex}{RESET} postfix regex -> {MAGENTA}{regex}{RESET}"            
            print(f"{YELLOW}{"="*len(debug)}{RESET}")
            print("correct postfix -> "+regex_hash[regex])
            print(f"{RED}FAIL{RESET}")
            print("=" * len(debug))
    print("accuracy -----> " + str((passed/len(regex_hash))*100)+"%")
            
            
test(regex_postfix_test)
