# Coding Standards

## Python Version
- **Minimum**: Python 3.9+
- **Recommended**: Python 3.11 or later
- Use type hints where appropriate (Python 3.9+ supports most typing features)

## PEP 8 Compliance

### Code Style
- Follow PEP 8 style guide
- Maximum line length: 88 characters (Black formatter default)
- Use 4 spaces for indentation (no tabs)
- Use blank lines to separate functions and classes
- Use blank lines to separate logical sections within functions

### Naming Conventions
- **Modules**: `lowercase_with_underscores`
- **Classes**: `PascalCase`
- **Functions/Methods**: `lowercase_with_underscores`
- **Constants**: `UPPER_CASE_WITH_UNDERSCORES`
- **Private**: Prefix with single underscore `_private_method`
- **Name Mangling**: Double underscore only when necessary `__special`

### Import Organization
Imports should be organized in this order:
1. Standard library imports
2. Related third-party imports
3. Local application/library specific imports

Use blank lines to separate each group:
```python
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo

import yaml
from icalendar import Calendar, Event

from generate import build_event, load_series
```

### Type Hints
- Use type hints for function parameters and return types
- Use `Optional[Type]` for parameters that can be None
- Use `Union[Type1, Type2]` when multiple types are possible
- Use `List[Type]`, `Dict[KeyType, ValueType]` for collections
- Use `Sequence[Type]` for read-only sequences

Example:
```python
def process_data(
    data: List[Dict[str, Any]],
    filter_func: Optional[Callable] = None
) -> Dict[str, int]:
    """Process data and return statistics."""
    pass
```

### Docstrings
- Use Google-style docstrings
- Include description, Args, Returns, Raises sections
- Document all public functions, classes, and methods

Example:
```python
def build_session_event(
    session: Dict[str, Any],
    round_info: Dict[str, Any],
    series_slug: str,
) -> Event:
    """
    Build an iCalendar Event for a single race session.
    
    Args:
        session: Parsed YAML session block (type, start, duration_minutes).
        round_info: Parent round info (name, circuit, location, tz).
        series_slug: Lowercase series identifier (e.g. "f1") used in UIDs.
    
    Returns:
        An icalendar.Event with DTSTART;TZID set and a stable UID.
    """
    pass
```

### Code Organization
- Keep functions focused and single-purpose
- Maximum function length: ~50 lines (guideline, not strict)
- Use helper functions to break down complex logic
- Group related functionality in modules
- Keep modules focused on a single responsibility

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Use try/except blocks appropriately
- Don't catch generic `Exception` unless necessary
- Log errors appropriately

### Comments
- Write self-documenting code (prefer clear code over comments)
- Use comments to explain "why", not "what"
- Keep comments up-to-date with code changes
- Use inline comments sparingly

## File Organization

### Module Structure
```python
"""Module docstring describing the module's purpose."""

from pathlib import Path
from typing import Dict, List

import yaml
from icalendar import Calendar

from generate import write_ics

DEFAULT_DURATION_MINUTES = 60

class SeriesCalendar:
    """Class docstring."""
    pass

def load_series(yaml_path: Path) -> Dict:
    """Function docstring."""
    pass

if __name__ == "__main__":
    main()
```

## Best Practices

### General
- Write readable, maintainable code
- Prefer explicit over implicit
- Follow DRY (Don't Repeat Yourself) principle
- Use meaningful variable names
- Keep functions small and focused

### Performance
- Profile before optimizing
- Use appropriate data structures
- Consider time/space complexity
- Cache expensive operations when appropriate

### Security
- Validate user input
- Use parameterized queries for database operations
- Don't expose sensitive information in logs
- Follow principle of least privilege

### Testing
- Write testable code
- Keep business logic separate from I/O
- Use dependency injection where appropriate
- Mock external dependencies in tests

## Tools

### Formatters
- **Black**: Code formatter (use default settings)
- Run: `python scripts/format.py`

### Linters
- **flake8**: Style guide enforcement
- **pylint**: Additional code quality checks
- **mypy**: Static type checking
- Run: `python scripts/lint.py`

### Pre-commit
- Consider setting up pre-commit hooks
- Run linters and formatters before commits
- Ensure tests pass before committing

