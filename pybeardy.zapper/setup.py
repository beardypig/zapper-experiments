import os
import sys
from setuptools import setup, find_packages


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

test_extra = []

# Python 2.6 and below require simplejson
if sys.version_info < (2, 7, 0):
    test_extra.append('unittest2')

setup(
    name="pybeardy.zapper",
    version=read("version").strip(),
    author="Beardypig",
    author_email="beardypig@users.noreply.github.com",
    install_requires=read("requirements.txt").split(),
    description="Library for interfacing with a NES Zapper connected to an Arduino via serial",
    license="MIT",
    long_description=read('README.rst'),
    namespace_packages=['pybeardy'],
    classifiers=[],
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    tests_require=read("test_requirements.txt").split() + test_extra,
)