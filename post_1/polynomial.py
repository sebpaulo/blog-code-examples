from __future__ import annotations
from collections.abc import Sequence


class Polynomial:
    """Simple class to illustrate the use of special methods in python.

    Parameters
    -----------
    - coefficients: sequence of numbers as coefficients in order of
      increasing degree

    >>> p = Polynomial((2.0, 4.0, -1.0))
    >>> p
    Polynomial((2.0, 4.0, -1.0))
    >>> print(p)
    -x^2 + 4x + 2
    >>> q = Polynomial((4.0, -1.0, -3.0, 0.0, 5.0))
    >>> p + q
    Polynomial((6.0, 3.0, -4.0, 0.0, 5.0))
    >>> p * 2
    Polynomial((4.0, 8.0, -2.0))
    """

    def __init__(self, coefficients: Sequence[float]) -> None:
        self.coefficients = tuple(float(coef) for coef in coefficients)

    def __add__(self, other: Polynomial) -> Polynomial:
        max_len = max(len(self.coefficients), len(other.coefficients))
        p_1 = self.coefficients + (0,) * (max_len - len(self.coefficients))
        p_2 = other.coefficients + (0,) * (max_len - len(other.coefficients))
        poly_sum = tuple(sum(i) for i in zip(p_1, p_2))
        return Polynomial(poly_sum)

    def __mul__(self, scalar: float) -> Polynomial:
        return Polynomial(tuple(scalar * coef for coef in self.coefficients))

    def __rmul__(self, scalar: float) -> Polynomial:
        return Polynomial(tuple(scalar * coef for coef in self.coefficients))

    def __repr__(self) -> str:
        coeffs = ", ".join(str(c) for c in self.coefficients)
        return f"Polynomial(({coeffs}))"

    def __str__(self) -> str:
        coefs_as_str = []
        for i in range(len(self.coefficients) - 1, -1, -1):
            if self.coefficients[i] == 0:
                continue
            elif i == 0:
                coefs_as_str.append(f"{self.coefficients[i]:g}")
            elif self.coefficients[i] == 1.0:
                coefs_as_str.append(f"x^{i}")
            elif self.coefficients[i] == -1.0:
                coefs_as_str.append(f"-x^{i}")
            else:
                coefs_as_str.append(f"{self.coefficients[i]:g}x^{i}")
        poly_str = " + ".join(coefs_as_str)
        poly_str = poly_str.replace("x^1", "x").replace(" + -", " - ")
        return poly_str


import doctest

doctest.testmod()
