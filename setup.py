# pylint: disable-all
# type: ignore
from setuptools import setup

exec(open("yourpackage/version.py").read())
setup(version=__version__)
