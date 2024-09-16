from View.simulacion import simular_AFD 
import json


with open('input.json', 'r') as archivo:
    # Carga el contenido del archivo JSON
    datos = json.load(archivo)

for regex, cadena in datos.items():
    simular_AFD( regex = regex , cadena = cadena)
    