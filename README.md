# Python Code Smell Detector

A lightweight static analysis tool for detecting maintainability issues in Python code.

## Background

Code smells are patterns in source code that may indicate maintainability problems. Although they do not always cause bugs directly, they can make code harder to understand, test, and modify.

This project aims to build a simple Python-based static analysis tool for detecting common code smells in beginner-level Python programs.

## Detected Code Smells

The current version detects:

- Long Method
- Too Many Parameters
- Deep Nesting
- Magic Number
- Broad Exception

## Project Structure

python-code-smell-detector/
├── src/
│   ├── analyzer.py
│   └── smell_rules.py
├── examples/
│   ├── bad_code.py
│   └── clean_code.py
├── tests/
│   └── test_smell_rules.py
├── docs/
├── results/
├── README.md
└── requirements.txt

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the analyzer:

python src/analyzer.py examples/bad_code.py

Run tests:

pytest

## Example Output

[Too Many Parameters] Line 1  
Message: Function 'process_student_data' has 7 parameters.

[Magic Number] Line 9  
Message: Magic number detected: 3.14

[Broad Exception] Line 13  
Message: Broad exception handler detected: except Exception.

## Current Limitations

- The magic number rule may report some acceptable constants as code smells.
- The detector currently analyzes one Python file at a time.
- The rules are threshold-based and may need adjustment for larger projects.
- Duplicate code detection is not included in the first version.

## Future Work

- Add duplicate code detection
- Support folder-level analysis
- Generate CSV and HTML reports
- Evaluate the tool on open-source Python projects
- Add GitHub Actions for automated testing

## What I Learned

Through this project, I practiced Python abstract syntax tree analysis, rule-based static analysis, unit testing, and software engineering project organization.
