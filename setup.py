#! /usr/bin/env python

from setuptools import setup

setup(
    name="django-template-i18n-lint",
    version="1.2.0",
    author="Rory McCann",
    author_email="rory@technomancy.org",
    py_modules=['django_template_i18n_lint'],
    install_requires=[
        'six'
    ],
    license='GPLv3+',
    url='http://www.technomancy.org/python/django-template-i18n-lint/',
    description='Lint tool to find non-trans/blocktrans text in django templates',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'django-template-i18n-lint = django_template_i18n_lint:main',
        ]
    },
)
