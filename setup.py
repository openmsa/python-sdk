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
    packages=['msa_sdk', 'requests', 'urllib3', 'chardet', 'idna', 'certifi'],
    package_dir={'requests': 'required_pkgs/requests',
                 'urllib3': 'required_pkgs/urllib3',
                 'chardet': 'required_pkgs/chardet',
                 'idna': 'required_pkgs/idna',
                 'certifi': 'required_pkgs/certifi'},
    data_files=[('/opt/ses/share/htdocs/msa_sdk', DOC_HTML_FILES)],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta"
    ],
)

# vim: ft=python
