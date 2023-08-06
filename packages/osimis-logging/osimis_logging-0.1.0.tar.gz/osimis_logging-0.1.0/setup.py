from setuptools import setup, find_packages

setup(
    name = 'osimis_logging',
    packages = find_packages(),
    version='0.1.0',  # always keep all zeroes version, it's updated by the CI script
    setup_requires=[],
    description = 'Extended logging classes.',
    author = 'Alain Mazy',
    author_email = 'am@osimis.io',
    url = 'https://bitbucket.org/osimis/python-osimis-logging',
    keywords = ['LogHelpers', 'logging'],
    classifiers = [],
)
