from openai import OpenAI
from src.utils.config import MODEL_NAME


class LLM:

    def __init__(self, api_key: str):

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
        model=MODEL_NAME,                                
        messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior software engineer. "
                        "Explain code clearly using file references."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content