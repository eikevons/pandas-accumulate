# `pandas-accumulate`: accumulate values along Pandas series

This package provides one function that allows accumulating values along a
Pandas series very similar to `cumsum` and `cumprod` but allowing also other
operators like `|`.

# Usage examples

## `cumsum`

Replicate cumsum:

```python
>>> import operator
>>> import pandas as pd
>>> from pandas_accumulate import accumulate
>>> s = pd.Series([1, 2, 3])
>>> accumulate(s, operator.add)
0    1
1    3
2    6
dtype: int64
```

## cumulative `unique()`

Collect the unique values cumulatively. _Note_: You need to pass an
`initial` value for the accumulation in this example:
```python
>>> s = pd.Series([1,2,1,3,2])
>>> def f(acc, v):
...     return acc | {v}
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
