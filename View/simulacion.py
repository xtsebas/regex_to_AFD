from Controller.postfix import regex_to_postfix
from Controller.AFND import postfix_to_AFND
from Controller.subconjuntos import AFND_subconjunto
from Controller.minAFD import minAFD
from Model.automata import Automaton
import json
import time

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
    print(f' {MAGENTA}POSTFIX -> {MAGENTA}{RESET}AFND\n')

    crear_archivo_json(automata= afnd, nombre_archivo = f'afnd_{cadena}')
    
    print(f' {MAGENTA}SIMULANDO AFND{MAGENTA}{RESET}\n')
    simular_cadena_AFND( afnd = afnd, cadena = cadena )

    
    # 3 -> afnd a afd con construccion de subconjuntos
    afd = AFND_subconjunto( AFND = afnd)
    print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFND -> {CYAN}AFD (subconjuntos){CYAN}\n{MATRIX_GREEN}\n')
    print(f' {MAGENTA}SIMULANDO AFD{MAGENTA}{RESET}\n')

    crear_archivo_json(automata= afd, nombre_archivo = f'afd_{cadena}')
    simular_cadena_AFD( afd = afd, cadena = cadena)

    
    # 4 -> Implementacion de un algoritmo para minimizacion de un AFD
    
    afd_min = minAFD( AFD = afd )
    print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFD -> {CYAN}AFD MIN{CYAN}\n{MATRIX_GREEN}\n')

    crear_archivo_json(automata= afd_min, nombre_archivo = f'afd_min{cadena}')

    # print(f'\n{GREEN}{"-"*13}{GREEN}{RESET}\n AFD -> {CYAN}AFD MIN{CYAN}\n{MATRIX_GREEN}{json.dumps(afd_min, indent=4)}{MATRIX_GREEN}{GREEN}\n{"-"*13}{GREEN}{RESET}\n')
    
    #5 -> Implementacion de simulacion de un AFD
    print(f' {MAGENTA}SIMULANDO AFD MIN{MAGENTA}{RESET}\n')
    
    verificar_cadena(automata = afd_min, cadena = cadena)

    simular_cadena_AFD( afd = afd_min, cadena = cadena)

