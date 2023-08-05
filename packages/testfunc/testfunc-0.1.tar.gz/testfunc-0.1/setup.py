from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='testfunc',
    version='0.1',

    description='A sample tool for testing functions',
    long_description=long_description,

    url='https://github.com/yanxurui/testfunc',

    # Author details
    author="Xurui Yan",
    author_email="yxr1993@gmail.com",

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='test',
    py_modules=["testfunc"],
    install_requires=['texttable>=1.1.1']
)
