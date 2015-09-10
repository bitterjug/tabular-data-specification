#!/usr/bin/env python

from distutils.core import setup

setup(
    name='tabular-data-specification',
    version='0.1',
    description='''A tool for DRY spreadsheet column specifications ''',
    author='Mark Skipper',
    author_email='marks@aptivate.org',
    url='https://github.com/bitterjug/tabular-data-specification',
    packages=['colspec'],
    long_description=open('README.rst').read(),
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
