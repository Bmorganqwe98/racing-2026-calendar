# Git Guidelines

## Commit Message Format

### Structure
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, config, etc.)
- **perf**: Performance improvements

### Scope (Optional)
- Module or component name
- Examples: `generate`, `data`, `workflow`, `readme`

### Subject
- Use imperative mood ("Add feature" not "Added feature")
- First letter lowercase (unless starting with proper noun)
- No period at the end
- Maximum 50 characters (guideline)

### Body (Optional)
- Explain "what" and "why" (not "how")
- Wrap at 72 characters
- Can include multiple paragraphs
- Use bullet points for lists

### Footer (Optional)
- Reference issues: `Fixes #123`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

**Simple:**
```
feat(generate): emit VTIMEZONE blocks for all sessions
```

**With body:**
```
fix(data): correct Le Mans 24h start time

The 2026 Le Mans race start was off by an hour due to a
DST boundary in the YAML. Updated tz to Europe/Paris and
verified against fiawec.com.

Fixes #12
```

**Breaking change:**
```
feat(generate): rename UID scheme for stability

BREAKING CHANGE: Event UIDs now use
{series}-2026-r{round}-{session}@racing-cal instead of
{series}-{session}-{round}. Re-importing will dedupe
against the new UIDs; old subscribers should resubscribe.
```

## Commit Best Practices

### When to Commit
- After completing a logical unit of work
- When tests pass
- Before leaving work (WIP commits are OK)
- After fixing a bug
- After adding a feature

### What to Include
- Related changes together
- One logical change per commit
- Complete, working code
- Passing tests
- Updated documentation (if needed)

### What NOT to Include
- Broken code
- Debugging print statements
- Commented-out code
- Sensitive information (API keys, passwords)
- Large binary files
- Generated files (unless necessary)

### Commit Frequency
- Commit often (multiple times per day)
- Small, focused commits are better than large ones
- Each commit should be a complete, working state
- Use WIP commits for work in progress

## Branch Strategy

### Main Branches
- **main**: Production-ready code
  - Always in deployable state
  - Protected branch (require PR reviews)
  - Only merge via pull requests

### Supporting Branches
- **feature/**: New features
  - Branch from: `main`
  - Merge back to: `main`
  - Delete after merge

- **fix/**: Bug fixes
  - Branch from: `main`
  - Merge back to: `main`
  - Delete after merge

- **docs/**: Documentation only
  - Branch from: `main`
  - Merge back to: `main`
  - Can be fast-forward merge

### Branch Naming
- Use kebab-case
- Be descriptive but concise
- Include issue number if applicable: `feature/123-add-progress-tracking`

Examples:
- `feature/add-combined-calendar-output`
- `fix/le-mans-tz-boundary`
- `docs/update-subscribe-walkthrough`
- `feature/12-handle-tba-sessions`

## Pull Requests

### PR Title
- Follow commit message format
- Be descriptive
- Include issue number if applicable

### PR Description
- Explain what changes were made
- Explain why the changes were made
- Reference related issues
- Include testing instructions
- Note any breaking changes

Template:
```markdown
## Description
Brief description of changes

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## Breaking Changes
None (or describe breaking changes)
```

### PR Best Practices
- Keep PRs focused (one feature/fix per PR)
- Keep PRs reasonably sized (< 500 lines if possible)
- Request appropriate reviewers
- Respond to feedback promptly
- Update PR based on feedback
- Ensure CI checks pass before requesting review

## Git Workflow Commands

### Starting Work
```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/my-feature
```

### During Development
```bash
# Check status
git status

# Stage changes
git add <file>
git add .  # All changes

# Commit
git commit -m "feat: add new feature"

# Push
git push origin feature/my-feature
```

### Before Submitting PR
```bash
# Update from main
git checkout main
git pull origin main
git checkout feature/my-feature
git merge main  # or git rebase main

# Run checks
python scripts/test.py
python scripts/lint.py
python scripts/format.py

# Push updates
git push origin feature/my-feature
```

## .gitignore

Ensure these are in `.gitignore`:
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `*.pyd`
- `.Python`
- `*.so`
- `*.egg-info/`
- `dist/`
- `build/`
- `.venv/`
- `venv/`
- `env/`
- `.env`
- `*.db`
- `*.sqlite`
- `.pytest_cache/`
- `.coverage`
- `htmlcov/`
- `.mypy_cache/`
- `.idea/`
- `.vscode/`
- `*.log`

## Best Practices

### General
- Pull before starting work
- Commit often
- Write clear commit messages
- Keep commits focused
- Review your own changes before committing

### Collaboration
- Communicate about large changes
- Coordinate on shared files
- Resolve conflicts promptly
- Help teammates when stuck

### Security
- Never commit secrets or API keys
- Use environment variables for sensitive data
- Review changes before committing
- Use `.gitignore` appropriately

### History
- Don't rewrite public history
- Use `git revert` for public commits
- Keep commit history clean and meaningful
- Don't force push to shared branches

