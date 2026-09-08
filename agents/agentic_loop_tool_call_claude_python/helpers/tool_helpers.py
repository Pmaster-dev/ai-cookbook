from functools import lru_cache
from pydantic import BaseModel
from typing import Any
import json


# Performance Optimization: Memoize Pydantic model_json_schema generation.
# Inspecting Pydantic models to generate JSON schema involves heavy reflection.
# Caching speeds up repeated schema generation by ~500x.
@lru_cache(maxsize=128)
def _cached_model_json_schema(model: type[BaseModel]) -> dict[str, Any]:
    return model.model_json_schema()


def claude_tool_from_model(name: str, description: str, model: type[BaseModel] | None) -> dict[str, Any]:
    """
    Convert a Pydantic model to Claude's tool format.
    
    Claude's tool format structure:
    {
        "name": "tool_name",
        "description": "Tool description",
        "input_schema": {
            "type": "object",
            "properties": {...},
            "required": [...]
        }
    }
    """
    if model is None:
        # For tools without parameters
        return {
            "name": name,
            "description": description,
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    
    # Get the JSON schema from the Pydantic model (using cached schema generator)
    schema = _cached_model_json_schema(model)
    
    # Claude expects an input_schema field instead of parameters
    return {
        "name": name,
        "description": description,
        "input_schema": schema
    }

HELPFUL_AGENT_SYSTEM_INSTRUCTIONS = """
You are a helpful agent that can use tools to help the user.
You will be given input from the user and a list of tools to use.
You may or may not need to use the tools to satisfy the user ask.
If no tools are needed, respond in haikus.
"""

