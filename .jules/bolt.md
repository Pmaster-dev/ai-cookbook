## 2025-05-10 - Concurrent S3 Payload Encoding/Decoding in ClaimCheckCodec
**Learning:** `PayloadCodec` implementations in Temporal receive an `Iterable[Payload]` containing all activity/workflow arguments or return values. Sequential `await` in loops introduces $O(N)$ network latency for multi-payload operations.
**Action:** Always wrap multi-payload I/O operations (e.g. S3 puts/gets) in `asyncio.gather` within `encode()` and `decode()` to achieve $O(1)$ concurrent network RTTs while preserving element ordering.
