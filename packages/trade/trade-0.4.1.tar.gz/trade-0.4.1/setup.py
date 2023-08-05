"""trade: Financial Application Framework.

Copyright (c) 2015-2017 Rafael da Silva Rocha
https://github.com/rochars/trade
http://trade.readthedocs.org/
License: MIT

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='trade',
    version="0.4.1",
    description='Financial Application Framework',
    long_description=long_description,
    url='https://github.com/rochars/trade',
    author="Rafael da Silva Rocha",
    author_email='rocha.rafaelsilva@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='asset stock exchange securities market finance investment money currency cost',
    packages=['trade'],
)
