from typing import Annotated, Callable, Dict, List, Tuple, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

RECURSION_LIMIT = 15


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class TutorGraph:
    def __init__(
        self,
        model: str,
        tools: List[Dict],
        tool_executor: Callable[[str, Dict], str],
    ):
        self.tool_executor = tool_executor
        self.llm = ChatOpenAI(model=model).bind_tools(tools)
        self.graph = self._build_graph()

    def _agent_node(self, state: AgentState) -> Dict:
        response = self.llm.invoke(state["messages"])
        return {"messages": [response]}

    def _tool_node(self, state: AgentState) -> Dict:
        last_message = state["messages"][-1]
        results = []
        for tool_call in last_message.tool_calls:
            output = self.tool_executor(tool_call["name"], tool_call["args"])
            results.append(
                ToolMessage(
                    content=output,
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )
        return {"messages": results}

    def _should_continue(self, state: AgentState) -> str:
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "tools"
        return END

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("agent", self._agent_node)
        graph.add_node("tools", self._tool_node)
        graph.set_entry_point("agent")
        graph.add_conditional_edges(
            "agent", self._should_continue, {"tools": "tools", END: END}
        )
        graph.add_edge("tools", "agent")
        return graph.compile()

    def run(self, messages: List[Dict], system_prompt: str) -> Tuple[str, List[str]]:
        lc_messages = [SystemMessage(content=system_prompt)]
        for message in messages:
            if message["role"] == "user":
                lc_messages.append(HumanMessage(content=message["content"]))
            elif message["role"] == "assistant":
                lc_messages.append(AIMessage(content=message["content"]))

        final_state = self.graph.invoke(
            {"messages": lc_messages},
            config={"recursion_limit": RECURSION_LIMIT},
        )

        tools_used = [
            message.name
            for message in final_state["messages"]
            if isinstance(message, ToolMessage)
        ]
        final_text = final_state["messages"][-1].content
        return final_text, tools_used
