# Table of Contents
 * [Triangular fuzzy numbers](#triangular-fuzzy-numbers)
 * [Fuzzy sets](#fuzzy-sets)
 * [Plotting](#plotting)

**To-Do**
- implementar Cauchyset [Done]
  1. Try with many codes []
  2. create a code with example at README []
- implementar tnorma( DeMorgan tripdrástica, produto e soma probabilista, min max ) obs: qualquer definição de uma tnorma -> automaticamente no t-conorma [Done]
  1. Verify the Tnorm product
  2. Create code example of Tnorm product
  3. Verify the Tconorm probabilistic sum
  4. Create code example of probabilistic sum
  5. verify the Tnorm min max
  6. Create code with Tnorm min and Tconorm max
- implementar takagi-sugeno, mandanam
  -> dados de saída são em dataframe com todas as variáveis 



# fuzzysets
**fuzzysets** is a simple Python package that is well suited for interactive experiments with fundamental concepts in fuzzy set theory.  

# Installation
The package is available on [PYPI](https://pypi.org/project/fuzzysets/) and can be installed with pip:  
```pip install fuzzysets```  
```pip install git+https://github.com/thigs0/fuzzysets.git```  
# Notation
In the following sections, code snippets will be highlighted like this.  

```python
import fuzzysets as fs
```

Examples involving a read-evaluate-print loop will show both the Python statement, which will be preceded by a `>>>` prompt, and its output, if any.  

<a name="triangular-fuzzy-numbers"></a>
## Triangular fuzzy numbers
One of the concepts implemented by **fuzzysets** is a triangular fuzzy number (TFN), represented with the *TriangularFuzzyNumber* class.  

Each TFN can be uniquely represented as a 3-tuple of real numbers (left, peak, right) (l, n and r below) where:

 - peak is the number whose membership degree is 1, that is, the number being modeled
 - left (< peak) and right (> peak) determine the fuzzy number's membership function:
    - mu(x) = 0, x ∈ (-inf, l) U (r, +inf)
    - mu(x) = (x - l) / (n - l), l <= x <= n
    - mu(x) = (r - x) / (r - n), n <= x <= r

The TriangularFuzzyNumber class offers a more complex abstraction than that.  

We first need to import the **fuzzysets** package:  

```python
>>> import fuzzysets as fs
```

The class is available through an alias - TFN. The default value of the class is 0:  

```python
>>> fs.TFN()
TriangularFuzzyNumber(l=-1.0, n=0.0, r=1.0)
```

As you can see, the *left* and *right* properties are offset by 1 by default. We could create a TFN that models any number like this:  

```python
>>> fs.TFN(11.5)
TriangularFuzzyNumber(l=10.5, n=11.5, r=12.5)
```

It is also possible to set one or both of the other properties:  

```python
>>> fs.TFN(10, r=12.8)
TriangularFuzzyNumber(l=9.0, n=10.0, r=12.8)
>>> fs.TFN(10.6, 8, 12)
TriangularFuzzyNumber(l=8.0, n=10.6, r=12.0)
```

Since the order of the arguments may seem a bit odd, a TFN can also be created from a tuple:  

```python
>>> tfn = fs.TFN.from_tuple((0, 1, 2.5))
>>> tfn
TriangularFuzzyNumber(l=0.0, n=1.0, r=2.5)
```

We can call the membership function of the TFN like this:  

```python
>>> tfn.mu(-1)
0
>>> tfn.mu(0.5)
0.5
>>> tfn.mu(1)
1.0
>>> tfn.mu(2.)
0.3333333333333333
```

Arithmetic operations on TFNs can be done with the corresponding operators:  

```python
>>> n = tfn.from_tuple((1, 2, 4))
>>> m = tfn.from_tuple((2, 4, 6))
>>> n + m
TriangularFuzzyNumber(l=3.0, n=6.0, r=10.0)
>>> n - m
TriangularFuzzyNumber(l=-5.0, n=-2.0, r=2.0)
>>> n * m
TriangularFuzzyNumber(l=2.0, n=8.0, r=24.0)
>>> n / m
TriangularFuzzyNumber(l=0.16666666666666666, n=0.5, r=2.0)
>>> -n
TriangularFuzzyNumber(l=-4.0, n=-2.0, r=-1.0)  
```

There are also predicates for (proper) subset and equality tests:  

```python
>>> fs.TFN.from_tuple((1.2, 2, 4)) < fs.TFN.from_tuple((1, 2, 4))
True
>>> n <= n
True
>>> m > m
False
>>> fs.TFN.from_tuple((1, 2, 3)) >= fs.TFN.from_tuple((1, 2.1, 3))
False
>>> n == n
True
>>> n != m
True
```

We can also obtain the alpha cut of a TFN:  

```python
>>> n
TriangularFuzzyNumber(l=1.0, n=2.0, r=4.0)
>>> n.alpha_cut
AlphaCut(1.0 + alpha * 1.0, 4.0 + alpha * -2.0)
```

It can be converted to a more user-friendly string than the one above and can compute the interval for a fixed alpha:  

```python
>>> cut = n.alpha_cut
>>> str(cut)
'[1.0 + alpha * 1.0, 4.0 + alpha * -2.0]'
>>> cut.for_alpha(0.5)
(1.5, 3.0)
```

TFNs are also hashable which means that we can store them in sets or use them as mapping keys:  

```python
>>> {fs.TFN(i) for i in range(2)}
{TriangularFuzzyNumber(l=0.0, n=1.0, r=2.0), TriangularFuzzyNumber(l=-1.0, n=0.0, r=1.0)}
>>> mapping = {fs.TFN(): "zero", fs.TFN(1): "one"}
>>> mapping
{TriangularFuzzyNumber(l=-1.0, n=0.0, r=1.0): 'zero', TriangularFuzzyNumber(l=0.0, n=1.0, r=2.0): 'one'}
```

We can also obtain the basic attributes of a TFN:  

```python
>>> n
TriangularFuzzyNumber(l=1.0, n=2.0, r=4.0)
>>> n.left
1.0
>>> n.peak
2.0
>>> n.right
4.0
```

TFNs are also iterable, their attributes are yielded in order from left to right. This means that we can unpack them just like tuples: 

```python
>>> a, b, c = n
>>> a
1.0
>>> b
2.0
>>> c
4.0
```

<a name="fuzzy-sets"></a>
