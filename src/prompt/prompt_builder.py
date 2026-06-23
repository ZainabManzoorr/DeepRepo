class PromptBuilder:

    def build(self, query: str, chunks: list):

        context = "\n\n".join(
            [
                f"FILE: {c['file']}\n"
                f"FUNCTION: {c.get('function','')}\n"
                f"CODE:\n{c['chunk']}"
                for c in chunks
            ]
        )

        prompt = f"""
You are a senior software engineer analyzing a codebase.

You MUST follow these rules:
- Use ONLY the provided code context
- If context is insufficient, say: "Not found in provided codebase"
- Do NOT hallucinate functions or files
- Be precise and technical

---

CODE CONTEXT:
{context}

---

QUESTION:
{query}

---

ANSWER FORMAT:

1. Short Explanation
2. Files Involved
3. Step-by-step Logic
4. Important Code Snippets (if needed)
"""

        return prompt