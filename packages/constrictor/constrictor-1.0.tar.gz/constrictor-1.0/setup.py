# Copyright 2017, Ryan P. Kelly.

from setuptools import setup


setup(
    name="constrictor",
    version="1.0",
    description="Simpler, better, and streaming gzip handling",
    author="Ryan P. Kelly",
    author_email="ryan@ryankelly.us",
    url="https://github.com/f0rk/constrictor",
    install_requires=[],
    tests_require=[
        "pytest",
    ],
    package_dir={"": "lib"},
    packages=["constrictor"],
    include_package_data=True,
    zip_safe=False,
)
