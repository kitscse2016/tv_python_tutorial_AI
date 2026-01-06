import subprocess
import tempfile
import sys
import textwrap

def execute_python_code(code: str):
    """
    Executes Python code safely in a temporary file
    Returns: output, error
    """

    # Normalize indentation
    code = textwrap.dedent(code)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False
    ) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out (possible infinite loop)."
