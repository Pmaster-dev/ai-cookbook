## 2025-05-18 - Concurrent Payload Processing in Custom Temporal Codecs
**Learning:** Custom Temporal payload codecs (such as S3 ClaimCheckCodec) often receive lists of `Payload` objects when workflows/activities pass multiple arguments or return multiple values. Processing payloads sequentially creates sequential I/O bottlenecks ($O(N \times L)$ latency).
**Action:** Always process lists of payloads concurrently using `asyncio.gather(*[_process_one(p) for p in payloads])` to reduce latency to $O(L)$.
