import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Algoritmos.postfix import regex_to_postfix, insertar_concatenacion # func test

GREEN = "\033[32m"
RESET = "\033[0m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED = "\033[31m"

regex_postfix_test = {
    "a(a+b)|b": "aab+b|",
    "abc": "abc",
    "ab|c": "abc|",
    "a(bb)+c": "abbc+",
    "abc(a|v)": "abcav|",
    "(b|b)*abb(a|b)*" : "bb|*abbab|*"
    }


def test(regex_hash):
    passed = 0
    for regex in regex_hash:
        
        postfix_output = regex_to_postfix(regex=regex)
        
        if postfix_output == regex_hash[regex]:
            
            passed += 1
            debug = f"infix regex --> {BLUE}{regex}{RESET} postfix regex -> {MAGENTA}{postfix_output}{RESET}"            
            print(f"{YELLOW}{"="*len(debug)}{RESET}")
            print(f"REGEX: {CYAN}{regex}{RESET}")
            print(f"expresion formateada: {CYAN}{insertar_concatenacion(regex)}{RESET}")
            print(debug)
            print(f"{GREEN}PASSED{RESET}")
            
        else:
            debug = f"infix regex --> {BLUE}{regex}{RESET} postfix regex -> {MAGENTA}{regex}{RESET}"            
            print(f"{YELLOW}{"="*len(debug)}{RESET}")
            print("correct postfix -> "+regex_hash[regex])
            print(f"{RED}FAIL{RESET}")
            print("=" * len(debug))
    print("accuracy -----> " + str((passed/len(regex_hash))*100)+"%")
            
            
test(regex_postfix_test)