def verificar_cadena(automata: dict, cadena: str):
    """
    Verifica si una cadena es aceptada por un autómata.

    Parámetros:
    - automata: Automata
        Autómata que se utilizará para verificar la cadena.
    - cadena: str
        Cadena de entrada que se evaluará en el autómata.

    Muestra:
    - Mensaje indicando si la cadena es aceptada o rechazada.
    """
    automaton = Automaton(automata["Q"], automata["s"], automata["q0"], automata["F"], automata["p"])
    
    if automaton.accepted( automaton.q0 , cadena):
        print(f"\n{GREEN}La cadena -> '{YELLOW}{cadena}{RESET}{GREEN}' es aceptada por el automata, aqui el procedimiento.{RESET}")
    else:
        print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET}")

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
    - Número de transiciones realizadas.
    - Tiempo total de ejecución.
    """

    # Iniciar medición de tiempo
    tiempo_inicio = time.perf_counter()

    # Inicializar contador de transiciones
    contador_transiciones = 0

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

    print(f"{MATRIX_GREEN}Estado inicial:{RESET} {YELLOW}{estado_actual}{RESET}")

    # Recorrer cada símbolo en la cadena de entrada
    for indice, simbolo in enumerate(cadena):
        print(f"\nPaso {MATRIX_GREEN}{indice + 1}:{RESET}")
        print(f"Símbolo de entrada: '{YELLOW}{simbolo}{RESET}'")

        # Verificar si el símbolo es parte del alfabeto
        if simbolo not in s:
            print(f"{RED}Símbolo '{simbolo}' no está en el alfabeto del autómata.{RESET}")
            print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET} Estado final: {YELLOW}{estado_actual}{RESET} no es un estado de aceptación.")
            # Finalizar medición de tiempo
            tiempo_fin = time.perf_counter()
            tiempo_total = tiempo_fin - tiempo_inicio
            print(f"\n{MAGENTA}Número de transiciones realizadas:{RESET} {contador_transiciones}")
            print(f"{MAGENTA}Tiempo total de ejecución:{RESET} {tiempo_total:.6f} segundos")
            return

        # Verificar si existe una transición para el símbolo desde el estado actual
        if simbolo in delta[estado_actual]:
            estado_siguiente = delta[estado_actual][simbolo]
            print(f"{BRIGHT_BLUE}Transición{RESET}: ({YELLOW}{estado_actual}{RESET}, '{YELLOW}{simbolo}{RESET}') {MAGENTA}->{RESET} {YELLOW}{estado_siguiente}{RESET}")
            estado_actual = estado_siguiente
            contador_transiciones += 1  # Incrementar el contador de transiciones
        else:
            print(f"{RED}No hay transición definida para el estado '{estado_actual}' con el símbolo '{simbolo}'.{RESET}")
            print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET} Estado final: {YELLOW}{estado_actual}{RESET} no es un estado de aceptación.")
            # Finalizar medición de tiempo
            tiempo_fin = time.perf_counter()
            tiempo_total = tiempo_fin - tiempo_inicio
            print(f"\n{MAGENTA}Número de transiciones realizadas:{RESET} {contador_transiciones}")
            print(f"{MAGENTA}Tiempo total de ejecución:{RESET} {tiempo_total:.6f} segundos")
            return

    # Verificar si el estado actual es un estado de aceptación
    if estado_actual in F:
        print(f"\n{MATRIX_GREEN}La cadena -> '{YELLOW}{cadena}{RESET}{MATRIX_GREEN}' es aceptada.{RESET} Estado final: {YELLOW}{estado_actual}{RESET} es un estado de aceptación.")
    else:
        print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET} Estado final: {YELLOW}{estado_actual}{RESET} no es un estado de aceptación.")

    # Finalizar medición de tiempo
    tiempo_fin = time.perf_counter()
    tiempo_total = tiempo_fin - tiempo_inicio

    # Mostrar número de transiciones y tiempo total
    print(f"\n{MAGENTA}Número de transiciones realizadas:{RESET} {contador_transiciones}")
    print(f"{MAGENTA}Tiempo total de ejecución:{RESET} {tiempo_total:.6f} segundos")


import time  # Importar el módulo time para medir el tiempo

# Definición de códigos de color ANSI
RESET = '\033[0m'
BRIGHT_BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
MATRIX_GREEN = '\033[92m'
MAGENTA = '\033[95m'

def simular_cadena_AFND(afnd: dict, cadena: str):
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
    - Número de transiciones realizadas.
    - Tiempo total de ejecución.
    """
    from collections import deque

    # Iniciar medición de tiempo
    tiempo_inicio = time.perf_counter()

    # Inicializar contador de transiciones
    contador_transiciones = 0

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
        nonlocal contador_transiciones  # Declarar contador_transiciones como nonlocal
        cierre = set(estados)
        pila = list(estados)
        while pila:
            estado = pila.pop()
            for estado_siguiente in delta[estado].get('E', set()):
                if estado_siguiente not in cierre:
                    cierre.add(estado_siguiente)
                    pila.append(estado_siguiente)
                    contador_transiciones += 1  # Incrementar contador por la transición épsilon
        return cierre

    # Inicializar el conjunto de estados actuales con el epsilon-cierre del estado inicial
    estados_actuales = epsilon_cierre({q0})

    print(f"{MATRIX_GREEN}Estado(s) inicial(es):{RESET} {YELLOW}{estados_actuales}{RESET}")

    # Recorrer cada símbolo en la cadena de entrada
    for indice, simbolo in enumerate(cadena):
        print(f"\nPaso {MATRIX_GREEN}{indice + 1}:{RESET}")
        print(f"Símbolo de entrada: '{YELLOW}{simbolo}{RESET}'")

        # Verificar si el símbolo es parte del alfabeto (excluyendo 'E')
        if simbolo not in s or simbolo == 'E':
            print(f"{RED}Símbolo '{simbolo}' no está en el alfabeto del autómata.{RESET}")
            print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET}")
            # Finalizar medición de tiempo
            tiempo_fin = time.perf_counter()
            tiempo_total = tiempo_fin - tiempo_inicio
            print(f"\n{MAGENTA}Número de transiciones realizadas:{RESET} {contador_transiciones}")
            print(f"{MAGENTA}Tiempo total de ejecución:{RESET} {tiempo_total:.6f} segundos")
            return

        # Conjunto para los estados alcanzables después de leer el símbolo
        nuevos_estados = set()
        for estado in estados_actuales:
            if simbolo in delta[estado]:
                for estado_siguiente in delta[estado][simbolo]:
                    contador_transiciones += 1  # Incrementar contador por la transición
                    cierre_epsilon = epsilon_cierre({estado_siguiente})
                    nuevos_estados.update(cierre_epsilon)
            else:
                continue  # No hay transición para este símbolo desde este estado

        if not nuevos_estados:
            print(f"{RED}No hay transiciones disponibles para este símbolo desde los estados actuales.{RESET}")
            print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET}")
            # Finalizar medición de tiempo
            tiempo_fin = time.perf_counter()
            tiempo_total = tiempo_fin - tiempo_inicio
            print(f"\n{MAGENTA}Número de transiciones realizadas:{RESET} {contador_transiciones}")
            print(f"{MAGENTA}Tiempo total de ejecución:{RESET} {tiempo_total:.6f} segundos")
            return

        estados_actuales = nuevos_estados
        print(f"{BRIGHT_BLUE}Estado(s) actual(es) después del símbolo '{YELLOW}{simbolo}{RESET}{BRIGHT_BLUE}':{RESET} {YELLOW}{estados_actuales}{RESET}")

    # Verificar si algún estado actual es de aceptación
    estados_aceptacion = estados_actuales.intersection(F)
    if estados_aceptacion:
        print(f"\n{MATRIX_GREEN}La cadena -> '{YELLOW}{cadena}{RESET}{MATRIX_GREEN}' es aceptada.{RESET} Estado(s) de aceptación alcanzado(s): {YELLOW}{estados_aceptacion}{RESET}")
    else:
        print(f"\n{RED}La cadena -> '{YELLOW}{cadena}{RESET}{RED}' es rechazada.{RESET} Ningún estado de aceptación fue alcanzado.")

    # Finalizar medición de tiempo
    tiempo_fin = time.perf_counter()
    tiempo_total = tiempo_fin - tiempo_inicio

    # Mostrar número de transiciones y tiempo total
    print(f"\n{MAGENTA}Número de transiciones realizadas:{RESET} {contador_transiciones}")
    print(f"{MAGENTA}Tiempo total de ejecución:{RESET} {tiempo_total:.6f} segundos")

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
    with open(f'Assets/{nombre_archivo}.json', 'w', encoding='utf-8') as f:
        json.dump(automata_json, f, ensure_ascii=False, indent=4)
    
    print(f"Archivo JSON '{nombre_archivo}.json' creado exitosamente en la carpeta 'salida'.")

