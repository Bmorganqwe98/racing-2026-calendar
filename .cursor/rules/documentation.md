# Documentation Standards

## Overview
This document outlines documentation standards for this Python project. Pair it with the project-specific rule (`racing-project-context.mdc`) for the canonical file map (`README.md`, `NOTES.md`, `data/*.yaml`).

## Documentation Types

### 1. Code Documentation (Docstrings)

#### Style: Google Style
Use Google-style docstrings for all public functions, classes, and methods.

#### Format
```python
def function_name(param1: Type, param2: Optional[Type] = None) -> ReturnType:
    """
    Brief description of the function.
    
    More detailed description if needed. Can span multiple lines
    and include examples or important notes.
    
    Args:
        param1: Description of param1.
        param2: Description of param2. Defaults to None.
    
    Returns:
        Description of return value.
    
    Raises:
        ValueError: When param1 is invalid.
        TypeError: When param2 is wrong type.
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        "test-42"
    """
    pass
```

#### Class Docstrings
```python
class MyClass:
    """
    Brief description of the class.
    
    More detailed description of the class, its purpose,
    and how it's used.
    
    Attributes:
        attribute1: Description of attribute1.
        attribute2: Description of attribute2.
    
    Example:
        >>> obj = MyClass("value")
        >>> obj.process()
    """
    
    def __init__(self, value: str):
        """Initialize MyClass.
        
        Args:
            value: Initial value for the class.
        """
        self.value = value
```

#### Module Docstrings
```python
"""
Module Name

Brief description of the module's purpose.

This module provides functionality for [purpose].
It includes [key features].

Example:
    Basic usage example here.
"""
```

### 2. README Files

#### Project README
Every major component should have a README.md with:

1. **Title and Description**
   - Clear title
   - Brief description of what it does

2. **Installation**
   - Prerequisites
   - Installation steps
   - Dependencies

3. **Usage**
   - Quick start example
   - Common use cases
   - Configuration

4. **Features**
   - List of key features
   - What it can do

5. **Documentation**
   - Links to detailed docs
   - API reference
   - Examples

6. **Contributing**
   - How to contribute
   - Development setup

#### Example Structure
```markdown
# Module Name

Brief description.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from module import function
result = function()
```

## Features

- Feature 1
- Feature 2

## Documentation

See [docs/](docs/) for detailed documentation.

## Contributing

[Contributing guidelines]
```

### 3. API Documentation

#### Function Documentation
- Document all public functions
- Include parameter types and descriptions
- Document return values
- Document exceptions raised
- Include usage examples

#### Class Documentation
- Document class purpose
- Document all public methods
- Document class attributes
- Include usage examples

### 4. User Guides

#### Structure
1. **Introduction**
   - What it is
   - Who it's for
   - What you'll learn

2. **Getting Started**
   - Installation
   - Quick start
   - First steps

3. **Core Concepts**
   - Key concepts explained
   - How things work
   - Important terminology

4. **Common Tasks**
   - Step-by-step guides
   - Examples
   - Troubleshooting

5. **Advanced Topics**
   - Advanced features
   - Customization
   - Best practices

6. **Reference**
   - API reference
   - Configuration options
   - Command reference

## Documentation Best Practices

### Writing Style
- **Clear and Concise**: Get to the point
- **User-Focused**: Write for the reader
- **Examples**: Include practical examples
- **Up-to-Date**: Keep docs current with code
- **Searchable**: Use clear headings and keywords

### Code Examples
- Use real, working examples
- Keep examples simple and focused
- Show both basic and advanced usage
- Test examples to ensure they work
- Update examples when APIs change

### Formatting
- Use consistent formatting
- Use code blocks for code
- Use lists for multiple items
- Use tables for structured data
- Use diagrams when helpful

### Maintenance
- Update docs when code changes
- Remove obsolete documentation
- Fix broken links
- Keep examples current
- Review docs during code review

## Documentation Tools

### Docstring Generation
- Use tools to generate API docs from docstrings
- Keep docstrings in sync with code
- Use type hints to improve generated docs

### Markdown
- Use Markdown for README files
- Use consistent Markdown style
- Use proper heading hierarchy
- Use code fences with language tags

### Diagrams
- Use diagrams for complex concepts
- Keep diagrams simple and clear
- Update diagrams when architecture changes
- Use standard diagram formats (Mermaid, PlantUML)

## Documentation Checklist

### For New Features
- [ ] Update README if needed
- [ ] Add docstrings to public functions
- [ ] Add docstrings to classes
- [ ] Update API documentation
- [ ] Add usage examples
- [ ] Update user guide if applicable

### For Code Changes
- [ ] Update docstrings if function signature changes
- [ ] Update examples if API changes
- [ ] Update README if behavior changes
- [ ] Update user guide if workflow changes

### For Bug Fixes
- [ ] Document the bug in commit message
- [ ] Update docs if fix changes behavior
- [ ] Add note if workaround was documented

## Documentation Locations

### Project Root
- `README.md`: Main project documentation
- `CHANGELOG.md`: Version history
- `CONTRIBUTING.md`: Contribution guidelines
- `LICENSE`: License information

### Component Directories
- `data/`: One YAML file per series with the canonical schedule.
- `output/`: Generated `.ics` feeds plus `index.html` landing page (gitignored; produced by Actions).
- `.github/workflows/`: GitHub Actions deploy workflow.

### Code
- Docstrings in source files
- Inline comments for complex logic
- Type hints for better IDE support

## Examples

### Good Docstring
```python
def build_session_uid(
    series_slug: str,
    round_number: int,
    session_type: str,
) -> str:
    """
    Build a stable iCalendar UID for a single race session.

    UIDs follow `{series}-2026-r{round}-{session}@racing-cal` so that
    re-generating the .ics updates events in place rather than creating
    duplicates in subscribers' calendars.

    Args:
        series_slug: Lowercase series identifier (e.g. "f1", "wec").
        round_number: 1-based round number within the season.
        session_type: Session type (e.g. "FP1", "Qualifying", "Race").

    Returns:
        The UID string, lowercased and stripped of whitespace.

    Raises:
        ValueError: If series_slug is empty or round_number < 1.

    Example:
        >>> build_session_uid("f1", 1, "Race")
        'f1-2026-r1-race@racing-cal'
    """
    pass
```

### Good README Section
```markdown
## Usage

### Basic Example

```bash
pip install -r requirements.txt
python generate.py
# -> output/f1.ics, f2.ics, wec.ics, imsa.ics, indycar.ics, wrc.ics, racing-2026.ics, index.html
```

### Advanced Example

Regenerate after editing a YAML schedule:

```bash
# Edit a session time
$EDITOR data/f1.yaml

# Regenerate locally for a quick preview
python generate.py

# Push to deploy via GitHub Actions to GitHub Pages
git add data/f1.yaml
git commit -m "fix(data): correct Australian GP qualifying time"
git push
# Subscribed Google Calendars refresh on their next poll (~8-24h).
```
```

## Review Process

### Documentation Review
- Review docs during code review
- Check for accuracy and clarity
- Verify examples work
- Ensure completeness
- Check formatting

### Documentation Updates
- Update docs with code changes
- Keep docs in version control
- Review docs periodically
- Remove outdated information

