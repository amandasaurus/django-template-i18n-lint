# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="django-template-i18n-lint",
    description="Django management command to find untranslated strings in templates.",
    version='0.2',
    author="Justin Hamade",
    author_email='test',
    url="http://github.com/justhamade/django-template-i18n-lint",
    download_url="http://github.com/justhamade/django-template-i18n-lint",
    platforms=['any', ],
    requires=[],
    install_requires=['Django'],
    packages=find_packages(),
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
