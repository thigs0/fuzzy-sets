import os
import sys
import time
import random
import pygame
import numpy as np
from fuzzysets import TriangularFuzzyNumber, AND, MamdaniInference, TakagiSugenoInference

# ——— Configurações Fuzzy —————————————————————————————————————————————
#fcactus_near = TriangularFuzzyNumber(r=210, n=100, l=90)
dist_low = TriangularFuzzyNumber(r=0.17, n=0.1, l=0)
dist_high = TriangularFuzzyNumber(r=1, n=0.5, l=0.1)

#vel_low = TriangularFuzzyNumber(r=7, n=6, l=5)
#vel_high = TriangularFuzzyNumber(r=12, n=9, l=6.999)

#scactus_near = TriangularFuzzyNumber(r=900, n=300, l=90)

#Mamdani Method Fuzzy results:
jump_zero     = TriangularFuzzyNumber(r=0.0001,   n=0,   l=-1)
jump_low      = TriangularFuzzyNumber(r=0.401,   n=0.4,   l=0)
jump_high     = TriangularFuzzyNumber(r=1,   n=0.9,   l=0.8)

#functions for Takagi-Sugeno Method:
#def jump_zero(x):return 0
#def jump_low(x): return 0.4
#def jump_high(x): return 1




#rules for x = distance:
#w1 = AND([dist_low,dist_low])
#w2 = AND([dist_high,dist_high])

#rules for x1 = distance; x2 = velocity
w1 = AND([dist_low,vel_low])
w2 = AND([dist_high,vel_low])
w3 = AND([dist_low,vel_high])
w4 = AND([dist_high,vel_high])

#w1 = AND([dist_low,vel_low])
#w2 = AND([dist_med,vel_low])
#w3 = AND([dist_high,vel_low])
#w4 = AND([dist_low,vel_high])
#w5 = AND([dist_med,vel_high])
#w6 = AND([dist_high,vel_high])


#w1 = AND([fcactus_near, player_vel])

#Mamdani method:
mi = MamdaniInference()

#Takagi-Sugeno method:
#mi = TakagiSugenoInference()


#rules for x = distance:
#mi.add_rule(antecedent=w1, consequent=jump_high)
#mi.add_rule(antecedent=w2, consequent=jump_zero)
#rules for x1 = distance; x2 = velocity
mi.add_rule(antecedent=w1, consequent=jump_low)
mi.add_rule(antecedent=w2, consequent=jump_zero)
mi.add_rule(antecedent=w3, consequent=jump_high)
mi.add_rule(antecedent=w4, consequent=jump_zero)


fuzzy_value = mi.infer([norm_dist], np.linspace(0, 100, 500))