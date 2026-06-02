from typing import Dict, List, Optional, Tuple

from app.llm.client import LLMClient
from app.prompts.tutor import (
    CONCEPT_PROMPT,
    PROJECT_PROMPT,
    ROADMAP_PROMPT,
    SYSTEM_PROMPT,
)
from app.tools.definitions import TOOLS


class TutorService:
    def __init__(self, model: str = None):
        self.llm = LLMClient(model=model)
        self.last_tool_used: Optional[str] = None

    def chat(self, messages: List[Dict]) -> Tuple[str, Optional[str]]:
        self.last_tool_used = None
        response, tool_used = self.llm.run_agent(
            messages=messages,
            tools=TOOLS,
            tool_executor=self._execute_tool,
            system_prompt=SYSTEM_PROMPT,
        )
        self.last_tool_used = tool_used
        return response, tool_used

    def _execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        if tool_name == "generate_roadmap":
            return self.generate_roadmap(**tool_args)
        if tool_name == "explain_concept":
            return self.explain_concept(**tool_args)
        if tool_name == "recommend_projects":
            return self.recommend_projects(**tool_args)
        return f"Unknown tool: {tool_name}"

    def generate_roadmap(
        self, topic: str, level: str, goal: str, time_per_week: int
    ) -> str:
        prompt = ROADMAP_PROMPT.format(
            topic=topic,
            level=level,
            goal=goal,
            time_per_week=time_per_week,
        )
        return self.llm.chat(
            [{"role": "user", "content": prompt}],
            system_prompt=SYSTEM_PROMPT,
        )

    def explain_concept(self, concept: str, level: str) -> str:
        prompt = CONCEPT_PROMPT.format(concept=concept, level=level)
        return self.llm.chat(
            [{"role": "user", "content": prompt}],
            system_prompt=SYSTEM_PROMPT,
        )

    def recommend_projects(self, topic: str, level: str, goal: str) -> str:
        prompt = PROJECT_PROMPT.format(topic=topic, level=level, goal=goal)
        return self.llm.chat(
            [{"role": "user", "content": prompt}],
            system_prompt=SYSTEM_PROMPT,
        )
