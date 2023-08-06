#!/bin/python2.7
# -*- coding: utf-8 -*-
"""
Jakub Janarek 2018
"""

import codecs
import io
import os
import sys
from shutil import rmtree

from setuptools import Command

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = [
    'newspaper_no_download',
]


if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload -r pypi')
    sys.exit()


# This *must* run early. Please see this API limitation on our users:
# https://github.com/codelucas/newspaper/issues/155
if sys.version_info[0] == 2 and sys.argv[-1] not in ['publish', 'upload']:
    sys.exit('run `$ pip3 install newspaper_no_download` for python3')


with open('requirements.txt') as f:
    required = f.read().splitlines()


with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='newspaper_no_download',
    version='0.0.1',
    description='Newspaper3k library with no download phase',
    long_description=readme,
    author='Jakub Janarek',
    author_email='jjanarek@gmail.com',
    url='https://github.com/jxub/newspaper_no_download',
    packages=packages,
    include_package_data=True,
    install_requires=required,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
