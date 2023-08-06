from setuptools import setup, find_packages

setup(
    name = 'osimis_cmd_helpers',
    packages = find_packages(),
    version='0.1.0',  # always keep all zeroes version, it's updated by the CI script
    setup_requires=[],
    description = 'Helpers to run system commands and get their output.',
    author = 'Alain Mazy',
    author_email = 'am@osimis.io',
    url = 'https://bitbucket.org/osimis/python-osimis-cmd-helpers',
    keywords = ['Helpers', 'Cmd'],
    classifiers = [],
)
