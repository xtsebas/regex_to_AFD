import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Algoritmos.minAFD import minAFD

def minAFD_test():
    # Definición del AFD
    AFD = {
        "Q": ["q0", "q1", "q2", "q3", "q4", "q5"], 
        "s": ["0", "1"], 
        "q0": "q0", 
        "F": ["q3", "q4", "q5"], 
        "p": [
        {"q": "q0", "a": "0", "q'": "q1"},
        {"q": "q0", "a": "1", "q'": "q1"},
        {"q": "q1", "a": "0", "q'": "q2"},
        {"q": "q1", "a": "1", "q'": "q2"},
        {"q": "q2", "a": "0", "q'": "q2"},
        {"q": "q2", "a": "1", "q'": "q3"},
        {"q": "q3", "a": "0", "q'": "q4"},
        {"q": "q3", "a": "1", "q'": "q4"},
        {"q": "q4", "a": "0", "q'": "q5"},
        {"q": "q4", "a": "1", "q'": "q5"},
        {"q": "q5", "a": "0", "q'": "q5"},
        {"q": "q5", "a": "1", "q'": "q5"},
        ]
    } 
    
    # Ejecutar la minimización del AFD
    minimized_AFD = minAFD(AFD)
    
    # Imprimir el AFD minimizado
    print("AFD Minimizado:")
    print("Estados:", minimized_AFD["Q"])
    print("Símbolos:", minimized_AFD["s"])
    print("Estado inicial:", minimized_AFD["q0"])
    print("Estados de aceptación:", minimized_AFD["F"])
    print("Transiciones:")
    for transition in minimized_AFD["p"]:
        print(f"{transition['q']} -{transition['a']}-> {transition["q'"]}")
        
minAFD_test()