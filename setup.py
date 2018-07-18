# -*- coding: utf-8 -*-
#
import os
import codecs

from setuptools import setup, find_packages

base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "polypy", "__about__.py"), "rb") as f:
    exec(f.read(), about)


def read(fname):
    return codecs.open(os.path.join(base_dir, fname), encoding="utf-8").read()


setup(
    name="polypy",
    version=about["__version__"],
    packages=find_packages(),
    url="https://github.com/nschloe/polypy",
    author=about["__author__"],
    author_email=about["__email__"],
    install_requires=["numpy"],
    extras_require={"all": ["matplotlib"], "plot": ["matplotlib"]},
    description="Polygon package",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license=about["__license__"],
    classifiers=[
        about["__license__"],
        about["__status__"],
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
