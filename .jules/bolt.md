## 2025-05-10 - Pre-compiling Regex Patterns in Pydantic Field Validators
**Learning:** Calling `re.match` or `re.search` repeatedly inside Pydantic field validators with raw string patterns incurs regex lookup/compilation overhead per field execution.
**Action:** Module-level pre-compiled regex objects (`re.compile(...)`) should be used for validation logic executed repeatedly during data cleaning or model parsing workflows.
