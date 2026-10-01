# reposift 🔍

[![PyPI version](https://img.shields.io/pypi/v/reposift.svg)](https://pypi.org/project/reposift/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/reposift.svg)](https://pypi.org/project/reposift/)

A high-performance repository context aggregator for Large Language Models (LLMs).

`reposift` scans your codebase, intelligently ignores bloat/binary files based on `.gitignore` and sensible defaults, calculates accurate token costs using `tiktoken`, and outputs a clean, structured Markdown file. This Markdown file can be directly copy-pasted into ChatGPT, Claude, Gemini, or other LLMs to give them full context of your project.

## Features ✨
- **Intelligent Scanning**: Respects `.gitignore` and `.reposiftignore`. Auto-skips binary files, `node_modules/`, `.git/`, and other standard bloat.
- **Accurate Token Counting**: Built-in `tiktoken` integration calculates exactly how much context your repository will consume.
- **Beautiful Terminal Dashboard**: Powered by `rich`, providing a live tree visualization, progress bars, and top-file metric summaries.
- **Flexible Outputs**: Save to a single Markdown file, copy directly to your clipboard, or export as JSON.
- **Configurable Presets**: Quickly toggle between different scanning profiles (e.g., `minimal` vs `full`).

## Installation 📦

You can install `reposift` via pip:

```bash
pip install git+https://github.com/AmhetCnaa/RepoSift.git
```

## Usage 🚀

Run `reposift` in any repository directory:

```bash
# Scan the current directory and display the dashboard
reposift

# Save the aggregated markdown to a file
reposift -o context.md

# Copy the aggregated markdown directly to your clipboard
reposift --copy

# Scan a specific directory
reposift /path/to/project

# Use a preset (e.g., 'minimal' ignores docs/ tests/ examples/)
reposift --preset minimal

# Output JSON summary instead of the dashboard
reposift --json
```

### Generated Output Format

The output is a nicely formatted Markdown document that LLMs easily understand:

```markdown
# Repository: project-name

## Directory Tree
```text
project-name
├── src
│   ├── main.py
│   └── utils.py
└── README.md
```

## Files
### `src/main.py`
```py
print("Hello world")
```
...
```

## Development

1. Clone the repository
2. Install dependencies: `pip install -e .[dev]`
3. Run tests: `pytest`
4. Lint code: `ruff check .`

## License

MIT
