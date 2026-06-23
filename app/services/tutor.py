from typing import Dict, List, Optional, Tuple

from app.llm.client import LLMClient
from app.prompts.tutor import (
    CONCEPT_PROMPT,
    MEMORY_CONTEXT_TEMPLATE,
    PROJECT_PROMPT,
    RAG_PROMPT,
    ROADMAP_PROMPT,
    SYSTEM_PROMPT,
)
from app.tools.definitions import TOOLS
from memory.store import MemoryStore
from rag.embeddings import EmbeddingClient
from rag.vector_store import VectorStore


class TutorService:
    def __init__(self, model: str = None):
        self.llm = LLMClient(model=model)
        self.memory = MemoryStore()
        self.last_tool_used: Optional[str] = None
        self.last_retrieved_chunks: List[Dict] = []

    def _system_prompt(self) -> str:
        memories = self.memory.format_for_prompt()
        if not memories:
            return SYSTEM_PROMPT
        return SYSTEM_PROMPT + MEMORY_CONTEXT_TEMPLATE.format(memories=memories)

    def chat(self, messages: List[Dict]) -> Tuple[str, Optional[str]]:
        self.last_tool_used = None
        self.last_retrieved_chunks = []
        response, tool_used = self.llm.run_agent(
            messages=messages,
            tools=TOOLS,
            tool_executor=self._execute_tool,
            system_prompt=self._system_prompt(),
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
        if tool_name == "search_knowledge_base":
            return self.search_knowledge_base(**tool_args)
        if tool_name == "remember_about_user":
            return self.remember_about_user(**tool_args)
        return f"Unknown tool: {tool_name}"

    def remember_about_user(self, fact: str) -> str:
        self.memory.add(fact)
        return f"Got it — I'll remember that: {fact}"

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
            system_prompt=self._system_prompt(),
        )

    def explain_concept(self, concept: str, level: str) -> str:
        prompt = CONCEPT_PROMPT.format(concept=concept, level=level)
        return self.llm.chat(
            [{"role": "user", "content": prompt}],
            system_prompt=self._system_prompt(),
        )

    def recommend_projects(self, topic: str, level: str, goal: str) -> str:
        prompt = PROJECT_PROMPT.format(topic=topic, level=level, goal=goal)
        return self.llm.chat(
            [{"role": "user", "content": prompt}],
            system_prompt=self._system_prompt(),
        )

    def search_knowledge_base(self, query: str) -> str:
        store = VectorStore()
        if not store.load() or not store.chunks:
            return (
                "Your knowledge base is empty. Add documents to `rag/documents/` "
                "and run `python -m rag.build_index` to index them."
            )

        embedder = EmbeddingClient()
        query_embedding = embedder.embed_one(query)
        results = store.search(query_embedding, top_k=4)
        self.last_retrieved_chunks = results

        context = "\n\n".join(
            f"[{i + 1}] (Source: {r['source']})\n{r['text']}"
            for i, r in enumerate(results)
        )
        prompt = RAG_PROMPT.format(query=query, context=context)
        return self.llm.chat(
            [{"role": "user", "content": prompt}],
            system_prompt=self._system_prompt(),
        )
