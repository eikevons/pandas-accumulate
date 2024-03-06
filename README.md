# `pandas-accumulate`: accumulate values along Pandas series

This package provides a function to accumulate values along a Pandas series.
This is the same as `cumsum` (for `+`) and `cumprod` (for `*`) but works
with any binary function, e.g. `operator.or_` (for `|`).

[![Test Status](https://github.com/eikevons/pandas-accumulate/actions/workflows/check.yml/badge.svg)](https://github.com/eikevons/pandas-accumulate/actions/workflows/check.yml)
[![Latest Version](https://img.shields.io/pypi/v/pandas-accumulate.svg)](https://pypi.org/project/pandas-accumulate/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pandas-accumulate)](https://pypi.org/project/pandas-accumulate/) 
[![PyPI Downloads](https://img.shields.io/pypi/dm/pandas-accumulate.svg?label=PyPI%20downloads)](https://pypi.org/project/pandas-accumulate/) 

# Installation

Simply pull from [PyPI](https://pypi.org/project/pandas-accumulate/):
```sh
pip install pandas-accumulate
```
 
# Usage examples

## cumulative `unique()`

Collect the unique values cumulatively. _Note_: You need to pass an
`initial` value for the accumulation in this example:
```python
>>> import pandas as pd
>>> from pandas_accumulate import accumulate
>>> s = pd.Series([1,2,1,3,2])
# Define an accumulating function
>>> def f(acc, v):
...     return acc | {v}
# ... and apply it
>>> accumulate(s, f, initial=set())
0          {1}
1       {1, 2}
2       {1, 2}
3    {1, 2, 3}
4    {1, 2, 3}
dtype: object
```

## cumulative `nunique()`

If you're interested only in the number of unique values, just call `len` at
the end:

```python
>>> accumulate(s, f, initial=set()).map(len)
0    1
1    2
2    2
3    3
4    3
dtype: int64
```
## Mock `cumsum` and `cumprod`

Replicate `cumsum`:

```python
>>> s = pd.Series([1, 2, 3])
>>> accumulate(s, operator.add)
0    1
1    3
2    6
dtype: int64
```

... and `cumprod`:

```python
>>> accumulate(s, operator.prod)
0    1
1    2
2    6
dtype: int64
```

