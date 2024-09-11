import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Algoritmos.subconjuntos import AFND_subconjunto

def subconjuntos_test():
    afnd = {
        "Q": ["q0", "q1", "q2", 'q3', 'q4'], 
        "s": ["0", "1", "E"], 
        "q0": "q0", 
        "F": ["q3", "q4"], 
        "p": [
            {"q": "q0", "a": "0", "q'": "q1"},
            {"q": "q0", "a": "1", "q'": "q1"},
            {"q": "q1", "a": "0", "q'": "q2"},
            {"q": "q1", "a": "1", "q'": "q2"},
            {"q": "q2", "a": "0", "q'": "q2"},
            {"q": "q2", "a": "1", "q'": "q3"},
            {"q": "q3", "a": "0", "q'": "q4"},
            {"q": "q3", "a": "1", "q'": "q4"},
            {"q": "q4", "a": "E", "q'": "q3"}

        ]
    }
    
    # Ejecutar la subconjuntos del AFND
    AFD = AFND_subconjunto(afnd)
    
    # Imprimir el AFD minimizado
    print("AFND a AFD:")
    print("Estados:", AFD["Q"])
    print("Símbolos:", AFD["s"])
    print("Estado inicial:", AFD["q0"])
    print("Estados de aceptación:", AFD["F"])
    print("Transiciones:")
    for transition in AFD["p"]:
        print(f"{transition['q']} -{transition['a']}-> {transition["q'"]}")

subconjuntos_test()