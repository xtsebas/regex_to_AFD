"""
Este modulo contiene la implementación de la conversión de un autómata finito no determinista a un autómata finito determinista.
Se debe utilizar el algoritmo de subconjuntos para realizar la conversión.
Regresa un objeto json con la representación del autómata finito determinista.
La estructura del objeto json esta en el README.md
"""
from collections import defaultdict, deque
import json

def AFND_subconjunto(AFND: dict) -> dict:
    # Función auxiliar para convertir un conjunto de estados a una tupla ordenada (para uso como clave de diccionario)
    def set_to_tuple(states):
        return tuple(sorted(states))

    # Extraer información del AFND
    Q = AFND["Q"]
    s = AFND["s"]
    q0 = AFND["q0"]
    F = set(AFND["F"])
    transitions = AFND["p"]

    # Construir la tabla de transiciones del AFND
    delta = defaultdict(lambda: defaultdict(set))
    for transition in transitions:
        delta[transition["q"]][transition["a"]].update(transition["q'"])

    # Inicializar el AFD
    start_state = set_to_tuple({q0})
    states = {start_state}
    queue = deque([start_state])
    transition_map = defaultdict(dict)
    final_states = set()

    while queue:
        current = queue.popleft()
        current_states = set(current)
        # Determinar si el conjunto de estados es final
        if any(state in F for state in current_states):
            final_states.add(current)

        for symbol in s:
            next_states = set()
            for state in current_states:
                next_states.update(delta[state][symbol])
            next_tuple = set_to_tuple(next_states)
            if next_tuple not in states:
                states.add(next_tuple)
                queue.append(next_tuple)
            transition_map[current][symbol] = next_tuple

    # Construir el resultado
    AFD = {
        "Q": [set_to_tuple(state) for state in states],
        "s": s,
        "q0": start_state,
        "F": [state for state in states if state in final_states],
        "p": [
            {"q": state, "a": symbol, "q'": next_state}
            for state in states
            for symbol in s
            if (next_state := transition_map[state].get(symbol)) is not None
        ]
    }

    return AFD