# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from utils import __version__ as version

setup(
    name="george-utils",
    version=version,
    author='GeorgeWang1994',
    author_email='georgewang1994@163.com',
    description='redis wrapper',
    url='https://github.com/GeorgeWang1994/george-utils',
    packages=find_packages(),
    install_requires=['django', 'enum'],
    zip_safe=False,
    include_package_data=True,
    test_suite="george_utils.test",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Object Brokering",
    ]
)
