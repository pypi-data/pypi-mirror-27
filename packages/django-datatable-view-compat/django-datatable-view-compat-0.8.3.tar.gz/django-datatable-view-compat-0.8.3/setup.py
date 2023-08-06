# -*- encoding: utf-8 -*-
"""setup.py: Django django-datatable-view-compat"""

from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()

setup(
    name='django-datatable-view-compat',
    version='0.8.3',
    description='This package is used in conjunction with the jQuery plugin '
                '(http://http://datatables.net/), and supports state-saving detection'
                ' with (http://datatables.net/plug-ins/api).  The package consists of '
                'a class-based view, and a small collection of utilities for rendering'
                ' table data from models.',
    long_description=long_description,
    author='utapyngo',
    author_email='ut@pyngo.tom.ru',
    url='https://github.com/utapyngo/django-datatable-view',
    download_url='https://github.com/utapyngo/django-datatable-view/tarball/django20',
    license='Apache License (2.0)',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'datatableview': ['static/js/*.js', 'templates/datatableview/*.html']},
    include_package_data=True,
    setup_requires=['pypandoc==1.4'],
    install_requires=['django>=2.0', 'python-dateutil>=2.1'],
)
