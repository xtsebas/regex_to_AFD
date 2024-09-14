"""
Este modulo contiene la implementación de la conversión de una expresión regular en notación postfix a un autómata finito no determinista.
Se debe utilizar el algoritmo de Thompson o Glushkov para realizar la conversión.
Debe retornar un objeto json con la representación del autómata finito no determinista y sin epsilon.
La estructura del objeto json esta en el README.md
"""

class AFN:
    def __init__(self):
        self.estados = []
        self.simbolos = set()
        self.transiciones = []
        self.estado_inicial = None
        self.estados_aceptacion = []

    def agregar_estado(self):
        estado = len(self.estados)
        estado_nombre = f"q{estado}"
        self.estados.append(estado_nombre)
        return estado_nombre

    def agregar_transicion(self, origen, simbolo, destinos):
        if not isinstance(destinos, list):
            destinos = [destinos]
        for destino in destinos:
            self.transiciones.append({"q": origen, "a": simbolo, "q'": destino})
        if simbolo != '' and simbolo != 'E':  # Only add symbols that are not epsilon
            self.simbolos.add(simbolo)

    def establecer_inicial(self, estado):
        self.estado_inicial = estado

    def establecer_aceptacion(self, estado):
        if estado not in self.estados_aceptacion:
            self.estados_aceptacion.append(estado)

    def to_json(self):
        # Return the automaton in the specified JSON format
        return {
            "Q": self.estados,
            "s": list(self.simbolos),  # List of symbols (without epsilon)
            "q0": self.estado_inicial,
            "F": self.estados_aceptacion,
            "p": [  # Transitions
                {
                    "q": transicion["q"],
                    "a": transicion["a"] if transicion["a"] != '' else "E",  # Epsilon represented as "E"
                    "q'": transicion["q'"]  # Destination state
                }
                for transicion in self.transiciones
            ]
        }

def postfix_to_AFND(postfix: str) -> dict:
    pila = []
    afn = AFN()

    for simbolo in postfix:
        if simbolo == ' ':
            continue

        if simbolo.isalnum() or simbolo == 'E':  # Operand
            estado_inicial = afn.agregar_estado()
            estado_aceptacion = afn.agregar_estado()
            transition_symbol = '' if simbolo == 'E' else simbolo
            afn.agregar_transicion(estado_inicial, transition_symbol, estado_aceptacion)
            pila.append((estado_inicial, estado_aceptacion))

        elif simbolo == '*':  # Estrella Kleene
            estado_anterior_inicial, estado_anterior_aceptacion = pila.pop()
            estado_inicial = afn.agregar_estado()
            estado_aceptacion = afn.agregar_estado()

            # Epsilon transitions for Kleene Star
            afn.agregar_transicion(estado_anterior_aceptacion, '', [estado_anterior_inicial, estado_aceptacion])
            afn.agregar_transicion(estado_inicial, '', [estado_anterior_inicial, estado_aceptacion])

            pila.append((estado_inicial, estado_aceptacion))

        elif simbolo == '|':  # Union
            estado2_inicial, estado2_aceptacion = pila.pop()
            estado1_inicial, estado1_aceptacion = pila.pop()
            estado_inicial = afn.agregar_estado()
            estado_aceptacion = afn.agregar_estado()

            # Epsilon transitions for Union
            afn.agregar_transicion(estado_inicial, '', [estado1_inicial, estado2_inicial])
            afn.agregar_transicion(estado1_aceptacion, '', estado_aceptacion)
            afn.agregar_transicion(estado2_aceptacion, '', estado_aceptacion)

            pila.append((estado_inicial, estado_aceptacion))

        elif simbolo == '?':  # Concatenation
            estado2_inicial, estado2_aceptacion = pila.pop()
            estado1_inicial, estado1_aceptacion = pila.pop()

            # Epsilon transition for Concatenation
            afn.agregar_transicion(estado1_aceptacion, '', estado2_inicial)

            pila.append((estado1_inicial, estado2_aceptacion))

        else:
            raise ValueError(f"Unknown symbol: {simbolo}")

    # Establish the initial and accepting states
    estado_inicial, estado_aceptacion = pila.pop()
    afn.establecer_inicial(estado_inicial)
    afn.establecer_aceptacion(estado_aceptacion)

    # Return the automaton in JSON format
    return afn.to_json()
