#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["requests", "requests-toolbelt", "oauthlib", "requests_oauthlib"]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
    "pytest-mock",
    "hypothesis",
    "tox",
    "flake8",
    "coverage",
]

setup(
    author="Joel Shprentz",
    author_email="jshprentz@his.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications",
    ],
    description="Load Meetup events into Wild Apricot.",
    entry_points={
        "console_scripts": [
            "meetup2apricot=meetup2apricot.__main__:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="etl",
    name="meetup2apricot",
    packages=find_packages(include=["meetup2apricot"]),
    project_urls={
        "Documentation": "https://meetup2apricot.readthedocs.io/",
        "Source Code": "https://github.com/jshprentz/meetup2apricot",
    },
    python_requires=">=3.9",
    scripts=[],
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jshprentz/meetup2apricot",
    version="1.0.3",
    zip_safe=False,
)
