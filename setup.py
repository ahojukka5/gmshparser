import setuptools

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
gmshparser is a lightweight and well-tested package that aims to reliably parse
the Gmsh ascii file format (.msh). The package does not introduce any external
dependencies and thus fits well with the needs of your own FEM research code.
"""

setuptools.setup(
    name="gmshparser",
    version="0.1.0",
    author="Jukka Aho",
    author_email="ahojukka5@gmail.com",
    description=description,
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
)
