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

def simular_AFD(regex: str, cadena: str):
    
    #mostrando regex
    print(f'{GREEN}{"-"*(len(regex)+11)}{GREEN}\n {RED}REGEX -> {RED}{YELLOW}{regex}{YELLOW}  \n{GREEN}{"-"*(len(regex)+11)}{GREEN}{RESET}')    

    # 1 -> regex a postfix con shunting yard
    postfix = regex_to_postfix( regex = regex )
    print(f'{GREEN}{"-"*(len(postfix)+22)}{GREEN}\n{RED} REGEX -> {MAGENTA}POSTFIX{MAGENTA} -> {RED}{MATRIX_GREEN}{postfix}{MATRIX_GREEN} \n{GREEN}{"-"*(len(postfix)+22)}{GREEN}{RESET}')    

    # 2 -> postfix a afnd con thompson
    afnd = postfix_to_AFND (postfix = postfix )
    crear_archivo_json(automata= afnd, nombre_archivo = f'afnd_{cadena}')
    
    print(f' {MAGENTA}POSTFIX -> {MAGENTA}{RESET}AFND\n{json.dumps(afnd, indent=4)}')
    
    # 3 -> afnd a afd con construccion de subconjuntos
    afd = AFND_subconjunto( AFND = afnd)
    crear_archivo_json(automata= afd, nombre_archivo = f'afd_{cadena}')

    print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFND -> {CYAN}AFD{CYAN}\n{MATRIX_GREEN}{json.dumps(afd, indent=4)}{MATRIX_GREEN}{GREEN}\n{"-"*13}{GREEN}{RESET}\n')
    
    # 4 -> Implementacion de un algoritmo para minimizacion de un AFD
    afd_min = minAFD( AFD = afd )
    crear_archivo_json(automata= afd_min, nombre_archivo = f'afd_min{cadena}')

    print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFD -> {CYAN}AFD MIN{CYAN}\n{MATRIX_GREEN}{json.dumps(afd_min, indent=4)}{MATRIX_GREEN}{GREEN}\n{"-"*13}{GREEN}{RESET}\n')
    
    #5 -> Implementacion de simulacion de un AFD
    simular_cadena_AFD( afd = afd_min, cadena = cadena)
    
def simular_cadena_AFD(afd: dict, cadena: str):
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
        print(f"\nPaso {MATRIX_GREEN}{indice + 1}:{MATRIX_GREEN}{RESET}")
        print(f"Símbolo de entrada: '{simbolo}'")

        # Verificar si el símbolo es parte del alfabeto
        if simbolo not in s:
            print(f"Símbolo '{simbolo}' no está en el alfabeto del autómata.")
            print(f"\n{RED}La cadena -> '{RED}{YELLOW}{cadena}{YELLOW}{RESET}' {RED}es rechazada.{RED}{RESET} Estado final: {estado_actual} no es un estado de aceptación.")            

        # Verificar si existe una transición para el símbolo desde el estado actual
        if simbolo in delta[estado_actual]:
            estado_siguiente = delta[estado_actual][simbolo]
            print(f"{BRIGHT_BLUE}Transición{BRIGHT_BLUE}{RESET}: ({estado_actual}, '{simbolo}') {YELLOW}->{YELLOW}{RESET} {estado_siguiente}")
            estado_actual = estado_siguiente
        else:
            print(f"No hay transición definida para el estado '{estado_actual}' con el símbolo '{simbolo}'.")
            print(f"\n{RED}La cadena -> '{RED}{YELLOW}{cadena}{YELLOW}{RESET}' {RED}es rechazada.{RED}{RESET} Estado final: {estado_actual} no es un estado de aceptación.")            
            return

    # Verificar si el estado actual es un estado de aceptación
    if estado_actual in F:
        print(f"\n{MATRIX_GREEN}La cadena -> '{MATRIX_GREEN}{YELLOW}{cadena}{YELLOW}{MATRIX_GREEN}' es aceptada.{MATRIX_GREEN}{RESET} Estado final: {estado_actual} es un estado de aceptación.")
    else:
        print(f"\n{RED}La cadena -> '{RED}{YELLOW}{cadena}{YELLOW}{RESET}' {RED}es rechazada.{RED}{RESET} Estado final: {estado_actual} no es un estado de aceptación.")

def crear_archivo_json(automata, nombre_archivo):
    print("Creando archivo JSON...")
    
    # Convertir los conjuntos a listas o cadenas adecuadas para JSON
    estados = sorted(list(automata["Q"]))
    simbolos = sorted(list(automata["s"]))
    inicio = automata["q0"]
    aceptacion = sorted(list(automata["F"]))
    transiciones = []

    # Formatear las transiciones como tuplas
    for transicion in automata["p"]:
        origen = transicion['q']
        simbolo = transicion['a']
        destino = transicion["q'"]
        # Formatear la transición como una tupla
        transiciones.append((origen, simbolo, destino))

    # Construir el diccionario con la estructura requerida
    automata_json = {
        "ESTADOS": estados,
        "SIMBOLOS": simbolos,
        "INICIO": inicio,
        "ACEPTACION": aceptacion,
        "TRANSICIONES": transiciones
    }


    # Escribir en un archivo JSON
    with open(f'salida/{nombre_archivo}.json', 'w', encoding='utf-8') as f:
        json.dump(automata_json, f, ensure_ascii=False, indent=4)
    
    print(f"Archivo JSON '{nombre_archivo}.json' creado exitosamente en la carpeta 'salida'.")

