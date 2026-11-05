from typing import Dict, List

from openai import OpenAI

from observability.tracing import trace_llm_call

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
        with trace_llm_call("llm-call", "generation", self.model, formatted) as span:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted,
            )
            content = response.choices[0].message.content
            span.update(
                output=content,
                usage_details={
                    "input": response.usage.prompt_tokens,
                    "output": response.usage.completion_tokens,
                },
            )
        return content
