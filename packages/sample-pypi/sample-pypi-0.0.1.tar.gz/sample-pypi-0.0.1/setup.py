from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sample-pypi',
    version='0.0.1',
    description='Sample PyPI library',
    long_description=long_description,

    url='https://gitlab.com/massood/sample-pypi',

    author='Massood',
    author_email='massoodkhaari@gmail.com',

    license='Closed-Source Proprietary License',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='sample pypi',

    packages=['my'],

    install_requires=[
        'six==1.11.0',
    ],
)
