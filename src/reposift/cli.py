import argparse
import json
import sys
from pathlib import Path

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.tree import Tree

from .config import PRESETS
from .formatter import generate_markdown
from .scanner import scan_repository
from .token_counter import count_file_tokens

console = Console()

def build_rich_tree(files, root_dir):
    tree = Tree(f"[bold blue]{root_dir.name}[/bold blue]")
    fs_tree = {}
    for f in files:
        parts = f.relative_to(root_dir).parts
        current = fs_tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def render_node(node, tree_node):
        for name, children in node.items():
            if children:
                branch = tree_node.add(f"[bold cyan]{name}[/bold cyan]")
                render_node(children, branch)
            else:
                tree_node.add(f"[green]{name}[/green]")
                
    render_node(fs_tree, tree)
    return tree

def main():
    parser = argparse.ArgumentParser(description="reposift - A high-performance repository context aggregator for LLMs.")
    parser.add_argument("dir", nargs="?", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("-o", "--output", help="Output markdown file path")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy output to clipboard")
    parser.add_argument("-j", "--json", action="store_true", help="Output JSON summary")
    parser.add_argument("-p", "--preset", choices=list(PRESETS.keys()), help="Configuration preset")
    
    args = parser.parse_args()
    
    root_dir = Path(args.dir).resolve()
    if not root_dir.is_dir():
        console.print(f"[bold red]Error:[/] Directory '{root_dir}' does not exist.")
        sys.exit(1)
        
    additional_ignores = []
    if args.preset:
        additional_ignores = PRESETS[args.preset]["ignore_additional"]
        
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Scanning repository...", total=None)
        files = scan_repository(root_dir, additional_ignores)
        
    if not files:
        console.print("[yellow]No suitable text files found.[/yellow]")
        sys.exit(0)
        
    file_tokens = {}
    total_tokens = 0
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Counting tokens...", total=len(files))
        for f in files:
            tokens = count_file_tokens(f)
            file_tokens[f] = tokens
            total_tokens += tokens
            progress.advance(task)
            
    markdown_content = generate_markdown(files, root_dir)
    
    if args.json:
        summary = {
            "total_files": len(files),
            "total_tokens": total_tokens,
            "files": [
                {"path": str(f.relative_to(root_dir)), "tokens": file_tokens[f]}
                for f in files
            ]
        }
        print(json.dumps(summary, indent=2))
        return

    # Display Dashboard
    console.print(Panel(f"[bold]reposift Summary[/bold]\nRepository: {root_dir}", border_style="blue"))
    console.print(build_rich_tree(files, root_dir))
    
    table = Table(title="Top 5 Largest Files", show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Tokens", justify="right", style="green")
    
    sorted_files = sorted(file_tokens.items(), key=lambda x: x[1], reverse=True)[:5]
    for f, tokens in sorted_files:
        table.add_row(str(f.relative_to(root_dir)), f"{tokens:,}")
        
    console.print(table)
    console.print(f"\n[bold]Total Files:[/] {len(files)}")
    console.print(f"[bold]Total Tokens:[/] {total_tokens:,}")
    
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(markdown_content, encoding='utf-8')
        console.print(f"\n[bold green]Success:[/] Saved to {out_path}")
        
    if args.copy:
        try:
            pyperclip.copy(markdown_content)
            console.print("\n[bold green]Success:[/] Copied to clipboard!")
        except pyperclip.PyperclipException as e:
            console.print(f"\n[bold red]Error:[/] Failed to copy to clipboard: {e}")
            
    if not args.output and not args.copy:
        console.print("\n[dim]Note: Use -o <file> to save output, or -c to copy to clipboard.[/dim]")

if __name__ == "__main__":
    main()
