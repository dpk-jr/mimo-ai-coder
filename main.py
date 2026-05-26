#!/usr/bin/env python3
"""MiMo AI Coder CLI"""
import sys, argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent))
from src.mimo_client import MiMoClient

console = Console()
SYS = "You are a senior software engineer. Analyze codebases, suggest refactoring, generate tests, migrate between languages. Preserve behavior and explain reasoning."

def cmd_analyze(args):
    client = MiMoClient(system_prompt=SYS)
    target = Path(args.directory)
    console.print(f"\n\U0001f4ca Analyzing [bold]{target}[/bold]...\n")
    files = [f for f in target.rglob("*.py") if "__pycache__" not in str(f)][:15]
    summary = "\n---\n".join([f"File: {f}\n{f.read_text()[:1500]}" for f in files[:8]])
    with console.status("[bold green]MiMo is analyzing..."):
        result = client.analyze_json(
            f"Analyze this project. Files:\n{summary}\n\n"
            f"Return: file_count, total_loc, avg_complexity, issues (list), dependencies (list), suggestions (list)."
        )
    table = Table(title="Project Analysis")
    table.add_column("Metric", style="cyan"), table.add_column("Value", style="green")
    table.add_row("Files", str(result.get("file_count", len(files))))
    table.add_row("Total LOC", str(result.get("total_loc", "N/A")))
    table.add_row("Avg Complexity", str(result.get("avg_complexity", "N/A")))
    console.print(table)
    if result.get("issues"):
        console.print("\n\u26a0\ufe0f  Issues:")
        for i in result["issues"][:8]: console.print(f"  \u2022 {i}")
    if result.get("suggestions"):
        console.print("\n\U0001f4a1 Suggestions:")
        for s in result["suggestions"][:5]: console.print(f"  \u2022 {s}")
    console.print()

def cmd_refactor(args):
    client = MiMoClient(system_prompt=SYS)
    path = Path(args.file)
    code = path.read_text()
    console.print(f"\n\U0001f527 Refactoring [bold]{path.name}[/bold] -- {args.action}\n")
    with console.status("[bold green]Refactoring..."):
        result = client.analyze_json(
            f"Refactor this code. Action: {args.action}. {'Lines: '+args.lines if args.lines else ''} {'Name: '+args.name if args.name else ''}\n\n```\n{code}\n```\n\n"
            f"Return: refactored_code, explanation, changes_made (list)."
        )
    if result.get("refactored_code"):
        console.print(Panel(Syntax(result["refactored_code"], "python", theme="monokai"), title="Refactored"))
    console.print(f"\n\U0001f4dd {result.get('explanation','')}\n")
    for c in result.get("changes_made", []): console.print(f"  \u2705 {c}")
    console.print()

def cmd_tests(args):
    client = MiMoClient(system_prompt=SYS)
    path = Path(args.file)
    code = path.read_text()
    console.print(f"\n\U0001f9ea Generating tests for [bold]{path.name}[/bold]...\n")
    with console.status("[bold green]Writing tests..."):
        result = client.analyze_json(
            f"Generate {args.framework} tests. Include happy path, edge cases, error cases.\n\n```\n{code}\n```\n\n"
            f"Return: test_code, test_count, coverage_estimate, notes (list)."
        )
    if result.get("test_code"):
        console.print(Panel(Syntax(result["test_code"], "python", theme="monokai"), title="Tests"))
    console.print(f"  Tests: {result.get('test_count','N/A')} | Coverage: {result.get('coverage_estimate','N/A')}\n")

def cmd_migrate(args):
    client = MiMoClient(system_prompt=SYS)
    path = Path(args.file)
    code = path.read_text()
    console.print(f"\n\U0001f504 Migrating [bold]{path.name}[/bold]: {args.src} -> {args.dst}\n")
    with console.status("[bold green]Migrating..."):
        result = client.analyze_json(
            f"Migrate this {args.src} code to {args.dst}. Preserve all behavior.\n\n```\n{code}\n```\n\n"
            f"Return: migrated_code, notes (list), breaking_changes (list)."
        )
    if result.get("migrated_code"):
        lang = "typescript" if args.dst == "typescript" else args.dst
        console.print(Panel(Syntax(result["migrated_code"], lang, theme="monokai"), title=f"Migrated to {args.dst}"))
    console.print()

def main():
    parser = argparse.ArgumentParser(description="MiMo AI Coder")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("analyze"); p.add_argument("directory"); p.set_defaults(func=cmd_analyze)
    p = sub.add_parser("refactor"); p.add_argument("file"); p.add_argument("--action", default="extract-method")
    p.add_argument("--lines"); p.add_argument("--name"); p.set_defaults(func=cmd_refactor)
    p = sub.add_parser("tests"); p.add_argument("file"); p.add_argument("--framework", default="pytest"); p.set_defaults(func=cmd_tests)
    p = sub.add_parser("migrate"); p.add_argument("file"); p.add_argument("--from", dest="src", default="python")
    p.add_argument("--to", dest="dst", default="typescript"); p.set_defaults(func=cmd_migrate)
    args = parser.parse_args()
    if not args.command: parser.print_help(); return
    args.func(args)

if __name__ == "__main__": main()
