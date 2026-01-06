def explain_error(error: str) -> str:
    if "IndentationError" in error:
        return "IndentationError means spacing is incorrect. Python uses spaces to define code blocks."

    if "NameError" in error:
        return "NameError means you used a variable or function that was not defined."

    if "TypeError" in error:
        return "TypeError occurs when an operation is applied to the wrong data type."

    if "ZeroDivisionError" in error:
        return "ZeroDivisionError means you tried to divide a number by zero."

    if "SyntaxError" in error:
        return "SyntaxError means Python grammar is incorrect. Check brackets, colons, or spelling."

    return "This is a runtime error. Review the traceback carefully or ask for clarification."
