kaybee
======

.. image:: https://img.shields.io/travis/pauleveritt/kaybee.svg
    :target: https://pypi.python.org/pypi/kaybee

.. image:: https://img.shields.io/pypi/v/kaybee.svg
    :target: https://pypi.python.org/pypi/kaybee

.. image:: https://img.shields.io/pypi/l/kaybee.svg
    :target: https://pypi.python.org/pypi/kaybee

.. image:: https://img.shields.io/pypi/pyversions/kaybee.svg
    :target: https://pypi.python.org/pypi/kaybee

Knowledge Base (KB, kaybee) using on Sphinx with schema-driven resource
directives in YAML.

See ``docs`` for details.

** Note: This package requires Python 3.6+ **

Development
-----------

#. Make a virtualenv e.g. ``python3 -m venv env36``

#. Update pip stuff with ``pip install --upgrade pip setuptools wheel``

#. ``pip install -r requirements.txt`` to get dev requirements plus the
editable package.

Release
-------

#. Bump the version using ``bumpversion``:

   - https://legacy-developer.atlassian.com/blog/2016/02/bumpversion-is-automation-for-semantic-versioning/

   - https://github.com/peritus/bumpversion/issues/77#issuecomment-130696156

#. Tag the release.

#. Run ``gitchangelog`` to generate the history that goes into the package.

#. Generate the package using ``python setup.py sdist bdist_wheel``

#. Upload to PyPI using ``twine``