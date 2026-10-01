from __future__ import annotations

from pathlib import Path


def generate_tree_text(files: list[Path], root_dir: Path) -> str:
    """Generate a simple text-based tree representation."""
    tree = []
    
    # Simple nested dictionary to represent tree
    fs_tree = {}
    for f in files:
        parts = f.relative_to(root_dir).parts
        current = fs_tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
            
    def render_node(node, prefix=""):
        items = list(node.items())
        for i, (name, children) in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            tree.append(prefix + connector + name)
            if children:
                child_prefix = prefix + ("    " if is_last else "│   ")
                render_node(children, child_prefix)

    tree.append(root_dir.name)
    render_node(fs_tree)
    return "\n".join(tree)


def generate_markdown(files: list[Path], root_dir: Path) -> str:
    lines = []
    lines.append(f"# Repository: {root_dir.name}")
    lines.append("")
    
    lines.append("## Directory Tree")
    lines.append("```text")
    lines.append(generate_tree_text(files, root_dir))
    lines.append("```")
    lines.append("")
    
    lines.append("## Files")
    for f in files:
        try:
            rel_path = f.relative_to(root_dir)
            lines.append(f"### `{rel_path}`")
            
            ext = f.suffix.lstrip('.')
            if not ext:
                ext = 'text'
                
            lines.append(f"```{ext}")
            with open(f, 'r', encoding='utf-8') as file_obj:
                content = file_obj.read()
                # To prevent markdown injection if a file contains ```
                content = content.replace("```", "\\`\\`\\`")
                lines.append(content)
            lines.append("```")
            lines.append("")
        except OSError as e:
            lines.append(f"*(Error reading file: {e})*")
            lines.append("")
            
    return "\n".join(lines)
