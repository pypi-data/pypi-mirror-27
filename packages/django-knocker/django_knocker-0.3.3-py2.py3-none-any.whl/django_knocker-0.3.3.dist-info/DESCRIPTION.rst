=============================
django-knocker
=============================

.. image:: https://img.shields.io/pypi/v/django-knocker.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-knocker
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/django-knocker.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-knocker
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/django-knocker.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-knocker
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/django-knocker/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-knocker?branch=master
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/django-knocker/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-knocker
   :alt: Code Climate


Channels-based desktop notification system

Documentation
-------------

The full documentation is at https://django-knocker.readthedocs.io.

Usage
-----

See https://django-knocker.readthedocs.io/en/latest/usage.html

Features
--------

* Sends desktop notifications to connected browsers
* Multilianguage support (with `django-parler`_ and `django-hvad`_)
* Uses `django-meta`_ API for a consistent metadata handling

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python cms_helper.py

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage-helper`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage-helper`: https://github.com/nephila/cookiecutter-djangopackage-helper
.. _django-hvad: https://github.com/KristianOellegaard/django-hvad
.. _django-parler: https://github.com/edoburu/django-parler
.. _django-meta: https://github.com/nephila/django-meta




History
-------

0.3.3 (2018-01-01)
++++++++++++++++++

* Fixed support for newer channel versions
* Fixed error in signal handling
* Added support for Django 1.11
* Improved test coverage

0.3.2 (2016-12-02)
++++++++++++++++++

* Add support for Django 1.10

0.3.1 (2016-09-10)
++++++++++++++++++

* Fix error in js message'

0.3.0 (2016-08-03)
++++++++++++++++++

* Make easier to customize the knocker url

0.2.0 (2016-06-11)
++++++++++++++++++

* Fixed documentation
* Improved routing setting in tests

0.1.1 (2016-04-08)
++++++++++++++++++

* Add Add pause_knocks / active_knocks functions.

0.1.0 (2016-04-07)
++++++++++++++++++

* First release on PyPI.


