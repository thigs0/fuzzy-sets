from typing import (
    Any,
    Iterator,
    Optional,
    Tuple,
    Union,
)

from numpy.polynomial.polynomial import Polynomial

from fuzzysets import utils

class TriangularFuzzyNumber:
    """
    Represents a triangular fuzzy number (TFN).

    Each TFN can be uniquely represented as a 3-tuple of real numbers
    (left, peak, right) (l, n and r below) where:
     - peak is the number whose membership degree is 1, that is, the
       number being modeled
     - left (< peak) and right (> peak) determine the fuzzy number's
       membership function:
        mu(x) = 0, x ∈ (-inf, l) U (r, +inf)
        mu(x) = (x - l) / (n - l), l <= x <= n
        mu(x) = (r - x) / (r - n), n <= x <= r
    """
    __PEAK_OFFSET = 1.

    @classmethod
    def from_tuple(cls, t: Tuple[float, float, float]) -> "TriangularFuzzyNumber":
        """
        Creates a TFN from a 3-tuple in the format (left, peak, right).
        Equivalent to `TNF(t[1], t[0], t[2])`.

        :raises ValueError: if t is not a 3-tuple or the values are not
        numeric or the following condition is not met:
        l < n < r.
        """
        if (isinstance(t, tuple) and len(t) == 3):
            l, n, r = t
            return cls(n, l, r)
        else:
            raise ValueError("Expected a 3-tuple!")

    def __init__(self,
                 n: float = 0.,
                 l: Optional[float] = None,
                 r: Optional[float] = None) -> None:
        """
        :param n: a float or int - the peak of the FN. Defaults to 0.0.
        :param l: a float or int - the 'left' component of the FN. If
        omitted or `None`, defaults to `n - PEAK_OFFSET`.
        :param r: a float or int - the 'right' component of the FN. If
        omitted or `None`, defaults to `n + PEAK_OFFSET`.

        :raises ValueError: if the values are not numeric or the
        following condition is not met: l < n < r.
        """
        self.__set_peak(utils.to_float_if_int(n))
        self.__set_left(utils.to_float_if_int(l))
        self.__set_right(utils.to_float_if_int(r))
        self.__alpha_cut = AlphaCut.for_tfn(self)

    def __set_peak(self, n: float) -> None:
        utils.verify_is_numeric(n)
        self.__n = n

    def __set_left(self, left: Optional[float]) -> None:
        left = utils.default_if_none(
            left,
            self.__n - self.__class__.__PEAK_OFFSET
        )
        utils.verify_is_numeric(left)

        if (left < self.__n):
            self.__l = left
        else:
            raise ValueError(
                f"l ({left}) >= n ({self.__n})!"
            )

    def __set_right(self, right: Optional[float]) -> None:
        right = utils.default_if_none(
            right,
            self.__n + self.__class__.__PEAK_OFFSET
        )
        utils.verify_is_numeric(right)

        if (self.__n < right):
            self.__r = right
        else:
            raise ValueError(
                f"r ({right}) <= n ({self.__n})!"
            )

    def mu(self, x: float) -> float:
        """
        Computes the membership degree of a real number.

        :param x: a float or int.
        :returns: a float in the range [0, 1].

        :raises ValueError: if x is not a number.
        """

        if (x > self.__l and x <= self.__n):
            return (x - self.__l)/(self.__n - self.__l)
        elif x > self.__n and x < self.__r:
            return -(self.__r - x)/(self.__l - self.__n)
        else:
            return 0

    def __add__(self, other: "TriangularFuzzyNumber") -> "TriangularFuzzyNumber":
        return self.__operation(other, op_name="_add")

    def __operation(self,
                    other: "TriangularFuzzyNumber",
                    op_name: str) -> "TriangularFuzzyNumber":
        self.__class__.__verify_has_same_type(other)
        op = getattr(self.__alpha_cut, op_name)
        result_polys = op(other.alpha_cut)
        left, right = result_polys(0.)
        peak = result_polys(1.)[0]

        return self.__class__(peak, left, right)

    @classmethod
    def __verify_has_same_type(cls, other: Any) -> None:
        if (not isinstance(other, cls)):
            raise TypeError(
               f"Expected an instance of {cls.__name__!r}!"
            )

    def __sub__(self, other: "TriangularFuzzyNumber") -> "TriangularFuzzyNumber":
        return self.__operation(other, op_name="_sub")

    def __mul__(self, other: "TriangularFuzzyNumber") -> "TriangularFuzzyNumber":
        return self.__operation(other, op_name="_mul")

    def __truediv__(self, other: "TriangularFuzzyNumber") -> "TriangularFuzzyNumber":
        return self.__operation(other, op_name="_div")

    def __neg__(self) -> "TriangularFuzzyNumber":
        return self.__class__(
            -self.__n,
            -self.__r,
            -self.__l
        )

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, self.__class__) and
                tuple(self) == tuple(other))

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __lt__(self, other: "TriangularFuzzyNumber") -> bool:
        self.__class__.__verify_has_same_type(other)
        return (self.__n == other.__n and
                ((self.__l > other.__l and self.__r <= other.__r) or
                 (self.__l >= other.__l and self.__r < other.__r)))

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
        return iter((self.__l, self.__n, self.__r))

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"l={self.__l}, "
                f"n={self.__n}, "
                f"r={self.__r})")

    @property
    def alpha_cut(self) -> "AlphaCut":
        """
        :returns: an instance of AlphaCut - the alpha cut of the TFN.
        """
        return self.__alpha_cut

    @property
    def peak(self) -> float:
        return self.__n

    @property
    def left(self) -> float:
        return self.__l

    @property
    def right(self) -> float:
        return self.__r


