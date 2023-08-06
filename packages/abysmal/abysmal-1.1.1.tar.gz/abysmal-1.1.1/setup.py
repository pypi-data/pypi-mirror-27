#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import io
import os
import sys
from glob import glob
from os.path import basename, dirname, join, relpath, splitext

from setuptools import Extension, find_packages, setup


if not sys.version_info >= (3, 3):
    raise Exception('*** abysmal only supports Python 3.3 and above ***')


extra_compile_args = ['-O3'] # setuptools specifies -O2 -- override it
extra_link_args = ['-O3']    # setuptools specifies -O1 -- override it

if os.environ.get('ABYSMAL_STRICT'):
    extra_compile_args += [
        '-ansi',
        '-Wall',
        '-Wextra',
        '-Werror',
        '-Wconversion',
        '-Wpedantic',
        '-std=c99',
        '-Wno-missing-field-initializers',
    ]
if os.environ.get('ABYSMAL_TRACE'):
    extra_compile_args += [
        '-DABYSMAL_TRACE'
    ]


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf-8')
    ) as file_:
        return file_.read()

setup(
    name='abysmal',
    version='1.1.1',

    license='MIT license',
    url='https://github.com/zillow/abysmal',
    author='John-Anthony Owens',
    author_email='johnao@zillowgroup.com',

    description='Abysmal (Appallingly Basic Yet Somehow Mostly Adequate Language)',
    long_description=read('README.rst'),

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
    ],

    keywords=['absymal', 'programming', 'language'],

    python_requires='>= 3.3',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    zip_safe=False,

    ext_modules=[
        Extension(
            splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
            sources=[path],
            include_dirs=[dirname(path)],
            libraries=['mpdec'],
            undef_macros=['NDEBUG'] if os.environ.get('ABYSMAL_DEBUG') else [],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args
        )
        for root, _, _ in os.walk('src')
        for path in glob(join(root, '*.c'))
    ]
)
