#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="django-osm-field",
    author="Markus Holtermann",
    author_email="info@markusholtermann.eu",
    description="Django OpenStreetMap Field",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarkusH/django-osm-field",
    packages=setuptools.find_packages(
        exclude=[
            "*.example",
            "*.example.*",
            "example.*",
            "example",
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests",
        ],
    ),
    install_requires=["Django>=2.2"],
    extras_require={"testing": ["coverage~=5.1"]},
    setup_requires=["setuptools_scm>=3.4.2,<4"],
    use_scm_version=True,
    keywords="OpenStreetMap, OSM, Django, Geo, Geoposition",
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.5",
)
