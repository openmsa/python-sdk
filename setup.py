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

    packages=['msa_sdk', 'requests', 'chardet', 'chardet.cli',
              'urllib3.packages',
              'urllib3.contrib',
              'urllib3.contrib._securetransport',
              'urllib3.packages',
              'urllib3.packages.backports',
              'urllib3.packages.rfc3986',
              'urllib3.packages.ssl_match_hostname',
              'urllib3.util',
              'idna', 'certifi'],
    package_dir={
        'requests': 'required_pkgs/requests',
        'urllib3': 'required_pkgs/urllib3',
        'chardet': 'required_pkgs/chardet',
        'idna': 'required_pkgs/idna',
        'certifi': 'required_pkgs/certifi'},
    data_files=[
        ('/opt/ses/share/htdocs/msa_sdk',
         DOC_HTML_FILES)],
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta"],
)

# vim: ft=python
