import ast
import operator

# Define allowed operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def evaluate_constant_expr(node):
    """Recursively evaluates constant expressions while keeping variables."""
    if isinstance(node, ast.BinOp):
        left = evaluate_constant_expr(node.left)
        right = evaluate_constant_expr(node.right)
        
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return OPERATORS[type(node.op)](left, right)
        else:
            return f"({left} {ast.dump(node.op)[4]} {right})"
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Name):
        return node.id
    return node

def constant_fold(expression):
    """Parses and optimizes an expression using constant folding."""
    tree = ast.parse(expression, mode='eval')
    optimized_expr = evaluate_constant_expr(tree.body)
    return optimized_expr if isinstance(optimized_expr, str) else str(optimized_expr)

# Sample test cases
expressions = [
    "5 + x - 3 * 2",
    "2 + 3 * 4 - 1",
    "x + (3 * 5) - 2",
    "(22 / 7) * r * r"
]

for expr in expressions:
    print(f"Original: {expr}")
    print(f"Optimized: {constant_fold(expr)}\n")
