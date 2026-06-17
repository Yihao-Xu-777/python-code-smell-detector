import ast
import sys
from smell_rules import detect_all_smells


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        tree = ast.parse(source_code)
        smells = detect_all_smells(tree)
        return smells

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return []

    except SyntaxError as error:
        print(f"Syntax error in {file_path}: {error}")
        return []


def print_report(file_path, smells):
    print("=" * 60)
    print(f"Code Smell Report for: {file_path}")
    print("=" * 60)

    if not smells:
        print("No code smells detected.")
        return

    for smell in smells:
        print(f"[{smell['type']}] Line {smell['line']}")
        print(f"Message: {smell['message']}")
        print("-" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/analyzer.py <python_file>")
        sys.exit(1)

    target_file = sys.argv[1]
    result = analyze_file(target_file)
    print_report(target_file, result)