#!/usr/bin/env python3

"""
    Copyright (c) 2017 Martin F. Falatic

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

PACKAGE_DATA = {
    'friendly_name': 'RemotePdb Client',
    'name': 'remote-pdb-client',
    'version': '0.9.1',
    'url': 'https://github.com/MartyMacGyver/remote-pdb-client',
    'author': 'Martin F. Falatic',
    'author_email': 'martin@falatic.com',
    'copyright': 'Copyright (c) 2017',
    'license': 'MIT License',
    'description': 'A client for the RemotePDB debugger',
    'long_description': """
`remotepdb_client --help` for more information

This is a development release and is not considered final

For Windows, OS X and Linux
    """,
    'keywords': 'remotepdb debugging pdb telnet',
    'classifiers': [
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
    ],
    'packages': [
        'remotepdb_client',
    ],
    'entry_points': {
        'console_scripts': [
            'remotepdb_client=remotepdb_client.remotepdb_client:main',
        ],
    },
    'install_requires': [
        'colorama>=0.3.9',
        'prompt-toolkit>=1.0.15'
    ],
    'extras_require': {},
    'package_data': {},
    'data_files': [],
}
