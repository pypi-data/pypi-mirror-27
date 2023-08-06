# coding:utf-8
from setuptools import setup, find_packages
from io import open

setup(
    name='checksum-cli',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/cupen/checksum-cli',
    license='WTFPL',
    author='cupen',
    author_email='cupen@foxmail.com',
    description='A command line interface program use for generate the checksum of file.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    python_requires='>=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    keywords='checksum cli',
    entry_points={
       "console_scripts": [
           "checksum = checksum:main_argv",
       ],
    },

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
