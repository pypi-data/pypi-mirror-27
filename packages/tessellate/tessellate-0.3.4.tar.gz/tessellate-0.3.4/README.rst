==========
Tessellate
==========


.. image:: https://img.shields.io/pypi/v/tessellate.svg
        :target: https://pypi.python.org/pypi/tessellate

.. image:: https://readthedocs.org/projects/tessellate/badge/?version=latest
        :target: https://tessellate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

A package for quantifying cyclic molecule conformations.


* Free software: Apache Software License 2.0
* Documentation: https://tessellate.readthedocs.io.

Using
-----

.. code:: bash

    make install; tessellate  data/example-builtin --input-format=builtin --output-format=json
    make install; tessellate  data/*DNA --input-format=pdblist --output-format=json

Installing
----------
- Use Python3. For example, Anaconda Python https://www.anaconda.com/download/ https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
- Use a virtual environment or conda environment.
- Install with pip or compile the source code

.. code:: bash

    # installing with pip
    pip install tessellate

    # Alternatively: compile from source
    make install


Usecase 1 - timeseries data
---------------------------

.. code:: bash

    tessellate  data/usecase-timeseries --input-format=builtin --output-format=json --output-dir=output-usecase-timeseries

Usecase 2 - RNA and DNA
-----------------------

.. code:: bash

    tessellate  data/usecase-*DNA --input-format=pdblist --output-format=json --output-dir=output-usecase-rnadna

Usecase 3 - Alpha Cyclodextrin
------------------------------

.. code:: bash

    tessellate  data/usecase-*CD --input-format=pdblist --output-format=json --output-dir=output-usecase-cyclodextrin

Run All Usecases
----------------

.. code:: bash

    tessellate  data/usecase-timeseries --input-format=builtin --output-format=json --output-dir=output-usecase-timeseries
    tessellate  data/usecase-*DNA --input-format=pdblist --output-format=json --output-dir=output-usecase-rnadna
    tessellate  data/usecase-*CD --input-format=pdblist --output-format=json --output-dir=output-usecase-cyclodextrin


Viewing Data
------------

Try out Montage to create reports for these datasets.
For example:

.. code:: bash
    USECASE_DATA=output-usecase-cyclodextrin
    multiqc $USECASE_DATA -m comp_tessellate -f  # -f to overwrite existing reports
    google-chrome multiqc_report.html

Compare all outputs:

.. code:: bash
    multiqc output* -m comp_tessellate -f  # -f to overwrite existing reports
    google-chrome multiqc_report.html


Features
--------

* Improve testing and documentation. Port existing tests over. 
* Tables
* Merge in tcl scripts and VMD examples


Development
-----------
Bump version numbers using bumpversion
X=thecurrentversion
`bumpversion  --current-version X minor`

To bump from x.y.z to x.y.a use patch as the part:
`bumpversion  --current-version X patch`

Uploading to PyPi
-----------------
Use twine

.. code:: bash
    conda install -c conda-forge twine
    make install
    make dist
    twine upload dist/*

Issues
------
Report Issues at https://github.com/scientificomputing/tessellate/issues 
Known issue - only relative paths supported



Read the Docs
-------------
Docs are here. RTD is authorised to acces GitHub repos. The RTD service hook builds doc on push.

Credits
---------


This package incorporates work from existing packages (all originally developed by Chris B. Barnett.)
* https://bitbucket.org/scientificomputing/triangular-tessellation-class http://git.cem.uct.ac.za/analysis-pucker/triangular-tessellation-class
* https://bitbucket.org/scientificomputing/ring-analytics-webserver https://bitbucket.org/rxncor/rad-dev http://git.cem.uct.ac.za/analysis-pucker/ring-analytics-dash
* https://bitbucket.org/scientificomputing/triangular-tessellation-in-vmd http://git.cem.uct.ac.za/analysis-pucker/triangular-decomposition-timeseries-in-VMD

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

