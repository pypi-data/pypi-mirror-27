# firanka

[![Build Status](https://travis-ci.org/smok-serwis/firanka.svg)](https://travis-ci.org/smok-serwis/firanka)
[![Maintainability](https://api.codeclimate.com/v1/badges/97a30fdc35e61f8d7c86/maintainability)](https://codeclimate.com/github/smok-serwis/firanka/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/97a30fdc35e61f8d7c86/test_coverage)](https://codeclimate.com/github/smok-serwis/firanka/test_coverage)
[![PyPI version](https://badge.fury.io/py/firanka.svg)](https://badge.fury.io/py/firanka)
[![PyPI](https://img.shields.io/pypi/pyversions/firanka.svg)]()
[![PyPI](https://img.shields.io/pypi/implementation/firanka.svg)]()
[![PyPI](https://img.shields.io/pypi/wheel/firanka.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

firanka is a Python library to perform calculations on particular kinds of
functions. These functions have a domain, which is a single continuous subset
of the real number line. These functions can have any values.

firanka allows you do define two classes of such functions or series.

First are the _DiscreteSeries_. _DiscreteSeries_ further divide the function
domain into slices (left-closed, right-open) that have constant values.
Manipulating _DiscreteSeries_ and performing calculations on them is cheap.

Then you have _FunctionSeries_. These are simply defined by user-supplied
Python callable.

Best part is, you can join series together (given a joining operator),
slice them and so on.


# Usage

## Series

Can be imported from _sai.series_. A generic abstract superclass for series - 
`Series` can be imported for checking if given object is a series.

Series are immutable, but non-hashable.

Read the source code of the [base class](firanka/series/series.py#L11) to get
to know more about series operations.

### DiscreteSeries

To use a _DiscreteSeries_ you must give it a set of data to work with. These
will define intervals, left-closed, right-open. Ie. 


```python
fs = DiscreteSeries([(0,1), (3, 4), (5, 6)])
fs[0.5] == 1
fs[3] == 4
fs[5] == 6
# fs[6] - NotInDomainError's
```

Datapoints given **must be already sorted**!. By default, the domain
will be both sides closed, from minimum to maximum given in data, but you can
specify a custom one:

```python
fs = DiscreteSeries([(0,1), (3, 4), (5, 6)], '(0; 8>')
# fs[0] - NotInDomainError's !
fs[6] == 6
```

Although you can't specify a domain where it would be impossible to compute the value.
(ie. starting at smaller than zero). Doing so will throw a _ValueError_.

Note that when using `join_discrete()` sometimes other series might get calls 
from beyond their domain. This can be seen for example here:

```python
logs = FunctionSeries(math.log, '(0;5>')
dirs = DiscreteSeries([(0,1)], '<0;5>')

# Raises ValueError due to math.log being called with 0
dirs.join_discrete(logs, lambda x, y: x+y)   
```

### FunctionSeries

Using _FunctionSeries_ is straightforward. Just give them a callable and
a domain:

```python
fs = FunctionSeries(lambda x: x**2, '<-2;2>')
```

### ModuloSeries

_ModuloSeries_ allow you to wrap a finite series in repetition.

```python
fs = ModuloSeries(someOtherSeries)
```

By definition, _ModuloSeries_ has the domain of all real numbers.

Note that someOtherSeries's domain length must be non-zero and finite. Otherwise
_ValueError_ will be thrown.

## Ranges

Can be imported from _sai.series_.

Range would have been better called an **interval**. It is a continuous subset
of the real number line.

You can create Ranges as follows:

```python
Range(-5, 5, True, False) == Range('<-5;5)')
```

First boolean argument signifies whether the interval is left-closed,
and second whether it is right-closed.

Range's are immutable and hashable. They can be sliced:

```python
Range('<-5;5>')[0:] == Range('<0;5>')
```

Slices work as a both-sides-closed range if both sides are shown!

You can check whether a range contains a point

```python
5 not in Range('<-1;5)')
```

Or you can check for strict inclusion

```python
Range('<-1;1>') in Range('<-2;2>')
```

