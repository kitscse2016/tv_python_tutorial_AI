from app.executor import execute_python_code
from app.error_explainer import explain_error
from app.free_ai_client import ask_python_topic

def is_python_code(text: str) -> bool:
    keywords = ["def ", "print(", "for ", "while ", "if ", "import ", "="]
    return any(k in text for k in keywords)

def generate_ai_response(user_input: str) -> str:
    text = user_input.strip()

    # 1️⃣ Python code execution
    if is_python_code(text):
        output, error = execute_python_code(text)
        if error:
            return f"❌ Error:\n{error}\n\n🧠 Explanation:\n{explain_error(error)}"
        return f"✅ Output:\n{output}"

    # 2️⃣ Python topic explanation (FREE API)
    return ask_python_topic(text)
