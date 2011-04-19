#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from serveme import __version__

setup(
    name = 'serve.me',
    version = __version__,
    description = "serve.me is a quick and dirty webserver to serve the current folder",
    long_description = """
serve.me is a quick and dirty webserver to serve the current folder as statics in the specified port
""",    
    keywords = 'web server static files',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    url = 'http://github.com/heynemann/serve.me',
    license = 'MIT',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages = find_packages(),
    package_dir = {"serveme": "serveme"},
    include_package_data = True,
    package_data = {
    },

    install_requires=[
        "tornado"
    ],

    entry_points = {
        'console_scripts': [
            'serveme = serveme.app:main',
        ],
    },


)

