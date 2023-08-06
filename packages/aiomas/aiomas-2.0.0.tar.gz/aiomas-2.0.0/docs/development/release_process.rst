Release Process
===============

This document describes how to release a new version of aiomas.


Preparations
------------

#. Close all `tickets for the next version
   <https://gitlab.com/sscherfke/aiomas/issues>`_.

#. Update the *minium* required versions of dependencies in :file:`setup.py`.
   Update the *exact* version of all entries in :file:`requirements.txt`.

#. Make sure the `pipeline <https://gitlab.com/sscherfke/aiomas/pipelines>`_
   passes.

   Additionaly, you should run :command:`tox`.  All tests must pass.

#. Check if all authors are listed in :file:`AUTHORS.rst`.

#. Update the change logs (:file:`CHANGES.rst` and
   :file:`docs/development/changelog.rst`). Only keep changes for the current
   major release in :file:`CHANGES.rst` and reference the history page from
   there.

#. Commit all changes:

   .. code-block:: console

    $ git add -u
    $ git commit -m 'Updated change log for the upcoming release.'

#. Update the version number in :file:`setup.py`, :file:`docs/conf.py`, and
   :file:`src/aiomas/__init__.py`.  Commit:

   .. code-block:: console

    $ git add -u
    $ git commit -m 'Bump version from x.y.z to a.b.c'

   .. warning::

      Do not yet tag and push the changes so that you can safely do a rollback
      if one of the next step fails and you need change something!

#. Write a draft for the announcement mail with a list of changes,
   acknowledgements and installation instructions.


Build and release
-----------------

#. Test the release process. Build a source distribution and a `wheel
   <https://pypi.python.org/pypi/wheel>`_ package and test them:

   .. code-block:: console

    $ python setup.py sdist bdist_wheel
    $ ls dist/
    aiomas-a.b.c-py2.py3-none-any.whl aiomas-a.b.c.tar.gz

   Test if the packages can be installed:

   .. code-block:: console

    $ ./release_test.sh a.b.c
    Checking packages for aiomas==a.b.c
    [...]
    Source distribution looks okay.
    [...]
    Wheel package looks okay.

#. Create or check your accounts for the `test server
   <https://testpypi.python.org/pypi>` and `PyPI
   <https://pypi.python.org/pypi>`_. Update your :file:`~/.pypirc` with your
   current credentials:

   .. code-block:: ini

      [distutils]
      index-servers =
          pypi
          test

      [pypi]
      repository = https://upload.pypi.org/legacy/
      username = <your production user name goes here>

      [test]
      repository = https://test.pypi.org/legacy/
      username = <your test user name goes here>

#. Upload the distributions for the new version to the test server and test the
   installation again:

   .. code-block:: bash

    $ twine upload -r test dist/aiomas*a.b.c*
    $ pip install -i https://testpypi.python.org/pypi aiomas[mpb]

#. Check if the package is displayed correctly:
   https://testpypi.python.org/pypi/aiomas

#. Finally upload the package to PyPI and test its installation one last time:

   .. code-block:: bash

    $ twine upload -r pypi dist/aiomas*a.b.c*
    $ pip install -U aiomas[mpb]

#. Check if the package is displayed correctly:
   https://pypi.python.org/pypi/aiomas


Post release
------------

#. Push your changes:

   .. code-block:: bash

    $ git tag a.b.c
    $ git push origin master a.b.c

#. Send the prepared email to the mailing list and post it on Twitter/Google+.

#. Post something to Planet Python (e.g., via Stefan's blog).
