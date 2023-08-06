Development Setup
=================

This documents explains how to setup a `virtual environment`_ for developing
aiomas, how to build the documentation and how to run its test suite.

.. _virtual environment: https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/


Setup
-----

You should use at latest version of Python 3 for your devleopment, but at least
Python 3.4.

Create a fresh virtualenv with that interpreter and activate it.  You can then
install all development dependencies with pip:

.. code-block:: console

   (aiomas)$ pip install -r requirements-setup.txt

This installs the newest version of everything.  If you should into problems
with this, you can also install a well-tested set of all dependencies:

.. code-block:: console

   (aiomas)$ pip install -r requirements.txt

.. note::

   If you are on Windows, you might want to download msgpack_ and blosc_ wheel
   packages from `Christoph Gohlke’s`_ website instead of compiling them on
   your own.

   .. _msgpack: https://www.lfd.uci.edu/~gohlke/pythonlibs/#msgpack
   .. _blosc: https://www.lfd.uci.edu/~gohlke/pythonlibs/#blosc
   .. _Christoph Gohlke’s: https://www.lfd.uci.edu/~gohlke/pythonlibs/

Apart from installing aiomas in `editable mode`_, it also provides you the
following list of tools:

- Flake8: for checking code quality and style guides

- Pytest: for running the tests and measuing the test coverage inside your
  virtualenv

- Sphinx: for building the documentation

- Tox: for running the test suite with all supported Python versions

- Twine: for uploading packages to PyPI

.. _editable mode: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=editable#editable-installs


Building the docs
-----------------

Sphinx is used to build the docs.  You can find ReST source files in the
:file:`docs/` folder.  The output folder for HTML documentation (and other
formats) is :file:`docs/_build/`.  The `online documentation`_ on `Read the
Docs`_ is everytime you push something to Bitbucket_.

.. _online documentation: https://aiomas.readthedocs.io/
.. _Read the Docs: https://readthedocs.org/
.. _Bitbucket: https://gitlab.com/sscherfke/aiomas/

When once you’ve set-up your venv, you can build aiomas' documentation this
way:

.. code-block:: console

   (aiomas)$ cd docs/
   (aiomas)$ make html  # For quick builds
   (aiomas)$ make clean html  # For a clean/full build

For Windows user, there is a :file:`make.bat` which does the same.

You can also let Sphinx check all external links:

.. code-block:: console

   (aiomas)$ make linkcheck

You can get a full list of make targets by running ``make help``.


Running the tests
-----------------

Aiomas uses pytest_ with the plugins pytest-asyncio_ and pytest-cov_ as testing
tool.  Its configuration is stored in the ``[pytest]`` sectionin of
:file:`setup.cfg`.

.. _pytest: https://pytest.org/
.. _pytest-asyncio: https://pypi.python.org/pypi/pytest-asyncio
.. _pytest-cov: https://pypi.python.org/pypi/pytest-cov

You can run all tests by executing:

.. code-block:: console

   (aiomas)$ py.test

By default, all doctests in :file:`README.rst` and :file:`docs/`, all examples
in :file:`examples/` and all tests in :file:`tests/` are run.

In order to measure the test coverage, run pytest with the following arguments:

.. code-block:: console

   (aiomas)$ py.test --cov=src/ --cov-report=html

This will produces a folder :file:`htmlcov` with the coverage results.

You can use tox to run the test suite on all supported Python interpreters.  It
also runs :command:`flake8` to do some code quality and style checks.
Currently, you need to have :command:`python3.4` and :command:`python3.5`
available in your path.  Running tox is then easy:

.. code-block:: console

   (aiomas)$ tox
   [...]
   ________ summary ________
     py34: commands succeeded
     py35: commands succeeded
     docs: commands succeeded
     flake8: commands succeeded
     congratulations :)

If you cannot / do not want to install all the Python versions, you can limit
tox to run only a selected environment:

.. code-block:: console

   (aiomas)$ tox -e py35  # Only run tests on Python 3.5
   (aiomas)$ tox -e flake8  # Only run flake8 checks
