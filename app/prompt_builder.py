def build_prompt(user_input: str) -> str:
    return f"""
You are an expert Python assistant.
User request:
{user_input}

Respond with:
- Clean Python code if applicable
- Explanation if required
- Best practices
"""
