# Contributing to Pydantic AI Claude Code

Thank you for your interest in contributing to Pydantic AI Claude Code! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Quality Standards](#code-quality-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Documentation](#documentation)

## Code of Conduct

This project follows a professional, respectful, and inclusive approach. Please:

- Be respectful and constructive in discussions
- Focus on technical merit and project goals
- Help create a welcoming environment for all contributors

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Claude Code CLI](https://claude.com/claude-code) installed and authenticated
- [Node.js/npm](https://nodejs.org/) for sandbox-runtime installation
- [uv](https://github.com/astral-sh/uv) (recommended) or pip for package management

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pydantic_ai_claude_code.git
   cd pydantic_ai_claude_code
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/wehnsdaefflae/pydantic_ai_claude_code.git
   ```

## Development Setup

### Using uv (Recommended)

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package with dev dependencies
uv pip install -e .
uv pip install pytest pytest-asyncio pytest-rerunfailures pytest-cov ruff mypy pylint

# Install sandbox-runtime
npm install -g @anthropic-ai/sandbox-runtime
# Or with bun:
bun i -g @anthropic-ai/sandbox-runtime
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install package in editable mode with dependencies
pip install -e .
pip install pytest pytest-asyncio pytest-rerunfailures pytest-cov ruff mypy pylint

# Install sandbox-runtime
npm install -g @anthropic-ai/sandbox-runtime
```

### Verify Installation

```bash
# Verify sandbox-runtime is installed
srt --version

# Run tests to ensure everything works
pytest tests/ -v
```

## Code Quality Standards

This project maintains high code quality standards. All contributions must pass the following checks:

### Linting with Ruff

```bash
# Check for linting issues
ruff check .

# Auto-fix issues where possible
ruff check --fix .

# Format code
ruff format .
```

**Configuration**: See `[tool.ruff]` in `pyproject.toml`

**Key Rules**:
- Maximum line length: 88 characters
- Maximum statements per function: 30
- Maximum branches per function: 12
- Maximum return statements: 6
- Maximum function arguments: 5

### Type Checking with MyPy

```bash
# Run type checking
mypy src/pydantic_ai_claude_code
```

**Configuration**: See `[tool.mypy]` in `pyproject.toml`

**Requirements**:
- Strict mode enabled
- All functions must have type annotations
- No `Any` types without justification
- All errors must be resolved (no `type: ignore` unless absolutely necessary)

### Additional Checks with Pylint

```bash
# Run pylint
pylint src/pydantic_ai_claude_code
```

**Target Score**: ≥9.5/10

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/pydantic_ai_claude_code --cov-report=html

# Run specific test file
pytest tests/test_core_modules.py -v

# Run specific test
pytest tests/test_core_modules.py::TestDebugSaver::test_debug_counter_thread_safety -xvs
```

### Writing Tests

1. **Test Organization**:
   - Place unit tests in `tests/`
   - Group related tests in classes (e.g., `TestDebugSaver`)
   - Use descriptive test names: `test_<what>_<expected_behavior>`

2. **Test Structure**:
   ```python
   def test_feature_does_expected_thing(self, tmp_path):
       """Test that feature correctly handles X when Y."""
       # Arrange
       setup_data = create_test_data()

       # Act
       result = function_under_test(setup_data)

       # Assert
       assert result.expected_property == expected_value
   ```

3. **Test Coverage Requirements**:
   - New features must include tests
   - Bug fixes should include regression tests
   - Aim for >80% code coverage
   - Critical paths (error handling, security) need comprehensive coverage

4. **Thread-Safety Tests**:
   - Use actual `threading.Thread` for concurrency tests
   - Verify no race conditions with 10+ concurrent threads
   - Test both unique value assignment and correct pairing

### Test Categories

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test interaction between components
- **Thread-Safety Tests**: Verify concurrent behavior
- **Regression Tests**: Prevent previously fixed bugs from returning

## Pull Request Process

### Before Submitting

1. **Sync with Upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run All Quality Checks**:
   ```bash
   # Linting
   ruff check .
   ruff format --check .

   # Type checking
   mypy src/pydantic_ai_claude_code

   # Tests
   pytest
   ```

3. **Update Documentation**:
   - Add/update docstrings for new/modified functions
   - Update README.md if adding features
   - Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format

### Creating a Pull Request

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make Your Changes**:
   - Write clean, well-documented code
   - Follow existing code style and patterns
   - Add/update tests
   - Update relevant documentation

3. **Commit Your Changes**:
   - Follow commit message guidelines (see below)
   - Make atomic commits (one logical change per commit)

4. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   - Go to GitHub and create a Pull Request
   - Fill out the PR template completely
   - Link related issues

### PR Title Format

Use conventional commit format:

- `feat: add support for custom timeout configuration`
- `fix: resolve thread-safety issue in debug counter`
- `docs: improve README examples for streaming`
- `test: add thread-safety tests for debug counter`
- `refactor: extract helper functions in retry logic`
- `chore: update dependencies`

### PR Description Template

```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- List of changes made
- Organized by category if multiple areas affected

## Testing
- Description of tests added/modified
- Manual testing performed
- Edge cases considered

## Related Issues
Fixes #123
Related to #456

## Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented if unavoidable)
```

## Commit Message Guidelines

### Format

```
<type>: <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding/updating tests
- `refactor`: Code restructuring without behavior change
- `perf`: Performance improvements
- `chore`: Build process, dependencies, tooling

### Subject

- Use imperative mood: "add feature" not "added feature"
- Don't capitalize first letter
- No period at the end
- Maximum 72 characters

### Body (Optional)

- Explain what and why, not how
- Wrap at 72 characters
- Separate from subject with blank line

### Footer (Optional)

- Reference issues: `Fixes #123`, `Related to #456`
- Document breaking changes: `BREAKING CHANGE: description`

### Example

```
fix: resolve thread-safety issue in debug counter

The global _debug_counter had a race condition in concurrent environments
where multiple threads could increment the counter between a prompt save
and its corresponding response save.

Implemented thread-safe solution:
- Added threading.Lock to protect counter increment
- Store counter value in settings['__debug_counter']
- Read counter from settings in save_response_debug

This ensures each prompt-response pair uses the same counter value, even
when multiple threads are creating debug files concurrently.

Fixes #789
```

## Documentation

### Docstring Style

Use Google-style docstrings:

```python
def calculate_wait_time(reset_time_str: str) -> int:
    """
    Calculate seconds to wait until rate limit resets.

    Parses a time string like "3PM" or "11AM" and calculates how many
    seconds to wait from now until that time. If the time is in the past
    today, adds 24 hours.

    Parameters:
        reset_time_str (str): Time in 12-hour format, e.g. "3PM", "11AM"

    Returns:
        int: Number of seconds to wait. Includes 1-minute buffer.
             Returns 300 (5 minutes) if time cannot be parsed.

    Raises:
        ValueError: If reset_time_str format is invalid
    """
```

### README Updates

When adding features:

1. Add to relevant section or create new section
2. Include working code examples
3. Explain benefits and use cases
4. Update table of contents if needed

### CHANGELOG Updates

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

### Added
- Thread-safe debug counter with settings-based pairing

### Fixed
- Race condition in debug file counter assignment

### Changed
- Debug counter now uses threading.Lock for synchronization
```

## Architecture Patterns

### Error Handling

- Use specific exception types
- Provide clear error messages
- Include recovery instructions where applicable
- Chain exceptions with `raise ... from e`

### Async/Sync Compatibility

- Provide both sync and async versions of public APIs
- Use `asyncio.run()` carefully (check if loop is already running)
- Test both execution paths

### Type Safety

- Use TypedDict for configuration dictionaries
- Avoid `Any` unless necessary
- Use `cast()` instead of `type: ignore` when safe
- Document why type narrowing isn't possible

### Thread Safety

- Use `threading.Lock` for shared mutable state
- Document thread-safety guarantees in docstrings
- Test with 10+ concurrent threads

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue with reproduction steps
- **Security**: Email maintainers privately (see SECURITY.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant changes
- README.md for major features
- GitHub contributor graphs

Thank you for contributing to Pydantic AI Claude Code!
