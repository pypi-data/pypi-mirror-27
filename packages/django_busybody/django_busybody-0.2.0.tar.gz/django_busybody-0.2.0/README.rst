=============================
django_busybody
=============================

.. image:: https://badge.fury.io/py/django_busybody.svg
    :target: https://badge.fury.io/py/django_busybody

.. image:: https://travis-ci.org/s1s5/django_busybody.svg?branch=master
    :target: https://travis-ci.org/s1s5/django_busybody

.. image:: https://codecov.io/gh/s1s5/django_busybody/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/s1s5/django_busybody

django misc

Documentation
-------------

The full documentation is at https://django_busybody.readthedocs.io.

Quickstart
----------

Install django_busybody::

    pip install django_busybody

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_busybody.apps.DjangoBusybodyConfig',
        ...
    )

Add django_busybody's URL patterns:

.. code-block:: python

    from django_busybody import urls as django_busybody_urls


    urlpatterns = [
        ...
        url(r'^', include(django_busybody_urls)),
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
