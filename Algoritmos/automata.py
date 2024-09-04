import json
from typing import List, Tuple, Dict

# clase para el autómata
class Automaton:
    def __init__(self, Q: List[str], s: List[str], q0: str, F: List[str], p: List[Dict[str, str]]):
        self.Q = Q
        self.s = s
        self.q0 = q0
        self.F = F
        self.p = {(d["q"], d["a"]): d["q'"] for d in p}
    
    def transition(self, q: str, a: str) -> str:
        return self.p.get((q, a), None)
    
    def final_state(self, q: str, w: str) -> str:
        current_state = q
        for symbol in w:
            current_state = self.transition(current_state, symbol)
        return current_state
    
    def derivation(self, q: str, w: str) -> List[Tuple[str, str, str]]:
        transitions = []
        current_state = q
        for symbol in w:
            next_state = self.transition(current_state, symbol)
            transitions.append((current_state, symbol, next_state))
            current_state = next_state
        return transitions
    
    def accepted(self, q: str, w: str) -> bool:
        final_state = self.final_state(q, w)
        return final_state in self.F

# Función para cargar el autómata desde un archivo JSON
def load_automaton_from_file(filename: str) -> Automaton:
    with open(filename, "r") as file:
        data = json.load(file)
    return Automaton(data["Q"], data["s"], data["q0"], data["F"], data["p"])
