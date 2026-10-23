import datetime
import platform

def get_system_status():
    """Returns the current system operational status and specs."""
    system_info = f"{platform.system()} {platform.release()}"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"System Operational | OS: {system_info} | Time: {current_time}"

def calculate_expression(expression: str):
    """Evaluates a basic mathematical expression safely."""
    try:
        allowed_chars = "0123456789+-*/(). "
        if all(c in allowed_chars for c in expression):
            return f"Result: {eval(expression)}"
        return "Error: Invalid characters in expression."
    except Exception as e:
        return f"Calculation Error: {str(e)}"
