"""
Este modulo contiene la implementación de la conversión de un autómata finito no determinista a un autómata finito determinista.
Se debe utilizar el algoritmo de subconjuntos para realizar la conversión.
Regresa un objeto json con la representación del autómata finito determinista.
La estructura del objeto json esta en el README.md
"""
from collections import defaultdict, deque
import json

def AFND_subconjunto(AFND: dict) -> dict:
    # Extraer información del AFND
    Q = AFND["Q"]
    s = AFND["s"]
    q0 = AFND["q0"]
    F = set(AFND["F"])
    transitions = AFND["p"]
    
    # Crear la tabla de transición delta con conjuntos para manejar múltiples transiciones
    delta = {}
    for state in Q:
        delta[state] = {}
    
    for transition in transitions:
        q = transition["q"]
        a = transition["a"]
        q_prime = transition["q'"]
        if q not in delta:
            delta[q] = {}
        if a not in delta[q]:
            delta[q][a] = set()
        if isinstance(q_prime, list):
            delta[q][a].update(q_prime)
        else:
            delta[q][a].add(q_prime)
    
    # Calcular las cláusulas (epsilon-cierres)
    clausulas = Clausulas(Q, delta)
    
    # Crear la nueva tabla de transición con las cláusulas
    delta_prime = {}
    estados_usados = []
    nuevos_estados = []
    procesados = set()
    
    inicial = tuple(sorted(clausulas[q0]))
    delta_prime[inicial] = {}
    estados_usados.append(inicial)
    nuevos_estados.append(inicial)
    
    s_prime = [symbol for symbol in s if symbol != 'E']  # Eliminar 'E' del alfabeto
    
    while estados_usados:
        # Procesamos el siguiente conjunto de estados (cláusula)
        clausula_actual = estados_usados.pop(0)
        procesados.add(clausula_actual)
        delta_prime[clausula_actual] = {}
        
        for symbol in s_prime:
            estados_alcanzables = set()
            
            # Para cada estado en la cláusula actual, encontramos sus transiciones
            for state in clausula_actual:
                destinos = delta[state].get(symbol, set())
                for destino in destinos:
                    estados_alcanzables.update(clausulas[destino])
            
            if estados_alcanzables:
                clausula_nueva = tuple(sorted(estados_alcanzables))  # Convertir el conjunto en tupla
                
                # Añadimos la transición a delta_prime
                delta_prime[clausula_actual][symbol] = clausula_nueva
                
                # Si el nuevo conjunto no ha sido procesado, lo añadimos a la lista de estados por explorar
                if clausula_nueva not in procesados and clausula_nueva not in estados_usados:
                    estados_usados.append(clausula_nueva)
                    nuevos_estados.append(clausula_nueva)
    
    # Convertir los estados (tuplas) a cadenas para simplificar
    estados_nombres = {}
    for estado in nuevos_estados:
        nombre_estado = ','.join(sorted(estado))
        estados_nombres[estado] = nombre_estado
    
    # Determinar el nuevo estado inicial
    q0_prime = estados_nombres[inicial]
    
    # Determinar los nuevos estados finales
    F_prime = []
    for estado in nuevos_estados:
        if any(subestado in F for subestado in estado):
            F_prime.append(estados_nombres[estado])
    
    # Crear los predicados de aceptación
    predicados = []
    for estado, transiciones in delta_prime.items():
        estado_str = estados_nombres[estado]
        for simbolo, destino in transiciones.items():
            destino_str = estados_nombres[destino]
            predicados.append({"q": estado_str, "a": simbolo, "q'": destino_str})
    
    # Crear el AFD resultante
    AFD = {
        "Q": list(estados_nombres.values()),
        "s": s_prime,
        "q0": q0_prime,
        "F": F_prime,
        "p": predicados
    }
    
    return AFD

    
def Clausulas(Q, delta):
    clausulas = {}
    
    for state in Q:
        cierre = set()
        stack = [state]
        while stack:
            actual = stack.pop()
            cierre.add(actual)
            for next_state in delta[actual].get('E', set()):
                if next_state not in cierre:
                    cierre.add(next_state)
                    stack.append(next_state)
        clausulas[state] = cierre
    return clausulas
