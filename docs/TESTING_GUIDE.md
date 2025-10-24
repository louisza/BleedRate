# 🧪 Testing Guide - BleedRate

Complete guide for running and automating tests in BleedRate.

## 🚀 Quick Start

```bash
# 1. Install all dependencies (including test tools)
make install

# 2. Install pre-commit hooks (one-time setup)
pre-commit install

# 3. Run tests
make test
```

## 📋 Available Test Commands

### Basic Testing
```bash
# Run all tests with coverage
make test

# Run with detailed output + HTML coverage report
make test-verbose

# Fast mode: stop at first failure
make test-fast

# Run specific test file
make test-specific
# Then enter: tests/test_calculators.py

# Run specific test function
pytest tests/test_calculators.py::test_alcohol_tax_beer -v
```

### Advanced Testing
```bash
# Watch mode: auto-run tests on file changes
make test-watch

# Parallel execution (uses all CPU cores)
make test-parallel

# Generate and open coverage report
make test-coverage

# CI mode: enforce 70% coverage minimum
make test-ci
```

### Test by Category (using markers)
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run only API tests
pytest -m api

# Run only calculation tests
pytest -m calculation
```

## 🎯 Test Markers

Add markers to your tests to categorize them:

```python
import pytest

@pytest.mark.unit
def test_simple_calculation():
    assert 1 + 1 == 2

@pytest.mark.integration
def test_database_integration():
    # Test with real database
    pass

@pytest.mark.slow
def test_complex_operation():
    # Tests that take >5 seconds
    pass

@pytest.mark.api
def test_endpoint():
    # API endpoint tests
    pass

@pytest.mark.calculation
def test_tax_calculation():
    # Tax calculation logic tests
    pass
```

## 🔄 Automated Testing with Pre-commit Hooks

Pre-commit hooks run automatically when you commit code!

### Setup (One-Time)
```bash
# Install pre-commit hooks
pre-commit install

# Test the hooks manually
pre-commit run --all-files
```

### What Runs Automatically

**On Every Commit:**
- ✅ Trailing whitespace removal
- ✅ End-of-file fixing
- ✅ YAML/JSON syntax checks
- ✅ Large file detection
- ✅ Black code formatting
- ✅ Ruff linting (with auto-fix)
- ✅ Bandit security checks
- ✅ **Fast tests** (non-slow tests only)

**On Every Push:**
- ✅ Full test suite with coverage check (70% minimum)

### Example Workflow
```bash
# Make changes
vim app/domain/calculators.py

# Stage changes
git add .

# Commit (pre-commit hooks run automatically!)
git commit -m "feat: add new calculator"

# If tests fail, commit is blocked
# Fix the issues and try again

