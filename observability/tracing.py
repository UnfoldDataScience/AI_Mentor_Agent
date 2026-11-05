import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional

from dotenv import load_dotenv
from langfuse import get_client, propagate_attributes
from langfuse.langchain import CallbackHandler

load_dotenv()

TRACING_ENABLED = bool(
    os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
)

if not TRACING_ENABLED:
    os.environ["LANGFUSE_TRACING_ENABLED"] = "false"
    logging.getLogger("langfuse").setLevel(logging.ERROR)


@contextmanager
def trace_turn(name: str, session_id: str, user_input: Any) -> Iterator[Any]:
    with get_client().start_as_current_observation(
        name=name, as_type="agent", input=user_input
    ) as span:
        with propagate_attributes(trace_name=name, session_id=session_id):
            yield span


@contextmanager
def trace_tool(name: str, args: Dict) -> Iterator[Any]:
    with get_client().start_as_current_observation(
        name=name, as_type="tool", input=args
    ) as span:
        yield span


@contextmanager
def trace_llm_call(name: str, as_type: str, model: str, llm_input: Any) -> Iterator[Any]:
    with get_client().start_as_current_observation(
        name=name, as_type=as_type, model=model, input=llm_input
    ) as span:
        yield span


def mark_error(message: str) -> None:
    get_client().update_current_span(level="ERROR", status_message=message)


def graph_callbacks() -> List[CallbackHandler]:
    return [CallbackHandler()]


def current_trace_url() -> Optional[str]:
    try:
        return get_client().get_trace_url()
    except Exception:
        return None
