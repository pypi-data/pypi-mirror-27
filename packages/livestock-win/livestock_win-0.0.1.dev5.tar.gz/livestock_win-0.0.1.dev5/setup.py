# Imports
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'livestock_win\README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='livestock_win',
    version='0.0.1.dev5',
    description='Livestock is a plugin/library for Grasshopper written in Python',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ocni-dtu/livestock_gh',

    # Author details
    author='Christian Kongsgaard Nielsen',
    author_email='ocni@dtu.dk',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Professionals and students',
        'Topic :: Environmental Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='hydrology 3dmodeling grasshopper',
    packages=['livestock_win'],
    install_requires=['numpy', 'paramiko'],

    # Python requirement
    python_requires='>=3',

    entry_points={
        'console_scripts': [
            'livestock_win=livestock_win:main',
        ],
    },
)