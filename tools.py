import ast
import datetime
import operator
import platform


def get_system_status():
    """Returns the current system operational status and specifications."""
    system_info = f"{platform.system()} {platform.release()}"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"System Operational | OS: {system_info} "
        f"| Time: {current_time}"
    )


def calculate_expression(expression: str):
    """Safely evaluates a basic mathematical expression."""

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Only numeric values are allowed.")

        if isinstance(node, ast.BinOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported mathematical operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            if abs(left) > 1e100 or abs(right) > 1e100:
                raise ValueError("Number is too large.")

            result = operation(left, right)

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported unary operator.")

            return operation(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    try:
        if not expression.strip():
            return "Error: Expression cannot be empty."

        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        return f"Result: {result}"

    except (ValueError, SyntaxError, TypeError, ZeroDivisionError, OverflowError) as error:
        return f"Calculation Error: {error}"


def get_idle_instances():
    """Returns EC2 instances with avg CPU and monthly cost (fake data for now)."""
    return [
        {"id": "i-0a1", "type": "m5.xlarge", "cpu_avg": 2, "monthly_cost": 140},
        {"id": "i-0b2", "type": "t3.small", "cpu_avg": 45, "monthly_cost": 15},
        {"id": "i-0c3", "type": "r5.2xlarge", "cpu_avg": 1, "monthly_cost": 360},
    ]
