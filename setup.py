import comparator

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

requirements = [
    'python-Levenshtein==0.12.0',
    'veryprettytable==0.8.1',
]

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='names_comparator',

    version=comparator.__version__,

    description='Simple tool to compare almost similar names which are coming from the same source (for example list of all company owners and officers of that company). Helps to cluster together persons with a slight difference in name spelling/typos. Better suited for Cyrillic names, but should work everywhere',
    long_description=long_description,

    url='https://github.com/dchaplinsky/comparator',

    author='dchaplinsky',
    author_email='chaplinsky.dmitry@gmail.com',

    license='MIT',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Natural Language :: Ukrainian',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
    ],

    keywords='names fuzzy comparison levenshtein',

    packages=[
        'comparator',
    ],

    include_package_data=True,

    package_data={'': ['LICENSE']},
)
