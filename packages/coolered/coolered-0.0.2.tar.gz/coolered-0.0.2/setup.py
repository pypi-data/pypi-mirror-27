from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='coolered',
    version="0.0.2",
    description='A better dslackw/colored',
    long_description=long_description,
    url='https://github.com/llamicron/coolered',
    author='Luke Sweeney',
    author_email='llamicron@gmail.com',
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='development color terminal text codes ascii colored coolered color-terminal',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['colored'],
    # $ pip install sampleproject[dev]
    extras_require={
        'test': ['coverage', 'pytest']
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },
    entry_points={  # Optional
        'console_scripts': [
            'coolered=coolered:demo',
        ],
    },
)
