from typing import (
    Any,
    Iterator,
    Optional,
    Tuple,
    Union,
)

from numpy.polynomial.polynomial import Polynomial

from fuzzysets import utils


class CauchyFuzzySet:
    """
    Represents a CauchyFuzzySet (TFN).

    """
    __PEAK_OFFSET = 1.

    @classmethod
    def from_tuple(cls, t: Tuple[float, float, float]) -> "CauchyFuzzySet":
        """
        Creates a CauchyFuzzySet from a 3-tuple in the format (a,b,c).

        :raises ValueError: if t is not a 3-tuple or the values are not
        numeric or the following condition is not met:
        a != 0, b > 0.
        """
        if (isinstance(t, tuple) and len(t) == 3):
            a, b, c = t
            if a!=0 and b > 0:
                return cls(a, b, c)
            else:
                raise ValueError("Verify if a is not 0 and b is bigger that 0")
        else:
            raise ValueError("Expected a 3-tuple!")

    def __init__(self,
                 a: float = 1.,
                 b: Optional[float] = 1,
                 c: Optional[float] = 1) -> None:
        """
        :param a: a float is the range of curve.
        :param b: a float is how plane is the function.
        :param c: a float, it is x-axis to value 

        :raises ValueError: if the values are not numeric or the
        following condition is not met: a != 0, b>0.
        """
        self.__set_range(utils.to_float_if_int(a))
        self.__set_plane(utils.to_float_if_int(b))
        self.__set_xpoint(utils.to_float_if_int(c))

    def __set_range(self, a: float) -> None:
        utils.verify_is_numeric(a)
        self.__a = a

    def __set_plane(self, b: Optional[float]) -> None:
        self.__b = utils.default_if_none(
            b,
            1
        )
        utils.verify_is_numeric(b)

    def __set_xpoint(self, c: Optional[float]) -> None:
        self.__c = utils.default_if_none(
            c,
            1
        )
        utils.verify_is_numeric(c)

    def mu(self, x: float) -> float:
        """
        Try computes the membership degree of a real number.

        :param x: a float or int.
        :returns: a float in the range [0, 1].

        :raises ValueError: if x is not a number.
        """
        
        return 1 / (1 + abs((x - self.__c)/self.__a)**(2*self.__b))

    @classmethod
    def __verify_has_same_type(cls, other: Any) -> None:
        if (not isinstance(other, cls)):
            raise TypeError(
               f"Expected an instance of {cls.__name__!r}!"
            )

    def __neg__(self) -> "TriangularFuzzyNumber":
        return self.__class__(
            -self.__a,
            -self.__b,
            -self.__c
        )

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, self.__class__) and
                tuple(self) == tuple(other))

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __lt__(self, other: "CauchyFuzzySet") -> bool:
        self.__class__.__verify_has_same_type(other)
        return (self.__a == other.__a and
                ((self.__b > other.__b and self.__c <= other.__c) or
                 (self.__a >= other.__a and self.__c < other.__c)))

    def __gt__(self, other: "TriangularFuzzyNumber") -> bool:
        self.__class__.__verify_has_same_type(other)
        return other < self

    def __le__(self, other: "TriangularFuzzyNumber") -> bool:
        return self == other or self < other

    def __ge__(self, other: "TriangularFuzzyNumber") -> bool:
        self.__class__.__verify_has_same_type(other)
        return other <= self

    def __iter__(self) -> Iterator[float]:
        """
        :returns: a generator which yields the `left`, `peak` and
        `right` properties of the TFN, in that order. This makes it
        possible to unpack the number like so:
        `tfn = TriangularFuzzyNumber()`
        `left, peak, right = tfn`
        or to convert it to a tuple:
        `t = tuple(tfn)`
        """
        return iter((self.__a, self.__b, self.__c))

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"a={self.__a}, "
                f"b={self.__b}, "
                f"c={self.__c})")

    @property
    def alpha_cut(self) -> "AlphaCut":
        """
        :returns: an instance of AlphaCut - the alpha cut of the TFN.
        """
        return self.__alpha_cut

    @property
    def range(self) -> float:
        return self.__a

    @property
    def plane(self) -> float:
        return self.__b

    @property
    def xpoint(self) -> float:
        return self.__c
