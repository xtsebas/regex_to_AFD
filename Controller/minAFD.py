"""
Este modulo contiene la implementación de la conversión de un autómata finito determinista a un autómata finito determinista mínimo.
Se debe utilizar algun algoritmo de minimización de estados para realizar la conversión.
Debe regresar un objeto json con la representación del autómata finito determinista mínimo.
La estructura del objeto json esta en el README.md
"""

from collections import defaultdict, deque
import json

def minAFD(AFD: dict) -> dict:
    # Función para convertir nombres de estados a cadenas
    def state_to_str(state):
        if isinstance(state, (list, tuple, set)):
            return ','.join(sorted(map(str, state)))
        else:
            return str(state)
    
    # Extraer información del AFD
    Q = [state_to_str(q) for q in AFD["Q"]]
    s = AFD["s"]
    q0 = state_to_str(AFD["q0"])
    F = set(state_to_str(f) for f in AFD["F"])
    transitions = AFD["p"]
    
    # Crear la función de transición delta
    delta = {}
    for state in Q:
        delta[state] = {}
    for transition in transitions:
        q = state_to_str(transition["q"])
        a = transition["a"]
        q_prime = state_to_str(transition["q'"])
        delta[q][a] = q_prime

    # Asegurar que todas las transiciones estén definidas, agregando el estado 'DEAD' si es necesario
    symbols = s
    for state in Q:
        for symbol in symbols:
            if symbol not in delta[state]:
                delta[state][symbol] = 'DEAD'
    if 'DEAD' not in delta:
        delta['DEAD'] = {}
        for symbol in symbols:
            delta['DEAD'][symbol] = 'DEAD'
        Q.append('DEAD')

    # Inicializar particiones
    non_final_states = set(Q) - F
    partitions = [F.copy(), non_final_states.copy()]
    new_partitions = []

    while True:
        new_partitions = []
        for group in partitions:
            # Crear un diccionario para agrupar estados por transiciones
            transition_groups = {}
            for state in group:
                # Crear una clave basada en las transiciones del estado
                key = []
                for symbol in symbols:
                    target_state = delta[state][symbol]
                    # Encontrar el índice de la partición donde está el estado de destino
                    for i, partition in enumerate(partitions):
                        if target_state in partition:
                            key.append(i)
                            break
                key = tuple(key)
                if key not in transition_groups:
                    transition_groups[key] = set()
                transition_groups[key].add(state)
            new_partitions.extend(transition_groups.values())
        # Verificar si las particiones han cambiado
        if len(new_partitions) == len(partitions) and all(new_partitions[i] == partitions[i] for i in range(len(partitions))):
            break
        else:
            partitions = new_partitions

    # Crear el nuevo autómata minimizado
    state_mapping = {}
    for i, group in enumerate(partitions):
        state_name = f'P{i}'
        for state in group:
            state_mapping[state] = state_name

    min_states = set(state_mapping.values())
    min_initial_state = state_mapping[q0]
    min_final_states = set()
    for state in F:
        min_final_states.add(state_mapping[state])

    min_transitions = []
    for group in partitions:
        representative_state = next(iter(group))
        min_state = state_mapping[representative_state]
        for symbol in symbols:
            target_state = delta[representative_state][symbol]
            min_target_state = state_mapping[target_state]
            min_transitions.append({
                'q': min_state,
                'a': symbol,
                'q\'': min_target_state
            })

    min_AFD = {
        "Q": list(min_states),
        "s": symbols,
        "q0": min_initial_state,
        "F": list(min_final_states),
        "p": min_transitions
    }

    return min_AFD

afd = {
    "Q": [ "q0,q2,q4", "q1,q3,q5,q6", "q7,q8", "q10,q9", "q11,q12,q14,q16", "q15,q17", "q13,q17"],
    "s": [ "b", "a"],
    "q0": "q0,q2,q4",
    "F": [ "q15,q17", "q13,q17"],
    "p": [
        {
            "q": "q0,q2,q4",
            "a": "b",
            "q'": "q1,q3,q5,q6"
        },
        {
            "q": "q1,q3,q5,q6",
            "a": "a",
            "q'": "q7,q8"
        },
        {
            "q": "q7,q8",
            "a": "b",
            "q'": "q10,q9"
        },
        {
            "q": "q10,q9",
            "a": "b",
            "q'": "q11,q12,q14,q16"
        },
        {
            "q": "q11,q12,q14,q16",
            "a": "b",
            "q'": "q15,q17"
        },
        {
            "q": "q11,q12,q14,q16",
            "a": "a",
            "q'": "q13,q17"
        }
    ]
}

# print(minAFD(afd))