import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from analyzer import analyze_file


EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}

SMELL_TYPES = [
    "Long Method",
    "Too Many Parameters",
    "Deep Nesting",
    "Magic Number",
    "Broad Exception",
]


def should_skip_file(file_path):
    return any(part in EXCLUDED_DIRS for part in file_path.parts)


def collect_python_files(project_path):
    project_path = Path(project_path).resolve()

    python_files = []

    for file_path in project_path.rglob("*.py"):
        file_path = file_path.resolve()
        if not should_skip_file(file_path):
            python_files.append(file_path)

    return sorted(python_files)


def count_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return sum(1 for _ in file)
    except UnicodeDecodeError:
        return 0


def make_relative_path(file_path):
    file_path = Path(file_path).resolve()

    try:
        return str(file_path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(file_path)


def evaluate_project(project_path):
    project_path = Path(project_path).resolve()
    project_name = project_path.name

    python_files = collect_python_files(project_path)

    all_smells = []
    total_loc = 0

    for file_path in python_files:
        total_loc += count_lines(file_path)
        smells = analyze_file(file_path)

        for smell in smells:
            smell["project"] = project_name
            smell["file"] = make_relative_path(file_path)

        all_smells.extend(smells)

    smell_counts = {smell_type: 0 for smell_type in SMELL_TYPES}

    for smell in all_smells:
        smell_type = smell.get("type")
        if smell_type in smell_counts:
            smell_counts[smell_type] += 1

    total_smells = len(all_smells)
    kloc = total_loc / 1000 if total_loc > 0 else 0
    smells_per_kloc = round(total_smells / kloc, 2) if kloc > 0 else 0

    summary = {
        "project": project_name,
        "files_analyzed": len(python_files),
        "loc": total_loc,
        "total_smells": total_smells,
        "smells_per_kloc": smells_per_kloc,
    }

    for smell_type in SMELL_TYPES:
        column_name = smell_type.lower().replace(" ", "_")
        summary[column_name] = smell_counts[smell_type]

    return summary, all_smells


def get_projects(projects_root):
    projects_root = Path(projects_root).resolve()

    if not projects_root.exists():
        return []

    projects = []

    for path in projects_root.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            projects.append(path.resolve())

    return sorted(projects)


def write_summary_csv(summaries, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not summaries:
        print("No project summaries to write.")
        return

    fieldnames = list(summaries[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)


def write_details_csv(smells, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["project", "file", "type", "function", "line", "message"]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for smell in smells:
            writer.writerow({
                "project": smell.get("project"),
                "file": smell.get("file"),
                "type": smell.get("type"),
                "function": smell.get("function"),
                "line": smell.get("line"),
                "message": smell.get("message"),
            })


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate code smells across multiple Python projects."
    )

    parser.add_argument(
        "--projects-root",
        default="evaluation_projects",
        help="Folder containing local Python projects for evaluation."
    )

    parser.add_argument(
        "--summary-output",
        default="results/tables/open_source_summary.csv",
        help="Path to save project-level summary results."
    )

    parser.add_argument(
        "--details-output",
        default="results/tables/open_source_smell_details.csv",
        help="Path to save detailed code smell results."
    )

    args = parser.parse_args()

    projects = get_projects(args.projects_root)

    if not projects:
        print("No projects found for evaluation.")
        print("Please clone or place Python projects inside evaluation_projects/.")
        return

    all_summaries = []
    all_smells = []

    for project_path in projects:
        print(f"Evaluating project: {project_path.name}")
        summary, smells = evaluate_project(project_path)
        all_summaries.append(summary)
        all_smells.extend(smells)

    write_summary_csv(all_summaries, args.summary_output)
    write_details_csv(all_smells, args.details_output)

    print(f"Summary saved to: {args.summary_output}")
    print(f"Details saved to: {args.details_output}")


if __name__ == "__main__":
    main()