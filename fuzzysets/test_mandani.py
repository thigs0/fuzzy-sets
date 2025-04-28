import numpy as np
from typing import Callable, List, Tuple
from cauchyfuzzyset import CauchyFuzzySet
from tnf import TriangularFuzzySet
from tnorm import Tnorm, AND
from inference import MamdaniInference

#heavy of cloths
ml = TriangularFuzzyNumber(-20, 0, 20)
l = TriangularFuzzyNumber(10, 30, 50)
p = TriangularFuzzyNumber(40, 65, 90)
mp = TriangularFuzzyNumber(75,90,100)

#dirt cloths
ql = TriangularFuzzyNumber(-20,0,20)
s = TriangularFuzzyNumber(10,30,50)
ms = TriangularFuzzyNumber(40, 70, 100)
es = TriangularFuzzyNumber(80, 100, 120)

# Define regras com funções anônimas ou conjuntos fuzzy
def muito_pouco(x):return  TriangularFuzzyNumber(0,10,20)
def pouco(x):return  TriangularFuzzyNumber(20,30,40)
def moderado(x):return  TriangularFuzzyNumber(40,50,60)
def exagerado(x):return  TriangularFuzzyNumber(60,70,80)
def maximo(x):return  TriangularFuzzyNumber(80,100,120)

#tnorm
w1 = AND(tnorm="minimum", fset=ml, sset=ql)
w2 = AND(tnorm="minimum", fset=ml, sset=s)
w3 = AND(tnorm="minimum", fset=ml, sset=ms)
w4 = AND(tnorm="minimum", fset=ml, sset=es)

w5 = AND(tnorm="minimum", fset=l, sset=ql)
w6 = AND(tnorm="minimum", fset=l, sset=s)
w7 = AND(tnorm="minimum", fset=l, sset=ms)
w8 = AND(tnorm="minimum", fset=l, sset=es)

w9  = AND(tnorm="minimum", fset=p, sset=ql)
w10 = AND(tnorm="minimum", fset=p, sset=s)
w11 = AND(tnorm="minimum", fset=p, sset=ms)
w12 = AND(tnorm="minimum", fset=p, sset=es)

w13 = AND(tnorm="minimum", fset=mp, sset=ql)
w14 = AND(tnorm="minimum", fset=mp, sset=s)
w15 = AND(tnorm="minimum", fset=mp, sset=ms)
w16 = AND(tnorm="minimum", fset=mp, sset=es)

# Sistema de inferência
mi = MamdaniInference()
mi.add_rule(antecedent = w1, consequent = muito_pouco)
mi.add_rule(antecedent = w2, consequent = pouco)
mi.add_rule(antecedent = w3, consequent = moderado)
mi.add_rule(antecedent = w4, consequent = moderado)
mi.add_rule(antecedent = w5, consequent = pouco)
mi.add_rule(antecedent = w6, consequent = pouco)
mi.add_rule(antecedent = w7, consequent = moderado)
mi.add_rule(antecedent = w8, consequent = exagerado)
mi.add_rule(antecedent = w9, consequent = moderado)
mi.add_rule(antecedent = w10, consequent = moderado)
mi.add_rule(antecedent = w11, consequent = exagerado)
mi.add_rule(antecedent = w12, consequent = exagerado)
mi.add_rule(antecedent = w13, consequent = moderado)
mi.add_rule(antecedent = w14, consequent = exagerado)
mi.add_rule(antecedent = w15, consequent = maximo)
mi.add_rule(antecedent = w16, consequent = maximo)

# Inferência
saida = mi.infer(10, 15)
print("Saída defuzzificada:", saida)
