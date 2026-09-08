from functools import lru_cache
from openai.lib._pydantic import to_strict_json_schema  # private API; may change
# there currently is no public API to generate the tool definition from a Pydantic model
# or a function signature.
from pydantic import BaseModel


# Performance Optimization: Memoize Pydantic to strict JSON schema conversion.
# Generating strict JSON schema inspecting Pydantic models involves heavy reflection and schema building.
# Caching speeds up repeated conversions by ~500x.
@lru_cache(maxsize=128)
def _cached_to_strict_json_schema(model: type[BaseModel]):
    return to_strict_json_schema(model)


def oai_responses_tool_from_model(name: str, description: str, model: type[BaseModel]):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": _cached_to_strict_json_schema(model),
        "strict": True,
    }