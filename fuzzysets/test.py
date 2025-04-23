from cauchyfuzzyset import CauchyFuzzySet
from tfn import TriangularFuzzyNumber
import tnorm
import numpy as np
from matplotlib import pyplot as plt

#def set
a = CauchyFuzzySet(1, 4, 2)

b = CauchyFuzzySet(4, 2, 1)

c = TriangularFuzzyNumber(l=-2, n=0, r=4)

tmin = tnorm.Tnorm("drastic", a, c)

x = np.linspace(-6, 5, 2000)
y = np.zeros(len(x))
C = np.zeros(len(x))
for i,j in enumerate(x):
    C[i] = c.mu(j)
    y[i] = tmin.tnorm(j)

plt.plot(x, a.mu(x), color="red")
plt.plot(x, C, color="black")
plt.plot(x, y, color="green")
plt.savefig("teste.png")
print(a.mu(2))
