"""Accumulate Pandas series"""

__version__ = "0.1.0"
__author__ = "Eike von Seggern <eike@vonseggern.space>"
__copyright__ = "Copyright (c) 2024 Eike von Seggern"
__licence__ = "MIT"

from itertools import accumulate as it_accumulate
from typing import Any, Callable, Literal, Optional, Union

import numpy as np
import pandas as pd

__all__ = ["accumulate"]


def accumulate(
    s: pd.Series,
    f: Callable[[Any, Any], Any],
    dtype: Optional[Union[np.dtype]] = None,
    initial: Optional[Any] = None,
) -> pd.Series:
    """Accumulate along a series.

    Parameters
    ----------
    s
        The series to accumulate
    f
        The accumulation function. This must take two arguments: first
        argument is the "accumulator", second argument is the value from
        ``s``.
        If ``initial`` is not specified, ``f``
        must return the same type as the values in ``s``!
    dtype
        The dtype of the accumulated series. If ``None`` (default), it is
        the dtype of ``initial`` is used if ``initial`` is present or the
        dtype of ``s``.
    initial
        Initial accumulator value.

    Returns
    -------
    acc
        The accumulated data.

    Examples
    --------

    Calculate the cumulative sum (same as ``pd.Series.cumsum``)::

        >>> from operator import add
        >>> s = pd.Series([1,2,3])
        >>> accumulate(s, add)
        0    1
        1    3
        2    6
        dtype: int64

    Collect the cumulative unique values by accumulating into a ``set``::

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

    Note: the above will fail if ``initial`` is not passed::

        >>> accumulate(s, f)
        [...]
        TypeError: unsupported operand type(s) for |: 'int' and 'set'
    """
    if dtype is None:
        if initial is not None:
            dtype = pd.Series([initial]).dtype
        else:
            dtype = s.dtype

    # NOTE: I did some `%timeit` comparison with
    # `np.frompyfunc(f, 2, 1).accumulate(s.values)`. The results are rather
    # similar for `f = lambda a, b: a | b`:
    # size | itertools | frompyfunc
    # ------|-----------|-----------
    # 1e5  | 19.1 ms   | 17.3 ms
    # 1e6  | 185  ms   | 200  ms
    # 1e7  | 2.06 s    | 1.98 s
    # 1e8  | 20.8 s    | 21.1 s
    values = it_accumulate(s.values, f, initial=initial)
    if initial is not None:
        # Consume the initial value from the iterator. This is prepended by
        # `itertools.accumulate()`.
        next(values)

    a = np.fromiter(
        values,
        dtype,
        count=len(s),
    )
    return pd.Series(
        a,
        name=s.name,
        index=s.index.copy(),
    )
