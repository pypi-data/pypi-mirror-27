
djangocms bootstrap grid
==================================

An opinionated implementation of a bootstrap grid plugin for djangocms.

Installation
------------

    pip install cmsplugin_ss_grid

In your settings.py

    INSTALLED_APPS = (
        ...
        'cmsplugin_ss_grid',
    )

In settings.py:

    CMSPLUGIN_SS_GRID = dict(
        CELL_DEFAULT_CLASS='class-added-to-all-cells'
    )

Development
-----------

We use djangocms-helper to execute django commands and run tests.

To run test:

    djangocms-helper cmsplugin_ss_grid test --cms


Create migrations:

    djangocms-helper cmsplugin_ss_grid makemigrations --cms

Tested on
    * Python 2.7. 3.4, 3.5
    * Django 1.8, 1.9, 1.10
    * DjangoCms 3.4
