# Contributing to Reactive Resume Python SDK

Thank you for showing interest in contributing to the Reactive Resume Python SDK! Here is a guide to help you get started with the project.

---

## 🛠️ Development Setup

1. Fork the repository and clone it locally.
2. Initialize virtual environment and install packages in editable mode:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. Run tests to ensure everything is set up correctly:
   ```bash
   pytest
   ```

---

## 📜 Commit Standards (Conventional Commits)

This repository enforces **Conventional Commits** via GitHub Actions title checks and automated version generation using `release-please`. Your pull request titles and commit messages must conform to the following template:

```
<type>(<scope>): <description>
```

### Allowed Types:
- `feat`: A new feature (e.g. `feat(api): add export resume support`) -> Increments **Minor** version.
- `fix`: A bug fix (e.g. `fix(client): handle 404 response conversion`) -> Increments **Patch** version.
- `docs`: Documentation changes only (e.g. `docs: update setup steps in readme`).
- `style`: Code style improvements (whitespace, formatting) that do not affect functionality.
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `chore`: Maintenance tasks, dependencies updates, etc.
- `ci`: CI configuration changes.

> **Breaking Changes**: Mark breaking changes by appending a `!` after the type (e.g., `feat!(auth): change auth method signature`). This increments the **Major** version.

---

## 🚀 Quality Guidelines

Before submitting your Pull Request, make sure:
1. **Linter & Formatting Checks Pass**:
   Run `ruff` to ensure clean formatting and no linting errors:
   ```bash
   ruff check .
   ruff format .
   ```
2. **All Tests Pass**:
   ```bash
   pytest
   ```
3. **Docs are Updated**: Add/update docstrings for any new features or updates you implement.

---

Thank you for contributing! Your efforts help make this SDK better for the developer community.
