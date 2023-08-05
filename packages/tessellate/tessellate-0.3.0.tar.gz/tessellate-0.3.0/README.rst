==========
Tessellate
==========


.. image:: https://img.shields.io/pypi/v/tessellate.svg
        :target: https://pypi.python.org/pypi/tessellate

.. image:: https://img.shields.io/travis/chrisbarnettster/tessellate.svg
        :target: https://travis-ci.org/chrisbarnettster/tessellate

.. image:: https://readthedocs.org/projects/tessellate/badge/?version=latest
        :target: https://tessellate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/chrisbarnettster/tessellate/shield.svg
     :target: https://pyup.io/repos/github/chrisbarnettster/tessellate/
     :alt: Updates


A package for quantifying cyclic molecule conformations.


* Free software: Apache Software License 2.0
* Documentation: https://tessellate.readthedocs.io.

Using
-----

`make install; tessellate  data/example-builtin --input-format=builtin --output-format=json `
`make install; tessellate  data/*DNA --input-format=pdblist --output-format=json `

Features
--------

* Improve testing and documentation
* Tables
* Merge in tcl scripts and VMD examples


Development
-----------
Bump version numbers using bumpversion
X=thecurrentversion
`bumpversion  --current-version X minor`

Uploading to PyPi
-----------------
Use twine
conda install -c conda-forge twine
make install
make dist
twine upload dist/*

Credits
---------


This package incorporates work from existing packages.
* https://bitbucket.org/scientificomputing/triangular-tessellation-class http://git.cem.uct.ac.za/analysis-pucker/triangular-tessellation-class
* https://bitbucket.org/scientificomputing/ring-analytics-webserver https://bitbucket.org/rxncor/rad-dev http://git.cem.uct.ac.za/analysis-pucker/ring-analytics-dash
* https://bitbucket.org/scientificomputing/triangular-tessellation-in-vmd http://git.cem.uct.ac.za/analysis-pucker/triangular-decomposition-timeseries-in-VMD

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

