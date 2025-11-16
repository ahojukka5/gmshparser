# Testing Guide

This guide covers testing practices for gmshparser development.

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_helpers.py
```

### Run with Coverage

```bash
pytest --cov=gmshparser --cov-report=term-missing
```

### Generate HTML Coverage Report

```bash
pytest --cov=gmshparser --cov-report=html
open htmlcov/index.html
```

## Writing Tests

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange - set up test data
    mesh = gmshparser.parse("testdata/simple/testmesh.msh")
    
    # Act - perform action
    result = mesh.get_nodes()
    
    # Assert - verify expectations
    assert len(result) > 0
```

### Testing Parsers

```python
def test_parser():
    """Test parser with known mesh file."""
    mesh = gmshparser.parse("testdata/simple/testmesh_v2_0.msh")
    
    assert mesh.get_version() == 2.0
    assert mesh.get_number_of_nodes() == 6
    assert mesh.get_number_of_elements() == 2
```

## Test Data

Test meshes are located in `testdata/`:

- `testdata/simple/` - Simple meshes for unit tests
- `testdata/complex/` - Complex meshes with mixed elements
- `testdata/large/` - Large meshes for performance testing

See [testdata/README.md](../../testdata/README.md) for details.

## Coverage Goals

- Target: 95%+ coverage
- Current: 97% coverage
- All new features must include tests

## Continuous Integration

Tests run automatically on every push via GitHub Actions.

## Next Steps

- See [Test Results](test-results.md) for current test status
- Check [Contributing Guide](contributing.md) for development workflow
