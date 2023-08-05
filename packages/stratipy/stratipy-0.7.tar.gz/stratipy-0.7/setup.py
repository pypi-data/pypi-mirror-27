import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "stratipy",
    version = "0.7",
    author = "Yang-Min KIM, Guillaume DUMAS",
    author_email = "yang-min.kim@pasteur.fr, guillaume.dumas@pasteur.fr",
    description = ("Patients stratification with Graph-regularized"
                   " Non-negative Matrix Factorization (GNMF) in Python."),
    license = "BSD",
    keywords = "bioinformatics graph network stratification",
    url = "https://github.com/GHFC/StratiPy",
    packages=['stratipy', 'test', 'data'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: BSD License",
    ],
)
