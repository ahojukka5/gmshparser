import setuptools

# https://packaging.python.org/guides/single-sourcing-package-version/

import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

test_deps = [
    'pytest',
    'pytest-cov',
    'pytest-pycodestyle',
    'pytest-pep8',
    'pytest-flake8',
]

extras = {
    'test': test_deps,
}

description = """
gmshparser is a lightweight, 100 % tested and well documented package that aims
to reliably parse the Gmsh ascii file format (.msh). The package does not
introduce any external dependencies and thus fits well with the needs of your
own FEM research code as a small stand-alone package. Project is hosted on
GitHub (https://github.com/ahojukka5/gmshparser) and documentation can be
found from ReadTheDocs (https://gmshparser.readthedocs.io/).
"""

entry_points = {
    'console_scripts': ['gmshparser=gmshparser.cli:main'],
}

setuptools.setup(
    name="gmshparser",
    version=get_version("gmshparser/__init__.py"),
    author="Jukka Aho",
    author_email="ahojukka5@gmail.com",
    description=" ".join(description.strip().splitlines()),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahojukka5/gmshparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=test_deps,
    extras_require=extras,
    entry_points=entry_points,
)
