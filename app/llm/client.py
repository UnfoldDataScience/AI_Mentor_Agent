from typing import Dict, List

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"
OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o"]


class LLMClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model or DEFAULT_MODEL
        self.client = OpenAI()

    def chat(self, messages: List[Dict], system_prompt: str = None) -> str:
        formatted = []
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        formatted.extend(messages)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted,
        )
        return response.choices[0].message.content
