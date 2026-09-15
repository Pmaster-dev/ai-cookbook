"""Tests for helpers/tool_helpers.py — oai_responses_tool_from_model."""

from pydantic import BaseModel, Field

from helpers.tool_helpers import oai_responses_tool_from_model, _cached_strict_json_schema


class _SampleModel(BaseModel):
    state: str = Field(description="A US state code")


class TestOaiResponsesToolFromModel:
    def test_returns_correct_structure(self):
        result = oai_responses_tool_from_model("get_weather", "Get weather info", _SampleModel)
        assert result["type"] == "function"
        assert result["name"] == "get_weather"
        assert result["description"] == "Get weather info"
        assert result["strict"] is True
        params = result["parameters"]
        assert params["type"] == "object"
        assert "state" in params["properties"]

    def test_caching_and_mutation_safety(self):
        _cached_strict_json_schema.cache_clear()
        res1 = oai_responses_tool_from_model("get_weather", "Get weather info", _SampleModel)
        res2 = oai_responses_tool_from_model("get_weather", "Get weather info", _SampleModel)
        assert res1["parameters"] == res2["parameters"]
        assert res1["parameters"] is not res2["parameters"]  # distinct copies to prevent mutation bugs
        info = _cached_strict_json_schema.cache_info()
        assert info.hits >= 1
