Django Template i18n lint
=========================

[![Build Status](https://travis-ci.org/rory/django-template-i18n-lint.png?branch=master)](https://travis-ci.org/rory/django-template-i18n-lint)
[![Coverage Status](https://coveralls.io/repos/rory/django-template-i18n-lint/badge.png?branch=master)](https://coveralls.io/r/rory/django-template-i18n-lint?branch=master)
[![PyPI version](https://pypip.in/v/django-template-i18n-lint/badge.png)](https://pypi.python.org/pypi/django-template-i18n-lint)
[![PyPI Downloads](https://pypip.in/d/django-template-i18n-lint/badge.png)](https://pypi.python.org/pypi/django-template-i18n-lint)


A simple script to find non-i18n text in a Django template.

It can also automatically wrap the strings in `{% trans "" %}` tags, by running it with the `-r` command-line flag.
The translation will be written to a new file, `<filename>_translated.html`.

The script also add `{% load i18n %}` to all translated templates.

For more info see [Lint tool to find non-i18n strings in a django template](http://www.technomancy.org/python/django-template-i18n-lint/)

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/rory/django-template-i18n-lint/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Installation
==
```sh
pip install git+ssh://git@gitlab.aiidatapro.net/utilities/django-template-i18n-lint.git
```
Usage
==
```
Usage: django-template-i18n-lint [options] <filenames>

You probably need just this: django-template-i18n-lint -r

Options:
  -h, --help            show this help message and exit
  -r, --replace         Ask to replace the strings in the file.
  -o, --overwrite       When replacing the strings, overwrite the original
                        file.  If not specified, the file will be saved in
                        a seperate file named X_translated.html
  -f, --force           Force to replace string with no questions
  -e EXCLUDE_FILENAME, --exclude=EXCLUDE_FILENAME
                        Exclude these filenames from being linted
  -x ACCEPT, --accept=ACCEPT
                        Exclude these regexes from results
```
