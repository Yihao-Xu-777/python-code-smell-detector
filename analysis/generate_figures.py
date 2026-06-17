import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_bar_chart(series, title, xlabel, ylabel, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    series.plot(kind="bar", ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def generate_smell_distribution(details_csv, figures_dir):
    details = pd.read_csv(details_csv)

    if details.empty:
        print("No smell details found. Skipping smell distribution figure.")
        return

    smell_counts = details["type"].value_counts()

    save_bar_chart(
        smell_counts,
        "Code Smell Distribution",
        "Code Smell Type",
        "Number of Detected Smells",
        Path(figures_dir) / "smell_distribution.png"
    )


def generate_project_total_smells(summary_csv, figures_dir):
    summary = pd.read_csv(summary_csv)

    if summary.empty:
        print("No project summary found. Skipping total smell figure.")
        return

    project_smells = summary.set_index("project")["total_smells"]

    save_bar_chart(
        project_smells,
        "Total Code Smells by Project",
        "Project",
        "Total Code Smells",
        Path(figures_dir) / "project_total_smells.png"
    )


def generate_project_smell_density(summary_csv, figures_dir):
    summary = pd.read_csv(summary_csv)

    if summary.empty:
        print("No project summary found. Skipping smell density figure.")
        return

    project_density = summary.set_index("project")["smells_per_kloc"]

    save_bar_chart(
        project_density,
        "Code Smell Density by Project",
        "Project",
        "Smells per KLOC",
        Path(figures_dir) / "project_smell_density.png"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate figures from code smell evaluation results."
    )

    parser.add_argument(
        "--summary-csv",
        default="results/tables/open_source_summary.csv",
        help="Path to the project summary CSV file."
    )

    parser.add_argument(
        "--details-csv",
        default="results/tables/open_source_smell_details.csv",
        help="Path to the detailed smell CSV file."
    )

    parser.add_argument(
        "--figures-dir",
        default="results/figures",
        help="Directory to save generated figures."
    )

    args = parser.parse_args()

    generate_smell_distribution(args.details_csv, args.figures_dir)
    generate_project_total_smells(args.summary_csv, args.figures_dir)
    generate_project_smell_density(args.summary_csv, args.figures_dir)

    print(f"Figures saved to: {args.figures_dir}")


if __name__ == "__main__":
    main()