import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.postfix import regex_to_postfix
from Controller.AFND import postfix_to_AFND
from Controller.subconjuntos import AFND_subconjunto
from Controller.minAFD import minAFD

regex = "(0?1)(0?1)0*1(0?1)*"

postfix = regex_to_postfix(regex)
print("Postfix:", postfix,'\n')

"""
Aqui iria el flujo de postfix a AFND
al tenerlo, eliminar el comentario y el afnd que se crea abajo
"""
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

AFD = AFND_subconjunto(afnd)

print("------------------------------------\nAFND a AFD:")
print("Estados:", AFD["Q"])
print("Símbolos:", AFD["s"])
print("Estado inicial:", AFD["q0"])
print("Estados de aceptación:", AFD["F"])
print("Transiciones:")
for transition in AFD["p"]:
    print(f"{transition['q']} -{transition['a']}-> {transition["q'"]}")
print("\n")

minimized_AFD = minAFD(AFD)
print("------------------------------------\nAFD Minimizado:")
print("Estados:", minimized_AFD["Q"])
print("Símbolos:", minimized_AFD["s"])
print("Estado inicial:", minimized_AFD["q0"])
print("Estados de aceptación:", minimized_AFD["F"])
print("Transiciones:")
for transition in minimized_AFD["p"]:
    print(f"{transition['q']} -{transition['a']}-> {transition["q'"]}")
print("\n")