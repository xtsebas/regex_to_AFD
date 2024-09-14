from Algoritmos.postfix import regex_to_postfix
from Algoritmos.AFND import postfix_to_AFND
from Algoritmos.subconjuntos import AFND_subconjunto
from Algoritmos.minAFD import minAFD
import json
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BRIGHT_BLUE = "\033[94m"
MAGENTA = "\033[35m"
BRIGHT_GREEN = "\033[92m"
MATRIX_GREEN = "\033[38;5;82m" 
RED = "\033[31m"

expresiones = [
    "(b|b)abb(a|b)",
    "((E|a)|b*)",
    "(0|(1(01*(00)0)*1))",
    "(0|1)(0|1)0*1(0|1)"
]



for regex in expresiones: 
    
    #mostrando regex
    print(f'{GREEN}{"-"*(len(regex)+11)}{GREEN}\n {RED}REGEX -> {RED}{YELLOW}{regex}{YELLOW}  \n{GREEN}{"-"*(len(regex)+11)}{GREEN}{RESET}')    
    
    #regex a postfix con shunting yard
    postfix = regex_to_postfix( regex = regex )
    print(f'{GREEN}{"-"*(len(postfix)+22)}{GREEN}\n{RED} REGEX -> {MAGENTA}POSTFIX{MAGENTA} -> {RED}{MATRIX_GREEN}{postfix}{MATRIX_GREEN} \n{GREEN}{"-"*(len(postfix)+22)}{GREEN}{RESET}')    

    #postfix a afnd con thompson
    afnd = postfix_to_AFND (postfix = postfix )
    print(f' {MAGENTA}POSTFIX -> {MAGENTA}{RESET}AFND\n{json.dumps(afnd, indent=4)}')

# regex = "(0|1)(0|1)0*1(0|1)*"
# print(f"Regex: {regex}")
# regex_postfix = regex_to_postfix(regex)
# print(f"Postfix: {regex_postfix}")

# print("AFND:")
# afnd = postfix_to_AFND(regex_postfix)
# print(json.dumps(afnd, indent=2))

# print("AFD:")
# afd = AFND_subconjunto(afnd)
# print(json.dumps(afd, indent=2))

# print("min AFD")
# mind_afd = minAFD(afd)
# print(json.dumps(mind_afd, indent=2))