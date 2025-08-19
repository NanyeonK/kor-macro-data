# Contributing to Korean Macro Data Package

Thank you for your interest in contributing to the Korean Macro Data package! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## 🚀 Getting Started

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/kor-macro-data.git
   cd kor-macro-data
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## 📝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version and OS
- Package version
- Relevant code snippets
- Error messages (full traceback)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear and descriptive title
- Detailed description of the proposed feature
- Use cases and examples
- Why this enhancement would be useful
- Possible implementation approach

### Pull Requests

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Add or update tests as needed

4. Update documentation if you're changing functionality

5. Run tests locally:
   ```bash
   pytest tests/
   ```

6. Run code quality checks:
   ```bash
   black kor_macro/
   flake8 kor_macro/
   mypy kor_macro/
   ```

7. Commit your changes:
   ```bash
   git commit -m "Add feature: brief description"
   ```

8. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

9. Create a Pull Request on GitHub

## 📋 Coding Standards

### Python Style Guide

- Follow PEP 8
- Use Black for code formatting (line length: 100)
- Use type hints where appropriate
- Write descriptive variable names
- Add docstrings to all functions, classes, and modules

### Docstring Format

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception occurs
        
    Example:
        >>> function_name(value1, value2)
        expected_result
    """
```

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## 🧪 Testing

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the structure of the main codebase
- Use pytest for testing
- Aim for >80% code coverage
- Include both unit tests and integration tests

Example test:
```python
import pytest
from kor_macro import DataMerger

def test_data_merger_initialization():
    """Test DataMerger initialization."""
    merger = DataMerger()
    assert merger is not None
    assert merger.datasets == {}

def test_data_merger_with_invalid_input():
    """Test DataMerger with invalid input."""
    merger = DataMerger()
    with pytest.raises(ValueError):
        merger.load_data(None, "test")
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=kor_macro

# Run specific test file
pytest tests/test_merger.py

# Run with verbose output
pytest -v
```

## 📚 Documentation

### Documentation Standards

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update CHANGELOG.md

### Building Documentation

```bash
cd docs/
make html
```

## 🔄 Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add entry to CHANGELOG.md
4. Request review from maintainers
5. Address review comments
6. Squash commits if requested
7. PR will be merged once approved

## 📦 Adding New Data Sources

When adding support for new data sources:

1. Create a new connector in `kor_macro/connectors/`
2. Inherit from `BaseConnector`
3. Implement required methods
4. Add column mappings for English standardization
5. Add tests for the new connector
6. Update documentation with usage examples
7. Add the new source to README.md

Example:
```python
from kor_macro.connectors.base import BaseConnector

class NewSourceConnector(BaseConnector):
    """Connector for New Data Source."""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv("NEW_SOURCE_API_KEY")
    
    def fetch_data(self, params: dict) -> pd.DataFrame:
        """Fetch data from the new source."""
        # Implementation here
        pass
```

## 🌏 Internationalization

When adding Korean data sources:
- Provide English translations for all column names
- Add mappings to `COLUMN_MAPPINGS` dictionary
- Document both Korean and English names
- Ensure UTF-8 encoding throughout

## 📈 Performance Considerations

- Use vectorized operations with pandas
- Implement caching for API calls
- Add progress bars for long operations
- Optimize memory usage for large datasets
- Profile code for bottlenecks

## 🔒 Security

- Never commit API keys or secrets
- Use environment variables for configuration
- Validate all user inputs
- Sanitize file paths
- Follow secure coding practices

## 🎯 Areas for Contribution

Current areas where we need help:

- [ ] Additional data source connectors
- [ ] Visualization modules
- [ ] Machine learning integration
- [ ] Performance optimizations
- [ ] Documentation translations
- [ ] Example notebooks
- [ ] Test coverage improvement
- [ ] CLI enhancements

## 💬 Questions?

Feel free to:
- Open an issue for questions
- Join discussions in existing issues
- Contact maintainers

## 🙏 Recognition

Contributors will be recognized in:
- AUTHORS.md file
- Release notes
- Project documentation

Thank you for contributing to Korean Macro Data Package!