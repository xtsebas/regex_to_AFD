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
        self.estados.append(f"q{estado}")
        return f"q{estado}"

    def agregar_transicion(self, origen, simbolo, destino):
        self.transiciones.append({"q": origen, "a": simbolo, "q'": destino})
        if simbolo != '':  # Solo agregar símbolos que no sean epsilon
            self.simbolos.add(simbolo)

    def establecer_inicial(self, estado):
        self.estado_inicial = estado

    def establecer_aceptacion(self, estado):
        self.estados_aceptacion.append(estado)

    def to_json(self):
        # Retornar el autómata en el formato JSON especificado
        return {
            "Q": self.estados,
            "s": list(filter(lambda x: x != '', self.simbolos)),  # Lista de símbolos (sin epsilon)
            "q0": self.estado_inicial,
            "F": self.estados_aceptacion,
            "p": [  # Transiciones
                {
                    "q": transicion["q"],
                    "a": transicion["a"] if transicion["a"] != "" else "E",  # Epsilon se representa como "E"
                    "q'": transicion["q'"]  # Lista de estados destino
                }
                for transicion in self.transiciones
            ]
        }

def postfix_to_AFND(postfix: str) -> dict:
    pila = []
    afn = AFN()

    for simbolo in postfix:
        if simbolo.isalnum():  # Si es un símbolo del alfabeto
            estado_inicial = afn.agregar_estado()
            estado_aceptacion = afn.agregar_estado()
            afn.agregar_transicion(estado_inicial, simbolo, [estado_aceptacion])
            pila.append((estado_inicial, estado_aceptacion))

        elif simbolo == '*':  # Cerradura de Kleene
            estado_inicial = afn.agregar_estado()
            estado_aceptacion = afn.agregar_estado()
            estado_anterior_inicial, estado_anterior_aceptacion = pila.pop()

            # Transiciones sin epsilon (revisar con el algoritmo de Thompson para cerrar bucles)
            afn.agregar_transicion(estado_inicial, '', [estado_anterior_inicial])
            afn.agregar_transicion(estado_anterior_aceptacion, '', [estado_anterior_inicial])
            afn.agregar_transicion(estado_anterior_aceptacion, '', [estado_aceptacion])
            afn.agregar_transicion(estado_inicial, '', [estado_aceptacion])
            
            pila.append((estado_inicial, estado_aceptacion))

        elif simbolo == '|':  # Unión
            estado_inicial = afn.agregar_estado()
            estado_aceptacion = afn.agregar_estado()
            estado2_inicial, estado2_aceptacion = pila.pop()
            estado1_inicial, estado1_aceptacion = pila.pop()

            # Transiciones para la unión
            afn.agregar_transicion(estado_inicial, '', [estado1_inicial, estado2_inicial])
            afn.agregar_transicion(estado1_aceptacion, '', [estado_aceptacion])
            afn.agregar_transicion(estado2_aceptacion, '', [estado_aceptacion])

            pila.append((estado_inicial, estado_aceptacion))

        elif simbolo == '.':  # Concatenación
            estado2_inicial, estado2_aceptacion = pila.pop()
            estado1_inicial, estado1_aceptacion = pila.pop()

            # No usar epsilon en concatenación
            afn.agregar_transicion(estado1_aceptacion, '', [estado2_inicial])

            pila.append((estado1_inicial, estado2_aceptacion))

    # Establecer los estados inicial y de aceptación
    estado_inicial, estado_aceptacion = pila.pop()
    afn.establecer_inicial(estado_inicial)
    afn.establecer_aceptacion(estado_aceptacion)

    # Retornar el autómata en formato JSON
    return afn.to_json()