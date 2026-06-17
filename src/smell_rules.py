import ast


def detect_long_method(tree, max_lines=30):
    smells = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                length = node.end_lineno - node.lineno + 1
                if length > max_lines:
                    smells.append({
                        "type": "Long Method",
                        "function": node.name,
                        "line": node.lineno,
                        "message": f"Function '{node.name}' has {length} lines."
                    })

    return smells


def detect_too_many_parameters(tree, max_params=5):
    smells = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            param_count = len(node.args.args)
            if param_count > max_params:
                smells.append({
                    "type": "Too Many Parameters",
                    "function": node.name,
                    "line": node.lineno,
                    "message": f"Function '{node.name}' has {param_count} parameters."
                })

    return smells


def detect_magic_numbers(tree):
    smells = []
    allowed_numbers = {-1, 0, 1}

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in allowed_numbers:
                smells.append({
                    "type": "Magic Number",
                    "function": None,
                    "line": getattr(node, "lineno", None),
                    "message": f"Magic number detected: {node.value}"
                })

    return smells


def detect_broad_exception(tree):
    smells = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if isinstance(node.type, ast.Name) and node.type.id == "Exception":
                smells.append({
                    "type": "Broad Exception",
                    "function": None,
                    "line": node.lineno,
                    "message": "Broad exception handler detected: except Exception."
                })

    return smells


def _get_max_nesting_level(node, current_level=0):
    max_level = current_level

    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While)):
            child_level = _get_max_nesting_level(child, current_level + 1)
        else:
            child_level = _get_max_nesting_level(child, current_level)

        max_level = max(max_level, child_level)

    return max_level


def detect_deep_nesting(tree, max_depth=3):
    smells = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            nesting_level = _get_max_nesting_level(node)
            if nesting_level > max_depth:
                smells.append({
                    "type": "Deep Nesting",
                    "function": node.name,
                    "line": node.lineno,
                    "message": f"Function '{node.name}' has nesting depth {nesting_level}."
                })

    return smells


def detect_all_smells(tree):
    smells = []
    smells.extend(detect_long_method(tree))
    smells.extend(detect_too_many_parameters(tree))
    smells.extend(detect_magic_numbers(tree))
    smells.extend(detect_broad_exception(tree))
    smells.extend(detect_deep_nesting(tree))
    return smells