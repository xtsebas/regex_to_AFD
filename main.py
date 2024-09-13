from Algoritmos.postfix import regex_to_postfix
from Algoritmos.AFND import postfix_to_AFND
from Algoritmos.subconjuntos import AFND_subconjunto
from Algoritmos.minAFD import minAFD

#1
regex = "(0|1)(0|1)0*1(0|1)*"
print(f"regex --> {regex}")
regex_postfix = regex_to_postfix(regex)
print(f"regex en postfix {regex_postfix}")

#2
print("AFND")
afnd = postfix_to_AFND(regex_postfix)
print(afnd)

#3
print("AFD")
afd = AFND_subconjunto(afnd)
print(afd)

#4
print("MIN AFD")
min_afd = minAFD(afd)
print(min_afd)


