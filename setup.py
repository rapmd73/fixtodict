from setuptools import setup, find_packages
from os import path
from io import open

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

version = {}

with open(path.join(HERE, 'fixtodict', "version.py"), encoding='utf-8') as f:
    exec(f.read(), version)

setup(
    name="fixtodict",
    version=version["__version__"],
    description='FIX Dictionary generator tool',
    long_description=LONG_DESCRIPTION,
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
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=['nltk', "click", "checksumdir==1.1.7",
                      "dict-recursive-update==1.0.1", "jsonpatch==1.25", "jsonschema==3.2.0"],
    entry_points="""
    [console_scripts]
    fixtodict=fixtodict.cli:cli
    """,
    test_suite='nose.collector',
    tests_require=['nose'],
)
