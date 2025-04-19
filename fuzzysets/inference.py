import numpy as numpy

class TakagiSugeno():
    """
    The TakagiSugeno use implementation of FuzzySet and Tnorm to calculate inference

    paramns
    rules: function that return np.array with values of activation  
    """
    def __init__(self, rules:Callable, sets:list):
        self.w = rules
        self.sets = sets

    def inference(self, value:np.darray):
        return dp.dot(self.w(value), self.sets(value))/ np.sum(self.w(value))

class Mandani():
    """
    The TakagiSugeno use implementation of FuzzySet and Tnorm to calculate inference

    paramns
    rules: function that return np.array with values of activation  
    """
    def __init__(self, rules:Callable, sets:list):
        self.w = rules
        self.sets = sets

    def inference(self, value:np.darray, tnorm):
        rules = self.w(value)
        sets = self.sets(value)
        #concatenar valor das tnormas
        return dp.dot(self.w(value), self.sets(value))/ np.sum(self.w(value))
