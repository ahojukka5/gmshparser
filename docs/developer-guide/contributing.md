# Contributing

Thank you for your interest in contributing to gmshparser! This guide will help you get started.

## Ways to Contribute

### Report Bugs

Found a bug? Please [open an issue](https://github.com/ahojukka5/gmshparser/issues) with:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your Python version and operating system
- Sample mesh file (if applicable)

### Suggest Features

Have an idea for improvement? [Open an issue](https://github.com/ahojukka5/gmshparser/issues) describing:

- The feature you'd like to see
- Why it would be useful
- Potential implementation approach

### Improve Documentation

Documentation improvements are always welcome:

- Fix typos or clarify explanations
- Add examples
- Improve API documentation
- Translate documentation

### Submit Code

#### Getting Started

1. **Fork the repository**

   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/gmshparser.git
   cd gmshparser
   ```

2. **Set up development environment**

   ```bash
   # Install Poetry (if not already installed)
   curl -sSL https://install.python-poetry.org | python3 -

   # Install dependencies
   poetry install

   # Activate virtual environment
   poetry shell
   ```

3. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Development Workflow

1. **Make your changes**

   Write code following the project style (see below).

2. **Run tests**

   ```bash
   pytest
   ```

   Ensure all tests pass and coverage remains high:

   ```bash
   pytest --cov=gmshparser --cov-report=term-missing
   ```

3. **Format code**

   ```bash
   black .
   ```

4. **Check code quality**

   ```bash
   flake8 gmshparser tests
   ```

5. **Commit your changes**

   Write clear, descriptive commit messages:

   ```bash
   git add .
   git commit -m "Add support for XYZ feature

   - Implemented XYZ parser
   - Added tests for XYZ
   - Updated documentation"
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a pull request**

   Go to GitHub and create a pull request from your fork to the main repository.

## Coding Standards

### Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use `black` for formatting (line length: 88)
- Use `flake8` for linting
- Write docstrings for all public functions/classes

### Example

```python
def parse_section(mesh: Mesh, io: TextIO) -> None:
    """Parse a section from the mesh file.

    Args:
        mesh: The Mesh object to populate
        io: File handle to read from

    Returns:
        None

    Raises:
        ValueError: If section format is invalid
    """
    line = io.readline().strip()
    # Implementation...
```

### Code Organization

- Keep functions focused and small
- Use type hints
- Avoid deep nesting (max 3-4 levels)
- Write self-documenting code

## Testing

### Writing Tests

Every feature should have tests:

```python
# tests/test_new_feature.py
def test_new_feature():
    """Test description."""
    # Arrange
    mesh = gmshparser.parse("data/test_mesh.msh")
    
    # Act
    result = mesh.get_something()
    
    # Assert
    assert result == expected_value
```

### Test Coverage

- Aim for 100% coverage on new code
- Test edge cases and error conditions
- Include integration tests for parsers

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_helpers.py

# Run specific test
pytest tests/test_helpers.py::test_get_triangles

# Run with coverage
pytest --cov=gmshparser --cov-report=html
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def get_triangles(mesh: Mesh) -> Tuple[List[float], List[float], List[List[int]]]:
    """Extract triangular elements from mesh.

    Args:
        mesh: Parsed mesh object

    Returns:
        Tuple of (X, Y, T) where:
            X: List of x-coordinates
            Y: List of y-coordinates
            T: List of triangle connectivity

    Example:
        >>> mesh = gmshparser.parse("mesh.msh")
        >>> X, Y, T = get_triangles(mesh)
        >>> print(len(T))  # Number of triangles
        42
    """
    # Implementation...
```

### Documentation Files

- Update relevant `.md` files in `docs/`
- Add examples to user guide
- Update API reference if needed

### Building Documentation

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Open in browser
open http://127.0.0.1:8000
```

## Pull Request Process

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted with `black`
- [ ] No `flake8` warnings
- [ ] Documentation is updated
- [ ] CHANGELOG is updated (if applicable)
- [ ] Commit messages are clear

### PR Description

Include in your PR description:

- **What**: Brief description of changes
- **Why**: Reason for the change
- **How**: Implementation approach
- **Testing**: How you tested the changes

### Review Process

1. Automated checks run (CI/CD)
2. Maintainer reviews code
3. Address any feedback
4. Once approved, PR is merged

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `gmshparser/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.x.0`
4. Push tag: `git push origin v0.x.0`
5. Build and publish: `poetry publish --build`

## Communication

### Contact

- **Issues**: [GitHub Issues](https://github.com/ahojukka5/gmshparser/issues)
- **Email**: <ahojukka5@gmail.com>
- **Discussions**: Use GitHub Discussions for questions

### Code of Conduct

Be respectful, inclusive, and constructive. We want gmshparser to be welcoming to all contributors.

## Recognition

Contributors are recognized in:

- GitHub contributors page
- Release notes
- Documentation (if significant contribution)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask! Open an issue or send an email. We're happy to help new contributors.

## Thank You

Your contributions make gmshparser better for everyone. Thank you for taking the time to contribute! 🎉
