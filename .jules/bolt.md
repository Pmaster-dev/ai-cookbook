## 2025-02-18 - Concurrent S3 operations in Temporal PayloadCodec
**Learning:** `PayloadCodec.encode` and `PayloadCodec.decode` in Temporal Python receive `Iterable[Payload]` batches. Sequential `for payload in payloads:` loops with `await` create an $O(N)$ network latency bottleneck for multi-payload activity/workflow inputs and outputs.
**Action:** Use `asyncio.gather` across payloads in custom `PayloadCodec` implementations to execute remote storage calls (e.g. S3 uploads/downloads) concurrently, reducing latency to $O(1)$ round-trips.
