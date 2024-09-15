"""
Este modulo contiene la implementación de la conversión de un autómata finito determinista a un autómata finito determinista mínimo.
Se debe utilizar algun algoritmo de minimización de estados para realizar la conversión.
Debe regresar un objeto json con la representación del autómata finito determinista mínimo.
La estructura del objeto json esta en el README.md
"""

from collections import defaultdict, deque
import json

def minAFD(AFD: dict) -> dict:
    # Extraer información del AFND
    Q = AFD["Q"]
    s = AFD["s"]
    q0 = AFD["q0"]
    F = set(AFD["F"])
    transitions = AFD["p"]
    
    # Crear la tabla de transición
    delta = {}
    for state in Q:
        delta[state] = {}
        for symbol in s:
            delta[state][symbol] = None
    
    for transition in transitions:
        q = transition["q"]
        a = transition["a"]
        q_prime = transition["q'"]
        delta[q][a] = q_prime
        
    # Crear la tabla de equivalencia
    equivalent_table = {}
    for i, state in enumerate(Q):
        equivalent_table[state] = {}
        for state_prime in Q[i:]:
            if state != state_prime:
                equivalent_table[state][state_prime] = False
    
    # Marcar como no equivalentes los estados de aceptación con los no estados de aceptación
    for i, state in enumerate(Q):
        for state_prime in Q[i:]:
            if state != state_prime:
                if (state in F and state_prime not in F) or (state_prime in F and state not in F):
                    equivalent_table[state][state_prime] = True
    

    # Crear un array de las parejas que sean true
    non_equivalent_pairs = []
    for state in Q:
        for state_prime in Q:
            if state != state_prime and equivalent_table[state].get(state_prime, False):
                non_equivalent_pairs.append((state, state_prime))

    
    # Iterar sobre las parejas no equivalentes
    while len(non_equivalent_pairs) > 0:
        state, state_prime = non_equivalent_pairs.pop(0)
                
        # Iterar sobre los símbolos del alfabeto
        for symbol in s:
            for state1 in Q:
                q = delta[state1][symbol]
                if q == state:
                    for state2 in Q:
                        q_prime = delta[state2][symbol]
                        if q_prime == state_prime:
                            if not equivalent_table[state1].get(state2, None):  # Evitar duplicados
                                non_equivalent_pairs.append((state1, state2))
                                equivalent_table[state1][state2] = True

    
    # Unificar estados equivalentes
    unified_states = []
    for state, inner_dict in equivalent_table.items():
        for state_prime, value in inner_dict.items():  
            if value == False:  
                unified_states.append((state, state_prime))
                   
    groups = []

    for state, state_prime in unified_states:
        found_group = None
        
        # Buscar si el estado o el estado_prime ya están en un grupo existente
        for group in groups:
            if state in group or state_prime in group:
                if found_group is None:
                    # Si ninguno de los estados ya tiene un grupo asignado, lo agregamos aquí
                    group.update([state, state_prime])
                    found_group = group
                else:
                    # Unimos dos grupos si ambos tienen elementos que ya existen
                    found_group.update(group)
                    groups.remove(group)
        
        # Si no se encontró un grupo existente, creamos uno nuevo
        if found_group is None:
            groups.append(set([state, state_prime]))

    # Convertimos los conjuntos en tuplas y los mostramos
    unified_groups = [tuple(group) for group in groups]
    
    # Crear la nueva tabla de transición
    new_delta = {}
    
    # Maneja los estados que no estan unificados
    for state in Q:
        if not any(state in group for group in unified_groups):
            new_delta[state] = {}
            for symbol in s:
                target_state = delta[state][symbol]
                if target_state:
                    for target_group in unified_groups:
                        if target_state in target_group:
                            new_delta[state][symbol] = target_group
                            break
                    else:
                        new_delta[state][symbol] = target_state
                else:
                    new_delta[state][symbol] = None
    
    # Maneja los estados que estan unificados
    for group in unified_groups:
        representative = group[0]
        new_delta[group] = {}
        for symbol in s:
            target_state = delta[representative][symbol]
            for target_group in unified_groups:
                if target_state in target_group:
                    new_delta[group][symbol] = target_group
                    break
                    
    
    # Verificar si los estados finales están unificados o no
    new_F = []
    for group in unified_groups:
        for state in group:
            if state in F:
                new_F.append(group)
                break
    
    # Agregar estados finales que no están unificados
    for final_state in F:
        if not any(final_state in group for group in unified_groups):
            new_F.append(final_state)
    
    
    # Verificar si el estado inicial está unificado o no
    new_q0 = None
    for group in unified_groups:
        if q0 in group:
            new_q0 = group
            break
    if new_q0 is None:
        new_q0 = q0
    
    
    # Crear el nuevo conjunto de estados
    new_Q = []
    for state in Q:
        if not any(state in group for group in unified_groups):
            new_Q.append(state)
    new_Q.extend(unified_groups)
    
    # Crear los nuevos predicados
    new_p = []
    for state, transitions in new_delta.items():
        for symbol, target in transitions.items():
            new_p.append({"q": state, "a": symbol, "q'": target})

    min_AFD = {
        "Q": new_Q,
        "s": s,
        "q0": new_q0,
        "F": new_F,
        "p": new_p
    }
    
    return min_AFD