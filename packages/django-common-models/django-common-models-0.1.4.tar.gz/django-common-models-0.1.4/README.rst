=============================
django-common-models
=============================

.. image:: https://badge.fury.io/py/django-common-models.svg
    :target: https://badge.fury.io/py/django-common-models

.. image:: https://travis-ci.org/george-silva/django-common-models.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-common-models

.. image:: https://codecov.io/gh/george-silva/django-common-models/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-common-models

Common models and utilities

Documentation
-------------

The full documentation is at https://django-common-models.readthedocs.io.

Quickstart
----------

Install django-common-models::

    pip install django-common-models

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'common.apps.CommonConfig',
        ...
    )

Add django-common-models's URL patterns:

.. code-block:: python

    from common import urls as common_urls


    urlpatterns = [
        ...
        url(r'^', include(common_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
