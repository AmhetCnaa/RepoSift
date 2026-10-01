from pathlib import Path

import tiktoken


def count_tokens(text: str, model_encoding: str = "cl100k_base") -> int:
    try:
        encoding = tiktoken.get_encoding(model_encoding)
        return len(encoding.encode(text))
    except (ValueError, KeyError):
        # Fallback approximation: 1 token ~= 4 characters
        return len(text) // 4

def count_file_tokens(filepath: Path, model_encoding: str = "cl100k_base") -> int:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return count_tokens(content, model_encoding)
    except OSError:
        return 0
