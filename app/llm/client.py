import json
from typing import Callable, Dict, List, Optional

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

    def run_agent(
        self,
        messages: List[Dict],
        tools: List[Dict],
        tool_executor: Callable[[str, Dict], str],
        system_prompt: str = None,
    ) -> tuple[str, Optional[str]]:
        formatted = []
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        formatted.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted,
            tools=tools,
            tool_choice="auto",
        )

        assistant_msg = response.choices[0].message

        if not assistant_msg.tool_calls:
            return assistant_msg.content, None

        tool_call = assistant_msg.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        tool_result = tool_executor(tool_name, tool_args)
        return tool_result, tool_name
