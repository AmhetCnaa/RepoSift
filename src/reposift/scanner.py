from __future__ import annotations

import os
from pathlib import Path

import pathspec

from .config import DEFAULT_IGNORE_PATTERNS


def load_ignore_patterns(root_dir: Path) -> list[str]:
    patterns = list(DEFAULT_IGNORE_PATTERNS)
    
    for ignore_file in ['.gitignore', '.reposiftignore']:
        ignore_path = root_dir / ignore_file
        if ignore_path.is_file():
            try:
                with open(ignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            patterns.append(line)
            except OSError:
                pass
                
    return patterns

def is_text_file(filepath: Path) -> bool:
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
        if b'\0' in chunk:
            return False
        chunk.decode('utf-8')
        return True
    except (UnicodeDecodeError, OSError):
        return False

def scan_repository(root_dir: Path, additional_ignores: list[str] | None = None) -> list[Path]:
    root_dir = root_dir.resolve()
    patterns = load_ignore_patterns(root_dir)
    if additional_ignores:
        patterns.extend(additional_ignores)
        
    spec = pathspec.PathSpec.from_lines('gitignore', patterns)
    
    found_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # We need to filter dirnames in-place to avoid walking ignored directories
        rel_dir = Path(dirpath).relative_to(root_dir)
        
        # Filter directories
        dirnames[:] = [
            d for d in dirnames
            if not spec.match_file(str(rel_dir / d) + '/')
        ]
        
        for filename in filenames:
            rel_file = rel_dir / filename
            if not spec.match_file(str(rel_file)):
                full_path = Path(dirpath) / filename
                if full_path.is_file() and is_text_file(full_path):
                    found_files.append(full_path)
                    
    return sorted(found_files)
