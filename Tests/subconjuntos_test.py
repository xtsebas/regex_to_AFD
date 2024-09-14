import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Algoritmos.subconjuntos import AFND_subconjunto

def subconjuntos_test():
    afnd1 = {
        "Q": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20", "q21", "q22", "q23", "q24", "q25"],
        "s": ["0", "1", "E"],
        "q0": "q4",
        "F": ["q25"],
        "p": [
            {"q": "q0", "a": "0", "q'": "q1"},
            {"q": "q2", "a": "1", "q'": "q3"},
            {"q": "q4", "a": "E", "q'": "q0"},
            {"q": "q4", "a": "E", "q'": "q2"},
            {"q": "q1", "a": "E", "q'": "q5"},
            {"q": "q3", "a": "E", "q'": "q5"},
            {"q": "q6", "a": "0", "q'": "q7"},
            {"q": "q8", "a": "1", "q'": "q9"},
            {"q": "q10", "a": "E", "q'": "q6"},
            {"q": "q10", "a": "E", "q'": "q8"},
            {"q": "q7", "a": "E", "q'": "q11"},
            {"q": "q9", "a": "E", "q'": "q11"},
            {"q": "q5", "a": "E", "q'": "q10"},
            {"q": "q12", "a": "0", "q'": "q13"},
            {"q": "q13", "a": "E", "q'": "q12"},
            {"q": "q13", "a": "E", "q'": "q15"},
            {"q": "q14", "a": "E", "q'": "q12"},
            {"q": "q14", "a": "E", "q'": "q15"},
            {"q": "q11", "a": "E", "q'": "q14"},
            {"q": "q16", "a": "1", "q'": "q17"},
            {"q": "q15", "a": "E", "q'": "q16"},
            {"q": "q18", "a": "0", "q'": "q19"},
            {"q": "q20", "a": "1", "q'": "q21"},
            {"q": "q22", "a": "E", "q'": "q18"},
            {"q": "q22", "a": "E", "q'": "q20"},
            {"q": "q19", "a": "E", "q'": "q23"},
            {"q": "q21", "a": "E", "q'": "q23"},
            {"q": "q23", "a": "E", "q'": "q22"},
            {"q": "q23", "a": "E", "q'": "q25"},
            {"q": "q24", "a": "E", "q'": "q22"},
            {"q": "q24", "a": "E", "q'": "q25"},
            {"q": "q17", "a": "E", "q'": "q24"}
        ]
    }
    
    afnd2 = {
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
    AFD = AFND_subconjunto(afnd1)
    
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