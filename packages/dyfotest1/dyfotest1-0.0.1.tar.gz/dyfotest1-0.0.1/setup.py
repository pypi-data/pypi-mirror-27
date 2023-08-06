import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="dyfotest1",
    version="0.0.1",
    author="Vishal Srivastava",
    author_email="vishal@dyfolabs.com",
    description="A product to test python package uploads.",
    license="Free",
    keywords="testpackage",
    url="https://dyfolabs.com",
    packages=['agents'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: Free For Educational Use",
    ],
)