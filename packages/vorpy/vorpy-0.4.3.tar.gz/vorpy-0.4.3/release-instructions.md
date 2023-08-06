# Maintainer Release Instructions

Register accounts with [pypi](https://pypi.org/account/register/) and [testpypi](https://test.pypi.org/account/register/)
(yes, you want both).  From [this](https://packaging.python.org/guides/using-testpypi/#using-test-pypi), note that the
database for TestPyPI may be periodically pruned, so it is not unusual for user accounts to be deleted.

Create the `~/.pypirc` file according to [this documentation](https://packaging.python.org/guides/migrating-to-pypi-org/).
Example:

    [distutils]
    index-servers =
        pypi
        pypitest

    [pypi]
    repository=https://pypi.python.org/pypi
    username=jethro-q-walrustitty
    password=raymond-luxury-yacht

    [testpypi]
    repository=https://testpypi.python.org/pypi/
    username=jethro-q-walrustitty
    password=raymond-luxury-yacht

IMPORTANT: Because this file contains your passwords in plaintext, you will want to set the permissions to as private as possible:

    chmod 600 ~/.pypirc

Omitting the password will cause the package upload to prompt for password.

Create the `setup.py` file and others according to
[this documentation](https://packaging.python.org/tutorials/distributing-packages/#initial-files).
The `long_description` could be the contents of `README.rst` for example.  See [this](setup.py) for an example.

Regarding `README.rst` -- PyPi doesn't support markdown.  If your project has a `README.md` file using markdown (e.g. a
github-hosted project), then you can convert it into `rst` format using [this script](generate-README.rst.py).

Build a "source distribution", as documented [here](https://packaging.python.org/tutorials/distributing-packages/#source-distributions).

    python3 setup.py sdist

This will create a `.tar.gz` file in the `dist` subdir.  Now build a "wheel" (a built version of the package), as documented
[here](https://packaging.python.org/tutorials/distributing-packages/#pure-python-wheels).  For example, to build a pure-Python
wheel for a project that only supports Python 3, run the following command.

    python3 setup.py bdist_wheel

This will create a `.whl` file in the `dist` subdir.

Now upload the distribution files you created to [testpypi](https://testpypi.python.org/pypi/) using `twine`:

    twine upload -r testpypi dist/*

## References

-   https://packaging.python.org/tutorials/distributing-packages/
-   https://packaging.python.org/guides/using-testpypi/#using-test-pypi

-   The instructions [here](http://peterdowns.com/posts/first-time-with-pypi.html) are outdated (certain steps are
    no longer necessary), but still useful.  NOTE: Outdated because certain versions of Python may transmit passwords
    in plaintext!

