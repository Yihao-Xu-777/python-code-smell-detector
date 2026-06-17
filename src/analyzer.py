import argparse
import ast
from pathlib import Path

from smell_rules import detect_all_smells
from report_generator import save_csv_report


def collect_python_files(target_path):
    path = Path(target_path)

    if path.is_file() and path.suffix == ".py":
        return [path]

    if path.is_dir():
        return sorted(path.rglob("*.py"))

    return []


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        tree = ast.parse(source_code)
        smells = detect_all_smells(tree)

        for smell in smells:
            smell["file"] = str(file_path)

        return smells

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return []

    except SyntaxError as error:
        print(f"Syntax error in {file_path}: {error}")
        return []


def print_report(smells):
    print("=" * 60)
    print("Python Code Smell Report")
    print("=" * 60)

    if not smells:
        print("No code smells detected.")
        return

    for smell in smells:
        print(f"File: {smell['file']}")
        print(f"[{smell['type']}] Line {smell['line']}")
        print(f"Function: {smell['function']}")
        print(f"Message: {smell['message']}")
        print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Detect code smells in Python files."
    )

    parser.add_argument(
        "target",
        help="A Python file or a folder containing Python files."
    )

    parser.add_argument(
        "--csv",
        help="Optional path to save the analysis result as a CSV file."
    )

    args = parser.parse_args()

    python_files = collect_python_files(args.target)

    if not python_files:
        print("No Python files found.")
        return

    all_smells = []

    for file_path in python_files:
        file_smells = analyze_file(file_path)
        all_smells.extend(file_smells)

    print_report(all_smells)

    if args.csv:
        save_csv_report(all_smells, args.csv)
        print(f"CSV report saved to: {args.csv}")


if __name__ == "__main__":
    main()