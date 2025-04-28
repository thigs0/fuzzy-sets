import numpy as np
from cauchyfuzzyset import CauchyFuzzySet

class TakagiSugeno:
    """
    The TakagiSugeno use implementation of FuzzySet and Tnorm to calculate inference

    paramns
    rules: function that return np.array with values of activation  
    """
    def __init__(self, rules:callable, sets:list):
        self.w = rules
        self.sets = sets

    def inference(self, value:np.ndarray):
        return dp.dot(self.w(value), self.sets(value))/ np.sum(self.w(value))

class Mandani():
    """
    The TakagiSugeno use implementation of FuzzySet and Tnorm to calculate inference

    paramns
    rules: function that return np.array with values of activation  
    """
    def __init__(self, rules:callable, sets:list):
        self.w = rules
        self.sets = sets

    def inference(self, value:np.ndarray, tnorm):
        rules = self.w(value)
        sets = self.sets(value)
        #concatenar valor das tnormas
        return dp.dot(self.w(value), self.sets(value))/ np.sum(self.w(value))
import numpy as np
from typing import Callable, List, Dict, Tuple


class MamdaniInference:
    """
    """

    def __init__(self):
        self.rules: List[Tuple[Callable[[float], float], CauchyFuzzySet]] = []

    def add_rule(self, antecedent: Callable[[float], float], consequent):
        """
        Adiciona uma regra fuzzy.

        :param antecedent: função de pertinência (mu(x)) para a entrada
        :param consequent: conjunto fuzzy do tipo CauchyFuzzySet como saída
        """
        self.rules.append((antecedent, consequent))

    def infer(self, input_value: list, universe:np.ndarray) -> float:
        """
        Realiza a inferência Mamdani e retorna o valor defuzzificado.

        :param input_value: va:wqlor numérico de entrada
        :param resolution: número de pontos para amostragem na saída
        :return: valor defuzzificado (saída)
        """

        output_membership = np.zeros_like(universe)

        for antecedent, consequent in self.rules:
            
            degree = antecedent(input_value)  # grau de ativação
            # Min (t-norma) entre grau da regra e a saída fuzzy
            consequent_values = np.array([consequent.mu(x) for x in universe])
            output_membership = np.fmax(output_membership, np.fmin(degree, consequent_values))

        # Defuzzificação: centroide
        numerator = np.sum(universe * output_membership)
        denominator = np.sum(output_membership)

        if denominator == 0:
            return 0.0  # sem ativação

        return numerator / denominator

