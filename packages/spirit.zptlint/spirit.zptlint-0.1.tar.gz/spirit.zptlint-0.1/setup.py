# -*- coding: utf-8 -*-
"""Setup for spirit.zptlint package."""

from setuptools import find_packages
from setuptools import setup

version = '0.1'
description = 'Linter for Zope Page Templates.'
long_description = ('\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
]))

install_requires = [
    'setuptools',
    # -*- Extra requirements: -*-
    'zope.contentprovider',
    'zope.pagetemplate',
    'zope.traversing',
]

setup(
    name='spirit.zptlint',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    keywords=[
        'zope',
        'linter,'
        'template',
    ],
    author='it-spirit',
    author_email='development@it-spir.it',
    url='https://github.com/it-spirit/spirit.zptlint',
    download_url='http://pypi.python.org/pypi/spirit.zptlint',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['spirit'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': [
        ]
    },
    entry_points={
        'console_scripts': [
            'zptlint = spirit.zptlint:run',
        ],
    },
)
