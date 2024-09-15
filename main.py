from Algoritmos.postfix import regex_to_postfix
from Algoritmos.AFND import postfix_to_AFND
from Algoritmos.subconjuntos import AFND_subconjunto
from Algoritmos.minAFD import minAFD
import json
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BRIGHT_BLUE = "\033[94m"
MAGENTA = "\033[35m"
BRIGHT_GREEN = "\033[92m"
MATRIX_GREEN = "\033[38;5;82m" 
RED = "\033[31m"
CYAN = "\033[36m"



expresiones = [
    # "(b|b)abb(a|b)", 
    # "((E|a)|b*)",
    # "(0|(1(01*(00)0)*1))",
    "(0|1)(0|1)0*1(0|1)*"
]

def simular_AFD(afd: dict, cadena: str):
    """
    Simula un AFD sobre una cadena de entrada.

    Parámetros:
    - afd: dict
        Diccionario que representa el AFD con las claves:
        - 'Q': Lista de estados.
        - 's': Lista de símbolos del alfabeto.
        - 'q0': Estado inicial.
        - 'F': Lista de estados de aceptación.
        - 'p': Lista de transiciones, donde cada transición es un diccionario con:
            - 'q': Estado actual.
            - 'a': Símbolo de entrada.
            - "q'": Estado destino.
    - cadena: str
        Cadena de entrada que se evaluará en el AFD.

    Muestra:
    - Cada transición realizada.
    - Mensaje indicando si la cadena es aceptada o rechazada.
    """

    # Extraer información del AFD
    Q = afd["Q"]
    s = afd["s"]
    q0 = afd["q0"]
    F = set(afd["F"])
    transiciones = afd["p"]

    # Construir la función de transición delta
    delta = {}
    for estado in Q:
        delta[estado] = {}
    for transicion in transiciones:
        q = transicion["q"]
        a = transicion["a"]
        q_prime = transicion["q'"]
        delta[q][a] = q_prime

    # Estado actual inicia en el estado inicial
    estado_actual = q0

    print(f"Estado inicial: {estado_actual}")

    # Recorrer cada símbolo en la cadena de entrada
    for indice, simbolo in enumerate(cadena):
        print(f"\nPaso {indice + 1}:")
        print(f"Símbolo de entrada: '{simbolo}'")

        # Verificar si el símbolo es parte del alfabeto
        if simbolo not in s:
            print(f"Símbolo '{simbolo}' no está en el alfabeto del autómata.")
            print("La cadena es rechazada.")
            return

        # Verificar si existe una transición para el símbolo desde el estado actual
        if simbolo in delta[estado_actual]:
            estado_siguiente = delta[estado_actual][simbolo]
            print(f"Transición: ({estado_actual}, '{simbolo}') -> {estado_siguiente}")
            estado_actual = estado_siguiente
        else:
            print(f"No hay transición definida para el estado '{estado_actual}' con el símbolo '{simbolo}'.")
            print("La cadena es rechazada.")
            return

    # Verificar si el estado actual es un estado de aceptación
    if estado_actual in F:
        print(f"\nLa cadena es aceptada. Estado final: {estado_actual} es un estado de aceptación.")
    else:
        print(f"\nLa cadena es rechazada. Estado final: {estado_actual} no es un estado de aceptación.")



