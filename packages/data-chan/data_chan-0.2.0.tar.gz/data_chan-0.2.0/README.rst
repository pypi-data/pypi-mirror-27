Data-Chan Python
================

|wercker status|

Data-Chan-python allows you to use the
`data-chan <https://github.com/neroreflex/data-chan>`__ comunication
library with Python and `Jupyter <http://jupyter.org/>`__.

Releasing
~~~~~~~~~

To release, just bump the version and push to master. Wercker-CI will
take care of the build and deploy process.

.. code:: shell

    pip install bump

    # Bump patch/major/minor
    bump setup.py -b
    bump setup.py -m
    bump setup.py -M

    # Create .tar.gz archive
    python setup.py sdist

    # Upload to PyPi the latest file
    twine upload dist/$(ls -tp dist | grep -v /$ | head -1)

.. |wercker status| image:: https://app.wercker.com/status/1fb1f6cc68959c13ef6b477ce7abefff/s/master
   :target: https://app.wercker.com/project/byKey/1fb1f6cc68959c13ef6b477ce7abefff
