#!/usr/bin/python3
# vim: set fileencoding=utf-8 :
"""
Flask-XStatic-Files
-------------------

Make using xstatic files simple
"""
from setuptools import setup


def readme():
    with open('README.rst') as file:
        return file.read()


setup(
    name='Flask-XStatic-Files',
    version='0.0.1',
    url='http://github.com/agx/flask-xstatic-files',
    license='LGPLv3+',
    author='Guio Günther',
    author_email='agx@sigxcpu.org',
    description='Easily use XStatic files in flask',
    long_description=readme(),
    py_modules=['flask_xstatic_files'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'XStatic',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
