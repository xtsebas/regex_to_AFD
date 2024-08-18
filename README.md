## Flujo de Trabajo del Proyecto

Este proyecto sigue un flujo de trabajo estructurado en cinco módulos clave, cada uno con un rol específico en la construcción y minimización de autómatas finitos deterministas (AFD). A continuación se describe cómo interactúan estos módulos:

### 1. `postfix.py`

- **Función**: Convierte una expresión regular en notación infija a notación postfix (notación polaca inversa) con el algoritmo Shunting Yard.
- **Objetivo**: Facilitar la manipulación de la expresión regular en los pasos subsiguientes.

### 2. `AFND.py`

- **Función**: Construye un Autómata Finito No Determinista (AFND) a partir de la expresión regular en notación postfix.
- **Objetivo**: Aplicar el algoritmo de Thompson o Glushkov para generar el AFD.

### 3. `subconjuntos.py`

- **Función**: Transforma un Autómata Finito No Determinista (AFND) en un Autómata Finito Determinista (AFD) utilizando el  algoritmo de Construccion de Subconjuntos.
- **Objetivo**: Determinizar el autómata para eliminar ambigüedades en la aceptación del lenguaje.

### 4. `minAFD.py`

- **Función**: Aplica un algoritmo de minimización de estados al AFD obtenido, reduciendo el número de estados sin cambiar el lenguaje aceptado.
- **Objetivo**: Simplificar el AFD, haciéndolo más eficiente.

### 5. `automata.py`

- **Función**: Maneja la creación, manipulación y representación de autómatas. Integra los pasos anteriores en un flujo coherente.
- **Objetivo**: Proveer una interfaz para crear y visualizar autómatas minimizados.

### Resumen del Flujo

1. **Expresión Regular** → `postfix.py` = **Notación Postfix**
2. `postfix.py` → `AFND.py` = **Construcción del AFND**
3. `AFND.py` → `subconjuntos.py` = **Determinización del AFD**
4. `subconjuntos.py` → `minAFD.py` = **Minimización del AFD**
5. `minAFD.py` → `automata.py` = **el main puede jugar con el AFD y el `automata.py`**
