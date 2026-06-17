import csv
from pathlib import Path


def save_csv_report(smells, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["file", "type", "function", "line", "message"]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for smell in smells:
            writer.writerow({
                "file": smell.get("file"),
                "type": smell.get("type"),
                "function": smell.get("function"),
                "line": smell.get("line"),
                "message": smell.get("message"),
            })