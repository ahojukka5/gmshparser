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

setuptools.setup(
    name="gmshparser",
    version="0.1.0",
    author="Jukka Aho",
    author_email="ahojukka5@gmail.com",
    description="Package is used to parser Gmsh .msh file format",
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
