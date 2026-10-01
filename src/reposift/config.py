DEFAULT_IGNORE_PATTERNS = [
    ".git/",
    ".svn/",
    ".hg/",
    "node_modules/",
    "__pycache__/",
    "dist/",
    "build/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".tox/",
    ".nox/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "venv/",
    ".venv/",
    "env/",
    ".env",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
    "*.log",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    "*.zip",
    "*.tar.gz",
    "*.pdf",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.ico",
    "*.svg",
    "*.mp4",
    "*.mp3",
    "*.wav"
]

PRESETS = {
    "minimal": {
        "ignore_additional": ["tests/", "docs/", "examples/"]
    },
    "full": {
        "ignore_additional": []
    }
}
