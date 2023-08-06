Matchstick: pattern matching in Python
======================================

.. image:: https://img.shields.io/circleci/project/github/brettbeatty/hand_grenade.svg
    :target: https://circleci.com/gh/brettbeatty/hand_grenade

.. image:: https://img.shields.io/github/license/brettbeatty/hand_grenade.svg
    :target: https://github.com/brettbeatty/hand_grenade/blob/master/LICENSE

.. image:: https://img.shields.io/codecov/c/github/brettbeatty/hand_grenade.svg
    :target: https://codecov.io/gh/brettbeatty/hand_grenade

.. image:: https://img.shields.io/pypi/v/hand_grenade.svg
    :target: https://pypi.org/project/hand_grenade/

Matchstick provides a decorator that allows for the overloading of Python functions.

.. code-block:: python

    >>> from matchstick import when
    >>> @when('x >= 0')
    ... def f(x):
    ...     return x
    ...
    >>> @when('x < 0')
    ... def f(x):
    ...     return -x
    ...
    >>> f(3)
    3
    >>> f(-2)
    2
    >>> f('a')
    'a'

Basic Use
---------
Conditions
^^^^^^^^^^
The match decorator takes a condition as a string. When the decorated function gets called, overloaded functions (grouped by module and qualified name) are checked in the order they are defined. Each condition is evaluated with the arguments passed to the function (including default parameter values, where applicable). If the condition evaluates truthy, the corresponding function is called. If the condition evaluates falsy or raises an exception, the corresponding function is passed over.

.. code-block:: python

    >>> @when('x[2] == 5')
    ... def f(x):
    ...     return sum(x)
    ...
    >>> @when('len(x) > 3')
    ... def f(x):
    ...     return x[3:]
    ...
    >>> @when('True')
    ... def f(x):
    ...     return x
    ...
    >>> f([3, 4, 5, 6])
    18
    >>> f([0, 1, 2, 3])
    [3]
    >>> f('abcd')
    'd'
    >>> f({})
    {}

NoMatchException
^^^^^^^^^^^^^^^^
If none of the conditions for a function evaluate truthy, a *matchstick.NoMatchException* is raised.