class AlphaCut:
    """
    Represents the alpha-cut of a TFN, parameterised by alpha:
    [left + alpha * (peak - left), right - alpha (right - peak)] =
    [a + alpha * b, c - alpha * d] = [p, q]
    """
    @classmethod
    def for_tfn(cls, tfn: TriangularFuzzyNumber) -> "AlphaCut":
        """
        :param tfn: a TriangularFuzzyNumber instance.
        """
        p = Polynomial([tfn.left, tfn.peak - tfn.left])
        q = Polynomial([tfn.right, tfn.peak - tfn.right])

        return cls(p, q)

    def __init__(self, p: Polynomial, q: Polynomial) -> None:
        """
        Non-public constructor.
        """
        self.__p = p
        self.__q = q

    def _add(self, other: "AlphaCut") -> "_PolynomialPair":
        return _PolynomialPair(
            self.__p + other.__p,
            self.__q + other.__q
        )

    def _sub(self, other: "AlphaCut") -> "_PolynomialPair":
        return _PolynomialPair(
            self.__p - other.__q,
            self.__q - other.__p
        )

    def _mul(self, other: "AlphaCut") -> "_PolynomialPair":
        return _PolynomialPair(
            self.__p * other.__p,
            self.__q * other.__q
        )

    def _div(self, other: "AlphaCut") -> "_PolynomialPair":
        return _PolynomialPair(
            (self.__p, other.__q),
            (self.__q, other.__p)
        )

    def for_alpha(self, alpha: float) -> Tuple[float, float]:
        """
        :param alpha: a float between 0 and 1.
        :returns: a two tuple representing the range
        [a + alpha * b, c - alpha * d]

        :raises ValueError: if `alpha` is not a float in the range
        [0, 1].
        """
        alpha = utils.to_float_if_int(alpha)
        utils.validate_alpha(alpha)

        return (self.__p(alpha), self.__q(alpha))

    def __str__(self) -> str:
        return f"[{self.__as_str()}]"

    def __as_str(self) -> str:
        a, b = self.__p.coef[:2]
        c, d = self.__q.coef[:2]

        return (f"{a} + alpha * {b}, "
                f"{c} + alpha * {d}")

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"{self.__as_str()})")


class _PolynomialPair:
    """
    Non-public class that represents the result of an operation on
    TFN alpha cuts.
    """
    PolynomialTuple = Tuple[Polynomial, Polynomial]

    def __init__(self,
                 lhs: Union[Polynomial, PolynomialTuple],
                 rhs: Union[Polynomial, PolynomialTuple]) -> None:
        self.__lhs = lhs
        self.__rhs = rhs

    def __call__(self, x: float) -> Tuple[float, float]:
        return (
            self.__class__.__value_of(self.__lhs, x),
            self.__class__.__value_of(self.__rhs, x)
        )

    @staticmethod
    def __value_of(p: Union[Polynomial, PolynomialTuple],
                   x: float) -> float:
        if (isinstance(p, tuple)):
            numerator, denominator = p
            return numerator(x) / denominator(x)
        else:
            return p(x)
