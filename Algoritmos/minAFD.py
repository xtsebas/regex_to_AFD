"""
Este modulo contiene la implementación de la conversión de un autómata finito determinista a un autómata finito determinista mínimo.
Se debe utilizar algun algoritmo de minimización de estados para realizar la conversión.
Debe regresar un objeto json con la representación del autómata finito determinista mínimo.
La estructura del objeto json esta en el README.md
"""

from collections import defaultdict, deque
import json

def minAFD(AFD: dict) -> dict:
    # Extraer información del AFD
    Q = AFD["Q"]
    s = AFD["s"]
    q0 = AFD["q0"]
    F = set(AFD["F"])
    transitions = AFD["p"]

    # Crear la función de transición delta
    delta = {}
    for state in Q:
        delta[state] = {}
    for transition in transitions:
        q = transition["q"]
        a = transition["a"]
        q_prime = transition["q'"]
        delta[q][a] = q_prime

    # Agregar estado sumidero (estado de muerte) si es necesario
    dead_state_needed = False
    for state in Q:
        for a in s:
            if a not in delta[state]:
                dead_state_needed = True
                delta[state][a] = 'DEAD'
    if dead_state_needed:
        delta['DEAD'] = {}
        for a in s:
            delta['DEAD'][a] = 'DEAD'
        Q.append('DEAD')

    # Actualizar la lista de estados
    states = Q

    # Inicializar la tabla de pares de estados
    pairs = []
    for i, p in enumerate(states):
        for j in range(i + 1, len(states)):
            q = states[j]
            pairs.append((p, q))

    # Inicializar la tabla de estados distinguibles
    distinguishable = set()
    table = {}
    for (p, q) in pairs:
        if (p in F and q not in F) or (p not in F and q in F):
            table[(p, q)] = True  # Marcado como distinguible
            distinguishable.add((p, q))
        else:
            table[(p, q)] = False  # Inicialmente no distinguible

    # Algoritmo de llenado de tablas
    changed = True
    while changed:
        changed = False
        for (p, q) in pairs:
            if table[(p, q)]:
                continue  # Ya marcado como distinguible
            for a in s:
                p1 = delta[p][a]
                q1 = delta[q][a]
                if p1 == q1:
                    continue
                # Ordenar los estados para mantener consistencia en las claves
                pair = (min(p1, q1), max(p1, q1))
                if table.get(pair, False):
                    table[(p, q)] = True  # Marcar como distinguible
                    distinguishable.add((p, q))
                    changed = True
                    break

    # Agrupar estados no distinguibles
    groups = []
    group_dict = {}
    for state in states:
        group_dict[state] = None

    for state in states:
        if group_dict[state] is not None:
            continue
        # Encontrar todos los estados no distinguibles de 'state'
        group = [state]
        group_dict[state] = state
        for other_state in states:
            if other_state == state or group_dict[other_state] is not None:
                continue
            pair = (min(state, other_state), max(state, other_state))
            if not table.get(pair, False):
                group.append(other_state)
                group_dict[other_state] = state
        groups.append(group)

    # Construir el AFD minimizado
    new_states = []
    new_state_names = {}
    for group in groups:
        name = ','.join(sorted(group))
        new_states.append(name)
        for state in group:
            new_state_names[state] = name

    new_delta = {}
    for name in new_states:
        new_delta[name] = {}

    for group in groups:
        representative = group[0]
        new_state = new_state_names[representative]
        for a in s:
            target = delta[representative][a]
            new_target = new_state_names[target]
            new_delta[new_state][a] = new_target

    # Determinar el nuevo estado inicial
    new_q0 = new_state_names[q0]

    # Determinar los nuevos estados de aceptación
    new_F = set()
    for group in groups:
        group_name = new_state_names[group[0]]
        if any(state in F for state in group):
            new_F.add(group_name)

    # Construir las nuevas transiciones
    new_transitions = []
    for state in new_delta:
        for a in new_delta[state]:
            new_transitions.append({
                'q': state,
                'a': a,
                'q\'': new_delta[state][a]
            })

    min_AFD = {
        "Q": new_states,
        "s": s,
        "q0": new_q0,
        "F": list(new_F),
        "p": new_transitions
    }

    return min_AFD
