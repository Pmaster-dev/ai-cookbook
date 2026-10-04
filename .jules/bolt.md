## 2025-05-18 - Concurrent Payload Processing in Codecs
**Learning:** `PayloadCodec` implementations (such as `ClaimCheckCodec`) that perform I/O operations (like S3 upload/download) on batches of payloads suffer from $O(N)$ sequential network latency when iterating sequentially with `await`.
**Action:** Use `asyncio.gather` for multi-payload batch processing in custom Temporal payload codecs to run network requests concurrently while preserving order.
