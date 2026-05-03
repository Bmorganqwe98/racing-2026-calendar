# Testing Guidelines

## Testing Framework

### Primary Framework: pytest
- Use pytest for all new tests
- Leverage pytest fixtures for setup/teardown
- Use pytest markers for test organization
- Use pytest parametrize for data-driven tests

### Installation
```bash
pip install pytest pytest-cov
```

## Test Organization

### Directory Structure
```
tests/
├── __init__.py
├── test_generate.py        # ICS event construction, UID stability, TBA handling
├── test_yaml_schema.py     # YAML loader + schema validation
├── test_timezones.py       # tz lookup + DST boundary cases
└── fixtures/
    └── sample_series.yaml
```

### File Naming
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Test Organization
- One test file per module
- Group related tests in classes
- Use descriptive test names

Example:
```python
class TestSessionEvent:
    """Test session-event construction in generate.py."""

    def test_event_has_tzid_dtstart(self):
        """DTSTART carries TZID when session.tz is set."""
        pass

    def test_uid_is_stable_across_runs(self):
        """Same input YAML produces the same UID on every regeneration."""
        pass
```

## Writing Tests

### Test Structure
1. **Arrange**: Set up test data and conditions
2. **Act**: Execute the code being tested
3. **Assert**: Verify the results

Example:
```python
def test_build_session_event_attaches_tz():
    sample = {
        "type": "Race",
        "start": "2026-03-08T15:00",
        "duration_minutes": 120,
    }
    round_info = {"name": "Australian GP", "tz": "Australia/Melbourne"}

    event = build_session_event(sample, round_info, series_slug="f1")

    assert "TZID=Australia/Melbourne" in event.to_ical().decode()
    assert event["UID"].startswith("f1-2026-r")
```

### Test Naming
- Be descriptive: `test_what_when_then`
- Examples:
  - `test_build_event_uses_session_tz_not_utc`
  - `test_tba_session_emits_all_day_event_with_note`
  - `test_uid_stays_stable_when_yaml_reformatted`

### Test Coverage Goals
- **Core Logic**: > 80% coverage
- **Critical Paths**: 100% coverage
- **Edge Cases**: Test all edge cases
- **Error Handling**: Test error paths

### What to Test

**Must Test:**
- All public functions and methods
- Business logic and calculations
- Error handling and edge cases
- Integration between components
- Database operations

**Should Test:**
- Helper functions
- Data transformations
- Validation logic
- Configuration handling

**Optional:**
- Simple getters/setters
- Trivial functions
- Third-party library code

## Test Types

### Unit Tests
- Test individual functions/methods in isolation
- Mock external dependencies
- Fast execution
- Most common test type

```python
def test_default_duration_for_practice_session():
    """FP sessions default to 60 minutes when duration_minutes is omitted."""
    sample = {"type": "FP1", "start": "2026-03-06T12:30"}
    duration = resolve_duration(sample)
    assert duration == timedelta(minutes=60)
```

### Integration Tests
- Test multiple components working together
- Use real dependencies where possible
- Test data flow between components

```python
def test_full_series_round_trip(tmp_path):
    """Loading a series YAML, building events, writing .ics, then reparsing yields the same event count."""
    series_yaml = tmp_path / "f1.yaml"
    series_yaml.write_text(SAMPLE_F1_YAML)
    cal = build_calendar(series_yaml)
    out = tmp_path / "f1.ics"
    out.write_bytes(cal.to_ical())

    reparsed = Calendar.from_ical(out.read_bytes())
    assert len(list(reparsed.walk("VEVENT"))) == len(list(cal.walk("VEVENT")))
```

### Fixtures
- Use pytest fixtures for common setup
- Share fixtures across tests
- Use scope appropriately (function, class, module)

```python
@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    # Setup
    db_path = create_temp_db()
    yield db_path
    # Teardown
    cleanup_temp_db(db_path)
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Tests
```bash
pytest tests/test_generate.py
pytest tests/test_generate.py::TestSessionEvent::test_uid_is_stable_across_runs
```

### Run with Coverage
```bash
pytest --cov=generate --cov-report=html
```

### Run with Verbose Output
```bash
pytest -v
pytest -vv  # Even more verbose
```

### Run Specific Markers
```bash
pytest -m unit
pytest -m integration
```

## Test Markers

Use markers to categorize tests:

```python
import pytest

@pytest.mark.unit
def test_unit_function():
    pass

@pytest.mark.integration
def test_integration_flow():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass
```

## Mocking

### When to Mock
- External APIs
- Database operations (in unit tests)
- File system operations
- Network requests
- Time-dependent functions

### Using unittest.mock
```python
from unittest.mock import patch

@patch('generate.fetch_remote_schedule')
def test_offline_run(mock_fetch):
    mock_fetch.return_value = {"rounds": []}
    # Test code that exercises the offline path
```

## Test Data

### Fixtures for Test Data
```python
@pytest.fixture
def sample_session():
    return {
        "type": "Race",
        "start": "2026-03-08T15:00",
        "duration_minutes": 120,
    }

@pytest.fixture
def sample_round():
    return {
        "round": 1,
        "name": "Australian Grand Prix",
        "circuit": "Albert Park Circuit",
        "location": "Melbourne, Australia",
        "tz": "Australia/Melbourne",
    }
```

### Test Databases
- Use temporary databases for tests
- Clean up after tests
- Use fixtures for database setup

## Best Practices

### Test Independence
- Each test should be independent
- Tests should not depend on execution order
- Clean up after each test
- Use fixtures for setup/teardown

### Test Clarity
- Write clear, readable tests
- Use descriptive names
- Add comments for complex test logic
- Keep tests focused (one assertion per test when possible)

### Test Maintenance
- Update tests when code changes
- Remove obsolete tests
- Refactor tests like production code
- Keep tests fast

### Test Coverage
- Aim for > 80% coverage on core logic
- Don't sacrifice quality for coverage
- Focus on meaningful tests
- Use coverage reports to find gaps

## Continuous Integration

### Pre-commit Checks
- Run tests before committing
- Ensure all tests pass
- Check coverage thresholds

### CI Pipeline
1. Install dependencies
2. Run linters
3. Run tests with coverage
4. Check coverage thresholds
5. Report results

## Common Patterns

### Testing Async Functions
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Testing Exceptions
```python
def test_raises_exception():
    with pytest.raises(ValueError):
        function_that_raises()
```

### Testing with Parameters
```python
@pytest.mark.parametrize("input,expected", [
    ([True, True], 0.8),
    ([False, False], 0.1),
    ([True, False], 0.5),
])
def test_with_parameters(input, expected):
    result = calculate(input)
    assert result == pytest.approx(expected, abs=0.1)
```

## Debugging Tests

### Run with Print Statements
```bash
pytest -s  # Show print output
```

### Use pdb
```python
import pdb; pdb.set_trace()  # Breakpoint in test
```

### Verbose Output
```bash
pytest -vv  # Very verbose
pytest --tb=short  # Shorter traceback
```

