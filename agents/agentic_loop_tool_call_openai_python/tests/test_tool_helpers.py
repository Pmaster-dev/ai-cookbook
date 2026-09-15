"""Tests for helpers/tool_helpers.py — oai_responses_tool_from_model."""

from pydantic import BaseModel, Field

from helpers.tool_helpers import (
    oai_responses_tool_from_model,
    _cached_strict_json_schema,
    HELPFUL_AGENT_SYSTEM_INSTRUCTIONS,
)


class _SampleModel(BaseModel):
    name: str = Field(description="A name")
    count: int = Field(description="A count")


class TestOaiResponsesToolFromModel:
    def test_with_pydantic_model(self):
        result = oai_responses_tool_from_model("my_tool", "Does something", _SampleModel)
        assert result["type"] == "function"
        assert result["name"] == "my_tool"
        assert result["description"] == "Does something"
        assert result["strict"] is True
        params = result["parameters"]
        assert params["type"] == "object"
        assert "name" in params["properties"]
        assert "count" in params["properties"]

    def test_caching_and_mutation_safety(self):
        _cached_strict_json_schema.cache_clear()
        res1 = oai_responses_tool_from_model("my_tool", "Does something", _SampleModel)
        res2 = oai_responses_tool_from_model("my_tool", "Does something", _SampleModel)
        assert res1["parameters"] == res2["parameters"]
        assert res1["parameters"] is not res2["parameters"]  # distinct copies to prevent mutation bugs
        info = _cached_strict_json_schema.cache_info()
        assert info.hits >= 1

    def test_with_none_model(self):
        result = oai_responses_tool_from_model("no_params", "No params", None)
        assert result["type"] == "function"
        assert result["name"] == "no_params"
        assert result["strict"] is True
        params = result["parameters"]
        assert params["type"] == "object"
        assert params["properties"] == {}
        assert params["additionalProperties"] is False


class TestSystemInstructions:
    def test_is_nonempty_string(self):
        assert isinstance(HELPFUL_AGENT_SYSTEM_INSTRUCTIONS, str)
        assert len(HELPFUL_AGENT_SYSTEM_INSTRUCTIONS.strip()) > 0
