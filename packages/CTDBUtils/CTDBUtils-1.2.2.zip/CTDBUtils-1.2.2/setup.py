"""Setup Script for DBUtils"""

from sys import version_info

__version__ = '1.2.2'

py_version = version_info[:2]
if py_version < (2, 6):
    raise ImportError('Python %d.%d is not supported by CTDBUtils.' % py_version)

import warnings
warnings.filterwarnings('ignore', 'Unknown distribution option')

from distutils.core import setup

setup(
    name='CTDBUtils',
    version=__version__,
    description='Database connections for multi-threaded environments.',
    long_description='''\
CTDBUtils is a suite of tools providing solid, persistent and pooled connections
to a database that can be used in all kinds of multi-threaded environments
like Webware for Python or other web application servers. The suite supports
DB-API 2 compliant database interfaces and the classic PyGreSQL interface.

Based on https://cito.github.io/CTDBUtils/
''',
    classifiers=['Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    author='Xu Rui',
    author_email='xurui1@chinatelecom.cn',
    url='https://github.com/189cn/CTDBUtils',
    platforms=['any'],
    license='MIT License',
    packages=['CTDBUtils', 'CTDBUtils.Examples', 'CTDBUtils.Tests'],
    package_data={'CTDBUtils': ['Docs/*']}
)
