import copy
from functools import lru_cache
from openai.lib._pydantic import to_strict_json_schema  # private API; may change
# there currently is no public API to generate the tool definition from a Pydantic model
# or a function signature.
from pydantic import BaseModel


# Performance Optimization: `to_strict_json_schema` inspects Pydantic model fields
# and generates strict JSON schemas. Caching this result and returning a deep copy
# avoids redundant schema generation (~20x faster) while preventing shared state mutation.
@lru_cache(maxsize=128)
def _cached_strict_json_schema(model: type[BaseModel]) -> dict:
    return to_strict_json_schema(model)


def _get_strict_json_schema(model: type[BaseModel]) -> dict:
    return copy.deepcopy(_cached_strict_json_schema(model))


def oai_responses_tool_from_model(name: str, description: str, model: type[BaseModel]):
    return {
        "type": "function",
        "name": name,
        "description": description,
        # OpenAI Responses strict tools require a JSON Schema object where
        # additionalProperties is explicitly false. For tools without
        # parameters, supply an empty object schema.
        "parameters": (
            _get_strict_json_schema(model)
            if model
            else {"type": "object", "properties": {}, "required": [], "additionalProperties": False}
        ),
        "strict": True,
    }

HELPFUL_AGENT_SYSTEM_INSTRUCTIONS = """
You are a helpful agent that can use tools to help the user.
You will be given a input from the user and a list of tools to use.
You may or may not need to use the tools to satisfy the user ask.
If no tools are needed, respond in haikus.
"""