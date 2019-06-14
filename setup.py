"""Setup"""

from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="msa_sdk",
    version="0.1",
    author="Ubiqube",
    author_email="",
    description=("MSA Python SDK"),
    license="",
    keywords="MSA",
    url="",
    packages=['msa_sdk'],
    classifiers=[
        "Development Status :: 4 - Beta"
    ],
)
