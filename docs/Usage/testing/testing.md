---
title: Tests
weight: 80
---
<!---
roam-ignore
-->
## Overview

### Test Coverage
[View Results](../../../coverage.md)

## Running Tests

To run all tests, navigate to the root directory of the project and execute:

```bash
pytest
```

This command will automatically discover and run all test files in the project.

## Writing Tests

When contributing to the project, please adhere to the following guidelines for writing tests:

- **Location**: Place your test files in the `tests` directory.
- **Naming**: Follow the naming convention `test_<module>.py` for test files and `test_<function>` for test functions.
- **Structure**: Organize tests to mirror the structure of the source code for easy navigation.

## Test Coverage

To measure test coverage, you can use the `pytest-cov` plugin. Install it via pip if not already installed:

```bash
pip install pytest-cov
```

Run tests with coverage reporting:

```bash
pytest --cov=frame
```

This will display a coverage report in the terminal. For a more detailed report, generate an HTML report:

```bash
pytest --cov=frame --cov-report=html
```

Open the `htmlcov/index.html` file in a browser to view the coverage report.

For the latest coverage report, please refer to [coverage](coverage.md).

To run tests for an individual class or file:

```bash
pytest tests/frame/src/services/llm/llm_adapters/lmql/test_lmql_adapter.py 
```

*Note*: Testing can take a little while as we have tests for rate limiting / retry logic, so you can exclude those (they are in the `llm_adapter` tests) if it's slow while developing others:
```python
pytest -k "not (llm_service or llm_adapter)"
```

