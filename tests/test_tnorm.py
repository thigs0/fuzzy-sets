import matplotlib.pyplot as plt
import numpy as np
from cauchyfuzzyset import CauchyFuzzySet as cfn
from tfn import TriangularFuzzyNumber as tfn
from tnorm import Tnorm
plt.style.use('ggplot')

c = cfn(1,2,3)
d = cfn(2,4,5)

x = np.linspace(-1,10,200)
sets = [c,d]
colors = ["yellow", "green"]
for i in range(2): plt.plot(x, [sets[i].mu(j) for j in x ], label=f"Fuzzy Set)", color=colors[i])

out = Tnorm("minimum", c,d)
plt.plot(x, [out.tnorm(i) for i in x], "r--", label="Tnorm")
plt.plot(x, [out.tconorm(i) for i in x], "*", label="tconorm", color="gray")
plt.title("tnorm and tconorm about two cauchy fuzzy set")
plt.legend(loc="center left")
plt.savefig('test.png', dpi=300)
