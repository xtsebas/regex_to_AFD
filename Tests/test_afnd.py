import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Algoritmos.AFND import postfix_to_AFND  # Importar la función que convierte postfix a AFND

def test_afnd():
    # Ejemplos de expresiones regulares en notación postfix
    pruebas = {
        "(b|b)*abb(a|b)*": "bb|*abbab|*",  # Ejemplo de proyecto
        "b*(z*|o)*s": "b*z*o|*s",
        "55((88)*|3)*zzx*": "5588*3|*zzx*",
        "(0|(1(01*(00)*0)*1)*)": "0101*00*0*1*|",  # Ejemplo de clase
        "((E|a)|b*)*": "Ea|b*|*"  # Epsilon test
    }

    for regex, postfix in pruebas.items():
        print(f"\nProbando expresión regular: {regex}")
        print(f"Notación postfix: {postfix}")
        
        # Convertir la expresión postfix a un AFND en formato JSON
        afnd = postfix_to_AFND(postfix)
        
        # Imprimir el resultado en formato JSON
        print("Autómata finito no determinista generado (AFND):")
        print(json.dumps(afnd, indent=4))  # Mostrar el autómata generado con indentación

if __name__ == "__main__":
    test_afnd()