def simular_AFND(afnd: dict, cadena: str):
    """
    Simula un AFND con transiciones epsilon sobre una cadena de entrada.

    Parámetros:
    - afnd: dict
        Diccionario que representa el AFND con las claves:
        - 'Q': Lista de estados.
        - 's': Lista de símbolos del alfabeto (incluyendo 'E' para epsilon).
        - 'q0': Estado inicial.
        - 'F': Lista de estados de aceptación.
        - 'p': Lista de transiciones, donde cada transición es un diccionario con:
            - 'q': Estado actual.
            - 'a': Símbolo de entrada (incluyendo 'E' para epsilon).
            - "q'": Estado destino.
    - cadena: str
        Cadena de entrada que se evaluará en el AFND.

    Muestra:
    - Cada conjunto de estados actuales después de procesar un símbolo.
    - Mensaje indicando si la cadena es aceptada o rechazada.
    """
    from collections import deque

    # Extraer información del AFND
    Q = afnd["Q"]
    s = afnd["s"]
    q0 = afnd["q0"]
    F = set(afnd["F"])
    transiciones = afnd["p"]

    # Construir la función de transición delta
    delta = {}
    for estado in Q:
        delta[estado] = {}
    for transicion in transiciones:
        q = transicion["q"]
        a = transicion["a"]
        q_prime = transicion["q'"]
        if a not in delta[q]:
            delta[q][a] = set()
        if isinstance(q_prime, list):
            delta[q][a].update(q_prime)
        else:
            delta[q][a].add(q_prime)

    # Función para calcular el epsilon-cierre de un conjunto de estados
    def epsilon_cierre(estados):
        cierre = set(estados)
        pila = list(estados)
        while pila:
            estado = pila.pop()
            for estado_siguiente in delta[estado].get('E', set()):
                if estado_siguiente not in cierre:
                    cierre.add(estado_siguiente)
                    pila.append(estado_siguiente)
        return cierre

    # Inicializar el conjunto de estados actuales con el epsilon-cierre del estado inicial
    estados_actuales = epsilon_cierre({q0})

    print(f"Estado(s) inicial(es): {estados_actuales}")

    # Recorrer cada símbolo en la cadena de entrada
    for indice, simbolo in enumerate(cadena):
        print(f"\nPaso {indice + 1}:")
        print(f"Símbolo de entrada: '{simbolo}'")

        # Verificar si el símbolo es parte del alfabeto (excluyendo 'E')
        if simbolo not in s or simbolo == 'E':
            print(f"Símbolo '{simbolo}' no está en el alfabeto del autómata.")
            print("La cadena es rechazada.")
            return

        # Conjunto para los estados alcanzables después de leer el símbolo
        nuevos_estados = set()
        for estado in estados_actuales:
            for estado_siguiente in delta[estado].get(simbolo, set()):
                nuevos_estados.update(epsilon_cierre({estado_siguiente}))

        if not nuevos_estados:
            print("No hay transiciones disponibles para este símbolo desde los estados actuales.")
            print("La cadena es rechazada.")
            return

        estados_actuales = nuevos_estados
        print(f"Estado(s) actual(es) después del símbolo '{simbolo}': {estados_actuales}")

    # Verificar si algún estado actual es de aceptación
    estados_aceptacion = estados_actuales.intersection(F)
    if estados_aceptacion:
        print(f"\nLa cadena es aceptada. Estado(s) de aceptación alcanzado(s): {estados_aceptacion}")
    else:
        print(f"\nLa cadena es rechazada. Ningún estado de aceptación fue alcanzado.")



for regex in expresiones: 
    
    #mostrando regex
    print(f'{GREEN}{"-"*(len(regex)+11)}{GREEN}\n {RED}REGEX -> {RED}{YELLOW}{regex}{YELLOW}  \n{GREEN}{"-"*(len(regex)+11)}{GREEN}{RESET}')    
    
    #regex a postfix con shunting yard
    postfix = regex_to_postfix( regex = regex )
    print(f'{GREEN}{"-"*(len(postfix)+22)}{GREEN}\n{RED} REGEX -> {MAGENTA}POSTFIX{MAGENTA} -> {RED}{MATRIX_GREEN}{postfix}{MATRIX_GREEN} \n{GREEN}{"-"*(len(postfix)+22)}{GREEN}{RESET}')    

    #postfix a afnd con thompson
    afnd = postfix_to_AFND (postfix = postfix )
    print(f' {MAGENTA}POSTFIX -> {MAGENTA}{RESET}AFND\n{json.dumps(afnd, indent=4)}')
    
    #afnd a afd con construccion de subconjuntos
    afd = AFND_subconjunto( AFND = afnd)
    print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFND -> {CYAN}AFD{CYAN}\n{MATRIX_GREEN}{json.dumps(afd, indent=4)}{MATRIX_GREEN}{GREEN}\n{"-"*13}{GREEN}{RESET}\n')
    
    print("simulando AFND")
    simular_AFND(afnd, '00000000000000000001')
    
    print("Simulando AFD")
    simular_AFD(afd, '00000000000000000001')

    #babbb <- si babbbb <- no

    afd_min = minAFD( AFD = afd )
    print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFD -> {CYAN}AFD MIN{CYAN}\n{MATRIX_GREEN}{json.dumps(afd_min, indent=4)}{MATRIX_GREEN}{GREEN}\n{"-"*13}{GREEN}{RESET}\n')
    print("TEST AFD MIN")
    simular_AFD(afd_min, '00000000000000000000000')

    



# regex = "(0|1)(0|1)0*1(0|1)*"
# print(f"Regex: {regex}")
# regex_postfix = regex_to_postfix(regex)
# print(f"Postfix: {regex_postfix}")

# print("AFND:")
# afnd = postfix_to_AFND(regex_postfix)
# print(json.dumps(afnd, indent=2))

# print("AFD:")
# afd = AFND_subconjunto(afnd)
# print(json.dumps(afd, indent=2))

# print("min AFD")
# mind_afd = minAFD(afd)
# print(json.dumps(mind_afd, indent=2))