# Push (coverage check runs)
git push origin dev
```

### Skip Hooks (Emergency Only)
```bash
# Skip pre-commit hooks (not recommended!)
git commit --no-verify -m "emergency fix"
```

## 🔍 GitHub Actions CI/CD

Automated testing runs on every push and PR!

### What Runs in CI

**Test Job:**
- ✅ Tests on Python 3.11 AND 3.12 (matrix testing)
- ✅ Parallel test execution (faster)
- ✅ Coverage reporting to Codecov
- ✅ Minimum 70% coverage enforced

**Security Job:**
- ✅ Bandit security scanning
- ✅ Security report artifacts

**Lint Job:**
- ✅ Black formatting check
- ✅ Ruff linting
- ✅ MyPy type checking (soft fail)

### View CI Results
1. Go to GitHub repository
2. Click "Actions" tab
3. See results for each push/PR

### CI Badge (Optional)
Add to README.md:
```markdown
[![Tests](https://github.com/louisza/BleedRate/actions/workflows/test.yml/badge.svg)](https://github.com/louisza/BleedRate/actions/workflows/test.yml)
```

## 📊 Coverage Reports

### View Coverage Locally
```bash
# Generate HTML coverage report
make test-coverage

# Opens in browser automatically
# Or manually open: htmlcov/index.html
```

### Coverage Settings
- **Minimum Required:** 70%
- **Configured in:** `pytest.ini`
- **Excludes:** 
  - `__init__.py` files
  - `config.py`
  - Test files themselves
  - Abstract methods

### Improve Coverage
```bash
# See which lines aren't covered
pytest --cov=app --cov-report=term-missing

# Focus on specific module
pytest --cov=app.domain.calculators --cov-report=term-missing
```

## 🏗️ Test Structure Best Practices

### Organize Tests by Domain
```
tests/
├── conftest.py              # Shared fixtures
├── test_calculators.py      # Tax calculation logic
├── test_engine.py           # Tax engine orchestration
├── test_api_public.py       # Public API endpoints
├── test_api_admin.py        # Admin API endpoints
├── test_rates.py            # Tax rates loading
└── test_profiles.py         # User profiles
```

### Write Good Tests
```python
import pytest
from app.domain.calculators import PAYECalculator

@pytest.mark.unit
@pytest.mark.calculation
def test_paye_calculation_basic():
    """Test basic PAYE calculation for middle income bracket"""
    # Arrange
    calculator = PAYECalculator(rates)
    profile = PersonalProfile(annual_salary=400000, age=35)
    
    # Act
    result = calculator.calculate(profile)
    
    # Assert
    assert result["PAYE (Income Tax)"] > 0
    assert result["UIF"] > 0
    assert result["UIF"] < 200  # UIF is capped
```

## 🐛 Troubleshooting

### Tests Not Running
```bash
# Check pytest is installed
pytest --version

# Reinstall dependencies
make install

# Clear cache
make clean
```

### Pre-commit Hooks Not Working
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Update hooks to latest versions
pre-commit autoupdate
```

### Coverage Too Low
```bash
# Find uncovered lines
pytest --cov=app --cov-report=term-missing

# See detailed HTML report
make test-coverage
```

### Slow Tests
```bash
# Skip slow tests during development
pytest -m "not slow"

# Find slowest tests
pytest --durations=10
```

## 📈 Testing Workflow

### Daily Development
```bash
# 1. Start working
make switch-to-dev

# 2. Run tests in watch mode (optional)
make test-watch

# 3. Make changes
vim app/domain/calculators.py

# 4. Tests auto-run (if using watch mode)
# Or run manually: make test-fast

# 5. Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: new feature"

# 6. Push (full coverage check runs)
git push origin dev

# 7. GitHub Actions runs full test suite
```

### Before Pull Request
```bash
# Run full test suite
make test-verbose

# Check coverage
make test-coverage

# Run security checks
bandit -r app/ -ll

# Run all pre-commit hooks
pre-commit run --all-files

# If all pass, create PR!
```

### Before Production Deploy
```bash
# Ensure all tests pass
make test-ci

# Check CI status on GitHub
# View GitHub Actions for latest results

# If green, promote to production
make promote-to-prod
```

## 🎓 Advanced Features

### Parallel Testing (Faster)
```bash
# Use all CPU cores
pytest -n auto

# Use specific number of cores
pytest -n 4
```

### Test Only Failed Tests
```bash
# Run only tests that failed last time
pytest --lf

# Run failed tests first, then all others
pytest --ff
```

### Debugging Tests
```bash
# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Very verbose output
pytest -vv
```

### Performance Profiling
```bash
# Show 10 slowest tests
pytest --durations=10

# Show all test durations
pytest --durations=0
```

## 📚 Configuration Files

- **`pytest.ini`** - Pytest configuration, coverage settings, markers
- **`.pre-commit-config.yaml`** - Pre-commit hook configuration
- **`.github/workflows/test.yml`** - GitHub Actions CI/CD pipeline
- **`Makefile`** - Test commands and shortcuts

## ✅ Checklist

### Initial Setup
- [ ] Run `make install`
- [ ] Run `pre-commit install`
- [ ] Run `make test` to verify setup
- [ ] Run `make test-coverage` to see initial coverage

### Daily Use
- [ ] Use `make test-watch` during development
- [ ] Let pre-commit hooks run on each commit
- [ ] Check GitHub Actions after push
- [ ] Maintain >70% test coverage

### Before Production
- [ ] All tests pass locally (`make test`)
- [ ] Coverage >70% (`make test-coverage`)
- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] GitHub Actions CI is green
- [ ] Security scan clean (`bandit -r app/ -ll`)

---

**Need Help?** Check the test output for specific error messages!
