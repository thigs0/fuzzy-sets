import numpy as np

class Tnorm():
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self,tnorm:str, fset, sset, tconorm=None):
        self.__fset = fset
        self.__sset = sset
        self.tnorm_name = self.__valid_tnorm(tnorm.lower()) #add the valid tnorm function or give error
        self.tconorm_name = self.__valid_tconorm(tconorm)
        self.__tnorm, self.__tconorm = self.__tnorm_tconorm()

    def __valid_tnorm(self, tnorm):
        if tnorm in ("minimum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like minimum, product, lukasiewicz, drastic")

    def __valid_tconorm(self, tconorm):
        if tconorm in ("maximum", "probabilistic", "lukasiewicz", "drastic"):
            return tconorm
        elif tconorm == None: # If user pass only tnorm, find tconorm
            if self.tnorm_name == "minimum": return "maximum"
            elif self.tnorm_name == "product": return "probabilistic"
            elif self.tnorm_name == "lukasiewicz": return "lukasiewicz"
            elif self.tnorm_name == "drastic": return "drastic"
            else: return None
        else:
            raise ValueError("Use only DeMorgan Tnorm, like maximum, probabilistic, lukasiewicz, drastic")

    def __tnorm_tconorm(self):
        if self.tnorm_name == "minimum" or self.tconorm_name == "maximum":
            return [Tnorm_minimum(self.__fset, self.__sset), Tconorm_maximum(self.__fset, self.__sset)]
        elif self.tnorm_name == "product" or self.tconorm_name == "probabilistic":
            return [Tnorm_product(self.__fset, self.__sset), Tconorm_probabilitic_sum(self.__fset, self.__sset)]
        elif self.tnorm_name == "lukasiewicz" or self.tconorm_name == "lukasiewicz":
            return [Tnorm_Lukasiewicz( self.__fset, self.__sset), Tconorm_Lukasiewicz( self.__fset, self.__sset)]
        elif self.tnorm_name == "drastic" or self.tconorm_name == "drastic":
            return [Tnorm_Drastic( self.__fset, self.__sset), Tconorm_drastic( self.__fset, self.__sset)]

    def tnorm(self, value:float):
        return self.__tnorm.tnorm(value)

    def tconorm(self, value:float):
        return self.__tconorm.tconorm(value)


class Tnorm_minimum():
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("minimum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like minimum, product, lukasiewicz, drastic")

    def tnorm(self, value:float):
        return min(self.__fset.mu(value), self.__sset.mu(value))

class Tconorm_maximum():
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("maximum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like maximum, product, lukasiewicz, drastic")

    def tconorm(self, value:float):
        return max(self.__fset.mu(value), self.__sset.mu(value))

class Tnorm_product():
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("minimum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like minimum, product, lukasiewicz, drastic")

    def tnorm(self, value:float):
        return self.__fset.mu(value) * self.__sset.mu(value)

class Tconorm_probabilitic_sum(): ##
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("maximum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like maximum, product, lukasiewicz, drastic")

    def tconorm(self, value:float):
        return self.__fset.mu(value) + self.__sset.mu(value) - self.__fset.mu(value) * self.__sset.mu(value)

class Tnorm_Lukasiewicz():
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("minimum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like minimum, product, lukasiewicz, drastic")

    def tnorm(self, value:float):
        return max(0, self.__fset.mu(value) + self.__sset.mu(value) -1)

class Tconorm_Lukasiewicz(): ##
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("maximum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like maximum, product, lukasiewicz, drastic")

    def tconorm(self, value:float):
        return min(1, self.__fset.mu(value) + self.__sset.mu(value))

class Tnorm_Drastic():
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset
    def __valid_tnorm(self, tnorm):
        if tnorm in ("minimum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like minimum, product, lukasiewicz, drastic")
    def tnorm(self, value:float):
        out = None
        if self.__sset.mu(value) == 1: return self.__fset.mu(value)
        elif self.__fset.mu(value) ==1: return self.__sset.mu(value)
        else: return 0

class Tconorm_drastic(): ##
    """
            Calculate many tnorms minimum, product, lukasiewicz, drastic
            It is a function that requires two fuzzysets
    """
    def __init__(self, fset, sset):
        self.__fset = fset
        self.__sset = sset

    def __valid_tnorm(self, tnorm):
        if tnorm in ("maximum", "product", "lukasiewicz", "drastic"):
            return tnorm
        else:
            raise ValueError("Use only DeMorgan Tnorm, like maximum, product, lukasiewicz, drastic")

    def tconorm(self, value:float):
        out = None
        if self.__sset.mu(value) == 0: return self.__fset.mu(value)
        elif self.__fset.mu(value) ==0: return self.__sset.mu(value)
        else: return 1




