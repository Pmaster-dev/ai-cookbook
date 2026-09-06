## 2025-05-18 - [Avoid decorating Pydantic validator functions directly with lru_cache]
**Learning:** Decorating a validator function directly with `@functools.lru_cache` causes a runtime `TypeError: unhashable type` if unhashable arguments (e.g. `dict` or `list`) are passed during validation.
**Action:** Extract string-only or hashable argument logic into a separate helper function (e.g., `_load_class_by_path(path: str)`) and apply `@functools.lru_cache` to that helper instead.
