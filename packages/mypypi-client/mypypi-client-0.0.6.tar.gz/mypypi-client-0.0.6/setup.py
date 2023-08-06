
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mypypi-client',
    version='0.0.6',
    description='Client library for MyPyPI',
    long_description=long_description,

    url='https://gitlab.com/massood/mypypi',

    author='Massood',
    author_email='massoodkhaari@gmail.com',

    license='Closed-Source Proprietary License',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='mypypi sample',

    packages=['my'],
    # py_modules=["my.client"],

    install_requires=[
        'PyYAML==3.12',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
        'my.data': ['../../my/data/*.json'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        # 'console_scripts': [],
    },
)
