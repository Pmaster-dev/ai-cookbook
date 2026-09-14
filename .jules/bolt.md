## 2025-05-18 - Parallelizing Payload Codec Network I/O
**Learning:** Sequential await loops over lists of Temporal payloads during encoding/decoding introduce N+1 network latency bottlenecks in custom PayloadCodecs (such as S3 Claim Check pattern). Using `asyncio.gather` reduces batch payload processing latency from O(N * latency) to O(1 * max_latency) while maintaining payload ordering.
**Action:** When implementing custom PayloadCodecs or bulk I/O activities that process sequences of inputs/payloads, use `asyncio.gather` for concurrent network requests instead of sequential loops.
