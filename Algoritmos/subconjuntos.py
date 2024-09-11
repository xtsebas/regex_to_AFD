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
    
    if 'E' in s:

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
        
        
        # Crear clausulas de transición
        clausulas = Clausulas(Q, s, delta)
        
        # Creamos la nueva tabla de transición con las clausulas
        delta_prime = {}
        estados_usados =[]
        nuevos_estados = []
        procesados = []
        
        inicial = tuple(clausulas[q0])
        delta_prime[inicial] = {}
        estados_usados.append(inicial)
        nuevos_estados.append(inicial)
        
        while estados_usados:
            # Procesamos el siguiente conjunto de estados (cláusula)
            clausula_actual = estados_usados.pop(0)
            procesados.append(clausula_actual)
            
            for symbol in s:
                if symbol != 'E':
                    estados_alcanzables = set()
                    
                    # Para cada estado en la cláusula actual, encontramos sus transiciones
                    for state in clausula_actual:
                        if delta[state][symbol] is not None:
                            estados_alcanzables.update(clausulas[delta[state][symbol]])
                    
                    if estados_alcanzables:
                        clausula_nueva = tuple(sorted(estados_alcanzables))  # Convertir el conjunto en tupla

                        # Añadimos la transición a delta_prime
                        delta_prime[clausula_actual][symbol] = clausula_nueva
                        
                        # Si el nuevo conjunto no ha sido procesado, lo añadimos a la lista de estados por explorar
                        if clausula_nueva not in procesados and clausula_nueva not in estados_usados:
                            estados_usados.append(clausula_nueva)
                            nuevos_estados.append(clausula_nueva)

                        # Añadimos el nuevo conjunto a la tabla de transición si aún no existe
                        if clausula_nueva not in delta_prime:
                            delta_prime[clausula_nueva] = {}
                
        
        # Revisar nuevos_estados y convertir tuplas de un solo elemento a string
        for i in range(len(nuevos_estados)):
            if len(nuevos_estados[i]) == 1:
                nuevos_estados[i] = nuevos_estados[i][0]
        
        
        # Crear el nuevo conjunto de símbolos sin 'E'
        s_prime = [symbol for symbol in s if symbol != 'E']
        
        
        # Determinar el nuevo estado inicial
        q0_prime = None
        for estado in nuevos_estados:
            if q0 in estado:
                q0_prime = estado
                break
                
        # Determinar los nuevos estados finales
        F_prime = []
        for estado in nuevos_estados:
            if isinstance(estado, tuple):
                if any(subestado in F for subestado in estado):
                    F_prime.append(estado)
            else:
                if estado in F:
                    F_prime.append(estado)
                
        # Crear los predicados de aceptación
        predicados = []
        for estado, transiciones in delta_prime.items():
            for simbolo, destino in transiciones.items():
                if isinstance(estado, tuple) and len(estado) == 1:
                    estado = estado[0]
                if isinstance(destino, tuple) and len(destino) == 1:
                    destino = destino[0]
                predicados.append({"q": estado, "a": simbolo, "q'": destino})
        
        
        # Crear el AFD resultante
        AFD = {
            "Q": nuevos_estados,
            "s": s_prime,
            "q0": q0_prime,
            "F": F_prime,
            "p": predicados
        }
        
        return AFD 
    else:
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

        # Crear clausulas de transición
        clausulas = Clausulas(Q, s, delta)
        
        # Creamos la nueva tabla de transición con las clausulas
        delta_prime = {}
        estados_usados = []
        nuevos_estados = []
        procesados = []
        
        inicial = tuple(clausulas[q0])
        delta_prime[inicial] = {}
        estados_usados.append(inicial)
        nuevos_estados.append(inicial)
        
        while estados_usados:
            # Procesamos el siguiente conjunto de estados (cláusula)
            clausula_actual = estados_usados.pop(0)
            procesados.append(clausula_actual)
            
            for symbol in s:
                estados_alcanzables = set()
                
                # Para cada estado en la cláusula actual, encontramos sus transiciones
                for state in clausula_actual:
                    if delta[state][symbol] is not None:
                        estados_alcanzables.update(clausulas[delta[state][symbol]])
                
                if estados_alcanzables:
                    clausula_nueva = tuple(sorted(estados_alcanzables))  # Convertir el conjunto en tupla

                    # Añadimos la transición a delta_prime
                    delta_prime[clausula_actual][symbol] = clausula_nueva
                    
                    # Si el nuevo conjunto no ha sido procesado, lo añadimos a la lista de estados por explorar
                    if clausula_nueva not in procesados and clausula_nueva not in estados_usados:
                        estados_usados.append(clausula_nueva)
                        nuevos_estados.append(clausula_nueva)

                    # Añadimos el nuevo conjunto a la tabla de transición si aún no existe
                    if clausula_nueva not in delta_prime:
                        delta_prime[clausula_nueva] = {}
        
        # Revisar nuevos_estados y convertir tuplas de un solo elemento a string
        for i in range(len(nuevos_estados)):
            if len(nuevos_estados[i]) == 1:
                nuevos_estados[i] = nuevos_estados[i][0]
        
        # Determinar el nuevo estado inicial
        q0_prime = None
        for estado in nuevos_estados:
            if q0 in estado:
                q0_prime = estado
                break
                
        # Determinar los nuevos estados finales
        F_prime = []
        for estado in nuevos_estados:
            if isinstance(estado, tuple):
                if any(subestado in F for subestado in estado):
                    F_prime.append(estado)
            else:
                if estado in F:
                    F_prime.append(estado)
                
        # Crear los predicados de aceptación
        predicados = []
        for estado, transiciones in delta_prime.items():
            for simbolo, destino in transiciones.items():
                if isinstance(estado, tuple) and len(estado) == 1:
                    estado = estado[0]
                if isinstance(destino, tuple) and len(destino) == 1:
                    destino = destino[0]
                predicados.append({"q": estado, "a": simbolo, "q'": destino})
        
        # Crear el AFD resultante
        AFD = {
            "Q": nuevos_estados,
            "s": s, 
            "q0": q0_prime,
            "F": F_prime,
            "p": predicados
        }
        
        return AFD
    
def Clausulas(Q, s, delta):
    clausulas = {}
    
    for state in Q:
        clausulas[state] = set()  # Usamos un set para evitar duplicados
        
        for symbol in s:
            if symbol == 'E' and delta[state][symbol] is not None:
                current_state = state
                clausulas[state].add(current_state)  # El estado se puede llegar a sí mismo
                
                # Navegar por las transiciones epsilon
                while current_state is not None:
                    next_state = delta[current_state]['E']
                    if next_state is None or next_state in clausulas[state]:
                        break
                    clausulas[state].add(next_state)
                    current_state = next_state

        # Si no se encontró ninguna transición epsilon, el estado se mantiene solo
        if not clausulas[state]:
            clausulas[state].add(state)

    # Convertir los sets en listas para el formato de salida esperado
    return clausulas