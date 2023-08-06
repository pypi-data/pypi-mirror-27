Changelog
=========

2.0.0 – 2017-12-28
------------------

- [BREAKING] Converted to f-Strings and ``async``/``await`` syntax.  The
  minimum required Python versions are now Python 3.6 and PyPy3 5.10.0.

- [BREAKING] Removed ``aiomas.util.async()`` and ``aiomas.util.create_task()``.

- [CHANGE] Move from Bitbucket and Mercurial to GitLab and Git.

- [FIX] Adjust to asyncio changes and explicitly pass references to the current
  event loop where necessary.

You can find information about older versions in the `documentation
<https://aiomas.readthedocs.io/en/latest/development/changelog.html>`_.
