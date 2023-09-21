"""Setup."""

import glob

from setuptools import setup

DOC_HTML_FILES = glob.glob('msa_sdk/html/msa_sdk/*.html')

setup(
    name="msa_sdk",
    author="Ubiqube",
    author_email="ubiqube@ubiqube.com",
    description="MSA Python SDK",
    license="",
    keywords="MSA",
    url="https://ubiqube.com",

    packages=['msa_sdk', 'requests', 'chardet', 'chardet.cli', 'idna'],
    package_dir={
        'requests': 'required_pkgs/requests',
        'chardet': 'required_pkgs/chardet',
        'idna': 'required_pkgs/idna'},
    data_files=[
        ],
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta"],
)

# vim: ft=python
