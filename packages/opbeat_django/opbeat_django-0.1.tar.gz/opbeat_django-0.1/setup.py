#!/usr/bin/env python3
"""
Opbeat-Django, an unofficial Python client for Opbeat.

It provides an API wrapper and a Django management command for release tracking.
"""

from setuptools import setup, find_packages

VERSION = '0.1'

INSTALL_REQUIRES = [
    'requests>=2.10',
]

setup(
    name='opbeat_django',
    version=VERSION,
    author='Netquity Corp',
    author_email='hello@netquity.com',
    url='https://github.com/netquity/opbeat_django',
    description='An unofficial API client for Opbeat',
    long_description="""Opbeat-Django
=============
opbeat_django is an unofficial Python client for `Opbeat <https://opbeat.com/>`_.
It provides a simple API wrapper and a Django management command for release
tracking. Is not really dependent on Django, can be used without.
""",
    packages=find_packages(),
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='opbeat django',
)
