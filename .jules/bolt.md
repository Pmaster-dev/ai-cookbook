## 2025-05-18 - Concurrent Payload Processing in Temporal Codecs
**Learning:** In Temporal PayloadCodec implementations (such as ClaimCheckCodec), `encode` and `decode` process sequences of payloads passed during workflow/activity serialization. Iterating sequentially with `await` introduces $O(N \cdot T)$ latency for S3 or remote storage operations.
**Action:** Use `asyncio.gather` for concurrent payload processing in custom Temporal codecs to reduce latency to $O(T)$ while maintaining strict payload order.
