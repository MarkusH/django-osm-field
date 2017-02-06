#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='django-osm-field',
    version='0.3.1',
    description='Django OpenStreetMap Field',
    long_description=readme + '\n\n' + history,
    author='Markus Holtermann, et al',
    author_email='info@markusholtermann.eu',
    url='https://github.com/MarkusH/django-osm-field',
    packages=[
        'osm_field',
    ],
    package_dir={'osm_field': 'osm_field'},
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
        'six',
    ],
    license="MIT",
    zip_safe=False,
    keywords='OpenStreetMap, OSM, Django, Geo, Geoposition',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
