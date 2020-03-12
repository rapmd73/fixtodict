from setuptools import setup
from os import path
from io import open

VERSION = {}

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'fixtodict', "version.py"), encoding='utf-8') as f:
    exec(f.read(), VERSION)

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="fixtodict",
    version=VERSION["__version__"],
    description='FIX Dictionary generator tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fixipe/fixtodict',
    author='Filippo Costa @neysofu',
    author_email='filippocosta.italy@gmail.com',
    license="Apache Software License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='FIX protocol XML fintech finance trading',
    packages=["fixtodict"],
    python_requires='>=3.5',
    install_requires=['nltk', "click"],
    entry_points="""
    [console_scripts]
    fixtodict=fixtodict.cli:main
    """,
    test_suite='nose.collector',
    tests_require=['nose'],
)
