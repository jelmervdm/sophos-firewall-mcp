# Contributing to Sophos Firewall MCP Server

Thank you for considering contributing to `sophos-firewall-mcp`!

## Getting Started

1. Fork the repository and create a feature branch.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/sophos-firewall-mcp.git
   cd sophos-firewall-mcp
   ```
3. Set up virtual environment and dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[router]" -r requirements-dev.txt
   ```

## Code Quality & Standards

Before submitting a pull request, ensure all checks pass:
- **Code Style**: Format code with `black` and lint with `flake8`.
- **Type Checking**: Verify type annotations with `mypy src/`.
- **Testing**: Run the full unit test suite with `pytest`.

```bash
black --check src tests
flake8 src tests
mypy src
pytest
```

## Pull Request Guidelines

- Give your PR a clear title and detailed summary.
- Add unit tests for any new tool modules or features.
- Update `CHANGELOG.md` to document major fixes or enhancements.
