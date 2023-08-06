# coding: utf-8

"""
    stylelens-search-vector
"""


from setuptools import setup, find_packages

NAME = "stylelens-search-vector"
VERSION = "1.0.3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["grpcio", "protobuf"]

setup(
    name=NAME,
    version=VERSION,
    description="stylelens-search-vector",
    author_email="bluehackmaster@bluehack.net",
    url="",
    keywords=["BlueLens", "stylelens-search-vector"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)
