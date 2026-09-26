## 2025-05-20 - String Formatting Micro-Optimizations in Workflows
**Learning:** In Temporal workflow endpoints (like deep research synthesis), formatting reports is a cold path dominated by network I/O and LLM model calls. Micro-optimizing string concatenation/joins yields negligible real-world gains (<1ms) compared to workflow latency (seconds/minutes).
**Action:** Focus performance optimizations on warm paths, hot loops, payload serialization, caching, or reducing network/API overheads.
