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
    project_urls={
        "CI": "https://github.com/MarkusH/django-osm-field/actions",  # noqa
        "Changelog": "https://github.com/MarkusH/django-osm-field/blob/main/CHANGELOG.md",  # noqa
        "Issues": "https://github.com/MarkusH/django-osm-field/issues",  # noqa
    },
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
    include_package_data=True,
    install_requires=["Django>=2.2"],
    extras_require={
        "dev": ["pre-commit"],
        "docs": [
            "Django",
            "sphinx_rtd_theme",
            "Sphinx>=3.0,<3.4",
        ],
        "test": [
            "coverage[toml]>=5,<6",
            "Django",
        ],
    },
    setup_requires=["setuptools_scm>=5<6"],
    use_scm_version=True,
    keywords="OpenStreetMap, OSM, Django, Geo, Geoposition",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.5",
)
