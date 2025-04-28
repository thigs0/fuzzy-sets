import numpy as np
from typing import Callable, List, Tuple
from cauchyfuzzyset import CauchyFuzzySet
from tfn import TriangularFuzzyNumber
from tnorm import Tnorm, AND
from inference import MamdaniInference

#heavy of cloths
ml = TriangularFuzzyNumber(0, -20, 20)
l = TriangularFuzzyNumber(30,10, 50)
p = TriangularFuzzyNumber(65, 40, 90)
mp = TriangularFuzzyNumber(90, 75,100)

#dirt cloths
ql = TriangularFuzzyNumber(0, -20, 20)
s = TriangularFuzzyNumber(30, 10, 50)
ms = TriangularFuzzyNumber(70, 40, 100)
es = TriangularFuzzyNumber(100, 80, 120)

# Define regras com funções anônimas ou conjuntos fuzzy
muito_pouco = TriangularFuzzyNumber(10, 0, 20)
pouco = TriangularFuzzyNumber(30, 20, 40)
moderado = TriangularFuzzyNumber(50, 40 ,60)
exagerado = TriangularFuzzyNumber(70, 60 ,80)
maximo = TriangularFuzzyNumber(100, 80 ,120)

#tnorm
p1,p2 = 10,15
ps = [p1, p2]
w1 = AND([ml, ql])
w2 = AND([ml, s])
w3 = AND([ml, ms])
w4 = AND([ml, es])

w5 = AND([l, ql])
w6 = AND([l, s])
w7 = AND([l, ms])
w8 = AND([l, es])

w9  = AND([p, ql])
w10 = AND([p, s])
w11 = AND([p, ms])
w12 = AND([p, es])

w13 = AND([mp, ql])
w14 = AND([mp, s])
w15 = AND([mp, ms])
w16 = AND([mp, es])

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
saida = mi.infer(ps, np.linspace(0, 100, 1000))
print("Saída defuzzificada:", saida)
