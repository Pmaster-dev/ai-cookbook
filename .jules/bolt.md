## 2025-02-18 - Concurrent Payload Processing in Temporal Codecs
**Learning:** Temporal payload codecs like `ClaimCheckCodec` receive iterables of payloads (e.g. for workflow/activity arguments and returns). Awaiting remote storage operations (e.g. S3 uploads/downloads) sequentially in a `for` loop causes O(N * RTT) latency. Parallelizing with `asyncio.gather` preserves payload order while reducing batch execution time to O(RTT).
**Action:** Always check payload codecs and custom converters for sequential async I/O loops and replace with `asyncio.gather`.
