#!/usr/bin/env python3

from setuptools import setup
from os import path
from chroma import Settings as S

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="chromawizard",
    url="https://gitlab.com/nauer/chromawizard",
    version=S.__version__,
    author="Norbert Auer",
    description="Chromosome painting software",
    long_description=long_description,
    license="GPL 3.0",
    author_email="norbert.auer@boku.ac.at",
    entry_points={'gui_scripts': ['chromawizard=chroma.__main__:main']},
    packages=["chroma"],
    package_data={'chroma': ['config.json', 'icons/*', 'images/*', 'lang/de/LC_MESSAGES/*', 'lang/en/LC_MESSAGES/*']},
    install_requires=["pillow>=3.0.0", "numpy>=1.10.2", "opencv-python>=3.0.0", "PyQt5>=5.7"], # Does not work with conda
    keywords='chromosome-painting FISH M-FISH CHO-K1',
    classifiers=[
         # How mature is this project? Common values are
         #   3 - Alpha
         #   4 - Beta
         #   5 - Production/Stable
         'Development Status :: 5 - Production/Stable',

         # Indicate who your project is intended for
         'Intended Audience :: Science/Research',
         'Topic :: Scientific/Engineering :: Visualization',

          # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

         # Specify the Python versions you support here. In particular, ensure
         # that you indicate whether you support Python 2, Python 3 or both.
         'Programming Language :: Python :: 3.5',
         'Programming Language :: Python :: 3.6',
    ]
)
