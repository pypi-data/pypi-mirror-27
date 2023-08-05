import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PyGASP",
    version = "0.2.1",
    author = "Erin Carrier, Nathan Bowman",
    author_email = "bowmanat@mail.gvsu.edu",
    description = ("A GPU-accelerated signal processing library."),
    license = "MIT",
    keywords = "signal processing, science, PyCUDA, DWT, FFT, DCT",
    url = "http://packages.python.org/PyGASP",
    packages=find_packages(),
    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ]
)
