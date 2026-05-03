# Development Workflow

## Overview
This document outlines the development workflow for this project (Python + GitHub Actions + GitHub Pages).

## Branch Strategy

### Simple Workflow
- **main**: Production-ready code
- **feature/**: Feature development branches
- **fix/**: Bug fix branches
- **docs/**: Documentation-only changes

### Branch Naming
- Feature branches: `feature/description-of-feature`
- Bug fixes: `fix/description-of-bug`
- Documentation: `docs/description-of-docs`
- Keep names short, descriptive, and kebab-case

### Workflow Steps

1. **Start New Work**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-new-feature
   ```

2. **Develop**
   - Make changes
   - Write tests
   - Run tests: `python scripts/test.py`
   - Lint code: `python scripts/lint.py`
   - Format code: `python scripts/format.py`

3. **Commit Changes**
   - Follow commit message format (see git.md)
   - Make atomic commits (one logical change per commit)
   - Commit frequently with meaningful messages

4. **Push and Create PR**
   ```bash
   git push origin feature/my-new-feature
   ```
   - Create pull request on GitHub/GitLab
   - Request review
   - Address feedback

5. **Merge**
   - After approval, merge to main
   - Delete feature branch after merge

## Development Process

### Starting a New Feature

1. **Plan**
   - Understand requirements
   - Break down into tasks
   - Consider edge cases
   - Plan tests

2. **Implement**
   - Write code following coding standards
   - Write tests alongside code (TDD preferred)
   - Ensure all tests pass
   - Update documentation

3. **Review**
   - Self-review your code
   - Run all checks (test, lint, format)
   - Ensure documentation is updated
   - Check for security issues

4. **Submit**
   - Create pull request
   - Provide clear description
   - Link related issues
   - Request appropriate reviewers

### Code Review Process

**As Author:**
- Provide clear PR description
- Explain "why" not just "what"
- Respond to feedback promptly
- Keep PRs focused and reasonably sized
- Update PR based on feedback

**As Reviewer:**
- Review within 24-48 hours if possible
- Be constructive and respectful
- Focus on code quality, not personal preferences
- Approve when satisfied, or request changes with clear feedback
- Test the changes if possible

### Testing Before Submission

Before submitting a PR, ensure:
- [ ] All tests pass: `python scripts/test.py`
- [ ] Code is linted: `python scripts/lint.py` (no errors)
- [ ] Code is formatted: `python scripts/format.py`
- [ ] Documentation is updated
- [ ] No sensitive data is committed
- [ ] Commit messages follow format

## Issue Management

### Creating Issues
- Use clear, descriptive titles
- Provide context and background
- Include steps to reproduce (for bugs)
- Label appropriately (bug, feature, enhancement, etc.)
- Link related issues/PRs

### Issue Labels
- `bug`: Something isn't working
- `feature`: New feature request
- `enhancement`: Improvement to existing feature
- `documentation`: Documentation changes
- `question`: Question or discussion
- `help wanted`: Extra attention needed

## Release Process

### Versioning
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Prepare Release**
   - Update version numbers
   - Update CHANGELOG.md
   - Ensure all tests pass
   - Update documentation

2. **Create Release Branch**
   ```bash
   git checkout -b release/v1.2.0
   ```

3. **Final Checks**
   - Run full test suite
   - Verify documentation
   - Check for security issues

4. **Tag Release**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

5. **Merge to Main**
   - Merge release branch to main
   - Push to main

## Daily Workflow

### Morning Routine
1. Pull latest changes: `git pull origin main`
2. Check for issues/PRs needing attention
3. Review any new dependencies or updates

### During Development
1. Work on assigned tasks
2. Commit frequently with clear messages
3. Run tests before committing
4. Keep code formatted and linted

### End of Day
1. Commit and push work in progress
2. Update issue status
3. Document any blockers or questions

## Communication

### Code Comments
- Use comments to explain "why", not "what"
- Keep comments up-to-date with code
- Remove commented-out code (use git history instead)

### Documentation
- Update README when adding features
- Update API docs when changing interfaces
- Keep examples current

### Team Communication
- Use clear, descriptive commit messages
- Provide context in PR descriptions
- Ask questions when unclear
- Share knowledge and findings

## Best Practices

### Code Quality
- Write tests first when possible (TDD)
- Refactor regularly
- Keep functions small and focused
- Remove dead code
- Keep dependencies up-to-date

### Git Practices
- Commit often, push regularly
- Write meaningful commit messages
- Don't commit broken code
- Use `.gitignore` appropriately
- Don't commit sensitive data

### Documentation
- Document public APIs
- Keep README current
- Update examples when APIs change
- Document design decisions

