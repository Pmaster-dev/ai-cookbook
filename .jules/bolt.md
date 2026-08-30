## 2025-03-08 - Concurrent S3 Payload Encoding/Decoding in Temporal Claim Check Codec
**Learning:** Sequential async loop processing of network I/O tasks like S3 uploads/downloads in Temporal codecs creates O(N * latency) bottlenecks when handling payload lists. Using `asyncio.gather` preserves payload ordering while executing S3 I/O concurrently in O(latency).
**Action:** When implementing custom Temporal `PayloadCodec` classes or handling batch activity/workflow payloads with I/O side effects, use `asyncio.gather` to parallelize operations concurrently instead of sequential `for` loops.
