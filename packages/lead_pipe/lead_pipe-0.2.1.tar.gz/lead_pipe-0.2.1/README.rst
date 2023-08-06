lead_pipe
=========

.. image:: https://img.shields.io/circleci/project/github/brettbeatty/lead_pipe.svg
    :target: https://circleci.com/gh/brettbeatty/lead_pipe

.. image:: https://img.shields.io/github/license/brettbeatty/lead_pipe.svg
    :target: https://github.com/brettbeatty/lead_pipe/blob/master/LICENSE

.. image:: https://img.shields.io/codecov/c/github/brettbeatty/lead_pipe.svg
    :target: https://codecov.io/gh/brettbeatty/lead_pipe

.. image:: https://img.shields.io/pypi/v/lead_pipe.svg
    :target: https://pypi.org/project/lead_pipe/

Lead Pipe allows values to be piped from one function to the next without nesting the calls. For example, the following blocks of code are equivalent.

.. code-block:: python

    a = foo(bar(baz(8, 2), a=3), 4)

.. code-block:: python

    from lead_pipe import Pipe
    a = ~Pipe(8)(baz, 2)(bar, a=3)(foo, 4)

Basic Use
---------
Creating a Pipe
^^^^^^^^^^^^^^^
Pipelines begin with a base value passed to the Pipe constructor.

.. code-block:: python

    >>> from lead_pipe import Pipe
    >>> Pipe(3)
    Pipe(3)
    >>> Pipe('a')
    Pipe('a')

Piping Results
^^^^^^^^^^^^^^
Each instance of Pipe is callable and takes any number of arguments (at least one). The first argument is a function that gets called with the pipeline's value followed by the additional arguments and keyword arguments, if any.

.. code-block:: python

    >>> Pipe(3)(lambda x: x + 0.5)(lambda x: x ** 2)(int)('{} - {x} + {}'.format, 1, x=8)(eval)
    Pipe(5)

Obtaining Result
^^^^^^^^^^^^^^^^
Once your pipeline is finished, you can retrieve the result with the tilde (~) operator or through the pipe's 'value' attribute.

.. code-block:: python

    >>> ~Pipe(11)
    11
    >>> Pipe('foo').value
    'foo'
    >>> ~Pipe(2)(pow, 3)(str)
    '8'

Advanced Features
-----------------
Intermediate Pipes
^^^^^^^^^^^^^^^^^^
Since each step along the pipeline is its own instance of Pipe, an intermediate pipe can be saved to pipe to multiple functions.

.. code-block:: python

    >>> p = Pipe(4)(range)(zip, range(2, 6))
    >>> p
    Pipe([(0, 2), (1, 3), (2, 4), (3, 5)])
    >>> p(dict).value[2]
    4
    >>> ~p(lambda x: x[1][1])
    3

Apply
^^^^^
Sometimes a function may return another function rather than a value to be piped to another function. Apply is a helper function that continues the pipeline with the function returned.

.. code-block:: python

    >>> from lead_pipe import apply
    >>> ~Pipe('{} foo{a} {}'.format)(apply, 'bar', 'baz', a=3)
    'bar foo3 baz'

Reflect
^^^^^^^
Sometimes one may want to call a member function of a value in the pipeline. One way would be to pipe the value to getattr then to apply, but the reflect function is the combination of the two.

.. code-block:: python

    >>> from lead_pipe import reflect
    >>> ~Pipe({'a': 1, 'b': 2})(reflect, 'get', 'a')
    1

In this specific example, one could pipe the dictionary to dict.get, but reflect is more general.
