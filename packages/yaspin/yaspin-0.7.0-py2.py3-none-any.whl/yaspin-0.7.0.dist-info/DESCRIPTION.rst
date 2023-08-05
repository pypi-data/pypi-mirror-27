Lightweight and easy to use terminal spinner. No external dependencies. Find documentation here: https://github.com/pavdmyt/yaspin

Features
========

- No external dependencies
- Runs at all major **CPython** versions (*2.6*, *2.7*, *3.3*, *3.4*, *3.5*, *3.6*), **PyPy** and **PyPy3**
- Supports all (60+) spinners from `cli-spinners`_
- Supports all *colors*, *highlights*, *attributes* and their mixes from `termcolor`_ library
- Flexible API, easy to integrate with existing code
- Safe **pipes** and **redirects**:

.. code-block:: bash

    $ python script_that_uses_yaspin.py > script.log
    $ python script_that_uses_yaspin.py | grep ERROR


Release History
===============

0.7.0 / 2017-11-28
------------------

* Reverse spinner support


0.6.0 / 2017-11-26
------------------

* Right spinner support


0.5.0 / 2017-11-24
------------------

* Colors support


0.4.2 / 2017-11-17
------------------

* RST vs PyPI episode 2


0.4.1 / 2017-11-17
------------------

* RST vs PyPI episode 1


0.4.0 / 2017-11-17
------------------

* Support for success and failure finalizers


0.3.0 / 2017-11-14
------------------

* Support for changing spinner properties on the fly


0.2.0 / 2017-11-10
------------------

* Support all spinners from `cli-spinners`_
* API changes:
    - `yaspin.spinner` -> `yaspin.yaspin`


0.1.0 / 2017-10-31
------------------

* First version


.. _cli-spinners: https://github.com/sindresorhus/cli-spinners
.. _termcolor: https://pypi.python.org/pypi/termcolor


