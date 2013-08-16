# -*- coding: utf-8 -*-

try:
    # Prefer setuptools generally
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name="django-template-i18n-lint",
    description="Django management command to find untranslated strings in templates.",
    version='0.1',
    author="Justin Hamade",
    url="http://github.com/justhamade/django-template-i18n-lint",
    download_url="http://github.com/justhamade/django-template-i18n-lint",
    platforms=['any',],
    requires=[],
    packages=['i18n-lint',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
