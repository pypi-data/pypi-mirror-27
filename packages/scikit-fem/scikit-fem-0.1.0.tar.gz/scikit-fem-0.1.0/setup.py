from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scikit-fem',
    version='0.1.0',
    description='Simple finite element assemblers',
    long_description=long_description,  # Optional
    url='https://github.com/kinnala/skfem',
    author='Tom Gustafsson',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='sample setuptools development',  # Optional
    packages=find_packages(exclude=['examples']),  # Required
    install_requires=['numpy', 'scipy', 'sympy', 'matplotlib'],  # Optional
    extras_require={  # Optional
        'all': ['pyevtk'],
    },
    download_url = 'https://github.com/kinnala/scikit-fem/archive/0.1.0.tar.gz'
)
