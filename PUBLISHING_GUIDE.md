# Publishing to PyPI - Complete Guide

This guide covers the complete process of publishing the Korean Macro Data package to PyPI (Python Package Index).

## 📋 Pre-Publication Checklist

Before publishing, ensure:

- [ ] All tests pass (`pytest tests/`)
- [ ] Documentation is up to date
- [ ] CHANGELOG.md reflects new version
- [ ] Version number updated in `setup.py` and `pyproject.toml`
- [ ] README.md is complete and accurate
- [ ] LICENSE file is present
- [ ] All API keys removed from code
- [ ] No sensitive data in repository

## 🚀 Step-by-Step Publication Process

### 1. Setup PyPI Account

1. Create account at https://pypi.org/account/register/
2. Create account at https://test.pypi.org/account/register/ (for testing)
3. Generate API tokens:
   - Go to Account Settings → API tokens
   - Create token with scope "Entire account" or specific to project
   - Save tokens securely

### 2. Configure Authentication

Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PRODUCTION_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
repository = https://test.pypi.org/legacy/
```

Secure the file:
```bash
chmod 600 ~/.pypirc
```

### 3. Install Build Tools

```bash
pip install --upgrade pip setuptools wheel twine build
```

### 4. Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### 5. Run Final Checks

```bash
# Run all tests
pytest tests/ --cov=kor_macro

# Check code quality
black kor_macro/
flake8 kor_macro/
mypy kor_macro/

# Validate setup.py
python setup.py check --strict

# Check package metadata
twine check dist/*  # After building
```

### 6. Update Version Number

Update version in multiple files:

**setup.py:**
```python
setup(
    name="kor-macro-data",
    version="1.0.0",  # Update this
    ...
)
```

**pyproject.toml:**
```toml
[project]
name = "kor-macro-data"
version = "1.0.0"  # Update this
```

**kor_macro/__init__.py:**
```python
__version__ = "1.0.0"  # Update this
```

### 7. Build the Package

```bash
# Using build (recommended)
python -m build

# Or using setup.py
python setup.py sdist bdist_wheel
```

This creates:
- `dist/kor-macro-data-1.0.0.tar.gz` (source distribution)
- `dist/kor_macro_data-1.0.0-py3-none-any.whl` (wheel distribution)

### 8. Test with TestPyPI

Upload to TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

Test installation:

```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ kor-macro-data

# Test import
python -c "import kor_macro; print(kor_macro.__version__)"

# Run basic tests
python -c "from kor_macro import KoreanMacroDataMerger; m = KoreanMacroDataMerger(); print('Success!')"
```

### 9. Publish to PyPI

Once testing passes:

```bash
twine upload dist/*
```

Or specify explicitly:

```bash
twine upload dist/kor-macro-data-1.0.0.tar.gz dist/kor_macro_data-1.0.0-py3-none-any.whl
```

### 10. Verify Publication

1. Check package page: https://pypi.org/project/kor-macro-data/
2. Test installation:

```bash
pip install kor-macro-data
```

## 📦 Version Management

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

Examples:
- `1.0.0` → `1.0.1`: Bug fix
- `1.0.1` → `1.1.0`: New feature
- `1.1.0` → `2.0.0`: Breaking change

### Creating a Release

1. Update version numbers
2. Update CHANGELOG.md
3. Commit changes:
   ```bash
   git add .
   git commit -m "Release version 1.0.0"
   ```

4. Create git tag:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0 release"
   git push origin v1.0.0
   ```

5. Create GitHub release:
   - Go to Releases → Create new release
   - Select tag
   - Add release notes from CHANGELOG.md
   - Attach built distributions

## 🔄 Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add PyPI token to GitHub secrets:
1. Go to Settings → Secrets → Actions
2. Add `PYPI_API_TOKEN` with your token

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid distribution file"**
   - Rebuild with clean environment
   - Check setup.py for errors

2. **"Version already exists"**
   - Increment version number
   - Delete old builds

3. **"Authentication failed"**
   - Check API token
   - Verify ~/.pypirc format

4. **Missing dependencies**
   ```bash
   pip install --upgrade setuptools wheel twine
   ```

5. **README rendering issues**
   - Validate with: `twine check dist/*`
   - Use online validator: https://pypi.org/project/readme-renderer/

## 📊 Post-Publication

### Monitor Package

- Check download statistics: https://pypistats.org/packages/kor-macro-data
- Monitor issues: GitHub Issues
- Track dependencies: https://libraries.io/pypi/kor-macro-data

### Update Documentation

- Update README with installation instructions
- Add PyPI badge to README:
  ```markdown
  [![PyPI version](https://badge.fury.io/py/kor-macro-data.svg)](https://pypi.org/project/kor-macro-data/)
  ```

### Announce Release

- GitHub release notes
- Project website/blog
- Social media
- Mailing list

## 🔒 Security Best Practices

1. **Never commit tokens**
   - Use environment variables
   - Add `.pypirc` to `.gitignore`

2. **Use 2FA on PyPI**
   - Enable at https://pypi.org/manage/account/

3. **Sign releases** (optional)
   ```bash
   gpg --detach-sign -a dist/package.tar.gz
   ```

4. **Verify packages**
   ```bash
   pip download --no-deps kor-macro-data
   # Check hash matches PyPI
   ```

## 📝 Maintenance

### Yanking Bad Releases

If you need to remove a broken version:

```bash
# Via web interface
# Go to project page → Manage → Releases → Select version → Yank

# Note: Yanked versions can still be installed explicitly
pip install kor-macro-data==1.0.0  # Still works if yanked
```

### Updating Package Metadata

To update description, keywords, etc.:
1. Update setup.py/pyproject.toml
2. Increment patch version
3. Rebuild and republish

## 📚 Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)

## Quick Command Reference

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload to test
twine upload --repository testpypi dist/*

# Upload to production
twine upload dist/*

# Install from test
pip install -i https://test.pypi.org/simple/ kor-macro-data

# Install from production
pip install kor-macro-data
```

---

**Remember**: Once published to PyPI, packages cannot be deleted (only yanked). Test thoroughly with TestPyPI first!