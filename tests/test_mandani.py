# Supondo que CauchyFuzzySet já foi importado

# Define conjuntos fuzzy para saída
baixa = CauchyFuzzySet(1.0, 2.0, 2.0)
media = CauchyFuzzySet(1.0, 2.0, 5.0)
alta = CauchyFuzzySet(1.0, 2.0, 8.0)

# Define regras com funções anônimas ou conjuntos fuzzy
def entrada_baixa(x): return 1 / (1 + ((x - 2)/1)**2)
def entrada_media(x): return 1 / (1 + ((x - 5)/1)**2)
def entrada_alta(x): return 1 / (1 + ((x - 8)/1)**2)

# Sistema de inferência
mi = MamdaniInference()
mi.add_rule(entrada_baixa, baixa)
mi.add_rule(entrada_media, media)
mi.add_rule(entrada_alta, alta)

# Inferência
saida = mi.infer(4.5)
print("Saída defuzzificada:", saida)
