#!/usr/bin/env python

from setuptools import (
    find_packages,
    setup,
)


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='prose-wc',
    version='0.3.4',
    description='Jekyll-aware prose wordcount utility',
    long_description=long_description,
    author='Madison Scott-Clary',
    author_email='makyo@drab-makyo.com',
    install_requires=['argparse', 'bs4', 'markdown', 'pyyaml'],
    packages=find_packages(),
    setup_requires=['nose>=1.0'],
    tests_require=['nose', 'coverage', 'mock>=2.0'],
    entry_points={
        'console_scripts': [
            'prose-wc = prose_wc.wc:run',
        ],
    },
    url='https://github.com/makyo/prose-wc',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Artistic Software',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ])
