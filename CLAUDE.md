# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands
- Run the application: `python voice_agent.py`
- Install dependencies: `uv sync` or `pip install -r requirements.txt`
- Create distributable package: `python -m build`

## Code Style Guidelines
- **Imports**: Group imports by standard library, third-party, and local modules
- **Formatting**: Use 4-space indentation; line length should not exceed 88 characters
- **Types**: Include type hints for function parameters and return values
- **Error Handling**: Use try/except blocks with specific exception types
- **Documentation**: Use docstrings for all functions and classes
- **Naming**:
  - Functions: snake_case
  - Variables: snake_case
  - Constants: UPPER_CASE
  - Classes: CamelCase

## Project Structure
- Keep all API keys in a .env file
- Organize related functionality into separate modules as the project grows
- Add unit tests to ensure reliability when modifying audio processing code