Django Template i18n lint
=========================

[![Build Status](https://travis-ci.org/rory/django-template-i18n-lint.png?branch=master)](https://travis-ci.org/rory/django-template-i18n-lint)
[![Coverage Status](https://coveralls.io/repos/rory/django-template-i18n-lint/badge.png?branch=master)](https://coveralls.io/r/rory/django-template-i18n-lint?branch=master)
[![PyPI version](https://pypip.in/v/django-template-i18n-lint/badge.png)](https://pypi.python.org/pypi/django-template-i18n-lint)
[![PyPI Downloads](https://pypip.in/d/django-template-i18n-lint/badge.png)](https://pypi.python.org/pypi/django-template-i18n-lint)

Fork of original project by Rory McCann, [https://github.com/rory/django-template-i18n-lint](https://github.com/rory/django-template-i18n-lint), description by original author: [Lint tool to find non-i18n strings in a django template](http://www.technomancy.org/python/django-template-i18n-lint/)


A simple script to find non-i18n text in a Django template.

* native Django translation `{% trans 'x' %}` and `{% blocktrans %}`

Usage:
======

    $ python django_angular_template_i18n_lint.py template_files

Program docs are available:

    $ python django_angular_template_i18n_lint --h


Usefull hints:
==============

Putting `{# notrans #}` or `<!-- notrans -->` at the begining of line will prevent that line from showin in the results.
