import ast
import sys
from pathlib import Path

# Add src folder to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from smell_rules import (
    detect_too_many_parameters,
    detect_magic_numbers,
    detect_broad_exception,
    detect_deep_nesting,
    detect_long_method,
)


def parse_code(code):
    return ast.parse(code)


def test_too_many_parameters_detected():
    code = """
def example(a, b, c, d, e, f):
    return a + b
"""
    tree = parse_code(code)
    smells = detect_too_many_parameters(tree)

    assert len(smells) == 1
    assert smells[0]["type"] == "Too Many Parameters"


def test_magic_number_detected():
    code = """
def example():
    return 42
"""
    tree = parse_code(code)
    smells = detect_magic_numbers(tree)

    assert len(smells) == 1
    assert smells[0]["type"] == "Magic Number"


def test_broad_exception_detected():
    code = """
def example():
    try:
        risky_call()
    except Exception:
        return None
"""
    tree = parse_code(code)
    smells = detect_broad_exception(tree)

    assert len(smells) == 1
    assert smells[0]["type"] == "Broad Exception"


def test_deep_nesting_detected():
    code = """
def example(x):
    if x > 0:
        for i in range(10):
            while i > 0:
                if i == 1:
                    return i
"""
    tree = parse_code(code)
    smells = detect_deep_nesting(tree)

    assert len(smells) == 1
    assert smells[0]["type"] == "Deep Nesting"


def test_long_method_detected():
    code = """
def long_example():
    x = 0
    x += 1
    x += 2
    x += 3
    x += 4
    x += 5
    x += 6
"""
    tree = parse_code(code)
    smells = detect_long_method(tree, max_lines=5)

    assert len(smells) == 1
    assert smells[0]["type"] == "Long Method"