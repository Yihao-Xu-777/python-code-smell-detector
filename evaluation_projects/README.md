# Evaluation Projects

This folder is used to store local copies of Python projects for evaluation.

External repositories placed in this folder are ignored by Git and should not be committed to this repository.

To reproduce the evaluation, clone selected Python repositories into this folder and run:

```bash
python analysis/evaluate_projects.py --projects-root evaluation_projects
python analysis/generate_figures.py