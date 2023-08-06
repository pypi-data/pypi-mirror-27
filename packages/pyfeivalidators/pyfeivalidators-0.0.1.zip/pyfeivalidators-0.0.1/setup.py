# -*- coding: utf-8 -*-
"""setup.py."""
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'requests>=2.0',
    'httplib2>=0.9'
]
VERSION = '0.0.1'

setup(
    name='pyfeivalidators',
    version=VERSION,
    description='Common pyfeivalidators component.',
    author='feiger',
    author_email='351275698@qq.com',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='MIT License',
    url='https://github.com/istommao/pyvalidators',
    keywords='pyfeivalidators is a common validators component,only testing!'
)