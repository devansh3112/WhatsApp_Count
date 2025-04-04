# Contributing to WhatsApp Chat Analyzer

Thank you for your interest in contributing to the WhatsApp Chat Analyzer project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We welcome contributions from everyone, regardless of background or experience level.

## How to Contribute

### Reporting Bugs

If you find a bug in the application, please create an issue with the following information:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Any error messages or logs
6. Your environment details (Python version, OS, etc.)

### Suggesting Enhancements

We welcome suggestions for new features or improvements. To suggest an enhancement:

1. Create an issue with a clear title
2. Describe the enhancement in detail
3. Explain why it would be valuable
4. Include any relevant examples or mockups

### Pull Requests

Follow these steps to contribute code:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Guidelines

### Setting Up the Development Environment

1. Clone your forked repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Code Style

Please follow these style guidelines:

- Use [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Include docstrings for all functions, classes, and modules
- Use meaningful variable names
- Keep functions small and focused
- Add comments for complex logic

### Testing

- Add tests for any new functionality
- Ensure all tests pass before submitting a pull request
- Test with different types of WhatsApp chat exports

## Documentation

When adding new features, please also update the relevant documentation:

- Update the README.md if needed
- Add or modify documentation in the docs/ directory
- Include example usage when applicable

## Commit Messages

- Use clear, descriptive commit messages
- Begin with a short summary (50 chars or less)
- Reference issue numbers if applicable

Example:
```
Add emoji frequency visualization (#42)

- Implements bar chart for top emojis
- Adds sorting options for emoji count
- Updates documentation with example
```

## Versioning

We use [Semantic Versioning](https://semver.org/). When proposing version changes:

- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 