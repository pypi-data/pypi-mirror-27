# dictutils
dictionary utils.

## Installation

This is a pure-Python package built for Python 2.7+ and Python 3.0+. To set up

    pip install dictutils

## Usage

``AttrDict`` behaves exactly like ``collections.OrderedDict``, but also allows
keys to be accessed as attributes::

    >>> from dictutils import AttrDict
    >>> ad = AttrDict()
    >>> ad['a'] = 1
    >>> assert ad.a == 1
    >>> ad.b = 2
    >>> assert ad['b'] == 2
    >>> ad.c = 3
    >>> assert ad.keys() == ['a', 'b', 'c']



