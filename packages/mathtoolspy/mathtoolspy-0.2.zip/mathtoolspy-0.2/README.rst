===========
mathtoolspy
===========

.. image:: https://img.shields.io/codeship/d89309c0-4619-0135-9944-0ac58edb84f9/master.svg
    :target: https://codeship.com//projects/231332

.. image:: https://readthedocs.org/projects/mathtoolspy/badge
    :target: http://mathtoolspy.readthedocs.io

A fast, efficient Python library for mathematically operations, like
integration, solver, distributions and other useful functions.


Example Usage
-------------

.. code-block:: python

    >>> from mathtoolspy.integration import gauss_kronrod

    >>> fct = lambda x:exp(-x*x)
    >>> integrator = gauss_kronrod()
    >>> integrator(fct, -1.0, 2.0)
    1.62890552357

Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install mathtoolspy

If the above fails, please try easy_install instead:

.. code-block:: bash

    $ easy_install mathtoolspy


Examples
--------

.. code-block:: python

    # Simplest example possible
	    a, b, c, d, e = 1, 4, -6, -6, 1
        fct = lambda x : a*x*x*x*x + b*x*x*x + c*x*x + d*x + e
        opt = Optimizer1Dim(minimize_algorithm=brent)
        result = opt.optimize(fct, constraint=Constraint(-10.0, -2.0), initila_value=1.0)
        >>> result.xmin
        -3.70107061641
        >>> result.fmin
        -74.1359364077
        >>> result.number_of_function_calls
        40


Development Version
-------------------

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade git+https://github.com/pbrisk/mathtoolspy.git


Contributions
-------------

.. _issues: https://github.com/pbrisk/mathtoolspy/issues
.. __: https://github.com/pbrisk/mathtoolspy/pulls

Issues_ and `Pull Requests`__ are always welcome.


License
-------

.. __: https://github.com/pbrisk/mathtoolspy/raw/master/LICENSE

Code and documentation are available according to the Apache Software License (see LICENSE__).


